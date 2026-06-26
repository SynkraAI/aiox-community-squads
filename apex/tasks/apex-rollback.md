# apex-rollback

> Rollback pipeline to a previous checkpoint, restoring code and state.

## Metadata

```yaml
task_id: apex-rollback
command: "*apex-rollback"
agent: apex-lead
category: pipeline-control
requires: [active pipeline OR completed pipeline with state file]
```

## Purpose

When a pipeline phase produces unwanted results (code the user rejects, design direction change, etc.), `*apex-rollback` reverts to the state at a previous checkpoint — both the pipeline state file AND the code changes.

## STRICT RULES

- NEVER rollback without user confirmation
- NEVER delete pipeline state — create a new state entry with `rolled_back_from` metadata
- ALWAYS preserve the current branch as a backup before rollback
- ONLY rollback to checkpoints that were COMPLETED (status: completed)
- Code rollback uses `git stash` + `git checkout` — NEVER `git reset --hard`

## Workflow

### Step 1: Load Pipeline State

```yaml
action: Read pipeline state from .aios/apex-pipeline/{pipeline-id}.yaml
validate: Verify state_checksum integrity (GAP-02 fix)
on_invalid: "State file corrupted. Cannot rollback safely. Options: (1) start new pipeline, (2) manual recovery"
```

### Step 2: Show Rollback Options

Present completed checkpoints with their timestamps and decisions:

```
Pipeline: {pipeline_id}
Current phase: {current_phase} ({status})

Available rollback points:
  1. CP-01 (Feature Brief) — completed {date} — "{decision}"
  2. CP-02 (Design Review) — completed {date} — "{decision}"
  3. CP-03 (Architecture) — completed {date} — "{decision}"

Which checkpoint to rollback to? (1/2/3 or "cancel")
```

### Step 3: Backup Current State

```yaml
actions:
  - "git stash push -m 'apex-rollback-backup-{pipeline_id}-phase-{current_phase}'"
  - "Copy current pipeline state to .aios/apex-pipeline/{pipeline-id}.rollback-backup.yaml"
```

### Step 4: Restore Code

```yaml
actions:
  - "Identify files modified AFTER the target checkpoint (from pipeline artifacts log)"
  - "git checkout {checkpoint_commit_ref} -- {list of files modified after checkpoint}"
  - "If no commit ref available: restore from git stash history"
fallback: "If no git history available, WARN user that code rollback is partial"
```

### Step 5: Restore Pipeline State

```yaml
actions:
  - "Reset all phases AFTER target checkpoint to 'pending'"
  - "Reset all gates AFTER target checkpoint to 'PENDING'"
  - "Set current_phase to target checkpoint's phase"
  - "Set status to 'paused_at_checkpoint'"
  - "Add rollback entry to escalation_log"
  - "Recompute state_checksum"
  - "Save updated state"
```

### Step 6: Confirm and Resume

```
Rollback complete.
  From: Phase {old_phase} ({old_status})
  To: Phase {target_phase} (CP-{checkpoint})
  Files restored: {count}
  Backup: git stash '{stash_name}'

Pipeline paused at CP-{checkpoint}. Ready to resume.
  1. Resume pipeline from here (*apex-resume)
  2. Review restored state
  3. Abort pipeline entirely (*apex-abort)
```

## Rollback Log Entry

```yaml
escalation_log_entry:
  event_type: rollback
  from_phase: {N}
  to_phase: {N}
  to_checkpoint: "CP-{N}"
  files_restored: [{list}]
  backup_ref: "git stash '{name}'"
  reason: "{user-provided reason}"
  timestamp: "{ISO 8601}"
```

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No pipeline active | "No active pipeline found. Nothing to rollback." |
| Only CP-01 completed | "Cannot rollback further — CP-01 is the starting point." |
| Code has uncommitted changes | "Stash uncommitted changes first, then rollback." |
| Pipeline already completed | "Pipeline completed. Rollback to any checkpoint still available." |
| State file missing | "State file not found. Manual recovery required." |

## Integration

- Updates `pipeline-state-schema.yaml` state file on rollback
- Adds entry to `escalation_log` (MELHORIA-04)
- Preserves `metrics` — rollback time not counted in phase durations
- Works with `*apex-resume` after rollback
