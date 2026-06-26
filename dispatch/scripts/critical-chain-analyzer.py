#!/usr/bin/env python3
"""
Critical chain analyzer — DAG longest path with duration-weighted edges.

Extends wave-optimizer.py with Goldratt's Critical Chain method:
  - Duration-weighted critical path (not just edge count)
  - Slack/float calculation per task
  - Resource conflict detection
  - Project makespan estimation

Usage:
  # From JSON file with tasks
  python scripts/critical-chain-analyzer.py --input dag.json

  # From stdin
  echo '{"tasks": [...]}' | python scripts/critical-chain-analyzer.py --stdin

  # With resource analysis
  python scripts/critical-chain-analyzer.py --input dag.json --resources

Input JSON format:
  {
    "tasks": [
      {"id": "T001", "depends_on": [], "duration": 120, "resource": "haiku"},
      {"id": "T002", "depends_on": ["T001"], "duration": 300, "resource": "sonnet"}
    ]
  }

Output (JSON):
  {
    "critical_chain": ["T001", "T002"],
    "makespan": 420,
    "tasks": [{"id": "T001", "earliest_start": 0, "latest_start": 0, "slack": 0, ...}],
    "resource_conflicts": []
  }

Source: Goldratt's Theory of Constraints + Critical Chain Project Management
Version: 1.0.0
Date: 2026-02-10
"""

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT DURATIONS (seconds) — from timeout-rules.yaml
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_DURATIONS = {
    "worker": 30,
    "haiku": 120,
    "sonnet": 300,
    "opus": 600,
}


def build_graph(tasks: list) -> tuple:
    """Build forward and reverse adjacency lists + in-degree map.

    Returns: (graph, reverse_graph, in_degree, task_map)
    """
    graph = defaultdict(set)          # task → dependents
    reverse_graph = defaultdict(set)  # task → dependencies
    in_degree = {}
    task_map = {}

    for t in tasks:
        tid = t["id"]
        task_map[tid] = t
        in_degree[tid] = 0

    for t in tasks:
        tid = t["id"]
        deps = t.get("depends_on", [])
        for dep in deps:
            if dep in task_map:
                graph[dep].add(tid)
                reverse_graph[tid].add(dep)
                in_degree[tid] = in_degree.get(tid, 0) + 1

    return graph, reverse_graph, in_degree, task_map


def detect_cycles(tasks: list, graph: dict, in_degree: dict) -> list:
    """Detect cycles using Kahn's algorithm. Returns list of cycle members."""
    in_deg = dict(in_degree)
    queue = deque(tid for tid, deg in in_deg.items() if deg == 0)
    visited = set()

    while queue:
        tid = queue.popleft()
        visited.add(tid)
        for dep in graph.get(tid, []):
            in_deg[dep] -= 1
            if in_deg[dep] == 0:
                queue.append(dep)

    all_ids = {t["id"] for t in tasks}
    return list(all_ids - visited)


def forward_pass(tasks: list, graph: dict, in_degree: dict, task_map: dict) -> dict:
    """Calculate earliest start/finish for each task (forward pass).

    Returns: dict[task_id] → {earliest_start, earliest_finish, duration}
    """
    in_deg = dict(in_degree)
    queue = deque(tid for tid, deg in in_deg.items() if deg == 0)
    result = {}

    # Initialize all tasks
    for t in tasks:
        tid = t["id"]
        duration = t.get("duration", DEFAULT_DURATIONS.get(
            (t.get("model") or t.get("resource") or "haiku").lower(), 120
        ))
        result[tid] = {
            "earliest_start": 0,
            "earliest_finish": duration,
            "duration": duration,
        }

    # Process in topological order
    order = []
    while queue:
        tid = queue.popleft()
        order.append(tid)
        for dep in graph.get(tid, []):
            # Dependent's earliest start = max of all dependency finish times
            dep_es = max(result[dep]["earliest_start"],
                        result[tid]["earliest_finish"])
            result[dep]["earliest_start"] = dep_es
            result[dep]["earliest_finish"] = dep_es + result[dep]["duration"]
            in_deg[dep] -= 1
            if in_deg[dep] == 0:
                queue.append(dep)

    return result


