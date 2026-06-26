# Analyze Cohort - Analise Completa de Cohorts para Retencao e Valor

## Metadata
```yaml
task_id: analyze-cohort
version: 1.0.0
category: customer-analytics
tier: TASK
difficulty: advanced
estimated_time: 6-10 hours
elicit: true
primary_agents:
  - peter-fader
  - wes-kao
secondary_agents:
  - sean-ellis
  - nick-mehta
dependencies:
  - tasks/calculate-clv.md
  - tasks/segment-rfm.md
  - checklists/customer-360-checklist.md
outputs:
  - Cohort Definition Matrix
  - Retention Curves Analysis
  - Cohort Comparison Report
  - Insights Extraction Document
  - Visualization Recommendations
  - Action Plan by Cohort
methodology:
  - Cohort Retention Analysis (Peter Fader/Wharton)
  - Shifted-Beta-Geometric Model (Fader & Hardie)
  - Cohort-Based Course Metrics (Wes Kao/Maven)
  - AARRR Framework Cohort View (Sean Ellis)
  - Customer Success Cohort Health (Nick Mehta)
```

---

## Objetivo

Conduzir uma analise completa de cohorts combinando a rigorosa metodologia academica de Peter Fader (Wharton) com a aplicacao pratica de Wes Kao para educacao e produtos digitais.

Esta task permite:

- **Definir cohorts estrategicamente** usando multiplas dimensoes (tempo, canal, produto, comportamento)
- **Construir retention curves** que revelam padroes de churn e engajamento
- **Comparar cohorts** para identificar o que funciona e o que nao funciona
- **Extrair insights acionaveis** para melhorar aquisicao, ativacao e retencao
- **Projetar retencao futura** usando modelos probabilisticos
- **Visualizar dados** de forma que conte uma historia clara

> "Cohort analysis lets you see the forest AND the trees. It shows you both the pattern and the individual variations that matter."
> - Peter Fader, Wharton School

> "The difference between 6% completion (MOOCs) and 96% completion (cohort-based) isn't content quality - it's design."
> - Wes Kao, Maven Co-founder

---

## CONTEXTO: POR QUE COHORT ANALYSIS

### O Problema com Metricas Agregadas

```
METRICAS AGREGADAS (Enganosas):
- "Nossa retencao mensal e 85%"
- "Completion rate medio: 15%"
- "Churn rate: 5% ao mes"

COHORT ANALYSIS (Reveladora):
- "Cohort de Janeiro reteve 72% no mes 3, mas Fevereiro apenas 58%"
- "Usuarios de referral tem 2x mais retencao que paid ads"
- "Cohorts pos-redesign tem curva de retencao 40% melhor"
```

### Analogia de Peter Fader

```
MEDIA vs COHORT:
Imagine calcular a "altura media" de todos os humanos.
- Voce obteria um numero (~1.65m)
- Mas esse numero nao descreve ninguem especificamente
- Criancas, adolescentes, adultos - todos diferentes

Cohorts sao como olhar grupos especificos:
- Altura media de bebes (50cm)
- Altura media de criancas de 10 anos (1.35m)
- Altura media de adultos (1.70m)

Agora voce entende a jornada de crescimento.
```

### Tipos de Cohort Analysis

| Tipo | Definicao | Exemplo | Quando Usar |
|------|-----------|---------|-------------|
| **Acquisition Cohort** | Agrupado por quando entrou | Janeiro 2024, Fevereiro 2024 | Analise de retencao temporal |
| **Behavioral Cohort** | Agrupado por acao inicial | Completou onboarding vs nao | Analise de ativacao |
| **Channel Cohort** | Agrupado por fonte | Organic, Paid, Referral | Analise de qualidade de aquisicao |
| **Product Cohort** | Agrupado por plano/produto | Free, Basic, Pro | Analise de valor por segmento |
| **Feature Cohort** | Agrupado por feature usada | Usou feature X vs nao | Analise de impacto de produto |

---

## PRE-REQUISITOS

### Checklist de Preparacao

```markdown
## Antes de Iniciar

### Dados Necessarios
- [ ] Historico de usuarios com data de cadastro (user_id, created_at)
- [ ] Eventos de atividade com timestamps (logins, acoes, compras)
- [ ] Informacao de canal/fonte de aquisicao (utm_source, referrer)
- [ ] Dados de produto/plano (se aplicavel)
- [ ] Eventos de churn/cancelamento (se contractual)

### Definicoes Alinhadas
- [ ] O que define um usuario "ativo"?
- [ ] Qual e a granularidade temporal? (dia, semana, mes)
- [ ] Qual e o periodo de analise minimo? (3+ meses recomendado)
- [ ] Quais eventos contam como "retorno"?

### Ferramentas
- [ ] Acesso a ferramenta de analytics (Amplitude, Mixpanel, GA4)
- [ ] Acesso a banco de dados ou data warehouse
- [ ] Planilha/BI para visualizacao (Excel, Looker, Tableau)
```

---

## FASE 0: DIAGNOSTICO INICIAL

### Step 0.1: Elicitacao de Contexto

```yaml
elicit: true
questions:
  - question: "Qual e o tipo de negocio?"
    options:
      - SaaS B2B (assinatura)
      - SaaS B2C (assinatura)
      - E-commerce (transacional)
      - Marketplace
      - Educacao/Cursos online
      - App mobile (freemium)
      - Outro

  - question: "Qual e o modelo de relacionamento com cliente?"
    options:
      - Contractual (assinatura com cancelamento explicito)
      - Non-contractual (cliente pode sumir sem avisar)
      - Hibrido (assinatura + compras avulsas)

  - question: "Qual o objetivo principal da analise?"
    options:
      - Entender retencao geral
      - Comparar canais de aquisicao
      - Avaliar impacto de mudanca de produto
      - Projetar receita futura
      - Identificar melhor momento para intervencao
      - Otimizar cohort-based course

  - question: "Qual o volume de dados disponivel?"
    options:
      - Pequeno (menos de 1.000 usuarios)
      - Medio (1.000 - 10.000 usuarios)
      - Grande (10.000 - 100.000 usuarios)
      - Enterprise (100.000+ usuarios)
```

### Step 0.2: Matriz de Adequacao de Modelo

```
┌────────────────────────────────────────────────────────────────┐
│                MATRIZ DE MODELO - FADER                         │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONTRACTUAL (churn observavel)                                 │
│  ├── Assinatura periodica (SaaS, gym, Netflix)                 │
│  ├── Modelo: Shifted-Beta-Geometric (sBG)                      │
│  └── Dado necessario: Data de entrada e saida                   │
│                                                                  │
│  NON-CONTRACTUAL (churn nao observavel)                        │
│  ├── E-commerce, app, marketplace                               │
│  ├── Modelo: BG/NBD ou Pareto/NBD                              │
│  └── Dado necessario: Historico de transacoes                   │
│                                                                  │
│  EDUCACAO (cohort-based)                                        │
│  ├── Cursos com inicio/fim definido                            │
│  ├── Modelo: Cohort completion + engagement                    │
│  └── Dado necessario: Progresso por semana/modulo               │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## FASE 1: DEFINICAO DE COHORTS

### Step 1.1: Cohort Definition Framework

```markdown
## Framework de Definicao de Cohorts

