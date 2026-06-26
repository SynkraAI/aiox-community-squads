#!/usr/bin/env python3
"""
Auto-fix simple V1.* veto violations before dispatch.

Replaces LLM reasoning in Phase 4.5 pre-execution gate for SIMPLE auto-fixable
violations. Complex violations (V1.1, V1.7, V1.10, V1.11) require human intervention.

Usage:
  # Fix task with violations
  python scripts/auto-fix-veto.py --task-file task-with-violations.json

  # Dry run (show fixes without applying)
  python scripts/auto-fix-veto.py --task-file task.json --dry-run

  # JSON output
  python scripts/auto-fix-veto.py --task-file task.json --format json

Exit codes:
  0 = all violations auto-fixed
  1 = manual review needed (flagged fixes require human judgment)
  2 = unfixable violations remain (V1.1, V1.7, V1.10, V1.11)

Source: squads/dispatch/checklists/pre-execution-gate.md (V1.*)
Version: 1.0.0
Date: 2026-02-12
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# V1.2: Subjective criteria flag words
SUBJECTIVE_WORDS = [
    'good', 'appropriate', 'adequate', 'well-written', 'nice', 'quality', 'proper',
    'better', 'best', 'great', 'excellent', 'fine', 'perfect'
]

# V1.3: Placeholder patterns
PLACEHOLDER_PATTERNS = [
    r'\[XXX\]',
    r'\{TODO\}',
    r'\bTBD\b',
    r'\[PLACEHOLDER\]',
    r'\[INSERT[^\]]*\]',
    r'\{\{[^}]+\}\}',  # {{variable}} placeholders
]

# V1.4: Language detection
PT_INDICATORS = [
    r'\b(não|nao|também|tambem|então|entao|porque|fazer|você|voce|'
    r'criar|escrever|preciso|quero|deve|pode|como|para|com|são|'
    r'está|estão|fazer|dizer|falar|olhar|aqui|isso|este|esta)\b'
]

EN_INDICATORS = [
    r'\b(the|is|are|was|were|have|has|had|will|would|should|could|'
    r'can|must|shall|may|might|do|does|did|been|being|this|that|'
    r'these|those|which|what|where|when|how|who|whom)\b'
]

# V1.6: Vague instruction patterns
VAGUE_PATTERNS = [
    (r'\bmake it (good|nice|better|great)\b', 'MANUAL_REVIEW: Replace with specific criteria'),
    (r'\bwrite something\b', 'MANUAL_REVIEW: Specify exact content type and length'),
    (r'\bcreate content\b', 'MANUAL_REVIEW: Define content type, structure, and acceptance criteria'),
    (r'\bdo your best\b', 'MANUAL_REVIEW: Replace with measurable success criteria'),
    (r'\bbe creative\b', 'MANUAL_REVIEW: Define creative constraints and examples'),
]

# V1.9: @agent notation (should be /agent)
AGENT_NOTATION_PATTERN = r'@([a-z-]+)'


# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def detect_subjective_criteria(text: str) -> List[Tuple[str, str]]:
    """V1.2: Detect subjective quality words."""
    findings = []
    text_lower = text.lower()
    for word in SUBJECTIVE_WORDS:
        pattern = r'\b' + word + r'\b'
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            context_start = max(0, match.start() - 20)
            context_end = min(len(text), match.end() + 20)
            context = text[context_start:context_end]
            findings.append((word, context))
    return findings


def detect_placeholders(text: str) -> List[Tuple[str, str]]:
    """V1.3: Detect placeholder text."""
    findings = []
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            findings.append((match.group(), match.group()))
    return findings


def detect_language_mix(text: str) -> Dict[str, Any]:
    """V1.4: Detect EN/PT-BR mixing."""
    text_lower = text.lower()

    pt_count = sum(len(re.findall(pattern, text_lower, re.IGNORECASE)) for pattern in PT_INDICATORS)
    en_count = sum(len(re.findall(pattern, text_lower, re.IGNORECASE)) for pattern in EN_INDICATORS)

    if pt_count > 0 and en_count > 0:
        primary = 'PT-BR' if pt_count > en_count else 'EN'
        return {'mixed': True, 'primary': primary, 'pt_count': pt_count, 'en_count': en_count}

    return {'mixed': False, 'primary': None}


def detect_vague_instructions(text: str) -> List[Tuple[str, str]]:
    """V1.6: Detect vague instructions."""
    findings = []
    for pattern, suggestion in VAGUE_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            findings.append((match.group(), suggestion))
    return findings


def detect_agent_notation(text: str) -> List[str]:
    """V1.9: Detect @agent notation."""
    return re.findall(AGENT_NOTATION_PATTERN, text)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-FIX FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def fix_subjective_criteria(prompt: str) -> Tuple[str, List[Dict]]:
    """V1.2: Replace subjective words with MANUAL_REVIEW markers."""
    fixes = []
    modified = prompt

    findings = detect_subjective_criteria(prompt)
    for word, context in findings:
        replacement = f"MANUAL_REVIEW: Replace '{word}' with operational criteria (e.g., '< 500 words', 'CTA present', '3+ sections')"
        pattern = r'\b' + re.escape(word) + r'\b'

        # Replace first occurrence
        modified = re.sub(pattern, replacement, modified, count=1, flags=re.IGNORECASE)

        fixes.append({
            'veto_id': 'V1.2',
            'original': context,
            'fixed': replacement,
            'type': 'manual_review'
        })

    return modified, fixes


def fix_placeholders(prompt: str) -> Tuple[str, List[Dict]]:
    """V1.3: Remove placeholder text."""
    fixes = []
    modified = prompt

    findings = detect_placeholders(prompt)
    for placeholder, _ in findings:
        modified = modified.replace(placeholder, '')
        fixes.append({
            'veto_id': 'V1.3',
            'original': placeholder,
            'fixed': '[REMOVED]',
            'type': 'auto'
        })

    return modified, fixes


def fix_language_mix(prompt: str) -> Tuple[str, List[Dict]]:
    """V1.4: Add language directive for mixed EN/PT-BR."""
    fixes = []
    lang_info = detect_language_mix(prompt)

    if lang_info['mixed']:
        directive = f"\n\nIMPORTANT: Write ENTIRELY in {lang_info['primary']}. Do not mix languages.\n"
        modified = directive + prompt

        fixes.append({
            'veto_id': 'V1.4',
            'original': f"Mixed {lang_info['pt_count']} PT + {lang_info['en_count']} EN indicators",
            'fixed': f"Added directive: Write in {lang_info['primary']}",
            'type': 'auto'
        })
        return modified, fixes

    return prompt, fixes


def fix_missing_template(task: Dict) -> Tuple[Dict, List[Dict]]:
    """V1.5: Add output template for Haiku tasks > 50 lines."""
    fixes = []

    model = task.get('model', '')
    expected_lines = task.get('expected_lines', 0)
    prompt = task.get('prompt', '')

    if model == 'haiku' and expected_lines > 50 and '## OUTPUT STRUCTURE' not in prompt:
        template = """

