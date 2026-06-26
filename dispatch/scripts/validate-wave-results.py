#!/usr/bin/env python3
"""
Dispatch Squad — Post-Execution Wave Validator
Law #1: CODE > LLM — File existence checks are deterministic.
Source: PRD Section 3.4 (quality-gate post-execution checks)

Validates outputs from a completed wave:
- V2.1: All output files exist
- V2.2: All output files non-empty
- V2.3: Cost within budget
- V2.4: No placeholder text in outputs

Usage:
    python squads/dispatch/scripts/validate-wave-results.py state.json --wave 1
    python squads/dispatch/scripts/validate-wave-results.py state.json --all
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


PLACEHOLDER_PATTERNS = [
    r"\[XXX\]",
    r"\{TODO\}",
    r"\bTBD\b",
    r"\[PLACEHOLDER\]",
    r"\[INSERT\]",
    r"\{\{[^}]+\}\}",  # Unresolved template vars
]


def validate_task_output(task: dict, project_root: str = ".") -> List[dict]:
    """Validate a single task's output against veto conditions V2.*"""
    issues = []
    output_path = task.get("output_path")
    task_id = task.get("task_id", task.get("id", "unknown"))

    if not output_path:
        # Tasks without output path (e.g., MCP operations) skip file checks
        return issues

    full_path = os.path.join(project_root, output_path)

    # V2.1: File exists
    if not os.path.exists(full_path):
        issues.append({
            "veto_id": "V2.1",
            "task_id": task_id,
            "severity": "FAIL",
            "message": f"Output file does not exist: {output_path}",
        })
        return issues  # Can't check further if file doesn't exist

    # V2.2: File non-empty
    file_size = os.path.getsize(full_path)
    if file_size == 0:
        issues.append({
            "veto_id": "V2.2",
            "task_id": task_id,
            "severity": "FAIL",
            "message": f"Output file is empty (0 bytes): {output_path}",
        })
        return issues

    # V2.4: No placeholder text
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for pattern in PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                issues.append({
                    "veto_id": "V2.4",
                    "task_id": task_id,
                    "severity": "FAIL",
                    "message": f"Placeholder text found in output: {matches[:3]}",
                })
                break
    except Exception as e:
        issues.append({
            "veto_id": "V2.4",
            "task_id": task_id,
            "severity": "WARNING",
            "message": f"Could not read output file: {e}",
        })

    return issues


def validate_wave_cost(tasks: List[dict], max_ratio: float = 3.0) -> List[dict]:
    """V2.3: Check if cost exceeded budget."""
    issues = []
    for task in tasks:
        actual = task.get("cost_usd", 0)
        estimated = task.get("estimated_cost", 0)
        if estimated > 0 and actual > estimated * max_ratio:
            issues.append({
                "veto_id": "V2.3",
                "task_id": task.get("task_id", task.get("id", "unknown")),
                "severity": "WARNING",
                "message": f"Cost ${actual:.4f} exceeded {max_ratio}x estimate ${estimated:.4f}",
            })
    return issues


def validate_wave(state: dict, wave_num: int, project_root: str = ".") -> dict:
    """Validate all tasks in a wave."""
    wave_key = str(wave_num)
    wave = state.get("waves", {}).get(wave_key, {})
    task_ids = wave.get("task_ids", [])

    all_issues = []
    tasks_checked = 0

    for tid in task_ids:
        task = state.get("tasks", {}).get(tid, {})
        if task.get("status") == "pass":
            issues = validate_task_output(task, project_root)
            issues.extend(validate_wave_cost([task]))
            all_issues.extend(issues)
            tasks_checked += 1

    failures = [i for i in all_issues if i["severity"] == "FAIL"]
    warnings = [i for i in all_issues if i["severity"] == "WARNING"]

    return {
        "wave": wave_num,
        "tasks_checked": tasks_checked,
        "failures": len(failures),
        "warnings": len(warnings),
        "issues": all_issues,
        "passed": len(failures) == 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate wave execution results")
    parser.add_argument("state_file", help="Path to state.json")
    parser.add_argument("--wave", type=int, help="Validate specific wave")
    parser.add_argument("--all", action="store_true", help="Validate all waves")
    parser.add_argument("--root", default=".", help="Project root directory")
    args = parser.parse_args()

    with open(args.state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    if args.wave:
        result = validate_wave(state, args.wave, args.root)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["passed"] else 1)

    elif args.all:
        total_failures = 0
        for wave_key in sorted(state.get("waves", {}).keys()):
            result = validate_wave(state, int(wave_key), args.root)
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"Wave {wave_key}: {status} ({result['tasks_checked']} tasks, {result['failures']} failures, {result['warnings']} warnings)")
            for issue in result["issues"]:
                severity = "❌" if issue["severity"] == "FAIL" else "⚠️"
                print(f"  {severity} {issue['veto_id']}: {issue['task_id']} — {issue['message']}")
            total_failures += result["failures"]
        sys.exit(0 if total_failures == 0 else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