### PERGUNTA 1: Qual a Dimensao de Agrupamento?

| Dimensao | Pergunta | Exemplo |
|----------|----------|---------|
| **Temporal** | Quando entraram? | Semana 1, Semana 2, Janeiro, Q1 |
| **Canal** | De onde vieram? | Google Ads, Referral, Organic |
| **Produto** | O que compraram/assinaram? | Free, Pro, Enterprise |
| **Comportamento** | O que fizeram inicialmente? | Completou setup, Convidou amigo |
| **Demografico** | Quem sao? | Brasil, USA, Enterprise vs SMB |

### PERGUNTA 2: Qual a Granularidade Temporal?

| Granularidade | Quando Usar | Exemplo |
|---------------|-------------|---------|
| **Diario** | Apps de alta frequencia | Day 1, Day 7, Day 30 |
| **Semanal** | SaaS, cursos cohort-based | Week 1, Week 2, Week 4 |
| **Mensal** | SaaS tradicional | Month 1, Month 3, Month 12 |
| **Por Cohort Course** | Educacao | Cohort Jan 2024, Cohort Feb 2024 |

### PERGUNTA 3: Qual o Evento de Retencao?

| Negocio | Evento de Retorno | Por que |
|---------|-------------------|---------|
| SaaS | Login ou acao core | Indica uso real |
| E-commerce | Compra | Indica valor |
| App | Sessao ativa | Indica engajamento |
| Curso | Aula completada | Indica progresso |
| Comunidade | Post ou comentario | Indica participacao |
```

### Step 1.2: Cohort Matrix Template

```markdown
## Template de Matriz de Cohort

### Acquisition Cohort (Temporal)

| Cohort | N Inicial | Mes 0 | Mes 1 | Mes 2 | Mes 3 | Mes 6 | Mes 12 |
|--------|-----------|-------|-------|-------|-------|-------|--------|
| Jan 24 | [___] | 100% | [__]% | [__]% | [__]% | [__]% | [__]% |
| Fev 24 | [___] | 100% | [__]% | [__]% | [__]% | [__]% | [__]% |
| Mar 24 | [___] | 100% | [__]% | [__]% | [__]% | [__]% | [__]% |
| Abr 24 | [___] | 100% | [__]% | [__]% | [__]% | [__]% | - |
| Mai 24 | [___] | 100% | [__]% | [__]% | [__]% | - | - |
| Jun 24 | [___] | 100% | [__]% | [__]% | - | - | - |

### Channel Cohort

| Canal | N Inicial | Mes 0 | Mes 1 | Mes 2 | Mes 3 |
|-------|-----------|-------|-------|-------|-------|
| Organic | [___] | 100% | [__]% | [__]% | [__]% |
| Paid (Google) | [___] | 100% | [__]% | [__]% | [__]% |
| Paid (Meta) | [___] | 100% | [__]% | [__]% | [__]% |
| Referral | [___] | 100% | [__]% | [__]% | [__]% |
| Partner | [___] | 100% | [__]% | [__]% | [__]% |

### Behavioral Cohort (Activation)

| Comportamento Inicial | N | Mes 0 | Mes 1 | Mes 2 | Mes 3 |
|-----------------------|---|-------|-------|-------|-------|
| Completou onboarding | [___] | 100% | [__]% | [__]% | [__]% |
| Parcialmente | [___] | 100% | [__]% | [__]% | [__]% |
| Nao completou | [___] | 100% | [__]% | [__]% | [__]% |
```

### Step 1.3: SQL Templates para Extracao

```sql
-- TEMPLATE 1: Acquisition Cohort (PostgreSQL/Supabase)

WITH user_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', created_at) AS cohort_month,
    created_at AS signup_date
  FROM users
  WHERE created_at >= '2024-01-01'
),

user_activities AS (
  SELECT
    user_id,
    DATE_TRUNC('month', activity_date) AS activity_month
  FROM user_events
  WHERE event_type = 'active_session' -- ou outro evento de retencao
  GROUP BY 1, 2
),

cohort_data AS (
  SELECT
    c.cohort_month,
    EXTRACT(MONTH FROM AGE(a.activity_month, c.cohort_month)) AS months_since_signup,
    COUNT(DISTINCT c.user_id) AS users
  FROM user_cohorts c
  LEFT JOIN user_activities a
    ON c.user_id = a.user_id
    AND a.activity_month >= c.cohort_month
  GROUP BY 1, 2
),

cohort_sizes AS (
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM user_cohorts
  GROUP BY 1
)

SELECT
  cd.cohort_month,
  cd.months_since_signup,
  cd.users,
  cs.cohort_size,
  ROUND(cd.users::numeric / cs.cohort_size * 100, 1) AS retention_rate
FROM cohort_data cd
JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
ORDER BY cd.cohort_month, cd.months_since_signup;
```

```sql
-- TEMPLATE 2: Channel Cohort

WITH user_channels AS (
  SELECT
    user_id,
    CASE
      WHEN utm_source = 'google' THEN 'Paid Google'
      WHEN utm_source = 'facebook' THEN 'Paid Meta'
      WHEN utm_source = 'referral' THEN 'Referral'
      WHEN utm_source IS NULL OR utm_source = 'direct' THEN 'Organic'
      ELSE 'Other'
    END AS acquisition_channel,
    created_at AS signup_date
  FROM users
),

user_retention AS (
  SELECT
    uc.user_id,
    uc.acquisition_channel,
    uc.signup_date,
    -- Mes 1: Ativo 30-60 dias apos signup
    CASE WHEN EXISTS (
      SELECT 1 FROM user_events ue
      WHERE ue.user_id = uc.user_id
      AND ue.activity_date BETWEEN uc.signup_date + INTERVAL '30 days'
                               AND uc.signup_date + INTERVAL '60 days'
    ) THEN 1 ELSE 0 END AS retained_month_1,
    -- Mes 2: Ativo 60-90 dias apos signup
    CASE WHEN EXISTS (
      SELECT 1 FROM user_events ue
      WHERE ue.user_id = uc.user_id
      AND ue.activity_date BETWEEN uc.signup_date + INTERVAL '60 days'
                               AND uc.signup_date + INTERVAL '90 days'
    ) THEN 1 ELSE 0 END AS retained_month_2
  FROM user_channels uc
)

