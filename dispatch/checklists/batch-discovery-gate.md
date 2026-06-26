# Batch Discovery Gate

> **Gate ID:** QG-BATCH-DISC
> **Transition:** Input → Prioritization
> **Type:** hard_block
> **Source:** wf-dispatch-batch.yaml Phase 0

---

## Purpose

Validates that all story files in the batch directory are valid, parseable, and have no circular inter-story dependencies before proceeding to prioritization.

---

## Veto Conditions

| ID | Condition | Check | Action |
|----|-----------|-------|--------|
| VB0.1 | No .md files found in directory | `Glob("plan/stories/*.md")` returns 0 files | HALT — directory empty or wrong path |
| VB0.2 | Circular inter-story dependencies | `wave-optimizer.py --check-cycles` detects cycle | HALT — show cycle, options: remove dep / merge / cancel |
| VB0.3 | External dependencies unsatisfied | Story references output from non-batch story | HALT — show missing deps, options: skip / run first / proceed |

---

## Checklist

- [ ] 1. Story directory path is valid and accessible
- [ ] 2. At least 1 .md file found (excluding README, INDEX, _prefixed)
- [ ] 3. Each .md file is valid markdown with identifiable acceptance criteria
- [ ] 4. Inter-story dependency graph extracted (from `depends_on` fields)
- [ ] 5. Dependency graph has NO circular references
- [ ] 6. All external dependencies (non-batch outputs) exist on disk
- [ ] 7. Discovery summary generated: {total_stories, dependency_edges, independent_stories}

---

## Pass Condition

All stories discovered AND dependency graph valid (no cycles) AND all external dependencies resolvable.

## On Fail

Present veto condition with options:
1. Fix the issue (remove circular dep, provide missing file)
2. Skip affected stories and continue with valid ones
3. Cancel batch
4. Other
