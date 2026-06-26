#!/usr/bin/env python3
"""
Assign timeout and max_turns for dispatch tasks.

Usage:
  # Single task
  python scripts/assign-timeout.py --task '{"model": "haiku", "domain": "copy"}'

  # Batch from file
  python scripts/assign-timeout.py --tasks-file execution-plan.yaml

  # Pipe from stdin
  echo '{"model": "sonnet"}' | python scripts/assign-timeout.py --stdin

Output (JSON):
  {
    "timeout": 120,
    "max_turns": 15,
    "rationale": "Rule 2: model=haiku → 120s, max_turns=15"
  }

Assignment Rules (first match wins):
  1. IF executor_type == 'worker' → 30s, max_turns=0
  2. IF model == 'haiku' → 120s, max_turns=15
  3. IF model == 'sonnet' → 300s, max_turns=20
  4. IF domain requires MCP → ×1.5 multiplier
  5. IF type == 'code_generation' → 180s
  6. DEFAULT → 120s, max_turns=15

Source: squads/dispatch/data/timeout-rules.yaml
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# TIMEOUT RULES
# ═══════════════════════════════════════════════════════════════════════════════

# Base timeouts per model/executor
BASE_TIMEOUTS = {
    "worker": 30,
    "haiku": 120,
    "sonnet": 300,
    "opus": 600,
}

# Max turns per model
MAX_TURNS = {
    "worker": 0,
    "haiku": 15,
    "sonnet": 20,
    "opus": 25,
}

# MCP domains get multiplier (API calls + retries)
MCP_DOMAINS = {"ac_automation", "bh_automation", "clickup"}
MCP_MULTIPLIER = 1.5

# Special type overrides
TYPE_TIMEOUTS = {
    "code_generation": 180,
    "mcp_operation": 60,
}

# Safety limits
MAX_WAVE_TIMEOUT = 900   # 15 minutes per wave
MAX_RUN_TIMEOUT = 3600   # 1 hour per run


def assign_timeout(task: dict) -> dict:
    """Assign timeout and max_turns to a single task.

    Args:
        task: dict with keys: model, executor_type, domain, type (all optional)

    Returns:
        dict with: timeout, max_turns, rationale
    """
    model = (task.get("model") or "haiku").lower().strip()
    executor_type = (task.get("executor_type") or "").lower().strip()
    domain = (task.get("domain") or "").lower().strip()
    task_type = (task.get("type") or "").lower().strip()

    # ─── Rule 1: Workers are instant ─────────────────────────────────────
    if executor_type == "worker" or model == "worker":
        return _result(30, 0, "Rule 1: executor=worker → 30s, max_turns=0")

    # ─── Rule 5: Special type overrides ──────────────────────────────────
    if task_type in TYPE_TIMEOUTS:
        timeout = TYPE_TIMEOUTS[task_type]
        turns = MAX_TURNS.get(model, 15)
        return _result(timeout, turns, f"Rule 5: type={task_type} → {timeout}s")

    # ─── Rule 2-3: Model-based timeout ───────────────────────────────────
    timeout = BASE_TIMEOUTS.get(model, 120)
    turns = MAX_TURNS.get(model, 15)
    rationale = f"Rule {2 if model == 'haiku' else 3}: model={model} → {timeout}s, max_turns={turns}"

    # ─── Rule 4: MCP multiplier ──────────────────────────────────────────
    if domain in MCP_DOMAINS:
        original = timeout
        timeout = int(timeout * MCP_MULTIPLIER)
        rationale += f" + MCP ×{MCP_MULTIPLIER} ({original}→{timeout}s)"

    return _result(timeout, turns, rationale)


def _result(timeout: int, max_turns: int, rationale: str) -> dict:
    """Build result dict."""
    return {
        "timeout": timeout,
        "max_turns": max_turns,
        "rationale": rationale,
    }


def assign_batch(tasks: list) -> dict:
    """Assign timeouts to a list of tasks."""
    results = []
    total_timeout = 0
    max_wave_time = 0
    current_wave = None

    for task in tasks:
        result = assign_timeout(task)
        result["task_id"] = task.get("task_id", f"T{len(results)+1:03d}")
        result["task_name"] = task.get("name", task.get("description", "")[:60])
        results.append(result)
        total_timeout += result["timeout"]

        # Track max per wave (parallel = max, not sum)
        wave = task.get("wave", 1)
        if wave != current_wave:
            current_wave = wave
            max_wave_time = max(max_wave_time, result["timeout"])
        else:
            max_wave_time = max(max_wave_time, result["timeout"])

    return {
        "tasks": results,
        "summary": {
            "total": len(results),
            "sum_timeouts_s": total_timeout,
            "max_wave_timeout_s": max_wave_time,
            "within_wave_limit": max_wave_time <= MAX_WAVE_TIMEOUT,
            "within_run_limit": total_timeout <= MAX_RUN_TIMEOUT,
        },
    }


def format_table(result: dict) -> str:
    """Format result as human-readable table."""
    lines = []
    lines.append(f"{'Task ID':<8} {'Timeout':<10} {'Max Turns':<10} {'Rationale'}")
    lines.append("-" * 80)
    for t in result["tasks"]:
        lines.append(
            f"{t['task_id']:<8} {t['timeout']:<10} {t['max_turns']:<10} {t['rationale']}"
        )
    lines.append("-" * 80)
    s = result["summary"]
    wave_ok = "✓" if s["within_wave_limit"] else "✗ EXCEEDS 15min"
    run_ok = "✓" if s["within_run_limit"] else "✗ EXCEEDS 1hr"
    lines.append(
        f"Total: {s['total']} | Sum: {s['sum_timeouts_s']}s | "
        f"Max wave: {s['max_wave_timeout_s']}s {wave_ok} | "
        f"Run limit: {run_ok}"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Assign timeout and max_turns for dispatch tasks"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task", type=str, help="Single task as JSON string")
    group.add_argument("--tasks-file", type=str, help="YAML/JSON file with tasks list")
    group.add_argument("--stdin", action="store_true", help="Read task JSON from stdin")

    parser.add_argument(
        "--format", choices=["json", "table"], default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    if args.task:
        try:
            task = json.loads(args.task)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            return 1
        result = assign_timeout(task)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Timeout: {result['timeout']}s | Max turns: {result['max_turns']} | {result['rationale']}")
        return 0

    if args.stdin:
        try:
            task = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
        if isinstance(task, list):
            result = assign_batch(task)
        else:
            result = assign_timeout(task)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "tasks" in result:
                print(format_table(result))
            else:
                print(f"Timeout: {result['timeout']}s | {result['rationale']}")
        return 0

    if args.tasks_file:
        filepath = Path(args.tasks_file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1
        try:
            import yaml
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except ImportError:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error: Cannot parse file (install PyYAML): {e}", file=sys.stderr)
                return 1

        tasks = data if isinstance(data, list) else data.get("tasks", [])
        result = assign_batch(tasks)

        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_table(result))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
