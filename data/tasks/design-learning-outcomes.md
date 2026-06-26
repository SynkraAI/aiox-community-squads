# Design Learning Outcomes - Framework Completo para Metricas de Aprendizagem

## Metadata
```yaml
task_id: design-learning-outcomes
version: 1.0.0
category: education-analytics
tier: TASK
difficulty: advanced
estimated_time: 8-12 hours
elicit: true
primary_agents:
  - wes-kao
secondary_agents:
  - peter-fader
  - david-spinks
  - nick-mehta
dependencies:
  - tasks/analyze-cohort.md
  - tasks/measure-community.md
  - checklists/health-score-checklist.md
outputs:
  - Learning Outcomes Framework Document
  - Completion Rate Optimization Plan
  - Engagement Score System Design
  - Learning Progression Tracking Model
  - Outcome Measurement Dashboard
  - Cohort-Based Benchmarks Report
methodology:
  - Cohort-Based Course Design (Wes Kao/Maven)
  - Course Mechanics Canvas (12 Levers)
  - State Change Method (Engagement)
  - Transformation-First Design (altMBA)
  - Community-Driven Learning (CBC Model)
  - NPS for Learning (Outcome Validation)
```

---

## Objetivo

Definir um framework completo para medir learning outcomes e otimizar completion rates em cursos e programas educacionais, usando a metodologia de Wes Kao (co-fundadora Maven, altMBA) que alcancou 96% de completion rate vs 3-6% de MOOCs tradicionais.

Esta task permite:

- **Definir completion rate methodology** que vai alem de "terminou/nao terminou"
- **Criar engagement score** por conteudo, modulo e sessao
- **Construir learning progression tracking** que mede progresso real
- **Implementar outcome measurement** (NPS, skill assessment, transformacao)
- **Estabelecer cohort-based benchmarks** para comparacao continua
- **Diagnosticar e corrigir** pontos de drop-off no aprendizado

> "The difference between 6% completion (MOOCs) and 96% completion (cohort-based) isn't content quality—it's design."
> — Wes Kao, Co-founder Maven & altMBA

> "You can't have a start and end date, and just expect a high completion rate. You need community to help students stay motivated and stick through learning hard things."
> — Wes Kao

> "Monotony causes audiences to tune out; movement causes alertness."
> — Wes Kao, The State Change Method

---

## CONTEXTO: O PROBLEMA DAS METRICAS DE APRENDIZAGEM

### Por Que MOOCs Falham (3-6% Completion)

```
┌────────────────────────────────────────────────────────────────┐
│              ANATOMIA DO FRACASSO DOS MOOCs                     │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PROBLEMA 1: SELF-PACED = SEM URGENCIA                         │
│  ├── "Faço depois" → nunca faz                                  │
│  ├── Sem deadline real → sem priorizacao                        │
│  └── Competing priorities sempre vencem                         │
│                                                                  │
│  PROBLEMA 2: SOZINHO = SEM ACCOUNTABILITY                       │
│  ├── Ninguem sabe se voce nao fez                              │
│  ├── Sem pressao social → facil desistir                       │
│  └── Sem comunidade → sem suporte emocional                    │
│                                                                  │
│  PROBLEMA 3: PASSIVO = FACIL DESENGAJAR                        │
│  ├── Assistir videos = consumo passivo                          │
│  ├── Sem producao de conteudo = sem skin in the game           │
│  └── Facil fazer multitasking (e perder foco)                  │
│                                                                  │
│  PROBLEMA 4: BAIXO PRECO = BAIXO COMMITMENT                     │
│  ├── $20 curso = "e se eu nao gostar?"                         │
│  ├── Sem dor financeira = sem urgencia                          │
│  └── Facil abandonar sem consequencia                           │
│                                                                  │
│  PROBLEMA 5: SEM FEEDBACK = NAO SABE SE ESTA APRENDENDO        │
│  ├── Quiz automatizado ≠ aprendizado real                       │
│  ├── Sem feedback de pares = sem validacao                      │
│  └── Sem aplicacao = conhecimento teorico apenas               │
│                                                                  │
│  RESULTADO: 3-6% completion rate                                │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Como CBCs Resolvem (96% Completion)

```
┌────────────────────────────────────────────────────────────────┐
│              ANATOMIA DO SUCESSO DOS CBCs                       │
│           (Cohort-Based Courses - Wes Kao/Maven)                │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SOLUCAO 1: FIXED SCHEDULE = URGENCIA REAL                     │
│  ├── Data de inicio/fim → compromisso claro                    │
│  ├── Semana 1, Semana 2, Semana 3 → ritmo                      │
│  └── "Perdi a aula ao vivo" = motivacao para nao perder        │
│                                                                  │
│  SOLUCAO 2: COHORT = ACCOUNTABILITY SOCIAL                     │
│  ├── Colegas sabem se voce nao fez                             │
│  ├── Pressao social positiva → motivacao                        │
│  └── Comunidade → suporte nos momentos dificeis                │
│                                                                  │
│  SOLUCAO 3: ATIVO = IMPOSSIVEL SER PASSIVO                     │
│  ├── Projetos com deadline → producao obrigatoria              │
│  ├── Discussoes ao vivo → participacao requerida               │
│  └── Feedback de pares → investimento mutuo                    │
│                                                                  │
│  SOLUCAO 4: PREMIUM PRICE = SKIN IN THE GAME                   │
│  ├── $500-5000 → "preciso aproveitar"                          │
│  ├── Dor financeira → urgencia                                  │
│  └── Valor percebido → respeito pelo programa                  │
│                                                                  │
│  SOLUCAO 5: FEEDBACK CONSTANTE = VALIDACAO                     │
│  ├── Peer feedback imediato → sabe se esta aprendendo          │
│  ├── Instrutor ao vivo → correcao em tempo real                │
│  └── Projetos aplicados → resultado visivel                    │
│                                                                  │
│  RESULTADO: 70-96% completion rate                              │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Dados Maven (Gagan Biyani, 2024)

```
┌────────────────────────────────────────────────────────────────┐
│               MAVEN vs MOOC: DADOS REAIS                        │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  METRICA                  │  MOOC     │  MAVEN CBC  │  DELTA    │
│  ─────────────────────────┼───────────┼─────────────┼───────────│
│  Enrolled → Week 1        │   39%     │    93%      │   2.4x    │
│  Week 1 → Week 2          │   16%     │    96%      │   6.0x    │
│  Enrolled → Week 2        │    6%     │    89%      │  14.8x    │
│                                                                  │
│  FATORES DE SUCESSO MAVEN:                                      │
│  1. Live, vetted instructor                                     │
│  2. Community of peers (cohort)                                 │
│  3. Interactive projects and discussions                        │
│                                                                  │
│  "Live interactive learning is 14x more effective               │
│   than passive video consumption."                              │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## PRE-REQUISITOS

### Checklist de Preparacao

```markdown
## Antes de Iniciar

### Dados Necessarios
- [ ] Enrollments com timestamps (user_id, enrolled_at, cohort_id)
- [ ] Progress tracking por modulo/aula (user_id, lesson_id, completed_at)
- [ ] Attendance em sessoes ao vivo (user_id, session_id, attended)
- [ ] Submissions de projetos (user_id, project_id, submitted_at, grade)
- [ ] Interacoes em comunidade (posts, comments, replies)
- [ ] Survey responses (NPS, satisfaction, feedback)

### Definicoes Alinhadas
- [ ] O que define "completion" para seu programa?
- [ ] Quais modulos/aulas sao obrigatorios vs opcionais?
- [ ] Qual e o threshold de engagement aceitavel?
- [ ] Como medimos "transformacao" do aluno?
- [ ] Qual e o periodo de analise (por cohort? por periodo?)

### Ferramentas
- [ ] LMS com tracking de progresso (Teachable, Thinkific, Circle, etc.)
- [ ] Analytics de comunidade (Circle, Slack, Discord)
- [ ] Survey tool (Typeform, Google Forms)
- [ ] Spreadsheet/BI para analise
```

---

## FASE 0: DIAGNOSTICO INICIAL

### Step 0.1: Elicitacao de Contexto

```yaml
elicit: true
questions:
  - question: "Qual e o formato do seu programa educacional?"
    options:
      - Self-paced (assincrono, on-demand)
      - Cohort-based course (inicio/fim definido, ao vivo)
      - Hibrido (conteudo assincrono + sessoes ao vivo)
      - Bootcamp intensivo (full-time ou part-time)
      - Community-led learning (peer-driven)
      - Outro

  - question: "Qual e a duracao tipica do programa?"
    options:
      - Curto (1-2 semanas)
      - Medio (3-6 semanas)
      - Longo (2-3 meses)
      - Extended (3+ meses)
      - Ongoing/assinatura

  - question: "Qual e o preco do programa?"
    options:
      - Gratuito
      - Low-ticket ($0-100)
      - Mid-ticket ($100-500)
      - High-ticket ($500-2000)
      - Premium ($2000+)

  - question: "Qual e o principal objetivo de aprendizado?"
    options:
      - Skill development (tecnico)
      - Mindset/comportamento
      - Certificacao/credencial
      - Networking/comunidade
      - Transformacao de carreira

  - question: "Qual e seu completion rate atual?"
    options:
      - Muito baixo (<10%)
      - Baixo (10-30%)
      - Medio (30-60%)
      - Alto (60-80%)
      - Muito alto (>80%)
      - Nao sei
