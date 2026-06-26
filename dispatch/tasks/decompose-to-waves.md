# ═══════════════════════════════════════════════════════════════════════════════
# TASK: Decompose to Waves
# ID: decompose-to-waves
# Version: 1.0.0
# Purpose: Take execution plan and optimize into DAG-based waves via
#          topological sort + batch size optimization.
# Agent: wave-planner
# Phase in Pipeline: Phase 3 (Wave Optimization)
# Pattern: DS-WP-001 (DAG Topological Sort), DS-WP-002 (Batch Size),
#          DS-WP-003 (Drum-Buffer-Rope)
# ═══════════════════════════════════════════════════════════════════════════════

## Overview

Receives a completed execution plan (output of plan-execution + route-tasks)
and transforms it into an optimized set of execution waves. Uses Kahn's
algorithm via `scripts/wave-optimizer.py` for topological sort (CODE > LLM),
groups independent tasks into waves for maximum parallelism, applies WIP
constraints, Reinertsen batch size optimization, and Goldratt buffers.

The output is a wave-manifest.yaml that the execution engine (execute-wave)
consumes directly. Each wave contains tasks that can ALL run in true parallel
with zero inter-dependencies.

**Critical law:** ALWAYS use `scripts/wave-optimizer.py` for DAG sort.
NEVER sort manually or with LLM reasoning. CODE > LLM is non-negotiable
(Dispatch Law #1).

### Worker Scripts (CODE > LLM)

Most phases are deterministic and executed as Worker scripts:

| Phase | Script | Purpose |
|-------|--------|---------|
| 1 | `scripts/wave-optimizer.py` | DAG topological sort (Kahn's algorithm) |
| 2 | `scripts/batch-size-optimizer.py` | Reinertsen U-curve batch sizing |
| 3 | `scripts/critical-chain-analyzer.py` | Critical path + slack analysis |

**Preferred:** Only Phase 4 (PDSA predictions) requires LLM reasoning. All other phases are deterministic.

---

## Inputs

| Parameter            | Type   | Required | Description                                                         |
|---------------------|--------|----------|---------------------------------------------------------------------|
| execution_plan_path | path   | YES      | Path to execution-plan.yaml (output of plan-execution + route-tasks)|
| run_id              | string | YES      | Dispatch run ID (from execution plan meta.run_id)                   |
| max_parallel        | int    | NO       | Override max tasks per wave (default: 7 from config.yaml)           |

---

## Preconditions

Before starting this task, the following MUST be true:

- [ ] `execution_plan_path` exists and is readable
- [ ] execution-plan.yaml has been validated by quality-gate (V1.* checks passed)
- [ ] Every task in the plan has: task_id, depends_on, blocks, model, agent, timeout
- [ ] Script exists: `squads/dispatch/scripts/wave-optimizer.py`
- [ ] Template exists: `squads/dispatch/templates/wave-manifest-tmpl.yaml`
- [ ] Data file exists: `squads/dispatch/data/timeout-rules.yaml`
- [ ] Data file exists: `squads/dispatch/data/model-selection-rules.yaml`
- [ ] run directory exists: `_temp/dispatch/runs/{run_id}/`

---

## PHASE 0: Load Context

**Checkpoint:** All required files loaded and validated.

### Action Items

- [ ] 0.1 — Read the execution plan: `_temp/dispatch/runs/{run_id}/execution-plan.yaml`
- [ ] 0.2 — Validate execution plan has `tasks` array with >= 1 task
- [ ] 0.3 — Validate every task has `task_id`, `depends_on`, `model`, `timeout` fields
- [ ] 0.4 — Read template: `squads/dispatch/templates/wave-manifest-tmpl.yaml`
- [ ] 0.5 — Read timeout rules: `squads/dispatch/data/timeout-rules.yaml`
- [ ] 0.6 — Read config max_parallel: `squads/dispatch/config.yaml` → `subagent_constraints.recommended_wave_size` (default: 7)
- [ ] 0.7 — Extract the task dependency graph as adjacency list: `{task_id: [dependency_ids]}`

### Phase 0 Checkpoint

- [ ] Execution plan loaded and has >= 1 task
- [ ] Every task has required fields for DAG processing
- [ ] Template loaded
- [ ] max_parallel determined (param override or config default: 7)
- [ ] Adjacency list extracted

---

## PHASE 1: Topological Sort via Script (CODE > LLM)

**Checkpoint:** Topological sort completed without cycles.

### Action Items

- [ ] 1.1 — Prepare input for `scripts/wave-optimizer.py`:
  - Extract task_ids and their `depends_on` arrays from execution plan
  - Format as JSON: `{"tasks": [{"id": "T001", "depends_on": []}, {"id": "T002", "depends_on": ["T001"]}, ...]}`
  - Write to `_temp/dispatch/runs/{run_id}/dag-input.json`
- [ ] 1.2 — Run script: `python squads/dispatch/scripts/wave-optimizer.py --input _temp/dispatch/runs/{run_id}/dag-input.json --max-parallel {max_parallel}`
  - Script uses Kahn's algorithm for topological sort
  - Script detects cycles and returns non-zero exit code if found (V1.4)
  - Script groups independent tasks into waves respecting max_parallel
- [ ] 1.3 — Read script output: `_temp/dispatch/runs/{run_id}/dag-output.json`
  - Contains: `{"waves": [{"wave_num": 1, "task_ids": ["T001", "T003"]}, ...], "critical_path": ["T001", "T002", "T005"]}`
- [ ] 1.4 — IF script returns non-zero exit code (cycle detected):
  - Read error output for cycle details
  - VETO V1.4: "Circular dependency in DAG"
  - BLOCK — return to wave-planner (plan-execution) to fix dependencies
- [ ] 1.5 — Verify ALL task_ids from execution plan appear in exactly one wave (none lost, none duplicated)

### Phase 1 Checkpoint

- [ ] Script executed successfully (exit code 0)
- [ ] Zero circular dependencies (V1.4 passed)
- [ ] All task_ids present in exactly one wave
- [ ] Wave count > 0

---

## PHASE 2: Apply WIP Constraints and Batch Optimization

**Checkpoint:** Waves respect max_parallel and are batch-optimized.

### Action Items

- [ ] 2.1 — Verify each wave has <= `max_parallel` tasks. If script already enforced this, validate. If any wave exceeds limit, split into sub-waves preserving dependency order.
- [ ] 2.2 — Apply Reinertsen batch size optimization (U-curve analysis):
  - **Transaction cost** = overhead of launching a wave (state save, progress update, validation): ~fixed per wave
  - **Holding cost** = tokens sitting idle while waiting for wave to complete: proportional to queue depth
  - **Optimal batch** = point where marginal transaction cost = marginal holding cost
  - For typical dispatch: 5-7 tasks per wave is the sweet spot (from config)
  - If a wave has only 1 task and the next wave also has few, consider merging IF no dependencies are violated
- [ ] 2.3 — Group tasks by domain WITHIN waves for prompt caching benefit:
  - Tasks in same domain share KB context (STATIC section of prompt)
  - Same-domain tasks that run in same wave get cache hits
  - Calculate `same_domain_count` and `cache_savings_pct` per wave
- [ ] 2.4 — Apply Goldratt Drum-Buffer-Rope:
  - **Drum** = API rate limit (max_concurrent: 10 from config)
  - **Buffer** = wave-level timeout from `timeout-rules.yaml` (per_wave.max_wall_clock: 900s)
  - **Rope** = wave N+1 starts ONLY after wave N is COMPLETE (strict sequential)
  - Assign `wave_timeout` to each wave: max(task timeouts in wave) + 30s buffer

### Phase 2 Checkpoint

- [ ] Every wave has <= max_parallel tasks
- [ ] No wave has 0 tasks
- [ ] Batch size justified (not just arbitrary grouping)
- [ ] Prompt caching opportunities identified per wave
- [ ] Every wave has timeout assigned

---

## PHASE 3: Calculate Critical Path

**Checkpoint:** Critical path identified and documented.

### Action Items

- [ ] 3.1 — Extract critical path from script output (longest chain of sequential dependencies)
- [ ] 3.2 — Calculate critical path duration: sum of estimated durations for each task in the chain
- [ ] 3.3 — Identify bottleneck: the single task on the critical path with the longest estimated duration
- [ ] 3.4 — Calculate optimization metrics:
  - `total_tasks`: count of all tasks
  - `total_waves`: count of waves
  - `optimization_pct`: `((total_tasks - total_waves) / total_tasks) * 100` — reduction from serialization
  - `flow_efficiency_pct`: `(critical_path_duration / total_sequential_duration) * 100` — how much parallelism helps
- [ ] 3.5 — Build Reinertsen metrics summary:
  - `batch_size`: "{total_tasks} tasks in {total_waves} waves (avg {avg}/wave)"
  - `wip_limit`: max_parallel
  - `queue_depth`: tasks waiting per wave
  - `flow_efficiency`: flow_efficiency_pct

### Phase 3 Checkpoint

- [ ] Critical path chain documented with task IDs
- [ ] Critical path duration calculated in minutes
- [ ] Bottleneck task identified
- [ ] Optimization ratio calculated
- [ ] Reinertsen metrics populated

---

## PHASE 4: Deming PDSA Predictions

**Checkpoint:** Every wave has a prediction (Plan-Do-Study-Act).

### Action Items

- [ ] 4.1 — For EACH wave, generate prediction:
  - `expected_outputs`: count of tasks in wave (should equal task_count)
  - `expected_failures`: estimate based on task complexity (0 for worker-only waves, 1-2 for mixed)
  - `expected_cost_usd`: sum of per-task cost estimates in this wave
  - `expected_duration_sec`: max of task timeouts in wave (parallel = longest wins)
  - `rationale`: one sentence explaining why these predictions (e.g., "All worker tasks, zero LLM — expect 100% success")
- [ ] 4.2 — Calculate plan-level cost estimate:
  - `subtotal_usd`: sum of all wave expected costs
  - `cache_savings_usd`: estimated savings from prompt caching (same-domain tasks)
  - `total_estimated_usd`: subtotal - cache savings
  - `vs_opus_main_context`: "If done in Opus main context: ~${opus_cost}. Dispatch: ~${dispatch_cost}. Savings: {pct}%"

### Phase 4 Checkpoint

- [ ] Every wave has prediction section populated
- [ ] Plan-level cost estimate calculated
- [ ] Opus comparison calculated

---

## PHASE 5: Generate Output

**Checkpoint:** wave-manifest.yaml written and valid.

### Action Items

- [ ] 5.1 — Load template: `squads/dispatch/templates/wave-manifest-tmpl.yaml`
- [ ] 5.2 — Fill template with all collected data:
  - `meta` section: run_id, total_waves, total_tasks, max_parallel, critical_path_length, optimization_ratio, timestamp
  - `critical_path` section: chain, estimated_duration, bottleneck
  - `waves` section: all waves with tasks, predictions, constraints, prompt_caching
  - `cost_estimate` section: by_model, subtotal, cache_savings, total, vs_opus comparison
  - `reinertsen` section: batch_size, wip_limit, queue_depth, flow_efficiency
- [ ] 5.3 — Validate output against template validation rules:
  - No circular dependencies (V1.4 — already checked by script)
  - Each wave has <= max_parallel tasks
  - All tasks from execution-plan present in waves (none lost)
  - Critical path identified and documented
  - Every wave has prediction (Deming PDSA)
- [ ] 5.4 — Write output to: `_temp/dispatch/runs/{run_id}/wave-manifest.yaml`
- [ ] 5.5 — Log summary to console:
  - "{total_tasks} tasks → {total_waves} waves ({optimization_pct}% reduction)"
  - "Critical path: {critical_path_length} tasks, ~{critical_path_duration} min"
  - "Estimated cost: ${total_estimated_usd} (vs ${opus_cost} in main context)"

### Phase 5 Checkpoint

- [ ] File exists at `_temp/dispatch/runs/{run_id}/wave-manifest.yaml`
- [ ] File is valid YAML (parseable)
- [ ] File contains all required sections per template
- [ ] All tasks accounted for (none missing from execution plan)

---

## Acceptance Criteria

All criteria are measurable and binary (PASS/FAIL):

1. Output file exists at `_temp/dispatch/runs/{run_id}/wave-manifest.yaml`
2. Output file is valid YAML (parseable by any YAML parser)
3. `scripts/wave-optimizer.py` was used for topological sort (not LLM reasoning)
4. Zero circular dependencies in the DAG (V1.4)
5. Every wave contains <= `max_parallel` tasks (default 7)
6. All task_ids from execution-plan.yaml appear in exactly one wave (none lost, none duplicated)
7. Independent tasks (no mutual dependencies) are in the SAME wave (not serialized)
8. Critical path is documented with task IDs and estimated duration
9. Every wave has a Deming PDSA prediction section
10. Every wave has a timeout value assigned from timeout-rules.yaml
11. Cost estimate section is populated with by_model breakdown
12. Reinertsen metrics section is populated
13. Console log shows summary with task count, wave count, critical path, and cost

---

## Output Specification

| Field         | Value                                                |
|--------------|------------------------------------------------------|
| Format       | YAML                                                  |
| Template     | `squads/dispatch/templates/wave-manifest-tmpl.yaml`   |
| Filename     | `wave-manifest.yaml`                                  |
| Location     | `_temp/dispatch/runs/{run_id}/`                       |
| Full path    | `_temp/dispatch/runs/{run_id}/wave-manifest.yaml`     |

### Intermediate Files

| File                                                      | Purpose                              |
|----------------------------------------------------------|--------------------------------------|
| `_temp/dispatch/runs/{run_id}/dag-input.json`            | Input for wave-optimizer.py          |
| `_temp/dispatch/runs/{run_id}/dag-output.json`           | Output from wave-optimizer.py        |

---

## Dependencies

| File                                                    | Type   | Purpose                                          |
|--------------------------------------------------------|--------|--------------------------------------------------|
| `squads/dispatch/scripts/wave-optimizer.py`            | script | DAG topological sort (Kahn's algorithm) — CODE   |
| Batch Optimizer                                         | script | `scripts/batch-size-optimizer.py`                |
| Critical Chain                                          | script | `scripts/critical-chain-analyzer.py`             |
| `squads/dispatch/templates/wave-manifest-tmpl.yaml`    | file   | Output structure template                        |
| `squads/dispatch/data/timeout-rules.yaml`              | file   | Timeout assignment per executor type             |
| `squads/dispatch/data/model-selection-rules.yaml`      | file   | Model cost rates for estimation                  |
| `squads/dispatch/config.yaml`                          | file   | max_parallel, pricing, subagent_constraints      |

---

## Error Handling

| Error                                        | Action                                                     |
|---------------------------------------------|------------------------------------------------------------|
| execution-plan.yaml does not exist          | BLOCK — plan-execution must run first                      |
| execution-plan.yaml has 0 tasks             | BLOCK — nothing to optimize                                |
| wave-optimizer.py returns non-zero          | VETO V1.4 — cycle detected, return to plan-execution       |
| wave-optimizer.py not found at script path  | BLOCK — script dependency missing, notify devops           |
| Task missing depends_on field               | BLOCK — plan-execution produced incomplete output          |
| All tasks in single wave (no parallelism)   | WARNING — valid but suboptimal, log for review             |
| max_parallel exceeded after optimization    | Split wave into sub-waves, re-validate                     |

---

## Estimated Time

| Scenario                    | Time     |
|----------------------------|----------|
| Small plan (3-8 tasks)     | 2 min    |
| Medium plan (9-20 tasks)   | 3-4 min  |
| Large plan (21-50 tasks)   | 4-5 min  |

Time is dominated by script execution (< 1s) and template filling. The script
handles the computationally intensive DAG sort. LLM time is minimal — only
used for generating predictions and formatting.

---

## Next Step

After this task completes, the wave manifest flows to:
1. **quality-gate** (pre-execution-gate) — validates all V1.* conditions before execution
2. **dispatch-chief** (execute-wave) — executes waves sequentially, tasks within each wave in parallel
