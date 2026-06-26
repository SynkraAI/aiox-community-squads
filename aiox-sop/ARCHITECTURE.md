# SOP Factory Architecture

## Intent

`aiox-sop` turns operational knowledge into structured SOP artifacts for humans and AI systems. It is enterprise-aware locally, but it must remain safe when copied into a less capable repository.

## Architecture Layers

1. Orchestrator layer: `sop-chief` routes requests and enforces quality.
2. Specialist layer: analyst, creator, extractor, ML architect, auditor.
3. Workflow layer: creation, audit, and extraction pipelines.
4. Runtime contract layer: environment detection decides which context surfaces may be used.

## Environment Contract

The squad resolves a shared contract with these fields:

- `access_tier`: `opensource|pro|enterprise`
- `runtime_mode`: `portable_docs_mode|full_workspace_mode`
- `source_of_truth`: `docs_projection|workspace_canonical`
- `reason`
- `evidence_paths`

Decision rules:

- `enterprise` requires explicit proof.
- `pro` is allowed when the Pro pack exists and enterprise is not proven.
- `portable_docs_mode` remains the default when explicit business context is absent or readiness is not proven.
- `full_workspace_mode` is allowed only when explicit runtime context and canonical COO readiness are both proven.

## Optional Workspace Business Context

When `full_workspace_mode` is proven for an explicit `business`, `aiox-sop`
may load a business-aware context snapshot before analysis, extraction, or
audit work that needs real `L0-identity`/`L1-strategy` data.

Canonical business context surfaces:

- `workspace/businesses/{business}/L0-identity/company-dna.yaml`
- `workspace/businesses/{business}/L1-strategy/icp.yaml`
- `workspace/businesses/{business}/L1-strategy/offerbook.yaml` when present
- `workspace/businesses/{business}/L1-strategy/team-structure.yaml`
- `workspace/businesses/{business}/L1-strategy/pricing-strategy.yaml`
- `workspace/businesses/{business}/L1-strategy/kpi-scorecards.yaml`
- `workspace/businesses/{business}/L1-strategy/commission-design.yaml` when present
- `workspace/_templates/business-template/L1-strategy/`

Loader surface:

- `squads/aiox-sop/scripts/load-workspace-context.cjs`
- `squads/aiox-sop/tasks/load-workspace-context.md`

This context remains read-first, but the same readiness gate also unlocks the
canonical machine-readable publish surface at
`workspace/businesses/{business}/sops/`.

## Non-Sensitive Projection

Portable mode consumes:

- `docs/squad/aiox-sop/operational-projection.yaml`

This projection may describe safe outputs, mode rules, and evidence surfaces, but it must not embed private workspace topology.

## Output Zones

- `docs/sops/`: canonical shared-safe markdown SOPs and draft SOPs
- `workspace/businesses/{business}/sops/`: canonical machine-readable SOPs for an explicit business in `full_workspace_mode`
- `outputs/aiox-sop/`: auxiliary generated artifacts
- `outputs/aiox-sop/extractions/`: extraction reports, confidence maps, and review aids
- `outputs/aiox-sop/audits/`: audit reports and dashboards
- `outputs/aiox-sop/analysis/`: analysis and benchmark reports
- `outputs/aiox-sop/converted/`: conversion validation reports and non-canonical byproducts
- `outputs/aiox-sop/checklists/`: generated checklists
- `outputs/aiox-sop/certificates/`: certification artifacts
- `squads/aiox-sop/outputs/`: retained reference packages; not a canonical runtime output zone

## Current Constraint

`aiox-sop` now has canonical readiness support in the COO resolver through the `operations` context. The correct runtime behavior is:

- without explicit `business`, runtime remains `portable_docs_mode`
- with explicit `business` and ready operations namespace, runtime may become `full_workspace_mode`
- shared-safe docs projection remains the default fallback source of truth
- markdown SOP publication does not require workspace write access
- YAML/JSON SOP publication requires explicit `business` and the canonical workspace gate
