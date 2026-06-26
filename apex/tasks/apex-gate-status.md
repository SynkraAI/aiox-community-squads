# *apex-gate-status — Quality Gate Status

> Show actual protection level: active, skipped, and manual gates for THIS project.

## When This Task Runs

- User runs `*apex-gate-status`
- Automatically after `*apex-audit` (appended to output)
- After `*apex-scan` if veto conditions exist

## What It Does

### Phase 1: Evaluate All Gates

For every gate in `data/veto-conditions.yaml`:
1. Read all conditions under the gate
2. For each condition, run the `available_check`
3. Classify condition as:
   - **ACTIVE** — available_check passes, condition will be enforced
   - **SKIPPED** — available_check fails, on_unavailable = SKIP
   - **MANUAL** — available_check fails, on_unavailable = MANUAL_CHECK
   - **BLOCKED** — available_check fails, on_unavailable = BLOCK (still enforced)

### Phase 2: Compute Coverage

```
gate_coverage = active_conditions / total_conditions
```

Classifications:
- `>= 70%` — **Protected** (healthy)
- `50-69%` — **Partial** (many tools missing)
- `< 50%` — **Exposed** (most gates skipped)

### Phase 3: Display Summary

Format:
```
Quality Gate Status — {project_name}

{active} of {total} conditions ACTIVE ({coverage}%)
Classification: {Protected | Partial | Exposed}

┌─────────────────────────────────┬────────┬────────┬────────┐
│ Gate                            │ Active │ Skipped│ Manual │
├─────────────────────────────────┼────────┼────────┼────────┤
│ QG-AX-001 Design Token Quality  │  3/5   │   2    │   0    │
│ QG-AX-002 Motion Quality        │  4/4   │   0    │   0    │
│ ...                             │        │        │        │
│ QG-AX-DEEP-006 Error Resilience │  2/3   │   1    │   0    │
└─────────────────────────────────┴────────┴────────┴────────┘

Skipped reasons:
  - Chromatic CLI not installed (affects: QG-AX-003, QG-AX-008)
  - Storybook not configured (affects: QG-AX-009)
  - axe-core CLI not available (affects: QG-AX-005)

Recommendation: Install Chromatic to enable 3 additional quality gates.
```

### Phase 4: Suggest Actions

IF coverage < 70%:
```
1. Install missing tools to increase coverage
2. Run *apex-audit for full assessment
3. Done
```

IF coverage >= 70%:
```
1. Run *apex-audit for full assessment
2. Done
```

## Quality Gate

| ID | Check | Action |
|----|-------|--------|
| VC-AX-GS-001 | Gate status evaluates ALL gates in veto-conditions.yaml | BLOCK if any gate is missing from evaluation |
| VC-AX-GS-002 | Coverage percentage is mathematically correct | BLOCK if calculation error |

## Owner

apex-lead (Emil) — meta command, not domain-specific
