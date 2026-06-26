# Task: Optimize Claude Code Workflow

**Task ID:** CCM-PI-003
**Version:** 1.1.0
**Command:** `*optimize-workflow`
**Owner:** Conduit (project-integrator)
**Purpose:** Optimize Claude Code workflow for maximum productivity by analyzing usage patterns, identifying bottlenecks, and configuring permissions, context, shortcuts, and automation against the current runtime contract.

## Contrato SINKRA

task: optimize-workflow
atomic_layer: Atom
executor: swarm-orchestrator
Domain: Tactical
accountability_token: TK-CCM-ACC-001
Input:
- contexto do projeto
- objetivo da task
- artefatos de referência
Output:
- optimize-workflow-report
- recomendação executável
output_schema: workflow-optimization-yaml
Pre-Conditions:
- Contexto do projeto disponível e legível
- Artefatos de referência acessíveis ao executor
- Critério de sucesso entendido antes da execução
Post-Conditions:
- Output publicado em formato auditável
- Próximo passo explícito ou handoff emitido
- Decisões relevantes registradas no artefato final
Performance:
- Execução em uma sessão sem falha silenciosa
- Thresholds e veto conditions respeitados
- Resultado acionável para o próximo executor
Completion Criteria:
- Workflow bottleneck identified with impact assessment
- Improvement applied and re-measured
- Before/after comparison documented

---


## Overview

```
  Current Setup
       |
       v
  +---------------------+
  | 1. Analyze Usage     |
  |    Patterns          |
  +---------------------+
       |
       v
  +---------------------+
  | 2. Identify          |
  |    Bottlenecks       |
  +---------------------+
       |
       v
  +---------------------+
  | 3. Optimize          |
  |    Permissions       |
  +---------------------+
       |
       v
  +---------------------+
  | 4. Set Up Keyboard   |
  |    Shortcuts         |
  +---------------------+
       |
       v
  +---------------------+
  | 5. Configure         |
  |    Auto-Memory       |
  +---------------------+
       |
       v
  +---------------------+
  | 6. Generate          |
  |    Optimization Plan |
  +---------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| project_path | string | User or cwd | Yes | Must contain .claude/ directory |
| pain_points | string[] | User | No | Described bottlenecks (e.g., "too many permission prompts") |
| workflow_type | enum | User | No | `solo-dev`, `team-review`, `ci-cd`, `exploratory` |

---

## Preconditions

- Claude Code integration exists (.claude/ directory present)
- User has used Claude Code on this project at least once

---

## Execution Phases

### Phase 1: Analyze Usage Patterns

Examine current configuration to infer usage patterns:

0. **Session usage baseline**: run `scripts/session-usage-report.py` for the target project or workspace and ingest:
   - `summary` for macro signals (errors, branches, task-agent adoption, research profile)
   - `facets` + `narrative` for dominant workflow patterns
   - `recommendations.global` + `recommendations.by_project` as the first-pass optimization backlog
1. **CLAUDE.md analysis**: what instructions are present, what is missing
2. **settings.json review**: current allow/deny rules, how restrictive
3. **Rules inventory**: how many rules, what domains they cover
4. **Hook presence**: what automation exists
5. **Command/skill inventory**: custom commands and skills defined
6. **Project size estimation**: file count, language distribution

Classify the current configuration maturity:
| Level | Description | Typical Signs |
|-------|-------------|---------------|
| Starter | Minimal setup | Only CLAUDE.md, no rules, no hooks |
| Intermediate | Functional | CLAUDE.md + settings + some rules |
| Advanced | Optimized | Full rules, hooks, skills, MCP configured |
| Expert | Fully automated | CI/CD integration, custom hooks, agent teams |

### Phase 2: Identify Bottlenecks

Check for common productivity killers:

1. **Permission prompts**: overly restrictive settings forcing repeated approvals
   - Look for missing allow rules for common commands (npm, git, build tools)
   - Check if `Bash` tool has no allows (causes prompt on every command)
2. **Slow tool execution**: MCP servers with high latency, missing caching
3. **Context bloat**: CLAUDE.md over 150 lines, too many always-loaded rules
4. **Missing automation**: repetitive tasks that could be hooks or skills
5. **Context rot**: long sessions without compaction strategy
6. **Redundant instructions**: duplicated guidance between CLAUDE.md and rules
7. **Foreground blocking loops**: `sleep`/polling patterns that should move to `run_in_background` or `Monitor`
8. **MCP ownership drift**: project servers scattered across settings instead of `.mcp.json` / managed policy

For each bottleneck found, estimate impact: HIGH, MEDIUM, LOW.

### Phase 3: Optimize Permission Strategy

Design a permission strategy that balances safety and speed:

1. **Safe allows** (add to settings.json allow list):
   - Build commands: `npm run build`, `npm run dev`, `npm test`
   - Lint commands: `npm run lint`, `npm run typecheck`
   - Git read commands: `git status`, `git diff`, `git log`
   - Language servers and formatters
2. **Smart denies** (keep or add to deny list):
   - Destructive commands: `rm -rf`, `DROP`, `git push --force`
   - Production access: database URLs, deployment commands
   - Sensitive paths: `.env`, credentials, secrets
3. **Contextual permissions**: use path-based rules for directory-specific allows

Present before/after comparison of expected permission prompts.

### Phase 4: Audit Keyboard Shortcuts Capability

Recommend keyboard shortcut configuration only if the runtime capability is actually available:

1. Check whether `~/.claude/keybindings.json` customization is available in this environment.
2. If available:
   - Validate format `{ "bindings": [ ... ] }`
   - Restrict contexts to `Global`, `Chat`, `Autocomplete`, `Confirmation`, `Help`
   - Avoid reserved terminal/platform shortcuts
3. If not available:
   - Do NOT prescribe Claude Code keybinding customization as a fix
   - Prefer command aliases, hooks, rules, and workflow restructuring instead

Do not substitute VS Code keybindings as if they were Claude Code runtime configuration.

### Phase 5: Configure Auto-Memory

Set up persistent memory for cross-session efficiency:

1. **Agent memory**: create `.claude/agent-memory/` structure
   - `MEMORY.md` only as a compact index of persistent patterns
   - Topic files for distilled domain knowledge when justified
2. **Memory hygiene rules**:
   - What to save: confirmed patterns, user preferences, debugging solutions
   - What NOT to save: session-specific state, speculative conclusions, derivable project state
   - Size limits: `MEMORY.md` under 200 lines and 25 KB
   - In assistant/KAIROS flows, new entries go to append-only daily logs before distillation
3. **Memory templates**: pre-populate with project conventions if detectable

### Phase 6: Generate Optimization Plan

Produce a prioritized optimization plan:

1. Start from `session-usage-report.recommendations` when available, then refine with local config findings
2. Sort all recommendations by impact (HIGH first)
3. Group by effort: Quick Wins (< 5 min), Medium (5-30 min), Investment (30+ min)
4. For each recommendation, provide exact implementation steps
5. Estimate total time saved per week after optimization

---

## Output Format

```markdown
## Workflow Optimization Report

