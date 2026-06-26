#!/usr/bin/env python3
"""
Validate Haiku prompt against 14 ALWAYS/NEVER rules.

Automates the deterministic checks from haiku-prompt-checklist.md.
Pattern selection (HP-001 through HP-006) remains Sonnet work.

Usage:
  # Validate a prompt string
  python scripts/validate-haiku-prompt.py --prompt "Create INDEX.md for folder..."

  # Validate from file
  python scripts/validate-haiku-prompt.py --prompt-file enriched-prompt.md

  # Validate with metadata
  python scripts/validate-haiku-prompt.py --prompt "..." --model haiku --expected-lines 200

  # Batch validate from JSON
  python scripts/validate-haiku-prompt.py --batch prompts.json

Output (JSON):
  {
    "passed": true,
    "score": "14/14",
    "violations": [],
    "veto_ids": [],
    "warnings": []
  }

Source: squads/dispatch/checklists/haiku-prompt-checklist.md
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# Portuguese indicators (for language detection)
PT_INDICATORS = [
    r'\b(não|nao|também|tambem|então|entao|porque|fazer|você|voce|'
    r'criar|escrever|preciso|quero|deve|pode|como|para|com|são|'
    r'está|estão|fazer|dizer|falar|olhar|aqui|isso|este|esta)\b'
]

# English indicators
EN_INDICATORS = [
    r'\b(the|is|are|was|were|have|has|had|will|would|should|could|'
    r'can|must|shall|may|might|do|does|did|been|being|this|that|'
    r'these|those|which|what|where|when|how|who|whom)\b'
]

# Implicit reference patterns
IMPLICIT_PATTERNS = [
    r'continue\s+from\s+(last|previous|before)',
    r'as\s+(before|mentioned|discussed|above)',
    r'same\s+as\s+(last|previous)',
    r'like\s+the\s+(last|previous)\s+one',
    r'keep\s+going',
    r'do\s+it\s+again',
    r'repeat\s+the\s+same',
]

# Vague instruction patterns
VAGUE_PATTERNS = [
    r'make\s+it\s+(good|nice|better|great)',
    r'do\s+your\s+best',
    r'be\s+creative',
    r'something\s+like',
    r'you\s+know\s+what',
    r'figure\s+it\s+out',
    r'whatever\s+works',
]

# Multiple deliverable indicators
MULTI_DELIVERABLE_PATTERNS = [
    r'create\s+(\d+)\s+files',
    r'generate\s+(both|all)',
    r'produce\s+(\d+)\s+(?:documents|files|outputs)',
    r'write\s+(?:both|all|multiple)',
    r'output\s+to\s+\S+\s+and\s+\S+',
]

# Output format markers
FORMAT_MARKERS = [
    "yaml", "json", "markdown", "md", "csv", "html",
    "text", "plain text", "code", "python", "bash",
]


def detect_language_mix(text: str) -> dict:
    """Detect language and mixing in prompt text."""
    text_lower = text.lower()

    pt_count = sum(len(re.findall(p, text_lower)) for p in PT_INDICATORS)
    en_count = sum(len(re.findall(p, text_lower)) for p in EN_INDICATORS)

    total = pt_count + en_count
    if total == 0:
        return {"primary": "unknown", "pt_ratio": 0, "en_ratio": 0, "is_mixed": False}

    pt_ratio = pt_count / total
    en_ratio = en_count / total

    # Mixed = significant presence of both (>20% each)
    is_mixed = pt_ratio > 0.2 and en_ratio > 0.2

    primary = "en" if en_ratio >= pt_ratio else "pt"

    return {
        "primary": primary,
        "pt_ratio": round(pt_ratio, 2),
        "en_ratio": round(en_ratio, 2),
        "is_mixed": is_mixed,
    }


def count_deliverables(text: str) -> int:
    """Estimate number of deliverables from prompt text."""
    text_lower = text.lower()

    for pattern in MULTI_DELIVERABLE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            groups = match.groups()
            for g in groups:
                if g and g.isdigit():
                    return int(g)
            return 2  # "both" / "all" / "multiple"

    # Count "output_path" or "Output:" mentions
    output_count = len(re.findall(r'output[_\s]*(?:path|file|to)\s*:', text_lower))
    if output_count > 1:
        return output_count

    return 1


def validate_prompt(prompt: str, model: str = "haiku",
                    expected_lines: int = 0,
                    has_template: bool = None) -> dict:
    """Validate a Haiku prompt against 14 rules.

    Args:
        prompt: The enriched prompt text
        model: Model assigned (should be haiku)
        expected_lines: Expected output lines (0 = unknown)
        has_template: Whether template is included (None = auto-detect)

    Returns:
        dict with: passed, score, violations, veto_ids, warnings
    """
    violations = []
    warnings = []
    veto_ids = []
    text_lower = prompt.lower()

    # Auto-detect template presence
    if has_template is None:
        has_template = bool(re.search(
            r'(## TEMPLATE|## OUTPUT STRUCTURE|## FORMAT|```yaml|```json|### Expected Format)',
            prompt, re.IGNORECASE
        ))

    lang = detect_language_mix(prompt)
    deliverables = count_deliverables(prompt)

    # ═══════════════════════════════════════════════════════════════════════
    # ALWAYS RULES (veto if absent)
    # ═══════════════════════════════════════════════════════════════════════

    # A1: Instructions in ENGLISH
    if lang["primary"] == "pt" and lang["pt_ratio"] > 0.6:
        violations.append("A1: Instructions NOT in English (primary language: PT)")
        veto_ids.append("V1.6")

    # A2: Template for outputs > 50 lines
    if expected_lines > 50 and not has_template:
        violations.append(f"A2: Expected {expected_lines} lines but NO template provided")
        veto_ids.append("V1.5")

    # A3: "DO NOT ask questions" present
    if not re.search(r'do\s+not\s+ask\s+questions', text_lower):
        if not re.search(r'execute\s+immediately', text_lower):
            violations.append('A3: Missing "DO NOT ask questions. Execute immediately."')

    # A4: "Return ONLY" for structured output
    has_structured = any(fmt in text_lower for fmt in ["yaml", "json", "csv"])
    if has_structured and not re.search(r'return\s+only', text_lower):
        warnings.append('A4: Structured output detected but no "Return ONLY [format]" instruction')

    # A5: 1 task = 1 deliverable
    if deliverables > 1:
        violations.append(f"A5: Multiple deliverables detected ({deliverables})")
        veto_ids.append("V1.7")

    # A6: Output format explicit
    has_format = any(fmt in text_lower for fmt in FORMAT_MARKERS)
    if not has_format:
        warnings.append("A6: No explicit output format specified (yaml/json/markdown/etc.)")

    # A7: Output language specified
    has_lang_spec = bool(re.search(
        r'(output\s+(?:in|language)\s*:\s*\w+|write\s+in\s+\w+|language\s*:\s*(?:pt|en|es))',
        text_lower
    ))
    if not has_lang_spec and lang["primary"] != "en":
        warnings.append("A7: Output language not explicitly specified")

    # ═══════════════════════════════════════════════════════════════════════
    # NEVER RULES (veto if present)
    # ═══════════════════════════════════════════════════════════════════════

    # N1: No context (empty or very short prompt)
    word_count = len(prompt.split())
    if word_count < 20:
        violations.append(f"N1: Prompt too short ({word_count} words) — insufficient context")

    # N2: "Generate document" without template
    if re.search(r'generate\s+\w*\s*document', text_lower) and not has_template:
        violations.append('N2: "Generate document" without template')
        veto_ids.append("V1.5")

    # N3: Code-switching (EN+PT mixed)
    if lang["is_mixed"]:
        violations.append(f"N3: Code-switching detected (PT: {lang['pt_ratio']}, EN: {lang['en_ratio']})")
        veto_ids.append("V1.6")

    # N4: Outputs > 300 lines without template
    if expected_lines > 300 and not has_template:
        violations.append(f"N4: Expected {expected_lines} lines without template — CRITICAL")
        veto_ids.append("V1.5")

    # N5: Multiple deliverables (duplicate check with A5)
    # Already checked in A5

    # N6: Implicit references
    for pattern in IMPLICIT_PATTERNS:
        if re.search(pattern, text_lower):
            violations.append(f'N6: Implicit reference detected: "{re.search(pattern, text_lower).group()}"')
            break

    # N7: Model not explicitly set
    if not model or model.lower() not in ("haiku", "sonnet", "worker"):
        violations.append(f"N7: Model not explicitly set (got: '{model}')")
        veto_ids.append("V1.10")

    # ═══════════════════════════════════════════════════════════════════════
    # SCORE
    # ═══════════════════════════════════════════════════════════════════════

    total_rules = 14
    passed_rules = total_rules - len(violations)
    passed = len(violations) == 0

    # De-duplicate veto IDs
    veto_ids = sorted(set(veto_ids))

    return {
        "passed": passed,
        "score": f"{passed_rules}/{total_rules}",
        "violations": violations,
        "veto_ids": veto_ids,
        "warnings": warnings,
        "details": {
            "language": lang,
            "deliverables": deliverables,
            "has_template": has_template,
            "word_count": word_count,
            "expected_lines": expected_lines,
            "model": model,
        },
    }


def format_report(result: dict) -> str:
    """Format validation result as human-readable report."""
    lines = []
    status = "✅ PASS" if result["passed"] else "❌ FAIL"
    lines.append(f"Haiku Prompt Validation: {status} ({result['score']})")
    lines.append("-" * 50)

    if result["violations"]:
        lines.append("VIOLATIONS:")
        for v in result["violations"]:
            lines.append(f"  ✗ {v}")

    if result["veto_ids"]:
        lines.append(f"VETO IDs: {', '.join(result['veto_ids'])}")

    if result["warnings"]:
        lines.append("WARNINGS:")
        for w in result["warnings"]:
            lines.append(f"  ⚠ {w}")

    d = result["details"]
    lines.append(f"Language: {d['language']['primary']} (PT:{d['language']['pt_ratio']} EN:{d['language']['en_ratio']})")
    lines.append(f"Words: {d['word_count']} | Deliverables: {d['deliverables']} | Template: {d['has_template']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Haiku prompt against 14 ALWAYS/NEVER rules"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", type=str, help="Prompt text to validate")
    group.add_argument("--prompt-file", type=str, help="File containing prompt")
    group.add_argument("--batch", type=str, help="JSON file with array of prompts")

    parser.add_argument("--model", type=str, default="haiku",
                        help="Model assigned (default: haiku)")
    parser.add_argument("--expected-lines", type=int, default=0,
                        help="Expected output lines (default: 0 = unknown)")
    parser.add_argument("--has-template", action="store_true", default=None,
                        help="Template is included in prompt")
    parser.add_argument("--format", choices=["json", "report"], default="json",
                        help="Output format (default: json)")

    args = parser.parse_args()

    if args.prompt:
        result = validate_prompt(args.prompt, args.model, args.expected_lines, args.has_template)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_report(result))
        return 0

    if args.prompt_file:
        filepath = Path(args.prompt_file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1
        prompt = filepath.read_text(encoding="utf-8")
        result = validate_prompt(prompt, args.model, args.expected_lines, args.has_template)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_report(result))
        return 0

    if args.batch:
        filepath = Path(args.batch)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1
        with open(filepath, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        results = []
        for p in prompts:
            if isinstance(p, str):
                r = validate_prompt(p, args.model, args.expected_lines)
            else:
                r = validate_prompt(
                    p.get("prompt", ""), p.get("model", "haiku"),
                    p.get("expected_lines", 0), p.get("has_template")
                )
            results.append(r)
        summary = {
            "total": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "failed": sum(1 for r in results if not r["passed"]),
            "results": results,
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
