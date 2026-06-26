# Workflow: Cohort Analysis

## Metadata

```yaml
workflow:
  id: cohort-analysis-workflow
  name: "Cohort Analysis Completo"
  version: "1.0"
  primary_agent: peter-fader
  tier_flow: [0, 0, 1, 2]
  phases: 4
  estimated_duration: "1-2 weeks"

  agents_involved:
    - peter-fader    # Tier 0 - Cohort value analysis
    - sean-ellis     # Tier 0 - Growth cohort metrics
    - wes-kao        # Tier 1 - Learning cohort completion
    - avinash-kaushik # Tier 2 - Reporting and presentation

  views_required:
    - v_clv_cohort_comparison
    - v_rfm_segments
    - v_customer_lifetime_value
    - v_customer_health_composite

  templates_used:
    - cohort-analysis-tmpl.yaml
    - executive-report-tmpl.yaml

  checklists_used:
    - pre-implementation-checklist.md
    - so-what-checklist.md

  deliverables:
    - Cohort retention matrix
    - CLV by cohort comparison
    - Acquisition channel analysis
    - Growth recommendations
    - Executive cohort report
```

---

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, cohort-definition, synthesis, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: cohort-definition
    - trigger: cohort_analysis_complete
      source: cohort-definition
      dest: synthesis
    - trigger: report_complete
      source: synthesis
      dest: complete
task_ref:
  primary:
    - analyze-cohort
  supporting:
    - calculate-clv
    - segment-rfm
    - design-learning-outcomes
    - create-dashboard
```

## Workspace Execution Contract

### Preflight (obrigatório)

1. `*workspace-preflight` (executa `bootstrap-data-workspace.sh` + `validate-data-essentials.sh`)
2. `*workspace-context {slug}`
3. Confirmar templates necessários em `workspace/_templates/analytics/`

### Output Routing

- **Canonical (template-first):**
  - `workspace/businesses/{slug}/analytics/cohort-analysis.yaml`
  - `workspace/businesses/{slug}/analytics/executive-report.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/cohort-analysis-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/` sem template correspondente em `workspace/_templates/analytics/`.
- Relatórios em `docs/data/{slug}/` são complementares e não substituem artefatos canônicos.

---

## Objetivo

Analisar performance de diferentes cohorts para identificar padrões de retenção, valor e comportamento ao longo do tempo.

> "Cohort analysis is the only way to truly understand customer behavior over time. Averages lie - cohorts reveal truth."
> — Inspirado em Peter Fader

---

## Regra de Ouro

**Nunca analise cohorts sem responder:**
1. Qual cohort tem maior CLV? (Valor)
2. Qual canal de aquisição traz melhores clientes? (Origem)
3. Qual cohort retém melhor ao longo do tempo? (Retenção)
4. O que diferencia os cohorts vencedores? (Padrões)

---

## Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINIÇÃO DE COHORTS (Peter Fader) - Tier 0             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Definir critérios de agrupamento                              │
│   └── Por mês de aquisição (padrão)                             │
│   └── Por canal de aquisição                                    │
│   └── Por produto inicial                                       │
│   └── Por valor da primeira compra                              │
│                                                                  │
│ □ Estabelecer período de análise                                │
│   └── Últimos 12 meses? 24 meses?                               │
│   └── Cohorts com pelo menos 3 meses de maturidade              │
│                                                                  │
│ □ Mapear métricas por cohort                                    │
│   └── CLV médio e mediano                                       │
│   └── Número de clientes                                        │
│   └── Receita total                                             │
│   └── Usar: v_clv_cohort_comparison                             │
│                                                                  │
│ □ Criar segmentação de valor por cohort                         │
│   └── % de Champions, Loyal, At Risk por cohort                 │
│   └── Correlacionar com canal de origem                         │
│                                                                  │
│ OUTPUT: Cohorts definidos + métricas base calculadas            │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Critérios de cohort documentados                              │
│ □ Período de análise definido                                   │
│ □ View v_clv_cohort_comparison populada                         │
│ □ Métricas base por cohort calculadas                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: ANÁLISE DE CRESCIMENTO (Sean Ellis) - Tier 0            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Calcular retention por cohort                                 │
│   └── M1, M2, M3... M12 retention                               │
│   └── Identificar curva de retenção típica                      │
│   └── Marcar cohorts acima/abaixo da média                      │
│                                                                  │
│ □ Analisar canais de aquisição                                  │
│   └── Qual canal traz clientes com maior retention?             │
│   └── Qual canal traz maior volume?                             │
│   └── Trade-off volume vs qualidade                             │
│                                                                  │
│ □ Medir viral coefficient por cohort                            │
│   └── Cohorts mais antigos indicam mais?                        │
│   └── Referral rate por cohort                                  │
│   └── Tempo médio até primeira indicação                        │
│                                                                  │
│ □ Identificar activation milestones                             │
│   └── Que ações nos primeiros 7 dias predizem retenção?         │
│   └── Comparar ativação entre cohorts                           │
│                                                                  │
│ OUTPUT: Retention matrix + channel analysis + viral metrics     │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Retention matrix criada (cohort x mês)                        │
│ □ Canais rankeados por qualidade                                │
│ □ Viral coefficient por cohort calculado                        │
│ □ Activation milestones identificados                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: COHORT DE APRENDIZADO (Wes Kao) - Tier 1                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Analisar completion rate por cohort                           │
│   └── Cohorts mais recentes completam mais?                     │
│   └── Mudanças no produto afetaram completion?                  │
│   └── Correlação completion → retention                         │
│                                                                  │
│ □ Mapear engagement patterns                                    │
│   └── Dias ativos por cohort                                    │
│   └── Sessões por semana                                        │
│   └── Features mais usadas por cohort                           │
│                                                                  │
│ □ Identificar learning outcomes                                 │
│   └── Que cohort atingiu mais outcomes?                         │
│   └── Tempo médio até primeiro outcome                          │
│   └── State change achievement rate                             │
│                                                                  │
│ □ Correlacionar aprendizado com valor                           │
│   └── Completion alto → CLV alto?                               │
│   └── Outcomes atingidos → menor churn?                         │
│                                                                  │
│ OUTPUT: Learning metrics por cohort + correlações               │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Completion rate por cohort calculado                          │
│ □ Engagement patterns mapeados                                  │
│ □ Learning outcomes por cohort medidos                          │
│ □ Correlações documentadas                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: REPORT E AÇÃO (Avinash Kaushik) - Tier 2                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Criar Cohort Dashboard                                        │
│   └── Retention heatmap                                         │
│   └── CLV trend por cohort                                      │
│   └── Channel performance matrix                                │
│                                                                  │
│ □ Aplicar So What Framework                                     │
│   └── SO WHAT: "Cohorts de referral têm 3x mais CLV"            │
│   └── WHAT CHANGED: "Últimos 3 meses: queda de 20%"             │
│   └── WHY: "Mudança na política de indicação"                   │
│   └── NOW WHAT: "Reverter política ou compensar"                │
│                                                                  │
│ □ Gerar recomendações acionáveis                                │
│   └── Onde investir em aquisição?                               │
│   └── Que cohorts precisam de intervenção?                      │
│   └── Que padrões replicar?                                     │
│                                                                  │
│ □ Definir monitoramento contínuo                                │
│   └── Cadência de análise (mensal)                              │
│   └── Alertas de desvio                                         │
│   └── Métricas de acompanhamento                                │
│                                                                  │
│ OUTPUT: Executive cohort report + action plan                   │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Dashboard criado                                              │
│ □ So What aplicado a cada insight                               │
│ □ Recomendações priorizadas                                     │
│ □ Monitoramento configurado                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Queries de Validação

```sql
-- CLV por cohort de aquisição
SELECT
    cohort_label,
    customers_acquired,
    cohort_total_revenue_brl,
    avg_clv_brl,
    median_clv_brl,
    cohort_age_months
