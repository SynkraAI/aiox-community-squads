# Workflow: Implement Attribution System

## Metadata

```yaml
workflow:
  id: implement-attribution
  name: "Implement Marketing Attribution System"
  version: "1.0"
  primary_agent: avinash-kaushik
  tier_flow: [0, 1, 2]
  phases: 4
  estimated_duration: "2-3 weeks"

  agents_involved:
    - avinash-kaushik  # Primary - Attribution models, DMMM
    - sean-ellis       # Referral attribution
    - peter-fader      # CLV-weighted attribution

  views_required:
    - v_attribution_touchpoint_journey (Sprint 2)
    - v_attribution_first_touch (Sprint 2)
    - v_attribution_last_touch (Sprint 2)
    - v_attribution_position_based (Sprint 2)
    - v_customer_lifetime_value
    - v_rfm_customer_classification

  templates_used:
    - attribution-report-tmpl.yaml
    - dmmm-tmpl.yaml

  checklists_used:
    - so-what-checklist.md
    - pre-implementation-checklist.md

  deliverables:
    - First-touch attribution
    - Last-touch attribution
    - Position-based attribution
    - CLV-weighted attribution
    - Monthly attribution report
    - DMMM documentation
```

---

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, attribution-modeling, reporting, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: attribution-modeling
    - trigger: model_validated
      source: attribution-modeling
      dest: reporting
    - trigger: reports_published
      source: reporting
      dest: complete
task_ref:
  primary:
    - build-attribution
  supporting:
    - calculate-clv
    - segment-rfm
    - create-dashboard
