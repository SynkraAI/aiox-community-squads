# Task: Load Workspace Context

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `load-workspace-context` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-chief` |
| **Execution Type** | `Worker` |

## Metadata
```yaml
id: load-workspace-context
name: "Load Workspace Context"
category: governance
agent: sop-chief
elicit: false
autonomous: true
description: "Load canonical business context from workspace/L0-identity + workspace/L1-strategy when the user wants business-aware SOP analysis."
```

## Purpose

Use this task when the user wants `aiox-sop` to analyze or extract SOPs with
explicit business context instead of relying only on generic process text.

This task is optional. `aiox-sop` remains safe and portable by default. Only
load workspace context when the user explicitly provides a `business` slug and
the `COO` confirms `operations` readiness.

## Preconditions

- [ ] Explicit `business` slug provided
- [ ] `COO` readiness for `aiox-sop` + `operations` resolves to `ready`
- [ ] Environment contract resolves `runtime_mode: full_workspace_mode`

## Command

```bash
node squads/aiox-sop/scripts/load-workspace-context.cjs --business={slug} --format=yaml
```

For full parsed payload:

```bash
node squads/aiox-sop/scripts/load-workspace-context.cjs --business={slug} --include-raw --format=json
```

## Canonical Sources

### Workspace registration

- `workspace/_system/config.yaml`

### Business company context

- `workspace/businesses/{slug}/L0-identity/company-dna.yaml`
- `workspace/businesses/{slug}/L1-strategy/icp.yaml`
- `workspace/businesses/{slug}/L1-strategy/offerbook.yaml` (optional)
- Optional brand context may be merged when the business already maintains a canonical brand file.

### Business operations context

- `workspace/businesses/{slug}/L1-strategy/team-registry.yaml`
- `workspace/businesses/{slug}/L1-strategy/pricing-strategy.yaml`
- `workspace/businesses/{slug}/L1-strategy/kpi-scorecards.yaml`
- `workspace/businesses/{slug}/L1-strategy/commission-design.yaml` (optional)
- Optional funnel/VSL references may be merged when the business already maintains them.

### Shared templates

- `workspace/_templates/business-template/L1-strategy/`

## Output Contract

This task is session-first. It loads context for analysis time and does not
write canonical business artifacts.

Minimum payload:

```yaml
workspace_context:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  business_slug: "{slug}"
  coo_readiness_status: "ready|blocked"
  runtime_mode: "portable_docs_mode|full_workspace_mode"
  source_of_truth: "docs_projection|workspace_canonical"
  loaded_sources:
    company: []
    operations: []
    templates: []
  blockers: []
```

## Veto Conditions

- STOP if `--business` is absent
- STOP if `COO` returns `blocked`
- STOP if environment contract does not resolve to `full_workspace_mode`
- STOP if required `L0-identity/` or `L1-strategy/` sources are missing
- STOP if a command attempts to treat portable docs mode as business-aware context

## Checklist

- [ ] Business slug provided explicitly
- [ ] COO readiness resolved and approved
- [ ] Environment contract switched to `full_workspace_mode`
- [ ] Company sources loaded
- [ ] Operations sources loaded
- [ ] Template inventory loaded