## OUTPUT STRUCTURE

```
[Define the exact structure/format here]
- Section 1: ...
- Section 2: ...
- Section 3: ...
```
"""
        task['prompt'] = prompt + template

        fixes.append({
            'veto_id': 'V1.5',
            'original': f"Haiku task with {expected_lines} expected lines, no template",
            'fixed': "Added ## OUTPUT STRUCTURE section",
            'type': 'auto'
        })

    return task, fixes


def fix_vague_instructions(prompt: str) -> Tuple[str, List[Dict]]:
    """V1.6: Flag vague instructions for manual review."""
    fixes = []
    modified = prompt

    findings = detect_vague_instructions(prompt)
    for phrase, suggestion in findings:
        # Don't modify, just flag
        modified = modified.replace(phrase, f"{phrase} [{suggestion}]")
        fixes.append({
            'veto_id': 'V1.6',
            'original': phrase,
            'fixed': suggestion,
            'type': 'manual_review'
        })

    return modified, fixes


def fix_missing_output_path(task: Dict) -> Tuple[Dict, List[Dict]]:
    """V1.8: Generate default output path if missing."""
    fixes = []

    if not task.get('output_path'):
        domain = task.get('domain', 'unknown')
        task_type = task.get('task_type', 'output')
        task_id = task.get('id', 'task')

        default_path = f"Output/{domain}/{task_id}_{task_type}.md"
        task['output_path'] = default_path

        fixes.append({
            'veto_id': 'V1.8',
            'original': 'No output_path',
            'fixed': default_path,
            'type': 'auto'
        })

    return task, fixes


def fix_agent_notation(prompt: str) -> Tuple[str, List[Dict]]:
    """V1.9: Replace @agent with /agent notation."""
    fixes = []
    modified = prompt

    agents = detect_agent_notation(prompt)
    for agent in agents:
        old_notation = f"@{agent}"
        new_notation = f"/{agent}"
        modified = modified.replace(old_notation, new_notation)

        fixes.append({
            'veto_id': 'V1.9',
            'original': old_notation,
            'fixed': new_notation,
            'type': 'auto'
        })

    return modified, fixes


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AUTO-FIX ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

def auto_fix_task(task: Dict, dry_run: bool = False) -> Dict:
    """Auto-fix all simple V1.* violations."""

    all_fixes = []
    modified_task = task.copy()
    prompt = modified_task.get('prompt', '')

    # V1.2: Subjective criteria
    prompt, fixes = fix_subjective_criteria(prompt)
    all_fixes.extend(fixes)

    # V1.3: Placeholders
    prompt, fixes = fix_placeholders(prompt)
    all_fixes.extend(fixes)

    # V1.4: Language mixing
    prompt, fixes = fix_language_mix(prompt)
    all_fixes.extend(fixes)

    # V1.6: Vague instructions
    prompt, fixes = fix_vague_instructions(prompt)
    all_fixes.extend(fixes)

    # V1.9: Agent notation
    prompt, fixes = fix_agent_notation(prompt)
    all_fixes.extend(fixes)

    # Update prompt in task
    modified_task['prompt'] = prompt

    # V1.5: Missing template (operates on task dict)
    modified_task, fixes = fix_missing_template(modified_task)
    all_fixes.extend(fixes)

    # V1.8: Missing output path (operates on task dict)
    modified_task, fixes = fix_missing_output_path(modified_task)
    all_fixes.extend(fixes)

    # Check for unfixable violations
    remaining_violations = []

    # V1.1: Not atomic (unfixable)
    if task.get('deliverable_count', 0) > 1:
        remaining_violations.append('V1.1: Task not atomic (requires decomposition)')

    # V1.7: Multiple deliverables (unfixable)
    if '## DELIVERABLE' in prompt and prompt.count('## DELIVERABLE') > 1:
        remaining_violations.append('V1.7: Multiple deliverables (requires split)')

    # V1.10: Architecture task (unfixable)
    if task.get('task_type') in ['architecture', 'prd', 'design']:
        remaining_violations.append('V1.10: Architecture task (requires foreground execution)')

    # V1.11: MCP task (unfixable)
    if task.get('requires_mcp', False):
        remaining_violations.append('V1.11: MCP task (requires foreground execution)')

    # Determine exit status
    has_manual_review = any(f['type'] == 'manual_review' for f in all_fixes)
    has_unfixable = len(remaining_violations) > 0

    all_fixed = len(all_fixes) > 0 and not has_manual_review and not has_unfixable

    result = {
        'task_id': task.get('id', 'unknown'),
        'fixes_applied': all_fixes if not dry_run else [],
        'fixes_proposed': all_fixes if dry_run else [],
        'remaining_violations': remaining_violations,
        'all_fixed': all_fixed,
        'requires_manual_review': has_manual_review,
        'unfixable': has_unfixable
    }

    if not dry_run:
        result['modified_task'] = modified_task

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Auto-fix simple V1.* veto violations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/auto-fix-veto.py --task-file task.json
  python scripts/auto-fix-veto.py --task-file task.json --dry-run
  python scripts/auto-fix-veto.py --task-file task.json --format json
        """
    )

    parser.add_argument('--task-file', required=True, help='JSON file with task + violations')
    parser.add_argument('--format', choices=['json', 'report'], default='report', help='Output format')
    parser.add_argument('--dry-run', action='store_true', help='Show fixes without applying')

    args = parser.parse_args()

    # Load task
    task_path = Path(args.task_file)
    if not task_path.exists():
        print(f"Error: File not found: {args.task_file}", file=sys.stderr)
        sys.exit(2)

    with open(task_path) as f:
        task = json.load(f)

    # Run auto-fix
    result = auto_fix_task(task, dry_run=args.dry_run)

    # Output
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        # Human-readable report
        print(f"\n{'=' * 80}")
        print(f"AUTO-FIX REPORT: {result['task_id']}")
        print(f"{'=' * 80}\n")

        if result['fixes_applied'] or result['fixes_proposed']:
            fixes = result['fixes_applied'] if result['fixes_applied'] else result['fixes_proposed']
            print(f"✅ {'Applied' if not args.dry_run else 'Proposed'} {len(fixes)} fixes:\n")
            for fix in fixes:
                icon = '🔧' if fix['type'] == 'auto' else '⚠️'
                print(f"  {icon} {fix['veto_id']}: {fix['original'][:60]}...")
                print(f"     → {fix['fixed'][:60]}...")
                print()

        if result['remaining_violations']:
            print(f"\n❌ {len(result['remaining_violations'])} unfixable violations:\n")
            for violation in result['remaining_violations']:
                print(f"  • {violation}")
            print()

        if result['all_fixed']:
            print("✅ All violations fixed. Task ready for dispatch.")
        elif result['requires_manual_review']:
            print("⚠️  Manual review needed for flagged fixes.")
        elif result['unfixable']:
            print("❌ Unfixable violations remain. Human intervention required.")

        print(f"\n{'=' * 80}\n")

    # Exit code
    if result['all_fixed']:
        sys.exit(0)
    elif result['requires_manual_review']:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == '__main__':
    main()
