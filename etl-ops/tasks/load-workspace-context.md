# ETL Load Workspace Context

## Contrato SINKRA

Domain: `Operational`
executor: etl-chief
atomic_layer: Atom
Input: business_slug opcional, workspace constraints
Output: workspace context snapshot, route decision
Pre-condition: scripts de preflight disponíveis e constraints carregadas
Post-condition: rota canônica/legacy/block definida e snapshot persistido
Performance: bloquear escrita canônica sem bootstrap válido


## Metadata

| Field | Value |
|---|---|
| **task_name** | Load Workspace Context for ETL |
| **status** | Active |
| **responsible_executor** | `@etl-chief` |
| **execution_type** | `Deterministic` |
| **input** | Optional `constraints.business_slug` from `process.schema.json` |
| **output** | Workspace context snapshot + canonical/custom route decision |
| **action_items** | 4-phase preflight and context mapping |
| **acceptance_criteria** | 7 measurable criteria |

## Purpose

Garantir que o ETL escreva no destino correto antes de processar qualquer fonte:

- **canonical (workspace-first):** `workspace/businesses/{slug}/etl/`
- **custom (ad-hoc):** `docs/etl/{slug}/`
- **legacy fallback:** `outputs/etl/{run_id}/` (somente quando não houver slug)

## Inputs

### Minimal Input

```json
{
  "constraints": {
    "business_slug": "acme"
  }
}
```

### Fallback Without Slug

```json
{
  "constraints": {}
}
```

## Execution Flow

### Phase 1: Preflight

Run in order:

```bash
bash squads/etl-ops/scripts/bootstrap-etl-workspace.sh {business_slug}
bash squads/etl-ops/scripts/validate-etl-essentials.sh
```

If `{business_slug}` is not provided, run only validation and set route to legacy/custom.

### Phase 2: Load Workspace Context

Read when available:

- `workspace/businesses/{business_slug}/L0-identity/company-dna.yaml`
- `workspace/businesses/{business_slug}/L1-strategy/icp.yaml`
- `workspace/businesses/{business_slug}/L2-tactical/brand/brand-guidelines.yaml`
- `workspace/domains/brand/entities.yaml`
- `workspace/domains/content/entities.yaml`
- `workspace/domains/movement/entities.yaml`
- `workspace/_templates/etl/*.yaml`

### Phase 3: Route Decision

Rules:

1. If `business_slug` exists and bootstrap passed:
   - `output_route.mode = canonical`
   - `output_route.root = workspace/businesses/{business_slug}/etl/`
2. If `business_slug` exists but bootstrap failed:
   - `output_route.mode = blocked`
3. If `business_slug` missing:
   - `output_route.mode = legacy_fallback`
   - `output_route.root = outputs/etl/{run_id}/`

### Phase 4: Persist Context Snapshot

Write snapshot in canonical mode:

- `workspace/businesses/{business_slug}/etl/workspace-context.yaml`

Fallback snapshot:

- `docs/etl/{business_slug|global}/workspace-context-{run_id}.md`

## Snapshot Contract

```yaml
workspace_context:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  business_slug: "{slug|null}"
  preflight_status: "pass|fail"
  output_route:
    mode: "canonical|legacy_fallback|blocked"
    root: "path"
  templates_available:
    - "workspace/_templates/etl/etl-run-envelope.yaml"
  blockers: []
  warnings: []
```

## Checkpoint Rules

| Phase | Checkpoint | Veto Condition |
|-------|------------|----------------|
| Preflight | Scripts executed | Essentials validation failed |
| Context | Required files checked | Slug provided but business directory missing |
| Route | Output route decided | Route mode `blocked` |
| Snapshot | Context persisted | Cannot write snapshot path |

## Acceptance Criteria

1. Preflight scripts execute before ETL processing.
2. Route decision is explicit (`canonical`, `legacy_fallback`, or `blocked`).
3. Canonical mode only when `business_slug` is valid.
4. Snapshot contains route + blockers + warnings.
5. Template catalog is checked in `_templates/etl`.
6. No canonical write outside `workspace/businesses/{slug}/etl/`.
7. If blocked, processing is vetoed before extraction.


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
