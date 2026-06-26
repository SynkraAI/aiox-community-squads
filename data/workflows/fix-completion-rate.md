# Workflow: Fix Completion Rate (3% → 80%)

## Metadata

```yaml
workflow:
  id: fix-completion-rate
  name: "Transform Course Completion Rate"
  version: "1.0"
  primary_agent: wes-kao
  tier_flow: [0, 1, 2]
  phases: 5
  estimated_duration: "4-8 weeks"

  agents_involved:
    - wes-kao         # Primary - CBC methodology, learning design
    - david-spinks    # Community elements
    - nick-mehta      # Student health monitoring
    - avinash-kaushik # Metrics and reporting

  views_required:
    - v_learning_completion_rate (Sprint 2)
    - v_learning_progression_tracking (Sprint 2)
    - v_customer_health_composite
    - v_cohort_retention_matrix (Sprint 2)

  templates_used:
    - learning-outcomes-tmpl.yaml
    - community-health-tmpl.yaml

  checklists_used:
    - cbc-readiness-checklist.md
    - community-health-checklist.md

  deliverables:
    - Diagnóstico de drop-off points
    - Redesign para CBC model
    - Community integration plan
    - Student Health Score
    - Metrics dashboard
    - Pilot validation
```

---

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, redesign, pilot-validation, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: redesign
    - trigger: redesign_complete
      source: redesign
      dest: pilot-validation
    - trigger: pilot_validated
      source: pilot-validation
      dest: complete
task_ref:
  primary:
    - design-learning-outcomes
  supporting:
    - analyze-cohort
    - design-health-score
    - measure-community
    - create-dashboard
```

## Workspace Execution Contract

### Preflight (obrigatório)

1. `*workspace-preflight` (executa `bootstrap-data-workspace.sh` + `validate-data-essentials.sh`)
2. `*workspace-context {slug}`
3. Confirmar templates necessários em `workspace/_templates/analytics/`

### Output Routing

- **Canonical (template-first):**
  - `workspace/businesses/{slug}/analytics/learning-outcomes.yaml`
  - `workspace/businesses/{slug}/analytics/community-health.yaml`
  - `workspace/businesses/{slug}/analytics/executive-report.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/fix-completion-rate-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/` sem template correspondente em `workspace/_templates/analytics/`.
- Relatórios em `docs/data/{slug}/` são complementares e não substituem artefatos canônicos.

---

## Objetivo

Transformar curso com 3% completion em programa com 80%+ usando metodologia Cohort-Based Course (CBC).

> "Completion rate de MOOCs é 6%. Cohort-based courses chegam a 96%. A diferença é design, não conteúdo."
> — Wes Kao

---

## Contexto do Problema

```
MOOC (3% completion):
- Self-paced (sem urgência)
- Sozinho (sem accountability)
- Passivo (assistir vídeos)
- Baixo commitment ($20-50)

