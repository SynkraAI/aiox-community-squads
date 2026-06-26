#!/usr/bin/env python3
"""
Validate sufficiency gate (V0.1, V0.2, V0.3) for dispatch Phase 0.

Replaces LLM reasoning with deterministic checks using regex and pattern matching.
Zero LLM needed — pure code.

Usage:
  python scripts/validate-sufficiency-gate.py --story-file plan/stories/story-name.md
  python scripts/validate-sufficiency-gate.py --story-file plan/stories/story-name.md --format report

Output (JSON default):
  {
    "passed": true,
    "score": "3/3",
    "checks": [
      {
        "id": "V0.1",
        "check": "Story has acceptance criteria",
        "result": "PASS",
        "message": "Found acceptance criteria section",
        "redirect": null
      }
    ]
  }

Exit codes:
  0 — PASS (all checks passed)
  1 — FAIL (one or more veto conditions triggered)

Source: squads/dispatch/data/veto-conditions.yaml
Version: 1.0.0
Date: 2026-02-12
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# V0.1: Acceptance criteria patterns
ACCEPTANCE_PATTERNS = [
    r'\bacceptance\s+criteria\b',
    r'\bsuccess\s+criteria\b',
    r'^##\s+(?:Acceptance\s+)?Criteria',
    r'^-\s*\[\s*\]',  # Checklist items
]

# V0.2: Deliverable type patterns
DELIVERABLE_PATTERNS = [
    r'\bemail',
    r'\bnewsletter',
    r'\bautomation',
    r'\btag',
    r'\breport',
    r'\bscript',
    r'\bpage',
    r'\bfunnel',
    r'\bsequence',
    r'\bpost',
    r'\bstory',
    r'\bworkflow',
    r'\bagent',
    r'\btask',
    r'\bcomponent',
]

# V0.3: Quantity patterns (from extract-quantities.py)
QUANTITY_PATTERNS = [
    r'(\d+)\s+newsletters?',
    r'(\d+)\s+emails?',
    r'(\d+)\s+tags?',
    r'(\d+)\s+(?:listas?|lists?)',
    r'(\d+)\s+(?:automações?|automations?)',
    r'(\d+)\s+(?:segmentos?|segments?)',
    r'(\d+)\s+(?:components?|componentes?)',
    r'(\d+)\s+(?:agents?|agentes?)',
    r'(\d+)\s+(?:tasks?|tarefas?)',
    r'(\d+)\s+(?:stories?|histórias?)',
    r'(\d+)\s+(?:workflows?)',
    r'(\d+)\s+(?:scripts?)',
    r'(\d+)\s+(?:pages?|páginas?)',
    r'(\d+)\s+(?:sequences?|sequências?)',
    r'(\d+)\s+(?:posts?)',
]


def check_v01_acceptance_criteria(content: str) -> Dict:
    """
    V0.1: Story has acceptance criteria.

    Returns:
        Dict with result, message, redirect
    """
    # Case insensitive search across multiple patterns
    for pattern in ACCEPTANCE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            return {
                'result': 'PASS',
                'message': 'Found acceptance criteria section',
                'redirect': None
            }

    return {
        'result': 'FAIL',
        'message': 'Story has no acceptance criteria',
        'redirect': '/po for acceptance criteria'
    }


def check_v02_input_length(content: str) -> Dict:
    """
    V0.2: Input >= 10 words AND mentions deliverables.

    Returns:
        Dict with result, message, redirect
    """
    # Count words (split on whitespace, filter empty)
    words = [w for w in content.split() if w.strip()]
    word_count = len(words)

    # Check if deliverables mentioned
    has_deliverables = any(
        re.search(pattern, content, re.IGNORECASE)
        for pattern in DELIVERABLE_PATTERNS
    )

    if word_count < 10 and not has_deliverables:
        return {
            'result': 'FAIL',
            'message': f'Input too short ({word_count} words) with no deliverables mentioned',
            'redirect': '/pm for scope'
        }

    return {
        'result': 'PASS',
        'message': f'Input sufficient ({word_count} words, deliverables: {has_deliverables})',
        'redirect': None
    }


def check_v03_specific_quantities(content: str) -> Dict:
    """
    V0.3: Specific quantities mentioned.

    Returns:
        Dict with result, message, redirect
    """
    # Extract quantities
    quantities_found = []

    for pattern in QUANTITY_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            quantities_found.append(match.group(0))

    if not quantities_found:
        return {
            'result': 'FAIL',
            'message': 'No specific deliverables or quantities mentioned',
            'redirect': 'ASK user for quantities'
        }

    return {
        'result': 'PASS',
        'message': f'Found {len(quantities_found)} quantity patterns: {", ".join(quantities_found[:3])}{"..." if len(quantities_found) > 3 else ""}',
        'redirect': None
    }


def validate_sufficiency(story_file: Path) -> Dict:
    """
    Run all V0.* sufficiency checks.

    Returns:
        Dict with passed, score, checks
    """
    # Read story file
    try:
        content = story_file.read_text(encoding='utf-8')
    except FileNotFoundError:
        return {
            'passed': False,
            'score': '0/3',
            'checks': [{
                'id': 'ERROR',
                'check': 'File existence',
                'result': 'FAIL',
                'message': f'Story file not found: {story_file}',
                'redirect': None
            }]
        }
    except Exception as e:
        return {
            'passed': False,
            'score': '0/3',
            'checks': [{
                'id': 'ERROR',
                'check': 'File read',
                'result': 'FAIL',
                'message': f'Error reading file: {e}',
                'redirect': None
            }]
        }

    # Run checks
    checks = [
        {
            'id': 'V0.1',
            'check': 'Story has acceptance criteria',
            **check_v01_acceptance_criteria(content)
        },
        {
            'id': 'V0.2',
            'check': 'Input >= 10 words AND mentions deliverables',
            **check_v02_input_length(content)
        },
        {
            'id': 'V0.3',
            'check': 'Specific quantities mentioned',
            **check_v03_specific_quantities(content)
        }
    ]

    # Calculate score
    passed_count = sum(1 for check in checks if check['result'] == 'PASS')
    total_count = len(checks)
    passed = passed_count == total_count

    return {
        'passed': passed,
        'score': f'{passed_count}/{total_count}',
        'checks': checks
    }


def format_as_report(result: Dict) -> str:
    """Format result as human-readable report."""
    lines = []
    lines.append("=" * 80)
    lines.append("SUFFICIENCY GATE VALIDATION (V0.1, V0.2, V0.3)")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Score: {result['score']}")
    lines.append(f"Status: {'✅ PASS' if result['passed'] else '❌ FAIL'}")
    lines.append("")
    lines.append("-" * 80)

    for check in result['checks']:
        status_icon = "✅" if check['result'] == 'PASS' else "❌"
        lines.append(f"{status_icon} {check['id']}: {check['check']}")
        lines.append(f"   {check['message']}")
        if check.get('redirect'):
            lines.append(f"   → Redirect: {check['redirect']}")
        lines.append("")

    lines.append("-" * 80)

    if result['passed']:
        lines.append("=== ALL VETO CONDITIONS PASSED ===")
    else:
        failed_count = sum(1 for c in result['checks'] if c['result'] == 'FAIL')
        lines.append(f"=== DISPATCH BLOCKED: {failed_count} veto conditions triggered ===")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate sufficiency gate (V0.1, V0.2, V0.3) for dispatch Phase 0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate-sufficiency-gate.py --story-file plan/stories/story-dispatch-smoke-test.md
  python validate-sufficiency-gate.py --story-file plan/stories/story-name.md --format report
        """
    )

    parser.add_argument(
        '--story-file',
        type=Path,
        required=True,
        help='Path to story .md file'
    )

    parser.add_argument(
        '--format',
        choices=['json', 'report'],
        default='json',
        help='Output format: json (default) or report'
    )

    args = parser.parse_args()

    # Run validation
    result = validate_sufficiency(args.story_file)

    # Output
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_as_report(result))

    # Exit code
    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