```

### Step 0.2: Matriz de Adequacao de Modelo

```
┌────────────────────────────────────────────────────────────────┐
│            MATRIZ DE MODELO - LEARNING OUTCOMES                 │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SELF-PACED (3-10% completion tipico)                          │
│  ├── Metricas: Progress %, video completion, quiz scores       │
│  ├── Desafio: Engagement sem accountability                    │
│  └── Foco: Gamificacao, milestones, email sequences            │
│                                                                  │
│  COHORT-BASED (70-96% completion tipico)                       │
│  ├── Metricas: Attendance, submission, peer interaction        │
│  ├── Desafio: Escalar mantendo qualidade                       │
│  └── Foco: Community, live sessions, accountability            │
│                                                                  │
│  HIBRIDO (30-70% completion tipico)                            │
│  ├── Metricas: Async progress + live attendance                │
│  ├── Desafio: Balancear flexibilidade e estrutura             │
│  └── Foco: Checkpoints, office hours, peer groups              │
│                                                                  │
│  BOOTCAMP (50-85% completion tipico)                           │
│  ├── Metricas: Daily attendance, project delivery, job outcome │
│  ├── Desafio: Intensidade vs burnout                           │
│  └── Foco: Career outcomes, portfolio, networking              │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## FASE 1: COMPLETION RATE METHODOLOGY

### Step 1.1: Definindo Completion Rate

```markdown
## Framework de Completion Rate - Wes Kao

### NIVEL 1: COMPLETION BASICA (Insuficiente)

Definicao simples: "Completou todas as aulas"

PROBLEMA:
- Nao mede aprendizado real
- Nao mede engajamento
- Nao mede transformacao
- Usuario pode "passar rapido" sem absorver

### NIVEL 2: COMPLETION QUALIFICADA (Minimo Aceitavel)

Definicao: "Completou conteudo + entregou projetos"

CRITERIOS:
- [x] 80%+ das aulas assistidas
- [x] Todos os projetos obrigatorios entregues
- [x] Nota minima nos projetos (se aplicavel)

### NIVEL 3: COMPLETION ENGAJADA (Recomendado)

Definicao: "Completou + engajou + interagiu"

CRITERIOS:
- [x] 80%+ das aulas assistidas
- [x] Todos os projetos obrigatorios entregues
- [x] 70%+ attendance em sessoes ao vivo
- [x] Minimo de N interacoes na comunidade
- [x] Participou de peer feedback

### NIVEL 4: COMPLETION TRANSFORMACIONAL (Ideal - Wes Kao)

Definicao: "Completou + engajou + transformou"

CRITERIOS:
- [x] 80%+ das aulas assistidas
- [x] Todos os projetos obrigatorios entregues
- [x] 70%+ attendance em sessoes ao vivo
- [x] Evidencia de aplicacao pratica
- [x] Self-reported transformation
- [x] NPS promoter (9-10)
```

### Step 1.2: Metricas de Completion por Tipo

```markdown
## Metricas de Completion por Formato

### SELF-PACED COURSE

| Metrica | Formula | Target | Benchmark |
|---------|---------|--------|-----------|
| **Enrollment to Start** | Started / Enrolled | >60% | 40-70% |
| **Module Completion** | Completed modules / Total modules | >50% | 20-50% |
| **Overall Completion** | Fully completed / Enrolled | >15% | 3-15% |
| **Certificate Rate** | Certificates / Enrolled | >10% | 5-12% |

### COHORT-BASED COURSE (Wes Kao/Maven)

| Metrica | Formula | Target | Benchmark |
|---------|---------|--------|-----------|
| **Activation Rate** | Week 1 active / Enrolled | >90% | 85-95% |
| **Weekly Retention** | Week N active / Week N-1 active | >95% | 90-98% |
| **Live Attendance** | Attended / Expected sessions | >80% | 70-90% |
| **Project Submission** | Submitted / Required projects | >90% | 85-95% |
| **Overall Completion** | Fully completed / Enrolled | >80% | 70-96% |
| **NPS** | Promoters - Detractors | >70 | 60-80 |

### BOOTCAMP

| Metrica | Formula | Target | Benchmark |
|---------|---------|--------|-----------|
| **Daily Attendance** | Days present / Total days | >90% | 85-95% |
| **Project Completion** | Projects done / Projects assigned | >95% | 90-98% |
| **Graduation Rate** | Graduated / Enrolled | >80% | 70-90% |
| **Job Placement** | Employed 6mo / Graduated | >70% | 50-80% |

### HIBRIDO

| Metrica | Formula | Target | Benchmark |
|---------|---------|--------|-----------|
| **Async Progress** | Async content completed | >70% | 50-80% |
| **Live Participation** | Live sessions attended | >60% | 50-75% |
| **Engagement Score** | Composite (async + live + community) | >65% | 50-70% |
| **Overall Completion** | Full completion | >50% | 35-60% |
```

### Step 1.3: Completion Rate Funnel Analysis

```markdown
## Analise de Funnel de Completion

### Template de Funnel (CBC - 4 Semanas)

```
ENROLLED          100%  |████████████████████████████████████████|
                        ↓ (-7%) No-show / Nao comecou
WEEK 1 ACTIVE      93%  |█████████████████████████████████████|
                        ↓ (-4%) Drop Week 1
WEEK 2 ACTIVE      89%  |███████████████████████████████████|
                        ↓ (-6%) Drop Week 2 (maior queda tipica)
WEEK 3 ACTIVE      83%  |█████████████████████████████████|
                        ↓ (-3%) Drop Week 3
WEEK 4 ACTIVE      80%  |████████████████████████████████|
                        ↓ (-2%) Nao finalizou projeto final
COMPLETED          78%  |██████████████████████████████|
```

### Pontos de Atencao

| Ponto | Drop Esperado | Drop Critico | Diagnostico |
|-------|---------------|--------------|-------------|
| Enrolled → W1 | <10% | >15% | Onboarding ruim ou expectativa errada |
| W1 → W2 | <5% | >10% | Conteudo W1 nao engajou |
| W2 → W3 | <8% | >12% | "Messy middle" - momentum perdido |
| W3 → W4 | <5% | >8% | Fadiga ou conteudo muito denso |
| W4 → Complete | <3% | >5% | Projeto final muito complexo |

### Perguntas Diagnosticas por Ponto

**Se drop Enrolled → W1 e alto:**
- O onboarding foi claro e acolhedor?
- O aluno sabe o que esperar?
- Ha bloqueio tecnico (acesso, plataforma)?
- A expectativa de vendas corresponde a realidade?

**Se drop W1 → W2 e alto:**
- A primeira semana entregou valor claro?
- O "aha moment" foi alcancado?
- O aluno se conectou com colegas?
- O ritmo foi adequado (nao muito facil, nao muito dificil)?

**Se drop W2 → W3 e alto (Wes Kao: "messy middle"):**
- Ha checkpoint de accountability mid-course?
- O instrutor fez follow-up individual?
- Grupos de estudo estao ativos?
- Ha fatigue de conteudo?

**Se drop W3 → W4 e alto:**
- O conteudo esta muito denso no final?
- Ha "finish line energy" sendo cultivada?
- Os alunos veem o valor do projeto final?

**Se drop W4 → Complete e alto:**
- O projeto final esta muito complexo?
- Ha suporte suficiente para finalizacao?
- O deadline e realista?
```

### Step 1.4: SQL Templates para Completion

```sql
-- TEMPLATE 1: Completion Rate por Cohort

WITH cohort_enrollments AS (
  SELECT
    c.id AS cohort_id,
    c.name AS cohort_name,
    c.start_date,
    COUNT(DISTINCT e.user_id) AS enrolled
  FROM cohorts c
  LEFT JOIN enrollments e ON c.id = e.cohort_id
  GROUP BY c.id, c.name, c.start_date
),

cohort_completions AS (
  SELECT
    e.cohort_id,
    COUNT(DISTINCT CASE WHEN p.completion_pct >= 80 THEN e.user_id END) AS completed_80,
    COUNT(DISTINCT CASE WHEN p.completion_pct = 100 THEN e.user_id END) AS completed_100,
    COUNT(DISTINCT CASE WHEN p.project_submitted = true THEN e.user_id END) AS projects_done
  FROM enrollments e
  LEFT JOIN progress p ON e.user_id = p.user_id AND e.cohort_id = p.cohort_id
  GROUP BY e.cohort_id
)

SELECT
  ce.cohort_name,
  ce.start_date,
  ce.enrolled,
  cc.completed_80,
  cc.completed_100,
  cc.projects_done,
  ROUND(cc.completed_80::numeric / NULLIF(ce.enrolled, 0) * 100, 1) AS completion_rate_80,
  ROUND(cc.completed_100::numeric / NULLIF(ce.enrolled, 0) * 100, 1) AS completion_rate_100,
  ROUND(cc.projects_done::numeric / NULLIF(ce.enrolled, 0) * 100, 1) AS project_submission_rate
FROM cohort_enrollments ce
LEFT JOIN cohort_completions cc ON ce.cohort_id = cc.cohort_id
ORDER BY ce.start_date DESC;
```

