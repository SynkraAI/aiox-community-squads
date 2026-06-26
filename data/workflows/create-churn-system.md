# Workflow: Create Churn Prevention System

## Metadata

```yaml
workflow:
  id: create-churn-system
  name: "Create Churn Alert & Prevention System"
  version: "1.0"
  primary_agent: nick-mehta
  tier_flow: [0, 1, 2]
  phases: 3
  estimated_duration: "2-3 weeks"

  agents_involved:
    - nick-mehta      # Primary - Churn signals and playbooks
    - peter-fader     # Tier 0 - Prioritization by CLV
    - david-spinks    # Tier 1 - Community drop signals
    - wes-kao         # Tier 1 - Learning stall signals

  views_required:
    - v_churn_risk_scores
    - v_churn_leading_indicators
    - v_customer_health_composite
    - v_customer_lifetime_value

  templates_used:
    - churn-alert-tmpl.yaml
    - health-score-report-tmpl.yaml

  checklists_used:
    - health-score-checklist.md
    - pre-implementation-checklist.md

  deliverables:
    - Churn risk scoring system
    - Leading indicator detection
    - Alert triggers
    - Playbooks by signal type
    - Escalation paths
```

---

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, signal-design, interventions, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: signal-design
    - trigger: signals_defined
      source: signal-design
      dest: interventions
    - trigger: playbooks_ready
      source: interventions
      dest: complete
task_ref:
  primary:
    - predict-churn
  supporting:
    - design-health-score
    - calculate-clv
    - measure-community
    - design-learning-outcomes
```

## Workspace Execution Contract

### Preflight (obrigatório)

1. `*workspace-preflight` (executa `bootstrap-data-workspace.sh` + `validate-data-essentials.sh`)
2. `*workspace-context {slug}`
3. Confirmar templates necessários em `workspace/_templates/analytics/`

### Output Routing

- **Canonical (template-first):**
  - `workspace/businesses/{slug}/analytics/churn-alert.yaml`
  - `workspace/businesses/{slug}/analytics/health-score-report.yaml`
  - `workspace/businesses/{slug}/analytics/executive-report.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/create-churn-system-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/` sem template correspondente em `workspace/_templates/analytics/`.
- Relatórios em `docs/data/{slug}/` são complementares e não substituem artefatos canônicos.

---

## Objetivo

Identificar clientes em risco antes do churn e acionar intervenção apropriada.

> "Customer Success é quando seus clientes atingem o resultado desejado através das interações com sua empresa."
> — Nick Mehta

---

## Regra de Ouro

**Priorizar por valor, não por volume.**
- Clientes de alto CLV = prioridade máxima
- Clientes de baixo CLV = prioridade menor (automação)

---

## Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINIR SINAIS (Nick Mehta + Fader) - Tier 0            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Mapear leading indicators de churn                            │
│   └── Login drop >50% (Mehta)                                   │
│   └── Support ticket crítico (Mehta)                            │
│   └── Champion deixou empresa (Mehta)                           │
│   └── Community drop >60% MoM (Spinks)                          │
│   └── Course stall >7 dias (Kao)                                │
│                                                                  │
│ □ Priorizar por CLV em risco (Fader)                            │
│   └── View: v_customer_lifetime_value                           │
│   └── Clientes de alto CLV = prioridade máxima                  │
│   └── Clientes de baixo CLV = prioridade menor                  │
│                                                                  │
│ □ Definir severidade                                            │
│   └── Critical: múltiplos sinais + alto CLV                     │
│   └── High: 1 sinal forte + alto CLV                            │
│   └── Medium: sinais moderados                                  │
│   └── Low: sinais fracos ou baixo CLV                           │
│                                                                  │
│ OUTPUT: Lista de tipos de alerta com severidade                 │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Leading indicators documentados                               │
│ □ Priorização por CLV definida                                  │
│ □ Matriz de severidade criada                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: CRIAR ALERTAS (Nick Mehta + Especialistas) - Tier 1    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ ALERTA: INACTIVITY                                            │
│   └── Trigger: 14 dias sem login/interação                      │
│   └── View: days_since_last_interaction > 14                    │
│   └── Severidade: baseada em CLV tier                           │
│   └── Ação: Email automático + task para CS                     │
│                                                                  │
│ □ ALERTA: HEALTH_DROP                                           │
│   └── Trigger: Health Score caiu >20 pontos em 30 dias          │
│   └── View: v_churn_risk_scores.low_health_risk                 │
│   └── Severidade: High se CLV > median                          │
│   └── Ação: CS Manager outreach                                 │
│                                                                  │
│ □ ALERTA: MEETING_RISK                                          │
│   └── Trigger: Renewal em <30 dias + health <50                 │
│   └── Severidade: Critical                                      │
│   └── Ação: Prep call + escalation                              │
│                                                                  │
│ □ ALERTA: COMMUNITY_DROP (com Spinks)                           │
│   └── Trigger: Participação caiu >60% mês-a-mês                 │
│   └── View: messages_30d = 0 AND previous > 5                   │
│   └── Severidade: Medium                                        │
│   └── Ação: Outreach personalizado + invite para evento         │
│                                                                  │
│ □ ALERTA: LEARNING_STALL (com Kao)                              │
│   └── Trigger: 7+ dias sem progresso no curso                   │
│   └── Severidade: Medium                                        │
│   └── Ação: Nudge automático + oferta de suporte                │
│                                                                  │
│ □ ALERTA: STREAK_BROKEN                                         │
│   └── Trigger: Streak quebrado após 7+ dias                     │
│   └── View: current_streak = 0 AND previous > 7                 │
│   └── Severidade: Low-Medium                                    │
│   └── Ação: Gamification nudge + re-engagement                  │
│                                                                  │
│ OUTPUT: Sistema de alertas funcionando                          │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Todos os alertas definidos                                    │
│ □ Triggers implementados em views                               │
│ □ Severidades mapeadas                                          │
│ □ Ações automáticas configuradas                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: PLAYBOOKS DE AÇÃO (Nick Mehta) - Tier 2                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ PLAYBOOK: Inactivity Response                                 │
│   └── Dia 1: Email automático "Sentimos sua falta"              │
│   └── Dia 3: Task para CS ligar                                 │
│   └── Dia 7: Email do founder/CEO                               │
│   └── Dia 14: Escalation para manager                           │
│   └── Dia 30: Oferta especial de reativação                     │
│                                                                  │
│ □ PLAYBOOK: Health Drop Response                                │
│   └── Imediato: Análise de root cause                           │
│   └── 24h: Call do CS Manager                                   │
│   └── 48h: Plano de ação documentado                            │
│   └── 7 dias: Follow-up de progresso                            │
│                                                                  │
│ □ PLAYBOOK: Meeting Risk Prep                                   │
│   └── -30 dias: Review completo da conta                        │
│   └── -14 dias: Call de alignment interno                       │
│   └── -7 dias: Prep de save offers                              │
│   └── Meeting: Executar save playbook                           │
│   └── +1 dia: Documentar outcome                                │
│                                                                  │
│ □ PLAYBOOK: Community Re-engagement                             │
│   └── Dia 1: Personal message do community manager              │
│   └── Dia 3: Invite para próximo evento                         │
│   └── Dia 7: Highlight de conteúdo relevante                    │
│   └── Dia 14: 1:1 call se alto CLV                              │
│                                                                  │
│ □ PLAYBOOK: Learning Nudge                                      │
│   └── Dia 1: Email com próximo passo claro                      │
│   └── Dia 3: Oferta de office hours                             │
│   └── Dia 7: Buddy match (peer support)                         │
│   └── Dia 14: Call do success team                              │
│                                                                  │
│ □ Métricas de efetividade                                       │
│   └── % alertas que viraram ação                                │
│   └── % ações que evitaram churn                                │
│   └── $ saved por alerta                                        │
│   └── Time to action (SLA)                                      │
│                                                                  │
│ OUTPUT: Playbooks documentados + métricas de tracking           │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Playbooks documentados                                        │
│ □ SLAs definidos por severidade                                 │
│ □ Métricas de efetividade implementadas                         │
│ □ Equipe treinada                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Matriz de Severidade

| Signal Count | CLV Tier | Severidade | SLA |
|--------------|----------|------------|-----|
| 3+ | Platinum/Gold | Critical | <4h |
| 2+ | Platinum/Gold | High | <24h |
| 3+ | Silver/Bronze | High | <24h |
| 2+ | Silver/Bronze | Medium | <48h |
| 1 | Any | Low | <7d |

---

## Queries de Monitoramento

```sql
-- Clientes com maior risco de churn
SELECT
    mind_slug,
    mind_name,
    churn_risk_score,
    risk_category,
    urgency,
    primary_signal,
    recommended_playbook
