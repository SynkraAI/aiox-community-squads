# Post-Execution Gate — Output Veto Conditions (V2.*)

> **Phase:** 5.5 (Post-Execution Verification)
> **Agent:** quality-gate (Deming)
> **Type:** Automatic (hard block, latency < 60s)
> **Behavior:** Mark task FAILED, retry or escalate
> **Source:** PRD Section 3.3 Phase 5.5 + veto-conditions.yaml V2.*
> **Script:** `scripts/validate-wave-results.py`

---

## Purpose

Validates outputs from completed tasks BEFORE marking them as PASS. Prevents false positives where a subagent says "done" but produced no useful output.

**Deming Principle:** "Study actual vs predicted. Act on the difference."

---

## Veto Conditions

### V2.1: Output File Exists

| Field | Value |
|-------|-------|
| **ID** | V2.1 |
| **Condition** | Output file does not exist |
| **Check** | `not os.path.exists(task.output_path)` |
| **Severity** | Hard block |
| **Action** | VETO — Task failed, retry or escalate |
| **Rationale** | No file = task produced nothing |

### V2.2: Output File Is Not Empty

| Field | Value |
|-------|-------|
| **ID** | V2.2 |
| **Condition** | Output file is empty (0 bytes) |
| **Check** | `os.path.getsize(task.output_path) == 0` |
| **Severity** | Hard block |
| **Action** | VETO — Task produced empty output |
| **Rationale** | Empty file = task ran but produced nothing useful |

### V2.3: Cost Within Budget

| Field | Value |
|-------|-------|
| **ID** | V2.3 |
| **Condition** | Cost exceeded 3x estimate |
| **Check** | `actual_cost > 3 * estimated_cost` |
| **Severity** | Warning (not hard block) |
| **Action** | FLAG — Investigate prompt efficiency |
| **Rationale** | 3x overrun = likely infinite loop or overly verbose prompt |

### V2.4: No Placeholder Text in Output

| Field | Value |
|-------|-------|
| **ID** | V2.4 |
| **Condition** | Output contains placeholder text |
| **Check** | `regex match in output: (\[XXX\]\|\{TODO\}\|TBD\|\[INSERT\]\|\[PLACEHOLDER\])` |
| **Severity** | Hard block |
| **Action** | VETO — Task did not fully execute |
| **Rationale** | Placeholders in output = incomplete execution |

---

## Execution Flow

```
Wave N completes → For EACH task in wave:
│
├── V2.1: File exists at output_path?
│   ├── YES → Continue
│   └── NO → FAIL task, attempt retry
│
├── V2.2: File size > 0?
│   ├── YES → Continue
│   └── NO → FAIL task, attempt retry
│
├── V2.4: No placeholders in output?
│   ├── CLEAN → Continue
│   └── HAS PLACEHOLDERS → FAIL task, attempt retry
│
├── V2.3: Cost within 3x estimate?
│   ├── YES → Continue
│   └── NO → FLAG warning (do not block)
│
├── Additional acceptance criteria (from task):
│   ├── Check each criterion in task.acceptance_criteria
│   ├── Binary: PASS or FAIL per criterion
│   └── ALL must pass for task to pass
│
└── ALL PASS → ✅ task.status = "pass"
    ANY V2.1/V2.2/V2.4 FAIL → ❌ task.status = "fail" → retry logic
```

---

## Retry Logic

| Scenario | Action |
|----------|--------|
| 1st failure, attempts < max_attempts | Retry with same prompt |
| 2nd failure, attempts < max_attempts | Retry with enhanced prompt (add explicit constraints) |
| 3rd failure (max_attempts reached) | Mark FAILED, escalate to user |
| 3+ tasks in same wave failed | HALT wave, show failures, ask user |

---

## Deming PDSA — Study Phase

After each wave, the post-execution gate records:

```yaml
study:
  wave: {{wave_num}}
  predicted:
    outputs: {{predicted_count}}
    failures: {{predicted_failures}}
    cost: {{predicted_cost}}
  actual:
    outputs: {{actual_count}}
    failures: {{actual_failures}}
    cost: {{actual_cost}}
  delta:
    outputs: "{{output_delta}}"
    failures: "{{failure_delta}}"
    cost: "{{cost_delta_pct}}%"
  learning: "{{what_to_adjust_for_next_wave}}"
```

This study data feeds into `dispatch-heuristics.yaml` PDSA → Act phase.

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Trust subagent's "done" without checking file | ALWAYS verify V2.1 + V2.2 |
| Skip V2.4 because "it's just a placeholder" | Placeholders = incomplete work |
| Hard block on cost overrun | V2.3 is a WARNING, not a block |
| Retry without any prompt changes | 2nd retry must enhance the prompt |
