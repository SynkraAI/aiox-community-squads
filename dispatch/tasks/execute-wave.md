# Execute Wave

| Field | Value |
|-------|-------|
| **Task ID** | `execute-wave` |
| **Version** | `1.0.0` |
| **Purpose** | Execute a single wave of tasks in TRUE PARALLEL via subagents |
| **Agent** | `dispatch-chief` (orchestrates execution) |
| **Phase** | Phase 5 (Execution) |
| **Pattern** | `DS-EP-001` (Three Ways Pipeline — Flow) |
| **Estimated Time** | Variable: 2-15 minutes per wave (depends on wave size and task complexity) |

---

## Description

Receives a wave manifest containing a set of independent tasks (no inter-task
dependencies within the wave) and executes ALL of them in TRUE PARALLEL using
subagents. Worker tasks (deterministic scripts) run via Bash tool. Agent tasks
(requiring LLM reasoning) launch via Task tool with explicit model parameter.
All tasks in a single wave fire in the SAME tool call block. After all tasks
complete, results are recorded in state.json for resume capability. Failures
are handled with retry logic (simple failures) or halt (cascading failures).

**Critical constraint:** ZERO execution happens in main context (Law #0).
Every task runs via subagent or script. The main context only orchestrates.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `wave_manifest_path` | string | YES | Path to wave-manifest.yaml for current wave |
| `wave_number` | integer | YES | Wave index (1-based) within the current run |
| `run_id` | string | YES | Unique run identifier (e.g., `run-2026-02-10-001`) |

---

## Preconditions

Before starting this task, ALL of the following MUST be true:

- [ ] `wave_manifest_path` exists and is valid YAML
- [ ] Wave manifest contains at least 1 task
- [ ] Wave manifest contains at most `max_concurrent` tasks (default: 7, from config.yaml)
- [ ] All tasks in wave have routing fields populated (agent, executor_type, model, enrichment_level, timeout_seconds)
- [ ] Pre-execution gate (QG-PRE) has PASSED for this wave
- [ ] Previous wave (if any) has status COMPLETED or SKIPPED in state.json
- [ ] `scripts/enrich-task.py` is accessible and executable
- [ ] `templates/task-prompt-tmpl.md` exists
- [ ] `lib/pipeline_state.py` is importable
- [ ] Run directory exists: `_temp/dispatch/runs/{run_id}/`

**If any precondition fails:** STOP. Report which precondition failed. Do NOT execute partial waves.

---

## Phase 1: Load Wave

**Objective:** Parse wave manifest and prepare all tasks for execution.

### Action Items

- [ ] 1.1 Read `wave_manifest_path` — parse YAML, extract task list
- [ ] 1.2 Validate wave structure:
  - Each task has: `task_id`, `task_name`, `agent`, `executor_type`, `model`, `enrichment_level`, `kb_files`, `timeout_seconds`, `output_path`, `acceptance_criteria`
  - Task count <= `max_concurrent` (7 from config)
- [ ] 1.3 Read current state from `_temp/dispatch/runs/{run_id}/state.json` via `lib/pipeline_state.py`
- [ ] 1.4 Check for previously attempted tasks (resume scenario):
  - If task status is COMPLETED → skip (already done)
  - If task status is FAILED with attempts < max_retries (2) → include for retry
  - If task status is FAILED with attempts >= max_retries → skip, already exhausted
- [ ] 1.5 Build final task list for this wave execution (excluding already completed)
- [ ] 1.6 Log wave start event via `lib/event_log.py`:
  - `event: wave_start`
  - `wave_number`: current wave
  - `task_count`: number of tasks to execute
  - `timestamp`: ISO 8601

### Checkpoint 1

- [ ] Wave manifest parsed without error
- [ ] All tasks have required routing fields
- [ ] Task count within max_concurrent limit
- [ ] Resume state handled correctly (completed tasks skipped)
- [ ] Wave start event logged

---

## Phase 2: Enrich Tasks

**Objective:** Inject KB context into each task's prompt using enrichment scripts.

### Action Items

For EACH task in the wave (parallel-safe — no dependencies between enrichments):

- [ ] 2.1 **Determine enrichment level** — Read `enrichment_level` from task metadata:
  - MINIMAL: Skip enrichment entirely (Worker tasks)
  - STANDARD: Inject agent context file only
  - FULL: Inject agent context + domain KB + relevant docs
- [ ] 2.2 **Run enrichment script** — Execute `scripts/enrich-task.py` with parameters:
  ```
  python scripts/enrich-task.py \
    --task-id {task_id} \
    --template templates/task-prompt-tmpl.md \
    --enrichment-level {MINIMAL|STANDARD|FULL} \
    --kb-files {comma-separated paths from task.kb_files} \
    --output _temp/dispatch/runs/{run_id}/prompts/{task_id}.md
  ```
- [ ] 2.3 **Verify enriched prompt** — Check output file exists and is non-empty
- [ ] 2.4 **For Worker tasks** — No enrichment needed. Script command is already defined in task metadata. Skip steps 2.2-2.3.
- [ ] 2.5 **For Haiku tasks** — Verify enriched prompt contains:
  - "DO NOT ask questions. Execute immediately." (mandatory per Haiku patterns)
  - Instructions in ENGLISH (output can be PT-BR if specified)
  - Template reference or inline template for outputs > 50 lines
  - Single deliverable specification
  - No code-switching (EN+PT mixed in instructions)
- [ ] 2.6 **For Sonnet tasks** — Verify enriched prompt contains:
  - Clear evaluation criteria (if evaluation task)
  - Sufficient context for judgment

### Checkpoint 2

- [ ] Every Agent task has an enriched prompt file at `_temp/dispatch/runs/{run_id}/prompts/{task_id}.md`
- [ ] Every enriched prompt is non-empty
- [ ] Haiku prompts pass all 5 Haiku constraints
- [ ] Worker tasks have no enrichment (MINIMAL)

---

## Phase 3: Prepare Executors

**Objective:** Build the exact tool calls for each task before firing.

### Action Items

For EACH task:

- [ ] 3.1 **Worker tasks** — Prepare Bash tool call:
  ```
  Tool: Bash
  command: {task.script_command}
  timeout: {task.timeout_seconds * 1000}  # convert to ms
  description: "Worker: {task.task_name}"
  ```
  - Verify script path exists before preparing
  - Scripts run directly (no subagent overhead)

- [ ] 3.2 **Agent (Haiku) tasks** — Prepare Task tool call:
  ```
  Tool: Task
  prompt: {contents of enriched prompt file}
  model: "haiku"
  subagent_type: "general-purpose"
  max_turns: 15
  ```
  - Read enriched prompt from `_temp/dispatch/runs/{run_id}/prompts/{task_id}.md`
  - **ALWAYS** set `model` explicitly — NEVER inherit from parent (Law #2)
  - Set `run_in_background: false` for MCP tasks (foreground_only flag)

- [ ] 3.3 **Agent (Sonnet) tasks** — Prepare Task tool call:
  ```
  Tool: Task
  prompt: {contents of enriched prompt file}
  model: "sonnet"
  subagent_type: "general-purpose"
  max_turns: 20
  ```
  - Same as Haiku but with sonnet model and higher max_turns
  - **ALWAYS** set `model` explicitly — NEVER inherit from parent (Law #2)

- [ ] 3.4 **Log task preparation** — For each task, record via `scripts/log-task-start.py`:
  - `task_id`, `executor_type`, `model`, `enrichment_level`, `timestamp`

### Checkpoint 3

- [ ] Every task has a prepared tool call definition
- [ ] Worker tasks point to existing scripts
- [ ] Agent tasks have model set EXPLICITLY (haiku or sonnet)
- [ ] No task inherits model from parent context
- [ ] MCP tasks have `run_in_background: false`
- [ ] All task starts logged

---

## Phase 4: Execute in TRUE PARALLEL

**Objective:** Fire ALL task tool calls in a SINGLE tool call block for maximum parallelism.

### THIS IS THE CRITICAL PHASE — READ CAREFULLY

### Action Items

- [ ] 4.1 **Build parallel tool call block** — Assemble ALL prepared tool calls into a SINGLE response:
  - All Bash calls (Worker tasks) in same block
  - All Task calls (Agent tasks) in same block
  - They fire SIMULTANEOUSLY — true parallel execution
  - Maximum tasks per block: `max_concurrent` (7 from config)
  - If wave has > 7 tasks: split into sub-batches of 7, execute sequentially

- [ ] 4.2 **Execute the block** — Send all tool calls at once:
  ```
  <tool_calls>
    <Bash command="python script1.py" timeout="30000" />
    <Bash command="python script2.py" timeout="30000" />
    <Task prompt="..." model="haiku" max_turns="15" />
    <Task prompt="..." model="haiku" max_turns="15" />
    <Task prompt="..." model="sonnet" max_turns="20" />
  </tool_calls>
  ```
  - **NEVER** execute tasks sequentially when they can be parallel
  - **NEVER** execute in main context (Law #0) — ALL via tool calls

- [ ] 4.3 **Wait for all results** — All tool calls in a block complete before proceeding
- [ ] 4.4 **Collect results** — For each completed task, capture:
  - `status`: SUCCESS or FAILED
  - `output`: tool call result content
  - `duration_ms`: execution time
  - `error`: error message if FAILED

### Checkpoint 4

- [ ] All tasks in wave have been executed (or attempted)
- [ ] Results collected for every task
- [ ] No task executed in main context
- [ ] Parallel execution confirmed (tasks ran simultaneously, not sequentially)

---

## Phase 5: Record Results

**Objective:** Persist all task results to state.json for resume capability and reporting.

### Action Items

- [ ] 5.1 **Process each result** — For each task result:
  - If SUCCESS:
    - Verify output file exists at `task.output_path` (if applicable)
    - Set `task.status: COMPLETED`
    - Record `task.duration_ms`
    - Record `task.cost_estimate` (from model pricing in config)
  - If FAILED:
    - Set `task.status: FAILED`
    - Record `task.error` message
    - Increment `task.attempts` counter
    - Record `task.duration_ms`

- [ ] 5.2 **Update state.json** — Via `lib/pipeline_state.py`:
  ```python
  from lib.pipeline_state import DispatchState
  state = DispatchState.load(run_id)
  for task_id, result in results.items():
      state.update_task(task_id, result)
  state.save()
  ```

- [ ] 5.3 **Log results** — Via `lib/event_log.py`:
  - For each task: `event: task_complete` or `event: task_failed`
  - Include `task_id`, `status`, `duration_ms`, `model`, `attempts`

- [ ] 5.4 **Calculate wave metrics**:
  - `tasks_completed`: count of SUCCESS
  - `tasks_failed`: count of FAILED
  - `wave_duration_ms`: max(task.duration_ms) — parallel execution, so wall time = longest task
  - `wave_cost_estimate`: sum of individual task costs
  - `success_rate`: tasks_completed / total_tasks

### Checkpoint 5

- [ ] state.json updated with results for ALL tasks in wave
- [ ] Event log has entries for every task
- [ ] Wave metrics calculated and stored

---

## Phase 6: Handle Failures

**Objective:** Apply retry logic or escalation based on failure patterns.

### Decision Tree

```
How many tasks failed in this wave?

0 failures → CONTINUE to next wave
1 failure  → RETRY (simple failure)
2 failures → RETRY all failed (with warning)
3+ failures → HALT wave, present to user (cascading failure)
```

### Action Items

- [ ] 6.1 **Count failures** — From Phase 5 results, count tasks with status FAILED
- [ ] 6.2 **Simple failure (1-2 failed)** — For each failed task:
  - Check `task.attempts` count
  - If attempts < 2 (max retries): add to retry queue
  - If attempts >= 2: mark as `EXHAUSTED`, move to next wave
  - Retry uses SAME enriched prompt (no changes)
  - Retry increments `task.attempts` by 1
  - Log: `event: task_retry, task_id, attempt_number`
- [ ] 6.3 **Execute retries** — Run retry queue using same parallel execution pattern (Phase 4):
  - Build tool call block for retry tasks only
  - Execute in parallel
  - Collect results
  - Update state.json
- [ ] 6.4 **Cascading failure (3+ failed)** — HALT the wave:
  - Set `wave.status: HALTED`
  - Record all failure details in state.json
  - Present failure report to user:
    ```
    WAVE {N} HALTED: {count} tasks failed

    Failed tasks:
    1. {task_name} — {error_message}
    2. {task_name} — {error_message}
    3. {task_name} — {error_message}

    Options:
    1. Retry all failed tasks
    2. Skip failed tasks, continue to next wave
    3. Abort entire run
    4. Other
    ```
  - **WAIT for user decision** — do NOT auto-retry cascading failures
- [ ] 6.5 **Timeout handling** — For tasks that exceeded `timeout_seconds`:
  - Mark as FAILED with error: `TIMEOUT after {timeout_seconds}s`
  - Do NOT retry timeout failures (likely a structural problem)
  - Move to next wave
- [ ] 6.6 **Circuit breaker check** — After handling failures:
  - Count consecutive failures across ALL waves in this run
  - If consecutive_failures >= 5 (circuit_breaker from config): HALT ENTIRE RUN
  - Report to user: "Circuit breaker triggered: {count} consecutive failures"

### Checkpoint 6

- [ ] All simple failures retried (up to 2 attempts)
- [ ] Cascading failures halted and presented to user
- [ ] Timeout failures marked and skipped
- [ ] Circuit breaker evaluated
- [ ] state.json reflects final status of all retried tasks

---

## Phase 7: Finalize Wave

**Objective:** Update wave status and prepare for next wave or reporting.

### Action Items

- [ ] 7.1 **Determine wave status**:
  - All tasks COMPLETED → `wave.status: COMPLETED`
  - Some tasks COMPLETED, some EXHAUSTED → `wave.status: PARTIAL`
  - All tasks FAILED → `wave.status: FAILED`
  - Halted by user or circuit breaker → `wave.status: HALTED`

- [ ] 7.2 **Update state.json** with wave-level metadata:
  ```yaml
  wave_{N}:
    status: COMPLETED | PARTIAL | FAILED | HALTED
    tasks_total: N
    tasks_completed: N
    tasks_failed: N
    tasks_exhausted: N
    duration_ms: N
    cost_estimate: $N.NN
    success_rate: N%
    started_at: ISO 8601
    completed_at: ISO 8601
  ```

- [ ] 7.3 **Log wave completion** — Via `lib/event_log.py`:
  - `event: wave_complete`
  - Include all wave metrics

- [ ] 7.4 **Display progress** — Via `lib/progress.py`:
  ```
  Wave {N}/{total_waves}: {status}
  Tasks: {completed}/{total} completed | {failed} failed | {exhausted} exhausted
  Duration: {wall_time}s | Cost: ${estimate}
  ```

- [ ] 7.5 **Check if more waves remain**:
  - If YES and wave status is not HALTED → return control to dispatch-chief for next wave
  - If NO → signal pipeline to move to Phase 6 (Reporting)
  - If HALTED → wait for user decision

### Checkpoint 7

- [ ] Wave status correctly determined and recorded
- [ ] state.json fully updated with wave and task results
- [ ] Progress displayed to user
- [ ] Next action determined (next wave, reporting, or halt)

---

## Acceptance Criteria

All criteria are binary (PASS/FAIL). ALL must PASS.

| # | Criterion | Measurement |
|---|-----------|-------------|
| AC1 | All tasks in wave were executed via subagent or script, NOT in main context | Event log shows tool type (Bash or Task) for every task |
| AC2 | Agent tasks have model set EXPLICITLY (haiku or sonnet) | No task inherits model from parent context |
| AC3 | Tasks within a wave executed in parallel (same tool call block) | Event log timestamps show simultaneous start times (within 1s) |
| AC4 | state.json updated after wave completion | `state.json` has wave_{N} entry with all metrics |
| AC5 | Failed tasks retried up to 2 times before marking exhausted | `task.attempts <= 3` for all tasks (1 initial + 2 retries) |
| AC6 | 3+ failures in single wave triggers HALT, not auto-retry | Wave status is HALTED when 3+ failures occur |
| AC7 | Circuit breaker triggers at 5 consecutive failures | Run status is HALTED after 5 consecutive failures |
| AC8 | MCP tasks executed in foreground only | Tasks with `mcp_required: true` have `run_in_background: false` |
| AC9 | Haiku tasks include "DO NOT ask questions. Execute immediately." | All Haiku enriched prompts contain the string |
| AC10 | Wave max concurrency of 7 respected | No tool call block contains > 7 parallel calls |
| AC11 | Resume capability works (re-running skips completed tasks) | Completed tasks have `skip: true` on re-execution |
| AC12 | Wave progress displayed after completion | User sees wave status, counts, duration, cost |

---

## Output Specification

| Field | Value |
|-------|-------|
| **File** | `_temp/dispatch/runs/{run_id}/state.json` |
| **Format** | JSON (managed by `lib/pipeline_state.py`) |
| **Content** | Updated state with wave results, task statuses, metrics |

### State Structure After Wave

```json
{
  "run_id": "run-2026-02-10-001",
  "status": "executing",
  "current_wave": 3,
  "waves": {
    "wave_1": { "status": "COMPLETED", "tasks_completed": 5, "tasks_failed": 0 },
    "wave_2": { "status": "COMPLETED", "tasks_completed": 4, "tasks_failed": 1 },
    "wave_3": {
      "status": "COMPLETED",
      "tasks_total": 6,
      "tasks_completed": 5,
      "tasks_failed": 0,
      "tasks_exhausted": 1,
      "duration_ms": 45200,
      "cost_estimate": "$0.142",
      "success_rate": "83%",
      "started_at": "2026-02-10T14:30:00Z",
      "completed_at": "2026-02-10T14:30:45Z"
    }
  },
  "tasks": {
    "task_001": { "status": "COMPLETED", "attempts": 1, "duration_ms": 12300 },
    "task_002": { "status": "COMPLETED", "attempts": 1, "duration_ms": 8700 },
    "task_003": { "status": "EXHAUSTED", "attempts": 3, "error": "Template not found" }
  }
}
```

---

## Dependencies

| Dependency | Type | Path (relative to squad root) |
|------------|------|-------------------------------|
| Enrich Task Script | script | `scripts/enrich-task.py` |
| Task Prompt Template | template | `templates/task-prompt-tmpl.md` |
| Pipeline State Library | lib | `lib/pipeline_state.py` |
| Event Log Library | lib | `lib/event_log.py` |
| Progress Library | lib | `lib/progress.py` |
| Log Task Start Script | script | `scripts/log-task-start.py` |
| Haiku Patterns | data | `data/haiku-patterns.yaml` |
| Timeout Rules | data | `data/timeout-rules.yaml` |
| Dispatch State Template | template | `templates/dispatch-state-tmpl.json` |

---

## Error Handling

| Error | Action |
|-------|--------|
| Wave manifest missing or invalid YAML | HALT. Cannot execute without manifest. |
| Enrichment script fails | Mark affected task as FAILED. Continue with other tasks. |
| Enriched prompt file missing | Mark affected task as FAILED (enrichment error). Continue with others. |
| Subagent returns empty result | Treat as FAILED. Retry per Phase 6 logic. |
| Script execution timeout | Mark as FAILED with TIMEOUT error. Do NOT retry. |
| state.json write fails | CRITICAL. Retry write 3 times. If still fails, dump state to stderr and HALT. |
| lib/pipeline_state.py import fails | HALT. Pipeline state is essential for resume capability. |
| Max concurrent exceeded | Split wave into sub-batches of 7. Execute sub-batches sequentially. |

---

## Performance Notes

- **Wall time** for a wave = duration of LONGEST task (parallel execution)
- **Cost** for a wave = sum of all task costs (each task billed independently)
- **Haiku tasks** typically complete in 5-30 seconds
- **Sonnet tasks** typically complete in 15-90 seconds
- **Worker tasks** typically complete in 1-10 seconds
- **Wave of 7 Haiku tasks** ≈ 30 seconds wall time, ~$0.049 total cost
- **Wave of 7 Sonnet tasks** ≈ 90 seconds wall time, ~$0.175 total cost
