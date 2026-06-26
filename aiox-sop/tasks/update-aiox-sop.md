# Task: Update SOP Factory

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `update-aiox-sop` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-chief` |
| **Execution Type** | `Agent` |

## Metadata
```yaml
id: update-aiox-sop
name: "Update SOP Factory"
category: maintenance
agent: sop-chief
elicit: false
autonomous: true
description: "Apply controlled updates to the SOP Factory while preserving the enterprise-aware fail-closed runtime contract."
```

## Purpose

Use this task when the squad needs structural, documentation, workflow, or projection updates without breaking its shared-safe posture.

## Guardrails

- Resolve the environment contract before assuming richer context surfaces.
- Preserve portable behavior as the default.
- Do not introduce implicit enterprise assumptions into versioned artifacts.
- Keep outputs aligned across config, tasks, workflows, and docs projection.

## Acceptance Criteria

- [ ] Runtime contract remains valid after the update
- [ ] Shared-safe docs projection remains aligned with squad config
- [ ] Structural docs and maintenance surfaces stay current
