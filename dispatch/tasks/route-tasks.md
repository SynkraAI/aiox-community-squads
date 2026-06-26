# Route Tasks

| Field | Value |
|-------|-------|
| **Task ID** | `route-tasks` |
| **Version** | `1.0.0` |
| **Purpose** | For each atomic task in execution plan, determine the correct agent, model, enrichment level, and timeout |
| **Agent** | `task-router` |
| **Phase** | Phase 2 (Routing) |
| **Pattern** | `DS-RP-001` |
| **Estimated Time** | 2-5 minutes |

---

## Description

Reads the execution plan produced by Phase 1 (Planning) and enriches every atomic task
with routing metadata: which agent executes it, which model powers the agent, how much
KB context to inject, and what timeout to enforce. Multi-domain tasks are split into
independent sub-tasks so each sub-task routes to exactly one domain. The output is the
same execution-plan.yaml file, now fully populated with routing fields ready for the
pre-execution gate.

### Worker Scripts (CODE > LLM)

Phases 2-6 can be executed **entirely as Worker scripts** (zero LLM needed):

| Phase | Script | Purpose |
|-------|--------|---------|
| 2 | `scripts/score-domain.py` | Domain detection via keyword matching |
| 4 | `scripts/select-model.py` | Q1-Q4 model decision tree |
| 5 | `scripts/assign-enrichment.py` | MINIMAL/STANDARD/FULL assignment |
| 6 | `scripts/assign-timeout.py` | Timeout + max_turns assignment |
| **All** | `scripts/route-tasks.py` | **Full pipeline orchestrator** (calls all above) |

**Preferred execution:** `python scripts/route-tasks.py --plan {execution_plan_path} --format table`

This replaces ~60% of task-router LLM work with deterministic scripts (~$0.075 savings per dispatch).

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `execution_plan_path` | string | YES | Path to execution-plan.yaml produced by `decompose-to-waves` |

---

## Preconditions

Before starting this task, ALL of the following MUST be true:

- [ ] `execution_plan_path` exists and is valid YAML
- [ ] Each task in the plan has `task_name`, `description`, `output_path`, `acceptance_criteria`
- [ ] `data/domain-registry.yaml` is accessible and non-empty
- [ ] `data/model-selection-rules.yaml` is accessible and non-empty
- [ ] `data/enrichment-rules.yaml` is accessible and non-empty
- [ ] `data/timeout-rules.yaml` is accessible and non-empty
- [ ] `data/command-registry.yaml` is accessible and non-empty (run `scripts/build-command-registry.py` if missing)

**If any precondition fails:** STOP. Report which precondition failed and what is needed to fix it. Do NOT attempt partial routing.

---

## Phase 1: Load Routing Data

**Objective:** Load all reference files into memory before processing any task.

### Action Items

- [ ] 1.1 Read `execution_plan_path` — parse full YAML, count total tasks
- [ ] 1.2 Read `data/domain-registry.yaml` — load all domain definitions with triggers, agents, KB files
- [ ] 1.3 Read `data/model-selection-rules.yaml` — load decision tree (Worker → Haiku → Sonnet → Opus redirect)
- [ ] 1.4 Read `data/enrichment-rules.yaml` — load enrichment levels (MINIMAL, STANDARD, FULL) with criteria
- [ ] 1.5 Read `data/timeout-rules.yaml` — load timeout values per executor type
- [ ] 1.6 Read `data/command-registry.yaml` — load all available slash commands across squads

### Checkpoint 1

- [ ] All 6 reference files loaded without error
- [ ] Total task count matches plan metadata
- [ ] Domain registry has at least 4 domains (development, architecture, quality, copy)
- [ ] Command registry has at least 20 entries

---

## Phase 2: Domain Detection

**Objective:** For each task, determine which domain(s) it belongs to using keyword scoring.

### Action Items

For EACH task in execution plan:

- [ ] 2.1 **Extract keywords** — Tokenize `task_name` + `description` into lowercase keywords. Remove stop words.
- [ ] 2.2 **CODE > LLM:** Run `python squads/dispatch/scripts/score-domain.py --task "$DESCRIPTION" --format json` for deterministic domain scoring. Do NOT use LLM for keyword matching.
  - Script scores against domain triggers from `domain-registry.yaml`:
  - Count matches against `triggers.primary` keywords → multiply by `weight_primary` (default: 3)
  - Count matches against `triggers.secondary` keywords → multiply by `weight_secondary` (default: 1)
  - Total score = (primary_matches * weight_primary) + (secondary_matches * weight_secondary)
