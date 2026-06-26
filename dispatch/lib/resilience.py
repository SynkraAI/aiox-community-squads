"""Resilience utilities for dispatch squad — retry logic and circuit breakers.

Provides configurable retry with exponential backoff and circuit breaker pattern
for fault-tolerant task execution.

Dependencies:
    - tenacity: Retry logic with exponential backoff
    - pybreaker: Circuit breaker pattern

Usage:
    # Retry with default config
    @create_retry_decorator(RETRY_API_CALL)
    def call_api():
        ...

    # Circuit breaker per wave
    breaker = DispatchCircuitBreaker.for_wave(wave_num=1)
    result = breaker.call(execute_task, task_data)

    # Circuit breaker per API provider
    api_breaker = DispatchCircuitBreaker.for_api("anthropic")
    response = api_breaker.call(anthropic.complete, prompt)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable, Tuple, Type

from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_random,
    before_sleep_log,
)

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """Configuration for retry behavior with exponential backoff.

    Attributes:
        max_attempts: Maximum number of retry attempts (default: 3)
        wait_base: Base multiplier for exponential backoff in seconds (default: 1.0)
        wait_max: Maximum wait time between retries in seconds (default: 30.0)
        retry_on: Tuple of exception types that trigger retry (default: (Exception,))
        jitter: Whether to add random jitter to wait time (default: True)
    """

    max_attempts: int = 3
    wait_base: float = 1.0
    wait_max: float = 30.0
    retry_on: Tuple[Type[Exception], ...] = (Exception,)
    jitter: bool = True


def create_retry_decorator(config: RetryConfig) -> Callable:
    """Create a tenacity retry decorator from config.

    Args:
        config: RetryConfig instance with retry parameters

    Returns:
        Configured tenacity retry decorator

    Example:
        @create_retry_decorator(RETRY_API_CALL)
        def unstable_function():
            # May fail and retry up to config.max_attempts times
            ...
    """
    wait_strategy = wait_exponential(
        multiplier=config.wait_base,
        max=config.wait_max,
    )

    # Add jitter if enabled (random 0-2 seconds added to backoff)
    if config.jitter:
        wait_strategy = wait_strategy + wait_random(0, 2)

    return retry(
        stop=stop_after_attempt(config.max_attempts),
        wait=wait_strategy,
        retry=retry_if_exception_type(config.retry_on),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


class DispatchCircuitBreaker:
    """Circuit breaker wrapper for dispatch tasks.

    Wraps pybreaker CircuitBreaker with dispatch-specific factories and utilities.
    Prevents cascading failures by opening circuit after consecutive failures.

    States:
        - closed: Normal operation, calls pass through
        - open: Circuit tripped, calls fail immediately
        - half-open: Testing if service recovered

    Example:
        breaker = DispatchCircuitBreaker.for_wave(wave_num=1)
        if breaker.is_available:
            result = breaker.call(execute_task, task_data)
    """

    def __init__(
        self,
        name: str,
        fail_max: int = 5,
        reset_timeout: int = 60,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            name: Unique identifier for this breaker
            fail_max: Number of consecutive failures before opening (default: 5)
            reset_timeout: Seconds before attempting to close from open state (default: 60)
        """
        self._breaker = CircuitBreaker(
            fail_max=fail_max,
            reset_timeout=reset_timeout,
            name=name,
        )
        self._name = name

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute function through circuit breaker.

        Args:
            func: Callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result of func(*args, **kwargs)

        Raises:
            CircuitBreakerError: If circuit is open
            Exception: Any exception raised by func
        """
        try:
            return self._breaker.call(func, *args, **kwargs)
        except CircuitBreakerError as e:
            logger.error(f"Circuit breaker '{self._name}' is OPEN: {e}")
            raise

    @property
    def state(self) -> str:
        """Current circuit breaker state.

        Returns:
            One of: "closed", "open", "half-open"
        """
        state = self._breaker.current_state
        return state.name.lower().replace("state", "")

    @property
    def is_available(self) -> bool:
        """Check if circuit breaker allows calls.

        Returns:
            True if state is closed or half-open, False if open
        """
        return self.state in ("closed", "half-open")

    def reset(self) -> None:
        """Manually reset circuit breaker to closed state."""
        self._breaker.close()
        logger.info(f"Circuit breaker '{self._name}' manually reset to CLOSED")

    @staticmethod
    def for_wave(wave_num: int, fail_max: int = 5) -> DispatchCircuitBreaker:
        """Factory: Create circuit breaker for a specific wave.

        Args:
            wave_num: Wave number (0-indexed)
            fail_max: Max failures before opening (default: 5)

        Returns:
            DispatchCircuitBreaker instance for the wave
        """
        return DispatchCircuitBreaker(
            name=f"wave_{wave_num}",
            fail_max=fail_max,
            reset_timeout=60,
        )

    @staticmethod
    def for_api(provider: str = "anthropic", fail_max: int = 3) -> DispatchCircuitBreaker:
        """Factory: Create circuit breaker for an API provider.

        Args:
            provider: API provider name (e.g., "anthropic", "openai")
            fail_max: Max failures before opening (default: 3, lower for APIs)

        Returns:
            DispatchCircuitBreaker instance for the API
        """
        return DispatchCircuitBreaker(
            name=f"api_{provider}",
            fail_max=fail_max,
            reset_timeout=120,  # Longer timeout for API recovery
        )


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

# API calls: 3 attempts, 2s base backoff, max 30s, retry on any exception
RETRY_API_CALL = RetryConfig(
    max_attempts=3,
    wait_base=2.0,
    wait_max=30.0,
    retry_on=(Exception,),
    jitter=True,
)

# Script execution: 2 attempts, 1s base backoff, retry on any exception
RETRY_SCRIPT = RetryConfig(
    max_attempts=2,
    wait_base=1.0,
    wait_max=10.0,
    retry_on=(Exception,),
    jitter=True,
)

# Critical tasks: 5 attempts, 0.5s base backoff, aggressive retry
RETRY_AGGRESSIVE = RetryConfig(
    max_attempts=5,
    wait_base=0.5,
    wait_max=20.0,
    retry_on=(Exception,),
    jitter=True,
)
