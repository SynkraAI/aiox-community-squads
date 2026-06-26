"""
Dispatch Squad — Event Log (Audit Trail)
Source: PRD Section 11.3

Append-only event log for dispatch runs.
Format: JSONL (one JSON object per line)
Location: _temp/dispatch/runs/{run_id}/events.jsonl

Events:
- run_started, run_completed, run_failed, run_aborted
- wave_started, wave_completed, wave_failed
- task_queued, task_started, task_completed, task_failed, task_retry
- gate_passed, gate_failed
- cost_recorded
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class EventLog:
    """Append-only event log for dispatch audit trail.

    Usage:
        log = EventLog("_temp/dispatch/runs/dispatch-20260209-143000")
        log.emit("run_started", run_id="dispatch-20260209-143000", input="story.md")
        log.emit("task_completed", task="001", cost=0.003, model="haiku")
    """

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.log_path = self.run_dir / "events.jsonl"
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, **kwargs: Any) -> Dict[str, Any]:
        """Append an event to the log.

        Args:
            event: Event type (e.g., "run_started", "task_completed")
            **kwargs: Event-specific data

        Returns:
            The complete event record
        """
        record = {
            "ts": datetime.now().isoformat(),
            "event": event,
            **kwargs,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def read_all(self) -> List[Dict[str, Any]]:
        """Read all events from the log."""
        events = []
        if not self.log_path.exists():
            return events
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events

    def read_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """Read events filtered by type."""
        return [e for e in self.read_all() if e.get("event") == event_type]

    def read_by_task(self, task_id: str) -> List[Dict[str, Any]]:
        """Read events filtered by task ID."""
        return [e for e in self.read_all() if e.get("task") == task_id]

    def read_by_wave(self, wave_num: int) -> List[Dict[str, Any]]:
        """Read events filtered by wave number."""
        return [e for e in self.read_all() if e.get("wave") == wave_num]

    def summary(self) -> Dict[str, Any]:
        """Generate summary statistics from event log."""
        events = self.read_all()
        if not events:
            return {"total_events": 0}

        task_events = [e for e in events if e.get("event", "").startswith("task_")]
        completed = [e for e in task_events if e["event"] == "task_completed"]
        failed = [e for e in task_events if e["event"] == "task_failed"]
        retried = [e for e in task_events if e["event"] == "task_retry"]

        total_cost = sum(e.get("cost", 0) for e in completed)

        return {
            "total_events": len(events),
            "tasks_completed": len(completed),
            "tasks_failed": len(failed),
            "tasks_retried": len(retried),
            "total_cost_usd": round(total_cost, 4),
            "first_event": events[0]["ts"] if events else None,
            "last_event": events[-1]["ts"] if events else None,
            "domains_used": list(set(
                e.get("domain", "unknown")
                for e in completed
                if "domain" in e
            )),
        }

    @property
    def event_count(self) -> int:
        """Count total events without loading all."""
        if not self.log_path.exists():
            return 0
        with open(self.log_path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
