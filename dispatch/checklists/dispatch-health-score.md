# Dispatch Health Score — 12-Point Run Quality Assessment

> **Phase:** 6 (Reporting)
> **Agent:** dispatch-chief
> **Type:** Post-run assessment
> **Source:** PRD Section 9.2 Pattern 5 + dispatch-heuristics.yaml
> **Script:** `scripts/dispatch-health-score.py`

---

## Purpose

Evaluates a completed dispatch run against 12 quality criteria derived from the 7 Immutable Laws. The health score measures HOW WELL dispatch followed its own principles, not just whether tasks completed.

**Insight:** A run can complete all tasks (100% pass) but score 4/12 if it violated dispatch principles (e.g., executed in main context, no caching, no state persistence).

---

## The 12-Point Checklist

### 1. Story-Driven Input

| Field | Value |
|-------|-------|
| **Check** | Input came from story/PRD (not free text) |
| **Pass** | `input_type in ["story", "prd"]` |
| **Legacy** | Free text without acceptance criteria |
| **Law** | Law #3 (Story-Driven) |

### 2. DAG Wave Optimization

| Field | Value |
|-------|-------|
| **Check** | wave-optimizer.py produced fewer waves than task count |
| **Pass** | `total_waves < total_tasks` |
| **Legacy** | Fixed order execution (ORG→RESOURCES→AUTO→FILES) |
| **Law** | Law #5 (Wave Optimized) |

### 3. Pre-Execution Gate Passed

| Field | Value |
|-------|-------|
| **Check** | All V1.* veto conditions checked, 0 uncaught errors |
| **Pass** | `pre_execution_errors == 0` |
| **Legacy** | No pre-execution validation |
| **Law** | Quality Built In (Deming) |

### 4. Model Selection Applied

| Field | Value |
|-------|-------|
| **Check** | Every task has explicit model (haiku/sonnet/worker) |
| **Pass** | `all(task.model is not None for task in tasks)` |
| **Legacy** | Default model for all tasks |
| **Law** | Law #2 (Right Model) |

### 5. CODE > LLM Enforced

| Field | Value |
|-------|-------|
| **Check** | Deterministic tasks used scripts, not LLM |
| **Pass** | `worker_tasks > 0 OR no deterministic tasks exist` |
| **Legacy** | LLM doing mkdir, mv, template fill |
| **Law** | Law #1 (CODE > LLM) |

### 6. Enrichment Levels Applied

| Field | Value |
|-------|-------|
| **Check** | Tasks have MINIMAL/STANDARD/FULL based on domain |
| **Pass** | `all(task.enrichment in ["MINIMAL", "STANDARD", "FULL"])` |
| **Legacy** | Same context for all tasks |
| **Law** | Resource optimization |

### 7. State Persisted

| Field | Value |
|-------|-------|
| **Check** | state.json saved after every wave |
| **Pass** | `state.json exists AND state.last_updated > state.started_at` |
| **Legacy** | No persistence, can't resume |
| **Law** | Crash recovery |

### 8. Acceptance Criteria Verified

| Field | Value |
|-------|-------|
| **Check** | Post-execution checked real criteria (file exists, sections present) |
| **Pass** | `post_execution_checks_run == True` |
| **Legacy** | Task said "done" without verification |
| **Law** | Quality Built In (Deming) |

### 9. Cost Tracked

| Field | Value |
|-------|-------|
| **Check** | Actual token cost recorded per task |
| **Pass** | `all(task.cost_usd > 0 for agent_tasks)` |
| **Legacy** | Only estimates, no actuals |
| **Law** | Law #6 (Optimize Everything) |

### 10. Zero Main Context Execution

| Field | Value |
|-------|-------|
| **Check** | Opus terminal used 0 tokens for content work |
| **Pass** | `main_context_content_tokens == 0` |
| **Legacy** | Content processed in main Opus context |
| **Law** | Law #0 (NEVER MAIN CONTEXT) |

### 11. Handoff Saved

| Field | Value |
|-------|-------|
| **Check** | Run state can be resumed via `*resume` |
| **Pass** | `state.json contains enough data to resume` |
| **Legacy** | No resume capability |
| **Law** | Crash recovery + session continuity |

### 12. Feedback Loop Active

| Field | Value |
|-------|-------|
| **Check** | Failed tasks got feedback + retry (not just fail) |
| **Pass** | `retry_count > 0 OR fail_count == 0` |
| **Legacy** | Fail = dead, no retry |
| **Law** | Self-healing (Pedro Valério pattern) |

---

## Scoring

| Score | Rating | Interpretation |
|-------|--------|----------------|
| **12/12** | Exemplary | All dispatch patterns applied correctly |
| **9-11/12** | Good | Minor improvements possible |
| **5-8/12** | Needs Work | Significant patterns missing |
| **1-4/12** | Poor | Most dispatch patterns absent |

---

## Score Calculation

```python
# From scripts/dispatch-health-score.py

def calculate_health_score(state: dict) -> dict:
    score = 0
    details = []

    # 1. Story-Driven Input
    if state["input_type"] in ["story", "prd"]:
        score += 1
        details.append({"id": 1, "name": "Story-Driven Input", "status": "PASS"})
    else:
        details.append({"id": 1, "name": "Story-Driven Input", "status": "FAIL"})

    # 2. DAG Wave Optimization
    if state["total_waves"] < len(state["tasks"]):
        score += 1
        details.append({"id": 2, "name": "DAG Wave Optimization", "status": "PASS"})
    # ... (all 12 checks)

    return {
        "score": score,
        "max": 12,
        "rating": get_rating(score),
        "details": details
    }
```

---

## Integration with Execution Report

The health score is included in the execution report (execution-report-tmpl.md) as:

```markdown
## Health Score

**Score: {{health_score}}/12 — {{health_rating}}**

| # | Check | Status |
|---|-------|--------|
| 1 | Story-Driven Input | PASS/FAIL |
| 2 | DAG Wave Optimization | PASS/FAIL |
| ... | ... | ... |
| 12 | Feedback Loop Active | PASS/FAIL |
```

---

## Trend Tracking

Over multiple runs, health scores reveal patterns:

| Pattern | Action |
|---------|--------|
| Score consistently 9-12 | System healthy, maintain |
| Score dropping over time | Investigate — are gates being bypassed? |
| Item 10 failing often | Main context contamination — audit dispatch flow |
| Item 5 always failing | CODE > LLM not being enforced — add more Workers |
| Item 1 always failing | Users not creating stories — consider auto-convert |

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Skip health score because run passed | Health score measures HOW, not WHAT |
| Score 6/12 and ignore | Investigate which 6 items failed |
| Only track score, not individual items | Individual items reveal systemic issues |
| Compare scores across different run sizes | Normalize by run complexity |
