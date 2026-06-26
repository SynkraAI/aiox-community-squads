# Workflow: Optimize Community

## Metadata

```yaml
workflow:
  id: optimize-community-workflow
  name: "Otimizar Comunidade"
  version: "1.0"
  primary_agent: david-spinks
  tier_flow: [1, 1, 1, 2]
  phases: 4
  estimated_duration: "2-3 weeks"

  agents_involved:
    - david-spinks   # Tier 1 - Community strategy and metrics
    - nick-mehta     # Tier 1 - Health Score integration
    - wes-kao        # Tier 1 - Learning community design
    - avinash-kaushik # Tier 2 - Reporting and ROI

  views_required:
    - v_community_stats
    - v_community_members
    - v_community_ranking
    - v_customer_health_composite

  templates_used:
    - community-health-tmpl.yaml
    - executive-report-tmpl.yaml

  checklists_used:
    - community-health-checklist.md
    - so-what-checklist.md

  deliverables:
    - SPACES assessment
    - Community health score
    - Engagement programs
    - ROI metrics
    - Action plan
```

---

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, diagnosis, programs, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: diagnosis
    - trigger: diagnosis_complete
      source: diagnosis
      dest: programs
    - trigger: community_plan_ready
      source: programs
      dest: complete
task_ref:
  primary:
    - measure-community
  supporting:
    - design-health-score
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
  - `workspace/businesses/{slug}/analytics/community-health.yaml`
  - `workspace/businesses/{slug}/analytics/executive-report.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/optimize-community-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/` sem template correspondente em `workspace/_templates/analytics/`.
- Relatórios em `docs/data/{slug}/` são complementares e não substituem artefatos canônicos.

---

## Objetivo

Diagnosticar saúde da comunidade e criar plano de otimização para aumentar engajamento, pertencimento e valor entregue aos membros.

> "Community is not about transactions - it's about transformation. Members should feel they belong to something bigger than themselves."
> — David Spinks, The Business of Belonging

---

## Regra de Ouro

**Nunca otimize comunidade sem responder:**
1. Por que membros deveriam participar? (Proposta de valor)
2. Como medimos se a comunidade está saudável? (Métricas)
3. Que comportamentos queremos incentivar? (Programas)
4. Qual o ROI de investir em comunidade? (Negócio)

---

## Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DIAGNÓSTICO SPACES (David Spinks) - Tier 1              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Avaliar cada dimensão do SPACES Model                         │
│                                                                  │
│   S - SUPPORT                                                   │
│   └── Membros se ajudam mutuamente?                             │
│   └── Tempo médio de resposta a perguntas                       │
│   └── % de perguntas respondidas por membros                    │
│   └── Score: ___/10                                             │
│                                                                  │
│   P - PRODUCT                                                   │
│   └── Comunidade influencia o produto?                          │
│   └── Feature requests da comunidade implementados              │
│   └── Beta testers ativos                                       │
│   └── Score: ___/10                                             │
│                                                                  │
│   A - ACQUISITION                                               │
│   └── Comunidade atrai novos clientes?                          │
│   └── Referrals originados da comunidade                        │
│   └── Conteúdo UGC que atrai tráfego                            │
│   └── Score: ___/10                                             │
│                                                                  │
│   C - CONTRIBUTION                                              │
│   └── Membros criam conteúdo/valor?                             │
│   └── Posts, templates, recursos compartilhados                 │
│   └── Membros que viraram mentores/embaixadores                 │
│   └── Score: ___/10                                             │
│                                                                  │
│   E - ENGAGEMENT                                                │
│   └── Membros participam ativamente?                            │
│   └── DAU/MAU ratio (stickiness)                                │
│   └── Eventos attendance rate                                   │
│   └── Score: ___/10                                             │
│                                                                  │
│   S - SUCCESS                                                   │
│   └── Membros atingem seus objetivos?                           │
│   └── Outcomes alcançados via comunidade                        │
│   └── NPS da comunidade                                         │
│   └── Score: ___/10                                             │
│                                                                  │
│ OUTPUT: SPACES assessment com scores + gaps identificados       │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Todas 6 dimensões avaliadas                                   │
│ □ Scores atribuídos com evidências                              │
│ □ Top 2-3 gaps priorizados                                      │
│ □ Quick wins identificados                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: INTEGRAÇÃO COM HEALTH (Nick Mehta) - Tier 1             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Correlacionar community engagement com Health Score           │
│   └── Membros ativos têm health mais alto?                      │
│   └── Participação em eventos → menor churn?                    │
│   └── Quantificar impacto no DEAR framework                     │
│                                                                  │
│ □ Definir Community Health Score                                │
│   └── Participation rate (peso: 30%)                            │
│   └── Contribution rate (peso: 25%)                             │
│   └── Response rate (peso: 20%)                                 │
│   └── Event attendance (peso: 15%)                              │
│   └── Referral rate (peso: 10%)                                 │
│                                                                  │
│ □ Criar alertas de community churn                              │
│   └── Membro ativo que parou de participar                      │
│   └── Contributor que parou de contribuir                       │
│   └── Evento host que cancelou                                  │
│                                                                  │
│ □ Mapear playbooks por status                                   │
│   └── New member → Onboarding sequence                          │
│   └── Active → Nurture para contributor                         │
│   └── Contributor → Nurture para ambassador                     │
│   └── At risk → Re-engagement campaign                          │
│                                                                  │
│ OUTPUT: Community Health Score + alertas + playbooks            │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Correlação community ↔ health documentada                     │
│ □ Community Health Score definido                               │
│ □ Alertas configurados                                          │
│ □ Playbooks por estágio criados                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: PROGRAMAS DE ENGAJAMENTO (Wes Kao) - Tier 1             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Desenhar programa de onboarding                               │
│   └── First 7 days experience                                   │
│   └── Buddy system / welcome committee                          │
│   └── Quick win activities                                      │
│   └── Activation milestones claros                              │
│                                                                  │
│ □ Criar calendar de programação                                 │
│   └── Eventos regulares (weekly, monthly)                       │
│   └── Mix de formatos (live, async, challenge)                  │
│   └── Owners/hosts para cada programa                           │
│   └── Aplicar Course Mechanics Canvas                           │
│                                                                  │
│ □ Implementar gamification                                      │
│   └── Badges/achievements                                       │
│   └── Leaderboards (cuidado com competição tóxica)              │
│   └── Streaks e recompensas                                     │
│   └── Member spotlights                                         │
│                                                                  │
│ □ Estruturar path de membro                                     │
│   └── Newcomer → Active → Contributor → Ambassador              │
│   └── Critérios claros para cada nível                          │
│   └── Benefícios progressivos                                   │
│   └── Recognition program                                       │
│                                                                  │
│ OUTPUT: Programas desenhados + calendar + member journey        │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Onboarding program criado                                     │
│ □ Calendar de 3 meses definido                                  │
│ □ Gamification implementada                                     │
│ □ Member path documentado                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: ROI E REPORT (Avinash Kaushik) - Tier 2                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Calcular ROI da comunidade                                    │
│   └── Support deflection (tickets evitados)                     │
│   └── Acquisition value (referrals, leads)                      │
│   └── Retention impact (churn evitado)                          │
│   └── Content value (UGC, knowledge base)                       │
│   └── Product value (feedback, beta testing)                    │
│                                                                  │
│ □ Criar Community Dashboard                                     │
│   └── SPACES scores over time                                   │
│   └── Member growth and engagement                              │
│   └── Top contributors                                          │
│   └── ROI metrics                                               │
│                                                                  │
│ □ Aplicar So What Framework                                     │
│   └── SO WHAT: "Membros ativos têm 40% menos churn"             │
│   └── WHAT CHANGED: "Engagement caiu 15% este mês"              │
│   └── WHY: "Menos eventos, holidays"                            │
│   └── NOW WHAT: "Janeiro: campaign de re-engagement"            │
│                                                                  │
│ □ Definir OKRs de comunidade                                    │
│   └── Objective: Comunidade como diferencial competitivo        │
│   └── KR1: DAU/MAU > 30%                                        │
│   └── KR2: NPS comunidade > 50                                  │
│   └── KR3: 20% de clientes ativos na comunidade                 │
│                                                                  │
│ OUTPUT: ROI calculado + dashboard + OKRs                        │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ ROI quantificado em $                                         │
│ □ Dashboard funcional                                           │
│ □ So What em cada métrica                                       │
│ □ OKRs definidos e aceitos                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Queries de Validação

