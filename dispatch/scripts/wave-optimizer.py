#!/usr/bin/env python3
"""
Dispatch Squad — Wave Optimizer (DAG Topological Sort)
Law #1: CODE > LLM — Kahn's algorithm is 100% deterministic.
Law #5: WAVE OPTIMIZED — Maximum parallelism via DAG.

Usage:
    python squads/dispatch/scripts/wave-optimizer.py tasks.json
    python squads/dispatch/scripts/wave-optimizer.py tasks.json --check-cycles
    python squads/dispatch/scripts/wave-optimizer.py tasks.json --max-parallel 5
    python squads/dispatch/scripts/wave-optimizer.py tasks.json --output waves.json

Input JSON format:
    {
        "tasks": [
            {"id": "task-001", "depends_on": []},
            {"id": "task-002", "depends_on": []},
            {"id": "task-003", "depends_on": ["task-001"]},
            {"id": "task-004", "depends_on": ["task-001", "task-002"]}
        ]
    }

Output: Waves grouped by dependency level, max parallelism respected.
"""

import argparse
import json
import sys
from collections import defaultdict, deque
from typing import Dict, List, Optional, Set, Tuple


def build_graph(tasks: List[dict]) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
    """Build adjacency list and in-degree map from task dependencies."""
    graph: Dict[str, Set[str]] = defaultdict(set)  # task -> set of dependents
    in_degree: Dict[str, int] = {}

    task_ids = {t["id"] for t in tasks}

    for task in tasks:
        tid = task["id"]
        in_degree[tid] = 0

    for task in tasks:
        tid = task["id"]
        deps = task.get("depends_on", [])
        for dep in deps:
            if dep not in task_ids:
                print(f"WARNING: Task {tid} depends on {dep} which does not exist", file=sys.stderr)
                continue
            graph[dep].add(tid)
            in_degree[tid] = in_degree.get(tid, 0) + 1

    return graph, in_degree


def detect_cycles(tasks: List[dict]) -> List[str]:
    """Detect circular dependencies in the task graph.

    Returns list of task IDs involved in cycles (empty if no cycles).
    """
    graph, in_degree = build_graph(tasks)
    queue = deque(tid for tid, deg in in_degree.items() if deg == 0)
    visited = set()

    while queue:
        tid = queue.popleft()
        visited.add(tid)
        for dependent in graph[tid]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    all_ids = {t["id"] for t in tasks}
    cycle_ids = all_ids - visited
    return sorted(cycle_ids)


def reconstruct_cycle_path(tasks: List[dict], cycle_ids: List[str]) -> List[str]:
    """Reconstruct the actual cycle path using DFS with color tracking.

    Uses WHITE (unvisited), GRAY (in-progress), BLACK (done) to detect cycles.
    When a GRAY node is revisited, we trace back through the stack to build the cycle.

    Args:
        tasks: List of task dictionaries
        cycle_ids: List of task IDs involved in cycles

    Returns:
        List of cycle paths as strings (e.g., ["T004 → T005 → T004"])
    """
    if not cycle_ids:
        return []

    # Build reverse dependency graph for DFS
    task_map = {t["id"]: t for t in tasks}
    graph: Dict[str, Set[str]] = defaultdict(set)

    for task in tasks:
        tid = task["id"]
        for dep in task.get("depends_on", []):
            if dep in task_map:
                graph[tid].add(dep)  # tid depends on dep

    # Color tracking: WHITE=0, GRAY=1, BLACK=2
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in cycle_ids}
    paths = []

    def dfs(node: str, stack: List[str]) -> bool:
        """DFS with cycle detection. Returns True if cycle found."""
        color[node] = GRAY
        stack.append(node)

        for neighbor in graph[node]:
            if neighbor not in cycle_ids:
                continue

            if color[neighbor] == GRAY:
                # Found cycle! Build path from stack
                cycle_start_idx = stack.index(neighbor)
                cycle_path = stack[cycle_start_idx:] + [neighbor]
                paths.append(" → ".join(cycle_path))
                return True
            elif color[neighbor] == WHITE:
                if dfs(neighbor, stack):
                    return True

        stack.pop()
        color[node] = BLACK
        return False

    # Try DFS from each unvisited node in cycle_ids
    for tid in cycle_ids:
        if color[tid] == WHITE:
            if dfs(tid, []):
                break  # Found one cycle, that's enough

    return paths


