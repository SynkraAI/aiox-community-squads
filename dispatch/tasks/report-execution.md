# report-execution

> **Task ID:** report-execution
> **Version:** 1.0.0
> **Squad:** dispatch
> **Agent:** dispatch-chief
> **Phase:** 6 (Reporting)
> **Executor Type:** Agent (dispatch-chief) + Worker (scripts)
> **Est. Time:** 2-5 min

---

## Purpose

Generate the final execution report and cost report after all waves complete. This task is the last phase in the dispatch pipeline. It transforms raw run state data into human-readable reports, calculates the dispatch health score, and optionally updates story file checkboxes for completed tasks.

**Why this matters:** Without a structured report, the human has no visibility into what happened, what it cost, what failed, and what to do next. The report is the primary interface between the dispatch engine and the decision-maker.

**Deming connection:** This is the STUDY phase of the overall dispatch PDSA cycle. The execution report provides the data needed for the ACT phase (what to improve next time).

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | string | YES | Dispatch run identifier (e.g., `DS-2026-0210-001`). Used to locate state file at `_temp/dispatch/runs/{run_id}/state.json` |
| `state_path` | string | NO | Override path to state.json. Defaults to `_temp/dispatch/runs/{run_id}/state.json` |
| `story_file` | string | NO | Path to original story file (if input was story-driven). Used for checkbox updates |

---

## Preconditions

| # | Condition | Check | Block On Failure |
|---|-----------|-------|------------------|
| P1 | State file exists | `os.path.exists(_temp/dispatch/runs/{run_id}/state.json)` | YES — cannot generate report without state |
| P2 | All waves have final status | Every wave in state.json has `status` in `[completed, failed, halted]` | YES — cannot report on in-progress waves |
| P3 | Execution report template exists | `os.path.exists(squads/dispatch/templates/execution-report-tmpl.md)` | YES — no template = no structured output |
| P4 | Cost report template exists | `os.path.exists(squads/dispatch/templates/cost-report-tmpl.md)` | YES — no template = no cost breakdown |
| P5 | Health score script exists | `os.path.exists(squads/dispatch/scripts/dispatch-health-score.py)` | YES — health score is mandatory |
| P6 | Cost tracker script exists | `os.path.exists(squads/dispatch/scripts/cost-tracker.py)` | YES — cost calculations must be deterministic |
| P7 | Dispatch heuristics data exists | `os.path.exists(squads/dispatch/data/dispatch-heuristics.yaml)` | YES — health score items come from here |

**If ANY precondition fails:** HALT with error message listing missing files. Do NOT generate partial reports.

---

## Phases

### PHASE 1: Load Run State (Worker — deterministic)

**Duration:** < 5 seconds
**Executor:** CODE (Python — `lib/pipeline_state.py`)

**Action Items:**

- [ ] 1.1 Load `_temp/dispatch/runs/{run_id}/state.json` via `lib/pipeline_state.py`
- [ ] 1.2 Validate state schema — all required fields present:
  - `run_id`, `status`, `started_at`, `completed_at`
  - `waves[]` with `wave_num`, `status`, `tasks[]`
  - `tasks[]` with `task_id`, `status`, `output_path`, `cost_usd`, `tokens_in`, `tokens_out`
- [ ] 1.3 Load `_temp/dispatch/runs/{run_id}/events.jsonl` via `lib/event_log.py`
- [ ] 1.4 Extract summary metrics from state:
  - Total tasks, total waves, total duration
  - Pass count, fail count, retry count
  - Total cost (sum of all task costs)
- [ ] 1.5 If `story_file` parameter provided, verify story file exists

**Checkpoint:** State loaded successfully, all required fields present. If state is malformed, HALT with parsing error.

---

### PHASE 2: Generate Execution Report (Agent — template fill)

**Duration:** 30-60 seconds
**Executor:** dispatch-chief (template fill with data from state)

**Action Items:**

- [ ] 2.1 Load template: `squads/dispatch/templates/execution-report-tmpl.md`
- [ ] 2.2 Fill **Run Summary** section:
  - `run_id`: from state
  - `started_at`, `completed_at`: from state timestamps
  - `duration_min`: calculate `(completed_at - started_at)` in minutes
  - `status`: from state (`completed`, `failed`, `halted`)
- [ ] 2.3 Fill **Input Summary** section:
  - `input_type`: story | prd | free_text | task_list
  - `input_path`: path to original input file
  - `description`: first 100 chars of input or story title
  - `total_tasks`: count from state
  - `total_waves`: count from state
