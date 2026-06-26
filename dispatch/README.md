# ⚡ Dispatch Squad — Parallel Execution Engine

> **Version:** 1.0.0 | **Minds:** Gene Kim, Reinertsen, Goldratt, Deming, Pedro Valério | **Status:** Active

---

## Overview

The Dispatch Squad is the **execution backbone** of AIOS. It receives stories, PRDs, or task lists, decomposes them into atomic sub-tasks, optimizes into DAG-based waves, routes to the correct agents/models, and executes in parallel via subagents — all while keeping the main Opus context clean.

**Core philosophy:** "Never contaminate the main context. Always subagents. Always."

**Cost savings:** ~43-58x cheaper than executing in the main Opus context.

---

## Architecture

```
                    ┌──────────────────────────────────┐
                    │         USER INPUT               │
                    │  Story / PRD / Free Text / Batch  │
                    └───────────────┬──────────────────┘
                                    │
                    ┌───────────────▼──────────────────┐
                    │      DISPATCH-CHIEF              │
                    │      (Gene Kim — Three Ways)      │
                    │  Orchestrates full pipeline        │
                    └──┬──────────┬──────────┬─────────┘
                       │          │          │
           ┌───────────▼──┐  ┌───▼────┐  ┌──▼──────────┐
           │ QUALITY-GATE  │  │ WAVE-  │  │ TASK-       │
           │ (Deming + PV) │  │PLANNER │  │ ROUTER      │
           │ Pre/post      │  │(Reiner-│  │ (Registry   │
           │ validation    │  │ tsen + │  │  based)     │
           │               │  │Goldratt│  │             │
           └───────────────┘  └────────┘  └─────────────┘
                                    │
                    ┌───────────────▼──────────────────┐
                    │         WAVE EXECUTION            │
                    │                                    │
                    │  Wave 1: [T1, T2, T3, T4] ← ALL  │
                    │          parallel via subagents    │
                    │  Wave 2: [T5, T6, T7] ← depends  │
                    │          on Wave 1 outputs         │
                    │  Wave N: [...]                     │
                    └──────────────────────────────────┘
```

---

## Elite Minds

| Mind | Framework | Role |
|------|-----------|------|
| **Gene Kim** | Three Ways of DevOps (Flow, Feedback, Learning) | `dispatch-chief` — pipeline orchestration |
| **Donald Reinertsen** | Product Development Flow (175 principles, queue theory) | `wave-planner` — batch optimization, WIP limits |
| **Eliyahu Goldratt** | Theory of Constraints + Critical Chain | `wave-planner` — bottleneck ID, Drum-Buffer-Rope |
| **W. Edwards Deming** | PDSA + Statistical Process Control | `quality-gate` — zero-ambiguity, predict-then-verify |
| **Pedro Valério** | Veto Conditions + Self-Healing | `quality-gate` — block impossible paths |

---

## Agents

| Agent | Tier | Mind | Purpose |
|-------|------|------|---------|
| `dispatch-chief` | Orchestrator | Gene Kim | Receives work, validates sufficiency, orchestrates pipeline |
| `quality-gate` | Tier 0 | Deming + PV | Pre/post-execution validation with veto conditions |
| `wave-planner` | Tier 1 | Reinertsen + Goldratt | DAG optimization, wave sizing, critical chain |
| `task-router` | Tier 2 | Registry-based | Agent/model/enrichment selection per task |

---

## Tasks

| Task | Purpose |
|------|---------|
| `plan-execution.md` | Story/task → execution plan |
| `decompose-to-waves.md` | Atomic decomposition + DAG optimization |
| `route-tasks.md` | Agent/model/enrichment selection |
| `execute-wave.md` | Execute single wave in parallel |
| `verify-wave.md` | Post-execution verification |
| `report-execution.md` | Generate execution + cost reports |
| `convert-input.md` | Normalize any input → dispatch format |

---

## Workflows

| Workflow | Purpose | Phases |
|----------|---------|--------|
| `wf-dispatch-main.yaml` | Story → Plan → Gate → Execute → Report | 7 |
| `wf-dispatch-free.yaml` | Free text → Dispatch (backward compat) | 8 |
| `wf-dispatch-batch.yaml` | Multiple stories in sequence | 4 |