CBC Target (80%+ completion):
- Fixed timeline (urgência)
- Cohort (accountability social)
- Ativo (projetos, discussões)
- High commitment ($500-5000)
```

---

## Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DIAGNÓSTICO (Wes Kao) - Tier 0                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Identificar onde drop acontece                                │
│   └── Quantos nunca começam? (0% progress)                      │
│   └── Quantos param no módulo 1?                                │
│   └── Quantos param no meio?                                    │
│   └── Quantos param quase no fim?                               │
│   └── Query: v_learning_progression_tracking                    │
│                                                                  │
│ □ Identificar causa do drop                                     │
│   └── Falta de urgência (sem deadline)                          │
│   └── Falta de accountability (sozinho)                         │
│   └── Falta de engajamento (vídeo passivo)                      │
│   └── Falta de commitment (preço baixo)                         │
│   └── Conteúdo muito longo/complexo                             │
│   └── Momento errado (comprou mas não era hora)                 │
│                                                                  │
│ □ Survey com quem dropou                                        │
│   └── "Por que você parou?"                                     │
│   └── "O que faria você continuar?"                             │
│   └── "Qual foi seu maior obstáculo?"                           │
│   └── "Você pretende voltar? Quando?"                           │
│                                                                  │
│ □ Analisar quem completa                                        │
│   └── Perfil demográfico                                        │
│   └── Comportamento pré-curso                                   │
│   └── Padrões de engajamento                                    │
│   └── O que eles têm em comum?                                  │
│                                                                  │
│ OUTPUT: Diagnóstico claro com root causes                       │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Funnel de drop mapeado                                        │
│ □ Top 3 causas identificadas                                    │
│ □ Survey realizado (min. 50 respostas)                          │
│ □ Perfil de "completers" documentado                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: REDESIGN (Wes Kao) - Tier 1                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Adicionar elementos de CBC                                    │
│   └── Fixed start/end dates (ex: 4 semanas)                     │
│   └── Cohort (turmas simultâneas, 20-50 alunos)                 │
│   └── Live sessions (ao menos 1/semana)                         │
│   └── Peer accountability (grupos de 4-5)                       │
│                                                                  │
│ □ Redesign de sessões (State Change Method)                     │
│   └── Alternar modalidades a cada 5-10 min                      │
│   └── Lecture → Chat → Poll → Breakout → Share → Q&A            │
│   └── Nunca mais de 15 min de lecture contínua                  │
│   └── Participação obrigatória (câmera on policy?)              │
│                                                                  │
│ □ Adicionar deliverables                                        │
│   └── Projeto prático obrigatório                               │
│   └── Peer feedback em cada módulo                              │
│   └── Showcase final (apresentação)                             │
│   └── Entregáveis semanais claros                               │
│                                                                  │
│ □ Redesign de conteúdo assíncrono                               │
│   └── Vídeos curtos (max 5 min)                                 │
│   └── Texto/leitura em vez de vídeo quando possível             │
│   └── Quiz de verificação após cada módulo                      │
│   └── Recursos downloadables (checklists, templates)            │
│                                                                  │
│ □ Revisar pricing e commitment                                  │
│   └── Preço mais alto = mais commitment                         │
│   └── Considerar R$500-2000 vs atual                            │
│   └── Payment plans disponíveis                                 │
│   └── Refund policy clara (7 dias? Nenhum?)                     │
│                                                                  │
│ OUTPUT: Novo design de curso documentado                        │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Elementos CBC definidos                                       │
│ □ State Change Method aplicado                                  │
│ □ Deliverables por semana listados                              │
│ □ Pricing strategy definida                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: COMMUNITY ELEMENTS (David Spinks) - Tier 1              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Criar comunidade do cohort                                    │
│   └── Slack/Discord privado do cohort                           │
│   └── Canais: #general, #dúvidas, #show-work                    │
│   └── Expectativa de participação diária                        │
│                                                                  │
│ □ Rituais de conexão                                            │
│   └── Intro posts no dia 1 (template)                           │
│   └── Daily check-in (como está se sentindo?)                   │
│   └── Weekly wins sharing                                       │
│   └── Celebration no final                                      │
│                                                                  │
│ □ Peer support structures                                       │
│   └── Study buddies (pares de accountability)                   │
│   └── Small groups (4-5 pessoas)                                │
│   └── Peer feedback obrigatório                                 │
│   └── Co-working sessions opcionais                             │
│                                                                  │
│ □ Alumni community                                              │
│   └── Graduados ajudam novos cohorts                            │
│   └── Networking contínuo                                       │
│   └── Eventos exclusivos                                        │
│   └── Job board/opportunities                                   │
│                                                                  │
│ □ Métricas SPACES                                               │
│   └── S - Support: Membros ajudando membros                     │
│   └── P - Product: Feedback coletado                            │
│   └── A - Acquisition: Referrals gerados                        │
│   └── C - Content: UGC criado                                   │
│   └── E - Engagement: Participação diária                       │
│   └── S - Success: Outcomes alcançados                          │
│                                                                  │
│ OUTPUT: Elementos de community integrados                       │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Comunidade do cohort configurada                              │
│ □ Rituais documentados                                          │
│ □ Peer structures definidas                                     │
│ □ Alumni program planejado                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: STUDENT HEALTH (Nick Mehta adaptado) - Tier 1           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Criar "Student Health Score"                                  │
│   └── Attendance (30%) - presença nas lives                     │
│   └── Assignment completion (30%) - entregas feitas             │
│   └── Community participation (20%) - posts/comments            │
│   └── Progress pace (20%) - on track vs behind                  │
│                                                                  │
│ □ Thresholds de Student Health                                  │
│   └── Verde (70-100): On track, engajado                        │
│   └── Amarelo (40-69): Precisa de nudge                         │
│   └── Vermelho (0-39): Intervenção urgente                      │
│                                                                  │
│ □ Sistema de alertas                                            │
│   └── 3 dias sem atividade → Nudge automático                   │
│   └── Faltou 1 live → Mensagem pessoal                          │
│   └── Faltou 2 lives → Call do team                             │
│   └── Assignment atrasado → Oferta de ajuda                     │
│   └── Health <40 → Escalation para instructor                   │
│                                                                  │
│ □ Playbooks de intervenção                                      │
│   └── Nudge: "Vimos que você não acessou, tudo bem?"            │
│   └── Check-in: "Como posso ajudar você a completar?"           │
│   └── Office hours: "Reservei 15 min para você"                 │
│   └── Buddy match: "Conectei você com [nome]"                   │
│                                                                  │
│ OUTPUT: Sistema de early warning para students                  │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Student Health Score definido                                 │
│ □ Alertas configurados                                          │
│ □ Playbooks documentados                                        │
│ □ Equipe treinada para intervenção                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 5: MÉTRICAS E ITERAÇÃO (Kao + Kaushik) - Tier 2            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Métricas de processo                                          │
│   └── Completion rate (meta: 80%)                               │
│   └── Attendance rate (meta: 85%)                               │
│   └── Assignment submission rate (meta: 90%)                    │
│   └── Community participation rate                              │
│   └── NPS (meta: 70+)                                           │
│                                                                  │
│ □ Métricas de outcome                                           │
│   └── % que atingiu objetivo declarado                          │
│   └── % que indicou após completar                              │
│   └── % que comprou próximo produto                             │
│   └── Salary/career improvement (se aplicável)                  │
│                                                                  │
│ □ Cohort pilot                                                  │
│   └── Tamanho: 20-30 alunos                                     │
│   └── Duração: 4-6 semanas                                      │
│   └── Feedback: Surveys semanais + final                        │
│   └── NPS e completion como gates                               │
│                                                                  │
│ □ Iteração pós-pilot                                            │
│   └── Analisar feedback intensivamente                          │
│   └── Identificar top 3 melhorias                               │
│   └── Ajustar antes de escalar                                  │
│   └── Documentar learnings                                      │
│                                                                  │
│ □ Reporting (Kaushik So What)                                   │
│   └── SO WHAT: "Completion subiu de 3% para 78%"                │
│   └── WHAT CHANGED: "Adicionamos CBC elements"                  │
│   └── WHY: "Accountability e deadlines funcionam"               │
│   └── NOW WHAT: "Escalar para todos os cursos"                  │
│                                                                  │
│ OUTPUT: Curso validado pronto para escala                       │
│                                                                  │
│ GATE CHECK:                                                     │
│ □ Pilot executado                                               │
│ □ Completion > 70% no pilot                                     │
│ □ NPS > 60 no pilot                                             │
│ □ Learnings documentados                                        │
│ □ Ajustes implementados                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Course Mechanics Canvas (Wes Kao)

```yaml
structure:
  duration: "4 semanas"
  cadence: "2 lives/semana + async"
  cohort_size: "20-50 alunos"

