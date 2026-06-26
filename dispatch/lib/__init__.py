# Dispatch Squad — Pipeline Library
# Provides state management, progress tracking, event logging,
# resilience patterns, typed models, and prompt caching optimization
# for the dispatch parallel execution engine.

from .pipeline_state import DispatchState, WaveState, TaskState, DispatchStateManager
from .event_log import EventLog
from .progress import ProgressTracker
from .cache_optimizer import CacheOptimizer, PromptStructure, estimate_cache_hit_rate
from .resilience import (
    RetryConfig,
    DispatchCircuitBreaker,
    create_retry_decorator,
    RETRY_API_CALL,
    RETRY_SCRIPT,
    RETRY_AGGRESSIVE,
)
from .dispatch_models import (
    RunStatus,
    WaveStatus,
    TaskStatus,
    ModelType,
    EnrichmentLevel,
    ExecutorType,
    InputType,
    VetoSeverity,
    TaskModel,
    WaveModel,
    DispatchRunModel,
    VetoCondition,
    validate_yaml_file,
)

__all__ = [
    # State management (original)
    "DispatchState",
    "WaveState",
    "TaskState",
    "DispatchStateManager",
    # Event logging
    "EventLog",
    # Progress display
    "ProgressTracker",
    # Cache optimization
    "CacheOptimizer",
    "PromptStructure",
    "estimate_cache_hit_rate",
    # Resilience (NEW)
    "RetryConfig",
    "DispatchCircuitBreaker",
    "create_retry_decorator",
    "RETRY_API_CALL",
    "RETRY_SCRIPT",
    "RETRY_AGGRESSIVE",
    # Typed models (NEW)
    "RunStatus",
    "WaveStatus",
    "TaskStatus",
    "ModelType",
    "EnrichmentLevel",
    "ExecutorType",
    "InputType",
    "VetoSeverity",
    "TaskModel",
    "WaveModel",
    "DispatchRunModel",
    "VetoCondition",
    "validate_yaml_file",
]