SELECT
  acquisition_channel,
  COUNT(*) AS total_users,
  SUM(retained_month_1) AS retained_m1,
  ROUND(SUM(retained_month_1)::numeric / COUNT(*) * 100, 1) AS retention_m1_pct,
  SUM(retained_month_2) AS retained_m2,
  ROUND(SUM(retained_month_2)::numeric / COUNT(*) * 100, 1) AS retention_m2_pct
FROM user_retention
GROUP BY acquisition_channel
ORDER BY retention_m1_pct DESC;
```

```sql
-- TEMPLATE 3: Cohort Course Completion (Wes Kao style)

WITH course_cohorts AS (
  SELECT
    e.user_id,
    c.cohort_name,
    c.start_date AS cohort_start,
    c.end_date AS cohort_end,
    e.enrolled_at
  FROM enrollments e
  JOIN cohorts c ON e.cohort_id = c.id
),

lesson_progress AS (
  SELECT
    p.user_id,
    p.lesson_id,
    l.week_number,
    p.completed_at
  FROM progress p
  JOIN lessons l ON p.lesson_id = l.id
  WHERE p.completed = true
),

cohort_weekly_completion AS (
  SELECT
    cc.cohort_name,
    lp.week_number,
    COUNT(DISTINCT cc.user_id) AS users_completed_week
  FROM course_cohorts cc
  LEFT JOIN lesson_progress lp ON cc.user_id = lp.user_id
  WHERE lp.week_number IS NOT NULL
  GROUP BY cc.cohort_name, lp.week_number
)

SELECT
  cwc.cohort_name,
  cwc.week_number,
  cwc.users_completed_week,
  cs.cohort_size,
  ROUND(cwc.users_completed_week::numeric / cs.cohort_size * 100, 1) AS completion_pct
FROM cohort_weekly_completion cwc
JOIN (
  SELECT cohort_name, COUNT(DISTINCT user_id) AS cohort_size
  FROM course_cohorts
  GROUP BY cohort_name
) cs ON cwc.cohort_name = cs.cohort_name
ORDER BY cwc.cohort_name, cwc.week_number;
```

---

## FASE 2: RETENTION CURVES

### Step 2.1: Entendendo Retention Curves

```
┌────────────────────────────────────────────────────────────────┐
│                    RETENTION CURVE ANATOMY                       │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  100% ─┬─────────────────────────────────────────────────────   │
│        │╲                                                        │
│        │ ╲ INICIAL DROP                                          │
│   80%  │  ╲  (Dia 1-7)                                          │
│        │   ╲ - Usuarios que nao engajaram                       │
│        │    ╲ - Problema de ativacao                            │
│   60%  │     ╲___                                                │
│        │         ╲                                               │
│        │          ╲ DECAY PHASE                                  │
│   40%  │           ╲  (Semana 2-8)                              │
│        │            ╲ - Churn gradual                           │
│        │             ╲ - Problema de valor                       │
│   20%  │              ╲___________                               │
│        │                          ╲                              │
│        │                           ╲___ PLATEAU                  │
│   10%  │                               ─────────                 │
│        │                              Core users                 │
│    0%  └─────────────────────────────────────────────────────   │
│        D1  D7  W2  W4  M2  M3  M6  M12                           │
│                                                                  │
│  ZONAS DE INTERVENCAO:                                          │
│  - Inicial Drop alto (>40%): Problema de onboarding             │
│  - Decay acentuado: Problema de valor percebido                  │
│  - Plateau baixo (<10%): Problema de product-market fit          │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Step 2.2: Metricas de Retention Curves

```markdown
## Metricas Essenciais de Retention

### Metricas de Curto Prazo

| Metrica | Formula | O que indica | Benchmark SaaS |
|---------|---------|--------------|----------------|
| **D1 Retention** | Ativos D1 / Signups | Primeira impressao | 40-60% |
| **D7 Retention** | Ativos D7 / Signups | Aha moment alcancado | 25-40% |
| **W1 Activation** | Ativados W1 / Signups | Onboarding efetivo | 50-70% |

### Metricas de Medio Prazo

| Metrica | Formula | O que indica | Benchmark SaaS |
|---------|---------|--------------|----------------|
| **M1 Retention** | Ativos M1 / Signups | Valor inicial percebido | 20-40% |
| **M2 Retention** | Ativos M2 / Signups | Habito formando | 15-30% |
| **M3 Retention** | Ativos M3 / Signups | Habito formado | 10-25% |

### Metricas de Longo Prazo

| Metrica | Formula | O que indica | Benchmark SaaS |
|---------|---------|--------------|----------------|
| **M6 Retention** | Ativos M6 / Signups | Core user base | 8-20% |
| **M12 Retention** | Ativos M12 / Signups | True loyal customers | 5-15% |
| **Steady State** | Plateau apos M6+ | Retencao sustentavel | 5-12% |

### Coleta de Dados - Sua Analise

| Periodo | Seu Valor | Benchmark | Status |
|---------|-----------|-----------|--------|
| D1 Retention | [___]% | 40-60% | [___] |
| D7 Retention | [___]% | 25-40% | [___] |
| M1 Retention | [___]% | 20-40% | [___] |
| M3 Retention | [___]% | 10-25% | [___] |
| M6 Retention | [___]% | 8-20% | [___] |
| M12 Retention | [___]% | 5-15% | [___] |
```

### Step 2.3: Modelo Shifted-Beta-Geometric (Fader)

```markdown
## Modelo sBG - Projecao de Retencao

### Conceito (Peter Fader)

"A heterogeneidade nao observada nas taxas de churn dos clientes
pode ser modelada usando uma distribuicao Beta."

### O que o Modelo Captura

```
REALIDADE:
- Nem todos os clientes tem a mesma probabilidade de churn
- Alguns clientes sao naturalmente mais fieis
- Outros sao mais propensos a sair cedo

MODELAGEM:
- Taxa de churn individual: p (varia por pessoa)
- Distribuicao de p: Beta(a, b)
- Parametros a e b sao estimados dos dados
```

### Formula de Retencao Esperada

```
Retention(t) = Beta(a, b + t) / Beta(a, b)

Onde:
- a, b = parametros da distribuicao Beta
- t = periodo de tempo
- Beta() = funcao Beta
```

### Implementacao em Excel/Sheets

```
PASSO 1: Dados de entrada
- Coluna A: Periodo (0, 1, 2, 3, ...)
- Coluna B: Retencao observada (100%, 75%, 55%, ...)

PASSO 2: Parametros iniciais
- Celula E1: a (comece com 1)
- Celula E2: b (comece com 1)

PASSO 3: Formula de projecao (Coluna C)
= EXP(GAMMALN(E$1)+GAMMALN(E$2+A2)-GAMMALN(E$1+E$2+A2)
      -GAMMALN(E$1)-GAMMALN(E$2)+GAMMALN(E$1+E$2))

