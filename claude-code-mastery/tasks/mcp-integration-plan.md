# Task: Plan MCP Server Integration

**Task ID:** CCM-PI-005
**Version:** 1.1.0
**Command:** `*mcp-integration-plan`
**Owner:** Conduit (project-integrator)
**Purpose:** Plan MCP server integration for a project by analyzing needs, mapping capabilities to available servers, estimating context budget impact, and prioritizing by ROI under the current Claude Code MCP ownership and policy model.

## Contrato SINKRA

task: mcp-integration-plan
atomic_layer: Atom
executor: mcp-integrator
Domain: Tactical
accountability_token: TK-CCM-ACC-001
Input:
- contexto do projeto
- objetivo da task
- artefatos de referência
Output:
- mcp-integration-plan-report
- recomendação executável
output_schema: mcp-integration-report-yaml
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
- Executor único definido
- Inputs e outputs explícitos
- Critério final verificável no artefato entregue

---


## Overview

```
  Project Analysis
       |
       v
  +---------------------+
  | 1. Analyze Project   |
  |    Needs             |
  +---------------------+
       |
       v
  +---------------------+
  | 2. Map Capabilities  |
  |    to Available MCPs |
  +---------------------+
       |
       v
  +---------------------+
  | 3. Estimate Context  |
  |    Budget Impact     |
  +---------------------+
       |
       v
  +---------------------+
  | 4. Prioritize by ROI |
  +---------------------+
       |
       v
  +---------------------+
  | 5. Create Integration|
  |    Plan              |
  +---------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| project_path | string | User or cwd | Yes | Valid project directory |
| budget | enum | User | No | `minimal` (1-2 MCPs), `standard` (3-5), `full` (no limit) |
| priorities | string[] | User | No | e.g., ["documentation", "web search", "database", "browser testing"] |

---

## Preconditions

- Project directory accessible for analysis
- Understanding of available MCP ecosystem (official + community)
- Awareness of current MCP config surfaces (`.mcp.json`, settings layers, `managed-mcp.json`) and who owns them

---

## Execution Phases

### Phase 1: Analyze Project Needs

Examine the project to identify where MCP servers would add value:

1. **Technology stack**: what frameworks, languages, databases are used
2. **External dependencies**: APIs consumed, services integrated
3. **Development workflow**: what tasks developers repeat frequently
4. **Documentation needs**: which libraries lack good inline docs
5. **Testing needs**: browser testing, API testing, E2E scenarios
6. **Data needs**: web search, scraping, research tasks

Produce a needs matrix:

| Need Category | Specific Need | Frequency | Current Solution |
|---------------|---------------|-----------|-----------------|
| Documentation | React docs lookup | Daily | Manual browser search |
| Database | Query execution | Hourly | Copy-paste to psql |
| Search | Find code examples | Daily | Manual Google search |

### Phase 2: Map Capabilities to Available MCPs

Match identified needs to available MCP servers:

**Official/Stable MCPs:**
| MCP Server | Capabilities | Transport | Best For | Typical Surface |
|------------|-------------|-----------|----------|-----------------|
| context7 | Library documentation | stdio | Framework/library docs | `.mcp.json` or managed |
| playwright | Browser automation | stdio | Web testing, screenshots | `.mcp.json` or managed |
| postgres/supabase | Database queries | stdio | DB operations | `.mcp.json` |
| filesystem | File operations | stdio | Cross-directory access | Managed or user-owned |

**Community MCPs:**
| MCP Server | Capabilities | Maturity | Best For | Typical Surface |
|------------|-------------|----------|----------|-----------------|
| exa | Web search | Stable | Research, finding examples | User-owned or `.mcp.json` |
| apify | Web scraping | Stable | Data extraction | `.mcp.json` |
| github | GitHub API | Stable | Issue/PR management | User-owned or managed |
| linear/jira | Project management | Varies | Task tracking | Managed or user-owned |

For each need, list candidate MCPs with fit score (1-5), preferred config surface, and likely owner (manual, plugin, enterprise).

### Phase 3: Estimate Context Budget Impact

Each MCP server has a context cost. Estimate:

1. **Tool registration cost**: number of tools exposed, description token count
2. **Per-call cost**: average input/output size of tool calls
3. **Startup latency**: time to initialize the server
4. **Memory footprint**: resources consumed while running

Calculate context budget:
```
Total context overhead = sum(tools_per_mcp * avg_description_tokens)
% of 200K context window used by MCP registrations
```

**Budget guidelines:**
| Budget Level | Max MCP Overhead | Max Servers |
|-------------|-----------------|-------------|
| Minimal | < 2% context window | 1-2 servers |
| Standard | < 5% context window | 3-5 servers |
| Full | < 10% context window | No hard limit |

Flag any MCP that registers more than 20 tools (context-heavy).

### Phase 4: Prioritize by ROI

Before scoring, enforce the runtime ownership constraints:

1. Prefer manual `.mcp.json` when the team owns the server definition
2. Treat `managed-mcp.json` as exclusive when present
3. Manual definitions suppress duplicate plugin servers; between plugins, first-loaded wins
4. Never place credentials directly in repo-tracked `.mcp.json`

Score each candidate MCP:

```
ROI = (frequency_of_need * time_saved_per_use) / (context_cost + setup_effort)
```

Where:
- **frequency_of_need**: daily=5, weekly=3, monthly=1
- **time_saved_per_use**: minutes saved vs manual approach
- **context_cost**: token overhead (normalized 1-5)
- **setup_effort**: configuration difficulty (1=trivial, 5=complex)

Rank all candidates by ROI score descending.

### Phase 5: Create Integration Plan

Produce the final plan with phased rollout:

**Phase A (Day 1)**: highest ROI MCPs, zero or minimal configuration
**Phase B (Week 1)**: medium ROI MCPs, moderate setup required
**Phase C (As needed)**: lower ROI MCPs, add when specific need arises

For each MCP in the plan:
1. Recommended config surface (`.mcp.json`, `~/.claude/settings.json`, or `managed-mcp.json`)
2. Ownership model (manual, plugin, enterprise)
3. Required environment variables or credentials
4. Verification command to test connectivity
5. Expected context budget impact
6. Precedence or policy notes

---

## Output Format

```markdown
## MCP Integration Plan

