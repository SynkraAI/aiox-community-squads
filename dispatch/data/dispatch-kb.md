# Dispatch Squad — Knowledge Base

> Consolidated knowledge for the Dispatch parallel execution engine.

---

## What is Dispatch?

Dispatch is the **execution backbone** of AIOS — every parallelizable work goes through it. It receives stories/PRDs/tasks, decomposes them into atomic sub-tasks, optimizes into DAG-based waves, routes to correct agents/models, and executes in parallel via subagents.

**Philosophy:** "Never contaminate the main context. Always subagents. Always."

---

## The 7 Immutable Laws

| # | Law | Rule |
|---|-----|------|
| 0 | **NEVER MAIN CONTEXT** | Zero execution in terminal principal. ALL work via subagents. |
| 1 | **CODE > LLM** | Deterministic → script. Reasoning → LLM. |
| 2 | **RIGHT MODEL** | Haiku for defined tasks. Sonnet for judgment. Opus NEVER as executor. |
| 3 | **STORY-DRIVEN** | All work from stories with acceptance criteria. |
| 4 | **SLASH COMMAND MAP** | Route with full path (`/copy:tasks:create-sales-page`), never `@`. |
| 5 | **WAVE OPTIMIZED** | DAG topological sort. Maximum parallelism. |
| 6 | **OPTIMIZE EVERYTHING** | Worker vs Agent decision on every task. |

---

## Elite Minds

### Gene Kim (dispatch-chief)
- **Three Ways of DevOps:** Flow → Feedback → Learning
- **Flow:** Fast left-to-right, make work visible, reduce batch sizes, build in quality
- **Feedback:** Right-to-left loops, rapid error detection, verification
- **Learning:** Experimentation and compound learning across dispatches

### Donald Reinertsen (wave-planner)
- **Queue Management:** Invisible queues = poor performance. Make ALL work visible.
- **Batch Size Optimization:** Smaller batches = faster flow. U-curve for economic batch size.
- **WIP Constraints:** Limit parallel tasks per wave to avoid context thrashing.
- **Cost of Delay:** Every queued task has a delay cost — prioritize by economic impact.

### Eliyahu Goldratt (wave-planner)
- **Five Focusing Steps:** IDENTIFY constraint → EXPLOIT → SUBORDINATE → ELEVATE → REPEAT
- **Critical Chain:** Longest path of RESOURCE dependencies, not just logical dependencies.
- **Drum-Buffer-Rope:** Pace all work at rate of constraint (rate limits, parallel limits).

### W. Edwards Deming (quality-gate)
- **Operational Definitions:** Every term measurable and unambiguous.
- **PDSA:** Predict results → Execute → Study actual vs predicted → Act on learnings.
- **Statistical Process Control:** Normal variation vs special cause.
- **Quality Built In:** Prevent defects before downstream, don't catch after.

### Pedro Valério (quality-gate)
- **Veto Conditions:** Formal blocking conditions with IDs (V0.*, V1.*, V2.*).
- **Gate Classification:** Human gates (latency 24h) vs automatic gates (< 60s).
- **Self-Healing:** Simple → auto-fix. Complex → escalate. No gray zone.
- **IDS:** REUSE > ADAPT > CREATE. Create only with justification.

---

## Pipeline Flow

```
Phase 0: SUFFICIENCY GATE (dispatch-chief)
  ├── Classify input (story/PRD/free text)
  ├── Validate sufficiency (veto V0.*)
  └── If insufficient → redirect to correct agent

Phase 1: DECOMPOSITION (wave-planner)
  ├── Extract tasks from story
  ├── Create atomic sub-tasks
  └── Build dependency DAG

Phase 2: ROUTING (task-router)
  ├── Determine domain per task
  ├── Select agent + model
  └── Determine enrichment level

Phase 3: WAVE OPTIMIZATION (wave-planner)
  ├── Topological sort of DAG
  ├── Group independent tasks into waves
  └── Apply WIP limits

Phase 4: ENRICHMENT (dispatch-chief → enrich-task.py)
  ├── Load KB per domain
  ├── Inject context per enrichment level
  └── Apply task-prompt template

Phase 4.5: PRE-EXECUTION QUALITY GATE (quality-gate)
  ├── Check ALL veto conditions (V1.*)
  ├── Validate Haiku prompt rules
  └── BLOCK if any fail → return to planner

Phase 5: EXECUTION (dispatch-chief → subagents)
  ├── Send ALL wave tasks in SAME tool call
  ├── Wait for completion
  ├── Verify acceptance criteria
  └── Retry failed tasks

Phase 5.5: POST-EXECUTION GATE (quality-gate)
  ├── Check output files exist
  ├── Check files non-empty
  └── Check cost within budget

Phase 6: REPORTING (dispatch-chief)
  ├── Generate execution report
  ├── Generate cost report
  ├── Update story checkboxes
  └── Save final state
```

---

## Cost Economy (2026 Pricing)

| Context | Cost per interaction | Ratio |
|---------|---------------------|-------|
| Main Opus (50k tokens) | $0.30 | 1x |
| Haiku subagent (2k tokens) | $0.007 | 43x cheaper |
| Haiku with cache | $0.005 | 58x cheaper |

---

## Key Data Files

| File | Purpose |
|------|---------|
| `domain-registry.yaml` | Domain → Agent → KB mapping |
| `model-selection-rules.yaml` | When Haiku vs Sonnet vs Opus |
| `veto-conditions.yaml` | All blocking conditions (V0.*, V1.*, V2.*) |
| `enrichment-rules.yaml` | MINIMAL/STANDARD/FULL definitions |
| `timeout-rules.yaml` | Per-task, per-wave, per-run timeouts |
| `haiku-patterns.yaml` | 6 validated prompt patterns |
| `dispatch-heuristics.yaml` | Gate classification, self-healing, health score |

---

## Quick Reference: Commands

| Command | Purpose |
|---------|---------|
| `*new {input}` | Start new dispatch |
| `*resume` | Resume interrupted dispatch |
| `*analyze {input}` | Dry run (plan without executing) |
| `*estimate {input}` | Quick cost estimate |
| `*status` | Current dispatch status |
| `*abort` | Cancel and save state |
| `*health {run_id}` | 12-point health score |
| `*history` | Past dispatch runs |
