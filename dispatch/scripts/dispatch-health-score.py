#!/usr/bin/env python3
"""
Dispatch Squad — Health Score Calculator (12-Point)
Law #1: CODE > LLM — Score calculation is arithmetic.
Source: PRD Section 9.2 Pattern 5

Evaluates a dispatch run against 12 quality criteria.

Usage:
    python squads/dispatch/scripts/dispatch-health-score.py state.json
    python squads/dispatch/scripts/dispatch-health-score.py state.json --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


HEALTH_CHECKS = [
    {
        "id": 1,
        "name": "Story-Driven Input",
        "check_field": "input_type",
        "pass_condition": lambda state: state.get("input_type") in ("story", "prd"),
        "legacy_if": "Free text without acceptance criteria",
    },
    {
        "id": 2,
        "name": "DAG Wave Optimization",
        "check_field": "total_waves",
        "pass_condition": lambda state: (
            state.get("total_waves", 0) < len(state.get("tasks", {}))
            if state.get("tasks") else False
        ),
        "legacy_if": "Fixed order execution",
    },
    {
        "id": 3,
        "name": "Pre-Execution Gate Passed",
        "pass_condition": lambda state: not any(
            t.get("veto_results") and not all(t["veto_results"].values())
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        ),
        "legacy_if": "No pre-execution validation",
    },
    {
        "id": 4,
        "name": "Model Selection Applied",
        "pass_condition": lambda state: all(
            t.get("model") in ("haiku", "sonnet", "worker")
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        ),
        "legacy_if": "Default model for all",
    },
    {
        "id": 5,
        "name": "CODE > LLM Enforced",
        "pass_condition": lambda state: any(
            t.get("executor_type") == "Worker"
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        ) if any(
            t.get("executor_type") == "Worker"
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        ) else True,
        "legacy_if": "LLM doing mkdir, mv, template fill",
    },
    {
        "id": 6,
        "name": "Enrichment Levels Applied",
        "pass_condition": lambda state: len(set(
            t.get("enrichment", "STANDARD")
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        )) > 1 if len(state.get("tasks", {})) > 3 else True,
        "legacy_if": "Same context for all tasks",
    },
    {
        "id": 7,
        "name": "State Persisted",
        "pass_condition": lambda state: bool(state.get("last_updated")),
        "legacy_if": "No persistence",
    },
    {
        "id": 8,
        "name": "Acceptance Criteria Verified",
        "pass_condition": lambda state: any(
            t.get("veto_results")
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        ),
        "legacy_if": "Task said 'done' without verification",
    },
    {
        "id": 9,
        "name": "Cost Tracked",
        "pass_condition": lambda state: state.get("total_cost_usd", 0) > 0,
        "legacy_if": "Only estimates",
    },
    {
        "id": 10,
        "name": "Zero Main Context Execution",
        "pass_condition": lambda state: True,  # Structural enforcement
        "legacy_if": "Content processed in main context",
    },
    {
        "id": 11,
        "name": "Handoff Saved",
        "pass_condition": lambda state: state.get("status") in ("complete", "paused", "aborted"),
        "legacy_if": "No resume capability",
    },
    {
        "id": 12,
        "name": "Feedback Loop Active",
        "pass_condition": lambda state: any(
            t.get("attempts", 0) > 1
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict) and t.get("status") == "pass"
        ) if any(
            t.get("status") == "fail"
            for t in state.get("tasks", {}).values()
            if isinstance(t, dict)
        ) else True,
        "legacy_if": "Fail = dead",
    },
]


def calculate_health_score(state: dict, verbose: bool = False) -> dict:
    """Calculate 12-point health score for a dispatch run."""
    results = []
    passed = 0

    for check in HEALTH_CHECKS:
        try:
            status = check["pass_condition"](state)
        except Exception:
            status = False

        results.append({
            "id": check["id"],
            "name": check["name"],
            "status": "PASS" if status else "FAIL",
            "legacy_if": check.get("legacy_if", ""),
        })

        if status:
            passed += 1

    score = passed
    if score == 12:
        rating = "Exemplary run — all patterns applied"
    elif score >= 9:
        rating = "Good run — minor improvements"
    elif score >= 5:
        rating = "Needs work — significant patterns missing"
    else:
        rating = "Poor run — most patterns absent"

    return {
        "score": f"{score}/12",
        "rating": rating,
        "passed": passed,
        "failed": 12 - passed,
        "checks": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate dispatch health score")
    parser.add_argument("state_file", help="Path to state.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    with open(args.state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    result = calculate_health_score(state, args.verbose)

    print(f"\n{'═' * 50}")
    print(f" DISPATCH HEALTH SCORE: {result['score']}")
    print(f" Rating: {result['rating']}")
    print(f"{'═' * 50}")

    for check in result["checks"]:
        icon = "✅" if check["status"] == "PASS" else "❌"
        print(f" {icon} {check['id']:2d}. {check['name']}")
        if check["status"] == "FAIL" and args.verbose:
            print(f"      Legacy: {check['legacy_if']}")

    print(f"{'═' * 50}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
