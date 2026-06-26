#!/usr/bin/env python3
"""
Dispatch Squad — Hook: SessionStart (after compact)
Re-injects dispatch context after Claude Code compacts the conversation.
Outputs a summary that gets injected into the new context.

Triggered by Claude Code SessionStart hook (compact matcher).
"""

import json
import os
import sys
from pathlib import Path


def find_active_run() -> Path:
    """Find the most recent active/paused dispatch run."""
    runs_dir = Path("_temp/dispatch/runs")
    if not runs_dir.exists():
        return None

    for run_dir in sorted(runs_dir.iterdir(), reverse=True):
        state_path = run_dir / "state.json"
        if state_path.exists():
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            if state.get("status") in ("executing", "planning", "paused"):
                return run_dir
    return None


def generate_context_summary(state: dict) -> str:
    """Generate compact context for re-injection (< 500 tokens)."""
    tasks = state.get("tasks", {})
    completed = sum(1 for t in tasks.values() if isinstance(t, dict) and t.get("status") == "pass")
    failed = sum(1 for t in tasks.values() if isinstance(t, dict) and t.get("status") == "fail")
    pending = sum(1 for t in tasks.values() if isinstance(t, dict) and t.get("status") in ("pending", "queued"))

    summary = f"""DISPATCH CONTEXT (re-injected after compaction):
Run: {state.get('run_id')}
Status: {state.get('status')}
Wave: {state.get('current_wave')}/{state.get('total_waves')}
Tasks: {completed} done, {failed} failed, {pending} pending
Cost: ${state.get('total_cost_usd', 0):.3f}
Input: {state.get('input_path', state.get('description', '')[:50])}
Use *resume to continue or *status for details."""

    return summary


def main():
    run_dir = find_active_run()
    if not run_dir:
        sys.exit(0)  # No active dispatch

    state_path = run_dir / "state.json"
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    summary = generate_context_summary(state)
    print(summary)


if __name__ == "__main__":
    main()
