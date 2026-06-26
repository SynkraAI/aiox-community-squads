#!/usr/bin/env python3
"""
Dispatch Squad — Hook: SubagentStop
Checks if current wave is complete after a subagent finishes.
If complete, logs wave_completed event.

Triggered by Claude Code SubagentStop hook.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def find_active_run() -> Path:
    """Find the most recent active dispatch run."""
    runs_dir = Path("_temp/dispatch/runs")
    if not runs_dir.exists():
        return None

    for run_dir in sorted(runs_dir.iterdir(), reverse=True):
        state_path = run_dir / "state.json"
        if state_path.exists():
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            if state.get("status") == "executing":
                return run_dir
    return None


def check_wave_completion(run_dir: Path) -> bool:
    """Check if the current wave has all tasks completed."""
    state_path = run_dir / "state.json"
    if not state_path.exists():
        return False

    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    current_wave = str(state.get("current_wave", 0))
    wave = state.get("waves", {}).get(current_wave, {})
    task_ids = wave.get("task_ids", [])

    if not task_ids:
        return False

    tasks = state.get("tasks", {})
    completed = sum(
        1 for tid in task_ids
        if tasks.get(tid, {}).get("status") in ("pass", "fail")
    )

    return completed >= len(task_ids)


def main():
    run_dir = find_active_run()
    if not run_dir:
        sys.exit(0)

    if check_wave_completion(run_dir):
        event = {
            "ts": datetime.now().isoformat(),
            "event": "wave_check_complete",
            "source": "hook:SubagentStop",
            "message": "All tasks in current wave finished",
        }

        events_path = run_dir / "events.jsonl"
        with open(events_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")


if __name__ == "__main__":
    main()