- [ ] 2.4 Fill **Wave Results** table — for each wave:
  - `wave_num`: wave index (1-based)
  - `task_count`: number of tasks in wave
  - `pass_count`: tasks with status == "pass"
  - `fail_count`: tasks with status == "fail"
  - `retry_count`: sum of (attempts - 1) for retried tasks
  - `duration_sec`: wave wall-clock time
  - `cost_usd`: sum of task costs in wave
- [ ] 2.5 Fill **Deming PDSA** table — for each wave:
  - `predicted_outputs`: from `wave.prediction.predicted_files`
  - `actual_outputs`: count of tasks with status == "pass"
  - `predicted_cost`: from `wave.prediction.predicted_cost`
  - `actual_cost`: sum of actual task costs
  - `delta_pct`: percentage difference `((actual - predicted) / predicted) * 100`
- [ ] 2.6 Fill **Task Details** section — for each task:
  - `task_id`, `description`, `agent`, `model`, `executor_type`
  - `status`: pass | fail | retry | halted
  - `attempts` / `max_attempts`
  - `output_path`: full path to output file
  - `cost_usd`: actual cost
  - `error`: error message if failed (null if passed)
  - `acceptance_criteria[]`: each criterion with passed: true/false
- [ ] 2.7 Fill **Failures & Retries** section:
  - Filter tasks where `status == "fail"` or `attempts > 1`
  - For each: `task_id`, `error`, `attempts`, `resolution` (retried | escalated | halted)
- [ ] 2.8 Fill **Veto Gate Results** section:
  - Pre-execution vetos (V1.*): from state `pre_execution_gate` results
  - Post-execution vetos (V2.*): from state `post_execution_gate` results per wave

**Checkpoint:** All template variables filled. Zero `{{placeholder}}` text remaining. Verify with regex scan.

---

### PHASE 3: Generate Cost Report (Worker — deterministic calculation)

**Duration:** < 10 seconds
**Executor:** CODE (`scripts/cost-tracker.py`)

**Action Items:**

- [ ] 3.1 Run `scripts/cost-tracker.py --run-id {run_id} --generate-report`
- [ ] 3.2 Script calculates from state.json:
  - **Cost Summary:**
    - `total_cost_usd`: sum of all task.cost_usd
    - `avg_cost_per_task`: total / task_count
    - `opus_equivalent_cost`: estimate what the same work would cost in main Opus context
      - Formula: `total_input_tokens * ($5.00/MTok) + total_output_tokens * ($25.00/MTok)`
    - `savings_pct`: `((opus_equivalent - total_cost) / opus_equivalent) * 100`
    - `savings_usd`: `opus_equivalent - total_cost`
  - **Cost by Wave:** per-wave breakdown (tokens, cost, cache savings)
  - **Cost by Model:**
    - Worker tasks: count, $0.00 cost
    - Haiku tasks: count, tokens_in, tokens_out, input_cost ($1.00/MTok), output_cost ($5.00/MTok)
    - Sonnet tasks: count, tokens_in, tokens_out, input_cost ($3.00/MTok), output_cost ($15.00/MTok)
    - Percentage breakdown per model
  - **Prompt Caching Analysis:**
    - `cacheable_tokens`: tokens from static KB sections shared across same-domain tasks
    - `cache_hits`: number of tasks that benefited from cache
    - `cache_read_cost`: cacheable_tokens * cache_read_rate per model
    - `uncached_cost`: cacheable_tokens * normal_input_rate per model
    - `cache_savings`: uncached_cost - cache_read_cost
    - `cache_savings_pct`: percentage saved via caching
  - **Estimate vs Actual:**
    - Compare estimated cost (from Phase 3 predictions) vs actual cost
    - Compare estimated tasks vs actual tasks (may differ if tasks were split or merged)
    - Compare estimated duration vs actual
    - V2.3 check: actual cost within 3x estimate
  - **CODE > LLM Efficiency:**
    - `worker_count`: tasks executed by scripts
    - `agent_count`: tasks executed by LLM subagents
    - `code_llm_ratio`: worker_count / (worker_count + agent_count)
    - `worker_savings`: estimated cost if worker tasks had used Haiku instead
    - `code_llm_recommendation`: if ratio < 30%, suggest identifying more deterministic tasks
- [ ] 3.3 Load template: `squads/dispatch/templates/cost-report-tmpl.md`
- [ ] 3.4 Fill all template variables with calculated values
- [ ] 3.5 Verify zero `{{placeholder}}` text in filled report

