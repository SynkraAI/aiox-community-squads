#!/usr/bin/env python3
"""
Dispatch Squad — Self-Healing Failure Classifier
Pure CODE — pattern matching, no AI.

Replaces LLM reasoning for failure classification and auto-healing in Phase 5.
Deterministic failure detection with prompt patching and model escalation.

Usage:
  python self-heal-failure.py --task-result result.json --run-id 20260212-1234 --format json
  python self-heal-failure.py --task-result '{"output_path": "..."}' --format report
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# FAILURE PATTERNS (V2.* post-execution veto conditions)
# ═══════════════════════════════════════════════════════════════════════════════

FAILURE_PATTERNS = {
    "TIMEOUT": {
        "check": lambda r: r.get("execution_time_ms", 0) > r.get("timeout_ms", float("inf")),
        "classification": "SIMPLE",
        "action": "Extend timeout 2x, retry with same model",
        "prompt_patch": None,  # No prompt change needed
        "should_escalate": False,
    },
    "OUTPUT_MISSING": {
        "check": lambda r: not os.path.exists(r.get("output_path", "")),
        "classification": "SIMPLE",
        "action": "Add explicit output path to prompt",
        "prompt_patch": lambda r: f"\n\nIMPORTANT: Save your output to: {r['output_path']}",
        "should_escalate": False,
    },
    "OUTPUT_EMPTY": {
        "check": lambda r: (
            os.path.exists(r.get("output_path", ""))
            and os.path.getsize(r["output_path"]) < 10
        ),
        "classification": "SIMPLE",
        "action": "Add minimum content constraint",
        "prompt_patch": lambda r: "\n\nIMPORTANT: Output must be at least 100 words. Complete ALL sections.",
        "should_escalate": False,
    },
    "PLACEHOLDER_LEAKED": {
        "check": lambda r: _check_placeholders(r.get("output_path", "")),
        "classification": "SIMPLE",
        "action": "Add placeholder resolution constraint",
        "prompt_patch": lambda r: "\n\nIMPORTANT: Resolve ALL placeholders. Do NOT leave [XXX], {TODO}, TBD, or [INSERT] in output.",
        "should_escalate": False,
    },
    "WRONG_LANGUAGE": {
        "check": lambda r: _check_language_mismatch(r),
        "classification": "SIMPLE",
        "action": "Add explicit language constraint",
        "prompt_patch": lambda r: f"\n\nIMPORTANT: Write output in {r.get('expected_language', 'EN')}.",
        "should_escalate": False,
    },
    "TRUNCATED": {
        "check": lambda r: _check_truncated(r.get("output_path", "")),
        "classification": "SIMPLE",
        "action": "Add completeness constraint",
        "prompt_patch": lambda r: "\n\nIMPORTANT: Complete ALL sections. Do not end mid-sentence.",
        "should_escalate": False,
    },
    "QUALITY_LOW": {
        "check": lambda r: r.get("quality_score", 1.0) < r.get("quality_threshold", 0.7),
        "classification": "MODERATE",
        "action": "Check enrichment level, upgrade if MINIMAL",
        "prompt_patch": None,
        "should_escalate": True,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL FALLBACK RULES (from model-selection-rules.yaml)
# ═══════════════════════════════════════════════════════════════════════════════

FALLBACK_RULES = {
    "haiku": {
        "on_failure": "sonnet",
        "max_retries_before_escalation": 2,
    },
    "sonnet": {
        "on_failure": "opus",
        "max_retries_before_escalation": 1,
    },
    "opus": {
        "on_failure": "human",
        "max_retries_before_escalation": 1,
    },
}

CIRCUIT_BREAKER_THRESHOLD = 3  # consecutive escalations


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def _check_placeholders(output_path: str) -> bool:
    """Check if output contains placeholder text (V2.4)."""
    if not output_path or not os.path.exists(output_path):
        return False

    try:
        with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        placeholder_pattern = r"(\[XXX\]|\{TODO\}|TBD|\[INSERT\]|\[PLACEHOLDER\])"
        return bool(re.search(placeholder_pattern, content))
    except Exception:
        return False


def _check_language_mismatch(result: Dict[str, Any]) -> bool:
    """Heuristic: check if output language doesn't match expected language."""
    output_path = result.get("output_path", "")
    expected_lang = result.get("expected_language", "").upper()

    if not output_path or not os.path.exists(output_path) or not expected_lang:
        return False

    try:
        with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Simple heuristic: count English vs Portuguese common words
        en_words = len(re.findall(r"\b(the|is|are|was|were|have|has|will|can)\b", content, re.I))
        pt_words = len(re.findall(r"\b(o|a|os|as|é|são|foi|tem|vai|pode)\b", content, re.I))

        if expected_lang == "PT-BR" and en_words > pt_words * 2:
            return True
        if expected_lang == "EN" and pt_words > en_words * 2:
            return True
    except Exception:
        pass

    return False


def _check_truncated(output_path: str) -> bool:
    """Heuristic: check if output ends mid-sentence."""
    if not output_path or not os.path.exists(output_path):
        return False

    try:
        with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()

        if not content:
            return False

        # Check if last 100 chars don't contain sentence-ending punctuation
        last_chunk = content[-100:]
        has_ending = bool(re.search(r"[.!?]\s*$", last_chunk))
        return not has_ending
    except Exception:
        return False