PASSO 4: Solver
- Minimize a soma dos erros quadrados
- Variando a e b
- Restricao: a > 0, b > 0
```

### Interpretacao dos Parametros

| Cenario | a | b | Significado |
|---------|---|---|-------------|
| Alto churn inicial, depois estabiliza | Baixo | Alto | Base heterogenea, alguns muito fieis |
| Churn constante | ~1 | ~1 | Base homogenea |
| Churn acelerando | Alto | Baixo | Base majoritariamente propensa a sair |
```

### Step 2.4: Retention Curves - WES KAO (Educacao)

```markdown
## Retention Curves para Cohort-Based Courses

### Framework Maven (Wes Kao)

```
┌────────────────────────────────────────────────────────────────┐
│             MOOC vs CBC RETENTION COMPARISON                    │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  100% ─┬─────────────────────────────────────────────────────   │
│        │╲  CBC (Cohort-Based Course)                            │
│        │ ╲  93% activation to Week 1                            │
│   93%  │  ╲─────────────────────────────                        │
│        │   ╲  96% Week 1 to Week 2                              │
│   89%  │    ────────────────────────────                        │
│        │                                                         │
│        │                                                         │
│   60%  │                                                         │
│        │                                                         │
│   39%  │  MOOC Traditional                                       │
│        │╲  39% activation to Week 1                             │
│        │ ╲                                                       │
│    6%  │  ╲──────────────────────                               │
│        │     6% Week 2 retention                                 │
│    0%  └─────────────────────────────────────────────────────   │
│        Enrolled  Week 1  Week 2  Week 3  Week 4                  │
│                                                                  │
│  DIFERENCA: 14x mais retencao em CBC vs MOOC                    │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Metricas de Completion (Cursos)

| Metrica | MOOC Tipico | CBC Tipico | Meta Excelente |
|---------|-------------|------------|----------------|
| **Enrollment to W1** | 39% | 93% | >90% |
| **W1 to W2** | 16% | 96% | >95% |
| **Overall Completion** | 3-10% | 70-96% | >80% |
| **Project Submission** | 5% | 85%+ | >90% |
| **NPS** | 20-40 | 70+ | >75 |

### Drivers de Retention em CBC

| Driver | Impacto | Como Medir |
|--------|---------|------------|
| **Fixed Schedule** | Cria urgencia | Completion vs prazo |
| **Cohort Peers** | Accountability social | Interacoes entre pares |
| **Live Sessions** | Engagement real-time | Attendance rate |
| **Projects/Deliverables** | Skin in the game | Submission rate |
| **High Price** | Commitment financeiro | Correlacao preco x completion |
```

---

## FASE 3: COHORT COMPARISON

### Step 3.1: Framework de Comparacao

```markdown
## Comparacao de Cohorts - Framework

### DIMENSAO 1: Temporal (Mes a Mes)

| Pergunta | O que revela |
|----------|--------------|
| Cohort de Janeiro vs Fevereiro? | Sazonalidade |
| Pre vs Pos lancamento de feature? | Impacto de produto |
| Pre vs Pos mudanca de preco? | Elasticidade |
| Pre vs Pos redesign de onboarding? | Eficacia de UX |

### Template de Comparacao Temporal

| Metrica | Cohort A (Jan) | Cohort B (Fev) | Delta | Significativo? |
|---------|----------------|----------------|-------|----------------|
| N inicial | [___] | [___] | [___]% | - |
| M1 Retention | [___]% | [___]% | [___]pp | [___] |
| M3 Retention | [___]% | [___]% | [___]pp | [___] |
| CLV Projetado | R$[___] | R$[___] | [___]% | [___] |

### DIMENSAO 2: Canal de Aquisicao

| Canal | Volume | M1 Ret | M3 Ret | CAC | CLV | CLV/CAC |
|-------|--------|--------|--------|-----|-----|---------|
| Organic | [___] | [___]% | [___]% | R$[___] | R$[___] | [___]x |
| Paid Google | [___] | [___]% | [___]% | R$[___] | R$[___] | [___]x |
| Paid Meta | [___] | [___]% | [___]% | R$[___] | R$[___] | [___]x |
| Referral | [___] | [___]% | [___]% | R$[___] | R$[___] | [___]x |

### DIMENSAO 3: Comportamento Inicial

| Comportamento | N | M1 Ret | M3 Ret | Insight |
|---------------|---|--------|--------|---------|
| Completou onboarding <24h | [___] | [___]% | [___]% | [insight] |
| Completou onboarding >24h | [___] | [___]% | [___]% | [insight] |
| Nao completou onboarding | [___] | [___]% | [___]% | [insight] |
| Convidou alguem W1 | [___] | [___]% | [___]% | [insight] |
| Usou feature X | [___] | [___]% | [___]% | [insight] |
```

### Step 3.2: Analise de Significancia Estatistica

```markdown
## Significancia Estatistica na Comparacao

### Por que importa

"Cohort A tem 25% de retencao e Cohort B tem 28%."
Isso e significativo ou apenas ruido?

### Teste de Proporcoes (Chi-quadrado)

```
H0: Retencao de A = Retencao de B
H1: Retencao de A != Retencao de B

Calculo simplificado:
- n_A, n_B = tamanhos das amostras
- p_A, p_B = proporcoes de retencao
- p_pooled = (n_A * p_A + n_B * p_B) / (n_A + n_B)

Z = (p_A - p_B) / sqrt(p_pooled * (1 - p_pooled) * (1/n_A + 1/n_B))

Se |Z| > 1.96, diferenca e significativa (p < 0.05)
```

### Calculadora de Tamanho de Amostra

| Baseline | Delta Minimo Detectavel | Tamanho Necessario (cada) |
|----------|-------------------------|---------------------------|
| 20% | 5pp (20% -> 25%) | ~600 |
| 20% | 3pp (20% -> 23%) | ~1,600 |
| 50% | 5pp (50% -> 55%) | ~780 |
| 50% | 3pp (50% -> 53%) | ~2,100 |

### Regra Pratica

```
Para detectar diferenca de X pontos percentuais:
N minimo por grupo ≈ 2 * (p * (1-p)) / (X/100)^2

Exemplo: Detectar 5pp de diferenca em retencao de 30%
N ≈ 2 * (0.30 * 0.70) / (0.05)^2 = 168

Com margem de seguranca, use 200-300 por grupo.
```
```

### Step 3.3: Cohort Comparison Visualization

```
## Visualizacao de Comparacao de Cohorts

### GRAFICO 1: Retention Curves Sobrepostas

```
  100% ─┬───●───────────────────────────────────────
        │   │╲ Cohort Jan (baseline)
        │   │ ╲
   80%  │   │  ╲____
        │   │       ╲
        │   │        ╲ ● Cohort Fev (worse)
   60%  │   │         ╲
        │   │          ╲___
        │   │              ╲
   40%  │   │               ╲___
        │   │                   ╲______
        │   │                          ╲___
   20%  │   │  ○ Cohort Mar (better)
        │   │   ○─────○─────○─────○──────────
        │   │
    0%  └───┴────────────────────────────────────
            M0   M1   M2   M3   M6   M12
```