def topological_sort_waves(
    tasks: List[dict],
    max_parallel: int = 7,
) -> List[List[str]]:
    """Kahn's algorithm with wave grouping.

    Groups ALL independent tasks (in-degree 0) into the same wave.
    Respects max_parallel limit by splitting large waves.

    Returns list of waves, each wave is a list of task IDs.
    """
    graph, in_degree = build_graph(tasks)
    queue = deque(tid for tid, deg in in_degree.items() if deg == 0)
    waves: List[List[str]] = []

    while queue:
        # All current in-degree=0 tasks form one wave
        current_wave = sorted(queue)  # Sort for determinism
        queue.clear()

        # Split into sub-waves if exceeding max_parallel
        for i in range(0, len(current_wave), max_parallel):
            waves.append(current_wave[i : i + max_parallel])

        # Update in-degrees for dependents
        for tid in current_wave:
            for dependent in graph[tid]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

    return waves


def calculate_critical_path(tasks: List[dict]) -> List[str]:
    """Calculate the critical path (longest chain of dependencies)."""
    task_map = {t["id"]: t for t in tasks}
    graph, _ = build_graph(tasks)

    # Calculate longest path to each node
    longest = {t["id"]: 0 for t in tasks}
    predecessor = {t["id"]: None for t in tasks}

    waves = topological_sort_waves(tasks, max_parallel=999)
    for wave in waves:
        for tid in wave:
            for dependent in graph[tid]:
                if longest[tid] + 1 > longest[dependent]:
                    longest[dependent] = longest[tid] + 1
                    predecessor[dependent] = tid

    # Find the end of the critical path
    end_task = max(longest, key=longest.get)
    path = []
    current = end_task
    while current is not None:
        path.append(current)
        current = predecessor[current]
    path.reverse()

    return path


def optimize(
    tasks: List[dict],
    max_parallel: int = 7,
) -> dict:
    """Full wave optimization: detect cycles, sort, calculate metrics."""
    # Check for cycles first
    cycles = detect_cycles(tasks)
    if cycles:
        cycle_paths = reconstruct_cycle_path(tasks, cycles)
        return {
            "error": "CIRCULAR_DEPENDENCY",
            "cycle_tasks": cycles,
            "cycle_path": cycle_paths,
            "message": f"Circular dependency detected involving: {', '.join(cycles)}",
        }

    waves = topological_sort_waves(tasks, max_parallel)
    critical_path = calculate_critical_path(tasks)

    # Build task lookup for metadata
    task_map = {t["id"]: t for t in tasks}

    wave_details = []
    for i, wave in enumerate(waves, 1):
        wave_details.append({
            "wave_num": i,
            "task_ids": wave,
            "task_count": len(wave),
            "tasks": [
                {
                    "id": tid,
                    "description": task_map[tid].get("description", ""),
                    "model": task_map[tid].get("model", "haiku"),
                    "domain": task_map[tid].get("domain", "unknown"),
                }
                for tid in wave
            ],
        })

    return {
        "total_tasks": len(tasks),
        "total_waves": len(waves),
        "max_parallel_per_wave": max(len(w) for w in waves) if waves else 0,
        "critical_path": critical_path,
        "critical_path_length": len(critical_path),
        "optimization_ratio": f"{len(tasks)}/{len(waves)} tasks/waves",
        "waves": wave_details,
    }


def main():
    parser = argparse.ArgumentParser(description="DAG-based wave optimizer for dispatch")
    parser.add_argument("input", help="Path to tasks JSON file")
    parser.add_argument("--check-cycles", action="store_true", help="Only check for cycles")
    parser.add_argument("--check-cycles-json", action="store_true", help="Check for cycles and output JSON")
    parser.add_argument("--max-parallel", type=int, default=7, help="Max parallel tasks per wave")
    parser.add_argument("--output", help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    tasks = data.get("tasks", [])

    if args.check_cycles_json:
        cycles = detect_cycles(tasks)
        cycle_paths = reconstruct_cycle_path(tasks, cycles) if cycles else []

        result = {
            "has_cycles": bool(cycles),
            "cycle_tasks": cycles,
            "cycle_path": cycle_paths,
        }

        if cycles:
            result["message"] = "Circular dependency detected"

        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1 if cycles else 0)

    if args.check_cycles:
        cycles = detect_cycles(tasks)
        cycle_paths = reconstruct_cycle_path(tasks, cycles) if cycles else []

        if cycles:
            print(f"CYCLES DETECTED: {', '.join(cycles)}", file=sys.stderr)
            if cycle_paths:
                print(f"CYCLE PATH: {cycle_paths[0]}", file=sys.stderr)
            sys.exit(1)
        else:
            print("No cycles detected.")
            sys.exit(0)

    result = optimize(tasks, max_parallel=args.max_parallel)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Waves written to {args.output}")
    else:
        print(output)

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
