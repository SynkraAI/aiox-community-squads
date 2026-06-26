# Workflow: Implement Customer 360

## Metadata

```yaml
workflow:
  id: implement-customer-360
  name: "Implement Customer 360 View"
  version: "1.0"
  primary_agent: peter-fader
  tier_flow: [0, 1, 2]
  phases: 3
  estimated_duration: "2-4 weeks"

  agents_involved:
    - peter-fader    # Tier 0 - Define value criteria
    - nick-mehta     # Tier 1 - Health Score design
    - avinash-kaushik # Tier 2 - Output and presentation

  views_required:
    - v_customer_lifetime_value
    - v_rfm_segments
    - v_rfm_customer_classification
    - v_customer_health_composite
    - v_health_components_breakdown

  templates_used:
    - health-score-report-tmpl.yaml
    - executive-report-tmpl.yaml

  checklists_used:
    - customer-360-checklist.md
    - pre-implementation-checklist.md

  deliverables:
    - Customer 360 database views
    - Health Score calculation
    - Segmentation rules
    - Report template
    - Playbooks by segment
```

---

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, value-modeling, delivery, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: value-modeling
    - trigger: segmentation_ready
      source: value-modeling
      dest: delivery
    - trigger: reports_ready
      source: delivery
      dest: complete
task_ref:
  primary:
    - calculate-clv
    - segment-rfm
  supporting:
    - design-health-score
    - create-dashboard
```

## Workspace Execution Contract

### Preflight (obrigatório)

1. `*workspace-preflight` (executa `bootstrap-data-workspace.sh` + `validate-data-essentials.sh`)
2. `*workspace-context {slug}`
3. Confirmar templates necessários em `workspace/_templates/analytics/`

### Output Routing

- **Canonical (template-first):**
  - `workspace/businesses/{slug}/analytics/customer-360.yaml`
  - `workspace/businesses/{slug}/analytics/health-score-report.yaml`
  - `workspace/businesses/{slug}/analytics/executive-report.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/implement-customer-360-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/` sem template correspondente em `workspace/_templates/analytics/`.
- Relatórios em `docs/data/{slug}/` são complementares e não substituem artefatos canônicos.

---

## Objetivo

Criar visão unificada do cliente com todos os dados relevantes para decisão.

> "Customer 360 não é sobre coletar mais dados - é sobre criar uma visão acionável que permite tratar cada cliente proporcionalmente ao seu valor."
> — Inspirado em Peter Fader

---

## Regra de Ouro

**Nunca implemente Customer 360 sem responder:**
1. Quem são nossos melhores clientes? (CLV)
2. Como identificamos quem está em risco? (Health Score)
3. Que ação tomamos com cada segmento? (Playbooks)

---

## Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: FUNDAMENTAÇÃO (Peter Fader) - Tier 0                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Definir critérios de "bom cliente"                            │
│   └── CLV alto? Frequência? Fit com ICP?                        │
│                                                                  │
│ □ Mapear dados disponíveis                                      │
│   └── Transações, engajamento, suporte, community               │
│   └── Usar: supabase/docs/SCHEMA.md como referência             │
│                                                                  │
│ □ Definir segmentação inicial                                   │
│   └── Por valor (RFM), por produto, por cohort                  │
│   └── View: v_rfm_customer_classification                       │
│                                                                  │
│ □ Estabelecer quais perguntas o 360 deve responder              │
│   └── "Este cliente vale investir?"                             │
│   └── "Qual próxima ação?"                                      │
│   └── "Que oferta faz sentido?"                                 │
│                                                                  │
│ OUTPUT: Lista de campos essenciais + lógica de segmentação      │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Critérios de valor documentados                               │
│ □ Dados disponíveis mapeados                                    │
│ □ Segmentos definidos                                           │
│ □ Perguntas-chave listadas                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: OPERACIONALIZAÇÃO (Nick Mehta) - Tier 1                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Definir componentes do Health Score                           │
│   └── Product usage (30%) - v_customer_health_composite         │
│   └── Engagement (25%)                                          │
│   └── Support health (20%)                                      │
│   └── Community participation (15%)                             │
│   └── Contract/relationship (10%)                               │
│                                                                  │
│ □ Criar thresholds                                              │
│   └── Verde: 70-100 (Healthy)                                   │
│   └── Amarelo: 40-69 (At Risk)                                  │
│   └── Vermelho: 0-39 (Critical)                                 │
│                                                                  │
│ □ Mapear ações por status                                       │
│   └── Verde → Candidato a upsell/referral                       │
│   └── Amarelo → Check-in proativo                               │
│   └── Vermelho → Intervenção urgente                            │
│                                                                  │
│ □ Implementar DEAR Framework                                    │
│   └── D - Deployment: Cliente implementou?                      │
│   └── E - Engagement: Cliente está ativo?                       │
│   └── A - Adoption: Usa features avançadas?                     │
│   └── R - ROI: Cliente vê valor?                                │
│                                                                  │
│ OUTPUT: Health Score funcionando + playbooks por status         │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ View v_customer_health_composite criada                       │
│ □ View v_health_components_breakdown criada                     │
│ □ Thresholds validados com amostra                              │
│ □ Playbooks documentados                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: COMUNICAÇÃO (Avinash Kaushik) - Tier 2                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Estruturar output visual                                      │
│   └── Quais campos na tela principal?                           │
│   └── Que drill-downs disponibilizar?                           │
│   └── Usar: health-score-report-tmpl.yaml                       │
│                                                                  │
│ □ Criar formato "So What"                                       │
│   └── Para cada cliente: situação + recomendação                │
│   └── Evitar data dump sem ação                                 │
│   └── SO WHAT → WHAT CHANGED → WHY → NOW WHAT                   │
│                                                                  │
│ □ Definir cadência de uso                                       │
│   └── Quem olha? Quando? Que decisão toma?                      │
│   └── Dashboard diário para CS                                  │
│   └── Report semanal para liderança                             │
│                                                                  │
│ □ Criar DMMM mapping                                            │
│   └── Business Objective → Goals → KPIs → Targets → Segments    │
│                                                                  │
│ OUTPUT: Interface e reports que geram ação                      │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Report template criado                                        │
│ □ So What framework aplicado                                    │
│ □ Cadência definida e documentada                               │
│ □ Stakeholders treinados                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Queries de Validação

```sql
-- Verificar distribuição de segmentos RFM
SELECT segment, COUNT(*) as customers,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as pct
FROM v_rfm_customer_classification
GROUP BY segment
ORDER BY customers DESC;

