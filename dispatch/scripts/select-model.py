#!/usr/bin/env python3
"""
Select model for dispatch task using Q1-Q4 decision tree.

Usage:
  # Single task (JSON string)
  python scripts/select-model.py --task '{"type": "create", "has_template": true}'

  # Batch from file
  python scripts/select-model.py --tasks-file execution-plan.yaml

  # Pipe from stdin
  echo '{"type": "move"}' | python scripts/select-model.py --stdin

Output (JSON):
  {
    "model": "haiku",
    "executor_type": "Agent",
    "rationale": "Q2: has_template=true → haiku",
    "timeout": 120,
    "max_turns": 15
  }

Decision Tree (first match wins):
  Q1: 100% deterministic (mkdir, mv, rename, delete, template fill) → worker
  Q2: Has template OR well-defined with criteria → haiku
  Q3: Requires judgment, evaluation, creative >500 words → sonnet
  Q4: Architectural/strategic → REDIRECT (do not dispatch)
  Default: haiku

Source: squads/dispatch/data/model-selection-rules.yaml
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# DETERMINISTIC CLASSIFICATION RULES
# ═══════════════════════════════════════════════════════════════════════════════

# Q1: Worker types — output is 100% predictable
WORKER_TYPES = {
    "move", "delete", "rename", "mkdir", "copy", "gitkeep",
    "index", "validate", "template_fill", "organize",
}

# Q1: Worker verb patterns in description
WORKER_VERBS = {
    "move", "rename", "delete", "create folder", "mkdir",
    "copy file", "organize", "generate index", "create index",
    "list files", "count files", "validate path",
}

# Q3: Sonnet types — requires judgment
SONNET_TYPES = {
    "evaluate", "audit", "analyze", "review", "diagnose",
    "assess", "compare", "debate", "critique", "score",
    "feedback", "decompose", "plan",
}

# Q3: Sonnet verb patterns in description
SONNET_VERBS = {
    "evaluate", "audit", "analyze", "review", "diagnose",
    "assess quality", "compare", "judge", "critique",
    "score against", "write feedback", "decompose story",
    "plan execution", "interpret requirements",
}

# Q4: Redirect types — should NOT be dispatched
REDIRECT_TYPES = {
    "architecture", "strategy", "prd", "system_design",
    "infrastructure", "database_schema", "migration_plan",
}

# Q4: Redirect keywords in description
REDIRECT_KEYWORDS = {
    "architecture decision", "system design", "trade-off analysis",
    "migration strategy", "infrastructure plan", "database schema",
    "microservice design", "api design",
}

# MCP domains that require foreground execution
MCP_DOMAINS = {"ac_automation", "bh_automation", "clickup"}


def classify_task(task: dict) -> dict:
    """Classify a single task using Q1-Q4 decision tree.

    Args:
        task: dict with keys: type, description, has_template,
              domain, word_count (all optional)

    Returns:
        dict with: model, executor_type, rationale, timeout, max_turns
    """
    task_type = (task.get("type") or "").lower().strip()
    description = (task.get("description") or "").lower().strip()
    has_template = task.get("has_template", False)
    domain = (task.get("domain") or "").lower().strip()
    word_count = task.get("word_count", 0)

    # ─── Q1: Is output 100% deterministic? ───────────────────────────────
    if task_type in WORKER_TYPES:
        return _result("worker", "Worker", f"Q1: type={task_type} is deterministic", 30, 0)

    if any(v in description for v in WORKER_VERBS):
        matched = next(v for v in WORKER_VERBS if v in description)
        return _result("worker", "Worker", f"Q1: verb '{matched}' is deterministic", 30, 0)

    # ─── Q4: Is it architectural/strategic? (check before Q2/Q3) ─────────
    if task_type in REDIRECT_TYPES:
        return _result("redirect", "Human", f"Q4: type={task_type} → REDIRECT, do not dispatch", 0, 0)

    if any(kw in description for kw in REDIRECT_KEYWORDS):
        matched = next(kw for kw in REDIRECT_KEYWORDS if kw in description)
        return _result("redirect", "Human", f"Q4: keyword '{matched}' → REDIRECT", 0, 0)

    # ─── Q2: Has template or is well-defined? ────────────────────────────
    if has_template:
        timeout = 60 if domain in MCP_DOMAINS else 120
        return _result("haiku", "Agent", "Q2: has_template=true → haiku", timeout, 15)

    # ─── Q3: Requires judgment or evaluation? ────────────────────────────
    if task_type in SONNET_TYPES:
        return _result("sonnet", "Agent", f"Q3: type={task_type} requires judgment", 300, 20)

    if any(v in description for v in SONNET_VERBS):
        matched = next(v for v in SONNET_VERBS if v in description)
        return _result("sonnet", "Agent", f"Q3: verb '{matched}' requires judgment", 300, 20)

    if word_count > 500:
        return _result("sonnet", "Agent", f"Q3: word_count={word_count} > 500 → creative", 300, 20)

    # ─── Default: haiku ──────────────────────────────────────────────────
    timeout = 60 if domain in MCP_DOMAINS else 120
    return _result("haiku", "Agent", "Default: well-defined task → haiku", timeout, 15)


def _result(model: str, executor_type: str, rationale: str,
            timeout: int, max_turns: int) -> dict:
    """Build result dict."""
    return {
        "model": model,
        "executor_type": executor_type,
        "rationale": rationale,
        "timeout": timeout,
        "max_turns": max_turns,
    }


def classify_batch(tasks: list) -> dict:
    """Classify a list of tasks and return summary."""
    results = []
    counts = {"worker": 0, "haiku": 0, "sonnet": 0, "redirect": 0}

    for task in tasks:
        result = classify_task(task)
        result["task_id"] = task.get("task_id", f"T{len(results)+1:03d}")
        result["task_name"] = task.get("name", task.get("description", "")[:60])
        results.append(result)
        counts[result["model"]] += 1

    return {
        "tasks": results,
        "summary": {
            "total": len(results),
            "worker": counts["worker"],
            "haiku": counts["haiku"],
            "sonnet": counts["sonnet"],
            "redirect": counts["redirect"],
            "estimated_cost_usd": round(
                counts["haiku"] * 0.007 + counts["sonnet"] * 0.025, 4
            ),
        },
    }


def format_table(result: dict) -> str:
    """Format result as human-readable table."""
    lines = []
    lines.append(f"{'Task ID':<8} {'Model':<10} {'Executor':<8} {'Timeout':<8} {'Rationale'}")
    lines.append("-" * 80)
    for t in result["tasks"]:
        lines.append(
            f"{t['task_id']:<8} {t['model']:<10} {t['executor_type']:<8} "
            f"{t['timeout']:<8} {t['rationale']}"
        )
    lines.append("-" * 80)
    s = result["summary"]
    lines.append(
        f"Total: {s['total']} | Worker: {s['worker']} | "
        f"Haiku: {s['haiku']} | Sonnet: {s['sonnet']} | "
        f"Redirect: {s['redirect']} | Est. cost: ${s['estimated_cost_usd']}"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Select model for dispatch tasks using Q1-Q4 decision tree"
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

    # Load input
    if args.task:
        try:
            task = json.loads(args.task)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            return 1
        result = classify_task(task)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Model: {result['model']} | {result['rationale']}")
        return 0

    if args.stdin:
        try:
            task = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
        if isinstance(task, list):
            result = classify_batch(task)
        else:
            result = classify_task(task)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "tasks" in result:
                print(format_table(result))
            else:
                print(f"Model: {result['model']} | {result['rationale']}")
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
            # Fallback: try JSON
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error: Cannot parse file (install PyYAML): {e}", file=sys.stderr)
                return 1

        tasks = data if isinstance(data, list) else data.get("tasks", [])
        result = classify_batch(tasks)

        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_table(result))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
