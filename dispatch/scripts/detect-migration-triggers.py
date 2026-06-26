#!/usr/bin/env python3
"""
Dispatch Squad — Migration Trigger Detection
Law #1: CODE > LLM — Detection is data analysis, not reasoning.
Source: PRD Section 10.4 + model-selection-rules.yaml migration_triggers

Scans completed dispatch runs to detect when:
1. Agent tasks should be converted to Worker scripts (high consistency)
2. Worker scripts should fallback to Agents (edge case failures)

Usage:
    python squads/dispatch/scripts/detect-migration-triggers.py
    python squads/dispatch/scripts/detect-migration-triggers.py --min-executions 30
    python squads/dispatch/scripts/detect-migration-triggers.py --verbose
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


# Migration thresholds from model-selection-rules.yaml
AGENT_TO_WORKER_MIN_EXECUTIONS = 50
AGENT_TO_WORKER_CONSISTENCY = 0.97
WORKER_TO_AGENT_FAILURE_RATE = 0.15  # 15% failure rate triggers fallback


def scan_dispatch_runs(runs_dir: Path) -> Dict[str, List[dict]]:
    """Scan all state.json files in _temp/dispatch/runs/*/state.json."""
    task_executions = defaultdict(list)

    if not runs_dir.exists():
        return {}

    for run_dir in runs_dir.iterdir():
        if not run_dir.is_dir():
            continue

        state_file = run_dir / "state.json"
        if not state_file.exists():
            continue

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)

            # Extract task executions
            for task_id, task_data in state.get("tasks", {}).items():
                if not isinstance(task_data, dict):
                    continue

                task_type = task_data.get("task_type", "unknown")
                executor_type = task_data.get("executor_type", "Agent")
                status = task_data.get("status", "unknown")

                task_executions[task_type].append({
                    "executor_type": executor_type,
                    "status": status,
                    "run_id": run_dir.name,
                    "task_id": task_id,
                })

        except (json.JSONDecodeError, Exception):
            continue

    return task_executions


def calculate_agent_consistency(executions: List[dict]) -> Tuple[int, int, float]:
    """Calculate consistency rate for Agent executions."""
    agent_executions = [e for e in executions if e["executor_type"] == "Agent"]

    if not agent_executions:
        return 0, 0, 0.0

    pass_count = sum(1 for e in agent_executions if e["status"] == "pass")
    total_count = len(agent_executions)
    consistency = pass_count / total_count if total_count > 0 else 0.0

    return pass_count, total_count, consistency


def calculate_worker_failure_rate(executions: List[dict]) -> Tuple[int, int, float]:
    """Calculate failure rate for Worker executions."""
    worker_executions = [e for e in executions if e["executor_type"] == "Worker"]

    if not worker_executions:
        return 0, 0, 0.0

    fail_count = sum(1 for e in worker_executions if e["status"] == "fail")
    total_count = len(worker_executions)
    failure_rate = fail_count / total_count if total_count > 0 else 0.0

    return fail_count, total_count, failure_rate


def detect_migration_signals(
    task_executions: Dict[str, List[dict]],
    min_executions: int = AGENT_TO_WORKER_MIN_EXECUTIONS,
    verbose: bool = False
) -> dict:
    """Detect migration triggers based on execution history."""

    agent_to_worker_candidates = []
    worker_to_agent_candidates = []

    for task_type, executions in task_executions.items():
        # Check for Agent → Worker migration
        pass_count, total_count, consistency = calculate_agent_consistency(executions)

        if total_count >= min_executions and consistency >= AGENT_TO_WORKER_CONSISTENCY:
            agent_to_worker_candidates.append({
                "task_type": task_type,
                "executions": total_count,
                "consistency": consistency,
                "pass_count": pass_count,
            })

        # Check for Worker → Agent fallback
        fail_count, worker_total, failure_rate = calculate_worker_failure_rate(executions)

        if worker_total > 0 and failure_rate >= WORKER_TO_AGENT_FAILURE_RATE:
            worker_to_agent_candidates.append({
                "task_type": task_type,
                "worker_executions": worker_total,
                "failure_rate": failure_rate,
                "fail_count": fail_count,
            })

    return {
        "agent_to_worker": sorted(
            agent_to_worker_candidates,
            key=lambda x: (x["executions"], x["consistency"]),
            reverse=True
        ),
        "worker_to_agent": sorted(
            worker_to_agent_candidates,
            key=lambda x: x["failure_rate"],
            reverse=True
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Detect migration triggers from dispatch runs")
    parser.add_argument(
        "--runs-dir",
        default="_temp/dispatch/runs",
        help="Path to dispatch runs directory (default: _temp/dispatch/runs)"
    )
    parser.add_argument(
        "--min-executions",
        type=int,
        default=AGENT_TO_WORKER_MIN_EXECUTIONS,
        help=f"Minimum executions for Agent→Worker migration (default: {AGENT_TO_WORKER_MIN_EXECUTIONS})"
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)

    print(f"\n{'═' * 60}")
    print(" MIGRATION TRIGGER DETECTION")
    print(f"{'═' * 60}")
    print(f" Scanning: {runs_dir}")

    task_executions = scan_dispatch_runs(runs_dir)

    if not task_executions:
        print(" No dispatch runs found.")
        print(f"{'═' * 60}\n")
        return

    print(f" Task types found: {len(task_executions)}")
    print(f"{'═' * 60}\n")

    signals = detect_migration_signals(task_executions, args.min_executions, args.verbose)

    # Report Agent → Worker candidates
    if signals["agent_to_worker"]:
        print(f" AGENT → WORKER CANDIDATES ({len(signals['agent_to_worker'])})")
        print(f" {'─' * 58}")
        print(" Tasks with >={} executions and ≥{}% consistency\n".format(
            args.min_executions,
            int(AGENT_TO_WORKER_CONSISTENCY * 100)
        ))

        for candidate in signals["agent_to_worker"]:
            print(f" 🔄 {candidate['task_type']}")
            print(f"    Executions: {candidate['executions']}")
            print(f"    Consistency: {candidate['consistency']:.1%} ({candidate['pass_count']}/{candidate['executions']} passed)")
            print(f"    Action: Create deterministic script, remove from LLM routing\n")
    else:
        print(" AGENT → WORKER CANDIDATES (0)")
        print(f" {'─' * 58}")
        print(" No tasks meet migration criteria yet.\n")

    # Report Worker → Agent candidates
    if signals["worker_to_agent"]:
        print(f" WORKER → AGENT FALLBACK NEEDED ({len(signals['worker_to_agent'])})")
        print(f" {'─' * 58}")
        print(f" Workers with ≥{int(WORKER_TO_AGENT_FAILURE_RATE * 100)}% failure rate\n")

        for candidate in signals["worker_to_agent"]:
            print(f" ⚠️  {candidate['task_type']}")
            print(f"    Worker executions: {candidate['worker_executions']}")
            print(f"    Failure rate: {candidate['failure_rate']:.1%} ({candidate['fail_count']}/{candidate['worker_executions']} failed)")
            print(f"    Action: Route to Agent with worker output as input (hybrid)\n")
    else:
        print(" WORKER → AGENT FALLBACK NEEDED (0)")
        print(f" {'─' * 58}")
        print(" All worker scripts performing within tolerance.\n")

    print(f"{'═' * 60}")

    # JSON output for programmatic use
    if args.verbose:
        print("\nJSON OUTPUT:")
        print(json.dumps(signals, indent=2))

    print()


if __name__ == "__main__":
    main()