---

## Checklists

| Checklist | Purpose |
|-----------|---------|
| `pre-dispatch-gate.md` | Sufficiency veto conditions (V0.*) |
| `pre-execution-gate.md` | Quality veto conditions (V1.*) |
| `post-execution-gate.md` | Output veto conditions (V2.*) |
| `haiku-prompt-checklist.md` | ALWAYS/NEVER rules for Haiku prompts |
| `dispatch-health-score.md` | 12-point run health score |
| `batch-discovery-gate.md` | Batch Phase 0: story discovery validation (VB0.*) |
| `batch-prioritization-gate.md` | Batch Phase 1: prioritization + cost confirmation (VB1.*) |
| `batch-dispatch-gate.md` | Batch Phase 2: circuit breaker + cost control (VB2.*) |

---

## Templates

| Template | Purpose |
|----------|---------|
| `execution-plan-tmpl.yaml` | Plan output structure |
| `wave-manifest-tmpl.yaml` | Wave definition |
| `task-prompt-tmpl.md` | Enriched prompt for subagent |
| `execution-report-tmpl.md` | Post-execution report |
| `cost-report-tmpl.md` | Cost breakdown |
| `dispatch-state-tmpl.json` | Initial state structure |

---

## Scripts (CODE > LLM)

| Script | Purpose |
|--------|---------|
| `wave-optimizer.py` | DAG topological sort (Kahn's algorithm) |
| `build-command-registry.py` | Scan all squads → command-registry.yaml |
| `cost-tracker.py` | Track actual costs per run |
| `validate-dispatch-gate.sh` | Veto condition checker |
| `validate-wave-results.py` | Post-execution verification |
| `enrich-task.py` | KB injection (template fill) |
| `dispatch-health-score.py` | Calculate 12-point health score |

### Optimization Scripts (v1.1 — CODE > LLM)

| Script | Purpose | Replaces |
|--------|---------|----------|
| `route-tasks.py` | Full routing pipeline orchestrator | 60% of task-router LLM |
| `select-model.py` | Q1-Q4 model decision tree | LLM model selection |
| `assign-enrichment.py` | MINIMAL/STANDARD/FULL assignment | LLM enrichment logic |
| `assign-timeout.py` | Timeout + max_turns assignment | LLM timeout logic |
| `batch-size-optimizer.py` | Reinertsen U-curve batch sizing | LLM batch decisions |
| `critical-chain-analyzer.py` | Goldratt critical chain + slack | LLM critical path |
| `estimate-batch-cost.py` | Per-story + total cost estimation | LLM cost calculation |
| `validate-haiku-prompt.py` | 14-rule ALWAYS/NEVER validation | Manual checklist |

### Hooks Scripts

| Script | Hook Event | Purpose |
|--------|-----------|---------|
| `log-task-start.py` | SubagentStart | Track wave progress |
| `check-wave-complete.py` | SubagentStop | Trigger next wave |
| `save-dispatch-state.py` | PreCompact | Auto-save before compaction |
| `reload-dispatch-context.py` | SessionStart(compact) | Re-inject context |
| `log-task-failure.py` | PostToolUseFailure | Log + retry logic |

---

## Data Files

| File | Purpose |
|------|---------|
| `domain-registry.yaml` | Domain → Agent → KB mapping (extensible) |
| `model-selection-rules.yaml` | When Haiku vs Sonnet vs Opus |
| `veto-conditions.yaml` | All blocking conditions (V0.*, V1.*, V2.*) |
| `enrichment-rules.yaml` | MINIMAL/STANDARD/FULL definitions |
| `timeout-rules.yaml` | Per-task, per-wave, per-run timeouts |
| `haiku-patterns.yaml` | 6 validated prompt patterns |
| `dispatch-heuristics.yaml` | Gate classification, self-healing, health score |
| `dispatch-kb.md` | Consolidated knowledge base |

---

## Quick Start

```bash
# Dispatch from story (PREFERRED)
*new plan/stories/story-feature.md

# Dry run — see plan without executing
*analyze plan/stories/story-feature.md

# Quick cost estimate
*estimate plan/stories/story-feature.md

# Resume interrupted dispatch
*resume

# Check dispatch health
*health
```

---

## Pipeline Phases

```
Phase 0: SUFFICIENCY GATE ──────── Is input well-defined?
Phase 1: DECOMPOSITION ─────────── Story → atomic tasks
Phase 2: ROUTING ────────────────── Task → agent + model
Phase 3: WAVE OPTIMIZATION ──────── DAG → parallel waves
Phase 4: ENRICHMENT ─────────────── Inject KB context
Phase 4.5: PRE-EXECUTION GATE ──── Veto conditions (V1.*)
Phase 5: EXECUTION ──────────────── Parallel subagents
Phase 5.5: POST-EXECUTION GATE ─── Verify outputs (V2.*)
Phase 6: REPORTING ──────────────── Report + cost + state
```

---

## Pack Structure

```
squads/dispatch/
├── config.yaml
├── README.md
├── agents/
│   ├── dispatch-chief.md          # Orchestrator (Gene Kim)
│   ├── quality-gate.md            # Tier 0 (Deming + PV)
│   ├── wave-planner.md            # Tier 1 (Reinertsen + Goldratt)
│   └── task-router.md             # Tier 2 (Registry-based)
├── tasks/
│   ├── plan-execution.md
│   ├── decompose-to-waves.md
│   ├── route-tasks.md
│   ├── execute-wave.md
│   ├── verify-wave.md
│   ├── report-execution.md
│   └── convert-input.md
├── workflows/
│   ├── wf-dispatch-main.yaml
│   ├── wf-dispatch-free.yaml
│   └── wf-dispatch-batch.yaml
├── checklists/
│   ├── pre-dispatch-gate.md
│   ├── pre-execution-gate.md
│   ├── post-execution-gate.md
│   ├── haiku-prompt-checklist.md
│   └── dispatch-health-score.md
├── data/
│   ├── domain-registry.yaml
│   ├── model-selection-rules.yaml
│   ├── veto-conditions.yaml
│   ├── dispatch-heuristics.yaml
│   ├── haiku-patterns.yaml
│   ├── enrichment-rules.yaml
│   ├── timeout-rules.yaml
│   └── dispatch-kb.md
├── templates/
│   ├── execution-plan-tmpl.yaml
│   ├── wave-manifest-tmpl.yaml
│   ├── task-prompt-tmpl.md
│   ├── execution-report-tmpl.md
│   ├── cost-report-tmpl.md
│   └── dispatch-state-tmpl.json
├── scripts/
│   ├── wave-optimizer.py
│   ├── build-command-registry.py
│   ├── cost-tracker.py
│   ├── validate-dispatch-gate.sh
│   ├── validate-wave-results.py
│   ├── enrich-task.py
│   ├── dispatch-health-score.py
│   ├── log-task-start.py
│   ├── check-wave-complete.py
│   ├── save-dispatch-state.py
│   ├── reload-dispatch-context.py
│   └── log-task-failure.py
├── lib/
│   ├── __init__.py
│   ├── pipeline_state.py
│   ├── progress.py
│   └── event_log.py
└── docs/
    ├── ARCHITECTURE.md
    └── MIGRATION.md
```

---

## Cost Economy (2026)

| Model | Input/MTok | Output/MTok | Cache Read |
|-------|-----------|------------|------------|
| Haiku 4.5 | $1.00 | $5.00 | $0.10 |
| Sonnet 4.5 | $3.00 | $15.00 | $0.30 |
| Opus 4.6 | $5.00 | $25.00 | $0.50 |

**Main context (50k tokens):** ~$0.30/interaction
**Haiku subagent (2k tokens):** ~$0.007/task = **43x cheaper**
**Haiku with cache:** ~$0.005/task = **58x cheaper**

---

## Integration

- **Source:** Self-contained in `squads/dispatch/` (legacy `.aios-core/` dispatcher files have been removed)
- **Auto-discovery:** `*discover` scans ecosystem and rebuilds registries automatically
- **Backward compat:** `wf-dispatch-free.yaml` supports legacy free-text input

---

*Dispatch Squad v1.0.0 — AIOS Framework*
