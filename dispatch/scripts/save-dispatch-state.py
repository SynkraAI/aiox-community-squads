#!/usr/bin/env python3
"""
Dispatch Squad — Hook: PreCompact
Auto-saves dispatch state before Claude Code compacts the context.
Ensures dispatch can resume after compaction.

Triggered by Claude Code PreCompact hook.
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
            if state.get("status") in ("executing", "planning"):
                return run_dir
    return None


def main():
    run_dir = find_active_run()
    if not run_dir:
        sys.exit(0)

    state_path = run_dir / "state.json"
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    # Mark state as saved before compaction
    state["last_updated"] = datetime.now().isoformat()

    # Save backup
    backup_path = run_dir / "state.pre-compact.json"
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    # Log event
    event = {
        "ts": datetime.now().isoformat(),
        "event": "state_saved_pre_compact",
        "source": "hook:PreCompact",
        "run_id": state.get("run_id"),
        "current_wave": state.get("current_wave"),
    }

    events_path = run_dir / "events.jsonl"
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    print(f"Dispatch state saved: {backup_path}")


if __name__ == "__main__":
    main()