```sql
-- TEMPLATE 2: Weekly Retention Funnel

WITH weekly_activity AS (
  SELECT
    e.cohort_id,
    e.user_id,
    EXTRACT(WEEK FROM a.activity_date) - EXTRACT(WEEK FROM c.start_date) + 1 AS week_number,
    COUNT(*) AS activities
  FROM enrollments e
  JOIN cohorts c ON e.cohort_id = c.id
  JOIN user_activities a ON e.user_id = a.user_id
  WHERE a.activity_date BETWEEN c.start_date AND c.end_date
  GROUP BY e.cohort_id, e.user_id, week_number
),

weekly_active AS (
  SELECT
    cohort_id,
    week_number,
    COUNT(DISTINCT user_id) AS active_users
  FROM weekly_activity
  GROUP BY cohort_id, week_number
),

cohort_size AS (
  SELECT cohort_id, COUNT(DISTINCT user_id) AS enrolled
  FROM enrollments
  GROUP BY cohort_id
)

SELECT
  c.name AS cohort_name,
  wa.week_number,
  wa.active_users,
  cs.enrolled,
  ROUND(wa.active_users::numeric / cs.enrolled * 100, 1) AS retention_pct,
  LAG(wa.active_users) OVER (PARTITION BY wa.cohort_id ORDER BY wa.week_number) AS prev_week,
  ROUND(
    (wa.active_users - LAG(wa.active_users) OVER (PARTITION BY wa.cohort_id ORDER BY wa.week_number))::numeric
    / NULLIF(LAG(wa.active_users) OVER (PARTITION BY wa.cohort_id ORDER BY wa.week_number), 0) * 100, 1
  ) AS week_over_week_change
FROM weekly_active wa
JOIN cohorts c ON wa.cohort_id = c.id
JOIN cohort_size cs ON wa.cohort_id = cs.cohort_id
ORDER BY c.start_date DESC, wa.week_number;
```

```sql
-- TEMPLATE 3: Completion por Nivel de Engajamento

WITH user_engagement AS (
  SELECT
    e.user_id,
    e.cohort_id,
    -- Contagem de atividades
    COUNT(DISTINCT a.session_id) AS sessions_attended,
    COUNT(DISTINCT p.post_id) AS community_posts,
    COUNT(DISTINCT pr.project_id) AS projects_submitted,
    -- Progresso
    COALESCE(prog.completion_pct, 0) AS content_completion
  FROM enrollments e
  LEFT JOIN attendance a ON e.user_id = a.user_id AND e.cohort_id = a.cohort_id
  LEFT JOIN community_posts p ON e.user_id = p.user_id
  LEFT JOIN project_submissions pr ON e.user_id = pr.user_id AND e.cohort_id = pr.cohort_id
  LEFT JOIN progress prog ON e.user_id = prog.user_id AND e.cohort_id = prog.cohort_id
  GROUP BY e.user_id, e.cohort_id, prog.completion_pct
),

user_segments AS (
  SELECT
    *,
    CASE
      WHEN content_completion >= 80 AND sessions_attended >= 3 AND community_posts >= 5 THEN 'High Engaged'
      WHEN content_completion >= 50 AND sessions_attended >= 2 THEN 'Medium Engaged'
      WHEN content_completion >= 20 THEN 'Low Engaged'
      ELSE 'Minimal'
    END AS engagement_level
  FROM user_engagement
)

SELECT
  engagement_level,
  COUNT(*) AS users,
  AVG(content_completion) AS avg_completion,
  AVG(sessions_attended) AS avg_sessions,
  AVG(community_posts) AS avg_posts,
  AVG(projects_submitted) AS avg_projects
FROM user_segments
GROUP BY engagement_level
ORDER BY avg_completion DESC;
```

---

## FASE 2: ENGAGEMENT SCORE POR CONTEUDO

### Step 2.1: Framework de Engagement Score (Wes Kao)

```markdown
## Engagement Score System - Inspirado em Wes Kao

### PRINCIPIO CENTRAL

"Engagement nao e sobre quanto tempo o aluno passou,
mas sobre quao ativamente ele participou da transformacao."

### COMPONENTES DO ENGAGEMENT SCORE

┌────────────────────────────────────────────────────────────────┐
│               ENGAGEMENT SCORE COMPONENTS                       │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CONTENT ENGAGEMENT (25%)                                    │
│     ├── Video completion rate                                   │
│     ├── Reading time vs expected                                │
│     ├── Quiz/exercise completion                                │
│     └── Re-watches (indica dificuldade ou interesse)           │
│                                                                  │
│  2. LIVE PARTICIPATION (30%)                                    │
│     ├── Session attendance rate                                 │
│     ├── Chat participation during live                          │
│     ├── Questions asked                                         │
│     └── Breakout room engagement                                │
│                                                                  │
│  3. PROJECT DELIVERY (25%)                                      │
│     ├── On-time submission                                      │
│     ├── Quality score (se avaliado)                            │
│     ├── Iteration/revision                                      │
│     └── Beyond requirements (extra effort)                      │
│                                                                  │
│  4. COMMUNITY CONTRIBUTION (20%)                                │
│     ├── Posts/discussions initiated                             │
│     ├── Replies/help to peers                                   │
│     ├── Peer feedback given                                     │
│     └── Networking activities                                   │
│                                                                  │
│  ENGAGEMENT SCORE = Weighted sum de todos os componentes        │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Step 2.2: Engagement Score por Tipo de Conteudo

```markdown
## Metricas de Engagement por Tipo de Conteudo

### VIDEO CONTENT

| Metrica | Formula | Target | Peso |
|---------|---------|--------|------|
| **Completion Rate** | Watched / Duration | >80% | 40% |
| **Engagement Points** | Plays, pauses, rewinds | Varies | 20% |
| **Drop-off Point** | Avg position of abandonment | >70% | 20% |
| **Replay Rate** | Re-watches / Total watches | 5-15% | 20% |

**Sinais de Problema:**
- Completion <50%: Video muito longo ou desengajante
- Drop-off <30%: Abertura fraca, perda de atencao imediata
- Replay >25%: Conteudo confuso (precisa revisar para entender)

### TEXT/READING CONTENT

| Metrica | Formula | Target | Peso |
|---------|---------|--------|------|
| **Read-through Rate** | Scrolled 100% / Opened | >60% | 40% |
| **Time on Page** | Actual / Expected read time | 80-120% | 30% |
| **Highlight/Save** | Users who saved/highlighted | >10% | 30% |

**Sinais de Problema:**
- Read-through <40%: Conteudo muito longo ou denso
- Time <50% expected: Scanning, nao lendo de verdade
- Time >150% expected: Conteudo confuso

### LIVE SESSIONS

| Metrica | Formula | Target | Peso |
|---------|---------|--------|------|
| **Attendance Rate** | Attended / Enrolled | >75% | 30% |
| **Stay Rate** | Stayed full session / Attended | >85% | 25% |
| **Chat Activity** | Messages / Attendees | >3 | 25% |
| **Poll Response** | Responded / Attendees | >60% | 20% |

**Sinais de Problema:**
- Attendance <60%: Horario ruim ou valor percebido baixo
- Stay <70%: Sessao nao engajante, monotona
- Chat <1/attendee: Falta de interatividade

### PROJECTS/ASSIGNMENTS

| Metrica | Formula | Target | Peso |
|---------|---------|--------|------|
| **Submission Rate** | Submitted / Assigned | >85% | 35% |
| **On-time Rate** | On-time / Submitted | >75% | 25% |
| **Quality Score** | Avg grade or rating | >70% | 25% |
| **Revision Rate** | Revised / Submitted | >30% | 15% |

**Sinais de Problema:**
- Submission <70%: Projeto muito complexo ou valor nao claro
- On-time <60%: Deadline irreal ou carga muito alta
- Quality <50%: Instrucoes confusas ou suporte insuficiente
```

### Step 2.3: State Change Method - Engagement em Sessoes ao Vivo

```markdown
## State Change Method (Wes Kao)

### CONCEITO

"Monotony causes audiences to tune out; movement causes alertness."

O instrutor deve mudar a modalidade a cada 3-5 minutos para
manter a atencao dos alunos em sessoes ao vivo/Zoom.

### TIPOS DE STATE CHANGE

┌────────────────────────────────────────────────────────────────┐
│               STATE CHANGE CATALOG                              │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VERBAL STATE CHANGES                                          │
│  ├── Ask a question for the chat                               │
│  ├── Cold call a participant                                   │
│  ├── Change speaker (co-instructor, guest)                     │
│  ├── Crack a joke / humor break                                │
│  └── Share personal story / anecdote                           │
│                                                                  │
│  VISUAL STATE CHANGES                                          │
│  ├── Switch from slides to gallery view                        │
│  ├── Show a video clip                                         │
│  ├── Share screen to demo something                            │
│  ├── Display a poll or quiz                                    │
│  └── Show participant's work                                   │
│                                                                  │
│  PARTICIPATORY STATE CHANGES                                   │
│  ├── Breakout rooms (2-4 people, 5-10 min)                    │
│  ├── Silent reflection (1-2 min)                              │
│  ├── Chat waterfall (everyone types, then send together)       │
│  ├── Poll or quiz                                              │
│  └── Raise hand / reaction exercise                            │
│                                                                  │
│  STRUCTURAL STATE CHANGES                                      │
│  ├── Mini-break (2-3 min stretch)                             │
│  ├── Transition to Q&A                                         │
│  ├── Case study analysis                                       │
│  └── Live exercise / apply learning                            │
│                                                                  │
└────────────────────────────────────────────────────────────────┘

### METRICAS DE STATE CHANGE

| Metrica | Formula | Target | Por que |
|---------|---------|--------|---------|
| **State Changes/Hour** | Total changes / Session hours | 10-15 | 1 change every 4-6 min |
| **Participation Rate** | Participated in change / Attendees | >60% | Validates engagement |
| **Chat Spike** | Messages during change / Before | >2x | Shows re-engagement |
| **Stay Rate** | % who stayed after 30 min | >90% | Indicates maintained interest |

