# ═══════════════════════════════════════════════════════════════════════════════
# TASK: Plan Execution
# ID: plan-execution
# Version: 1.0.0
# Purpose: Transform story/PRD/task-list into a structured execution plan
#          with atomic sub-tasks and dependency DAG.
# Agent: wave-planner
# Phase in Pipeline: Phase 1 (Decomposition)
# Pattern: DS-WP-001 (DAG Topological Sort), DS-QG-001 (Operational Definitions)
# ═══════════════════════════════════════════════════════════════════════════════

## Overview

Receives a story file (with acceptance criteria), PRD, or structured task list
and decomposes it into atomic sub-tasks suitable for parallel dispatch execution.
Each sub-task is sized at ~500-2000 tokens, has a single deliverable, measurable
acceptance criteria, and explicit dependencies on other tasks. The output is a
complete execution plan in YAML format following the execution-plan template.

This task is the FIRST reasoning step in the dispatch pipeline. Everything
downstream (routing, wave optimization, execution) depends on the quality of
this decomposition. Garbage in = garbage out.

### Worker Scripts (CODE > LLM)

Several phases can be executed as Worker scripts (zero LLM needed):

| Phase | Script | Purpose |
|-------|--------|---------|
| 2 | `scripts/extract-quantities.py` | Extract quantity patterns from text |
| 4 | `scripts/estimate-batch-cost.py` | Per-task cost estimation |
| 4 | `scripts/select-model.py` | Q1-Q4 model decision tree |
| 3 | `scripts/wave-optimizer.py --check-cycles` | Cycle detection in DAG |
| 3 | `scripts/critical-chain-analyzer.py` | Critical path calculation |

**Preferred:** Run deterministic phases as scripts, reserve LLM for Phase 1 (task extraction from natural language) and Phase 2 (atomization requiring judgment).

---

## Inputs

| Parameter    | Type   | Required | Description                                                        |
|-------------|--------|----------|--------------------------------------------------------------------|
| story_file  | path   | YES      | Absolute path to .md story, PRD, or task list file                 |
| input_type  | enum   | YES      | One of: `story`, `prd`, `task_list`. Determines parsing strategy   |
| run_id      | string | NO       | Dispatch run ID. Auto-generated if not provided (dispatch-YYYYMMDD-HHMMSS) |

---

## Preconditions

Before starting this task, the following MUST be true:

- [ ] `story_file` exists and is readable
- [ ] `story_file` has been validated by dispatch-chief sufficiency gate (V0.* checks passed)
- [ ] If `input_type` is `story`: file contains acceptance criteria (V0.1 passed)
- [ ] If `input_type` is `prd`: file contains requirements section
- [ ] If `input_type` is `task_list`: each item has at least a description
- [ ] Template file exists: `squads/dispatch/templates/execution-plan-tmpl.yaml`
- [ ] Data files exist: `squads/dispatch/data/veto-conditions.yaml`, `squads/dispatch/data/enrichment-rules.yaml`

---

## PHASE 0: Load Context

**Checkpoint:** All required files loaded and validated.

### Action Items

- [ ] 0.1 — Read the story/PRD/task-list file at `story_file` path (MUST read, never assume content)
- [ ] 0.2 — Read template: `squads/dispatch/templates/execution-plan-tmpl.yaml`
- [ ] 0.3 — Read veto conditions: `squads/dispatch/data/veto-conditions.yaml`
- [ ] 0.4 — Read enrichment rules: `squads/dispatch/data/enrichment-rules.yaml` (for quantity_patterns and acceptance_by_type)
- [ ] 0.5 — Read model selection rules: `squads/dispatch/data/model-selection-rules.yaml`
- [ ] 0.6 — Read timeout rules: `squads/dispatch/data/timeout-rules.yaml`
- [ ] 0.7 — Generate `run_id` if not provided: format `dispatch-YYYYMMDD-HHMMSS`
- [ ] 0.8 — Create run directory: `_temp/dispatch/runs/{run_id}/`

### Phase 0 Checkpoint

- [ ] All 6 data files successfully loaded
- [ ] run_id is set (provided or generated)
- [ ] Run directory exists at `_temp/dispatch/runs/{run_id}/`

---

## PHASE 1: Extract Raw Tasks

**Checkpoint:** All tasks extracted from input, none lost.

### Action Items

- [ ] 1.1 — **IF input_type == story:** Extract tasks from acceptance criteria checkboxes (`- [ ]` items). Each checkbox = 1 candidate task. Also extract any implicit tasks from the story description that are not covered by checkboxes.
- [ ] 1.2 — **IF input_type == prd:** Extract requirements from requirements section. Each requirement = 1 or more candidate tasks. Decompose compound requirements (e.g., "create X and Y") into separate tasks.
- [ ] 1.3 — **IF input_type == task_list:** Parse each item as a candidate task. Validate each has a description.
- [ ] 1.4 — Apply quantity patterns from `enrichment-rules.yaml` (`quantity_patterns` section) to detect multiplied tasks (e.g., "3 newsletters" = 3 separate tasks, not 1).
- [ ] 1.5 — Count total raw tasks extracted. Log count.
- [ ] 1.6 — Verify no acceptance criterion from the original story is orphaned (every criterion maps to at least 1 task).

