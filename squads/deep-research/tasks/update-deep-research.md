# Update Deep Research Squad

**Task ID:** `dr-update-squad`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Update Deep Research Squad |
| **status** | `pending` |
| **responsible_executor** | dr-orchestrator |
| **execution_type** | `Agent` |
| **input** | Update request specifying changes |
| **output** | Updated squad artifacts with validation report |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Lifecycle task for modifying the Deep Research squad configuration. This covers adding new specialist agents, modifying existing agent prompts, updating task definitions, refreshing knowledge bases, adjusting pipeline routing, and upgrading framework references. All changes go through validation to ensure the squad remains internally consistent and functional after the update.

## Input
- **update_request** (object) - Contains `change_type` (add_agent/modify_agent/update_task/refresh_knowledge/modify_pipeline/upgrade_framework), `target` (which artifact to modify), `changes` (the specific modifications to apply), `reason` (justification for the update)

## Output
- **updated_artifacts** (array) - List of files modified with before/after summaries
- **validation_report** (object) - Contains `config_valid` (boolean), `agent_references_intact` (boolean), `task_dependencies_intact` (boolean), `pipeline_routing_valid` (boolean), `warnings` (array of non-blocking issues)

## Action Items
### Step 1: Identify Required Changes
Parse the update request and determine all files that need modification. Map the change type to affected artifacts:
- `add_agent`: new agent prompt file in agents/, update config.yaml roster, add task files, update pipeline routing
- `modify_agent`: edit agent prompt file, verify task compatibility
- `update_task`: edit task file in tasks/, verify agent references
- `refresh_knowledge`: update framework references and benchmark data within agent prompts
- `modify_pipeline`: update orchestrator routing logic, verify tier assignments
- `upgrade_framework`: update pattern versions, migrate deprecated fields

### Step 2: Apply Changes
Execute the modifications to each identified file. For agent additions, scaffold from the agent prompt template. For task updates, maintain HO-TP-001 pattern compliance. For pipeline changes, update the activation plan logic in the orchestrator. Preserve all existing functionality that is not targeted by the update.

### Step 3: Validate Configuration
Run validation checks against the updated squad:
- Config syntax: YAML/Markdown files parse correctly
- Agent references: every agent_id referenced in tasks exists in the roster
- Task dependencies: every task referenced in the pipeline has a corresponding task file
- Pipeline routing: every use case maps to valid agents and tasks
- No orphaned artifacts: no files exist that are unreferenced by any config

### Step 4: Run Smoke Tests
Execute a minimal dry-run of the pipeline with a sample query to verify the updated squad can classify a query, build an activation plan, and route to agents without errors. This does not require full execution -- just validation that the pipeline structure is intact.

## Acceptance Criteria
- [ ] All modified files are listed in the updated_artifacts output with change summaries
- [ ] Config validation confirms YAML/Markdown parsing succeeds
- [ ] Agent reference integrity check passes (no dangling references)
- [ ] Task dependency check passes (no missing task files)
- [ ] Smoke test confirms pipeline can execute basic classify-build-route cycle

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
