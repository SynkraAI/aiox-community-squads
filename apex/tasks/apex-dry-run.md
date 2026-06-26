# apex-dry-run

> Preview the full pipeline plan WITHOUT executing any changes.

## Metadata

```yaml
task_id: apex-dry-run
command: "*apex-dry-run"
aliases: ["*apex-plan", "*apex-preview"]
agent: apex-lead
category: pipeline-control
modifies_files: false
modifies_git: false
```

## Purpose

Show exactly what `*apex-go` would do — which phases, agents, gates, and checkpoints — without writing a single line of code. Helps the user decide before investing time.

## STRICT RULES

- NEVER modify any file
- NEVER create pipeline state
- NEVER execute any agent task
- ONLY scan project context (read-only) and compute the plan

## Workflow

### Step 1: Scan Project (read-only)

```yaml
action: Run apex-scan silently (cached if available)
output: project_context (framework, styling, components, profile)
```

### Step 2: Classify Request

```yaml
input: User's natural language description
output:
  intent: "{fix|improve|create|redesign|audit}"
  scope: "{micro|small|medium|large|cross-platform}"
  pipeline: "{*apex-fix|*apex-quick|*apex-go}"
  domains: ["{css|react|motion|a11y|perf|...}"]
```

### Step 3: Compute Agent Routing

```yaml
output:
  profile: "{full|web-next|web-spa|minimal}"
  active_agents: ["{agent_ids}"]
  routed_agents: ["{agents that would be activated}"]
  estimated_phases: ["{phases that would run}"]
```

### Step 4: Compute Gate Requirements

```yaml
output:
  gates_applicable: ["{gate_ids with available_check = true}"]
  gates_skipped: ["{gate_ids with available_check = false + reason}"]
  non_waivable: ["{QG-AX-005, QG-AX-010}"]
```

### Step 5: Present Plan

```markdown
# Dry Run — "{description}"

## Pipeline: *apex-go (7 phases)
## Profile: web-spa (8 agents)

| Phase | Agent(s) | Gates | Checkpoint |
|-------|----------|-------|------------|
| 1. Specify | apex-lead | — | CP-01 |
| 2. Design | interaction-dsgn, design-sys-eng | QG-AX-001 (SKIP: no packages/tokens), QG-AX-002, QG-AX-003 | CP-02 |
| 3. Architect | frontend-arch | QG-AX-004 | CP-03 |
| 4. Implement | css-eng, react-eng | QG-AX-005 (ACTIVE), QG-AX-006 (ACTIVE) | — |
| 5. Polish | motion-eng → a11y-eng → perf-eng | QG-AX-005, QG-AX-006, QG-AX-007 | CP-05 |
| 6. QA | qa-visual | QG-AX-008 (SKIP: no Chromatic) | — |
| 7. Ship | apex-lead → @devops | QG-AX-010 (NON-WAIVABLE) | CP-04, CP-06 |

## Summary
- **Agents involved:** 8
- **Active gates:** 6 of 10
- **Skipped gates:** 4 (tooling unavailable)
- **Checkpoints (user decisions):** 6
- **Non-waivable gates:** 2

Ready to execute? Use `*apex-go` to start.
```

## Options

| Flag | Effect |
|------|--------|
| `--verbose` | Show veto conditions per gate |
| `--json` | Output as JSON (for scripting) |
| `--compare {pipeline}` | Show diff between *apex-go and *apex-quick plans |
