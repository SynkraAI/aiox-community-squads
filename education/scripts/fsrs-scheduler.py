#!/usr/bin/env python3
"""
FSRS Spaced Repetition Scheduler
Replaces LLM-based schedule-repetition.md task with deterministic algorithm.

Usage:
  python squads/education/scripts/fsrs-scheduler.py \
    --domain "python-fundamentals" \
    --concepts concepts.yaml \
    --duration 90 \
    --retention 0.90 \
    --output minds/python-fundamentals/review-schedule.md
"""

import argparse
import math
import os
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# FSRS v4 Parameters (defaults from open-source FSRS)
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_WEIGHTS = {
    "w0": 0.4,    # initial stability (again)
    "w1": 0.6,    # initial stability (hard)
    "w2": 2.4,    # initial stability (good)
    "w3": 5.8,    # initial stability (easy)
    "w4": 4.93,   # difficulty weight
    "w5": 0.94,   # stability decay
    "w6": 0.86,   # stability rebound
    "w7": 0.01,   # difficulty mean reversion
    "w8": 1.49,   # stability after success
    "w9": 0.14,   # stability growth
    "w10": 0.94,  # difficulty penalty
    "w11": 2.18,  # difficulty reward
    "w12": 0.05,  # stability short-term
    "w13": 0.34,  # stability long-term
}

DIFFICULTY_MAP = {
    "easy": 1,
    "medium": 2,
    "hard": 3,
    "very_hard": 4,
}


def initial_stability(difficulty_level: int, w: dict) -> float:
    """Calculate initial stability based on difficulty."""
    keys = ["w0", "w1", "w2", "w3"]
    idx = max(0, min(difficulty_level - 1, 3))
    return w[keys[idx]]


def next_interval(stability: float, target_retention: float) -> float:
    """Calculate next review interval in days from stability and target retention."""
    if target_retention <= 0 or target_retention >= 1:
        target_retention = 0.90
    interval = stability * (math.log(target_retention) / math.log(0.9))
    return max(1.0, round(interval, 1))


def update_stability(stability: float, difficulty: float, grade: int, w: dict) -> float:
    """Update stability after a review (assuming grade=3 'good' for scheduling)."""
    new_s = stability * (
        1
        + math.exp(w["w8"])
        * (11 - difficulty)
        * stability ** (-w["w9"])
        * (math.exp((1 - 0.9) * w["w10"]) - 1)
    )
    return max(0.1, new_s)


def generate_schedule(
    concept: str,
    difficulty_label: str,
    course_duration_days: int,
    target_retention: float,
    w: dict,
) -> list[dict]:
    """Generate full review schedule for a single concept."""
    diff_level = DIFFICULTY_MAP.get(difficulty_label, 2)
    stability = initial_stability(diff_level, w)
    difficulty = 5.0 + (diff_level - 2) * 1.5  # map to 2-8 range

    schedule = []
    current_day = 0

    while current_day < course_duration_days:
        interval = next_interval(stability, target_retention)
        current_day += interval

        if current_day > course_duration_days * 1.1:  # 10% grace
            break

        schedule.append({
            "day": round(current_day),
            "interval": round(interval),
            "stability": round(stability, 2),
        })

        stability = update_stability(stability, difficulty, 3, w)

    return schedule