**Project:** {project_path}
**Budget:** {budget_level}
**Date:** {YYYY-MM-DD}

### Needs Analysis

| Need | Frequency | Matched MCP | ROI Score |
|------|-----------|-------------|-----------|
| {need} | {freq} | {mcp} | {score} |

### Context Budget

| MCP Server | Tools | Est. Tokens | % Window |
|------------|-------|-------------|----------|
| {mcp} | {N} | {N} | {N}% |
| **Total** | | | {N}% |

### Ownership and Policy

| MCP Server | Surface | Owner | Policy Notes |
|------------|---------|-------|--------------|
| {mcp} | {.mcp.json|managed-mcp.json|user settings} | {manual|plugin|enterprise} | {notes} |

### Rollout Plan

#### Phase A: Immediate (Day 1)
1. **{mcp_name}**: {reason}
   - ROI: {score}
   - Surface: {surface}
   - Owner: {owner}
   - Config:
     ```json
     { "mcpServers": { "{name}": { ... } } }
     ```
   - Verify: {command}
   - Policy: {policy_note}

#### Phase B: Short-term (Week 1)
1. **{mcp_name}**: {reason}

#### Phase C: On-demand
1. **{mcp_name}**: {reason}

### Excluded MCPs

| MCP | Reason for Exclusion |
|-----|---------------------|
| {mcp} | {reason} |
```

---

## Veto Conditions

- **NEVER** recommend MCPs that require credentials the user has not agreed to provide
- **NEVER** exceed the stated budget level without explicit user approval
- **NEVER** recommend experimental or abandoned MCPs without flagging maturity risk
- **NEVER** recommend manual MCP writes when `managed-mcp.json` has exclusive control
- **NEVER** put secrets directly into repo-tracked `.mcp.json`
- **NEVER** ignore manual-vs-plugin precedence when duplicate servers are likely
- **NEVER** install or configure MCPs in this task -- this task produces a plan only

---

## Completion Criteria

- [ ] Project needs analyzed with frequency assessment
- [ ] Available MCPs mapped to identified needs
- [ ] Context budget estimated for each candidate
- [ ] ROI scores calculated and ranked
- [ ] Phased integration plan created with configuration snippets
- [ ] Budget compliance verified
- [ ] Plan delivered in standard format