```sql
-- Community stats overview
SELECT
    COUNT(DISTINCT mind_id) AS total_members,
    COUNT(DISTINCT CASE WHEN last_activity > NOW() - INTERVAL '30 days' THEN mind_id END) AS active_30d,
    COUNT(DISTINCT CASE WHEN last_activity > NOW() - INTERVAL '7 days' THEN mind_id END) AS active_7d,
    ROUND(COUNT(DISTINCT CASE WHEN last_activity > NOW() - INTERVAL '7 days' THEN mind_id END)::NUMERIC /
          NULLIF(COUNT(DISTINCT CASE WHEN last_activity > NOW() - INTERVAL '30 days' THEN mind_id END), 0) * 100, 1) AS stickiness
FROM v_community_members;

-- Top contributors
SELECT
    mind_slug,
    mind_name,
    messages_count,
    events_hosted,
    contributions_count,
    member_since
FROM v_community_ranking
ORDER BY contributions_count DESC
LIMIT 20;

-- Correlação community → health
SELECT
    CASE
        WHEN cm.messages_30d >= 10 THEN 'High engagement'
        WHEN cm.messages_30d >= 5 THEN 'Medium engagement'
        WHEN cm.messages_30d >= 1 THEN 'Low engagement'
        ELSE 'No engagement'
    END AS engagement_level,
    ROUND(AVG(h.health_score), 1) AS avg_health_score,
    COUNT(*) AS members
FROM v_customer_health_composite h
LEFT JOIN (
    SELECT sender_mind_id AS mind_id, COUNT(*) AS messages_30d
    FROM messages
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY sender_mind_id
) cm ON cm.mind_id = h.mind_id
GROUP BY 1
ORDER BY avg_health_score DESC;

-- Event attendance trends
SELECT
    DATE_TRUNC('month', e.starts_at) AS month,
    COUNT(DISTINCT e.id) AS events,
    SUM(e.rsvp_count) AS total_rsvps,
    ROUND(AVG(e.rsvp_count), 1) AS avg_rsvps_per_event
FROM events e
WHERE e.starts_at > NOW() - INTERVAL '6 months'
GROUP BY 1
ORDER BY 1 DESC;
```

---

## SPACES Quick Assessment Template

```yaml
spaces_assessment:
  date: "YYYY-MM-DD"
  assessor: "@david-spinks"

  support:
    score: _/10
    evidence:
      - "X% perguntas respondidas por membros"
      - "Tempo médio resposta: X horas"
    gap: ""
    action: ""

  product:
    score: _/10
    evidence:
      - "X features originadas da comunidade"
      - "X beta testers ativos"
    gap: ""
    action: ""

  acquisition:
    score: _/10
    evidence:
      - "X% clientes vieram via comunidade"
      - "X referrals no mês"
    gap: ""
    action: ""

  contribution:
    score: _/10
    evidence:
      - "X contribuidores ativos"
      - "X peças de UGC no mês"
    gap: ""
    action: ""

  engagement:
    score: _/10
    evidence:
      - "DAU/MAU: X%"
      - "Event attendance: X%"
    gap: ""
    action: ""

  success:
    score: _/10
    evidence:
      - "NPS comunidade: X"
      - "X outcomes reportados"
    gap: ""
    action: ""

  total_score: _/60
  priority_gaps:
    1: ""
    2: ""
    3: ""
```

---

## Checklist de Completude

```yaml
pre_implementation:
  - [ ] Acesso aos dados de comunidade garantido
  - [ ] Stakeholders de community identificados
  - [ ] Baseline metrics coletadas
  - [ ] Budget para programas definido

fase_1_diagnostico:
  - [ ] SPACES assessment completo
  - [ ] Scores com evidências
  - [ ] Gaps priorizados
  - [ ] Quick wins listados

fase_2_health:
  - [ ] Correlação community ↔ health medida
  - [ ] Community Health Score definido
  - [ ] Alertas de churn configurados
  - [ ] Playbooks por estágio criados

fase_3_programas:
  - [ ] Onboarding program desenhado
  - [ ] Calendar de 3 meses criado
  - [ ] Gamification implementada
  - [ ] Member path documentado

fase_4_roi:
  - [ ] ROI calculado
  - [ ] Dashboard criado
  - [ ] So What aplicado
  - [ ] OKRs definidos

go_live:
  - [ ] Programas lançados
  - [ ] Métricas sendo coletadas
  - [ ] Team ownership definido
  - [ ] Cadência de revisão acordada
```

---

## Referências

- **David Spinks**: "The Business of Belonging", SPACES Model
- **Nick Mehta**: Community as CS channel, Health Score integration
- **Wes Kao**: Cohort community design, Engagement programs
- **Avinash Kaushik**: So What Framework, ROI measurement
- **CMX**: Community Industry Report, Benchmarks
- **Template**: `templates/community-health-tmpl.yaml`
- **Checklist**: `checklists/community-health-checklist.md`

---

*Data Intelligence Pack - Workflow v1.0*
*Primary Agent: @david-spinks | Secondary: @nick-mehta, @wes-kao, @avinash-kaushik*