```

## Workspace Execution Contract

### Preflight (obrigatório)

1. `*workspace-preflight` (executa `bootstrap-data-workspace.sh` + `validate-data-essentials.sh`)
2. `*workspace-context {slug}`
3. Confirmar templates necessários em `workspace/_templates/analytics/`

### Output Routing

- **Canonical (template-first):**
  - `workspace/businesses/{slug}/analytics/attribution-report.yaml`
  - `workspace/businesses/{slug}/analytics/dmmm.yaml`
  - `workspace/businesses/{slug}/analytics/executive-report.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/implement-attribution-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/` sem template correspondente em `workspace/_templates/analytics/`.
- Relatórios em `docs/data/{slug}/` são complementares e não substituem artefatos canônicos.

---

## Objetivo

Entender quais canais/fontes trazem e convertem clientes de maior valor.

> "A maioria das empresas está data-rich e insight-poor. Não faltam dados, faltam decisões."
> — Avinash Kaushik

---

## Regra de Ouro

**Attribution deve informar decisões de alocação de budget.**
- Se um número não muda uma decisão, é ruído.
- Não apenas "quantos clientes" mas "quanto CLV cada fonte gera".

---

## Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINIR OBJETIVO (Kaushik + Fader) - Tier 0             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Que decisão será informada? (Kaushik - DMMM)                  │
│   └── "Onde investir mais em marketing?"                        │
│   └── "Qual canal desligar?"                                    │
│   └── "Quanto vale cada fonte?"                                 │
│                                                                  │
│ □ Conectar com valor do cliente (Fader)                         │
│   └── Não apenas "quantos clientes"                             │
│   └── Mas "quanto CLV cada fonte gera"                          │
│   └── View: v_customer_lifetime_value                           │
│                                                                  │
│ □ Mapear fontes a rastrear                                      │
│   └── Paid (Google, Meta, etc)                                  │
│   └── Organic (SEO, Direct)                                     │
│   └── Referral (indicações) ← foco principal                    │
│   └── Social (orgânico)                                         │
│   └── Events/Webinars                                           │
│   └── Email marketing                                           │
│                                                                  │
│ □ Criar DMMM mapping                                            │
│   └── Business Objective: Ex. "Aumentar receita 20%"            │
│   └── Goals: Ex. "Aumentar aquisição", "Aumentar CLV"           │
│   └── KPIs: Ex. "CAC", "CLV/CAC ratio", "Conversion rate"       │
│   └── Targets: Ex. "CLV/CAC > 3:1"                              │
│   └── Segments: Ex. "Novos via Referral"                        │
│                                                                  │
│ OUTPUT: Lista de fontes + pergunta que attribution responde     │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Decisões a informar documentadas                              │
│ □ CLV integration planejada                                     │
│ □ Fontes mapeadas                                               │
│ □ DMMM framework preenchido                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: IMPLEMENTAR MODELOS (Kaushik) - Tier 1                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ First-Touch Attribution                                       │
│   └── "O que trouxe o cliente inicialmente?"                    │
│   └── Campo: first_touch_source                                 │
│   └── Uso: Otimizar awareness/discovery                         │
│   └── Query: Primeira interação registrada                      │
│                                                                  │
│ □ Last-Touch Attribution                                        │
│   └── "O que converteu o cliente?"                              │
│   └── Campo: last_touch_source                                  │
│   └── Uso: Otimizar conversão                                   │
│   └── Query: Última interação antes da compra                   │
│                                                                  │
│ □ Position-Based (40/20/40)                                     │
│   └── 40% crédito para first-touch                              │
│   └── 20% distribuído entre touchpoints do meio                 │
│   └── 40% crédito para last-touch                               │
│   └── Uso: Balanço entre discovery e close                      │
│                                                                  │
│ □ Linear Attribution                                            │
│   └── Crédito igual para todos touchpoints                      │
│   └── Uso: Jornadas longas e complexas                          │
│                                                                  │
│ □ Comparação First vs Last                                      │
│   └── Se muito diferentes = jornada longa                       │
│   └── Se iguais = jornada curta                                 │
│   └── Insight: Onde focar otimização                            │
│                                                                  │
│ OUTPUT: Modelos de attribution implementados                    │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ First-touch calculado                                         │
│ □ Last-touch calculado                                          │
│ □ Position-based implementado                                   │
│ □ Comparação first vs last documentada                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: REFERRAL ATTRIBUTION (Sean Ellis) - Tier 1              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Rastrear cadeia de indicação                                  │
│   └── Quem indicou quem?                                        │
│   └── Campo: referred_by_mind_id                                │
│   └── Depth: Até 3 níveis de indicação                          │
│                                                                  │
│ □ Calcular Viral Coefficient (K)                                │
│   └── K = Invites × Conversion Rate                             │
│   └── Meta: K > 0.5 (cada 100 trazem 50)                        │
│   └── Ideal: K > 1.0 (crescimento exponencial)                  │
│                                                                  │
│ □ Medir qualidade de referrals                                  │
│   └── CLV de indicados vs outros canais                         │
│   └── Retention de indicados vs outros                          │
│   └── Completion rate de indicados vs outros                    │
│   └── View: v_rfm_customer_classification por source            │
│                                                                  │
│ □ Otimizar programa de referral                                 │
│   └── Quando pedir indicação? (timing pós-completion)           │
│   └── Qual incentivo funciona? (A/B test)                       │
│   └── Qual mensagem converte? (copy testing)                    │
│                                                                  │
│ OUTPUT: Referral como canal otimizado e rastreado               │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Cadeia de indicação rastreável                                │
│ □ Viral coefficient calculado                                   │
│ □ Comparação CLV referral vs outros                             │
│ □ Timing de ask otimizado                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: REPORTING (Kaushik - So What) - Tier 2                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Report mensal de Attribution                                  │
│   └── SO WHAT: "Referral traz 40% dos clientes com 2x CLV"      │
│   └── WHAT CHANGED: "Paid caiu 20% em eficiência"               │
│   └── WHY: "Saturação de audiência no Meta"                     │
│   └── NOW WHAT: "Mover 30% budget de Paid → Referral program"   │
│                                                                  │
│ □ Attribution por CLV (Fader contribution)                      │
│   └── Não só "fonte trouxe 100 clientes"                        │
│   └── Mas "fonte trouxe R$500K em CLV"                          │
│   └── Tabela: Source | Customers | Total CLV | Avg CLV          │
│                                                                  │
│ □ See-Think-Do-Care mapping                                     │
│   └── SEE: First-touch sources (awareness)                      │
│   └── THINK: Engagement sources (consideration)                 │
│   └── DO: Last-touch sources (conversion)                       │
│   └── CARE: Referral sources (loyalty)                          │
│                                                                  │
│ □ Recomendações de alocação                                     │
│   └── Budget por canal baseado em CLV/CAC                       │
│   └── Channels to scale vs cut                                  │
│   └── Experimentos recomendados                                 │
│                                                                  │
│ OUTPUT: Report que gera decisão de alocação                     │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ So What framework aplicado                                    │
│ □ CLV attribution calculado                                     │
│ □ STDC mapping completo                                         │
│ □ Recomendações acionáveis                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## DMMM Template

```yaml
dmmm:
  business_objective: "Aumentar receita da Academia em 25% em 2026"

  goals:
    - goal: "Aumentar aquisição de alunos"
      kpi: "Novos alunos/mês"
      target: "500 → 750"
      segment: "Vindos de indicação"

    - goal: "Melhorar qualidade da aquisição"
      kpi: "Avg CLV por fonte"
      target: "CLV médio > R$2.000"
      segment: "Todos os canais"

    - goal: "Aumentar eficiência"
      kpi: "CLV/CAC ratio"
      target: "> 3:1"
      segment: "Paid channels"