### CHECKLIST DE SESSAO AO VIVO

```markdown
## Pre-Sessao
- [ ] Session planejada com state changes a cada 5 min
- [ ] Breakout rooms configurados
- [ ] Polls/quizzes preparados
- [ ] Ice-breaker definido para primeiros 5 minutos

## Durante Sessao
- [ ] Participacao incentivada nos primeiros 5 min
- [ ] State change a cada 3-5 min
- [ ] Chat monitorado e referenciado
- [ ] Breakout room de pelo menos 5-10 min

## Pos-Sessao
- [ ] Recording disponivel em <24h
- [ ] Follow-up com quem nao veio
- [ ] Highlights compartilhados na comunidade
```
```

### Step 2.4: Engagement Score Calculator

```markdown
## Calculadora de Engagement Score

### FORMULA GERAL

```
ENGAGEMENT_SCORE =
  (Content_Score * 0.25) +
  (Live_Score * 0.30) +
  (Project_Score * 0.25) +
  (Community_Score * 0.20)

Onde cada sub-score e de 0-100
```

### CALCULO POR COMPONENTE

**CONTENT_SCORE (0-100):**
```
= (video_completion_rate * 0.4) +
  (reading_engagement * 0.3) +
  (quiz_completion * 0.3)

Exemplo:
- Video completion: 85%
- Reading engagement: 70%
- Quiz completion: 90%
- CONTENT_SCORE = (85*0.4) + (70*0.3) + (90*0.3) = 34 + 21 + 27 = 82
```

**LIVE_SCORE (0-100):**
```
= (attendance_rate * 0.35) +
  (stay_rate * 0.25) +
  (chat_participation * 0.20) +
  (poll_response * 0.20)

Exemplo:
- Attendance: 80%
- Stay rate: 95%
- Chat participation: 60%
- Poll response: 75%
- LIVE_SCORE = (80*0.35) + (95*0.25) + (60*0.20) + (75*0.20) = 28 + 23.75 + 12 + 15 = 78.75
```

**PROJECT_SCORE (0-100):**
```
= (submission_rate * 0.35) +
  (on_time_rate * 0.25) +
  (quality_score * 0.25) +
  (revision_effort * 0.15)

Exemplo:
- Submission rate: 100%
- On-time: 80%
- Quality: 75%
- Revision: 50%
- PROJECT_SCORE = (100*0.35) + (80*0.25) + (75*0.25) + (50*0.15) = 35 + 20 + 18.75 + 7.5 = 81.25
```

**COMMUNITY_SCORE (0-100):**
```
= (posts_initiated * 0.25) +
  (peer_replies * 0.30) +
  (feedback_given * 0.25) +
  (networking_activity * 0.20)

Normalizado: cada metrica convertida para % do esperado

Exemplo:
- Posts: 3/5 esperado = 60%
- Replies: 8/5 esperado = 100% (cap at 100)
- Feedback: 4/4 esperado = 100%
- Networking: 2/3 esperado = 67%
- COMMUNITY_SCORE = (60*0.25) + (100*0.30) + (100*0.25) + (67*0.20) = 15 + 30 + 25 + 13.4 = 83.4
```

**ENGAGEMENT SCORE FINAL:**
```
= (82 * 0.25) + (78.75 * 0.30) + (81.25 * 0.25) + (83.4 * 0.20)
= 20.5 + 23.625 + 20.3125 + 16.68
= 81.1 (HIGH ENGAGEMENT)
```

### INTERPRETACAO DO SCORE

| Score | Categoria | Interpretacao | Acao |
|-------|-----------|---------------|------|
| 90-100 | Exceptional | Top performer, potencial ambassador | Reconhecer, envolver como mentor |
| 75-89 | High | Muito engajado, completara | Manter momentum, check-in positivo |
| 60-74 | Medium | Engajado mas pode cair | Intervencao proativa, suporte |
| 40-59 | Low | Risco de nao completar | Outreach urgente, investigar barreiras |
| 0-39 | Critical | Muito provavelmente abandona | Contato direto, oferecer extensao/pausa |
```

---

## FASE 3: LEARNING PROGRESSION TRACKING

### Step 3.1: Framework de Learning Progression

```markdown
## Learning Progression - Modelo Wes Kao

### CONCEITO: TRANSFORMATION-FIRST DESIGN

"O design do curso deve comecar com a transformacao desejada.
Qual e o estado inicial do aluno? Qual e o estado final?
Como medimos a 'distancia viajada'?"

### ESTADOS DE APRENDIZADO

┌────────────────────────────────────────────────────────────────┐
│               LEARNING PROGRESSION STATES                       │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STATE 0: ENROLLED (Potencial)                                 │
│  ├── Pagou/se inscreveu                                        │
│  ├── Tem intencao de fazer                                     │
│  └── Ainda nao comecou                                         │
│                                                                  │
│  STATE 1: ACTIVATED (Comecou)                                  │
│  ├── Acessou plataforma                                        │
│  ├── Completou onboarding                                      │
│  └── Consumiu primeiro conteudo                                │
│                                                                  │
│  STATE 2: ENGAGED (Engajado)                                   │
│  ├── Completando conteudo regularmente                         │
│  ├── Participando de sessoes/comunidade                        │
│  └── Entregando projetos                                       │
│                                                                  │
│  STATE 3: PROGRESSING (Progredindo)                            │
│  ├── 50%+ do conteudo completo                                │
│  ├── Mostrando sinais de aprendizado                          │
│  └── Aplicando conhecimento                                    │
│                                                                  │
│  STATE 4: COMPLETING (Finalizando)                             │
│  ├── 80%+ do conteudo completo                                │
│  ├── Trabalhando no projeto final                              │
│  └── Participando das sessoes finais                           │
│                                                                  │
│  STATE 5: COMPLETED (Completou)                                │
│  ├── 100% conteudo + projeto final                            │
│  ├── Certificado emitido                                       │
│  └── Objetivo inicial alcancado                                │
│                                                                  │
│  STATE 6: TRANSFORMED (Transformado) ← OBJETIVO REAL          │
│  ├── Aplicou aprendizado na vida real                          │
│  ├── Mudanca mensuravel de comportamento/skill                │
│  └── NPS promoter + recomenda ativamente                       │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Step 3.2: Metricas de Progressao por Estado

```markdown
## Metricas de Transicao entre Estados

### ENROLLED → ACTIVATED

| Metrica | Formula | Target | Urgencia se abaixo |
|---------|---------|--------|-------------------|
| **Activation Rate** | Activated / Enrolled | >90% | <80% = problema grave |
| **Time to Activate** | Avg days to first access | <3 dias | >7 dias = intervir |
| **Onboarding Complete** | Completed onboarding / Enrolled | >85% | <70% = revisar onboarding |

**Acoes para baixa ativacao:**
- Email sequence de welcome mais urgente
- Contato direto nos primeiros 48h
- Video de welcome do instrutor
- "First win" imediato (quick assignment)

### ACTIVATED → ENGAGED

| Metrica | Formula | Target | Urgencia se abaixo |
|---------|---------|--------|-------------------|
| **Week 1 Engagement** | Active Week 1 / Activated | >95% | <85% = problema |
| **First Session Attendance** | Attended session 1 / Activated | >80% | <65% = intervir |
| **First Post** | Posted in community / Activated | >50% | <30% = incentivar |

**Acoes para baixo engajamento inicial:**
- Buddy system (parear com outro aluno)
- Accountability group automatico
- Instructor outreach personalizado
- Gamificacao do primeiro post

### ENGAGED → PROGRESSING

| Metrica | Formula | Target | Urgencia se abaixo |
|---------|---------|--------|-------------------|
| **Mid-Course Retention** | Active Week 3+ / Active Week 1 | >85% | <75% = "messy middle" |
| **Halfway Completion** | 50%+ content / Active | >70% | <50% = intervir |
| **Project Submission W1-2** | Submitted early projects / Active | >80% | <60% = problema |

**Acoes para "messy middle" (Wes Kao):**
- Mid-course checkpoint call
- Peer accountability groups
- Celebration de milestones
- Re-engajamento de valor (why this matters)

### PROGRESSING → COMPLETING

| Metrica | Formula | Target | Urgencia se abaixo |
|---------|---------|--------|-------------------|
| **Final Stretch Retention** | Active Week N-1 / Active Week N-2 | >90% | <80% = finish line push |
| **Final Project Start** | Started final / Progressing | >95% | <85% = suporte urgente |
| **Pre-Graduation Engagement** | Engaged Week N / Progressing | >85% | <70% = check-in |

**Acoes para finalizar forte:**
- "Finish line" energy - celebrar que estao quase la
- Dedicated office hours para projeto final
- Showcase dos projetos (motivacao para terminar)
- Deadline flexibility se necessario

### COMPLETING → COMPLETED

| Metrica | Formula | Target | Urgencia se abaixo |
|---------|---------|--------|-------------------|
| **Graduation Rate** | Completed / Completing | >95% | <85% = problema |
| **Project Final Submission** | Submitted final / Completing | >90% | <80% = suporte |
| **Certificate Claimed** | Claimed / Completed | >80% | <60% = comunicar valor |

### COMPLETED → TRANSFORMED (Objetivo Real)

| Metrica | Formula | Target | Urgencia se abaixo |
|---------|---------|--------|-------------------|
| **NPS Promoter** | Promoters / Completed | >60% | <40% = revisar programa |
| **Real-World Application** | Applied learning / Completed | >70% | <50% = add aplicacao |
| **Outcome Achievement** | Achieved stated goal / Completed | >50% | <30% = revisar promessa |
| **Alumni Engagement** | Active in alumni / Completed | >30% | <15% = criar valor pos |
```

