"""
Dispatch Squad — Pydantic v2 Models
Source: PRD Section 3.7 + 9.2 + 10.4 + 11 (Pipeline Patterns)

Provides typed, validated models for all dispatch squad YAML/JSON schemas:
- Enums: RunStatus, WaveStatus, TaskStatus, ModelType, etc.
- TaskModel: Atomic task with validation, computed properties
- WaveModel: Wave (group of parallel tasks)
- DispatchRunModel: Complete run state
- VetoCondition: Formal blocking conditions
- ModelSelectionRules: Model selection decision tree
- Config validators: validate_yaml_file()

All models use Pydantic v2 with strict validation.

Quick Usage:
    # Create a task
    task = TaskModel(
        task_id="T001",
        description="Create email",
        agent="/copy:tasks:create-email",
        model=ModelType.haiku,
        wave=1
    )

    # Create a wave
    wave = WaveModel(wave_num=1, task_ids=["T001", "T002"])

    # Create a run
    run = DispatchRunModel(
        run_id="dispatch-20260211-143000",
        description="Email campaign",
        input_type=InputType.story
    )
    run.tasks["T001"] = task
    run.waves["1"] = wave

    # Save/load run state
    run.save(Path("_temp/dispatch/runs/dispatch-20260211-143000/state.json"))
    loaded = DispatchRunModel.load(Path("_temp/dispatch/runs/..."))

    # Validate YAML files
    valid, errors = validate_yaml_file(
        Path("data/veto-conditions.yaml"),
        VetoCondition,
        extract_items=True
    )

    # Load configurations
    rules = load_model_selection_rules(Path("data/model-selection-rules.yaml"))
    vetos = load_veto_conditions(Path("data/veto-conditions.yaml"))
"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, computed_field, field_validator


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════


class RunStatus(str, Enum):
    """Status of a dispatch run."""

    planning = "planning"
    executing = "executing"
    paused = "paused"
    complete = "complete"
    failed = "failed"
    aborted = "aborted"


class WaveStatus(str, Enum):
    """Status of a wave (group of parallel tasks)."""

    pending = "pending"
    executing = "executing"
    complete = "complete"
    failed = "failed"


class TaskStatus(str, Enum):
    """Status of a single task. Note: 'pass' is reserved word, using 'pass_' with alias."""

    pending = "pending"
    queued = "queued"
    executing = "executing"
    pass_ = "pass"
    fail = "fail"
    retry = "retry"


class ModelType(str, Enum):
    """Claude model type for task execution."""

    haiku = "haiku"
    sonnet = "sonnet"
    opus = "opus"
    worker = "worker"  # Script-based execution, no LLM


class EnrichmentLevel(str, Enum):
    """Context enrichment level for task execution."""

    MINIMAL = "MINIMAL"  # Basic task description only
    STANDARD = "STANDARD"  # Task + domain context
    FULL = "FULL"  # Task + domain + cross-references


class ExecutorType(str, Enum):
    """Type of executor for task."""

    Agent = "Agent"  # Claude agent (Haiku/Sonnet/Opus)
    Worker = "Worker"  # Script-based execution


class InputType(str, Enum):
    """Type of input for dispatch run."""

    story = "story"
    prd = "prd"
    free_text = "free_text"
    batch = "batch"


class VetoSeverity(str, Enum):
    """Severity of veto condition."""

    soft_block = "soft_block"  # Redirect with recommendation
    hard_block = "hard_block"  # Block execution, require fix
    warning = "warning"  # Log but allow execution


# ═══════════════════════════════════════════════════════════════════════════════
# TASK MODEL
# ═══════════════════════════════════════════════════════════════════════════════


class TaskModel(BaseModel):
    """State for a single atomic task in the dispatch pipeline.

    Source: PRD Section 11 (Pipeline Patterns)
    """

    task_id: str
    description: str
    agent: str = Field(
        ..., description="Slash command path (e.g., /copy:tasks:create-sales-page)"
    )
    model: ModelType
    enrichment: EnrichmentLevel = EnrichmentLevel.MINIMAL
    executor_type: ExecutorType = ExecutorType.Agent
    status: TaskStatus = TaskStatus.pending
    wave: int = Field(0, ge=0)
    attempts: int = Field(0, ge=0)
    max_attempts: int = Field(2, ge=1)
    output_path: str = ""
    cost_usd: float = Field(0.0, ge=0.0)
    tokens_in: int = Field(0, ge=0)
    tokens_out: int = Field(0, ge=0)
    timeout: int = Field(120, ge=1)
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    veto_results: dict[str, bool] = Field(default_factory=dict)
    prediction: str = ""  # Deming PDSA

    model_config = {"use_enum_values": True}

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Task is in terminal state (pass or fail)."""
        return self.status in (TaskStatus.pass_, TaskStatus.fail)

    @computed_field
    @property
    def is_retriable(self) -> bool:
        """Task can be retried (failed but under max attempts)."""
        return self.status == TaskStatus.fail and self.attempts < self.max_attempts

    @computed_field
    @property
    def duration_seconds(self) -> float | None:
        """Duration in seconds if both started_at and completed_at are set."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def model_dump_json(self, **kwargs) -> str:
        """Override to handle TaskStatus.pass_ -> 'pass' serialization."""
        data = self.model_dump(**kwargs)
        # Convert pass_ back to pass for JSON
        if data.get("status") == "pass":
            pass  # Already correct
        return json.dumps(data, default=str, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# WAVE MODEL
# ═══════════════════════════════════════════════════════════════════════════════


class WaveModel(BaseModel):
    """State for a single wave (group of parallel tasks).

    Source: PRD Section 11 (Pipeline Patterns)
    """

    wave_num: int = Field(..., ge=1)
    status: WaveStatus = WaveStatus.pending
    task_ids: list[str] = Field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    prediction: str = ""  # Deming PDSA
    cost_usd: float = Field(0.0, ge=0.0)

    model_config = {"use_enum_values": True}

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Wave is in terminal state."""
        return self.status in (WaveStatus.complete, WaveStatus.failed)