- [ ] 2.3 **Rank domains** — Sort domains by total score descending
- [ ] 2.4 **Apply threshold** — Domain is a match only if score >= 3 (at least one primary keyword hit)
- [ ] 2.5 **Handle zero matches** — If no domain scores >= 3:
  - Check if task is purely filesystem/structural (mkdir, mv, cp) → assign domain: `worker`
  - Otherwise → flag as `UNROUTABLE`, add to routing_issues list
- [ ] 2.6 **Handle multi-domain** — If 2+ domains score >= 3:
  - Mark task as `MULTI_DOMAIN`
  - Record all matching domains with scores
  - Task will be split in Phase 2.5

### Checkpoint 2

- [ ] Every task has at least one domain assigned OR is flagged as UNROUTABLE
- [ ] Multi-domain tasks are identified and marked
- [ ] Zero tasks left without a domain classification
- [ ] Routing issues list is empty OR contains only genuinely ambiguous tasks

---

## Phase 2.5: Multi-Domain Splitting

**Objective:** Split multi-domain tasks into independent sub-tasks, one per domain.

### Action Items

For EACH task flagged `MULTI_DOMAIN`:

- [ ] 2.5.1 **Analyze task description** — Identify which parts map to which domain
- [ ] 2.5.2 **Create sub-tasks** — One sub-task per domain, each with:
  - `task_name`: `{original_name}__split_{domain}` (double underscore separator)
  - `description`: portion of original description relevant to this domain
  - `output_path`: derived from original, suffixed with domain
  - `acceptance_criteria`: subset from original that applies to this domain
  - `parent_task`: reference to original task name
- [ ] 2.5.3 **Update dependencies** — Sub-tasks from same parent are independent (can parallelize). External dependencies preserved on all sub-tasks.
- [ ] 2.5.4 **Remove original** — Replace original multi-domain task with its sub-tasks in the plan
- [ ] 2.5.5 **Update task count** — Recalculate total tasks after splitting

### Checkpoint 2.5

- [ ] Zero tasks remain with `MULTI_DOMAIN` flag
- [ ] Every sub-task has exactly ONE domain
- [ ] All sub-tasks have valid `parent_task` reference
- [ ] Dependencies are correctly inherited

---

## Phase 3: Agent Selection

**Objective:** Map each task's domain to the correct executing agent using full slash command paths.

### Action Items

For EACH task (including newly split sub-tasks):

