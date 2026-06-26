#!/usr/bin/env python3
"""
Dispatch Squad — Hook: PostToolUseFailure (Task)
Logs task failures for retry logic and diagnostics.

Triggered by Claude Code PostToolUseFailure hook (Task matcher).
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
        sys.exit(0)

    # Log failure event
    event = {
        "ts": datetime.now().isoformat(),
        "event": "task_failure_detected",
        "source": "hook:PostToolUseFailure",
    }

    events_path = run_dir / "events.jsonl"
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    # Check circuit breaker: 5 consecutive failures
    events = []
    with open(events_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    # Count recent consecutive failures
    recent_failures = 0
    for e in reversed(events):
        if e.get("event") in ("task_failure_detected", "task_failed"):
            recent_failures += 1
        elif e.get("event") in ("task_completed", "wave_completed"):
            break

    if recent_failures >= 5:
        circuit_event = {
            "ts": datetime.now().isoformat(),
            "event": "circuit_breaker_triggered",
            "source": "hook:PostToolUseFailure",
            "consecutive_failures": recent_failures,
            "message": "5+ consecutive failures — dispatch should be halted",
        }
        with open(events_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(circuit_event) + "\n")

        print(f"⚠️ CIRCUIT BREAKER: {recent_failures} consecutive task failures detected")


if __name__ == "__main__":
    main()
