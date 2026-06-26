# Task: Load Workspace Context

```yaml
task:
  id: load-workspace-context
  name: Carregar Contexto do Workspace
  agent: brand-chief
  elicit: false
```

## Descrição

Task de preflight do squad `brand` para consolidar contexto real do workspace antes de executar qualquer workflow de naming, posicionamento ou ativação.

## Objetivos

1. Executar validação de infraestrutura `workspace_first`.
2. Ler contexto de negócio e domínios que influenciam decisões de brand.
3. Definir rota de saída:
   - **canonical:** `workspace/businesses/{brand_name}/L2-tactical/brand/`
   - **custom:** `docs/brand/{brand_name}/` (ad-hoc, sem contrato canônico)

## Fase 1: Preflight obrigatório

Executar, nesta ordem:

```bash
bash squads/brand/scripts/bootstrap-brand-workspace.sh {brand_name}
bash squads/brand/scripts/validate-brand-essentials.sh
node workspace/scripts/resolve-squad-workspace-readiness.cjs --squad=brand --business={brand_name} --context-type=brand
```

Se falhar, bloquear execução dos workflows.

## Fase 2: Leitura de contexto

### Base do negócio (`{brand_name}`)

- `workspace/businesses/{brand_name}/L0-identity/company-dna.yaml`
- `workspace/businesses/{brand_name}/L1-strategy/icp.yaml`
- `workspace/businesses/{brand_name}/L1-strategy/pricing-strategy.yaml`
- `workspace/businesses/{brand_name}/L1-strategy/kpi-scorecards.yaml`
- `workspace/businesses/{brand_name}/L2-tactical/brand/brandbook.yaml`
- `workspace/businesses/{brand_name}/L2-tactical/brand/domain-decision.yaml`

### Domínios complementares

- `workspace/domains/brand/entities.yaml`
- `workspace/domains/content/entities.yaml`
- `workspace/domains/movement/entities.yaml`

### Catálogo de templates canônicos

- `workspace/_templates/business-template/L2-tactical/brand/*`

## Fase 3: Decisão de saída

### Modo canonical (preferencial)

Use quando houver template correspondente:

- saída: `workspace/businesses/{brand_name}/L2-tactical/brand/{artifact}.md|yaml`
- pré-condição: namespace `L2-tactical/brand` disponível

### Modo custom (exceção controlada)

Use para exploração fora do contrato canônico:

- saída: `docs/brand/{brand_name}/{artifact}.md`
- sem template obrigatório
- marcar `custom_report: true`

## Output da task

Salvar snapshot em:

- `workspace/businesses/{brand_name}/L2-tactical/brand/workspace-context.yaml`

Contrato mínimo:

```yaml
workspace_context:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  brand_name: "{brand_name}"
  workspace_preflight: "pass|fail"
  coo_readiness_status: "ready|blocked"
  canonical_namespace: "workspace/businesses/{brand_name}/L2-tactical/brand/"
  available_canonical_templates: []
  missing_templates: []
  canonical_outputs_allowed: []
  custom_outputs_allowed:
    - "docs/brand/{brand_name}/"
  blockers: []
```

## Veto Conditions

- Bloquear se `validate-brand-essentials.sh` falhar.
- Bloquear se o `COO` retornar `blocked`.
- Bloquear escrita em qualquer path de workspace fora de `workspace/businesses/{brand_name}/L2-tactical/brand/`.

## Checklist

- [ ] Preflight executado e aprovado.
- [ ] Contexto de negócio carregado.
- [ ] Contexto de domínios complementares carregado.
- [ ] Catálogo de templates brand carregado.
- [ ] Rotas canonical/custom definidas antes da execução.

---

*Task do Squad Brand - Brand Chief*