### Step 3.3: Learning Progression Dashboard

```markdown
## Dashboard de Learning Progression

### VISAO GERAL (Todos os Alunos)

```
┌────────────────────────────────────────────────────────────────┐
│                   LEARNING PROGRESSION FUNNEL                    │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ENROLLED      ████████████████████████████████████████  100    │
│                         ↓ -8%                                    │
│  ACTIVATED     █████████████████████████████████████     92     │
│                         ↓ -5%                                    │
│  ENGAGED       ████████████████████████████████         87     │
│                         ↓ -9%                                    │
│  PROGRESSING   ███████████████████████████              78     │
│                         ↓ -6%                                    │
│  COMPLETING    ███████████████████████                  72     │
│                         ↓ -4%                                    │
│  COMPLETED     █████████████████████                    68     │
│                         ↓ -28%                                   │
│  TRANSFORMED   ██████████████                           40     │
│                                                                  │
│  MAIOR OPORTUNIDADE: Engaged → Progressing (-9%)                │
│  ACAO: Implementar mid-course checkpoint                         │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### VISAO POR COHORT

```
┌────────────────────────────────────────────────────────────────┐
│            PROGRESSION BY COHORT (Current State)                │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  COHORT        │ ENR │ ACT │ ENG │ PRG │ CMP │ COM │ TRF │     │
│  ──────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼     │
│  Janeiro 2024  │ 50  │  -  │  -  │  -  │  -  │ 42  │ 28  │ 56% │
│  Fevereiro 24  │ 48  │  -  │  -  │  -  │  -  │ 38  │ 22  │ 46% │
│  Marco 2024    │ 55  │  -  │  -  │  -  │ 48  │  -  │  -  │ 87% │
│  Abril 2024    │ 52  │  -  │  -  │ 42  │  -  │  -  │  -  │ 81% │
│  Maio 2024     │ 60  │  -  │ 55  │  -  │  -  │  -  │  -  │ 92% │
│  Junho 2024    │ 58  │ 54  │  -  │  -  │  -  │  -  │  -  │ 93% │
│                                                                  │
│  INSIGHT: Cohort Fevereiro teve 10% menos transformacao         │
│  INVESTIGAR: O que foi diferente nesse cohort?                  │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### ALERTA DE RISCO (At-Risk Students)

```
┌────────────────────────────────────────────────────────────────┐
│                    AT-RISK STUDENTS ALERT                        │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HIGH RISK (Score <40) - 8 alunos                              │
│  ├── Maria S. - Stuck at ACTIVATED (7 dias sem atividade)      │
│  ├── Joao P. - ENGAGED falling (3 sessoes perdidas)            │
│  ├── Ana C. - PROGRESSING stalled (projeto nao iniciado)       │
│  └── [+5 mais]                                                  │
│                                                                  │
│  MEDIUM RISK (Score 40-59) - 12 alunos                         │
│  ├── Pedro L. - ENGAGED (engagement score caindo)              │
│  ├── Carla M. - PROGRESSING (atrasada em 1 semana)            │
│  └── [+10 mais]                                                 │
│                                                                  │
│  ACAO SUGERIDA:                                                 │
│  - High Risk: Contato direto do instrutor em <24h              │
│  - Medium Risk: Email personalizado + check-in automatizado     │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```
```

---

## FASE 4: OUTCOME MEASUREMENT

### Step 4.1: Framework de Outcome Measurement (Wes Kao)

```markdown
## Outcome Measurement - Modelo Wes Kao

### PRINCIPIO: TRANSFORMATION OVER COMPLETION

"Completion rate e uma metrica de output, nao de outcome.
O verdadeiro sucesso e a transformacao do aluno."

### NIVEIS DE OUTCOME MEASUREMENT

┌────────────────────────────────────────────────────────────────┐
│              OUTCOME MEASUREMENT HIERARCHY                      │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  NIVEL 1: REACTION (Imediato)                                  │
│  "O aluno gostou?"                                              │
│  ├── Satisfaction score (1-10)                                 │
│  ├── NPS (Net Promoter Score)                                  │
│  └── Would recommend (Y/N)                                     │
│                                                                  │
│  NIVEL 2: LEARNING (Pos-programa)                              │
│  "O aluno aprendeu?"                                            │
│  ├── Knowledge assessment (pre/post)                           │
│  ├── Skill demonstration (projeto)                             │
│  └── Self-reported confidence increase                         │
│                                                                  │
│  NIVEL 3: BEHAVIOR (30-90 dias depois)                         │
│  "O aluno mudou comportamento?"                                 │
│  ├── Application in real life                                  │
│  ├── Habit formation                                           │
│  └── Peer/manager feedback                                     │
│                                                                  │
│  NIVEL 4: RESULTS (6-12 meses depois)                          │
│  "O aluno atingiu o resultado?"                                 │
│  ├── Career outcome (promocao, novo emprego)                   │
│  ├── Business outcome (revenue, growth)                        │
│  └── Life outcome (goal achievement)                           │
│                                                                  │
│  IDEAL: Medir todos os 4 niveis                                 │
│  MINIMO: Medir niveis 1 e 2                                    │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Step 4.2: NPS para Learning Outcomes

```markdown
## NPS (Net Promoter Score) para Educacao

### CONCEITO

NPS mede a probabilidade de recomendacao em escala 0-10:
- **Promoters (9-10):** Entusiastas que vao recomendar
- **Passives (7-8):** Satisfeitos mas nao entusiastas
- **Detractors (0-6):** Insatisfeitos que podem prejudicar

NPS = % Promoters - % Detractors

### NPS BENCHMARKS PARA EDUCACAO

| Tipo de Programa | NPS Baixo | NPS Medio | NPS Alto | Excelente |
|------------------|-----------|-----------|----------|-----------|
| MOOC | <10 | 10-30 | 30-50 | >50 |
| Bootcamp | <30 | 30-50 | 50-70 | >70 |
| CBC (Cohort-Based) | <50 | 50-65 | 65-80 | >80 |
| Premium Workshop | <60 | 60-75 | 75-85 | >85 |

### QUANDO MEDIR NPS

```
TIMING                  │  O QUE CAPTURA          │  LIMITACOES
────────────────────────┼─────────────────────────┼───────────────────
Imediato pos-curso      │  Reacao emocional       │  "Honeymoon effect"
30 dias pos-curso       │  Retencao de valor      │  Pode esquecer detalhes
90 dias pos-curso       │  Aplicacao real         │  Low response rate
6 meses pos-curso       │  Resultado de longo prazo│  Very low response
```

**RECOMENDACAO:** Medir NPS em pelo menos 2 momentos:
1. Imediato (para feedback rapido)
2. 30-90 dias (para outcome real)

### PERGUNTAS COMPLEMENTARES AO NPS

**Alem da pergunta padrao de NPS, pergunte:**

1. **Para Promoters (9-10):**
   - "O que voce mais gostou do programa?"
   - "Voce ja recomendou para alguem? Para quem?"

2. **Para Passives (7-8):**
   - "O que faltou para voce dar nota 9 ou 10?"
   - "O que poderiamos melhorar?"

3. **Para Detractors (0-6):**
   - "O que nao atendeu suas expectativas?"
   - "O que teria feito a diferenca para voce?"

### TEMPLATE DE SURVEY NPS

```yaml
survey:
  title: "[Nome do Programa] - Feedback Survey"
  timing: "Imediato pos-programa"

  questions:
    - id: nps
      type: scale_0_10
      text: "Qual a probabilidade de voce recomendar [Programa] para um amigo ou colega?"
      required: true

    - id: nps_reason
      type: open_text
      text: "Qual o principal motivo da sua nota?"
      required: true

    - id: most_valuable
      type: open_text
      text: "Qual foi a parte mais valiosa do programa para voce?"

    - id: improvement
      type: open_text
      text: "O que poderiamos melhorar?"

    - id: transformation
      type: scale_1_5
      text: "O quanto voce se sente transformado apos o programa?"
      labels: ["Nada", "Pouco", "Moderadamente", "Muito", "Completamente"]

    - id: would_apply
      type: yes_no
      text: "Voce pretende aplicar o que aprendeu nas proximas semanas?"

    - id: testimonial
      type: yes_no
      text: "Podemos usar seu feedback como depoimento (com sua aprovacao)?"
```

### ANALISE DE NPS

```markdown
## Analise de NPS por Segmento

### SEGMENTACAO RECOMENDADA

| Segmento | Por que segmentar | O que procurar |
|----------|-------------------|----------------|
| Por Cohort | Comparar evolucao | Tendencia melhorando/piorando |
| Por Completion | Correlacionar completion x NPS | Completers tem NPS maior? |
| Por Engagement | Correlacionar engagement x NPS | High engaged = High NPS? |
| Por Demographics | Identificar fit | Algum perfil tem NPS muito diferente? |

### ACOES POR NPS

| NPS Score | Status | Acao |
|-----------|--------|------|
| >70 | Excelente | Solicitar depoimentos, criar programa de embaixadores |
| 50-70 | Bom | Manter qualidade, identificar pontos de melhoria |
| 30-50 | Atencao | Investigar detratores, fazer melhorias |
| <30 | Critico | Parar e revisar programa, entrevistas profundas |
```
```

### Step 4.3: Skill Assessment (Pre/Post)

```markdown
## Skill Assessment - Medicao de Aprendizado