def backward_pass(tasks: list, graph: dict, task_map: dict,
                  forward: dict, makespan: int) -> dict:
    """Calculate latest start/finish and slack (backward pass).

    Returns: dict[task_id] → {latest_start, latest_finish, slack}
    """
    result = {}

    # Find sink nodes (no dependents)
    all_ids = {t["id"] for t in tasks}
    has_dependents = set()
    for tid, deps in graph.items():
        has_dependents.update(deps)
    sink_nodes = all_ids - has_dependents

    # Initialize all tasks
    for t in tasks:
        tid = t["id"]
        result[tid] = {
            "latest_finish": makespan,
            "latest_start": makespan - forward[tid]["duration"],
            "slack": 0,
        }

    # Process in reverse topological order (BFS from sinks backward)
    # Build reverse graph
    reverse = defaultdict(set)
    for tid, deps in graph.items():
        for dep in deps:
            reverse[dep].add(tid)

    # Start from sinks
    for tid in sink_nodes:
        result[tid]["latest_finish"] = makespan
        result[tid]["latest_start"] = makespan - forward[tid]["duration"]

    # Process in reverse order — iterate multiple times until stable
    changed = True
    iterations = 0
    while changed and iterations < len(tasks):
        changed = False
        iterations += 1
        for t in tasks:
            tid = t["id"]
            dependents = graph.get(tid, set())
            if dependents:
                min_ls = min(result[dep]["latest_start"] for dep in dependents
                            if dep in result)
                new_lf = min_ls
                new_ls = new_lf - forward[tid]["duration"]
                if new_lf < result[tid]["latest_finish"]:
                    result[tid]["latest_finish"] = new_lf
                    result[tid]["latest_start"] = new_ls
                    changed = True

    # Calculate slack
    for tid in result:
        result[tid]["slack"] = result[tid]["latest_start"] - forward[tid]["earliest_start"]

    return result


def find_critical_chain(tasks: list, forward: dict, backward: dict) -> list:
    """Find critical chain (tasks with zero slack)."""
    critical = []
    for t in tasks:
        tid = t["id"]
        if backward[tid]["slack"] == 0:
            critical.append(tid)

    # Sort by earliest start
    critical.sort(key=lambda tid: forward[tid]["earliest_start"])
    return critical


def detect_resource_conflicts(tasks: list, forward: dict) -> list:
    """Detect resource conflicts — parallel tasks using same resource."""
    conflicts = []
    task_intervals = []

    for t in tasks:
        tid = t["id"]
        resource = (t.get("resource") or t.get("model") or "haiku").lower()
        es = forward[tid]["earliest_start"]
        ef = forward[tid]["earliest_finish"]
        task_intervals.append((tid, resource, es, ef))

    # Check for overlapping intervals on same resource
    for i, (tid1, res1, es1, ef1) in enumerate(task_intervals):
        for j, (tid2, res2, es2, ef2) in enumerate(task_intervals):
            if i >= j:
                continue
            if res1 == res2 and es1 < ef2 and es2 < ef1:
                conflicts.append({
                    "task_a": tid1,
                    "task_b": tid2,
                    "resource": res1,
                    "overlap_start": max(es1, es2),
                    "overlap_end": min(ef1, ef2),
                    "overlap_duration": min(ef1, ef2) - max(es1, es2),
                })

    return conflicts


