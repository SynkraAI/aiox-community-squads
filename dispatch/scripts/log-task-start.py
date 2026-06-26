#!/usr/bin/env python3
"""
Dispatch Squad — Hook: SubagentStart
Logs task start to events.jsonl for wave progress tracking.

Triggered by Claude Code SubagentStart hook.
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


def main():
    run_dir = find_active_run()
    if not run_dir:
        sys.exit(0)  # No active dispatch, nothing to log

    event = {
        "ts": datetime.now().isoformat(),
        "event": "task_started",
        "source": "hook:SubagentStart",
    }

    events_path = run_dir / "events.jsonl"
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


if __name__ == "__main__":
    main()