### CONCEITO

Medir a mudanca de conhecimento/habilidade do aluno
comparando antes (pre) e depois (post) do programa.

### TIPOS DE ASSESSMENT

┌────────────────────────────────────────────────────────────────┐
│                    ASSESSMENT TYPES                             │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. KNOWLEDGE ASSESSMENT (Conhecimento)                        │
│     ├── Quiz de multipla escolha                               │
│     ├── Perguntas de verdadeiro/falso                          │
│     └── Correlacao de conceitos                                │
│     QUANDO: Skills teoricos, certificacoes                      │
│                                                                  │
│  2. SKILL DEMONSTRATION (Habilidade)                           │
│     ├── Projeto pratico                                        │
│     ├── Simulacao / role-play                                  │
│     └── Portfolio                                               │
│     QUANDO: Skills praticos, aplicados                          │
│                                                                  │
│  3. SELF-ASSESSMENT (Auto-avaliacao)                           │
│     ├── Escala de confianca (1-10)                            │
│     ├── Checklist de competencias                              │
│     └── Reflexao estruturada                                   │
│     QUANDO: Soft skills, mindset                               │
│                                                                  │
│  4. PEER/360 ASSESSMENT                                        │
│     ├── Feedback de colegas                                    │
│     ├── Feedback de gestor/cliente                             │
│     └── Avaliacao de stakeholders                              │
│     QUANDO: Skills interpessoais, lideranca                    │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### TEMPLATE DE PRE/POST ASSESSMENT

```yaml
assessment:
  name: "[Skill] Assessment"
  type: pre_post

  sections:
    - name: "Knowledge Check"
      weight: 30%
      questions:
        - id: k1
          type: multiple_choice
          text: "[Pergunta sobre conceito fundamental]"
          options: [A, B, C, D]
          correct: B
        - id: k2
          type: multiple_choice
          text: "[Pergunta sobre aplicacao]"
          options: [A, B, C, D]
          correct: C
        # ... mais perguntas

    - name: "Confidence Scale"
      weight: 30%
      questions:
        - id: c1
          type: scale_1_10
          text: "Qual sua confianca em [skill 1]?"
        - id: c2
          type: scale_1_10
          text: "Qual sua confianca em [skill 2]?"
        # ... mais skills

    - name: "Competency Checklist"
      weight: 40%
      questions:
        - id: comp1
          type: checklist
          text: "Marque as competencias que voce domina:"
          options:
            - "Sei definir [conceito]"
            - "Consigo aplicar [tecnica]"
            - "Posso ensinar [skill] para outros"
            # ... mais competencias

metrics:
  - name: "Knowledge Gain"
    formula: "(Post Knowledge - Pre Knowledge) / Pre Knowledge * 100"
    target: ">30%"

  - name: "Confidence Lift"
    formula: "Post Confidence Avg - Pre Confidence Avg"
    target: ">2 pontos"

  - name: "Competency Growth"
    formula: "Post Competencies Checked - Pre Competencies Checked"
    target: ">50% growth"
```

### Step 4.4: Real-World Application Tracking

```markdown
## Tracking de Aplicacao no Mundo Real

### CONCEITO (Wes Kao)

"O objetivo nao e que o aluno complete o curso.
O objetivo e que o aluno aplique o que aprendeu
e tenha resultado na vida real."

### METRICAS DE APLICACAO

| Metrica | Formula | Target | Como Coletar |
|---------|---------|--------|--------------|
| **Intent to Apply** | % que pretende aplicar | >90% | Survey pos-curso |
| **Actually Applied** | % que aplicou | >70% | Survey 30 dias |
| **Application Success** | % que teve resultado | >50% | Survey 90 dias |
| **Outcome Achievement** | % que atingiu objetivo inicial | >40% | Survey 6 meses |

### TEMPLATE DE FOLLOW-UP SURVEY (30 dias)

```yaml
survey:
  title: "30 Days Check-in"
  timing: "30 dias pos-programa"

  questions:
    - id: applied
      type: yes_no_partial
      text: "Voce aplicou algo que aprendeu no [Programa]?"
      options: ["Sim, totalmente", "Sim, parcialmente", "Ainda nao", "Nao pretendo"]

    - id: what_applied
      type: open_text
      text: "O que especificamente voce aplicou?"
      conditional: applied in ["Sim, totalmente", "Sim, parcialmente"]

    - id: result
      type: open_text
      text: "Qual foi o resultado?"
      conditional: applied in ["Sim, totalmente", "Sim, parcialmente"]

    - id: barrier
      type: multiple_choice
      text: "O que te impediu de aplicar?"
      conditional: applied in ["Ainda nao", "Nao pretendo"]
      options:
        - "Falta de tempo"
        - "Falta de oportunidade"
        - "Nao me senti preparado"
        - "O conteudo nao era aplicavel"
        - "Outro"

    - id: confidence_now
      type: scale_1_10
      text: "Qual sua confianca em [skill principal] hoje?"

    - id: support_needed
      type: open_text
      text: "Que suporte adicional ajudaria voce a aplicar?"
```

### TEMPLATE DE OUTCOME SURVEY (90+ dias)

```yaml
survey:
  title: "Outcome Check"
  timing: "90 dias pos-programa"

  questions:
    - id: original_goal
      type: open_text
      text: "Qual era seu objetivo ao se inscrever no [Programa]?"

    - id: goal_achieved
      type: scale_1_5
      text: "O quanto voce alcancou esse objetivo?"
      labels: ["Nada", "Pouco", "Parcialmente", "Muito", "Completamente"]

    - id: tangible_result
      type: open_text
      text: "Descreva um resultado tangivel que voce conseguiu:"

    - id: career_impact
      type: multiple_choice
      text: "O programa impactou sua carreira?"
      options:
        - "Consegui promocao"
        - "Mudei de emprego/area"
        - "Assumi novas responsabilidades"
        - "Aumentei minha renda"
        - "Lancei projeto/negocio"
        - "Nao teve impacto ainda"

    - id: would_do_again
      type: yes_no
      text: "Sabendo o que sabe hoje, voce faria o programa novamente?"

    - id: nps_90d
      type: scale_0_10
      text: "Qual a probabilidade de recomendar o programa?"
```
```

---

## FASE 5: COHORT-BASED BENCHMARKS

### Step 5.1: Benchmarks por Tipo de Programa

```markdown
## Benchmarks de Learning Outcomes por Tipo

### MOOC (Massive Open Online Course)

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Enrollment to Start | 30% | 45% | 60% | 75% |
| Overall Completion | 3% | 6% | 12% | 20% |
| NPS | 10 | 25 | 40 | 55 |
| Would Recommend | 20% | 35% | 50% | 65% |

### COHORT-BASED COURSE (CBC)

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Enrollment to Week 1 | 80% | 90% | 95% | 98% |
| Week-over-Week Retention | 85% | 92% | 96% | 98% |
| Overall Completion | 65% | 78% | 88% | 95% |
| Project Submission | 75% | 85% | 92% | 97% |
| Live Attendance | 60% | 75% | 85% | 92% |
| NPS | 55 | 68 | 78 | 88 |

### BOOTCAMP

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Graduation Rate | 60% | 75% | 85% | 92% |
| Daily Attendance | 75% | 85% | 92% | 97% |
| Project Completion | 70% | 82% | 90% | 95% |
| Job Placement (6mo) | 40% | 60% | 75% | 85% |
| NPS | 45 | 60 | 72% | 82 |

### CORPORATE TRAINING

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Completion Rate | 50% | 70% | 85% | 95% |
| Satisfaction | 3.2 | 3.8 | 4.3 | 4.7 |
| Knowledge Gain | 15% | 25% | 40% | 55% |
| Behavior Change (30d) | 20% | 35% | 50% | 65% |
```

### Step 5.2: Comparacao de Cohorts

```markdown
## Template de Comparacao de Cohorts

### VISAO GERAL

| Cohort | Enrolled | Completed | Rate | NPS | vs Prev |
|--------|----------|-----------|------|-----|---------|
| Jan 24 | 50 | 42 | 84% | 72 | baseline |
| Fev 24 | 48 | 36 | 75% | 65 | -9pp, -7 NPS |
| Mar 24 | 55 | 48 | 87% | 78 | +12pp, +13 NPS |
| Abr 24 | 52 | 44 | 85% | 74 | -2pp, -4 NPS |
| Mai 24 | 60 | 52 | 87% | 80 | +2pp, +6 NPS |

### ANALISE DE VARIACOES

**COHORT FEVEREIRO (underperformer):**
- O que foi diferente?
  - [ ] Mudanca de instrutor?
  - [ ] Mudanca de conteudo?
  - [ ] Mudanca de preco/promocao?
  - [ ] Fatores externos (feriado, sazonalidade)?
- Acoes tomadas:
  - [descrever acoes]
- Resultado:
  - Cohort Marco voltou ao baseline

**COHORT MARCO (overperformer):**
- O que foi diferente?
  - [ ] Novo sistema de accountability?
  - [ ] Instrutor diferente?
  - [ ] Composicao do cohort?
- Learnings para replicar:
  - [descrever learnings]

### COMPARACAO DE METRICAS DETALHADAS

| Metrica | Jan | Fev | Mar | Abr | Mai | Trend |
|---------|-----|-----|-----|-----|-----|-------|
| Activation (W1) | 96% | 90% | 98% | 94% | 97% | → |
| W1→W2 Retention | 95% | 88% | 97% | 94% | 96% | ↑ |
| W2→W3 Retention | 90% | 82% | 92% | 88% | 90% | → |
| W3→W4 Retention | 92% | 90% | 93% | 94% | 95% | ↑ |
| Project Sub | 88% | 78% | 92% | 86% | 90% | ↑ |
| Live Attend | 75% | 65% | 82% | 78% | 80% | ↑ |
| Community Posts | 4.2/user | 2.8/user | 5.1/user | 4.5/user | 4.8/user | ↑ |
| NPS | 72 | 65 | 78 | 74 | 80 | ↑ |

**MAIOR OPORTUNIDADE:** W2→W3 Retention (messy middle)
**ACAO:** Implementar checkpoint mid-course
```