### Phase 1 Checkpoint

- [ ] Total raw tasks > 0 (if 0 tasks extracted, BLOCK — input is insufficient)
- [ ] Every original acceptance criterion maps to at least 1 task
- [ ] Quantity patterns applied (no compound deliverables remaining)

---

## PHASE 2: Atomize Tasks

**Checkpoint:** Every task is atomic — 1 task = 1 deliverable.

### Action Items

- [ ] 2.1 — For EACH raw task, verify it produces exactly 1 deliverable. If it produces multiple deliverables, SPLIT into separate tasks. (Veto V1.7: "Task has multiple deliverables")
- [ ] 2.2 — For EACH task, assign a sequential `task_id`: T001, T002, T003, etc.
- [ ] 2.3 — For EACH task, write a clear `description` that answers: WHAT to do, in one sentence. No vague verbs (V1.9: no "improve", "optimize", "enhance" without specifics).
- [ ] 2.4 — For EACH task, define `output_path` — the exact file path where the deliverable will be saved. (Veto V1.1: "Task has no output path")
- [ ] 2.5 — For EACH task, define `output_format`: one of `yaml`, `json`, `markdown`, `code`.
- [ ] 2.6 — For EACH task, write `acceptance_criteria` — a list of measurable, binary conditions. NEVER subjective: no "good quality", "well-written", "appropriate tone". (Veto V1.2) Use patterns from `enrichment-rules.yaml` `acceptance_by_type` section when task type matches.
- [ ] 2.7 — For EACH task, estimate token consumption:
  - `estimated_tokens_in`: input context tokens (prompt + KB + business context)
  - `estimated_tokens_out`: expected output tokens
  - Use enrichment level guidelines: MINIMAL ~500, STANDARD ~1500, FULL ~3000
- [ ] 2.8 — For EACH task, scan for placeholders: `[XXX]`, `{TODO}`, `TBD`, `[PLACEHOLDER]`. If found, resolve them NOW. (Veto V1.3)
- [ ] 2.9 — For EACH task, assign preliminary `timeout` from `timeout-rules.yaml` based on expected executor type. (Veto V1.8)

### Phase 2 Checkpoint

- [ ] Every task has exactly 1 deliverable (V1.7 passed)
- [ ] Every task has `task_id` assigned (T001..T{N})
- [ ] Every task has `output_path` defined (V1.1 passed)
- [ ] Every acceptance criterion is measurable and binary (V1.2 passed)
- [ ] Zero placeholders in any task (V1.3 passed)
- [ ] Zero vague verbs in descriptions (V1.9 passed)
- [ ] Every task has timeout assigned (V1.8 passed)

---

## PHASE 3: Build Dependency DAG

**Checkpoint:** Dependencies are explicit, no cycles.

### Action Items

- [ ] 3.1 — For EACH task, determine `depends_on`: list of task_ids that MUST complete before this task can start. Ask: "Does this task need output from another task?"
- [ ] 3.2 — For EACH task, determine `blocks`: list of task_ids that depend on THIS task's output. This is the inverse of `depends_on`.
- [ ] 3.3 — Verify consistency: if T002 depends_on T001, then T001 must have T002 in its `blocks` list.
- [ ] 3.4 — **CODE > LLM:** Run `python squads/dispatch/scripts/wave-optimizer.py tasks.json --check-cycles-json` to detect circular dependencies. Triggers V1.4 veto if cycles found. (Veto V1.4) If cycles detected, restructure by splitting the cyclic task.
- [ ] 3.5 — Identify root tasks: tasks with `depends_on: []` (no dependencies). These form Wave 1.
- [ ] 3.6 — Identify leaf tasks: tasks with `blocks: []` (nothing depends on them). These are final deliverables.
- [ ] 3.7 — Calculate critical path: the longest chain of sequential dependencies. Document it.

### Phase 3 Checkpoint

- [ ] Every task has `depends_on` defined (even if empty list `[]`)
- [ ] Every task has `blocks` defined (even if empty list `[]`)
- [ ] Zero circular dependencies (V1.4 passed)
- [ ] At least 1 root task exists (Wave 1 is not empty)
- [ ] Critical path identified and documented

---

## PHASE 4: Estimate Costs

**Checkpoint:** Cost estimate calculated for the full plan.

### Action Items

- [ ] 4.1 — For EACH task, assign preliminary `model` based on task complexity:
  - Deterministic (mkdir, move, validate) → `worker` ($0.00)
  - Well-defined with template → `haiku` (~$0.007/task)
  - Judgment/evaluation/creative → `sonnet` (~$0.025/task)
- [ ] 4.2 — Calculate per-task estimated cost: `(estimated_tokens_in * input_rate + estimated_tokens_out * output_rate) / 1_000_000`. Use pricing from `config.yaml` `context_economy.pricing_2026`.
- [ ] 4.3 — Sum all task costs for `estimated_cost_usd` at plan level.
- [ ] 4.4 — Calculate `estimated_duration_min`: sum of critical path task durations (sequential), not total tasks (parallel).
- [ ] 4.5 — Build `domain_summary`: group tasks by domain, count per domain, identify primary agent.
- [ ] 4.6 — Build `model_distribution`: count of worker, haiku, sonnet tasks.

