# SOP Factory

Enterprise-aware SOP creation and audit squad that remains portable when shared.

## Operating Contract

- Shared default is fail-closed. The squad must not assume `enterprise` just because `workspace/`, `c-level`, or `pro` exist.
- The runtime source of truth is resolved by `scripts/resolve-environment-contract.cjs`.
- When canonical readiness is not proven, the squad stays in `portable_docs_mode` and uses `docs/squad/aiox-sop/operational-projection.yaml`.
- When an explicit `--business=<slug>` is provided and the COO resolves `operations` readiness, the squad may enter `full_workspace_mode`.
- Human-readable SOPs and draft markdown SOPs publish under `docs/sops/`.
- Machine-readable SOPs publish under `workspace/businesses/{business}/sops/` when `business` is explicit and `full_workspace_mode` is proven.
- Auxiliary reports remain under `outputs/aiox-sop/`.
- `squads/aiox-sop/outputs/` stores retained reference packages only; it is not the canonical publish root for new runtime artifacts.

## Optional Business Context

`aiox-sop` can preload canonical business context when the user wants the
analysis to be grounded in the real company and operations data for a specific
business.

Run:

```bash
node squads/aiox-sop/scripts/load-workspace-context.cjs --business=aiox --format=yaml
```

For full parsed payload:

```bash
node squads/aiox-sop/scripts/load-workspace-context.cjs --business=aiox --include-raw --format=json
```

Business-aware context is optional and only valid when:

- `--business=<slug>` is explicit
- the `COO` resolves `operations` readiness as `ready`
- the environment contract switches to `full_workspace_mode`

The loader pulls canonical sources from:

- `workspace/businesses/{slug}/L0-identity/`
- `workspace/businesses/{slug}/L1-strategy/`
- `workspace/businesses/{slug}/L2-tactical/brand/`
- `workspace/_templates/business-template/L1-strategy/`

## Core Surfaces

- `config.yaml`: squad manifest and distribution contract
- `agents/`: orchestrator and specialists
- `tasks/`: creation, extraction, audit, and maintenance tasks
- `workflows/`: end-to-end SOP pipelines
- `docs/`: root shared documentation surface; `docs/sops/` is the publish root for markdown SOPs
- `outputs/`: retained in-repo reference packages kept for historical/support context
- `../docs/squad/aiox-sop/operational-projection.yaml`: non-sensitive portable projection
- `scripts/load-workspace-context.cjs`: optional business-context loader for full workspace mode

## Runtime Modes

- `portable_docs_mode`: default. Use docs projection, root `docs/sops/`, and auxiliary shared-safe outputs only.
- `full_workspace_mode`: only allowed after explicit business context plus canonical `operations` readiness from the COO, enabling canonical `workspace/businesses/{business}/sops/` publication.

## Environment Detection

Run:

```bash
node squads/aiox-sop/scripts/resolve-environment-contract.cjs --format=yaml
```

To check workspace-backed readiness for a real business:

```bash
node squads/aiox-sop/scripts/resolve-environment-contract.cjs --business=aiox --format=yaml
```

`enterprise` is only proven by the canonical marker `workspace/license/enterprise-runtime.capability.yaml`. Without that proof, the access tier stays fail-closed.