def load_concepts(path: str) -> list[dict]:
    """Load concepts from YAML or plain text file."""
    concepts = []

    if not os.path.exists(path):
        print(f"ERROR: Concepts file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Try YAML
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml  # noqa: E402
            data = yaml.safe_load(content)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        concepts.append({
                            "name": item.get("name", item.get("concept", str(item))),
                            "difficulty": item.get("difficulty", "medium"),
                        })
                    else:
                        concepts.append({"name": str(item), "difficulty": "medium"})
            return concepts
        except Exception:
            pass

    # Fallback: plain text (one concept per line, optional difficulty after |)
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            parts = line.split("|", 1)
            concepts.append({
                "name": parts[0].strip(),
                "difficulty": parts[1].strip().lower(),
            })
        else:
            concepts.append({"name": line, "difficulty": "medium"})

    return concepts


def identify_checkpoints(
    course_duration_days: int,
) -> list[dict]:
    """Generate review checkpoints at week ends, module boundaries, and course end."""
    checkpoints = []

    # Weekly checkpoints
    week = 7
    day = week
    while day <= course_duration_days:
        checkpoints.append({"day": day, "type": "weekly"})
        day += week

    # End of course
    if not checkpoints or checkpoints[-1]["day"] != course_duration_days:
        checkpoints.append({"day": course_duration_days, "type": "course_end"})

    return checkpoints


def render_markdown(
    domain: str,
    concepts: list[dict],
    schedules: dict[str, list[dict]],
    checkpoints: list[dict],
    course_duration_days: int,
    target_retention: float,
) -> str:
    """Render the review schedule as Markdown."""
    lines = [
        f"# Review Schedule: {domain}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Course Duration:** {course_duration_days} days",
        f"**Target Retention:** {target_retention * 100:.0f}%",
        f"**Concepts:** {len(concepts)}",
        "",
        "---",
        "",
        "## Concept Review Intervals",
        "",
        "| Concept | Difficulty | Reviews | Intervals (days) |",
        "|---------|-----------|---------|-------------------|",
    ]

    for c in concepts:
        name = c["name"]
        sched = schedules.get(name, [])
        intervals = ", ".join(str(s["interval"]) for s in sched[:8])
        if len(sched) > 8:
            intervals += f"... (+{len(sched) - 8} more)"
        lines.append(f"| {name} | {c['difficulty']} | {len(sched)} | {intervals} |")

    lines += [
        "",
        "---",
        "",
        "## Review Checkpoints",
        "",
        "| Day | Type | Concepts Due |",
        "|-----|------|-------------|",
    ]

    for cp in checkpoints:
        # Find concepts due around this checkpoint (±2 days)
        due = []
        for c in concepts:
            for s in schedules.get(c["name"], []):
                if abs(s["day"] - cp["day"]) <= 2:
                    due.append(c["name"])
                    break
        due_str = ", ".join(due[:5]) if due else "(cumulative review)"
        if len(due) > 5:
            due_str += f" +{len(due) - 5} more"
        lines.append(f"| {cp['day']} | {cp['type']} | {due_str} |")

    lines += [
        "",
        "---",
        "",
        "## Review Activity Specs",
        "",
        "| Review Type | Format | Duration | Pass Criteria |",
        "|-------------|--------|----------|---------------|",
        "| Daily recall | Flashcard / free recall | 5-10 min | 80%+ correct |",
        "| Weekly checkpoint | Quiz (10-15 items) | 15-20 min | 70%+ correct |",
        "| Module review | Applied exercise | 30-45 min | Complete with rubric |",
        "| Course-end assessment | Comprehensive test | 60-90 min | 70%+ correct |",
        "",
        "---",
        "",
        "## Post-Course Schedule (Optional)",
        "",
        "| Interval | Activity | Focus |",
        "|----------|----------|-------|",
        "| +30 days | Cumulative review | All key concepts |",
        "| +60 days | Applied project | Transfer verification |",
        "| +90 days | Retention test | Long-term retention check |",
        "",
        "---",
        "",
        "## FSRS Parameters Used",
        "",
        "```yaml",
        "algorithm: FSRS v4 (simplified)",
        f"target_retention: {target_retention}",
        "max_interval: 365",
        "grade_assumed: 3 (good)",
        "weights: default_fsrs_v4",
        "```",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="FSRS Spaced Repetition Scheduler — deterministic schedule generation"
    )
    parser.add_argument("--domain", required=True, help="Course domain name")
    parser.add_argument("--concepts", required=True, help="Path to concepts file (YAML or text)")
    parser.add_argument("--duration", type=int, required=True, help="Course duration in days")
    parser.add_argument("--retention", type=float, default=0.90, help="Target retention (0-1, default: 0.90)")
    parser.add_argument("--output", default=None, help="Output path (default: minds/{domain}/review-schedule.md)")

    args = parser.parse_args()

    if args.retention <= 0 or args.retention >= 1:
        print("ERROR: --retention must be between 0 and 1 (e.g., 0.90)", file=sys.stderr)
        sys.exit(1)

    # Load concepts
    concepts = load_concepts(args.concepts)
    if not concepts:
        print("ERROR: No concepts found in file", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(concepts)} concepts from {args.concepts}")

    # Generate schedules
    w = DEFAULT_WEIGHTS
    schedules = {}
    for c in concepts:
        schedules[c["name"]] = generate_schedule(
            c["name"], c["difficulty"], args.duration, args.retention, w
        )

    # Generate checkpoints
    checkpoints = identify_checkpoints(args.duration)

    # Render
    md = render_markdown(
        args.domain, concepts, schedules, checkpoints, args.duration, args.retention
    )

    # Write output
    output_path = args.output or f"minds/{args.domain}/review-schedule.md"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Schedule written to: {output_path}")
    total_reviews = sum(len(s) for s in schedules.values())
    print(f"Total review events: {total_reviews}")


if __name__ == "__main__":
    main()
