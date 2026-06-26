# Task: Delete Claude Code Mastery Squad

**Task ID:** CCM-LIFECYCLE-002
**Version:** 1.0.0
**Command:** `*delete-squad`
**Orchestrator:** Orion (claude-mastery-chief)
**Purpose:** Safely remove the Claude Code Mastery squad from the workspace, including all agents, tasks, data, and configuration. Optionally archive before deletion.

## Contrato SINKRA

task: delete-claude-code-mastery
atomic_layer: Atom
executor: claude-mastery-chief
Domain: Operational
accountability_token: TK-CCM-ACC-001
Input:
- contexto do projeto
- objetivo da task
- artefatos de referência
Output:
- delete-claude-code-mastery-report
- recomendação executável
output_schema: deletion-confirmation
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
- All squad files removed from target project
- Registry updated to reflect removal
- IDE sync clean with 0 orphan references

---


## Overview

```
  Deletion Request
       |
       v
  +-------------------+
  | 1. Confirm Intent |
  |    (require "yes") |
  +-------------------+
       |
       v
  +-------------------+
  | 2. List           |
  |    Dependencies    |
  +-------------------+
       |
       v
  +-------------------+
  | 3. Archive        |
  |    (if requested)  |
  +-------------------+
       |
       v
  +-------------------+
  | 4. Remove Files   |
  +-------------------+
       |
       v
  +-------------------+
  | 5. Update Registry|
  |    & Report        |
  +-------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| confirmation | string | User prompt | Yes | Must be exactly "yes" or "confirm" to proceed |
| archive | boolean | User prompt | No | If true, create archive before deletion (default: true) |
| archive_path | string | User prompt | No | Custom archive location (default: `.aiox/archives/`) |

---

## Preconditions

- Claude Code Mastery squad exists at `squads/claude-code-mastery/`
- User has write access to the squad directory and parent directories
- No active sessions are using squad agents (warn if detected)

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| deletion_report | object | Summary of files removed, archive location, registry updates |
| archive_path | string | Path to archive file if archiving was enabled |
| files_removed | list | Complete list of deleted files and directories |
| registry_updates | list | Configuration files updated to remove squad references |

---

## Execution Phases

### Phase 1: Confirm Intent

1. Display warning:
   ```
   WARNING: This will permanently delete the Claude Code Mastery squad.

   This includes:
   - 8 agent definitions (claude-mastery-chief, hooks-architect, mcp-integrator,
     swarm-orchestrator, config-engineer, skill-craftsman, project-integrator,
     roadmap-sentinel)
   - All task definitions (26 tasks)
   - All templates, checklists, data files, and workflows
   - config.yaml, CHANGELOG.md, README.md, ARCHITECTURE.md

   Type "yes" to confirm deletion.
   ```
2. Wait for explicit user confirmation
3. If confirmation is not "yes" or "confirm", HALT with message: "Deletion cancelled."

### Phase 2: List Dependencies

1. Scan the workspace for references to this squad:
   - Search for `claude-code-mastery` in all YAML, JSON, and markdown files outside the squad directory
   - Check `.aiox/active-workflow.json` for active squad references
   - Check `docs/stories/` for stories referencing CCM agents
   - Check `.claude/settings.json` for any agent or skill references
2. Report all found dependencies:
   ```
   Dependencies found:
   - .aiox/active-workflow.json references claude-mastery-chief
   - a legacy storybook story mentions @claude-code-mastery:hooks-architect
   ```
3. If critical dependencies found (active workflow), warn user and request re-confirmation
4. Non-critical dependencies (documentation references) are noted but do not block deletion

### Phase 3: Archive (if requested)

1. If `archive` is true (default):
   - Create archive directory: `{archive_path}/claude-code-mastery-{date}/`
   - Copy the entire `squads/claude-code-mastery/` directory to archive
   - Generate a manifest file listing all archived files with sizes
   - Verify archive integrity (file count matches source)
2. Report archive location and size
3. If archive fails, HALT and report error. Do not proceed to deletion.

### Phase 4: Remove Files

1. Delete the following in order:
   - `squads/claude-code-mastery/agents/` (all agent markdown files)
   - `squads/claude-code-mastery/tasks/` (all task files)
   - `squads/claude-code-mastery/templates/` (all template files)
   - `squads/claude-code-mastery/checklists/` (all checklist files)
   - `squads/claude-code-mastery/data/` (all data files)
   - `squads/claude-code-mastery/workflows/` (all workflow files)
   - `squads/claude-code-mastery/scripts/` (all script files)
   - `squads/claude-code-mastery/config.yaml`
   - `squads/claude-code-mastery/CHANGELOG.md`
   - `squads/claude-code-mastery/README.md`
   - `squads/claude-code-mastery/ARCHITECTURE.md`
   - `squads/claude-code-mastery/` (empty directory)
2. Track each deletion for the report

### Phase 5: Update Registry and Report

1. Check if any workspace-level registry references the squad:
   - If `workspace/domains/` has a domain entry, remove or mark as deleted
   - If `.aiox-core/data/entity-registry.yaml` has entries, remove squad entities
2. Generate deletion report:
   ```
   Deletion Report: Claude Code Mastery Squad
   ──────────────────────────────────────────
   Archive:     .aiox/archives/claude-code-mastery-2026-03-06/
   Files removed: 52
   Directories removed: 9
   Registry updates: 2 files cleaned

   Status: COMPLETE
   ```
3. Display the report to the user

---

## Postconditions

- `squads/claude-code-mastery/` directory no longer exists
- No orphaned references to CCM agents in workspace configuration files
- Archive exists at specified path (if archiving was enabled)
- Deletion report is displayed to the user

---

## Error Handling

| Error | Recovery |
|-------|----------|
| User does not confirm | Abort immediately with "Deletion cancelled." |
| Archive creation fails | HALT, report error, do not proceed to deletion |
| File deletion fails (permission) | Report specific file, skip it, continue with others, note in report |
| Active workflow references squad | Warn user, require second confirmation, note in report |
| Registry update fails | Report error, note manual cleanup needed |

---

## Rollback

If deletion was preceded by archiving, restoration is possible:
1. Copy archive directory back to `squads/claude-code-mastery/`
2. Re-register squad in any workspace registries that were updated
3. Verify `config.yaml` is valid after restoration

---

*Task: delete-claude-code-mastery v1.0.0*
