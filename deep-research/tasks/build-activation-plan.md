# Build Activation Plan

**Task ID:** `dr-build-plan`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Build Activation Plan |
| **status** | `pending` |
| **responsible_executor** | dr-orchestrator |
| **execution_type** | `Agent` |
| **input** | Use case classification, available agents roster |
| **output** | Sequenced activation plan with tiers and parallelism |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
After query classification, the orchestrator constructs a concrete activation plan that sequences Tier 0 diagnostic agents, parallelizes Tier 1 execution agents, and queues QA agents. The plan respects dependency ordering: Tier 0 must complete before Tier 1 begins, and all Tier 1 outputs must be collected before QA runs.

## Input
- **use_case_classification** (object) - Output from classify-research-query containing use case IDs, agent routing, and confidence
- **available_agents** (array) - Current roster of agents with their readiness status (ready/busy/unavailable)

## Output
- **activation_plan** (object) - Contains `tier_0_sequence` (ordered array of Tier 0 agent tasks), `tier_1_parallel` (set of Tier 1 agent tasks that run concurrently), `qa_sequence` (ordered array of QA agent tasks), `estimated_steps` (total expected turns)
- **unavailable_agent_warnings** (array) - Agents that were requested but are not available, with fallback strategy

## Action Items
### Step 1: Verify Tier 0 Readiness
Check that sackett, booth, and creswell are available. Tier 0 always runs in fixed sequence: sackett (PICO formulation) then booth (methodology selection) then creswell (research design). If any Tier 0 agent is unavailable, halt and report -- Tier 0 is non-negotiable.

### Step 2: Select Tier 1 Agents
From the use case classification, resolve primary and secondary agents. Check each against the available agents roster. For unavailable primary agents, escalate to the user. For unavailable secondary agents, log a warning and proceed without them.

### Step 3: Configure QA Sequence
Always activate ioannidis (evidence reliability audit) first, then kahneman (decision quality audit). QA agents receive all Tier 1 outputs as input. If the query is classified as UC-003 (OSINT), add an extra source verification pass to ioannidis.

### Step 4: Produce Activation Plan
Assemble the final plan object with all three tiers, estimated step count, and any warnings. Validate that no circular dependencies exist and that every agent in the plan has a defined task file.

## Acceptance Criteria
- [ ] Tier 0 sequence always contains sackett, booth, creswell in that exact order
- [ ] Tier 1 agents match the routing from the use case classification
- [ ] QA sequence runs ioannidis before kahneman
- [ ] Unavailable agents produce explicit warnings with fallback strategies
- [ ] The activation plan is a valid structured object consumable by the orchestrator dispatch loop

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