-- Verificar distribuição de Health Score
SELECT health_category, health_color, COUNT(*) as customers
FROM v_customer_health_composite
GROUP BY health_category, health_color
ORDER BY
  CASE health_category
    WHEN 'Critical' THEN 1
    WHEN 'At Risk' THEN 2
    ELSE 3
  END;

-- Top 10 clientes de maior CLV
SELECT mind_slug, mind_name, historical_clv_brl, clv_tier, clv_percentile
FROM v_customer_lifetime_value
ORDER BY historical_clv_brl DESC
LIMIT 10;
```

---

## Checklist de Completude

```yaml
pre_implementation:
  - [ ] Assessment de qualidade de dados realizado
  - [ ] Sponsor executivo identificado
  - [ ] Equipe responsável designada
  - [ ] Métricas de sucesso definidas

fase_1_fundamentacao:
  - [ ] Critérios de "bom cliente" documentados
  - [ ] Dados disponíveis auditados
  - [ ] Segmentação por valor definida
  - [ ] Perguntas do 360 listadas

fase_2_operacionalizacao:
  - [ ] Componentes do Health Score definidos
  - [ ] Pesos validados
  - [ ] Thresholds testados
  - [ ] DEAR Framework implementado
  - [ ] Playbooks por status criados

fase_3_comunicacao:
  - [ ] Output visual estruturado
  - [ ] So What format aplicado
  - [ ] Cadência de uso definida
  - [ ] Reports automatizados
  - [ ] Stakeholders treinados

go_live:
  - [ ] Views em produção
  - [ ] Dashboard funcionando
  - [ ] Alertas configurados
  - [ ] Documentação completa
```

---

## Referências

- **Peter Fader**: "Customer Centricity", "The Customer Centricity Playbook"
- **Nick Mehta**: "Customer Success", "The Customer Success Economy"
- **Avinash Kaushik**: DMMM Framework, So What Framework
- **Checklist completo**: `checklists/customer-360-checklist.md`
- **Template de report**: `templates/health-score-report-tmpl.yaml`

---

*Data Intelligence Pack - Workflow v1.0*
*Primary Agent: @peter-fader | Secondary: @nick-mehta, @avinash-kaushik*
