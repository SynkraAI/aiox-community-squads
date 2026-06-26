# Task: Update Claude Code Mastery Squad

**Task ID:** CCM-LIFECYCLE-001
**Version:** 1.0.0
**Command:** `*update-squad`
**Orchestrator:** Orion (claude-mastery-chief)
**Purpose:** Update the Claude Code Mastery squad by adding agents, refreshing knowledge, modifying configuration, or applying structural changes.

## Contrato SINKRA

task: update-claude-code-mastery
atomic_layer: Atom
executor: roadmap-sentinel
Domain: Strategic
accountability_token: TK-CCM-ACC-001
Input:
- changelog Anthropic
- docs oficiais
- estado atual do squad
Output:
- roadmap-delta-report
- knowledge-update-report
output_schema: update-report-yaml
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
  Update Request
       |
       v
  +-------------------+
  | 1. Identify       |
  |    Changes Needed  |
  +-------------------+
       |
       v
  +-------------------+
  | 2. Apply Updates  |
  |    (agents, config,|
  |     tasks, data)   |
  +-------------------+
       |
       v
  +-------------------+
  | 3. Validate Config|
  |    (YAML, refs)    |
  +-------------------+
       |
       v
  +-------------------+
  | 4. Run Smoke Tests|
  |    (3 per agent)   |
  +-------------------+
       |
       v
  +-------------------+
  | 5. Update         |
  |    CHANGELOG.md    |
  +-------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| update_request | string | User prompt | Yes | Description of what to update (add agent, refresh knowledge, modify config, etc.) |
| scope | enum | User or inferred | No | `agent`, `config`, `task`, `data`, `runtime-contract`, `validator`, `memory-context`, `p0`, `all` |
| target_agent | string | User prompt | No | Agent ID if updating a specific agent |
| dry_run | boolean | User prompt | No | If true, show planned changes without applying |

---

## Preconditions

- Claude Code Mastery squad directory exists at `squads/claude-code-mastery/`
- `config.yaml` is valid and all agents are registered
- User has write access to the squad directory

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| updated_artifacts | list | Files that were created, modified, or removed |
| validation_result | object | Config validation pass/fail with details |
| smoke_test_results | list | Results of smoke test queries per agent |
| changelog_entry | string | Entry added to CHANGELOG.md |

---

## Execution Phases

### Phase 1: Identify Changes Needed

1. Parse the update request to determine scope:
   - **Add specialist:** New agent definition needed (file + config.yaml registration)
   - **Refresh knowledge:** Update data files, knowledge base sections in agents
   - **Modify config:** Update config.yaml settings, tiers, handoffs
   - **Update task:** Modify or add task definitions
   - **Runtime contract:** Synchronize squad references with extracted Claude Code runtime contract
   - **Validator:** Rebuild audit/setup validator against runtime-aware checks
   - **Memory/context:** Align CLAUDE.md, MEMORY.md and context tasks with runtime limits
   - **Update voice/thinking DNA:** Modify agent personality or decision framework
2. List all files that will be affected
3. If `dry_run` is true, present the plan and HALT for approval

**P0 Runtime Alignment Wave**

When the request references `P0`, execute in this order:

1. `*refresh-runtime-contract` via `roadmap-sentinel`
2. `*rebuild-validator` via `config-engineer`
3. `*align-memory-context` via `skill-craftsman`

If a later step depends on unresolved drift from an earlier step, HALT and emit handoff instead of proceeding with stale assumptions.

### Phase 2: Apply Updates

Depending on scope:

**Adding a specialist:**
1. Create agent markdown file in `agents/` following the existing pattern
2. Add specialist entry to `config.yaml` under appropriate tier
3. Update handoff matrix in `config.yaml`
4. Update `ARCHITECTURE.md` with new agent in tier diagram and handoff matrix
5. Ensure voice_dna and thinking_dna sections are present (quality_standards requirement)

**Refreshing knowledge:**
1. Identify outdated data in `data/` directory
2. Update agent knowledge_base sections with current information
3. Verify external references (URLs, version numbers) are current

**Running the P0 runtime wave:**
1. Load decoded runtime artifacts from `outputs/decoded/claude-code-main/`
2. Apply `refresh-runtime-contract` to eliminate terminology drift
3. Apply `rebuild-runtime-validator` to convert checklist validation into contract validation
4. Apply `align-memory-context` to synchronize context guidance and memory doctrine
5. Emit explicit handoff order if any executor is blocked

**Modifying configuration:**
1. Edit `config.yaml` with requested changes
2. Validate YAML syntax after changes
3. Verify all cross-references (agent IDs, handoff targets) are valid

**Updating tasks:**
1. Create or modify task file in `tasks/` directory
2. Follow the 8-field pattern: Task ID, Version, Command, Orchestrator, Purpose, Inputs, Outputs, Phases
3. Link task to appropriate agent via dependencies

### Phase 3: Validate Configuration

1. Parse `config.yaml` and verify:
   - All agent IDs referenced in tiers exist as files in `agents/`
   - All handoff targets reference valid agent IDs
   - No orphaned agents (registered in config but no file, or file exists but not registered)
   - Quality standards fields are present (voice_dna_required, thinking_dna_required, min_score)
2. For each modified agent file, verify:
   - YAML block is syntactically valid
   - Required fields present: agent.name, agent.id, agent.title, persona, commands
   - voice_dna section exists (if voice_dna_required is true)
   - thinking_dna section exists (if thinking_dna_required is true, except orchestrator)
3. Report validation result with pass/fail per check

### Phase 4: Run Smoke Tests

For each modified or new agent, run 3 smoke test queries:
1. A basic greeting activation test (verify agent responds in character)
2. A domain-specific question (verify specialist knowledge is accurate)
3. A handoff trigger test (verify routing to collaborating agents works)

Report results as pass/fail per test per agent.

### Phase 5: Update CHANGELOG

1. Read current `CHANGELOG.md`
2. Add new entry at the top with:
   - Date
   - Version bump (patch for fixes, minor for additions, major for breaking changes)
   - Summary of changes
   - List of affected files
3. Write updated `CHANGELOG.md`

---

## Postconditions

- All modified files are syntactically valid
- `config.yaml` references are consistent
- Smoke tests pass for all modified agents
- CHANGELOG.md reflects the update

---

## Error Handling

| Error | Recovery |
|-------|----------|
| YAML parse error in agent file | Show exact line, suggest fix, do not proceed |
| Missing agent file referenced in config | Create stub or remove reference |
| Smoke test failure | Report failing query, suggest agent fix, do not mark as complete |
| Handoff target not found | List valid targets, prompt user to select |

---

*Task: update-claude-code-mastery v1.0.0*
