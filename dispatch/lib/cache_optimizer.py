"""
Cache Optimizer — Prompt Caching Strategy for Dispatch Squad

Provides utilities to structure prompts for maximum Anthropic prompt caching efficiency.
Achieves ~70-80% cached token reuse within same-domain waves, ~30-40% across mixed domains.

Architecture:
- Static prefix (CACHEABLE): Agent definition + checklist + template structure
- Dynamic suffix (NOT cached): Task-specific instructions + context + KB excerpt

Cache TTL: 5 minutes
Cache pricing (2026): Read is 10x cheaper than write for all models

Reference: squads/dispatch/data/model-selection-rules.yaml (prompt_caching section)
"""

from dataclasses import dataclass
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# PRICING CONSTANTS (2026)
# ═══════════════════════════════════════════════════════════════════════════════

PRICING = {
    "haiku": {
        "input": 1.00,         # $/MTok
        "output": 5.00,        # $/MTok
        "cache_read": 0.10,    # $/MTok (10x cheaper)
        "cache_write": 1.25,   # $/MTok (25% more expensive)
    },
    "sonnet": {
        "input": 3.00,         # $/MTok
        "output": 15.00,       # $/MTok
        "cache_read": 0.30,    # $/MTok (10x cheaper)
        "cache_write": 3.75,   # $/MTok (25% more expensive)
    },
    "opus": {
        "input": 5.00,         # $/MTok
        "output": 25.00,       # $/MTok
        "cache_read": 0.50,    # $/MTok (10x cheaper)
        "cache_write": 6.25,   # $/MTok (25% more expensive)
    },
}

CACHE_TTL_SECONDS = 300  # 5 minutes
CHARS_PER_TOKEN = 4      # Rough estimate for token calculation


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PromptStructure:
    """
    Represents a cache-optimized prompt with static (cacheable) and dynamic parts.

    Static prefix contains agent definition, checklist, template — reused across
    tasks with same agent. Dynamic content contains task-specific instructions.
    """
    static_prefix: str      # Agent def + template + checklist (CACHEABLE)
    dynamic_content: str    # Task-specific instructions (NOT cached)

    @property
    def full_prompt(self) -> str:
        """Complete prompt with cache breakpoint marker."""
        return f"""{self.static_prefix.strip()}

=== CACHE BREAKPOINT ===

{self.dynamic_content.strip()}"""

    @property
    def static_tokens_estimate(self) -> int:
        """Estimate tokens in cacheable static prefix (~4 chars per token)."""
        return len(self.static_prefix) // CHARS_PER_TOKEN

    @property
    def dynamic_tokens_estimate(self) -> int:
        """Estimate tokens in non-cached dynamic content (~4 chars per token)."""
        return len(self.dynamic_content) // CHARS_PER_TOKEN

    @property
    def total_tokens_estimate(self) -> int:
        """Total estimated tokens (static + dynamic)."""
        return self.static_tokens_estimate + self.dynamic_tokens_estimate

    @property
    def cache_ratio(self) -> float:
        """Ratio of cacheable tokens to total (0.0 to 1.0)."""
        total = self.total_tokens_estimate
        if total == 0:
            return 0.0
        return self.static_tokens_estimate / total


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE OPTIMIZER
# ═══════════════════════════════════════════════════════════════════════════════