**Project:** {project_path}
**Current Maturity:** {level}
**Estimated Improvement:** {X}% fewer interruptions

### Bottlenecks Found

| Bottleneck | Impact | Fix Effort |
|------------|--------|------------|
| {description} | HIGH/MED/LOW | Quick/Medium/Investment |

### Quick Wins (Apply Now)

1. **{title}**: {description}
   ```json
   // Exact config change
   ```

### Medium Effort

1. **{title}**: {description}
   - Step 1: ...
   - Step 2: ...

### Investment Items

1. **{title}**: {description}
   - Estimated time: {X} minutes
   - Expected benefit: {description}

### Permission Optimization

**Before:** {N} expected prompts per session
**After:** {M} expected prompts per session
**Reduction:** {X}%

### Session Report Inputs Used

- Summary signals: {session_report_summary_keys}
- Facets used: {session_report_facet_keys}
- Imported recommendations: {session_report_recommendation_ids}
```

---

## Veto Conditions

- **NEVER** add allow rules for destructive operations to reduce prompts
- **NEVER** disable security hooks for convenience
- **NEVER** remove deny rules without explaining the security tradeoff
- **NEVER** make changes without presenting the plan first -- this task produces a plan, user applies it

---

## Completion Criteria

- [ ] Usage patterns analyzed and maturity level classified
- [ ] Bottlenecks identified with impact assessment
- [ ] Permission strategy designed with before/after comparison
- [ ] Keyboard shortcuts recommended for workflow type
- [ ] Memory configuration suggested
- [ ] Prioritized optimization plan delivered