### GRAFICO 2: Heatmap de Cohorts

```
         M0    M1    M2    M3    M4    M5    M6
Jan 24  100%  [72%] [55%] [42%] [35%] [30%] [28%]
        ████  ████  ████  ████  ███   ███   ██

Fev 24  100%  [68%] [50%] [38%] [32%] [27%]
        ████  ███   ███   ███   ██    ██

Mar 24  100%  [75%] [60%] [48%] [40%]
        ████  ████  ████  ████  ███

LEGENDA:
████ >60%  ███ 40-60%  ██ 20-40%  █ <20%
```

### GRAFICO 3: Comparacao por Canal (Bar Chart)

```
M3 Retention por Canal

Referral      |██████████████████████| 45%
Organic       |████████████████████| 38%
Paid Google   |███████████████| 28%
Paid Meta     |█████████████| 22%
              0%   10%   20%   30%   40%   50%
```
```

---

## FASE 4: INSIGHTS EXTRACTION

### Step 4.1: Framework de Extracao de Insights

```markdown
## Framework de Insights - DICE

### D - Describe (Descrever)

| Pergunta | Sua Resposta |
|----------|--------------|
| O que os numeros dizem literalmente? | [___] |
| Qual cohort performa melhor? | [___] |
| Qual cohort performa pior? | [___] |
| Ha tendencia ao longo do tempo? | [___] |

### I - Interpret (Interpretar)

| Pergunta | Sua Resposta |
|----------|--------------|
| Por que isso pode estar acontecendo? | [___] |
| O que mudou entre cohorts? | [___] |
| Qual e a causa provavel? | [___] |
| Ha fatores externos? | [___] |

### C - Compare (Comparar)

| Pergunta | Sua Resposta |
|----------|--------------|
| Como estamos vs benchmark? | [___] |
| Como estamos vs concorrentes? | [___] |
| Como estamos vs nosso historico? | [___] |
| O delta e significativo? | [___] |

### E - Execute (Executar)

| Pergunta | Sua Resposta |
|----------|--------------|
| O que devemos fazer com isso? | [___] |
| Qual acao imediata? | [___] |
| Qual acao de medio prazo? | [___] |
| Como vamos medir impacto? | [___] |
```

### Step 4.2: Patterns Comuns em Cohort Analysis

```markdown
## Patterns e o que Significam

### PATTERN 1: Todas as Curvas Melhorando

```
VISUAL:
Cohort Jan: ─────────────
Cohort Fev:  ──────────────
Cohort Mar:   ────────────────

INTERPRETACAO:
- Produto melhorando ao longo do tempo
- Onboarding mais eficaz
- Market fit aumentando

ACAO:
- Identificar o que mudou
- Dobrar a aposta
- Documentar best practices
```

### PATTERN 2: Todas as Curvas Piorando

```
VISUAL:
Cohort Jan: ────────────────
Cohort Fev:  ──────────────
Cohort Mar:   ─────────────

INTERPRETACAO:
- Qualidade de aquisicao caindo
- Produto perdendo relevancia
- Concorrencia aumentando
- Bug ou problema de UX

ACAO:
- Investigar urgentemente
- Checar mudancas recentes
- Revisar canais de aquisicao
- Entrevistar churned users
```

### PATTERN 3: Um Canal Muito Melhor

```
VISUAL:
Referral:    ──────────────────────
Organic:     ─────────────────
Paid:        ─────────────

INTERPRETACAO:
- Referrals sao mais qualificados
- Proof social funciona
- Paid traz usuarios menos engajados

ACAO:
- Investir em programa de referral
- Aumentar share of wallet em referral
- Melhorar qualificacao de paid
```

### PATTERN 4: Drop Inicial Alto, Depois Estabiliza

```
VISUAL:
100% ─┐
      │
40%   └────────────────────

INTERPRETACAO:
- Problema severo de ativacao
- Expectativa vs realidade
- Onboarding nao entrega valor rapido

ACAO:
- Redesenhar onboarding
- Acelerar time-to-value
- Melhorar comunicacao pre-signup
```

### PATTERN 5: Decay Constante (Sem Plateau)

```
VISUAL:
100% ─┐
      │╲
      │ ╲
      │  ╲
  0%      ╲

INTERPRETACAO:
- Sem core users formando habito
- Problema de product-market fit
- Valor nao e suficiente para retenção

ACAO:
- Investigar por que ninguem fica
- Revisar proposta de valor
- Considerar pivot de produto
```

### PATTERN 6: Cohort Course Completion Drop por Semana

```
VISUAL:
W1: 95%
W2: 80%
W3: 60%
W4: 45%

INTERPRETACAO (Wes Kao):
- Conteudo semana 3 pode ser problemático
- Ponto de desistência identificado
- Falta de accountability mid-course

ACAO:
- Redesenhar semana 3
- Adicionar checkpoint mid-course
- Aumentar interacao pares semana 2-3
```
```

### Step 4.3: Template de Documento de Insights

```markdown
# Cohort Analysis Insights - [Data]

## Executive Summary

### Headline
[Uma frase que resume o principal insight]

### Numero Chave
[Metrica mais importante com contexto]

### Recomendacao Principal
[Acao mais critica a tomar]

---

## Insights Detalhados

### Insight 1: [Titulo]

**Observacao:**
[O que os dados mostram]

**Interpretacao:**
[Por que acreditamos que isso acontece]

**Impacto:**
[Qual o impacto no negocio]

**Acao Recomendada:**
[O que fazer a respeito]

**Metrica de Sucesso:**
[Como saberemos se a acao funcionou]

---

### Insight 2: [Titulo]
[Mesmo formato]

---

## Proximos Passos

| Acao | Responsavel | Prazo | KPI |
|------|-------------|-------|-----|
| [Acao 1] | [Nome] | [Data] | [Metrica] |
| [Acao 2] | [Nome] | [Data] | [Metrica] |

---

## Appendix

### Dados Brutos
[Link para dados]

### Metodologia
[Como a analise foi feita]

### Limitacoes
[O que a analise nao captura]
```

---

## FASE 5: VISUALIZATION RECOMMENDATIONS

### Step 5.1: Principios de Visualizacao (Kaushik + Fader)

```markdown
## Principios de Visualizacao de Cohorts

### PRINCIPIO 1: So What Test (Avinash Kaushik)

"Todo grafico deve responder: E dai? O que faco com isso?"

ERRADO:
- Mostrar retencao sem contexto
- Grafico bonito que nao leva a acao

CERTO:
- Destacar anomalias
- Incluir benchmark
- Sugerir acao no titulo

### PRINCIPIO 2: Comparacao Visual (Fader)