format:
  live_vs_async: "40% live, 60% async"
  lecture_vs_discussion: "30% lecture, 70% discussion/work"
  individual_vs_group: "40% individual, 60% group"

engagement:
  accountability: "Study buddies + small groups"
  community: "Private Slack channel"
  feedback: "Peer review + instructor feedback"

outcomes:
  deliverables: "1 projeto final + entregas semanais"
  certification: "Certificado de conclusão"
  alumni: "Acesso vitalício à comunidade"
```

---

## Métricas Target

| Métrica | Atual | Meta | Como Medir |
|---------|-------|------|------------|
| Completion Rate | 3% | 80% | % que termina todos módulos |
| Attendance Rate | - | 85% | % presença nas lives |
| Assignment Rate | - | 90% | % entregas no prazo |
| NPS | ? | 70+ | Survey final |
| Referral Rate | ? | 30% | % que indica após completar |

---

## Checklist de Completude

```yaml
fase_1_diagnostico:
  - [ ] Funnel de drop mapeado
  - [ ] Top 3 causas identificadas
  - [ ] Survey com dropouts realizado
  - [ ] Perfil de completers documentado

fase_2_redesign:
  - [ ] Elementos CBC definidos
  - [ ] State Change Method aplicado
  - [ ] Deliverables por semana listados
  - [ ] Pricing strategy definida
  - [ ] Conteúdo reestruturado

fase_3_community:
  - [ ] Comunidade do cohort configurada
  - [ ] Rituais de conexão definidos
  - [ ] Peer structures implementadas
  - [ ] Alumni program planejado

fase_4_student_health:
  - [ ] Student Health Score definido
  - [ ] Alertas configurados
  - [ ] Playbooks de intervenção documentados
  - [ ] Equipe treinada

fase_5_metricas:
  - [ ] Dashboard de métricas criado
  - [ ] Cohort pilot executado
  - [ ] Completion > 70% atingido
  - [ ] NPS > 60 atingido
  - [ ] Learnings documentados
  - [ ] Ready to scale
```

---

## Referências

- **Wes Kao**: CBC Methodology, Course Mechanics Canvas, State Change Method
- **David Spinks**: SPACES Model, Community-led learning
- **Nick Mehta**: Health Score adaptation for learning
- **Avinash Kaushik**: So What reporting framework
- **Source**: altMBA case study (96% completion)
- **Template**: `templates/learning-outcomes-tmpl.yaml`
- **Checklist**: `checklists/cbc-readiness-checklist.md`

---

*Data Intelligence Pack - Workflow v1.0*
*Primary Agent: @wes-kao*