**Checkpoint:** Cost report generated with all calculations. Verify totals add up (sum of wave costs == total cost). Verify savings percentage is >= 0% (dispatch should ALWAYS be cheaper than main context).

---

### PHASE 4: Calculate Health Score (Worker — deterministic)

**Duration:** < 10 seconds
**Executor:** CODE (`scripts/dispatch-health-score.py`)

**Action Items:**

- [ ] 4.1 Run `scripts/dispatch-health-score.py --run-id {run_id}`
- [ ] 4.2 Script evaluates 12 health items from `data/dispatch-heuristics.yaml`:
  - `[1] Story-Driven Input`: Input came from story/PRD (not free text)
  - `[2] DAG Wave Optimization`: wave-optimizer.py produced fewer waves than task count
  - `[3] Pre-Execution Gate Passed`: All veto conditions checked (0 errors)
  - `[4] Model Selection Applied`: Every task has explicit model (haiku/sonnet)
  - `[5] CODE > LLM Enforced`: Deterministic tasks used scripts, not LLM
  - `[6] Enrichment Levels Applied`: Tasks have MINIMAL/STANDARD/FULL based on domain
  - `[7] State Persisted`: state.json saved after every wave
  - `[8] Acceptance Criteria Verified`: Post-execution checked real criteria
  - `[9] Cost Tracked`: Actual token cost recorded per task
  - `[10] Zero Main Context Execution`: Opus terminal used 0 tokens for content work
  - `[11] Handoff Saved`: Run state can be resumed via *resume
  - `[12] Feedback Loop Active`: Failed tasks got feedback + retry
- [ ] 4.3 Each item scores 1 (PASS) or 0 (FAIL/LEGACY)
- [ ] 4.4 Total score: sum of all items (0-12)
- [ ] 4.5 Rating assignment:
  - 12/12 = "Exemplary run — all patterns applied"
  - 9-11/12 = "Good run — minor improvements"
  - 5-8/12 = "Needs work — significant patterns missing"
  - 1-4/12 = "Poor run — most patterns absent"
- [ ] 4.6 Insert health score into execution report (Health Score section)

**Checkpoint:** Health score is an integer between 0 and 12. Rating matches the scoring table. All 12 items have explicit PASS/FAIL/LEGACY status.

---

### PHASE 5: Update Story Checkboxes (Conditional — only if story input)

**Duration:** < 10 seconds
**Executor:** CODE (script or Edit tool)

**Action Items:**

- [ ] 5.1 Check if `story_file` parameter was provided AND file exists
- [ ] 5.2 If NO story input: skip this phase entirely, note in report "Input was not a story — no story checkboxes to update"
- [ ] 5.3 If YES story input:
  - [ ] 5.3.1 Read the story file
  - [ ] 5.3.2 For each task in the dispatch run that has `status == "pass"`:
    - Find the matching acceptance criterion checkbox in the story file
    - Match by task description or acceptance criterion text
    - Change `[ ]` to `[x]` ONLY for criteria whose corresponding task PASSED verification
  - [ ] 5.3.3 For tasks with `status == "fail"`:
    - DO NOT mark checkbox — leave as `[ ]`
    - Add a comment after the checkbox: `<!-- DISPATCH: task failed — {error} -->`
  - [ ] 5.3.4 Save the updated story file
- [ ] 5.4 Record which checkboxes were updated in the execution report (Story Update section)

**CRITICAL RULE:** Mark checkboxes ONLY for tasks that PASSED post-execution verification (Phase 5.5). NEVER mark a checkbox for a failed task. Marking a failed task as done is worse than not marking it — it creates a false sense of completion.

**Checkpoint:** If story input: checkboxes updated match exactly the set of tasks with `status == "pass"`. No extra checkboxes marked. No failed tasks marked as done.

---

### PHASE 6: Persist Reports & Log Completion (Worker — deterministic)

**Duration:** < 5 seconds
**Executor:** CODE (file write + event log)

**Action Items:**

- [ ] 6.1 Save execution report to `_temp/dispatch/runs/{run_id}/report.md`
- [ ] 6.2 Save cost report to `_temp/dispatch/runs/{run_id}/cost-report.md`
- [ ] 6.3 Log `run_completed` event via `lib/event_log.py`:
  ```python
  event_log.emit("run_completed",
      run_id=run_id,
      status=final_status,
      total_tasks=total_tasks,
      pass_count=pass_count,
      fail_count=fail_count,
      total_cost=total_cost,
      health_score=health_score,
      duration_sec=duration_sec
  )
  ```