"Mostrar heterogeneidade e mais importante que mostrar medias."

ERRADO:
- Mostrar apenas retencao media
- Agregar todos os cohorts

CERTO:
- Mostrar cada cohort separadamente
- Destacar variancia entre cohorts
- Identificar outliers

### PRINCIPIO 3: Storytelling com Dados

"O grafico deve contar uma historia, nao apenas mostrar numeros."

ESTRUTURA:
1. SETUP: O que estamos olhando?
2. CONFLITO: O que nao esta funcionando?
3. RESOLUCAO: O que podemos fazer?
```

### Step 5.2: Tipos de Visualizacao Recomendados

```markdown
## Catalogo de Visualizacoes

### 1. RETENTION HEATMAP (Recomendado)

**Quando Usar:** Visao geral de multiplos cohorts

```
         M0   M1   M2   M3   M4   M5   M6
Jan 24  100  72   55   42   35   30   28
Fev 24  100  68   50   38   32   27   --
Mar 24  100  75   60   48   40   --   --
Apr 24  100  70   52   --   --   --   --

Cor: Verde = alto, Amarelo = medio, Vermelho = baixo
```

**Pros:**
- Visualiza todos os dados de uma vez
- Identifica padroes rapidamente
- Mostra tendencias temporais

**Cons:**
- Pode ser overwhelming com muitos cohorts
- Dificil comparar curvas especificas

---

### 2. LINE CHART - CURVAS SOBREPOSTAS

**Quando Usar:** Comparar 2-5 cohorts especificos

```
100% ─┬─●─────────────────────
      │ │╲  ● Cohort A
      │ │ ○─○──○──○──○──○  ○ Cohort B
 50%  │ │   ╲
      │ │    ╲__●__●__●__●
      │ │
  0%  └─┴────────────────────────
        M0  M1  M2  M3  M4  M5  M6
```

**Pros:**
- Comparacao direta entre cohorts
- Mostra forma da curva claramente
- Identifica ponto de divergencia

**Cons:**
- Fica confuso com muitos cohorts
- Dificil ver valores exatos

---

### 3. BAR CHART - RETENTION POR PERIODO

**Quando Usar:** Comparar retention em momento especifico

```
M3 Retention por Cohort

Jan 24  |████████████████| 42%
Fev 24  |██████████████| 38%
Mar 24  |██████████████████| 48%
Apr 24  |█████████████| 35%
        0%      25%      50%
```

**Pros:**
- Comparacao clara em ponto especifico
- Facil identificar melhor/pior
- Ordenavel por valor

**Cons:**
- Perde visao da curva completa
- Nao mostra tendencia

---

### 4. COHORT FUNNEL

**Quando Usar:** Cursos cohort-based, onboarding

```
Enrolled  → Week 1 → Week 2 → Week 3 → Complete
  1000       930      890      820      780
 (100%)     (93%)    (89%)    (82%)    (78%)
   |         |        |        |        |
   ▼         ▼        ▼        ▼        ▼
  ████      ████     ████     ███      ███
```

**Pros:**
- Mostra progressao claramente
- Identifica maior drop-off
- Intuitivo para stakeholders

---

### 5. RETENTION CURVE + PROJECTION

**Quando Usar:** Projetar retencao futura (Modelo sBG)

```
100% ─┬─●─────────────────────────────────
      │ │╲
      │ │ ╲  ● Observado
      │ │  ╲
 50%  │ │   ╲●
      │ │    ╲
      │ │     ╲●
      │ │      ╲  ○ Projetado (modelo sBG)
 25%  │ │       ╲●
      │ │        ○──○──○──○──○──○
      │ │
  0%  └─┴────────────────────────────────
        M0  M1  M2  M3  M4  M5  M6  M7  M8
```

**Pros:**
- Visualiza projecao vs real
- Valida modelo
- Ajuda planejamento

---

### 6. DUAL AXIS - RETENTION + REVENUE

**Quando Usar:** Conectar retention com impacto financeiro

```
      Retention                    Revenue
100% ─┬───────────────────────── $50k
      │  ●
      │   ╲
 50%  │    ●                    $25k
      │     ╲  ○──○──○──○
      │      ●__●__●__●
      │
  0%  └───────────────────────── $0
        M0  M1  M2  M3  M4  M5

● Retention    ○ Cumulative Revenue
```
```

### Step 5.3: Dashboard Recomendado

```markdown
## Layout de Dashboard de Cohort Analysis

### SECAO 1: KPIs PRINCIPAIS (Topo)

┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  D7 RETENTION    M1 RETENTION    M3 RETENTION    LTV MEDIO   │
│     32%             24%             15%           $180       │
│   (+3% vs ant)    (-2% vs ant)   (+1% vs ant)  (+$20 vs ant) │
│                                                               │
└─────────────────────────────────────────────────────────────┘

### SECAO 2: RETENTION HEATMAP (Centro Esquerdo)

┌─────────────────────────────────┐
│      Cohort Retention Heatmap   │
│                                 │
│      M0  M1  M2  M3  M4  M5    │
│ Jan  ██  ██  █▓  █░  █░  █░    │
│ Fev  ██  ██  █▓  █░  █░        │
│ Mar  ██  ██  █▓  █▓            │
│ Apr  ██  ██  █░                │
│                                 │
└─────────────────────────────────┘

### SECAO 3: CURVAS COMPARATIVAS (Centro Direito)

┌─────────────────────────────────┐
│    Top vs Bottom Cohort         │
│                                 │
│    ●───●───●───●  Mar (best)   │
│    ○───○──○──○    Apr (worst)  │
│                                 │
│    M0   M1   M2   M3            │
└─────────────────────────────────┘

### SECAO 4: RETENTION POR CANAL (Inferior Esquerdo)

┌─────────────────────────────────┐
│  M3 Retention by Channel        │
│                                 │
│  Referral  ████████████ 45%    │
│  Organic   █████████ 35%       │
│  Paid      █████ 22%           │
│                                 │
└─────────────────────────────────┘

### SECAO 5: ALERTAS E INSIGHTS (Inferior Direito)

┌─────────────────────────────────┐
│  Insights & Alerts              │
│                                 │
│  ⚠️ Cohort Abril com drop de   │
│     15% no M1 vs baseline       │
│                                 │
│  ✅ Referrals mantendo 45%     │
│     de M3 retention             │
│                                 │
│  📊 Acao: Investigar onboarding │
│     de Abril                    │
└─────────────────────────────────┘
```

---

## FASE 6: ACTION PLAN BY COHORT

### Step 6.1: Playbooks por Situacao

```markdown
## Playbooks de Intervencao

### SITUACAO 1: Cohort com Retention Inicial Baixa (D1-D7)

**Diagnostico:** Problema de ativacao

**Acoes Imediatas:**
1. Revisar onboarding flow
2. Identificar "Aha moment" e acelera-lo
3. Implementar welcome sequence
4. Adicionar guidance in-app

