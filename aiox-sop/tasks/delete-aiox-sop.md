# Task: Delete SOP Factory

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `delete-aiox-sop` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-chief` |
| **Execution Type** | `Agent` |

## Metadata
```yaml
id: delete-aiox-sop
name: "Delete SOP Factory"
category: maintenance
agent: sop-chief
elicit: true
autonomous: false
description: "Retire or remove the SOP Factory safely, ensuring shared-safe artifacts are reviewed before deletion."
```

## Purpose

Use this task when decommissioning the squad or removing obsolete surfaces. The review must confirm that no deletion depends on private local enterprise markers.

## Guardrails

- Review versioned artifacts separately from machine-local runtime state.
- Do not treat `workspace/license/enterprise-runtime.capability.yaml` as a normal squad artifact without explicit workspace-owner review.
- Archive or document any still-relevant operational projection before deletion.

## Acceptance Criteria

- [ ] Versioned squad artifacts selected for deletion are explicit
- [ ] Workspace-level enterprise capability artifacts are handled only with explicit workspace-owner review
- [ ] Retirement plan or archive note is produced before final deletion
