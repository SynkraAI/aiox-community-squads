# Verify Wave

| Field | Value |
|-------|-------|
| **Task ID** | `verify-wave` |
| **Version** | `1.0.0` |
| **Purpose** | Verify acceptance criteria for all tasks in a completed wave |
| **Agent** | `quality-gate` |
| **Phase** | Phase 5.5 (Post-Execution Gate) |
| **Pattern** | `DS-QG-001` (Operational Definitions) + `DS-QG-002` (Veto Conditions V2.*) |
| **Estimated Time** | 1-3 minutes (script-driven, minimal LLM reasoning) |

---

## Description

After a wave completes execution (Phase 5), this task runs deterministic verification
on every task output. It checks file existence, file size, placeholder contamination,
cost bounds, and task-specific acceptance criteria. ALL deterministic checks run via
`scripts/validate-wave-results.py` (CODE > LLM, Law #1). The quality-gate agent only
intervenes for non-deterministic evaluation (rare). Results feed into Deming's PDSA
cycle: STUDY actual vs predicted performance, ACT by recommending adjustments for
subsequent waves. Failed tasks are routed to retry or escalated to the user.

**Binary outcomes only:** Every check is PASS or FAIL. No "partial", "maybe", or
"good enough". This is a hard block (QG-POST from config.yaml).

### Worker Scripts (CODE > LLM)

Most verification phases are deterministic and executed as Worker scripts:

| Phase | Script | Purpose |
|-------|--------|---------|
| 2 | `scripts/validate-wave-results.py` | V2.1-V2.4 veto condition checks |
| 3 | `scripts/validate-haiku-prompt.py` | Haiku prompt quality validation |
| - | `scripts/cost-tracker.py` | Duration/cost deviation calculation |
| - | `scripts/dispatch-health-score.py` | 12-point health score |

**Preferred:** Only Phase 4 (PDSA analysis) requires LLM reasoning. Phases 2, 3, 5 are deterministic.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | string | YES | Unique run identifier (e.g., `run-2026-02-10-001`) |
| `wave_number` | integer | YES | Wave index (1-based) that just completed execution |

---

## Preconditions

Before starting this task, ALL of the following MUST be true:

- [ ] Wave `wave_number` has status COMPLETED or PARTIAL in state.json (execution finished)
- [ ] `_temp/dispatch/runs/{run_id}/state.json` exists and is valid JSON
- [ ] `scripts/validate-wave-results.py` is accessible and executable
- [ ] `data/veto-conditions.yaml` is accessible (V2.* conditions for post-execution)
- [ ] `checklists/post-execution-gate.md` is accessible
- [ ] `data/dispatch-heuristics.yaml` is accessible (PDSA rules)
- [ ] Execution plan with acceptance criteria is available in state or run directory

**If any precondition fails:** STOP. Report which precondition failed. Do NOT attempt partial verification.

---

## Phase 1: Load Wave Results

**Objective:** Gather all completed task results and their acceptance criteria.

### Action Items

- [ ] 1.1 Read `_temp/dispatch/runs/{run_id}/state.json` via `lib/pipeline_state.py`
- [ ] 1.2 Extract wave_{wave_number} data:
  - List of tasks with their statuses (COMPLETED, FAILED, EXHAUSTED)
  - For each COMPLETED task: output_path, duration_ms, cost_estimate, model, attempts
  - For each FAILED/EXHAUSTED task: error message, attempts count
- [ ] 1.3 Read execution plan to get acceptance criteria for each task
- [ ] 1.4 Read `data/veto-conditions.yaml` — extract V2.* (post-execution) veto conditions
- [ ] 1.5 Read `checklists/post-execution-gate.md` — load verification checklist
- [ ] 1.6 Read `data/dispatch-heuristics.yaml` — load PDSA rules and prediction baselines
- [ ] 1.7 Build verification queue: list of tasks to verify (only COMPLETED tasks — FAILED/EXHAUSTED skip verification)

### Checkpoint 1

- [ ] State loaded successfully
- [ ] Wave data extracted with task list
- [ ] Veto conditions V2.* loaded
- [ ] Verification queue built (only COMPLETED tasks)
- [ ] FAILED/EXHAUSTED tasks excluded from verification (they already have a status)

---

## Phase 2: Run Deterministic Checks (CODE > LLM)

**Objective:** Execute `scripts/validate-wave-results.py` for ALL deterministic validations. Do NOT use LLM for checks that code can perform.

### The Script Handles These Checks

| Check ID | Check | Method | Pass Condition |
|----------|-------|--------|----------------|
| V2.1 | Output file exists | `os.path.exists(output_path)` | File exists at declared path |
| V2.2 | Output file non-empty | `os.path.getsize(output_path) > 0` | File size > 0 bytes |
| V2.3 | Cost within bounds | `actual_cost <= estimated_cost * 3` | Cost does not exceed 3x estimate |
| V2.4 | No placeholder text | `regex scan for [XXX], {TODO}, TBD, PLACEHOLDER, {{.*}}` | Zero matches |

### Action Items

- [ ] 2.1 **Execute validation script**:
  ```bash
  python scripts/validate-wave-results.py \
    --run-id {run_id} \
    --wave {wave_number} \
    --state-path _temp/dispatch/runs/{run_id}/state.json \
    --veto-conditions data/veto-conditions.yaml \
    --output _temp/dispatch/runs/{run_id}/verification-wave-{wave_number}.json
  ```
- [ ] 2.2 **Read script output** — Parse verification-wave-{wave_number}.json:
  ```json
  {
    "wave": 3,
    "tasks_verified": 5,
    "tasks_passed": 4,
    "tasks_failed": 1,
    "results": [
      {
        "task_id": "task_001",
        "checks": {
          "V2.1_file_exists": "PASS",
          "V2.2_non_empty": "PASS",
          "V2.3_cost_bounds": "PASS",
          "V2.4_no_placeholders": "PASS"
        },
        "overall": "PASS"
      },
      {
        "task_id": "task_003",
        "checks": {
          "V2.1_file_exists": "PASS",
          "V2.2_non_empty": "PASS",
          "V2.3_cost_bounds": "WARNING",
          "V2.4_no_placeholders": "FAIL"
        },
        "overall": "FAIL",
        "failure_details": "V2.4: Found placeholder '[XXX]' at line 42"
      }
    ]
  }
  ```
- [ ] 2.3 **Handle script failure** — If the validation script itself crashes:
  - Record error in state.json
  - Fall back to manual checks in Phase 3 (LLM-assisted, last resort)
  - Log: `event: validation_script_error, error: {message}`

### Checkpoint 2

- [ ] Validation script executed successfully
- [ ] Verification JSON produced at expected path
- [ ] Every COMPLETED task has V2.1, V2.2, V2.3, V2.4 results
- [ ] V2.3 (cost bounds) uses WARNING level (does not block, only alerts)
- [ ] V2.4 (placeholders) is a hard FAIL

---

## Phase 3: Check Task-Specific Acceptance Criteria

**Objective:** Verify each task against its own acceptance criteria from the execution plan.

### Action Items

For EACH task that PASSED Phase 2 checks:

- [ ] 3.1 **Load acceptance criteria** — From execution plan, get the task's `acceptance_criteria` list
- [ ] 3.2 **Classify each criterion**:
  - **Deterministic:** Can be checked by code (file exists, word count, contains string, format valid)
    - Execute via script or Bash command
  - **Non-deterministic:** Requires LLM judgment (quality of writing, coherence, relevance)
    - Flag for optional LLM review (only if explicitly configured)
- [ ] 3.3 **Execute deterministic criteria** — For each deterministic criterion:
  - Build a Bash command or Python one-liner to check
  - Execute and record PASS/FAIL
  - Example checks:
    - "Output has >= 500 words" → `wc -w output.md | awk '{print ($1 >= 500) ? "PASS" : "FAIL"}'`
    - "Output is valid YAML" → `python -c "import yaml; yaml.safe_load(open('output.yaml'))"`
    - "Output contains section 'Summary'" → `grep -c '# Summary' output.md > 0`
- [ ] 3.4 **Handle non-deterministic criteria** — Default behavior:
  - Log as `SKIPPED_NON_DETERMINISTIC`
  - Do NOT use LLM to evaluate unless `config.yaml` has `llm_verification: true`
  - These are deferred to human review in the execution report
- [ ] 3.5 **Aggregate results** — For each task:
  - All deterministic criteria PASS + V2.* PASS → task status: `VERIFIED`
  - Any deterministic criterion FAIL → task status: `VERIFICATION_FAILED`
  - Only non-deterministic criteria remaining → task status: `VERIFIED_PARTIAL` (human review needed)

### Checkpoint 3

- [ ] Every COMPLETED task has been checked against its acceptance criteria
- [ ] Deterministic criteria executed via code, not LLM
- [ ] Non-deterministic criteria logged as SKIPPED (deferred to human)
- [ ] Every task has a final verification status: VERIFIED, VERIFICATION_FAILED, or VERIFIED_PARTIAL

---

## Phase 4: Deming PDSA Cycle

**Objective:** STUDY actual results versus predictions. ACT by recommending adjustments for next waves.

### PDSA Framework

```
PLAN: (was done in Phase 4.5 pre-execution — predictions recorded)
DO:   (was done in Phase 5 — execution)
STUDY: Compare actual vs predicted (THIS PHASE)
ACT:   Recommend adjustments based on deviations
```

### Action Items

- [ ] 4.1 **Load predictions** — From state.json, read predictions recorded during pre-execution (Phase 4.5):
  - Predicted duration per task
  - Predicted cost per task
  - Predicted success rate per wave
  - Predicted model suitability
- [ ] 4.2 **STUDY — Compare actuals vs predictions**:
  - **Duration deviation:** For each task, calculate `actual_duration / predicted_duration`
    - Within 0.5x-2.0x → NORMAL
    - Outside range → DEVIATION (record which direction)
  - **Cost deviation:** For each task, calculate `actual_cost / predicted_cost`
    - Within 0.5x-3.0x → NORMAL (3x is the V2.3 warning threshold)
    - Outside range → DEVIATION
  - **Success rate deviation:** `actual_success_rate - predicted_success_rate`
    - Within +/-10% → NORMAL
    - Outside range → DEVIATION
  - **Model suitability:** Did tasks routed to Haiku succeed? Did Sonnet tasks need more turns?
    - Haiku task used > 12 turns (of 15 max) → flag as potentially under-modeled
    - Sonnet task completed in < 5 turns → flag as potentially over-modeled
- [ ] 4.3 **ACT — Generate recommendations** for subsequent waves:
  - If Haiku tasks consistently fail → recommend upgrading to Sonnet for similar tasks
  - If Sonnet tasks consistently finish fast → recommend downgrading to Haiku
  - If timeouts occur → recommend increasing timeout or splitting task
  - If cost exceeds 3x → recommend reducing enrichment level
  - If success rate < 70% → recommend halting and reviewing task definitions
- [ ] 4.4 **Record PDSA findings** in state.json:
  ```json
  {
    "pdsa_wave_{N}": {
      "deviations": [
        {"task_id": "task_003", "metric": "duration", "predicted": 15000, "actual": 45200, "ratio": 3.01},
        {"task_id": "task_005", "metric": "model_suitability", "note": "Haiku used 14/15 turns — consider Sonnet"}
      ],
      "recommendations": [
        "Upgrade task_type 'evaluate' from Haiku to Sonnet for remaining waves",
        "Increase timeout for MCP tasks from 120s to 180s"
      ],
      "adjustments_applied": false
    }
  }
  ```
- [ ] 4.5 **Present recommendations** — If significant deviations found:
  - Display to user with context
  - Offer options:
    ```
    1. Apply recommendations to remaining waves
    2. Continue without changes
    3. Review recommendations in detail
    4. Other
    ```

### Checkpoint 4

- [ ] Predictions loaded from state.json (or skipped if no predictions recorded)
- [ ] Duration, cost, success rate, and model suitability deviations calculated
- [ ] Recommendations generated for significant deviations
- [ ] PDSA findings recorded in state.json
- [ ] Recommendations presented if significant

---

## Phase 5: Handle Failed Verifications

**Objective:** Route verification failures to retry or escalation.

### Action Items

- [ ] 5.1 **Count verification failures** — Tasks with status `VERIFICATION_FAILED`
- [ ] 5.2 **For each failed task**, determine action:
  - Check `task.attempts` in state.json
  - If attempts < 2 → recommend RETRY
    - Set `task.status: PENDING_RETRY`
    - Add to retry queue for next `execute-wave` invocation
  - If attempts >= 2 → recommend ESCALATE
    - Set `task.status: ESCALATED`
    - Add to escalation list for user
- [ ] 5.3 **Circuit breaker evaluation** — Count consecutive failures across entire run:
  - Load failure count from state.json (all waves combined)
  - If consecutive_failures >= 5 (from `config.yaml` `circuit_breaker` setting):
    - Set `run.status: HALTED`
    - Report: "Circuit breaker triggered: {count} consecutive failures across waves"
    - HALT entire pipeline
- [ ] 5.4 **Build verification report** — For user visibility:
  ```
  WAVE {N} VERIFICATION REPORT
  ════════════════════════════

  Verified: {count_verified}/{count_total}
  Failed:   {count_failed}
  Partial:  {count_partial} (human review needed)

  FAILURES:
  - task_003: V2.4 FAIL — Found placeholder '[XXX]' at line 42
  - task_007: AC2 FAIL — Output has 312 words (required >= 500)

  ACTIONS:
  - task_003: RETRY (attempt 2/3)
  - task_007: ESCALATED (attempts exhausted)

  PDSA RECOMMENDATIONS:
  - Upgrade 'evaluate' tasks from Haiku to Sonnet
  ```
- [ ] 5.5 **Present report to user** — Always show, even if all tasks passed (transparency)

### Checkpoint 5

- [ ] All verification failures have an assigned action (RETRY or ESCALATE)
- [ ] Circuit breaker evaluated
- [ ] Verification report generated
- [ ] Report presented to user

---

## Phase 6: Update State and Finalize

**Objective:** Persist all verification results and prepare for next phase.

### Action Items

- [ ] 6.1 **Update state.json** with verification results for every task:
  ```json
  {
    "task_001": {
      "status": "VERIFIED",
      "verification": {
        "V2.1": "PASS",
        "V2.2": "PASS",
        "V2.3": "PASS",
        "V2.4": "PASS",
        "acceptance_criteria": ["PASS", "PASS", "SKIPPED_NON_DETERMINISTIC"]
      },
      "verified_at": "2026-02-10T14:31:15Z"
    }
  }
  ```

- [ ] 6.2 **Update wave status** based on verification:
  - All tasks VERIFIED → `wave.verification_status: PASS`
  - Some tasks VERIFICATION_FAILED → `wave.verification_status: PARTIAL`
  - All tasks VERIFICATION_FAILED → `wave.verification_status: FAIL`

- [ ] 6.3 **Log verification completion** — Via `lib/event_log.py`:
  - `event: wave_verified`
  - Include: `wave_number`, `tasks_verified`, `tasks_failed`, `tasks_partial`, `pdsa_deviations_count`

- [ ] 6.4 **Write verification artifact** — Save detailed results to:
  - `_temp/dispatch/runs/{run_id}/verification-wave-{wave_number}.json` (from Phase 2 script)
  - Append PDSA findings and acceptance criteria results

- [ ] 6.5 **Return control** — Signal to dispatch-chief:
  - If wave verification PASS → proceed to next wave (or reporting if last wave)
  - If wave verification PARTIAL with retries queued → execute-wave for retry batch
  - If wave verification FAIL → present to user with options
  - If circuit breaker triggered → HALT

### Checkpoint 6

- [ ] state.json fully updated with verification results
- [ ] Wave verification status set
- [ ] Verification event logged
- [ ] Verification artifact written
- [ ] Next action determined and signaled

---

## Acceptance Criteria

All criteria are binary (PASS/FAIL). ALL must PASS.

| # | Criterion | Measurement |
|---|-----------|-------------|
| AC1 | All deterministic checks run via `scripts/validate-wave-results.py`, NOT by LLM | Script execution log present in event log |
| AC2 | Every COMPLETED task checked for V2.1 (file exists) | `verification.V2.1` present for all COMPLETED tasks |
| AC3 | Every COMPLETED task checked for V2.2 (non-empty) | `verification.V2.2` present for all COMPLETED tasks |
| AC4 | Every COMPLETED task checked for V2.3 (cost bounds) | `verification.V2.3` present for all COMPLETED tasks |
| AC5 | Every COMPLETED task checked for V2.4 (no placeholders) | `verification.V2.4` present for all COMPLETED tasks |
| AC6 | Verification status is BINARY: PASS or FAIL per check | Zero checks have status "partial", "maybe", "good enough" |
| AC7 | Failed tasks route to RETRY (attempts < 2) or ESCALATE (attempts >= 2) | `task.status` is PENDING_RETRY or ESCALATED for all failures |
| AC8 | Circuit breaker triggers at 5 consecutive failures | Run halted when `consecutive_failures >= 5` |
| AC9 | PDSA study compares actuals vs predictions | `pdsa_wave_{N}` entry exists in state.json |
| AC10 | Verification report presented to user | Report displayed with counts, failures, and actions |
| AC11 | state.json updated with verification results for ALL tasks | Every task in wave has `verification` block in state |
| AC12 | Verification artifact saved to run directory | `verification-wave-{N}.json` exists in run directory |

---

## Output Specification

| Field | Value |
|-------|-------|
| **Primary** | Updated `_temp/dispatch/runs/{run_id}/state.json` with verification results |
| **Artifact** | `_temp/dispatch/runs/{run_id}/verification-wave-{wave_number}.json` |
| **Format** | JSON |
| **Content** | V2.* check results, acceptance criteria results, PDSA findings, recommendations |

### Verification Artifact Structure

```json
{
  "run_id": "run-2026-02-10-001",
  "wave_number": 3,
  "verified_at": "2026-02-10T14:31:15Z",
  "summary": {
    "tasks_verified": 5,
    "tasks_passed": 4,
    "tasks_failed": 1,
    "verification_status": "PARTIAL"
  },
  "checks": {
    "task_001": {
      "V2.1_file_exists": "PASS",
      "V2.2_non_empty": "PASS",
      "V2.3_cost_bounds": "PASS",
      "V2.4_no_placeholders": "PASS",
      "acceptance_criteria": {
        "ac_1": { "description": "Output >= 500 words", "method": "wc -w", "result": "PASS", "actual": 623 },
        "ac_2": { "description": "Valid YAML format", "method": "yaml.safe_load", "result": "PASS" }
      },
      "overall": "PASS"
    },
    "task_003": {
      "V2.1_file_exists": "PASS",
      "V2.2_non_empty": "PASS",
      "V2.3_cost_bounds": "WARNING",
      "V2.4_no_placeholders": "FAIL",
      "failure_details": "Found '[XXX]' at line 42, '{TODO}' at line 87",
      "overall": "FAIL",
      "action": "PENDING_RETRY"
    }
  },
  "pdsa": {
    "deviations": [
      { "task_id": "task_005", "metric": "duration", "predicted_ms": 15000, "actual_ms": 45200, "ratio": 3.01 }
    ],
    "recommendations": [
      "Increase timeout for MCP tasks from 120s to 180s"
    ]
  }
}
```

---

## Dependencies

| Dependency | Type | Path (relative to squad root) |
|------------|------|-------------------------------|
| Validate Wave Results Script | script | `scripts/validate-wave-results.py` |
| Haiku Validator | script | `scripts/validate-haiku-prompt.py` |
| Veto Conditions | data | `data/veto-conditions.yaml` (V2.* section) |
| Post-Execution Gate Checklist | checklist | `checklists/post-execution-gate.md` |
| Dispatch Heuristics | data | `data/dispatch-heuristics.yaml` (PDSA rules) |
| Pipeline State Library | lib | `lib/pipeline_state.py` |
| Event Log Library | lib | `lib/event_log.py` |

---

## Error Handling

| Error | Action |
|-------|--------|
| state.json missing or corrupt | HALT. Cannot verify without execution state. |
| validate-wave-results.py crashes | Log error. Fall back to manual checks (Phase 3 only). Record degraded verification. |
| Output file path doesn't exist | V2.1 FAIL for that task. Task fails verification. |
| Verification JSON write fails | Retry 3 times. If still fails, log to stderr and continue (state.json is primary). |
| No predictions recorded (PDSA) | Skip PDSA study. Log: "No predictions available — PDSA skipped." |
| Circuit breaker triggers | HALT entire run immediately. Present all failure details to user. |
