#!/usr/bin/env python3
"""
Optimal batch size calculator using Reinertsen's U-curve.

Usage:
  # Calculate optimal batch size
  python scripts/batch-size-optimizer.py --transaction-cost 0.025 --holding-cost 0.003 --max-parallel 7

  # From task list with durations
  python scripts/batch-size-optimizer.py --tasks-file execution-plan.yaml --max-parallel 7

  # JSON output
  python scripts/batch-size-optimizer.py --transaction-cost 0.025 --holding-cost 0.003 --format json

Theory (Reinertsen PDFLOW Principle B9):
  Total cost = Transaction cost + Holding cost
  Transaction cost per item = fixed_cost / batch_size  (decreases with larger batches)
  Holding cost per item = batch_size × cost_per_unit_time  (increases with larger batches)
  Optimal batch = sqrt(2 × transaction_cost / holding_cost)  (Economic Order Quantity)

Source: squads/dispatch/data/dispatch-heuristics.yaml
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import math
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULTS (from dispatch config)
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_MAX_PARALLEL = 7           # Max concurrent subagents per wave
DEFAULT_TRANSACTION_COST = 0.025   # Cost of setting up a wave (~Sonnet overhead)
DEFAULT_HOLDING_COST = 0.003       # Cost of delay per task per wave-slot
MIN_BATCH = 1
MAX_BATCH = 15                     # Hard ceiling (API rate limits)


def calculate_optimal_batch(
    transaction_cost: float,
    holding_cost: float,
    max_parallel: int = DEFAULT_MAX_PARALLEL,
    total_tasks: int = 0,
) -> dict:
    """Calculate optimal batch size using EOQ formula.

    Args:
        transaction_cost: Fixed cost of starting a wave (coordination overhead)
        holding_cost: Cost per task per time-slot of waiting in queue
        max_parallel: Maximum parallel tasks (rate limit / API constraint)
        total_tasks: Total tasks to batch (0 = ignore)

    Returns:
        dict with: optimal_batch, total_cost_at_optimal, wave_count, analysis
    """
    if holding_cost <= 0:
        return _result(max_parallel, transaction_cost, 0, total_tasks, max_parallel,
                       "Holding cost=0 → maximize batch (no delay penalty)")

    if transaction_cost <= 0:
        return _result(1, 0, holding_cost, total_tasks, max_parallel,
                       "Transaction cost=0 → minimize batch (no setup penalty)")

    # EOQ formula: sqrt(2 * D * S / H)
    # In our context: sqrt(2 * transaction_cost / holding_cost)
    eoq = math.sqrt(2 * transaction_cost / holding_cost)
    optimal = max(MIN_BATCH, min(int(round(eoq)), MAX_BATCH, max_parallel))

    # Calculate total costs at different batch sizes for analysis
    analysis = []
    for size in range(1, min(max_parallel + 1, MAX_BATCH + 1)):
        tc = transaction_cost / size         # Transaction cost per item
        hc = size * holding_cost             # Holding cost per item
        total = tc + hc
        analysis.append({
            "batch_size": size,
            "transaction_cost_per_item": round(tc, 6),
            "holding_cost_per_item": round(hc, 6),
            "total_cost_per_item": round(total, 6),
            "is_optimal": size == optimal,
        })

    tc_at_optimal = transaction_cost / optimal
    hc_at_optimal = optimal * holding_cost

    return _result(optimal, tc_at_optimal, hc_at_optimal, total_tasks, max_parallel,
                   f"EOQ={eoq:.2f}, clamped to [{MIN_BATCH}, min({max_parallel}, {MAX_BATCH})]",
                   analysis)


def _result(optimal: int, tc: float, hc: float, total_tasks: int,
            max_parallel: int, rationale: str, analysis: list = None) -> dict:
    """Build result dict."""
    wave_count = math.ceil(total_tasks / optimal) if total_tasks > 0 else 0
    return {
        "optimal_batch_size": optimal,
        "total_cost_per_item": round(tc + hc, 6),
        "transaction_cost_per_item": round(tc, 6),
        "holding_cost_per_item": round(hc, 6),
        "wave_count": wave_count,
        "total_tasks": total_tasks,
        "max_parallel": max_parallel,
        "rationale": rationale,
        "u_curve": analysis or [],
    }


def estimate_from_tasks(tasks: list, max_parallel: int) -> dict:
    """Estimate optimal batch from task list characteristics."""
    if not tasks:
        return calculate_optimal_batch(DEFAULT_TRANSACTION_COST, DEFAULT_HOLDING_COST,
                                       max_parallel, 0)

    # Estimate transaction cost from model distribution
    model_costs = {"worker": 0.0, "haiku": 0.007, "sonnet": 0.025, "opus": 0.055}
    total_cost = 0
    for t in tasks:
        model = (t.get("model") or "haiku").lower()
        total_cost += model_costs.get(model, 0.007)

    avg_cost = total_cost / len(tasks) if tasks else 0.007

    # Transaction cost = wave setup overhead (~Sonnet planning per wave)
    transaction_cost = 0.025  # Fixed Sonnet overhead per wave

    # Holding cost = avg delay cost per task per wave-slot
    holding_cost = avg_cost * 0.1  # 10% of avg task cost as delay penalty

    return calculate_optimal_batch(transaction_cost, holding_cost,
                                   max_parallel, len(tasks))


def format_table(result: dict) -> str:
    """Format U-curve as human-readable table."""
    lines = []
    lines.append("=" * 70)
    lines.append("REINERTSEN U-CURVE BATCH OPTIMIZATION")
    lines.append("=" * 70)
    lines.append(f"Optimal batch size: {result['optimal_batch_size']}")
    lines.append(f"Total cost/item at optimal: ${result['total_cost_per_item']:.4f}")
    lines.append(f"Max parallel: {result['max_parallel']}")
    if result['total_tasks'] > 0:
        lines.append(f"Total tasks: {result['total_tasks']} → {result['wave_count']} waves")
    lines.append(f"Rationale: {result['rationale']}")
    lines.append("")

    if result["u_curve"]:
        lines.append(f"{'Size':<6} {'Trans/item':<14} {'Hold/item':<14} {'Total/item':<14} {'Optimal'}")
        lines.append("-" * 60)
        for row in result["u_curve"]:
            marker = "  ◄──" if row["is_optimal"] else ""
            lines.append(
                f"{row['batch_size']:<6} "
                f"${row['transaction_cost_per_item']:<12.4f} "
                f"${row['holding_cost_per_item']:<12.4f} "
                f"${row['total_cost_per_item']:<12.4f} "
                f"{marker}"
            )

    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Optimal batch size via Reinertsen U-curve (EOQ formula)"
    )
    parser.add_argument("--transaction-cost", type=float, default=DEFAULT_TRANSACTION_COST,
                        help=f"Fixed cost per wave setup (default: {DEFAULT_TRANSACTION_COST})")
    parser.add_argument("--holding-cost", type=float, default=DEFAULT_HOLDING_COST,
                        help=f"Delay cost per task per slot (default: {DEFAULT_HOLDING_COST})")
    parser.add_argument("--max-parallel", type=int, default=DEFAULT_MAX_PARALLEL,
                        help=f"Max concurrent tasks (default: {DEFAULT_MAX_PARALLEL})")
    parser.add_argument("--total-tasks", type=int, default=0,
                        help="Total tasks to calculate wave count (default: 0)")
    parser.add_argument("--tasks-file", type=str,
                        help="YAML/JSON file with tasks to estimate from")
    parser.add_argument("--format", choices=["json", "table"], default="json",
                        help="Output format (default: json)")

    args = parser.parse_args()

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
                print(f"Error: Cannot parse: {e}", file=sys.stderr)
                return 1
        tasks = data if isinstance(data, list) else data.get("tasks", [])
        result = estimate_from_tasks(tasks, args.max_parallel)
    else:
        result = calculate_optimal_batch(
            args.transaction_cost, args.holding_cost,
            args.max_parallel, args.total_tasks
        )

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_table(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