def analyze(tasks: list, check_resources: bool = False) -> dict:
    """Full critical chain analysis.

    Returns complete analysis with critical chain, makespan, slack, conflicts.
    """
    if not tasks:
        return {"error": "No tasks provided", "critical_chain": [], "makespan": 0}

    graph, reverse_graph, in_degree, task_map = build_graph(tasks)

    # Check for cycles
    cycles = detect_cycles(tasks, graph, in_degree)
    if cycles:
        return {
            "error": f"Circular dependencies detected: {cycles}",
            "critical_chain": [],
            "makespan": 0,
            "cycle_members": cycles,
        }

    # Forward pass
    forward = forward_pass(tasks, graph, in_degree, task_map)

    # Calculate makespan
    makespan = max(f["earliest_finish"] for f in forward.values()) if forward else 0

    # Backward pass
    backward = backward_pass(tasks, graph, task_map, forward, makespan)

    # Critical chain
    critical = find_critical_chain(tasks, forward, backward)

    # Build task details
    task_details = []
    for t in tasks:
        tid = t["id"]
        detail = {
            "id": tid,
            "duration": forward[tid]["duration"],
            "earliest_start": forward[tid]["earliest_start"],
            "earliest_finish": forward[tid]["earliest_finish"],
            "latest_start": backward[tid]["latest_start"],
            "latest_finish": backward[tid]["latest_finish"],
            "slack": backward[tid]["slack"],
            "is_critical": tid in critical,
            "depends_on": list(reverse_graph.get(tid, [])),
        }
        if t.get("resource") or t.get("model"):
            detail["resource"] = (t.get("resource") or t.get("model", "")).lower()
        task_details.append(detail)

    result = {
        "critical_chain": critical,
        "critical_chain_duration": sum(forward[tid]["duration"] for tid in critical),
        "makespan": makespan,
        "total_tasks": len(tasks),
        "critical_tasks": len(critical),
        "non_critical_tasks": len(tasks) - len(critical),
        "tasks": task_details,
    }

    # Resource conflicts (optional)
    if check_resources:
        conflicts = detect_resource_conflicts(tasks, forward)
        result["resource_conflicts"] = conflicts
        result["has_resource_conflicts"] = len(conflicts) > 0

    return result


def format_table(result: dict) -> str:
    """Format analysis as human-readable table."""
    lines = []
    lines.append("=" * 90)
    lines.append("CRITICAL CHAIN ANALYSIS (Goldratt)")
    lines.append("=" * 90)

    if result.get("error"):
        lines.append(f"ERROR: {result['error']}")
        return "\n".join(lines)

    lines.append(f"Makespan: {result['makespan']}s ({result['makespan']/60:.1f}min)")
    lines.append(f"Critical chain: {' → '.join(result['critical_chain'])}")
    lines.append(f"Critical duration: {result['critical_chain_duration']}s")
    lines.append(f"Tasks: {result['total_tasks']} total, {result['critical_tasks']} critical, "
                 f"{result['non_critical_tasks']} with slack")
    lines.append("")

    lines.append(f"{'ID':<10} {'Dur':<6} {'ES':<8} {'EF':<8} {'LS':<8} {'LF':<8} {'Slack':<8} {'Critical'}")
    lines.append("-" * 80)
    for t in result["tasks"]:
        crit = "◄── CRIT" if t["is_critical"] else ""
        lines.append(
            f"{t['id']:<10} {t['duration']:<6} {t['earliest_start']:<8} "
            f"{t['earliest_finish']:<8} {t['latest_start']:<8} "
            f"{t['latest_finish']:<8} {t['slack']:<8} {crit}"
        )

    if result.get("resource_conflicts"):
        lines.append("")
        lines.append(f"RESOURCE CONFLICTS ({len(result['resource_conflicts'])})")
        lines.append("-" * 60)
        for c in result["resource_conflicts"]:
            lines.append(f"  {c['task_a']} ↔ {c['task_b']} on '{c['resource']}' "
                        f"(overlap: {c['overlap_duration']}s)")

    lines.append("=" * 90)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Critical chain analysis — DAG longest path with durations"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", type=str, help="JSON file with tasks")
    group.add_argument("--stdin", action="store_true", help="Read from stdin")

    parser.add_argument("--resources", action="store_true",
                        help="Enable resource conflict detection")
    parser.add_argument("--format", choices=["json", "table"], default="json",
                        help="Output format (default: json)")

    args = parser.parse_args()

    if args.input:
        filepath = Path(args.input)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.stdin:
        data = json.loads(sys.stdin.read())
    else:
        return 1

    tasks = data if isinstance(data, list) else data.get("tasks", [])
    result = analyze(tasks, check_resources=args.resources)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_table(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