**Metricas de Sucesso:**
- D1 retention +10pp
- Time to first value -30%
- Setup completion +20%

---

### SITUACAO 2: Cohort com Decay Rapido (M1-M3)

**Diagnostico:** Problema de valor percebido

**Acoes Imediatas:**
1. Entrevistar churned users (5-10)
2. Mapear features mais usadas por retained vs churned
3. Criar re-engagement campaign
4. Revisar proposta de valor

**Metricas de Sucesso:**
- M3 retention +5pp
- Feature adoption +25%
- Reactivation rate 10%+

---

### SITUACAO 3: Canal com Performance Ruim

**Diagnostico:** Problema de qualidade de aquisicao

**Acoes Imediatas:**
1. Revisar targeting do canal
2. Comparar messaging pre-signup com realidade
3. Implementar qualification no signup
4. Ajustar ou pausar canal

**Metricas de Sucesso:**
- M1 retention do canal +10pp
- CLV/CAC do canal >3x
- Qualified lead rate +15%

---

### SITUACAO 4: Course Completion Caindo Mid-Course (Wes Kao)

**Diagnostico:** Problema de engajamento ou conteudo

**Acoes Imediatas:**
1. Adicionar accountability checkpoint
2. Criar sub-grupos de estudo
3. Redesenhar semana problematica
4. Implementar reminder system

**Metricas de Sucesso:**
- Mid-course completion +20pp
- Engagement score +25%
- Project submission +15%

---

### SITUACAO 5: Nenhum Cohort com Plateau Saudavel

**Diagnostico:** Problema de product-market fit

**Acoes Imediatas:**
1. Fazer PMF survey (Sean Ellis Test)
2. Identificar segmento com melhor retention
3. Focar nesse segmento
4. Considerar pivot se <40% "muito desapontado"

**Metricas de Sucesso:**
- Identificar segmento com M6 retention >15%
- PMF score >40%
- Core user base definido
```

### Step 6.2: Template de Plano de Acao

```markdown
## Plano de Acao - Cohort [Nome]

### CONTEXTO

| Item | Valor |
|------|-------|
| Cohort Analisado | [Nome/Data] |
| N Inicial | [___] usuarios |
| Retention Atual (M3) | [___]% |
| Retention Target (M3) | [___]% |
| Gap | [___] pontos percentuais |

### DIAGNOSTICO

**Problema Identificado:**
[Descricao do problema principal]

**Evidencias:**
- [Dado 1]
- [Dado 2]
- [Dado 3]

**Hipotese:**
[Por que acreditamos que isso esta acontecendo]

### PLANO DE ACAO

#### SEMANA 1-2: Quick Wins

| Acao | Owner | Status | KPI |
|------|-------|--------|-----|
| [Acao 1] | [Nome] | [ ] | [Metrica] |
| [Acao 2] | [Nome] | [ ] | [Metrica] |

#### SEMANA 3-4: Implementacoes

| Acao | Owner | Status | KPI |
|------|-------|--------|-----|
| [Acao 1] | [Nome] | [ ] | [Metrica] |
| [Acao 2] | [Nome] | [ ] | [Metrica] |

#### MES 2: Validacao

| Acao | Owner | Status | KPI |
|------|-------|--------|-----|
| [Acao 1] | [Nome] | [ ] | [Metrica] |

### METRICAS DE ACOMPANHAMENTO

| Metrica | Baseline | Semana 2 | Semana 4 | Mes 2 |
|---------|----------|----------|----------|-------|
| D7 Retention | [___]% | [___]% | [___]% | [___]% |
| M1 Retention | [___]% | - | [___]% | [___]% |
| M3 Retention | [___]% | - | - | [___]% |

### RISCOS E MITIGACAO

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| [Risco 1] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [Acao] |
| [Risco 2] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [Acao] |
```

---

## FASE 7: FERRAMENTAS E RECURSOS

### Step 7.1: Ferramentas Recomendadas

```markdown
## Ferramentas para Cohort Analysis

### ANALYTICS PLATFORMS

| Ferramenta | Melhor Para | Preco |
|------------|-------------|-------|
| **Amplitude** | Product analytics, cohorts complexos | Freemium |
| **Mixpanel** | Event tracking, cohorts | Freemium |
| **PostHog** | Open source, product analytics | Free / Paid |
| **GA4** | Web analytics, cohorts basicos | Free |

### BI / VISUALIZATION

| Ferramenta | Melhor Para | Preco |
|------------|-------------|-------|
| **Looker** | Data modeling, dashboards | Paid |
| **Metabase** | Open source BI | Free / Paid |
| **Tableau** | Visualizacoes complexas | Paid |
| **Google Sheets** | Analises rapidas | Free |

### CUSTOMER SUCCESS

| Ferramenta | Melhor Para | Preco |
|------------|-------------|-------|
| **Gainsight** | Health score, churn prediction | Enterprise |
| **ChurnZero** | Customer success automation | Paid |
| **Vitally** | B2B customer success | Paid |

### EDUCACAO / COURSES

| Ferramenta | Melhor Para | Preco |
|------------|-------------|-------|
| **Maven** | Cohort-based courses | Revenue share |
| **Circle** | Community + courses | Paid |
| **Teachable** | Self-paced + cohort | Paid |
```

### Step 7.2: Templates Prontos

```markdown
## Templates Disponiveis

### Google Sheets Templates

1. **Cohort Retention Heatmap**
   - Link: [criar template]
   - Uso: Cole dados, visualize heatmap automaticamente

2. **sBG Model Calculator**
   - Link: [criar template]
   - Uso: Insira retention, obtenha projecao

3. **Channel Comparison Dashboard**
   - Link: [criar template]
   - Uso: Compare canais lado a lado

### SQL Query Library

1. **Acquisition Cohort Query** (Seção 1.3)
2. **Channel Cohort Query** (Seção 1.3)
3. **Course Completion Query** (Seção 1.3)
```

---

## FASE 8: BENCHMARKS POR INDUSTRIA

### Step 8.1: Benchmarks de Retention

```markdown
## Benchmarks de Retention por Industria

### SaaS B2B

| Metrica | P25 | P50 (Mediana) | P75 | P90 |
|---------|-----|---------------|-----|-----|
| M1 Retention | 60% | 75% | 85% | 92% |
| M3 Retention | 40% | 55% | 70% | 82% |
| M12 Retention | 20% | 35% | 50% | 65% |
| Logo Retention Annual | 75% | 85% | 92% | 97% |

### SaaS B2C

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| M1 Retention | 25% | 40% | 55% | 68% |
| M3 Retention | 12% | 22% | 35% | 48% |
| M12 Retention | 5% | 12% | 22% | 35% |