### Step 5.3: Benchmark Dashboard

```markdown
## Learning Outcomes Dashboard

### SECAO 1: KPIs PRINCIPAIS

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│  COMPLETION RATE    ENGAGEMENT SCORE    NPS           TRANSFORM  │
│      82%                 74/100         +72             68%      │
│   (+5pp vs ant)      (-2 vs ant)    (+8 vs ant)    (+12% vs ant)│
│   Target: 80%        Target: 75      Target: 70     Target: 60%  │
│      ✅                  ⚠️             ✅              ✅       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### SECAO 2: PROGRESSION FUNNEL

```
┌─────────────────────────────────────────────────────────────────┐
│                   CURRENT COHORT PROGRESSION                      │
│                                                                   │
│  Enrolled     ████████████████████████████████████████  100      │
│  Activated    █████████████████████████████████████     94       │
│  Engaged      ████████████████████████████████          88       │
│  Progressing  ██████████████████████████████            82       │
│  Completing   ████████████████████████████              78       │
│  Completed    -                                          -       │
│                                                                   │
│  CURRENT WEEK: 3 of 4                                             │
│  PROJECTED COMPLETION: 75-80%                                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### SECAO 3: COHORT COMPARISON

```
┌─────────────────────────────────────────────────────────────────┐
│                   COHORT COMPARISON (6 months)                   │
│                                                                   │
│  Completion Rate                                                  │
│  Jan █████████████████████████████████████████ 84%              │
│  Fev ███████████████████████████████ 75% ↓                      │
│  Mar ██████████████████████████████████████████ 87% ↑           │
│  Abr ████████████████████████████████████████ 85%               │
│  Mai ██████████████████████████████████████████ 87%             │
│                                                                   │
│  BEST: Mar 2024 (87%)  |  WORST: Fev 2024 (75%)                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### SECAO 4: AT-RISK ALERTS

```
┌─────────────────────────────────────────────────────────────────┐
│                        AT-RISK STUDENTS                          │
│                                                                   │
│  🔴 HIGH RISK (5)                                                │
│     → 3 sem atividade ha 5+ dias                                 │
│     → 2 nao submeteram projeto W2                                │
│                                                                   │
│  🟡 MEDIUM RISK (8)                                              │
│     → 5 com engagement score caindo                              │
│     → 3 perderam ultima sessao ao vivo                          │
│                                                                   │
│  ACAO SUGERIDA: Outreach imediato para High Risk                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### SECAO 5: NPS TREND

```
┌─────────────────────────────────────────────────────────────────┐
│                         NPS OVER TIME                            │
│                                                                   │
│    +80 ─┬────────────────────●──                                 │
│         │              ●─────                                     │
│    +70 ─┼────────●─────                                          │
│         │   ●────                                                 │
│    +60 ─┼───            ↓ Feb dip                                │
│         │  ●                                                      │
│    +50 ─┼──                                                       │
│         │                                                         │
│    +40 ─┴────────────────────────────────                        │
│         Jan  Feb  Mar  Apr  May  Jun                              │
│                                                                   │
│  TREND: Crescente (+8 pontos em 6 meses)                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```
```

---

## FASE 6: DIAGNOSTICO E OTIMIZACAO

### Step 6.1: Diagnostico de Problemas Comuns

```markdown
## Diagnostico de Learning Outcomes

### PROBLEMA 1: Completion Rate Baixo (<50%)

**Sintomas:**
- Muitos alunos nao terminam
- Drop alto nas primeiras semanas
- Projetos nao entregues

**Diagnostico - Perguntas:**
1. O aluno entendeu o que esperar antes de se inscrever?
2. O onboarding entrega valor nos primeiros minutos?
3. Ha accountability (cohort, deadline, pares)?
4. O preco gera commitment suficiente?
5. Ha muita complexidade / pouca orientacao?

**Solucoes (Wes Kao):**
- Adicionar fixed schedule (datas de inicio/fim)
- Criar cohort com peers para accountability
- Aumentar preco (skin in the game)
- Simplificar primeiros passos (quick wins)
- Adicionar sessoes ao vivo

### PROBLEMA 2: Engagement Score Baixo (<60)

**Sintomas:**
- Alunos completam mas nao participam
- Sessoes ao vivo com baixa audiencia
- Comunidade vazia
- Projetos superficiais

**Diagnostico - Perguntas:**
1. As sessoes ao vivo sao interativas ou monologos?
2. Ha incentivo para participar na comunidade?
3. Os projetos sao relevantes para a vida real?
4. O aluno ve valor em participar (nao so completar)?

**Solucoes (Wes Kao - State Change Method):**
- State change a cada 3-5 min nas sessoes
- Breakout rooms obrigatorios
- Peer feedback como parte do programa
- Gamificacao da comunidade
- Projetos com aplicacao imediata

### PROBLEMA 3: NPS Baixo (<50)

**Sintomas:**
- Alunos completam mas nao recomendam
- Feedback negativo ou neutro
- Baixa taxa de depoimentos
- Poucos repeat customers

**Diagnostico - Perguntas:**
1. A promessa de venda corresponde a entrega?
2. O aluno atingiu o resultado que esperava?
3. O suporte foi adequado?
4. Houve momentos de "wow" / transformacao?

**Solucoes:**
- Alinhar marketing com realidade do programa
- Focar em outcomes, nao so completion
- Melhorar suporte e acessibilidade
- Criar momentos de celebracao e vitoria
- Follow-up pos-programa para aplicacao

### PROBLEMA 4: Baixa Transformacao (<40%)

**Sintomas:**
- Alunos completam, gostam, mas nao mudam
- Nao aplicam na vida real
- Nao atingem objetivo original
- Feedback de "foi interessante mas..."

**Diagnostico - Perguntas:**
1. O programa foca em conhecimento ou aplicacao?
2. Ha oportunidade de praticar durante o programa?
3. O aluno saiu com um plano de acao?
4. Ha follow-up para incentivar aplicacao?

**Solucoes (Wes Kao):**
- Projects over lectures (fazer > assistir)
- Aplicacao real durante o programa
- Accountability post-programa
- Alumni community ativa
- Coaching / mentoria de follow-up
```

### Step 6.2: Framework de Otimizacao

```markdown
## Framework de Otimizacao de Learning Outcomes

### CICLO DE MELHORIA CONTINUA

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│    1. MEDIR                                                       │
│       │                                                           │
│       ↓                                                           │
│    2. ANALISAR ←──────────────────────────┐                      │
│       │                                     │                      │
│       ↓                                     │                      │
│    3. IDENTIFICAR GAPS                      │                      │
│       │                                     │                      │
│       ↓                                     │                      │
│    4. PRIORIZAR (ICE Score)                 │                      │
│       │                                     │                      │
│       ↓                                     │                      │
│    5. IMPLEMENTAR                           │                      │
│       │                                     │                      │
│       ↓                                     │                      │
│    6. TESTAR (A/B ou Cohort)               │                      │
│       │                                     │                      │
│       └─────────────────────────────────────┘                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### PRIORIZACAO COM ICE SCORE

| Melhoria | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score |
|----------|---------------|-------------------|-------------|-----------|
| Add mid-course checkpoint | 8 | 8 | 7 | 17.9 |
| State change training | 7 | 9 | 8 | 16.8 |
| Peer accountability groups | 8 | 7 | 6 | 14.0 |
| Increase price | 6 | 5 | 9 | 13.3 |
| Add alumni community | 7 | 6 | 4 | 11.2 |

ICE = (Impact * Confidence * Ease) / 10

**TOP PRIORITY:** Add mid-course checkpoint (ICE 17.9)

### TEMPLATE DE EXPERIMENTO

```yaml
experiment:
  name: "Mid-Course Checkpoint"
  hypothesis: "Adicionar checkpoint na semana 2 reduzira drop W2→W3 em 5pp"

  current_state:
    w2_w3_retention: 85%
    completion_rate: 78%

  target_state:
    w2_w3_retention: 90%
    completion_rate: 82%

  implementation:
    - "Criar sessao de checkpoint na semana 2"
    - "Incluir 1-on-1 opcional com instrutor"
    - "Survey de 'como esta indo'"
    - "Celebracao de milestones"

  measurement:
    primary_metric: "W2→W3 retention"
    secondary_metrics:
      - "Completion rate"
      - "NPS"
      - "Engagement score W2-3"

  timeline:
    start: "Cohort Julho"
    duration: "1 cohort (4 semanas)"
    analysis: "1 semana pos-cohort"

  success_criteria:
    - "W2→W3 retention >= 90%"
    - "Nao reduzir NPS"
    - "Feedback positivo sobre checkpoint"
```
```

### Step 6.3: Playbooks de Intervencao

```markdown
## Playbooks de Intervencao

