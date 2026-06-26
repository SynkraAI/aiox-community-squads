# Batch Prioritization Gate

> **Gate ID:** QG-BATCH-PRIO
> **Transition:** Discovery → Dispatch
> **Type:** soft_block (requires user confirmation for large batches)
> **Source:** wf-dispatch-batch.yaml Phase 1

---

## Purpose

Validates that stories are properly ordered, cost estimates are calculated, and user has approved the batch plan before execution begins.

---

## Veto Conditions

| ID | Condition | Check | Action |
|----|-----------|-------|--------|
| VB1.1 | Topological sort failed | `wave-optimizer.py` returned error | HALT — fix dependency graph first |
| VB1.2 | Cost estimate exceeds budget | Total estimated cost > user threshold | WARN — present cost, ask to proceed |

---

## Checklist

- [ ] 1. Topological sort completed via `scripts/wave-optimizer.py` (Kahn's algorithm)
- [ ] 2. WSJF tie-breaking applied within same dependency level
- [ ] 3. Execution order is deterministic and reproducible
- [ ] 4. Per-story cost estimated via `scripts/estimate-batch-cost.py`
- [ ] 5. Total batch cost and estimated duration calculated
- [ ] 6. Batch plan summary presented to user with:
  - Story execution order
  - Per-story task count and estimated cost
  - Total cost (with and without cache)
  - Estimated total duration
- [ ] 7. User confirmation received IF:
  - `total_stories > 10` OR
  - `total_estimated_cost > $1.00`
  - (Small batches proceed automatically)

---

## Pass Condition

Story execution order defined AND estimates calculated AND user confirmed (if required).

## On Fail

Options:
1. Re-prioritize (change order or exclude stories)
2. Reduce batch size
3. Cancel batch
4. Other
