# Task: Load Workspace Context

```yaml
task:
  id: load-workspace-context
  name: Carregar Contexto do Workspace
  agent: data-chief
  elicit: false
```

## Descrição

Task de preflight do squad `data` para alinhar leituras e rotas de output antes de qualquer análise.

## Objetivos

1. Executar validação de infraestrutura `workspace_first`.
2. Ler contexto real do negócio (`brand`, `content`, `movement`, `L0-identity`, `L1-strategy`).
3. Definir rota correta de saída:
   - **canonical**: `workspace/businesses/{slug}/analytics/` (template-first)
   - **canonical cohorts**: `workspace/businesses/{slug}/analytics/cohorts/` (template-first)
   - **custom**: `docs/data/{slug}/` (ad-hoc, sem contrato canônico)

## Fase 1: Preflight obrigatório

Executar, nesta ordem:

```bash
bash squads/data/scripts/bootstrap-data-workspace.sh {slug}
bash squads/data/scripts/validate-data-essentials.sh
```

Se falhar, não iniciar workflows/tasks analíticas.

## Fase 2: Leitura de contexto

### Base do negócio (`{slug}`)

- `workspace/businesses/{slug}/L0-identity/company-dna.yaml`
- `workspace/businesses/{slug}/L1-strategy/icp.yaml`
- `workspace/businesses/{slug}/L2-tactical/brand/brand-guidelines.yaml`
- `workspace/businesses/{slug}/L1-strategy/pricing-strategy.yaml`
- `workspace/businesses/{slug}/L1-strategy/kpi-scorecards.yaml`

### Contexto de domínio complementar

- `workspace/domains/brand/entities.yaml`
- `workspace/domains/content/entities.yaml`
- `workspace/domains/movement/entities.yaml`

### Catálogo de templates canônicos

- `workspace/_templates/analytics/*.yaml`
- `workspace/_templates/analytics/cohorts/*.yaml`

## Fase 3: Decisão de saída

### Modo canonical (preferencial)

Use quando houver template correspondente:

- saída: `workspace/businesses/{slug}/analytics/{artifact}.yaml`
- pré-condição: `workspace/_templates/analytics/{artifact}.yaml` existe

Para diagnóstico de cohorts:

- saída: `workspace/businesses/{slug}/analytics/cohorts/{artifact}.yaml`
- pré-condição: `workspace/_templates/analytics/cohorts/{artifact}.yaml` existe

### Modo custom (exceção controlada)

Use para exploração e relatórios fora do contrato padrão:

- saída: `docs/data/{slug}/{artifact}.md`
- sem template obrigatório
- deve ser marcado como `custom_report: true`

## Output da task

Salvar resumo de contexto em:

- `workspace/businesses/{slug}/evidence/data-workspace-context.yaml`

Contrato mínimo:

```yaml
workspace_context:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  business_slug: "{slug}"
  workspace_preflight: "pass|fail"
  available_canonical_templates: []
  missing_templates: []
  canonical_outputs_allowed: []
  custom_outputs_allowed:
    - "docs/data/{slug}/"
  blockers: []
```

## Veto Conditions

- Bloquear se `validate-data-essentials.sh` falhar.
- Bloquear escrita em `workspace/businesses/{slug}/analytics/` sem template correspondente.
- Bloquear escrita em `workspace/businesses/{slug}/analytics/cohorts/` sem template correspondente.
- Bloquear escrita em qualquer path de workspace fora de `workspace/businesses/{slug}/analytics/`.

## Checklist

- [ ] Preflight executado e aprovado.
- [ ] Contexto de negócio carregado.
- [ ] Catálogo de templates analytics carregado.
- [ ] Rotas canonical/custom definidas antes da execução analítica.

---

*Task do Squad Data - Data Chief*
