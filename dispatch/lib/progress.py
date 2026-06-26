"""
Dispatch Squad — Progress Tracker
Source: PRD Section 11 + Section 12

Provides human-readable progress display for dispatch runs.
Saves consolidated learnings to progress.txt (max 5 key learnings).

Format matches Claude Code Task tool output:
  ● N Task agents finished (ctrl+o to expand)
    ├─ US-001: Description · N tool uses · Nk tokens
    │  └ Done
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ProgressTracker:
    """Tracks and displays dispatch progress.

    Usage:
        tracker = ProgressTracker("_temp/dispatch/runs/dispatch-20260209-143000")
        tracker.start_wave(1, ["task-001", "task-002", "task-003"])
        tracker.complete_task("task-001", cost=0.003, tokens=2100)
        tracker.complete_wave(1, total_cost=0.009)
        tracker.save_learnings(["Haiku needs templates for > 50 lines"])
    """

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.progress_path = self.run_dir / "progress.txt"
        self.run_dir.mkdir(parents=True, exist_ok=True)

    # ─── WAVE DISPLAY ─────────────────────────────────────────────────────

    def format_wave_start(
        self,
        wave_num: int,
        task_count: int,
        task_descriptions: Optional[List[str]] = None,
    ) -> str:
        """Format wave start message."""
        lines = [f"● WAVE {wave_num}: Executing {task_count} tasks in PARALLEL"]
        if task_descriptions:
            for desc in task_descriptions:
                lines.append(f"  ├─ {desc}")
        return "\n".join(lines)

    def format_wave_complete(
        self,
        wave_num: int,
        results: List[Dict],
        total_waves: int,
        completed_tasks: int,
        total_tasks: int,
    ) -> str:
        """Format wave completion message matching Claude Code output."""
        lines = []

        # Task results
        passed = [r for r in results if r.get("status") == "pass"]
        failed = [r for r in results if r.get("status") == "fail"]

        lines.append(f"● {len(results)} Task agents finished")
        for i, r in enumerate(results):
            connector = "└─" if i == len(results) - 1 else "├─"
            status = "Done" if r.get("status") == "pass" else f"FAILED: {r.get('error', 'unknown')}"
            tokens_str = f"{r.get('tokens', 0) / 1000:.1f}k tokens" if r.get("tokens") else ""
            lines.append(f"  {connector} {r.get('task_id', '???')}: {r.get('description', '')} · {tokens_str}")
            lines.append(f"     └ {status}")

        # Wave summary box
        lines.append("")
        lines.append(f"┌{'─' * 58}┐")
        lines.append(f"│ WAVE {wave_num} COMPLETE {'✓' if not failed else '⚠'}{'':>44}│")
        lines.append(f"│{'':>58}│")
        for r in passed:
            desc = r.get("description", "")[:50]
            lines.append(f"│ ✓ {r.get('task_id', '')}: {desc:<51}│")
        for r in failed:
            desc = r.get("description", "")[:50]
            lines.append(f"│ ✗ {r.get('task_id', '')}: {desc:<51}│")
        lines.append(f"│{'':>58}│")
        lines.append(f"│ Progress: {completed_tasks}/{total_tasks} tasks{'':>36}│")
        if wave_num < total_waves:
            lines.append(f"│ Starting Wave {wave_num + 1}...{'':>38}│")
        else:
            lines.append(f"│ All waves complete!{'':>38}│")
        lines.append(f"└{'─' * 58}┘")

        return "\n".join(lines)

    # ─── PLAN DISPLAY ─────────────────────────────────────────────────────

    def format_plan_summary(
        self,
        description: str,
        task_count: int,
        haiku_count: int,
        sonnet_count: int,
        worker_count: int,
        wave_count: int,
        domains: List[str],
        estimated_cost: float,
        estimated_time_min: float,
        gate_status: str = "ALL PASS",
    ) -> str:
        """Format execution plan summary box."""
        lines = []
        model_str = []
        if haiku_count:
            model_str.append(f"{haiku_count} Haiku")
        if sonnet_count:
            model_str.append(f"{sonnet_count} Sonnet")
        if worker_count:
            model_str.append(f"{worker_count} Worker")

        lines.append(f"┌{'─' * 50}┐")
        lines.append(f"│ Dispatch Plan: {description[:33]:<34}│")
        lines.append(f"├{'─' * 50}┤")
        lines.append(f"│ Tasks: {task_count} ({', '.join(model_str)}){'':>10}│")
        lines.append(f"│ Domains: {', '.join(domains)[:39]:<40}│")
        lines.append(f"│ Waves: {wave_count:<42}│")
        lines.append(f"│ Estimated cost: ${estimated_cost:.3f}{'':>30}│")
        lines.append(f"│ Estimated time: ~{estimated_time_min:.0f} min{'':>28}│")
        lines.append(f"│ Quality gate: {'✅' if gate_status == 'ALL PASS' else '❌'} {gate_status:<36}│")
        lines.append(f"└{'─' * 50}┘")

        return "\n".join(lines)

    # ─── RESUME DISPLAY ───────────────────────────────────────────────────

    def format_resume_context(
        self,
        run_id: str,
        last_wave: int,
        total_waves: int,
        completed_tasks: int,
        pending_tasks: int,
        cost_so_far: float,
        failed_count: int,
    ) -> str:
        """Format resume context box."""
        lines = []
        lines.append(f"┌{'─' * 50}┐")
        lines.append(f"│ Resuming: {run_id:<39}│")
        lines.append(f"│ Last good wave: {last_wave}/{total_waves} ({completed_tasks} tasks complete){'':>5}│")
        lines.append(f"│ Pending: {pending_tasks} tasks in waves {last_wave + 1}-{total_waves}{'':>15}│")
        lines.append(f"│ Cost so far: ${cost_so_far:.3f}{'':>33}│")
        if failed_count:
            lines.append(f"│ Failed tasks: {failed_count} (will retry){'':>22}│")
        lines.append(f"└{'─' * 50}┘")
        return "\n".join(lines)

    # ─── LEARNINGS ────────────────────────────────────────────────────────

    def save_learnings(self, learnings: List[str]) -> None:
        """Save consolidated learnings to progress.txt (max 5)."""
        content = f"# Dispatch Run Learnings\n# Updated: {datetime.now().isoformat()}\n\n"
        for i, learning in enumerate(learnings[:5], 1):
            content += f"{i}. {learning}\n"
        with open(self.progress_path, "w", encoding="utf-8") as f:
            f.write(content)

    def load_learnings(self) -> List[str]:
        """Load learnings from progress.txt."""
        if not self.progress_path.exists():
            return []
        learnings = []
        with open(self.progress_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and line[0].isdigit():
                    # Remove "1. " prefix
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        learnings.append(parts[1])
        return learnings
