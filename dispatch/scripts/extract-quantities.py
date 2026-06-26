#!/usr/bin/env python3
"""
extract-quantities.py — Quantity pattern extraction for dispatch pipeline

Purpose:
  Extracts quantity patterns from free-text input to determine deliverable counts.
  Used by convert-input.md Phase 1B to parse user requests like:
  "Create 3 newsletters and 5 emails for the launch"

Usage:
  python squads/dispatch/scripts/extract-quantities.py --input "Create 3 newsletters and 5 emails"
  python squads/dispatch/scripts/extract-quantities.py --input-file path/to/input.txt
  python squads/dispatch/scripts/extract-quantities.py --format table --input "..."

Arguments:
  --input TEXT          Free text string to extract from
  --input-file PATH     File containing input text (alternative to --input)
  --rules PATH          Path to enrichment-rules.yaml (default: squads/dispatch/data/enrichment-rules.yaml)
  --format FORMAT       Output format: json (default) or table

Output:
  JSON with structure:
  {
    "total_deliverables": 8,
    "items": [
      {"type": "newsletter", "count": 3, "matched_text": "3 newsletters", "position": 7}
    ],
    "has_quantities": true
  }

Exit codes:
  0 — Success (even if no quantities found)
  1 — Error (missing input, file not found, invalid YAML)

Version: 1.0.0
Author: AIOS Dispatch Squad
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Fallback patterns if YAML file not found or missing section
FALLBACK_PATTERNS = [
    {'pattern': r'(\d+)\s+newsletters?', 'type': 'newsletter', 'category': 'file'},
    {'pattern': r'(\d+)\s+emails?', 'type': 'email', 'category': 'file'},
    {'pattern': r'(\d+)\s+tags?\s*(?:AC|activecampaign)?', 'type': 'tag_ac', 'category': 'resource'},
    {'pattern': r'(\d+)\s+tags?\s*(?:BH|beehiiv)?', 'type': 'tag_bh', 'category': 'resource'},
    {'pattern': r'(\d+)\s+(?:listas?|lists?)', 'type': 'list', 'category': 'resource'},
    {'pattern': r'(\d+)\s+(?:automações?|automations?)', 'type': 'automation', 'category': 'resource'},
    {'pattern': r'(\d+)\s+(?:segmentos?|segments?)', 'type': 'segment', 'category': 'resource'},
    {'pattern': r'(\d+)\s+(?:components?|componentes?)', 'type': 'component', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:agents?|agentes?)', 'type': 'agent', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:tasks?|tarefas?)', 'type': 'task', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:stories?|histórias?)', 'type': 'story', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:workflows?)', 'type': 'workflow', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:scripts?)', 'type': 'script', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:pages?|páginas?)', 'type': 'page', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:sequences?|sequências?)', 'type': 'sequence', 'category': 'file'},
    {'pattern': r'(\d+)\s+(?:posts?)', 'type': 'post', 'category': 'file'},
]

# Number words to digits mapping (EN and PT-BR)
WORD_TO_NUMBER = {
    # English
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
    'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
    # Portuguese
    'um': 1, 'uma': 1, 'dois': 2, 'duas': 2, 'três': 3, 'quatro': 4, 'cinco': 5,
    'seis': 6, 'sete': 7, 'oito': 8, 'nove': 9, 'dez': 10,
    'onze': 11, 'doze': 12, 'treze': 13, 'quatorze': 14, 'quinze': 15,
    'dezesseis': 16, 'dezessete': 17, 'dezoito': 18, 'dezenove': 19, 'vinte': 20,
}


def load_patterns_from_yaml(yaml_path: Path) -> List[Dict]:
    """Load quantity patterns from YAML file with fallback."""
    try:
        import yaml

        if not yaml_path.exists():
            print(f"Warning: {yaml_path} not found, using fallback patterns", file=sys.stderr)
            return FALLBACK_PATTERNS

        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if 'quantity_patterns' not in data:
            print(f"Warning: quantity_patterns section not found in {yaml_path}, using fallback", file=sys.stderr)
            return FALLBACK_PATTERNS

        return data['quantity_patterns']

    except ImportError:
        print("Warning: PyYAML not available, using fallback patterns", file=sys.stderr)
        return FALLBACK_PATTERNS
    except Exception as e:
        print(f"Warning: Error reading {yaml_path}: {e}, using fallback", file=sys.stderr)
        return FALLBACK_PATTERNS


def convert_word_to_number(text: str) -> str:
    """Convert number words to digits (e.g., 'three emails' -> '3 emails')."""
    text_lower = text.lower()
    for word, number in WORD_TO_NUMBER.items():
        # Match word boundaries to avoid partial matches
        text_lower = re.sub(rf'\b{word}\b', str(number), text_lower)
    return text_lower


def detect_modifiers(text: str, match_start: int, match_end: int) -> Dict[str, bool]:
    """Detect quantity modifiers like 'each', 'per', 'cada' near the match."""
    context_window = 20  # Characters before and after match
    start = max(0, match_start - context_window)
    end = min(len(text), match_end + context_window)
    context = text[start:end].lower()

    modifiers = {
        'has_each': bool(re.search(r'\b(?:each|per|cada|por)\b', context)),
        'has_multiple': bool(re.search(r'\b(?:multiple|varios|várias|many)\b', context)),
        'has_total': bool(re.search(r'\b(?:total|altogether|no total)\b', context)),
    }

    return modifiers


def extract_quantities(
    text: str,
    patterns: List[Dict]
) -> Dict:
    """
    Extract quantity patterns from text.

    Args:
        text: Input text to analyze
        patterns: List of pattern dicts with 'pattern', 'type', 'category'

    Returns:
        Dict with 'total_deliverables', 'items', 'has_quantities'
    """
    # Preprocess: convert number words to digits
    processed_text = convert_word_to_number(text)

    items = []

    for pattern_def in patterns:
        pattern = pattern_def['pattern']
        item_type = pattern_def['type']
        category = pattern_def.get('category', 'unknown')

        # Find all matches (case insensitive)
        for match in re.finditer(pattern, processed_text, re.IGNORECASE):
            count_str = match.group(1)
            count = int(count_str)
            matched_text = match.group(0)
            position = match.start()

            # Detect contextual modifiers
            modifiers = detect_modifiers(processed_text, match.start(), match.end())

            item = {
                'type': item_type,
                'count': count,
                'matched_text': matched_text,
                'position': position,
                'category': category,
            }

            # Add modifiers if present
            if any(modifiers.values()):
                item['modifiers'] = modifiers

            items.append(item)

    # Sort by position in text
    items.sort(key=lambda x: x['position'])

    # Calculate total deliverables
    total = sum(item['count'] for item in items)

    return {
        'total_deliverables': total,
        'items': items,
        'has_quantities': len(items) > 0,
    }


def format_as_table(result: Dict) -> str:
    """Format result as ASCII table."""
    if not result['has_quantities']:
        return "No quantities detected.\n"

    lines = []
    lines.append("=" * 80)
    lines.append(f"TOTAL DELIVERABLES: {result['total_deliverables']}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"{'Type':<15} {'Count':>6} {'Position':>9} {'Matched Text':<30}")
    lines.append("-" * 80)

    for item in result['items']:
        lines.append(
            f"{item['type']:<15} {item['count']:>6} {item['position']:>9} {item['matched_text']:<30}"
        )

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Extract quantity patterns from free-text input for dispatch pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract-quantities.py --input "Create 3 newsletters and 5 emails"
  python extract-quantities.py --input-file brief.txt --format table
  python extract-quantities.py --rules custom-rules.yaml --input "Build 2 agents"
        """
    )

    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--input',
        type=str,
        help='Free text string to extract from'
    )
    input_group.add_argument(
        '--input-file',
        type=Path,
        help='File containing input text'
    )

    # Configuration
    parser.add_argument(
        '--rules',
        type=Path,
        default=Path('squads/dispatch/data/enrichment-rules.yaml'),
        help='Path to enrichment-rules.yaml (default: squads/dispatch/data/enrichment-rules.yaml)'
    )

    # Output format
    parser.add_argument(
        '--format',
        choices=['json', 'table'],
        default='json',
        help='Output format: json (default) or table'
    )

    args = parser.parse_args()

    # Read input text
    try:
        if args.input:
            text = args.input
        else:
            if not args.input_file.exists():
                print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
                sys.exit(1)
            text = args.input_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    # Load patterns
    patterns = load_patterns_from_yaml(args.rules)

    # Extract quantities
    result = extract_quantities(text, patterns)

    # Output
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_as_table(result))

    sys.exit(0)


if __name__ == '__main__':
    main()
