#!/usr/bin/env python3
"""
Dispatch Squad — Cost Tracker
Law #1: CODE > LLM — Cost calculation is arithmetic.

Tracks actual token costs per task, wave, and run.
Uses 2026 pricing: Haiku $1/$5, Sonnet $3/$15, Opus $5/$25 per MTok.

Usage:
    python squads/dispatch/scripts/cost-tracker.py record --run-id dispatch-20260209-143000 --task task-001 --model haiku --tokens-in 2000 --tokens-out 1000
    python squads/dispatch/scripts/cost-tracker.py summary --run-id dispatch-20260209-143000
    python squads/dispatch/scripts/cost-tracker.py estimate --tasks 10 --model haiku --avg-tokens-in 3000 --avg-tokens-out 1500
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


# 2026 Pricing (per million tokens)
PRICING = {
    "haiku": {"input": 1.00, "output": 5.00, "cache_write": 1.25, "cache_read": 0.10},
    "sonnet": {"input": 3.00, "output": 15.00, "cache_write": 3.75, "cache_read": 0.30},
    "opus": {"input": 5.00, "output": 25.00, "cache_write": 6.25, "cache_read": 0.50},
    "worker": {"input": 0.00, "output": 0.00, "cache_write": 0.00, "cache_read": 0.00},
}


def calculate_cost(
    model: str,
    tokens_in: int,
    tokens_out: int,
    cached_tokens_in: int = 0,
) -> float:
    """Calculate cost for a single task execution."""
    if model not in PRICING:
        model = "haiku"

    prices = PRICING[model]
    uncached_in = tokens_in - cached_tokens_in

    cost = (
        (uncached_in / 1_000_000) * prices["input"]
        + (cached_tokens_in / 1_000_000) * prices["cache_read"]
        + (tokens_out / 1_000_000) * prices["output"]
    )
    return round(cost, 6)


def record_cost(run_dir: Path, task_id: str, model: str, tokens_in: int, tokens_out: int, cached: int = 0) -> dict:
    """Record a task's cost to the run's cost log."""
    cost = calculate_cost(model, tokens_in, tokens_out, cached)
    record = {
        "ts": datetime.now().isoformat(),
        "task_id": task_id,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cached_tokens_in": cached,
        "cost_usd": cost,
    }

    cost_log = run_dir / "costs.jsonl"
    with open(cost_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return record


def summarize_costs(run_dir: Path) -> dict:
    """Summarize costs for an entire run."""
    cost_log = run_dir / "costs.jsonl"
    if not cost_log.exists():
        return {"total_cost_usd": 0.0, "tasks": 0}

    records = []
    with open(cost_log, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    total_cost = sum(r["cost_usd"] for r in records)
    total_tokens_in = sum(r["tokens_in"] for r in records)
    total_tokens_out = sum(r["tokens_out"] for r in records)

    by_model = {}
    for r in records:
        m = r["model"]
        if m not in by_model:
            by_model[m] = {"count": 0, "cost": 0.0, "tokens_in": 0, "tokens_out": 0}
        by_model[m]["count"] += 1
        by_model[m]["cost"] += r["cost_usd"]
        by_model[m]["tokens_in"] += r["tokens_in"]
        by_model[m]["tokens_out"] += r["tokens_out"]

    return {
        "total_cost_usd": round(total_cost, 4),
        "total_tokens_in": total_tokens_in,
        "total_tokens_out": total_tokens_out,
        "task_count": len(records),
        "avg_cost_per_task": round(total_cost / len(records), 4) if records else 0.0,
        "by_model": by_model,
    }


def estimate_cost(task_count: int, model: str, avg_tokens_in: int, avg_tokens_out: int) -> dict:
    """Estimate cost for a planned dispatch run."""
    per_task = calculate_cost(model, avg_tokens_in, avg_tokens_out)
    total = per_task * task_count

    # With caching estimate (first task full, rest cached at 90%)
    first_task = per_task
    cached_tasks = calculate_cost(model, avg_tokens_in, avg_tokens_out, int(avg_tokens_in * 0.8))
    total_cached = first_task + cached_tasks * (task_count - 1)

    return {
        "model": model,
        "task_count": task_count,
        "per_task_cost": round(per_task, 4),
        "total_without_cache": round(total, 4),
        "total_with_cache": round(total_cached, 4),
        "cache_savings_pct": round((1 - total_cached / total) * 100, 1) if total > 0 else 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Dispatch cost tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Record
    rec = subparsers.add_parser("record", help="Record task cost")
    rec.add_argument("--run-id", required=True)
    rec.add_argument("--task", required=True)
    rec.add_argument("--model", required=True, choices=["haiku", "sonnet", "opus", "worker"])
    rec.add_argument("--tokens-in", type=int, required=True)
    rec.add_argument("--tokens-out", type=int, required=True)
    rec.add_argument("--cached", type=int, default=0)
    rec.add_argument("--root", default=".")

    # Summary
    summ = subparsers.add_parser("summary", help="Summarize run costs")
    summ.add_argument("--run-id", required=True)
    summ.add_argument("--root", default=".")

    # Estimate
    est = subparsers.add_parser("estimate", help="Estimate dispatch cost")
    est.add_argument("--tasks", type=int, required=True)
    est.add_argument("--model", default="haiku", choices=["haiku", "sonnet", "opus"])
    est.add_argument("--avg-tokens-in", type=int, default=3000)
    est.add_argument("--avg-tokens-out", type=int, default=1500)

    args = parser.parse_args()

    if args.command == "record":
        run_dir = Path(args.root) / "_temp/dispatch/runs" / args.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        result = record_cost(run_dir, args.task, args.model, args.tokens_in, args.tokens_out, args.cached)
        print(json.dumps(result, indent=2))

    elif args.command == "summary":
        run_dir = Path(args.root) / "_temp/dispatch/runs" / args.run_id
        result = summarize_costs(run_dir)
        print(json.dumps(result, indent=2))

    elif args.command == "estimate":
        result = estimate_cost(args.tasks, args.model, args.avg_tokens_in, args.avg_tokens_out)
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