# ═══════════════════════════════════════════════════════════════════════════════
# DISPATCH RUN MODEL
# ═══════════════════════════════════════════════════════════════════════════════


class DispatchRunModel(BaseModel):
    """Complete state for a dispatch run.

    Source: PRD Section 11 (Pipeline Patterns)
    Persisted to: _temp/dispatch/runs/{run_id}/state.json
    """

    run_id: str
    description: str
    input_type: InputType
    input_path: str | None = None
    status: RunStatus = RunStatus.planning
    current_wave: int = Field(0, ge=0)
    total_waves: int = Field(0, ge=0)
    started_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    waves: dict[str, WaveModel] = Field(default_factory=dict)
    tasks: dict[str, TaskModel] = Field(default_factory=dict)
    total_tokens_in: int = Field(0, ge=0)
    total_tokens_out: int = Field(0, ge=0)
    total_cost_usd: float = Field(0.0, ge=0.0)
    health_score: float | None = Field(None, ge=0.0, le=12.0)
    learnings: list[str] = Field(default_factory=list)
    domains_used: list[str] = Field(default_factory=list)

    model_config = {"use_enum_values": True}

    def save(self, path: Path) -> None:
        """Save run state to JSON file."""
        self.last_updated = datetime.now()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            # Use model_dump with custom serialization for datetime
            data = self.model_dump(mode="json")
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    @classmethod
    def load(cls, path: Path) -> DispatchRunModel:
        """Load run state from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def task_summary(self) -> dict[str, int]:
        """Get task counts by status."""
        summary: dict[str, int] = {
            "pending": 0,
            "queued": 0,
            "executing": 0,
            "pass": 0,
            "fail": 0,
            "retry": 0,
        }
        for task in self.tasks.values():
            status = task.status.value if isinstance(task.status, TaskStatus) else task.status
            # Handle pass_ -> pass
            if status == "pass":
                summary["pass"] += 1
            elif status in summary:
                summary[status] += 1
        return summary


# ═══════════════════════════════════════════════════════════════════════════════
# VETO CONDITION MODEL
# ═══════════════════════════════════════════════════════════════════════════════


class VetoCondition(BaseModel):
    """Formal blocking condition for dispatch quality gates.

    Source: PRD Section 9.2 (Pedro Valério patterns)
    Pattern: "Se o executor CONSEGUE fazer errado, VAI fazer errado"
    """

    id: str = Field(..., pattern=r"^V\d+(\.\d+)+$", description="Veto ID (e.g., V0.1, V1.2)")
    condition: str = Field(..., min_length=10, description="What triggers this veto")
    check: str = Field(..., min_length=5, description="How to verify condition")
    action: str = Field(..., min_length=10, description="What to do when triggered")
    severity: VetoSeverity
    examples: dict[str, list[str]] | None = Field(
        None, description="Optional examples (bad/good)"
    )
    source: str | None = Field(None, description="Source of this veto (e.g., 'Pedro Valério PV002')")

    model_config = {"use_enum_values": True}


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL SELECTION RULES
# ═══════════════════════════════════════════════════════════════════════════════


class ModelRule(BaseModel):
    """Rules for when to use a specific model."""

    when: list[str] = Field(default_factory=list, description="Conditions for using this model")
    cost: str = Field(..., description="Cost estimate for this model")
    timeout: int = Field(..., ge=1, description="Timeout in seconds")
    constraints: list[str] | None = Field(
        None, description="Constraints when using this model"
    )
    note: str | None = Field(None, description="Additional notes")


class PromptCachingConfig(BaseModel):
    """Prompt caching strategy configuration."""

    strategy: str = Field(..., description="Caching strategy description")
    static_prefix: list[str] = Field(
        default_factory=list, description="Static prefix components"
    )
    dynamic_suffix: list[str] = Field(
        default_factory=list, description="Dynamic suffix components"
    )
    savings: dict[str, str] = Field(
        default_factory=dict, description="Expected savings by scenario"
    )
    cache_pricing: dict[str, str] = Field(
        default_factory=dict, description="Cache pricing by model"
    )


class RateLimitConfig(BaseModel):
    """Rate limit configuration for dispatch."""

    minimum_tier: int = Field(..., ge=1, le=5, description="Minimum Anthropic tier required")
    tier_2: dict[str, int] = Field(..., description="Tier 2 rate limits")
    per_wave_budget: dict[str, int] = Field(..., description="Per-wave budget constraints")
    note: str | None = Field(None, description="Additional notes")


class ModelSelectionRules(BaseModel):
    """Complete model selection rules.

    Source: PRD Section 3.7 + Section 10.4
    File: squads/dispatch/data/model-selection-rules.yaml
    """

    rules: dict[str, ModelRule] = Field(
        ..., description="Rules by model type (worker, haiku, sonnet, opus)"
    )
    decision_tree: dict[str, dict[str | bool, str]] = Field(
        ..., description="Decision tree for model selection (keys can be 'yes'/'no' or booleans)"
    )
    prompt_caching: PromptCachingConfig
    rate_limits: RateLimitConfig

    @field_validator("rules")
    @classmethod
    def validate_required_models(cls, v: dict[str, ModelRule]) -> dict[str, ModelRule]:
        """Ensure all required model types are present."""
        required = {"worker", "haiku", "sonnet", "opus"}
        missing = required - set(v.keys())
        if missing:
            raise ValueError(f"Missing required model rules: {missing}")
        return v


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG VALIDATORS
# ═══════════════════════════════════════════════════════════════════════════════


def validate_yaml_file(
    path: Path,
    model_class: type[BaseModel],
    extract_items: bool = False,
) -> tuple[bool, list[str]]:
    """Load YAML file and validate against Pydantic model.

    Args:
        path: Path to YAML file
        model_class: Pydantic model class to validate against
        extract_items: If True and data is dict with lists, validate each item in lists

    Returns:
        Tuple of (valid: bool, errors: list[str])

    Example:
        >>> # Validate single model
        >>> valid, errors = validate_yaml_file(
        ...     Path("data/model-selection-rules.yaml"),
        ...     ModelSelectionRules
        ... )
        >>> # Validate list items (e.g., veto conditions organized by category)
        >>> valid, errors = validate_yaml_file(
        ...     Path("data/veto-conditions.yaml"),
        ...     VetoCondition,
        ...     extract_items=True
        ... )
    """
    errors = []

    # Check file exists
    if not path.exists():
        return False, [f"File not found: {path}"]

    # Load YAML
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parse error: {e}"]
    except Exception as e:
        return False, [f"Failed to read file: {e}"]

    # Validate against model
    try:
        if isinstance(data, list):
            # List of items (e.g., direct list of models)
            for i, item in enumerate(data):
                try:
                    model_class(**item)
                except Exception as e:
                    errors.append(f"Item {i}: {e}")
        elif isinstance(data, dict):
            if extract_items:
                # Extract items from nested structure (e.g., veto conditions by category)
                item_count = 0
                for category, items in data.items():
                    if isinstance(items, list):
                        for i, item in enumerate(items):
                            try:
                                model_class(**item)
                                item_count += 1
                            except Exception as e:
                                errors.append(f"{category}[{i}]: {e}")
                if item_count == 0:
                    errors.append("No items found to validate in nested structure")
            else:
                # Single item or complete structure
                try:
                    model_class(**data)
                except Exception as e:
                    errors.append(str(e))
        else:
            errors.append(f"Unexpected data type: {type(data)}")
    except Exception as e:
        errors.append(f"Validation error: {e}")

    return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: Load Veto Conditions from YAML
# ═══════════════════════════════════════════════════════════════════════════════


def load_veto_conditions(path: Path) -> list[VetoCondition]:
    """Load and validate veto conditions from YAML.

    Args:
        path: Path to veto-conditions.yaml

    Returns:
        List of validated VetoCondition objects

    Raises:
        ValueError: If validation fails
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    conditions = []

    # Veto conditions are organized by category (sufficiency, pre_execution, post_execution)
    for category, items in data.items():
        if category == "validation_script":
            continue  # Skip validation script metadata
        if isinstance(items, list):
            for item in items:
                conditions.append(VetoCondition(**item))

    return conditions


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: Load Model Selection Rules from YAML
# ═══════════════════════════════════════════════════════════════════════════════


def load_model_selection_rules(path: Path) -> ModelSelectionRules:
    """Load and validate model selection rules from YAML.

    Args:
        path: Path to model-selection-rules.yaml

    Returns:
        Validated ModelSelectionRules object

    Raises:
        ValueError: If validation fails
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Remove feedback_loop section if present (not part of model)
    if "feedback_loop" in data:
        del data["feedback_loop"]

    return ModelSelectionRules(**data)