- [ ] 6.4 If run failed or was halted, also log `run_failed` or `run_halted` with reason
- [ ] 6.5 Update state.json with final status and report paths:
  ```python
  state.report_path = f"_temp/dispatch/runs/{run_id}/report.md"
  state.cost_report_path = f"_temp/dispatch/runs/{run_id}/cost-report.md"
  state.health_score = health_score
  state.health_rating = rating
  state.status = "completed"  # or "completed_with_failures"
  state_manager.save()
  ```
- [ ] 6.6 Verify all output files exist and are non-empty:
  - `_temp/dispatch/runs/{run_id}/report.md` exists and > 0 bytes
  - `_temp/dispatch/runs/{run_id}/cost-report.md` exists and > 0 bytes
  - `_temp/dispatch/runs/{run_id}/state.json` updated with final status

**Checkpoint:** All report files persisted. State updated. Event logged. Files verified non-empty.

---

### PHASE 7: Present Results to User

**Duration:** < 5 seconds
**Executor:** dispatch-chief (output to user)

**Action Items:**

- [ ] 7.1 Generate summary output in dispatch-chief voice:
  ```
  DISPATCH COMPLETE

  Run: {run_id}
  Duration: {duration_min} min
  Tasks: {pass_count}/{total_tasks} completed
  Waves: {total_waves}
  Cost: ${total_cost} (estimated: ${estimated_cost})
  Health score: {health_score}/12 ({health_rating})

  Files created:
  - {file_1_path}
  - {file_2_path}
  - ...

  Reports:
  - Execution report: _temp/dispatch/runs/{run_id}/report.md
  - Cost report: _temp/dispatch/runs/{run_id}/cost-report.md

  Next steps:
  1. {contextual_next_step_1}
  2. {contextual_next_step_2}
  3. {contextual_next_step_3}
  4. Other
  ```
- [ ] 7.2 Next steps MUST be contextual (not generic):
  - If all tasks passed: "Review outputs at {output_dir}"
  - If some tasks failed: "Retry {N} failed tasks with *resume"
  - If health score < 9: "Review health score — {specific_improvement}"
  - If cost exceeded estimate: "Investigate cost overrun in cost-report.md"
  - Always include a "Run another dispatch" option
- [ ] 7.3 If story was updated, mention: "Story updated: {N} checkboxes marked [x]"

**Checkpoint:** User sees complete summary with actionable next steps. No generic "want to continue?" questions.

---

## Acceptance Criteria

| # | Criterion | Method | PASS/FAIL |
|---|-----------|--------|-----------|
| AC1 | Execution report generated and saved | File exists at `_temp/dispatch/runs/{run_id}/report.md` AND size > 0 bytes | Binary |
| AC2 | Cost report generated and saved | File exists at `_temp/dispatch/runs/{run_id}/cost-report.md` AND size > 0 bytes | Binary |
| AC3 | Health score calculated | Integer 0-12, rating matches scoring table | Binary |
| AC4 | Zero placeholders in reports | `grep -cE '\{\{[a-z_]+\}\}' report.md == 0` | Binary |
| AC5 | Cost totals are correct | Sum of wave costs == total cost. Sum of model costs == total cost | Binary |
| AC6 | Savings percentage >= 0% | Dispatch cost <= Opus equivalent cost | Binary |
| AC7 | Story checkboxes accurate (if story input) | ONLY passed tasks have [x]. Zero failed tasks marked [x] | Binary |
| AC8 | Event log updated | `events.jsonl` contains `run_completed` event with correct run_id | Binary |
| AC9 | State file updated | `state.json` has `status: completed` and report paths | Binary |
| AC10 | User receives summary with next steps | Output includes file list + numbered options (1,2,3,4) | Binary |

---

## Output

| Artifact | Path | Format |
|----------|------|--------|
| Execution Report | `_temp/dispatch/runs/{run_id}/report.md` | Markdown (from execution-report-tmpl.md) |
| Cost Report | `_temp/dispatch/runs/{run_id}/cost-report.md` | Markdown (from cost-report-tmpl.md) |
| Updated State | `_temp/dispatch/runs/{run_id}/state.json` | JSON (final status + report paths) |
| Updated Event Log | `_temp/dispatch/runs/{run_id}/events.jsonl` | JSONL (run_completed event appended) |
| Updated Story (conditional) | `{story_file}` path | Markdown (checkboxes [x] for passed tasks) |

---

## Dependencies

### Templates (loaded in Phase 2-3)