### Mobile Apps (Non-Gaming)

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| D1 Retention | 15% | 25% | 35% | 45% |
| D7 Retention | 8% | 15% | 22% | 32% |
| D30 Retention | 4% | 8% | 14% | 22% |

### E-commerce

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Repeat Purchase 90d | 15% | 25% | 35% | 45% |
| Repeat Purchase 365d | 25% | 40% | 55% | 68% |

### Online Courses (MOOC)

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Week 1 Completion | 25% | 40% | 55% | 70% |
| Overall Completion | 3% | 8% | 15% | 25% |

### Cohort-Based Courses (CBC)

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Week 1 to Course | 75% | 85% | 92% | 96% |
| Overall Completion | 55% | 75% | 88% | 95% |
```

### Step 8.2: Comparacao com Benchmark

```markdown
## Sua Posicao vs Benchmark

### Template de Comparacao

| Metrica | Seu Valor | Benchmark P50 | vs Benchmark | Quartil |
|---------|-----------|---------------|--------------|---------|
| M1 Retention | [___]% | [___]% | [+/-___]pp | [___] |
| M3 Retention | [___]% | [___]% | [+/-___]pp | [___] |
| M6 Retention | [___]% | [___]% | [+/-___]pp | [___] |
| M12 Retention | [___]% | [___]% | [+/-___]pp | [___] |

### Interpretacao

**ACIMA DO P50:**
- Metricas: [lista]
- Insight: [o que esta funcionando]
- Acao: Manter e escalar

**ABAIXO DO P50:**
- Metricas: [lista]
- Insight: [gap identificado]
- Acao: Priorizar melhoria

**PRIORIDADE #1:**
[Metrica mais critica para melhorar]
```

---

## OUTPUT FINAL

### Deliverables

Ao completar esta task, voce tera:

1. **Cohort Definition Matrix** - Definicao clara de todos os cohorts analisados
2. **Retention Curves Analysis** - Curvas de retencao com interpretacao
3. **Cohort Comparison Report** - Comparacao detalhada entre cohorts
4. **Insights Extraction Document** - Documento com insights DICE
5. **Visualization Recommendations** - Dashboard e graficos recomendados
6. **Action Plan by Cohort** - Plano de acao especifico

### Template de Relatorio Executivo

```markdown
# Cohort Analysis Report
## [Empresa/Produto] - [Data]

### Executive Summary

**Headline:**
[Uma frase que resume o principal insight]

**Numero Chave:**
[Metrica mais importante com contexto]

**Recomendacao Principal:**
[Acao mais critica a tomar]

---

### Visao Geral de Cohorts

| Cohort | N | M1 | M3 | M6 | Tendencia |
|--------|---|----|----|----|-----------|
| [Cohort 1] | [N] | [%] | [%] | [%] | [↑/↓/→] |
| [Cohort 2] | [N] | [%] | [%] | [%] | [↑/↓/→] |

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

### Retention vs Benchmark

| Metrica | Atual | Benchmark | Gap |
|---------|-------|-----------|-----|
| M1 | [%] | [%] | [+/-] |
| M3 | [%] | [%] | [+/-] |

---

### Plano de Acao (90 Dias)

| Prioridade | Acao | Owner | Prazo | KPI |
|------------|------|-------|-------|-----|
| 1 | [Acao] | [Nome] | [Data] | [Metrica] |
| 2 | [Acao] | [Nome] | [Data] | [Metrica] |
| 3 | [Acao] | [Nome] | [Data] | [Metrica] |

---

### Proxima Analise

- Data: [Data da proxima revisao]
- Foco: [O que sera analisado]
- KPIs a monitorar: [Lista]
```

---

## REFERENCIAS

### Peter Fader
- Paper: "Probability Models for Customer-Base Analysis" (2009)
- Paper: "How to Project Customer Retention" (2007)
- Livro: "Customer Centricity" (2012)
- Livro: "The Customer Centricity Playbook" (2018)
- Modelo: Shifted-Beta-Geometric (sBG) para retention

### Wes Kao
- Maven data: 14x mais retention que MOOCs
- Framework: Course Mechanics Canvas (12 Levers)
- Newsletter: weskao.substack.com
- Podcast: Lenny's Podcast episode

### Bruce Hardie
- Co-autor com Fader em modelos CLV
- Site: brucehardie.com (templates Excel)
- Paper: "Reconciling CLV Formulas"

### Amplitude
- Retention Analysis Documentation
- Cohort Analysis Best Practices

### Sean Ellis
- AARRR Framework aplicado a cohorts
- North Star Metric por cohort

---

## CHECKLIST FINAL

```markdown
## Validacao da Task

### Completude
- [ ] Cohorts definidos claramente (dimensao, granularidade, evento)
- [ ] Dados extraidos via SQL ou ferramenta
- [ ] Retention curves construidas
- [ ] Comparacao entre cohorts feita
- [ ] Significancia estatistica verificada (se aplicavel)
- [ ] Insights extraidos (framework DICE)
- [ ] Visualizacoes criadas
- [ ] Plano de acao documentado

### Qualidade
- [ ] Definicoes consistentes ao longo da analise
- [ ] Dados verificados (sem erros de extracao)
- [ ] Comparacao com benchmark incluida
- [ ] Insights acionaveis (nao apenas descritivos)
- [ ] Recomendacoes especificas com owners e prazos

### Entrega
- [ ] Relatorio executivo pronto
- [ ] Dashboard/visualizacoes compartilhaveis
- [ ] Proximos passos definidos
- [ ] Data da proxima revisao agendada
```

---

## ANTI-PATTERNS

### Erros Comuns a Evitar

1. **Olhar apenas agregados**
   - ERRADO: "Retencao media e 30%"
   - CERTO: "Cohort Jan tem 35%, Fev tem 22%, precisamos investigar"

2. **Definicao inconsistente de "ativo"**
   - ERRADO: Mudar definicao no meio da analise
   - CERTO: Definir upfront e manter consistente

3. **Ignorar tamanho de amostra**
   - ERRADO: "Cohort X tem 80% retention!" (N=20)
   - CERTO: Verificar significancia estatistica

4. **Nao conectar com acoes**
   - ERRADO: Apresentar dados sem recomendacoes
   - CERTO: Cada insight tem uma acao associada

5. **Comparar cohorts incomparaveis**
   - ERRADO: Comparar cohort de 100 usuarios com 10.000
   - CERTO: Normalizar ou comparar similares

6. **Ignorar contexto externo**
   - ERRADO: Culpar produto quando houve feriado
   - CERTO: Considerar fatores externos

---

**Total de Linhas: 1200+**
**Metodologias Integradas: 6** (Fader, Wes Kao, sBG Model, AARRR, DICE, Kaushik)
**Frameworks Incluidos: 10+**
**Templates SQL: 3**
**Benchmarks: 5 industrias**
**Calculadoras: 4** (Retention, Significancia, Projecao, Comparacao)
