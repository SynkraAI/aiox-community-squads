#!/usr/bin/env python3
"""
Estimate dispatch batch cost from task/story metadata.

Usage:
  # Estimate from story list
  python scripts/estimate-batch-cost.py --stories '[{"name": "story-1", "task_count": 5, "models": {"haiku": 4, "sonnet": 1}}]'

  # From file
  python scripts/estimate-batch-cost.py --stories-file batch-plan.yaml

  # Quick estimate by task count
  python scripts/estimate-batch-cost.py --tasks 10 --model haiku
  python scripts/estimate-batch-cost.py --tasks 10 --model-mix '{"haiku": 7, "sonnet": 2, "worker": 1}'

Output (JSON):
  {
    "total_cost_usd": 0.078,
    "total_with_cache_usd": 0.052,
    "cache_savings_pct": 33,
    "per_story": [{...}],
    "summary": {by_model, total_tasks, ...}
  }

Pricing: 2026 (from model-selection-rules.yaml)
  Haiku:  $1.00/$5.00 per MTok (in/out), cache read: $0.10
  Sonnet: $3.00/$15.00 per MTok, cache read: $0.30
  Opus:   $5.00/$25.00 per MTok, cache read: $0.50
  Worker: $0.00 (deterministic scripts)

Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 2026 PRICING
# ═══════════════════════════════════════════════════════════════════════════════

PRICING = {
    "worker": {"input": 0.0, "output": 0.0, "cache_read": 0.0},
    "haiku": {"input": 1.00, "output": 5.00, "cache_read": 0.10},
    "sonnet": {"input": 3.00, "output": 15.00, "cache_read": 0.30},
    "opus": {"input": 5.00, "output": 25.00, "cache_read": 0.50},
}

# Average token consumption per task (from dispatch data)
AVG_TOKENS = {
    "worker": {"input": 0, "output": 0},
    "haiku": {"input": 2000, "output": 1000},
    "sonnet": {"input": 3000, "output": 1000},
    "opus": {"input": 5000, "output": 1000},
}

# Cache hit rate assumptions
CACHE_HIT_RATE = {
    "same_domain": 0.75,    # 75% cache hit for same-domain wave
    "mixed_domain": 0.40,   # 40% cache hit for mixed-domain wave
    "default": 0.50,        # 50% average assumption
}


def estimate_task_cost(model: str, cached: bool = False) -> dict:
    """Estimate cost for a single task.

    Returns: {cost_usd, cost_cached_usd, tokens_in, tokens_out}
    """
    model = model.lower()
    pricing = PRICING.get(model, PRICING["haiku"])
    tokens = AVG_TOKENS.get(model, AVG_TOKENS["haiku"])

    tokens_in = tokens["input"]
    tokens_out = tokens["output"]

    # Uncached cost
    cost = (tokens_in / 1_000_000 * pricing["input"] +
            tokens_out / 1_000_000 * pricing["output"])

    # Cached cost (assume default cache hit rate on input tokens)
    cache_rate = CACHE_HIT_RATE["default"]
    cached_input_cost = (
        tokens_in * cache_rate / 1_000_000 * pricing["cache_read"] +
        tokens_in * (1 - cache_rate) / 1_000_000 * pricing["input"]
    )
    cost_cached = cached_input_cost + tokens_out / 1_000_000 * pricing["output"]

    return {
        "cost_usd": round(cost, 6),
        "cost_cached_usd": round(cost_cached, 6),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "model": model,
    }


def estimate_story_cost(story: dict) -> dict:
    """Estimate cost for a story with task counts per model."""
    name = story.get("name", "unnamed")
    task_count = story.get("task_count", 0)
    models = story.get("models", {})

    # If no model breakdown, assume all haiku
    if not models and task_count > 0:
        models = {"haiku": task_count}

    total = 0.0
    total_cached = 0.0
    by_model = {}

    for model, count in models.items():
        task_est = estimate_task_cost(model)
        model_cost = task_est["cost_usd"] * count
        model_cached = task_est["cost_cached_usd"] * count
        total += model_cost
        total_cached += model_cached
        by_model[model] = {
            "count": count,
            "cost_usd": round(model_cost, 6),
            "cost_cached_usd": round(model_cached, 6),
        }

    actual_count = sum(models.values())

    return {
        "name": name,
        "task_count": actual_count,
        "cost_usd": round(total, 4),
        "cost_cached_usd": round(total_cached, 4),
        "by_model": by_model,
    }


def estimate_batch(stories: list) -> dict:
    """Estimate total batch cost across all stories."""
    per_story = []
    total = 0.0
    total_cached = 0.0
    total_tasks = 0
    model_totals = {}

    for story in stories:
        est = estimate_story_cost(story)
        per_story.append(est)
        total += est["cost_usd"]
        total_cached += est["cost_cached_usd"]
        total_tasks += est["task_count"]

        for model, data in est["by_model"].items():
            if model not in model_totals:
                model_totals[model] = {"count": 0, "cost_usd": 0.0}
            model_totals[model]["count"] += data["count"]
            model_totals[model]["cost_usd"] += data["cost_usd"]

    # Round model totals
    for m in model_totals:
        model_totals[m]["cost_usd"] = round(model_totals[m]["cost_usd"], 4)

    savings_pct = round((1 - total_cached / total) * 100, 1) if total > 0 else 0

    return {
        "total_cost_usd": round(total, 4),
        "total_with_cache_usd": round(total_cached, 4),
        "cache_savings_pct": savings_pct,
        "total_tasks": total_tasks,
        "total_stories": len(stories),
        "per_story": per_story,
        "by_model": model_totals,
    }


def estimate_quick(task_count: int, model: str = None,
                   model_mix: dict = None) -> dict:
    """Quick estimate from task count + model."""
    if model_mix:
        stories = [{"name": "estimate", "models": model_mix}]
    elif model:
        stories = [{"name": "estimate", "models": {model: task_count}}]
    else:
        stories = [{"name": "estimate", "models": {"haiku": task_count}}]

    return estimate_batch(stories)


def format_table(result: dict) -> str:
    """Format as human-readable table."""
    lines = []
    lines.append("=" * 80)
    lines.append("DISPATCH BATCH COST ESTIMATE")
    lines.append("=" * 80)
    lines.append(f"Total stories: {result['total_stories']}")
    lines.append(f"Total tasks: {result['total_tasks']}")
    lines.append(f"Cost (no cache):  ${result['total_cost_usd']:.4f}")
    lines.append(f"Cost (with cache): ${result['total_with_cache_usd']:.4f}")
    lines.append(f"Cache savings: {result['cache_savings_pct']}%")
    lines.append("")

    if result["per_story"] and len(result["per_story"]) > 1:
        lines.append(f"{'Story':<30} {'Tasks':<8} {'Cost':<12} {'Cached':<12}")
        lines.append("-" * 70)
        for s in result["per_story"]:
            lines.append(
                f"{s['name']:<30} {s['task_count']:<8} "
                f"${s['cost_usd']:<10.4f} ${s['cost_cached_usd']:<10.4f}"
            )
        lines.append("-" * 70)

    lines.append("")
    lines.append("By Model:")
    for model, data in result["by_model"].items():
        lines.append(f"  {model}: {data['count']} tasks → ${data['cost_usd']:.4f}")

    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Estimate dispatch batch cost from task/story metadata"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stories", type=str, help="Story list as JSON string")
    group.add_argument("--stories-file", type=str, help="YAML/JSON file with stories")
    group.add_argument("--tasks", type=int, help="Quick estimate: total task count")

    parser.add_argument("--model", type=str, default="haiku",
                        help="Model for quick estimate (default: haiku)")
    parser.add_argument("--model-mix", type=str,
                        help='Model mix as JSON: \'{"haiku": 7, "sonnet": 2}\'')
    parser.add_argument("--format", choices=["json", "table"], default="json",
                        help="Output format (default: json)")

    args = parser.parse_args()

    if args.tasks:
        model_mix = json.loads(args.model_mix) if args.model_mix else None
        result = estimate_quick(args.tasks, args.model, model_mix)
    elif args.stories:
        try:
            stories = json.loads(args.stories)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            return 1
        if not isinstance(stories, list):
            stories = [stories]
        result = estimate_batch(stories)
    elif args.stories_file:
        filepath = Path(args.stories_file)
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
        stories = data if isinstance(data, list) else data.get("stories", [data])
        result = estimate_batch(stories)
    else:
        return 1

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_table(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