| Template | Phase | Purpose |
|----------|-------|---------|
| `templates/execution-report-tmpl.md` | 2 | Execution report structure with Handlebars-style variables |
| `templates/cost-report-tmpl.md` | 3 | Cost breakdown structure with pricing tables |

### Scripts (executed in Phase 3-4)

| Script | Phase | Purpose |
|--------|-------|---------|
| `scripts/cost-tracker.py` | 3 | Deterministic cost calculations — token math, savings, caching |
| `scripts/dispatch-health-score.py` | 4 | 12-point health assessment from dispatch-heuristics.yaml |

### Data (read in Phase 4)

| Data File | Phase | Purpose |
|-----------|-------|---------|
| `data/dispatch-heuristics.yaml` | 4 | Health score item definitions (12 items) |

### Library Modules (imported in Phase 1, 6)

| Module | Phase | Purpose |
|--------|-------|---------|
| `lib/pipeline_state.py` | 1, 6 | Load/save DispatchState, WaveState, TaskState |
| `lib/event_log.py` | 6 | Append run_completed event to events.jsonl |

---

## Key Rules

### CODE > LLM

All calculations in this task are deterministic and MUST use scripts:

| Calculation | Script | Why Not LLM |
|-------------|--------|-------------|
| Cost math (token pricing) | `scripts/cost-tracker.py` | Arithmetic must be exact |
| Health score (12 items) | `scripts/dispatch-health-score.py` | Binary checks, no judgment |
| Savings percentage | `scripts/cost-tracker.py` | Formula: `((opus - actual) / opus) * 100` |
| Cache efficiency | `scripts/cost-tracker.py` | Token-level accounting |
| File existence checks | `os.path.exists()` | Deterministic I/O |

LLM is used ONLY for:
- Filling the execution report template with human-readable narrative
- Generating contextual next steps based on run results
- Formulating the user-facing summary

### Never Inflate Metrics

- Report ACTUAL results, not aspirational ones
- If a task failed, report it as failed — do not mask with "partially completed"
- If cost exceeded estimate, report the delta — do not round down
- If health score is low, report the score — do not add caveats like "but it was close"
- Health score items are binary: PASS or FAIL. No "mostly passed"

### Health Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 12/12 | Exemplary | Log as reference run for future benchmarking |
| 9-11/12 | Good | Note specific items that failed for improvement |
| 5-8/12 | Needs Work | Flag for review — significant patterns missing |
| 1-4/12 | Poor | Investigate root cause — likely systemic issue |

### Story Checkbox Rules

- Mark `[x]` ONLY for tasks where:
  1. Post-execution gate (V2.*) PASSED
  2. All acceptance criteria for that task verified as met
  3. Output file exists and is non-empty
- NEVER mark `[x]` for a task that:
  1. Failed any V2.* veto
  2. Was halted by circuit breaker
  3. Exceeded max retry attempts
  4. Has unresolved errors
- If the run was halted mid-execution, only mark checkboxes for tasks that completed BEFORE the halt

---

## Anti-Patterns

| FORBIDDEN | DO THIS INSTEAD |
|-----------|-----------------|
| Generate report without reading state.json | ALWAYS load state first (Phase 1) |
| Calculate costs with LLM (approximation) | ALWAYS use scripts/cost-tracker.py (exact) |
| Skip health score "because run was simple" | ALWAYS calculate health score — every run, no exception |
| Mark all story checkboxes as done | ONLY mark PASSED tasks — verify each one |
| Generic next steps ("want to continue?") | Contextual next steps based on actual run results |
| Partial report (skip cost or health) | ALL sections mandatory — execution + cost + health |
| Report without file list | ALWAYS list every file created with full paths |
| Omit failure details | ALWAYS show error message and resolution for each failure |

---

## Metadata

```yaml
task_id: report-execution
version: 1.0.0
squad: dispatch
agent: dispatch-chief
phase: 6
executor_types: [worker, agent]
est_time_min: 2
est_time_max: 5
created: 2026-02-10
source: "config.yaml tasks.reporting[2]"
pipeline_position: "Final phase — produces user-facing deliverables"
patterns:
  - "DS-EP-001: Three Ways Pipeline (Reporting = Third Way — Learning)"
  - "DS-CP-001: Context Economy (cost report proves ROI)"
  - "DS-QG-001: Operational Definitions (health score = measurable quality)"
```

---

*report-execution Task - Dispatch Squad v1.0.0*
*Created: 2026-02-10*
*Phase: 6 (Reporting)*
*Lines: 250+*