- [ ] 3.1 **Look up domain agent** — From `domain-registry.yaml`, get `agents.primary` for the task's domain
- [ ] 3.2 **Resolve slash command** — Cross-reference with `data/command-registry.yaml`:
  - Find the most specific matching command for the task type
  - Use FULL slash path format: `/squad:category:command` (e.g., `/copy:tasks:create-sales-page`)
  - **NEVER** use `@` notation (Law #4)
- [ ] 3.3 **Handle squad agents** — If domain maps to a squad agent:
  - Verify the squad exists in command registry
  - Use squad-specific task path (e.g., `/copy:tasks:create-email-sequence`)
- [ ] 3.4 **Handle core agents** — If domain maps to core agent:
  - Use core agent path (e.g., `/dev`, `/qa`, `/architect`)
- [ ] 3.5 **Flag architecture tasks** — If domain is `architecture`:
  - Set `routing_action: REDIRECT` (not DISPATCH)
  - Add note: "Architecture tasks should NOT be dispatched — redirect to /architect"
  - These tasks will be removed from execution plan and reported to user
- [ ] 3.6 **Flag MCP tasks** — If task involves ActiveCampaign, Beehiiv, or ClickUp:
  - Set `mcp_required: true`
  - Set `foreground_only: true` (MCP unavailable in background subagents)
  - Set `run_in_background: false`

### Checkpoint 3

- [ ] Every task has an `agent` field with full slash path or core agent reference
- [ ] Zero tasks use `@` notation
- [ ] Architecture tasks are flagged REDIRECT, not DISPATCH
- [ ] MCP tasks are flagged `foreground_only: true`
- [ ] All slash paths exist in command-registry.yaml

---

## Phase 4: Model Selection

**Objective:** Apply the decision tree from `model-selection-rules.yaml` to assign the correct model to each task.

### Decision Tree (executed in order — first match wins):

```
Q1: Is output 100% predictable? (mkdir, mv, template fill with no reasoning)
    YES → executor: worker (script)
    NO  → continue

Q2: Does task have an explicit template to fill?
    YES → executor: agent, model: haiku
    NO  → continue

Q3: Does task require judgment, evaluation, or creative writing > 500 words?
    YES → executor: agent, model: sonnet
    NO  → continue

Q4: Is task architectural or strategic?
    YES → DO NOT DISPATCH. Set routing_action: REDIRECT
    NO  → default to haiku (conservative choice)
```

### Action Items

For EACH task:

- [ ] 4.1 **Apply Q1** — Check if task type is in worker list (CREATE folder, MOVE file, DELETE, RENAME, template fill without reasoning)
- [ ] 4.2 **Apply Q2** — Check if task references a template file. Verify template exists at declared path.
- [ ] 4.3 **Apply Q3** — Check if task type is EVALUATE, AUDIT, ANALYZE, or if description contains judgment indicators
- [ ] 4.4 **Apply Q4** — Check if domain is architecture. If so, already flagged in Phase 3.
- [ ] 4.5 **Record decision** — For each task, set:
  - `executor_type`: worker | agent
  - `model`: null (worker) | haiku | sonnet
  - `decision_rationale`: which Q was matched and why
- [ ] 4.6 **Apply Haiku constraints** — For all haiku tasks, verify:
  - Task can produce 1 deliverable
  - Template exists for outputs > 50 lines
  - Instructions can be expressed in English without code-switching

### Checkpoint 4

- [ ] Every task has `executor_type` and `model` assigned
- [ ] Zero tasks assigned to Opus (Law #2 — Opus NEVER as executor)
- [ ] Worker tasks have `model: null`
- [ ] Haiku tasks pass Haiku constraint check
- [ ] Decision rationale recorded for every task

---

## Phase 5: Enrichment Assignment

**Objective:** Determine how much KB context to inject into each task's prompt.

### Enrichment Levels

| Level | When | KB Injection |
|-------|------|-------------|
| MINIMAL | Worker tasks, simple file ops | None (0 tokens) |
| STANDARD | Haiku tasks with template | Agent context file only (~400 tokens) |
| FULL | Sonnet tasks, evaluation, audit | Agent context + domain KB + relevant docs (~2000 tokens) |

### Action Items

For EACH task:

- [ ] 5.1 **Apply enrichment rules** from `data/enrichment-rules.yaml`:
  - Worker tasks → MINIMAL
  - Haiku with template → STANDARD
  - Sonnet or evaluation/audit → FULL
- [ ] 5.2 **Resolve KB files** — From `domain-registry.yaml`, get `kb_files` list for the task's domain
- [ ] 5.3 **Verify KB files exist** — For STANDARD and FULL enrichment, confirm all KB file paths resolve to real files
- [ ] 5.4 **Record enrichment** — Set on each task:
  - `enrichment_level`: MINIMAL | STANDARD | FULL
  - `kb_files`: list of file paths to inject (empty for MINIMAL)

### Checkpoint 5

- [ ] Every task has `enrichment_level` assigned
- [ ] Worker tasks have `enrichment_level: MINIMAL` and empty `kb_files`
- [ ] STANDARD/FULL tasks have at least one valid KB file path
- [ ] No broken KB file paths

---

## Phase 6: Timeout Assignment

**Objective:** Set execution timeout for each task based on executor type.

### Timeout Rules

| Executor | Timeout | Source |
|----------|---------|--------|
| Worker (script) | 30s | `data/timeout-rules.yaml` |
| Agent (Haiku) | 120s | `data/timeout-rules.yaml` |
| Agent (Sonnet) | 300s | `data/timeout-rules.yaml` |

### Action Items

- [ ] 6.1 **Apply timeout rules** from `data/timeout-rules.yaml` for each task based on `executor_type` and `model`
- [ ] 6.2 **Handle MCP tasks** — MCP tasks may need extended timeout (1.5x base) due to API latency
- [ ] 6.3 **Record timeout** — Set `timeout_seconds` on each task
- [ ] 6.4 **Calculate max_turns** — For agent tasks:
  - Haiku: `max_turns: 15`
  - Sonnet: `max_turns: 20`
  - Worker: not applicable (single script execution)

### Checkpoint 6

- [ ] Every task has `timeout_seconds` assigned
- [ ] Agent tasks have `max_turns` assigned
- [ ] MCP tasks have extended timeout if applicable

---

## Phase 7: Write Updated Plan

**Objective:** Write the fully routed execution plan back to YAML.

### Action Items

- [ ] 7.1 **Compile routing summary** — Count tasks per executor type, per model, per enrichment level
- [ ] 7.2 **Add routing metadata** to plan header:
  - `routing_timestamp`: ISO 8601
  - `routing_agent`: task-router
  - `total_tasks`: count after splitting
  - `tasks_by_model`: {worker: N, haiku: N, sonnet: N}
  - `tasks_redirected`: count of REDIRECT tasks
  - `routing_issues`: list of unresolved issues
- [ ] 7.3 **Write updated YAML** — Overwrite `execution_plan_path` with fully routed plan
- [ ] 7.4 **Report redirected tasks** — List any REDIRECT tasks for user awareness
- [ ] 7.5 **Report unroutable tasks** — List any UNROUTABLE tasks that need manual intervention

### Checkpoint 7

- [ ] Updated execution-plan.yaml is valid YAML
- [ ] Every task has ALL routing fields: `agent`, `executor_type`, `model`, `enrichment_level`, `kb_files`, `timeout_seconds`
- [ ] Routing metadata header is present and accurate
- [ ] Task count matches sum of tasks_by_model

---

## Acceptance Criteria

All criteria are binary (PASS/FAIL). ALL must PASS.

| # | Criterion | Measurement |
|---|-----------|-------------|
| AC1 | Every task in plan has `agent` field populated | `grep -c "agent:" plan.yaml == total_tasks` |
| AC2 | Zero tasks use `@` notation for agent | `grep -c "@" plan.yaml == 0` (in agent fields) |
| AC3 | Every task has `executor_type` (worker/agent) | Field present on 100% of tasks |
| AC4 | Every task has `model` (null/haiku/sonnet) | Field present on 100% of tasks |
| AC5 | Zero tasks assigned to Opus | `grep -c "model: opus" plan.yaml == 0` |
| AC6 | Every task has `enrichment_level` | Field present on 100% of tasks |
| AC7 | Every task has `timeout_seconds` | Field present on 100% of tasks |
| AC8 | Architecture tasks flagged REDIRECT, not dispatched | All architecture-domain tasks have `routing_action: REDIRECT` |
| AC9 | MCP tasks flagged `foreground_only: true` | All AC/BH/ClickUp tasks have the flag |
| AC10 | Multi-domain tasks split into single-domain sub-tasks | Zero tasks remain with `MULTI_DOMAIN` flag |
| AC11 | All slash command paths exist in command-registry.yaml | Cross-reference check passes |
| AC12 | Updated plan is valid YAML | `python -c "import yaml; yaml.safe_load(open('plan.yaml'))"` succeeds |

---

## Output Specification

| Field | Value |
|-------|-------|
| **File** | `execution-plan.yaml` (same path as input, overwritten) |
| **Format** | YAML |
| **Content** | Original plan + routing fields on every task + routing metadata header |

### Routing Fields Added Per Task

```yaml
tasks:
  - task_name: "create-email-sequence"
    # ... original fields ...
    # === ROUTING FIELDS (added by route-tasks) ===
    agent: "/copy:tasks:create-email-sequence"
    executor_type: agent
    model: haiku
    enrichment_level: STANDARD
    kb_files:
      - "squads/copy/data/copywriting-kb.md"
    timeout_seconds: 120
    max_turns: 15
    mcp_required: false
    foreground_only: false
    routing_action: DISPATCH
    decision_rationale: "Q2 match: has template (email-sequence-tmpl.yaml)"
```

---

## Dependencies

| Dependency | Type | Path (relative to squad root) |
|------------|------|-------------------------------|
| Domain Registry | data | `data/domain-registry.yaml` |
| Model Selection Rules | data | `data/model-selection-rules.yaml` |
| Enrichment Rules | data | `data/enrichment-rules.yaml` |
| Timeout Rules | data | `data/timeout-rules.yaml` |
| Command Registry | data | `data/command-registry.yaml` |
| Build Command Registry | script | `scripts/build-command-registry.py` |
| Domain Scorer | script | `scripts/score-domain.py` |
| Model Selector | script | `scripts/select-model.py` |
| Enrichment Assigner | script | `scripts/assign-enrichment.py` |
| Timeout Assigner | script | `scripts/assign-timeout.py` |
| **Full Pipeline** | script | `scripts/route-tasks.py` |

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing domain-registry.yaml | HALT. Cannot route without domain definitions. |
| Missing command-registry.yaml | Run `scripts/build-command-registry.py` first. If still missing, HALT. |
| Task matches zero domains | Flag as UNROUTABLE. Include in routing_issues. Present to user. |
| Slash command not in registry | Flag task with `routing_issue: command_not_found`. Continue routing others. |
| KB file path doesn't exist | Downgrade enrichment to MINIMAL. Add warning to routing_issues. |
