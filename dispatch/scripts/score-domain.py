#!/usr/bin/env python3
"""
score-domain.py — Domain scoring for task routing

Purpose:
    Score task descriptions against domain registry to determine routing.
    Used by route-tasks.md Phase 2.

Usage:
    # Single task
    python score-domain.py --task "Create email sequence for product launch"

    # With custom registry
    python score-domain.py --task "Configure AC automation" --registry path/to/registry.yaml

    # Batch mode
    python score-domain.py --task-file tasks.json --format table

    # Custom threshold
    python score-domain.py --task "some task" --threshold 5

Output:
    JSON with scoring results and classification (SINGLE_DOMAIN/MULTI_DOMAIN/UNROUTABLE)

Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Stop words for EN and PT-BR
STOP_WORDS = {
    # English
    'the', 'a', 'an', 'is', 'are', 'for', 'to', 'in', 'of', 'and', 'with', 'on', 'at',
    'by', 'from', 'or', 'but', 'not', 'this', 'that', 'it', 'as', 'be', 'has', 'have',
    'was', 'were', 'do', 'does', 'did', 'will', 'would', 'can', 'could', 'should',
    'shall', 'may', 'might', 'must',
    # Portuguese
    'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das', 'em', 'no',
    'na', 'nos', 'nas', 'para', 'com', 'por', 'e', 'ou', 'que', 'se'
}

# Fallback domains (hardcoded in case yaml not found)
FALLBACK_DOMAINS = {
    'marketing_copy': {
        'triggers': {
            'primary': ['newsletter', 'email', 'copy', 'subject line', 'cta', 'headline',
                       'sales page', 'bullets', 'lead magnet'],
            'secondary': ['escrever', 'criar texto', 'conteúdo', 'persuasion', 'offer'],
            'weight_primary': 3,
            'weight_secondary': 1
        },
        'agents': {'primary': '/copy:agents:copy-chief'},
        'default_model': 'sonnet'
    },
    'automation_ac': {
        'triggers': {
            'primary': ['activecampaign', 'ac', 'tag', 'lista', 'automação', 'contato', 'automation'],
            'secondary': ['crm', 'email marketing', 'segment'],
            'weight_primary': 3,
            'weight_secondary': 1
        },
        'agents': {'primary': '@ac-automation'},
        'default_model': 'haiku'
    },
    'automation_bh': {
        'triggers': {
            'primary': ['beehiiv', 'bh', 'subscriber', 'post beehiiv', 'segmento'],
            'secondary': ['newsletter platform'],
            'weight_primary': 3,
            'weight_secondary': 1
        },
        'agents': {'primary': '@bh-automation'},
        'default_model': 'haiku'
    },
    'development': {
        'triggers': {
            'primary': ['code', 'function', 'refactor', 'bug', 'feature', 'component',
                       'API', 'endpoint', 'implement', 'script'],
            'secondary': ['class', 'method', 'module', 'package', 'import', 'test'],
            'weight_primary': 3,
            'weight_secondary': 1
        },
        'agents': {'primary': '@dev'},
        'default_model': 'haiku'
    },
    'data_engineering': {
        'triggers': {
            'primary': ['ETL', 'pipeline', 'schema', 'database', 'migration', 'data model'],
            'secondary': ['transform', 'extract', 'load', 'SQL'],
            'weight_primary': 3,
            'weight_secondary': 1
        },
        'agents': {'primary': '@data-engineer'},
        'default_model': 'sonnet'
    }
}


def load_registry(registry_path: str) -> Dict:
    """Load domain registry from YAML file, fallback to hardcoded if not found."""
    path = Path(registry_path)

    if not path.exists():
        print(f"Warning: Registry not found at {registry_path}, using fallback domains",
              file=sys.stderr)
        return {'domains': FALLBACK_DOMAINS}

    try:
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        print("Warning: PyYAML not installed, using fallback domains", file=sys.stderr)
        return {'domains': FALLBACK_DOMAINS}
    except Exception as e:
        print(f"Error loading registry: {e}, using fallback domains", file=sys.stderr)
        return {'domains': FALLBACK_DOMAINS}


def tokenize_task(task: str) -> Set[str]:
    """
    Tokenize task description for scoring.
    - Lowercase
    - Remove stop words
    - Preserve multi-word phrases by also including them
    """
    # Lowercase the entire task
    task_lower = task.lower()

    # Extract all words
    words = re.findall(r'\b\w+\b', task_lower)

    # Remove stop words but keep original sequence
    tokens = set()
    for word in words:
        if word not in STOP_WORDS:
            tokens.add(word)

    # Also add the full lowercase task for multi-word matching
    tokens.add(task_lower)

    return tokens


def match_trigger(trigger: str, tokens: Set[str], task_lower: str) -> bool:
    """
    Check if trigger matches in tokens.
    Handles both single words and multi-word phrases.
    """
    trigger_lower = trigger.lower()

    # Check if it's a multi-word trigger (contains space)
    if ' ' in trigger_lower:
        # For multi-word triggers, check if phrase exists in full task
        return trigger_lower in task_lower
    else:
        # For single-word triggers, check if word is in tokens
        return trigger_lower in tokens


def score_domain(task: str, domain_name: str, domain_config: Dict) -> Tuple[int, List[str], List[str]]:
    """
    Score a task against a single domain.

    Returns:
        (total_score, primary_hits, secondary_hits)
    """
    triggers = domain_config.get('triggers', {})
    primary_keywords = triggers.get('primary', [])
    secondary_keywords = triggers.get('secondary', [])
    weight_primary = triggers.get('weight_primary', 3)
    weight_secondary = triggers.get('weight_secondary', 1)

    # Tokenize task
    tokens = tokenize_task(task)
    task_lower = task.lower()

    # Score primary triggers
    primary_hits = []
    for keyword in primary_keywords:
        if match_trigger(keyword, tokens, task_lower):
            primary_hits.append(keyword)

    # Score secondary triggers
    secondary_hits = []
    for keyword in secondary_keywords:
        if match_trigger(keyword, tokens, task_lower):
            secondary_hits.append(keyword)

    total_score = (len(primary_hits) * weight_primary) + (len(secondary_hits) * weight_secondary)

    return total_score, primary_hits, secondary_hits


def score_task(task: str, domains: Dict, threshold: int = 3) -> Dict:
    """
    Score a task against all domains and classify.

    Returns:
        Dictionary with scoring results and classification
    """
    matches = []

    for domain_name, domain_config in domains.items():
        score, primary_hits, secondary_hits = score_domain(task, domain_name, domain_config)

        if score >= threshold:
            matches.append({
                'domain': domain_name,
                'score': score,
                'primary_hits': primary_hits,
                'secondary_hits': secondary_hits,
                'agent': domain_config.get('agents', {}).get('primary', 'unknown'),
                'model': domain_config.get('default_model', 'haiku')
            })

    # Sort matches by score (descending), then alphabetically for ties
    matches.sort(key=lambda x: (-x['score'], x['domain']))

    # Classify
    if len(matches) == 0:
        classification = 'UNROUTABLE'
        primary_domain = None
        confidence = 0
    elif len(matches) == 1:
        classification = 'SINGLE_DOMAIN'
        primary_domain = matches[0]['domain']
        confidence = matches[0]['score']
    else:
        classification = 'MULTI_DOMAIN'
        primary_domain = matches[0]['domain']
        confidence = matches[0]['score']

    return {
        'task': task,
        'primary_domain': primary_domain,
        'confidence': confidence,
        'classification': classification,
        'matches': matches,
        'is_multi_domain': classification == 'MULTI_DOMAIN'
    }


def format_table(results: List[Dict]) -> str:
    """Format results as a table."""
    lines = []
    lines.append("=" * 100)
    lines.append(f"{'Task':<40} {'Classification':<15} {'Primary Domain':<20} {'Score':<5}")
    lines.append("=" * 100)

    for result in results:
        task = result['task'][:37] + '...' if len(result['task']) > 40 else result['task']
        classification = result['classification']
        primary = result['primary_domain'] or 'N/A'
        score = str(result['confidence'])

        lines.append(f"{task:<40} {classification:<15} {primary:<20} {score:<5}")

    lines.append("=" * 100)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Score task descriptions against domain registry for routing'
    )
    parser.add_argument('--task', type=str, help='Task description string to score')
    parser.add_argument('--task-file', type=str, help='JSON file with array of task descriptions')
    parser.add_argument('--registry', type=str,
                       default='squads/dispatch/data/domain-registry.yaml',
                       help='Path to domain-registry.yaml')
    parser.add_argument('--threshold', type=int, default=3,
                       help='Minimum score to consider a match (default: 3)')
    parser.add_argument('--format', type=str, choices=['json', 'table'], default='json',
                       help='Output format')

    args = parser.parse_args()

    # Validate inputs
    if not args.task and not args.task_file:
        parser.error('Either --task or --task-file is required')
        return 1

    if args.task and args.task_file:
        parser.error('Cannot specify both --task and --task-file')
        return 1

    # Load registry
    registry = load_registry(args.registry)
    domains = registry.get('domains', {})

    if not domains:
        print("Error: No domains found in registry", file=sys.stderr)
        return 1

    # Process tasks
    if args.task:
        # Single task mode
        result = score_task(args.task, domains, args.threshold)

        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_table([result]))

    else:
        # Batch mode
        try:
            with open(args.task_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        except Exception as e:
            print(f"Error reading task file: {e}", file=sys.stderr)
            return 1

        if not isinstance(tasks, list):
            print("Error: Task file must contain a JSON array", file=sys.stderr)
            return 1

        results = []
        for task in tasks:
            if isinstance(task, str):
                results.append(score_task(task, domains, args.threshold))
            else:
                print(f"Warning: Skipping non-string task: {task}", file=sys.stderr)

        # Generate summary
        summary = {
            'total': len(results),
            'single_domain': sum(1 for r in results if r['classification'] == 'SINGLE_DOMAIN'),
            'multi_domain': sum(1 for r in results if r['classification'] == 'MULTI_DOMAIN'),
            'unroutable': sum(1 for r in results if r['classification'] == 'UNROUTABLE')
        }

        if args.format == 'json':
            output = {
                'results': results,
                'summary': summary
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print(format_table(results))
            print()
            print(f"Summary: {summary['total']} total | "
                  f"{summary['single_domain']} single | "
                  f"{summary['multi_domain']} multi | "
                  f"{summary['unroutable']} unroutable")

    return 0


if __name__ == '__main__':
    sys.exit(main())