def _get_next_model(current_model: str, retry_count: int) -> Optional[str]:
    """Determine next model based on fallback rules."""
    rules = FALLBACK_RULES.get(current_model.lower())
    if not rules:
        return None

    if retry_count >= rules["max_retries_before_escalation"]:
        return rules["on_failure"]

    return current_model  # Retry with same model


def _check_circuit_breaker(run_id: str) -> bool:
    """Check if circuit breaker threshold exceeded (3 consecutive escalations)."""
    run_dir = Path("_temp/dispatch/runs") / run_id
    events_path = run_dir / "events.jsonl"

    if not events_path.exists():
        return False

    # Read recent escalation events
    escalations = []
    with open(events_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                event = json.loads(line)
                if event.get("event") == "model_escalation":
                    escalations.append(event)

    # Count consecutive escalations (no successful tasks in between)
    consecutive = 0
    for event in reversed(escalations):
        if event.get("event") == "model_escalation":
            consecutive += 1
        else:
            break

    return consecutive >= CIRCUIT_BREAKER_THRESHOLD


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLASSIFICATION LOGIC
# ═══════════════════════════════════════════════════════════════════════════════


def classify_failure(task_result: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    """
    Classify failure and determine healing action.

    Returns:
        {
            "classification": "SIMPLE" | "MODERATE" | "COMPLEX",
            "failure_type": str,
            "action": str,
            "prompt_patch": str | None,
            "should_escalate": bool,
            "next_model": str | None,
            "retry_recommended": bool,
            "circuit_breaker": bool
        }
    """
    current_model = task_result.get("model", "haiku")
    retry_count = task_result.get("retry_count", 0)

    # Check each failure pattern
    for failure_type, pattern in FAILURE_PATTERNS.items():
        if pattern["check"](task_result):
            # Generate prompt patch if function provided
            prompt_patch = None
            if pattern["prompt_patch"]:
                if callable(pattern["prompt_patch"]):
                    prompt_patch = pattern["prompt_patch"](task_result)
                else:
                    prompt_patch = pattern["prompt_patch"]

            # Determine next model
            next_model = None
            if pattern["should_escalate"]:
                next_model = _get_next_model(current_model, retry_count)

            # Check circuit breaker
            circuit_breaker = _check_circuit_breaker(run_id)

            return {
                "classification": pattern["classification"],
                "failure_type": failure_type,
                "action": pattern["action"],
                "prompt_patch": prompt_patch,
                "should_escalate": pattern["should_escalate"],
                "next_model": next_model,
                "retry_recommended": not circuit_breaker,
                "circuit_breaker": circuit_breaker,
            }

    # No known pattern matched → COMPLEX failure
    return {
        "classification": "COMPLEX",
        "failure_type": "UNKNOWN",
        "action": "Escalate to user — unknown failure pattern",
        "prompt_patch": None,
        "should_escalate": True,
        "next_model": _get_next_model(current_model, retry_count),
        "retry_recommended": False,
        "circuit_breaker": _check_circuit_breaker(run_id),
    }


def format_report(result: Dict[str, Any]) -> str:
    """Format classification result as human-readable report."""
    lines = [
        "═══════════════════════════════════════════════════════════",
        "SELF-HEALING FAILURE CLASSIFICATION",
        "═══════════════════════════════════════════════════════════",
        "",
        f"Failure Type: {result['failure_type']}",
        f"Classification: {result['classification']}",
        f"Action: {result['action']}",
        "",
    ]

    if result["prompt_patch"]:
        lines.append("Prompt Patch:")
        lines.append(result["prompt_patch"])
        lines.append("")

    lines.append(f"Should Escalate: {result['should_escalate']}")
    if result["next_model"]:
        lines.append(f"Next Model: {result['next_model']}")

    lines.append(f"Retry Recommended: {result['retry_recommended']}")

    if result["circuit_breaker"]:
        lines.append("")
        lines.append("⚠️ CIRCUIT BREAKER TRIGGERED ⚠️")
        lines.append("3+ consecutive escalations detected.")
        lines.append("Action: HALT wave, alert dispatch-chief")

    lines.append("═══════════════════════════════════════════════════════════")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="Self-healing failure classifier for Dispatch Squad"
    )
    parser.add_argument(
        "--task-result",
        required=True,
        help="Task result JSON (string or file path)",
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="Dispatch run ID (e.g., 20260212-1234)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "report"],
        default="json",
        help="Output format",
    )

    args = parser.parse_args()

    # Load task result
    task_result_input = args.task_result
    if os.path.exists(task_result_input):
        with open(task_result_input, "r", encoding="utf-8") as f:
            task_result = json.load(f)
    else:
        task_result = json.loads(task_result_input)

    # Classify failure
    result = classify_failure(task_result, args.run_id)

    # Output
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

    # Exit codes
    if result["circuit_breaker"]:
        sys.exit(2)  # Circuit breaker
    elif result["should_escalate"]:
        sys.exit(1)  # Needs escalation
    else:
        sys.exit(0)  # Auto-healable


if __name__ == "__main__":
    main()