FROM v_clv_cohort_comparison
ORDER BY cohort_month DESC
LIMIT 12;

-- Retention matrix (simplificada)
WITH cohort_activity AS (
    SELECT
        DATE_TRUNC('month', MIN(t.paid_at)) AS cohort_month,
        t.mind_id,
        DATE_TRUNC('month', t.paid_at) AS activity_month
    FROM transactions t
    WHERE t.status = 'approved'
    GROUP BY t.mind_id, DATE_TRUNC('month', t.paid_at)
)
SELECT
    TO_CHAR(cohort_month, 'YYYY-MM') AS cohort,
    EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) AS month_number,
    COUNT(DISTINCT mind_id) AS active_customers
FROM cohort_activity
GROUP BY cohort_month, EXTRACT(MONTH FROM AGE(activity_month, cohort_month))
ORDER BY cohort_month, month_number;

-- Distribuição de segmentos por cohort
SELECT
    cc.cohort_label,
    rc.segment,
    COUNT(*) AS customers
FROM v_clv_cohort_comparison cc
JOIN v_rfm_customer_classification rc USING (mind_id)
GROUP BY cc.cohort_label, rc.segment
ORDER BY cc.cohort_label, customers DESC;
```

---

## Checklist de Completude

```yaml
pre_implementation:
  - [ ] Período de análise definido
  - [ ] Critérios de cohort acordados
  - [ ] Dados de aquisição disponíveis
  - [ ] Stakeholders identificados

fase_1_definicao:
  - [ ] Cohorts criados
  - [ ] Métricas base calculadas
  - [ ] CLV por cohort disponível
  - [ ] Segmentação por valor mapeada

fase_2_crescimento:
  - [ ] Retention matrix criada
  - [ ] Canais de aquisição analisados
  - [ ] Viral metrics por cohort
  - [ ] Activation milestones identificados

fase_3_aprendizado:
  - [ ] Completion por cohort calculado
  - [ ] Engagement patterns mapeados
  - [ ] Learning outcomes medidos
  - [ ] Correlações documentadas

fase_4_report:
  - [ ] Dashboard criado
  - [ ] So What aplicado
  - [ ] Recomendações documentadas
  - [ ] Monitoramento configurado

go_live:
  - [ ] Report executivo entregue
  - [ ] Ações priorizadas
  - [ ] Cadência de revisão definida
  - [ ] Ownership atribuído
```

---

## Referências

- **Peter Fader**: Cohort-based CLV analysis, Customer Centricity
- **Sean Ellis**: Growth accounting, Retention analysis
- **Wes Kao**: Learning cohort analysis, Completion metrics
- **Avinash Kaushik**: So What Framework, Data Storytelling
- **Template**: `templates/cohort-analysis-tmpl.yaml`
- **Checklist**: `checklists/pre-implementation-checklist.md`

---

*Data Intelligence Pack - Workflow v1.0*
*Primary Agent: @peter-fader | Secondary: @sean-ellis, @wes-kao, @avinash-kaushik*