class CacheOptimizer:
    """
    Builds cache-optimized prompts and estimates savings for dispatch batches.

    Strategy:
    - Static prefix: Agent definition + checklist + template (reused across tasks)
    - Dynamic suffix: Task description + KB excerpt + acceptance criteria
    - Group same-domain tasks consecutively for maximum cache hits

    Savings:
    - Same-domain wave (6 tasks): ~75% cached (first task writes, rest read)
    - Mixed-domain wave: ~40% cached (shared structure, different agents)
    """

    def __init__(self):
        self._prefix_cache: dict[str, str] = {}  # domain -> static prefix

    def build_prompt(
        self,
        agent_path: str,
        task_content: str,
        agent_definition: str = "",
        checklist: str = "",
        template: str = "",
        kb_content: str = "",
        acceptance_criteria: str = ""
    ) -> PromptStructure:
        """
        Build cache-optimized prompt structure.

        Puts static content (agent def, checklist, template) FIRST as cacheable prefix.
        Puts dynamic content (task specifics, KB excerpt, criteria) LAST.

        Args:
            agent_path: Squad path (e.g., "copy:agents:gary-halbert")
            task_content: Task-specific instructions
            agent_definition: Agent voice/rules/constraints
            checklist: Quality checklist items
            template: Output template structure
            kb_content: Knowledge base excerpt (task-specific)
            acceptance_criteria: Task acceptance criteria

        Returns:
            PromptStructure with optimized static/dynamic split
        """
        # Build static prefix (CACHEABLE — same across tasks with same agent)
        static_parts = []

        if agent_definition:
            static_parts.append(f"## Agent Definition\n\n{agent_definition}")

        if checklist:
            static_parts.append(f"## Quality Checklist\n\n{checklist}")

        if template:
            static_parts.append(f"## Output Template\n\n{template}")

        static_prefix = "\n\n".join(static_parts) if static_parts else ""

        # Cache static prefix by agent path
        self._prefix_cache[agent_path] = static_prefix

        # Build dynamic content (NOT cached — varies per task)
        dynamic_parts = []

        if task_content:
            dynamic_parts.append(f"## Task Instructions\n\n{task_content}")

        if kb_content:
            dynamic_parts.append(f"## Context\n\n{kb_content}")

        if acceptance_criteria:
            dynamic_parts.append(f"## Acceptance Criteria\n\n{acceptance_criteria}")

        dynamic_content = "\n\n".join(dynamic_parts) if dynamic_parts else ""

        return PromptStructure(
            static_prefix=static_prefix,
            dynamic_content=dynamic_content
        )

    def group_by_domain(self, tasks: list[dict]) -> dict[str, list[dict]]:
        """
        Group tasks by agent domain for maximum cache hits.

        Tasks with same agent should run consecutively to benefit from cache.

        Args:
            tasks: List of task dicts with 'agent_path' or 'domain' field

        Returns:
            Dict mapping domain -> list of tasks
        """
        grouped: dict[str, list[dict]] = {}

        for task in tasks:
            # Extract domain from agent_path (e.g., "copy:agents:gary-halbert" -> "copy")
            agent_path = task.get("agent_path", task.get("domain", "unknown"))
            domain = agent_path.split(":")[0] if ":" in agent_path else agent_path

            if domain not in grouped:
                grouped[domain] = []
            grouped[domain].append(task)

        return grouped

    def estimate_savings(
        self,
        tasks: list[dict],
        model: str = "haiku",
        output_tokens_per_task: int = 1000
    ) -> dict:
        """
        Estimate cache savings for a batch of tasks.

        Assumes:
        - First task per domain: cache WRITE (static prefix)
        - Subsequent tasks same domain: cache READ (static prefix)
        - Dynamic content: always input cost (not cached)

        Args:
            tasks: List of task dicts with 'agent_path' and optional 'tokens_estimate'
            model: Model name ("haiku", "sonnet", "opus")
            output_tokens_per_task: Estimated output tokens per task

        Returns:
            Dict with cost breakdown and savings estimate:
            {
                'total_tokens': int,
                'cacheable_tokens': int,
                'cache_ratio': float,
                'estimated_cost_no_cache': float (USD),
                'estimated_cost_with_cache': float (USD),
                'savings_pct': float,
                'savings_usd': float
            }
        """
        if not tasks or model not in PRICING:
            return {
                "total_tokens": 0,
                "cacheable_tokens": 0,
                "cache_ratio": 0.0,
                "estimated_cost_no_cache": 0.0,
                "estimated_cost_with_cache": 0.0,
                "savings_pct": 0.0,
                "savings_usd": 0.0,
            }

        pricing = PRICING[model]
        grouped = self.group_by_domain(tasks)

        # Estimate tokens
        # Default: ~2000 tokens input (1500 static + 500 dynamic)
        static_tokens_per_task = 1500
        dynamic_tokens_per_task = 500
        total_tokens_input = 0
        cacheable_tokens = 0

        # Cost calculation
        cost_no_cache = 0.0
        cost_with_cache = 0.0

        for domain, domain_tasks in grouped.items():
            for i, task in enumerate(domain_tasks):
                # Use task's token estimate if available
                task_static = task.get("static_tokens", static_tokens_per_task)
                task_dynamic = task.get("dynamic_tokens", dynamic_tokens_per_task)
                task_total = task_static + task_dynamic

                total_tokens_input += task_total

                # No cache: all input at input rate
                cost_no_cache += (task_total / 1_000_000) * pricing["input"]
                cost_no_cache += (output_tokens_per_task / 1_000_000) * pricing["output"]

                # With cache:
                # - First task in domain: cache WRITE for static, input for dynamic
                # - Subsequent tasks: cache READ for static, input for dynamic
                if i == 0:
                    # First task: write cache
                    cost_with_cache += (task_static / 1_000_000) * pricing["cache_write"]
                    cost_with_cache += (task_dynamic / 1_000_000) * pricing["input"]
                    cacheable_tokens += task_static
                else:
                    # Subsequent tasks: read cache (10x cheaper)
                    cost_with_cache += (task_static / 1_000_000) * pricing["cache_read"]
                    cost_with_cache += (task_dynamic / 1_000_000) * pricing["input"]
                    cacheable_tokens += task_static

                # Output tokens: always same cost
                cost_with_cache += (output_tokens_per_task / 1_000_000) * pricing["output"]

        cache_ratio = cacheable_tokens / total_tokens_input if total_tokens_input > 0 else 0.0
        savings_usd = cost_no_cache - cost_with_cache
        savings_pct = (savings_usd / cost_no_cache * 100) if cost_no_cache > 0 else 0.0

        return {
            "total_tokens": total_tokens_input,
            "cacheable_tokens": cacheable_tokens,
            "cache_ratio": cache_ratio,
            "estimated_cost_no_cache": round(cost_no_cache, 4),
            "estimated_cost_with_cache": round(cost_with_cache, 4),
            "savings_pct": round(savings_pct, 1),
            "savings_usd": round(savings_usd, 4),
        }

    def optimize_wave_order(self, waves: dict[int, list[dict]]) -> dict[int, list[dict]]:
        """
        Reorder tasks within waves to maximize cache hits.

        Groups same-domain tasks together so cache can be reused within wave.

        Args:
            waves: Dict mapping wave_id -> list of tasks

        Returns:
            Optimized waves with tasks reordered for cache efficiency
        """
        optimized_waves = {}

        for wave_id, tasks in waves.items():
            # Group by domain
            grouped = self.group_by_domain(tasks)

            # Flatten back into list, keeping domain groups together
            optimized_tasks = []
            for domain in sorted(grouped.keys()):
                optimized_tasks.extend(grouped[domain])

            optimized_waves[wave_id] = optimized_tasks

        return optimized_waves


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def estimate_cache_hit_rate(tasks: list[dict]) -> float:
    """
    Quick estimate of cache hit percentage based on domain distribution.

    Formula:
    - First task per domain = cache MISS (write)
    - Subsequent tasks per domain = cache HIT (read)
    - Hit rate = (total - unique_domains) / total

    Args:
        tasks: List of task dicts with 'agent_path' or 'domain' field

    Returns:
        Estimated cache hit rate as percentage (0.0 to 100.0)

    Example:
        6 tasks, 2 domains (3 each) -> 4 hits / 6 tasks = 66.7%
    """
    if not tasks:
        return 0.0

    # Count unique domains
    domains = set()
    for task in tasks:
        agent_path = task.get("agent_path", task.get("domain", "unknown"))
        domain = agent_path.split(":")[0] if ":" in agent_path else agent_path
        domains.add(domain)

    unique_domains = len(domains)
    total_tasks = len(tasks)

    # First task per domain is cache MISS, rest are HITs
    cache_hits = max(0, total_tasks - unique_domains)
    hit_rate = (cache_hits / total_tasks * 100) if total_tasks > 0 else 0.0

    return round(hit_rate, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE (for testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    # Quick test
    optimizer = CacheOptimizer()

    # Simulate 6-task wave with 2 domains
    test_tasks = [
        {"agent_path": "copy:agents:gary-halbert", "domain": "copy"},
        {"agent_path": "copy:agents:gary-halbert", "domain": "copy"},
        {"agent_path": "copy:agents:gary-halbert", "domain": "copy"},
        {"agent_path": "curator:agents:transcript-miner", "domain": "curator"},
        {"agent_path": "curator:agents:transcript-miner", "domain": "curator"},
        {"agent_path": "curator:agents:transcript-miner", "domain": "curator"},
    ]

    print("=== Cache Optimizer Test ===\n")

    # Test grouping
    grouped = optimizer.group_by_domain(test_tasks)
    print(f"Grouped by domain: {list(grouped.keys())}")
    for domain, tasks in grouped.items():
        print(f"  {domain}: {len(tasks)} tasks")

    # Test cache hit rate
    hit_rate = estimate_cache_hit_rate(test_tasks)
    print(f"\nEstimated cache hit rate: {hit_rate}%")

    # Test cost estimation
    savings = optimizer.estimate_savings(test_tasks, model="haiku")
    print("\nCost estimate (Haiku, 6 tasks):")
    print(f"  Total tokens: {savings['total_tokens']:,}")
    print(f"  Cacheable: {savings['cacheable_tokens']:,} ({savings['cache_ratio']:.1%})")
    print(f"  Cost without cache: ${savings['estimated_cost_no_cache']:.4f}")
    print(f"  Cost with cache: ${savings['estimated_cost_with_cache']:.4f}")
    print(f"  Savings: ${savings['savings_usd']:.4f} ({savings['savings_pct']:.1f}%)")

    # Test prompt building
    prompt = optimizer.build_prompt(
        agent_path="copy:agents:gary-halbert",
        task_content="Write sales email using PAS framework",
        agent_definition="You are Gary Halbert. Write visceral, emotional copy.",
        checklist="- [ ] Hook in first 3 words\n- [ ] Personal story\n- [ ] Clear CTA",
        kb_content="ICP: 40-55yo entrepreneurs, pain: scattered marketing"
    )

    print(f"\nPrompt structure:")
    print(f"  Static tokens: {prompt.static_tokens_estimate:,}")
    print(f"  Dynamic tokens: {prompt.dynamic_tokens_estimate:,}")
    print(f"  Cache ratio: {prompt.cache_ratio:.1%}")
    print(f"\nFirst 200 chars of full prompt:")
    print(f"  {prompt.full_prompt[:200]}...")
