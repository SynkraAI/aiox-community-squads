"""
Dispatch Squad — Pipeline State Management
Source: PRD Section 11 (Pipeline Patterns)

Provides:
- DispatchState: Complete state for a dispatch run
- WaveState: State per wave
- TaskState: State per task
- DispatchStateManager: Load/save/update state from JSON

State is persisted to JSON after EVERY event for crash recovery.
Location: _temp/dispatch/runs/{run_id}/state.json
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class TaskState:
    """State for a single atomic task in the dispatch pipeline."""

    task_id: str
    description: str
    agent: str  # Slash command path (e.g., /copy:tasks:create-sales-page)
    model: str  # haiku | sonnet | worker
    enrichment: str  # MINIMAL | STANDARD | FULL
    executor_type: str  # Worker | Agent | Hybrid
    status: str = "pending"  # pending | queued | executing | pass | fail | retry
    wave: int = 0
    attempts: int = 0
    max_attempts: int = 3
    output_path: Optional[str] = None
    cost_usd: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    timeout: int = 120  # seconds
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    veto_results: Dict[str, bool] = field(default_factory=dict)
    prediction: Optional[str] = None  # Deming PDSA

    @property
    def is_complete(self) -> bool:
        return self.status in ("pass", "fail")

    @property
    def is_retriable(self) -> bool:
        return self.status == "fail" and self.attempts < self.max_attempts


@dataclass
class WaveState:
    """State for a single wave (group of parallel tasks)."""

    wave_num: int
    status: str = "pending"  # pending | executing | complete | failed
    task_ids: List[str] = field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    prediction: Optional[str] = None  # Deming PDSA
    cost_usd: float = 0.0

    @property
    def is_complete(self) -> bool:
        return self.status in ("complete", "failed")


@dataclass
class DispatchState:
    """Complete state for a dispatch run."""

    run_id: str  # dispatch-YYYYMMDD-HHMMSS
    description: str
    input_type: str  # story | prd | free_text | batch
    input_path: Optional[str] = None
    status: str = "planning"  # planning | executing | paused | complete | failed | aborted
    current_wave: int = 0
    total_waves: int = 0
    started_at: str = ""
    last_updated: str = ""
    waves: Dict[int, dict] = field(default_factory=dict)
    tasks: Dict[str, dict] = field(default_factory=dict)
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    total_cost_usd: float = 0.0
    health_score: Optional[int] = None  # 0-12
    learnings: List[str] = field(default_factory=list)
    domains_used: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.started_at:
            self.started_at = datetime.now().isoformat()
        if not self.last_updated:
            self.last_updated = self.started_at


# ═══════════════════════════════════════════════════════════════════════════════
# STATE MANAGER
# ═══════════════════════════════════════════════════════════════════════════════


class DispatchStateManager:
    """Manages dispatch state persistence to JSON.

    State is saved after EVERY event for crash recovery.
    Location: _temp/dispatch/runs/{run_id}/state.json
    """

    BASE_DIR = "_temp/dispatch/runs"

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.base_dir = self.project_root / self.BASE_DIR

    def _run_dir(self, run_id: str) -> Path:
        return self.base_dir / run_id

    def _state_path(self, run_id: str) -> Path:
        return self._run_dir(run_id) / "state.json"

    # ─── CREATE ───────────────────────────────────────────────────────────

    def create_run(
        self,
        description: str,
        input_type: str,
        input_path: Optional[str] = None,
    ) -> DispatchState:
        """Create a new dispatch run with fresh state."""
        run_id = f"dispatch-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        state = DispatchState(
            run_id=run_id,
            description=description,
            input_type=input_type,
            input_path=input_path,
        )

        # Create run directory with wave subdirs
        run_dir = self._run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)

        self.save(state)
        return state

    # ─── SAVE / LOAD ─────────────────────────────────────────────────────

    def save(self, state: DispatchState) -> None:
        """Save state to JSON. Called after EVERY event."""
        state.last_updated = datetime.now().isoformat()
        path = self._state_path(state.run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(state), f, indent=2, ensure_ascii=False)

    def load(self, run_id: str) -> Optional[DispatchState]:
        """Load state from JSON."""
        path = self._state_path(run_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return DispatchState(**data)

    # ─── QUERY ────────────────────────────────────────────────────────────

    def list_runs(self, status_filter: Optional[str] = None) -> List[dict]:
        """List all dispatch runs, optionally filtered by status."""
        runs = []
        if not self.base_dir.exists():
            return runs

        for run_dir in sorted(self.base_dir.iterdir(), reverse=True):
            state_path = run_dir / "state.json"
            if state_path.exists():
                with open(state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if status_filter is None or data.get("status") == status_filter:
                    runs.append({
                        "run_id": data["run_id"],
                        "description": data["description"],
                        "status": data["status"],
                        "current_wave": data.get("current_wave", 0),
                        "total_waves": data.get("total_waves", 0),
                        "total_cost_usd": data.get("total_cost_usd", 0.0),
                        "started_at": data.get("started_at", ""),
                    })
        return runs

    def find_resumable(self) -> List[dict]:
        """Find runs that can be resumed (not complete/aborted)."""
        return self.list_runs(status_filter=None)

    # ─── UPDATE HELPERS ───────────────────────────────────────────────────

    def update_task(
        self,
        state: DispatchState,
        task_id: str,
        **kwargs,
    ) -> None:
        """Update a task's state and save."""
        if task_id in state.tasks:
            state.tasks[task_id].update(kwargs)
        self.save(state)

    def update_wave(
        self,
        state: DispatchState,
        wave_num: int,
        **kwargs,
    ) -> None:
        """Update a wave's state and save."""
        wave_key = str(wave_num)
        if wave_key in state.waves:
            state.waves[wave_key].update(kwargs)
        self.save(state)

    def add_learning(self, state: DispatchState, learning: str) -> None:
        """Add a learning from this run."""
        state.learnings.append(learning)
        if len(state.learnings) > 10:
            state.learnings = state.learnings[-10:]  # Keep last 10
        self.save(state)

    # ─── WAVE DIRECTORY MANAGEMENT ────────────────────────────────────────

    def create_wave_dir(self, run_id: str, wave_num: int) -> Path:
        """Create directory for wave artifacts."""
        wave_dir = self._run_dir(run_id) / f"wave_{wave_num:03d}"
        wave_dir.mkdir(parents=True, exist_ok=True)
        return wave_dir

    def get_wave_dir(self, run_id: str, wave_num: int) -> Path:
        """Get wave directory path."""
        return self._run_dir(run_id) / f"wave_{wave_num:03d}"