### Phase 4 Checkpoint

- [ ] Every task has `model` assigned (even if preliminary — V1.10 will be enforced later by task-router)
- [ ] Plan-level `estimated_cost_usd` calculated
- [ ] Plan-level `estimated_duration_min` calculated
- [ ] `domain_summary` populated
- [ ] `model_distribution` populated

---

## PHASE 5: Generate Output

**Checkpoint:** execution-plan.yaml written and valid.

### Action Items

- [ ] 5.1 — Load template: `squads/dispatch/templates/execution-plan-tmpl.yaml`
- [ ] 5.2 — Fill template with all collected data:
  - `meta` section: run_id, input_type, input_path, description, timestamp, total_tasks, estimated_cost, estimated_duration
  - `story_acceptance` section: original criteria mapped to task_ids
  - `tasks` section: all atomized tasks with full attributes
  - `domain_summary` section: grouped by domain
  - `model_distribution` section: worker/haiku/sonnet counts
- [ ] 5.3 — Validate output against template validation rules (V1.1 through V1.11)
- [ ] 5.4 — Write output to: `_temp/dispatch/runs/{run_id}/execution-plan.yaml`
- [ ] 5.5 — Log task count, cost estimate, critical path length to console

### Phase 5 Checkpoint

- [ ] File exists at `_temp/dispatch/runs/{run_id}/execution-plan.yaml`
- [ ] File is valid YAML (parseable)
- [ ] File contains all required sections per template
- [ ] Zero placeholders remain in output

---

## Acceptance Criteria

All criteria are measurable and binary (PASS/FAIL):

1. Output file exists at `_temp/dispatch/runs/{run_id}/execution-plan.yaml`
2. Output file is valid YAML (parseable by any YAML parser)
3. Every task in the plan has exactly 1 deliverable (V1.7)
4. Every task has `output_path` defined (V1.1)
5. Every acceptance criterion is measurable and binary — no subjective terms (V1.2)
6. Zero placeholders `[XXX]`, `{TODO}`, `TBD` in output (V1.3)
7. Zero circular dependencies in the DAG (V1.4)
8. Every task has `timeout` assigned (V1.8)
9. Every original story acceptance criterion maps to at least 1 task
10. Total task count matches expected count from input analysis
11. `estimated_cost_usd` is calculated and > 0
12. Critical path is documented with task IDs

---

## Output Specification

| Field         | Value                                               |
|--------------|-----------------------------------------------------|
| Format       | YAML                                                 |
| Template     | `squads/dispatch/templates/execution-plan-tmpl.yaml` |
| Filename     | `execution-plan.yaml`                                |
| Location     | `_temp/dispatch/runs/{run_id}/`                      |
| Full path    | `_temp/dispatch/runs/{run_id}/execution-plan.yaml`   |

---

## Dependencies

| Resource | Type | Path |
|----------|------|------|
| Template | file | `squads/dispatch/templates/execution-plan-tmpl.yaml` |
| Veto Conditions | data | `squads/dispatch/data/veto-conditions.yaml` |
| Enrichment Rules | data | `squads/dispatch/data/enrichment-rules.yaml` |
| Model Selection Rules | data | `squads/dispatch/data/model-selection-rules.yaml` |
| Timeout Rules | data | `squads/dispatch/data/timeout-rules.yaml` |
| Config | yaml | `squads/dispatch/config.yaml` |
| Wave Optimizer | script | `scripts/wave-optimizer.py` |
| Cost Estimator | script | `scripts/estimate-batch-cost.py` |
| Model Selector | script | `scripts/select-model.py` |
| Critical Chain | script | `scripts/critical-chain-analyzer.py` |

---

## Error Handling

| Error                                    | Action                                              |
|-----------------------------------------|------------------------------------------------------|
| story_file does not exist               | BLOCK — return error with path                       |
| story_file has no acceptance criteria   | VETO V0.1 — redirect to /po                         |
| Input < 10 words, no deliverables      | VETO V0.2 — redirect to /pm or /po                  |
| Circular dependency detected            | VETO V1.4 — restructure DAG, split cyclic tasks     |
| Subjective acceptance criterion found   | VETO V1.2 — rewrite with measurable criterion       |
| Placeholder detected                    | VETO V1.3 — resolve before continuing               |
| 0 tasks extracted                       | BLOCK — input is insufficient for dispatch           |

---

## Estimated Time

| Scenario               | Time     |
|-----------------------|----------|
| Simple story (3-5 tasks)  | 5 min    |
| Medium story (6-15 tasks) | 8-10 min |
| Complex PRD (16-30 tasks) | 12-15 min |

---

## Next Step

After this task completes, the execution plan flows to:
1. **task-router** (route-tasks.md) — assigns agent, model, and enrichment level per task
2. **wave-planner** (decompose-to-waves.md) — optimizes into DAG-based waves
