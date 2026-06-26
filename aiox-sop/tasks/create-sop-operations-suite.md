# Task: Create SOP Operations Suite

```yaml
task:
  id: create-sop-operations-suite
  name: Criar Suite de SOPs Operacionais
  agent: sop-chief
  trigger: manual
  elicit: false
  commands:
    - "*create-sop-operations-suite {slug}"
  requires:
    - workspace-context loaded
    - COO readiness = ready
```

## Descrição

Task que cria SOPs a partir dos YAMLs de operations preenchidos pelo C-Level. Consome dados canônicos do workspace e transforma cada YAML operacional em um SOP executável (human-readable e/ou ML-readable).

**Trigger principal:** Diagnóstico C-Level identifica Operations < 70 e recomenda esta task.
**Fluxo:** `*diagnose-business {slug}` → gap Operations → `*create-sop-operations-suite {slug}`

**Guardian:** sop-chief (Deming)

## Pré-requisitos

1. Business existe: `workspace/businesses/{slug}/` presente
2. Pelo menos 1 YAML de operations preenchido (não apenas template)
3. COO readiness = `ready` (via `resolve-squad-workspace-readiness.cjs`)

## Workflow

### Fase 0: Resolver Ambiente e Carregar Contexto

```yaml
environment:
  steps:
    - resolve_environment: "*environment"
    - force_mode: "full_workspace_mode"  # Esta task REQUER workspace
    - load_context: "*workspace-context {slug}"
    - validate_readiness: "COO readiness must be 'ready'"
```

Se readiness != ready: HALT com "Readiness não confirmado pelo COO. Execute `*resolve-readiness aiox-sop` no C-Level primeiro."

### Fase 1: Inventário de Operations

Listar arquivos em `workspace/businesses/{slug}/L1-strategy/`:

```yaml
operations_inventory:
  files:
    - id: team-structure
      path: "L1-strategy/team-structure.yaml"
      sop_type: "Estrutura Organizacional"
      sop_id: "SOP-OPS-TEAM"

    - id: pricing-strategy
      path: "L1-strategy/pricing-strategy.yaml"
      sop_type: "Decisões de Pricing"
      sop_id: "SOP-OPS-PRICING"

    - id: kpi-scorecards
      path: "L1-strategy/kpi-scorecards.yaml"
      sop_type: "Gestão de KPIs"
      sop_id: "SOP-OPS-KPI"

    - id: commission-design
      path: "L1-strategy/commission-design.yaml"
      sop_type: "Cálculo de Comissões"
      sop_id: "SOP-OPS-COMMISSION"
```

Para cada arquivo:
- Verificar se existe
- Se existe, verificar completude (% campos preenchidos vs FILL_THIS)
- Se completude < 30%: marcar como "skip" (template quase vazio)
- Se completude >= 30%: marcar como "process" (dados suficientes)

### Fase 2: Geração de SOPs

Para cada arquivo marcado como "process":

```yaml
generation:
  for_each: operations_inventory[status=process]
  steps:
    - read_source: "Ler YAML completo do workspace"
    - extract_fields: "Extrair campos preenchidos (ignorar FILL_THIS/null)"
    - route_to_creator: "@sop-creator *create-sop-human"
    - input_context:
        source_yaml: "{arquivo lido}"
        sop_type: "{tipo do SOP}"
        sop_id: "{ID do SOP}"
        business_context: "{dados do workspace-context carregado}"
    - output_path: "workspace/businesses/{slug}/sops/{sop_id}.md"
```

**Mapeamento Source → SOP:**

| Source YAML | SOP | Conteúdo do SOP |
|-------------|-----|-----------------|
| `team-structure.yaml` | SOP-OPS-TEAM | Organograma, roles, KPIs por role, reporting lines, hiring roadmap |
| `pricing-strategy.yaml` | SOP-OPS-PRICING | Modelo de pricing, filosofia, psicologia, posição competitiva, cadência de revisão |
| `kpi-scorecards.yaml` | SOP-OPS-KPI | North star, métricas por departamento, cadência de review, escalation rules |
| `commission-design.yaml` | SOP-OPS-COMMISSION | Estrutura de comissão, tiers, bônus, guardrails, clawbacks |

### Fase 3: Scoring Embutido

Cada YAML de operations tem um `_strength_score` embutido (4 dimensões, 1-10). Se preenchido, incluir no SOP como seção "Diagnóstico":

```yaml
diagnostic_inclusion:
  if: "source_yaml has _strength_score with values != FILL_THIS"
  then: "Incluir seção 'Diagnóstico' no SOP com scores e gaps identificados"
  format: |
    ## Diagnóstico Operacional
    | Dimensão | Score | Status |
    |----------|-------|--------|
    | {dim_1} | {score}/10 | {9-10: Forte, 7-8: Bom, 4-6: Atenção, 1-3: Crítico} |
```

### Fase 4: Quality Gate

Após gerar cada SOP:

```yaml
quality_gate:
  checks:
    - sop_has_title: "Título claro e descritivo"
    - sop_has_scope: "Escopo definido (quem, quando, o quê)"
    - sop_has_steps: "Passos numerados e acionáveis"
    - sop_has_owner: "Responsável definido"
    - sop_has_source: "Referência ao YAML fonte"
    - sop_no_business_in_squad: "SOP está em workspace/, não em squads/"
  verdict: "PASS se 5/6 checks ok, FAIL se < 5"
```

### Fase 5: Relatório

Gerar relatório consolidado:

```yaml
output:
  path: "workspace/businesses/{slug}/sops/SOP-OPS-SUITE-REPORT.md"
  content: |
    # Operations SOP Suite: {business_name}
    **Gerado em:** {date}
    **Business:** {slug}
    **SOPs gerados:** {count}/{total_possible}

    | SOP ID | Tipo | Source | Status | Path |
    |--------|------|--------|--------|------|
    | SOP-OPS-TEAM | Estrutura Organizacional | team-structure.yaml | GERADO | sops/SOP-OPS-TEAM.md |
    | SOP-OPS-PRICING | Decisões de Pricing | pricing-strategy.yaml | SKIP (completude < 30%) | - |

    ## Próximos Passos
    - SOPs com status SKIP: completar YAML fonte via C-Level `*elicit-operations {slug}`
    - SOPs gerados: auditar via `*audit-sop {path}`
```

## Validação da Task

- [ ] Ambiente resolvido (full_workspace_mode)
- [ ] Workspace context carregado
- [ ] Readiness validado via COO
- [ ] Inventário de operations completo
- [ ] SOPs gerados para YAMLs com completude >= 30%
- [ ] Quality gate executado para cada SOP
- [ ] Relatório consolidado gerado
- [ ] Nenhum dado de business dentro de `squads/`

---

*Task do Squad AIOX-SOP - SOP Chief (Deming)*
*Versão: 1.0.0*
