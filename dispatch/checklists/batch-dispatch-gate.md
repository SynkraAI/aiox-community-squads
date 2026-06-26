# Batch Dispatch Gate

> **Gate ID:** QG-BATCH-EXEC
> **Transition:** Per-story execution → Next story
> **Type:** hard_block (circuit breaker + cost control)
> **Source:** wf-dispatch-batch.yaml Phase 2

---

## Purpose

Monitors batch execution health during dispatch. Triggers circuit breaker on consecutive failures and cost overrun. Validates per-story completion before proceeding to next story.

---

## Veto Conditions

| ID | Condition | Check | Action |
|----|-----------|-------|--------|
| VB2.1 | Circuit breaker triggered | 3+ consecutive story failures | HALT — show last 3 failures, options: resume / retry / cancel |
| VB2.2 | Cost overrun | Actual cost > 5× batch estimate | HALT — show cost comparison, options: continue / cancel / review |

---

## Per-Story Validation Checklist

Before dispatching each story:

- [ ] 1. All inter-story dependencies for this story are satisfied
- [ ] 2. Dependency output files exist on disk (from previously dispatched stories)
- [ ] 3. Story file is accessible and unchanged since discovery

After each story completes:

- [ ] 4. Story dispatch completed (status: complete, failed, or skipped)
- [ ] 5. Story outputs verified at declared paths
- [ ] 6. Story metrics recorded:
  - Task count (completed / failed / skipped)
  - Cost (actual vs estimated)
  - Duration
  - Health score
- [ ] 7. Batch state updated with story completion status
- [ ] 8. Consecutive failure counter updated (reset on success, increment on failure)

---

## Circuit Breaker Logic

```
consecutive_failures = 0

for each story:
  result = dispatch(story)
  if result.status == "complete":
    consecutive_failures = 0          # Reset
  elif result.status == "failed":
    consecutive_failures += 1         # Increment
    if consecutive_failures >= 3:
      HALT → VB2.1 triggered
```

---

## Cost Control Logic

```
if actual_total_cost > 5 * estimated_total_cost:
  HALT → VB2.2 triggered
  Present: {actual, estimated, ratio, remaining_stories}
```

---

## Pass Condition

All stories dispatched (completed, skipped, or failed with user decision) AND circuit breaker NOT triggered AND cost within 5× estimate.

## On Fail

Options:
1. Resume from next story (skip failed)
2. Retry last failed story
3. Cancel remaining stories
4. Other