### PLAYBOOK 1: Aluno em Risco de Drop (Engagement Score <50)

**TRIGGER:** Engagement score cai abaixo de 50

**ACOES AUTOMATICAS (Dia 1):**
- [ ] Email personalizado: "Vi que voce nao participou de X, esta tudo bem?"
- [ ] Slack/comunidade DM: Check-in rapido
- [ ] Adicionar a lista de acompanhamento

**ACOES MANUAIS (Dia 2-3):**
- [ ] Instrutor envia mensagem pessoal
- [ ] Oferecer office hours 1-on-1
- [ ] Identificar barreira especifica

**ACOES DE SUPORTE (Dia 4+):**
- [ ] Buddy system (parear com colega engajado)
- [ ] Extensao de prazo se necessario
- [ ] Opcao de pausar e voltar proximo cohort

### PLAYBOOK 2: Messy Middle (Drop W2→W3 alto)

**TRIGGER:** Retencao W2→W3 < 85%

**ACOES PREVENTIVAS (Para proximo cohort):**
- [ ] Adicionar checkpoint call na semana 2
- [ ] Criar peer groups na semana 1 (accountability)
- [ ] Celebrar milestones de W2 publicamente
- [ ] Redesenhar conteudo de W2 se necessario

**ACOES REATIVAS (Cohort atual):**
- [ ] Comunicacao especial "estamos na metade!"
- [ ] Energia de "push" para o final
- [ ] Incentivo extra para quem esta atrasado
- [ ] Preview do valor das semanas finais

### PLAYBOOK 3: Projeto Final Nao Entregue

**TRIGGER:** Aluno chegou W4 mas nao entregou projeto

**ACOES (Sequencia):**
1. Lembrete amigavel (D-3 do prazo)
2. Oferecer extensao de 3 dias
3. Office hours dedicado para duvidas
4. Simplificar escopo se necessario
5. Opcao de entrega parcial com feedback

**COMUNICACAO:**
- "Voce esta tao perto! Falta apenas o projeto final."
- "Posso ajudar com [barreira especifica]?"
- "Lembre: o certificado e seu, so falta esse passo."

### PLAYBOOK 4: NPS Detractor (0-6)

**TRIGGER:** Aluno deu NPS <= 6

**ACOES IMEDIATAS:**
- [ ] Contato pessoal em <24h
- [ ] Perguntar: "O que poderiamos ter feito diferente?"
- [ ] Ouvir sem defender
- [ ] Oferecer compensacao se apropriado

**ACOES DE FOLLOW-UP:**
- [ ] Documentar feedback para melhoria
- [ ] Identificar se e problema sistemico ou pontual
- [ ] Se sistemico, criar plano de acao
- [ ] Acompanhar se problema foi resolvido

**OBJETIVO:** Converter detractor em passive (no minimo)
```

---

## OUTPUTS ESPERADOS

### Deliverables

Ao completar esta task, voce tera:

1. **Learning Outcomes Framework Document**
   - Definicao de completion rate para seu programa
   - Metricas de cada fase de progressao
   - Thresholds e triggers

2. **Completion Rate Optimization Plan**
   - Diagnostico do estado atual
   - Gaps identificados vs benchmark
   - Acoes priorizadas (ICE score)

3. **Engagement Score System Design**
   - Componentes do score
   - Pesos por componente
   - Sistema de tracking

4. **Learning Progression Tracking Model**
   - Estados definidos
   - Transicoes mapeadas
   - Alerts e triggers

5. **Outcome Measurement Dashboard**
   - KPIs principais
   - Visualizacoes
   - Alertas

6. **Cohort-Based Benchmarks Report**
   - Seus benchmarks vs mercado
   - Comparacao entre cohorts
   - Tendencias

---

## TEMPLATE DE RELATORIO EXECUTIVO

```markdown
# Learning Outcomes Report
## [Programa] - [Periodo]

### Executive Summary

**Headline:**
[Uma frase resumindo o principal insight]

**Numero Chave:**
[Metrica mais importante com contexto]

**Recomendacao Principal:**
[Acao mais critica a tomar]

---

### KPIs Principais

| Metrica | Atual | Target | vs Target | Trend |
|---------|-------|--------|-----------|-------|
| Completion Rate | [%] | [%] | [+/-%] | [↑↓→] |
| Engagement Score | [/100] | [/100] | [+/-] | [↑↓→] |
| NPS | [+/-] | [+/-] | [+/-] | [↑↓→] |
| Transformation Rate | [%] | [%] | [+/-%] | [↑↓→] |

---

### Cohort Comparison

| Cohort | Completion | NPS | Transformation | Notes |
|--------|------------|-----|----------------|-------|
| [Cohort 1] | [%] | [+/-] | [%] | [notes] |
| [Cohort 2] | [%] | [+/-] | [%] | [notes] |

---

### Top 3 Insights

1. **[Insight 1]**
   - Dado: [evidencia]
   - Impacto: [business impact]
   - Acao: [o que fazer]

2. **[Insight 2]**
   - Dado: [evidencia]
   - Impacto: [business impact]
   - Acao: [o que fazer]

3. **[Insight 3]**
   - Dado: [evidencia]
   - Impacto: [business impact]
   - Acao: [o que fazer]

---

### Plano de Acao (90 Dias)

| Prioridade | Acao | Owner | Prazo | KPI |
|------------|------|-------|-------|-----|
| 1 | [Acao] | [Nome] | [Data] | [Metrica] |
| 2 | [Acao] | [Nome] | [Data] | [Metrica] |
| 3 | [Acao] | [Nome] | [Data] | [Metrica] |

---

### Proximos Passos

- Data da proxima analise: [Data]
- Metricas a monitorar: [Lista]
- Experimentos em andamento: [Lista]
```

---

## CHECKLIST FINAL

```markdown
## Validacao da Task

### Completude
- [ ] Completion rate definido com criterios claros
- [ ] Engagement score system desenhado
- [ ] Learning progression states mapeados
- [ ] Outcome measurement definido (NPS, skill assessment, application)
- [ ] Benchmarks coletados e comparados
- [ ] Diagnostico realizado
- [ ] Plano de otimizacao criado

### Qualidade
- [ ] Metricas alinhadas com objetivo do programa
- [ ] Thresholds baseados em benchmarks reais
- [ ] Playbooks de intervencao acionaveis
- [ ] Dashboard visualizavel e util
- [ ] Experimentos priorizados (ICE score)

### Entrega
- [ ] Relatorio executivo pronto
- [ ] Dashboard implementavel
- [ ] Proximos passos definidos
- [ ] Owners atribuidos
```

---

## ANTI-PATTERNS

### Erros Comuns a Evitar

1. **Focar so em completion rate**
   - ERRADO: "95% completion, sucesso!"
   - CERTO: "78% completion + 72 NPS + 65% aplicaram = sucesso"

2. **Nao medir outcomes de longo prazo**
   - ERRADO: Parar de medir apos certificado
   - CERTO: Follow-up 30/90/180 dias

3. **Ignorar engagement durante o programa**
   - ERRADO: So olhar quem completou no final
   - CERTO: Monitorar engagement em tempo real

4. **Tratar todos os alunos igual**
   - ERRADO: Mesma intervencao para todos
   - CERTO: Segmentar por engagement score e intervir diferente

5. **Nao comparar cohorts**
   - ERRADO: "Nossa completion e 75%"
   - CERTO: "Cohort Fev foi 10pp abaixo do baseline, investigar"

6. **Sessoes ao vivo como monologos (Anti-Wes Kao)**
   - ERRADO: 60 min de slides sem interacao
   - CERTO: State change a cada 3-5 min

7. **Preco baixo demais**
   - ERRADO: "Vou cobrar barato para mais gente fazer"
   - CERTO: "Preco premium = commitment = completion"

---

## REFERENCIAS

### Wes Kao
- Blog: weskao.com/blog
- Newsletter: weskao.substack.com
- a16z: "In Online Ed, Content Is No Longer King—Cohorts Are"
- Medium: "How to Design an Online Course with a 96% Completion Rate"
- State Change Method: weskao.com/blog/the-state-change-method
- Course Mechanics Canvas: maven.com/resources/course-mechanics-canvas
- Maven Course Accelerator: maven.com/maven/course-accelerator

### Maven Data (Gagan Biyani, 2024)
- LinkedIn: Enrolled→W1 93% (vs 39% MOOC), W1→W2 96% (vs 16% MOOC)
- 14x more retention than video-based courses

### altMBA
- 96% completion rate (vs 3-6% MOOC)
- 550+ cities in 45 countries

### Peter Fader (Supporting)
- Cohort retention analysis methodology
- Customer heterogeneity models

### David Spinks (Supporting)
- Community metrics for learning communities
- SPACES framework for engagement

---

**Total de Linhas: 1400+**
**Metodologias Integradas:** Wes Kao (CBC, State Change, Course Mechanics Canvas), Maven Data, altMBA, NPS, Kirkpatrick Model
**Frameworks Incluidos:** 12+ (Completion Levels, Engagement Score, Progression States, Outcome Hierarchy, State Change Method, etc.)
**Templates SQL:** 3 (Completion by Cohort, Weekly Retention, Engagement Segments)
**Benchmarks:** 4 tipos de programa (MOOC, CBC, Bootcamp, Corporate)
**Playbooks:** 4 (At-Risk Student, Messy Middle, Final Project, NPS Detractor)
**Dashboards:** 3 (Progression Funnel, Cohort Comparison, At-Risk Alerts)