```

---

## Queries de Attribution

```sql
-- Attribution por fonte (simplificado)
-- Nota: Requer campo first_touch_source na tabela de leads/transactions

-- CLV total por fonte de aquisição (se houver campo source)
SELECT
    t.metadata->>'source' AS acquisition_source,
    COUNT(DISTINCT t.mind_id) AS customers,
    SUM(clv.historical_clv_brl) AS total_clv_brl,
    AVG(clv.historical_clv_brl) AS avg_clv_brl,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY clv.historical_clv_brl) AS median_clv_brl
FROM transactions t
JOIN v_customer_lifetime_value clv ON clv.mind_id = t.mind_id
WHERE t.metadata->>'source' IS NOT NULL
GROUP BY t.metadata->>'source'
ORDER BY total_clv_brl DESC;

-- Comparação RFM por segmento de aquisição
SELECT
    segment,
    COUNT(*) AS customers,
    AVG(rfm_weighted_score) AS avg_rfm_score,
    AVG(total_spent_brl) AS avg_spent
FROM v_rfm_customer_classification
GROUP BY segment
ORDER BY avg_spent DESC;
```

---

## Checklist de Completude

```yaml
fase_1_objetivo:
  - [ ] Decisões a informar listadas
  - [ ] CLV integration planejada
  - [ ] Fontes mapeadas
  - [ ] DMMM framework preenchido

fase_2_modelos:
  - [ ] First-touch attribution implementado
  - [ ] Last-touch attribution implementado
  - [ ] Position-based (40/20/40) implementado
  - [ ] Comparação first vs last documentada

fase_3_referral:
  - [ ] Cadeia de indicação rastreável
  - [ ] Viral coefficient calculado
  - [ ] CLV comparativo por fonte
  - [ ] Timing otimizado

fase_4_reporting:
  - [ ] So What framework aplicado
  - [ ] CLV attribution report
  - [ ] STDC mapping completo
  - [ ] Recomendações de budget
  - [ ] Stakeholders treinados
```

---

## Referências

- **Avinash Kaushik**: DMMM, So What Framework, See-Think-Do-Care
- **Sean Ellis**: Viral Coefficient, AARRR, Referral optimization
- **Peter Fader**: CLV-weighted attribution
- **Template**: `templates/attribution-report-tmpl.yaml`
- **Template**: `templates/dmmm-tmpl.yaml`

---

*Data Intelligence Pack - Workflow v1.0*
*Primary Agent: @avinash-kaushik*