FROM v_churn_leading_indicators
WHERE churn_risk_score >= 60
ORDER BY churn_risk_score DESC
LIMIT 20;

-- Distribuição de risco
SELECT
    risk_category,
    COUNT(*) as customers,
    ROUND(AVG(churn_risk_score)) as avg_risk
FROM v_churn_risk_scores
GROUP BY risk_category
ORDER BY avg_risk DESC;

-- Alertas críticos com CLV
SELECT
    cli.mind_slug,
    cli.churn_risk_score,
    cli.primary_signal,
    clv.historical_clv_brl,
    clv.clv_tier
FROM v_churn_leading_indicators cli
JOIN v_customer_lifetime_value clv ON clv.mind_id = cli.mind_id
WHERE cli.risk_category = 'High Risk'
  AND clv.clv_tier IN ('Platinum', 'Gold')
ORDER BY clv.historical_clv_brl DESC;
```

---

## Checklist de Completude

```yaml
fase_1_sinais:
  - [ ] Leading indicators de Mehta documentados
  - [ ] Community signals de Spinks integrados
  - [ ] Learning signals de Kao integrados
  - [ ] Priorização por CLV implementada
  - [ ] Matriz de severidade criada

fase_2_alertas:
  - [ ] INACTIVITY alert configurado
  - [ ] HEALTH_DROP alert configurado
  - [ ] MEETING_RISK alert configurado
  - [ ] COMMUNITY_DROP alert configurado
  - [ ] LEARNING_STALL alert configurado
  - [ ] STREAK_BROKEN alert configurado
  - [ ] Automações implementadas

fase_3_playbooks:
  - [ ] Inactivity Response playbook documentado
  - [ ] Health Drop Response playbook documentado
  - [ ] Meeting Risk Prep playbook documentado
  - [ ] Community Re-engagement playbook documentado
  - [ ] Learning Nudge playbook documentado
  - [ ] SLAs por severidade definidos
  - [ ] Métricas de efetividade implementadas
  - [ ] Equipe treinada

go_live:
  - [ ] Views em produção
  - [ ] Alertas disparando
  - [ ] Playbooks acessíveis
  - [ ] Dashboard de monitoramento
  - [ ] Report semanal configurado
```

---

## Referências

- **Nick Mehta**: DEAR Framework, Churn Signals, Customer Success
- **Peter Fader**: CLV-based prioritization
- **David Spinks**: Community engagement signals
- **Wes Kao**: Learning completion signals
- **Template**: `templates/churn-alert-tmpl.yaml`

---

*Data Intelligence Pack - Workflow v1.0*
*Primary Agent: @nick-mehta*
