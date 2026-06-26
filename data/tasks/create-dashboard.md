# Create Dashboard Task

## Purpose

Criar dashboards efetivos que geram ação, não relatórios decorativos. Este task guia a implementação completa de dashboards usando a metodologia DMMM (Digital Marketing & Measurement Model) de Avinash Kaushik, aplicando o So What Test em cada métrica, seguindo princípios de design de dashboard, organizando métricas em hierarquia (acquisition, behavior, outcomes) e usando storytelling com dados para comunicar insights que movem o negócio.

## Workspace Output Contract

- Preflight: `*workspace-preflight` + `*workspace-context {slug}`
- Output canônico (template-first): `workspace/businesses/{slug}/analytics/executive-report.yaml`
- Output canônico adicional: `workspace/businesses/{slug}/analytics/dmmm.yaml`
- Output custom (ad-hoc): `docs/data/{slug}/dashboard-spec-{date}.md`
- Regra: escrita canônica só se existir template correspondente em `workspace/_templates/analytics/`

---

## Primary Agent

**Avinash Kaushik** - Digital Analytics Evangelist, ex-Google (10+ anos)

> "A maioria das empresas está data-rich e insight-poor. Não faltam dados, faltam decisões."

Kaushik argumenta que dashboards existem para gerar AÇÃO, não para impressionar. Se um dashboard não muda decisões, é desperdício de tempo e dinheiro.

---

## Core Philosophy

### The Dashboard Problem

```yaml
dashboard_problem:

  reality_in_most_companies:
    - "47 métricas no dashboard principal"
    - "Ninguém sabe qual olhar"
    - "Reuniões viram sessões de leitura de números"
    - "Nenhuma decisão é tomada"
    - "Dashboard bonito, empresa perdida"

  kaushik_diagnosis: |
    "Dashboards cheios de dados são um sintoma de medo.
    Medo de escolher o que importa.
    Medo de ser cobrado por algo que não estava lá.
    O resultado? Um mar de números que ninguém usa."

  the_fix:
    principle_1: "Menos métricas, mais insights"
    principle_2: "Toda métrica deve passar no So What Test"
    principle_3: "Dashboard deve responder perguntas, não gerar mais"
    principle_4: "Ação recomendada junto com cada insight"
```

### The 10/90 Rule Applied to Dashboards

```
┌─────────────────────────────────────────────────────────────────┐
│                      10/90 RULE                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ERRADO (como a maioria faz):                                   │
│  ├── 90% do budget em ferramentas de BI                         │
│  ├── 10% em pessoas que interpretam                             │
│  └── Resultado: dashboards bonitos que ninguém usa              │
│                                                                  │
│  CERTO (como deveria ser):                                      │
│  ├── 10% em ferramentas de BI                                   │
│  ├── 90% em analistas que PENSAM sobre os dados                 │
│  └── Resultado: insights que mudam o negócio                    │
│                                                                  │
│  APLICAÇÃO EM DASHBOARDS:                                       │
│  ├── Gastar tempo escolhendo métricas certas                    │
│  ├── Gastar tempo definindo thresholds                          │
│  ├── Gastar tempo escrevendo insights                           │
│  └── NÃO gastar tempo polindo visualizações                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tier 0: Diagnostic Questions

Antes de criar qualquer dashboard, responda estas perguntas diagnósticas:

```yaml
tier_0_diagnosis:

  purpose_clarity:
    - "Quem vai usar este dashboard?"
    - "Qual pergunta principal ele deve responder?"
    - "Que decisões serão tomadas com base nele?"
    - "Com que frequência será consultado?"

  business_context:
    - "Qual é o objetivo de negócio principal?"
    - "Quais são os 3-5 KPIs mais importantes?"
    - "Existe um North Star Metric definido?"
    - "Quais métricas a liderança já acompanha?"

  audience_analysis:
    - "CEO/Board? (precisa de high-level)"
    - "Gerentes? (precisa de operational)"
    - "Analistas? (precisa de detailed)"
    - "Qual é o data literacy do público?"

  existing_landscape:
    - "Que dashboards já existem?"
    - "Por que não estão funcionando?"
    - "Que métricas estão sendo ignoradas?"
    - "Há sobreposição de reports?"

  data_availability:
    - "Os dados necessários estão disponíveis?"
    - "Qual é a latência dos dados? (real-time, daily, weekly)"
    - "Há data quality issues conhecidos?"
    - "Todas as fontes estão integradas?"
```

---

## Inputs

```yaml
required:
  - business_objective: "O objetivo de negócio que o dashboard deve servir"
  - primary_audience: "Quem é o usuário principal (CEO, gerentes, analistas)"
  - key_questions: "As 3-5 perguntas que o dashboard deve responder"
  - data_sources: "Fontes de dados disponíveis"
  - refresh_frequency: "Com que frequência os dados são atualizados"

optional:
  - existing_dashboards: "Dashboards atuais para avaliar"
  - north_star_metric: "Se já definido"
  - target_kpis: "KPIs com targets específicos"
  - comparison_periods: "Períodos de comparação relevantes"
  - user_segments: "Segmentos de usuários a filtrar"
  - mobile_requirement: "Se precisa funcionar em mobile"
```

---

## The DMMM Framework (Digital Marketing & Measurement Model)

### Framework Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                         DMMM FRAMEWORK                              │
│              (Avinash Kaushik - Google)                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  NÍVEL 1: BUSINESS OBJECTIVES                                      │
│  ├── O que a empresa quer alcançar?                                │
│  ├── Ex: "Aumentar revenue em 20%"                                 │
│  └── DASHBOARD: Headline metric                                    │
│                                                                     │
│                        ↓                                            │
│                                                                     │
│  NÍVEL 2: GOALS (por objetivo)                                     │
│  ├── Que comportamentos levam ao objetivo?                          │
│  ├── Ex: "Aumentar conversões", "Reduzir churn"                    │
│  └── DASHBOARD: Primary KPIs section                               │
│                                                                     │
│                        ↓                                            │
│                                                                     │
│  NÍVEL 3: KPIs (por goal)                                          │
│  ├── Como medimos progresso no goal?                               │
│  ├── Ex: "Conversion rate", "Churn rate"                           │
│  └── DASHBOARD: Supporting metrics                                 │
│                                                                     │
│                        ↓                                            │
│                                                                     │
│  NÍVEL 4: TARGETS (por KPI)                                        │
│  ├── Qual número queremos atingir?                                 │
│  ├── Ex: "Conversion rate de 3% → 5%"                              │
│  └── DASHBOARD: Targets e progress bars                            │
│                                                                     │
│                        ↓                                            │
│                                                                     │
│  NÍVEL 5: SEGMENTS (por target)                                    │
│  ├── Para quem especificamente?                                     │
│  ├── Ex: "Novos visitantes de paid search"                         │
│  └── DASHBOARD: Filters e breakdowns                               │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### DMMM Implementation Process

```yaml
dmmm_implementation:

  step_1_define_objectives:
    description: "Definir objetivos de negócio claros"
    questions:
      - "Qual é o objetivo principal da empresa este ano?"
      - "Quais são os 2-3 objetivos secundários?"
      - "Como sucesso é definido?"
    output: "Lista de 1-3 business objectives"
    example:
      primary: "Aumentar MRR em 40%"
      secondary:
        - "Reduzir churn em 20%"
        - "Aumentar NPS para 50"

  step_2_identify_goals:
    description: "Para cada objetivo, identificar goals"
    questions:
      - "Que comportamentos levam a este objetivo?"
      - "O que precisa acontecer para atingir o objetivo?"
      - "Quais são os leading indicators?"
    output: "2-3 goals por objective"
    example:
      objective: "Aumentar MRR em 40%"
      goals:
        - "Aumentar aquisição de novos clientes"
        - "Aumentar expansion revenue"
        - "Reduzir churn"

  step_3_select_kpis:
    description: "Para cada goal, selecionar KPIs"
    questions:
      - "Como sabemos se estamos progredindo?"
      - "O que podemos medir?"
      - "Qual métrica melhor representa o goal?"
    output: "1-2 KPIs por goal"
    example:
      goal: "Aumentar aquisição de novos clientes"
      kpis:
        - "New customers/month"
        - "CAC"

  step_4_set_targets:
    description: "Para cada KPI, definir targets"
    questions:
      - "Qual é o baseline atual?"
      - "O que é alcançável?"
      - "O que seria excepcional?"
    output: "Target numérico por KPI"
    example:
      kpi: "New customers/month"
      baseline: 100
      target: 150
      stretch: 200

  step_5_define_segments:
    description: "Para cada target, identificar segmentos"
    questions:
      - "Para quem especificamente?"
      - "Quais breakdowns são relevantes?"
      - "Onde há mais oportunidade?"
    output: "Segmentos relevantes por KPI"
    example:
      kpi: "New customers/month"
      segments:
        - "By channel (organic, paid, referral)"
        - "By plan type (starter, pro, enterprise)"
        - "By geography"
```

### DMMM Template

```yaml
dmmm_template:

  business_objective: "[OBJETIVO DE NEGÓCIO]"

  goals:
    goal_1:
      name: "[GOAL 1]"
      kpis:
        - name: "[KPI 1.1]"
          current: "[BASELINE]"
          target: "[TARGET]"
          segments: ["[SEGMENT A]", "[SEGMENT B]"]
        - name: "[KPI 1.2]"
          current: "[BASELINE]"
          target: "[TARGET]"
          segments: ["[SEGMENT A]", "[SEGMENT B]"]

    goal_2:
      name: "[GOAL 2]"
      kpis:
        - name: "[KPI 2.1]"
          current: "[BASELINE]"
          target: "[TARGET]"
          segments: ["[SEGMENT A]", "[SEGMENT B]"]

    goal_3:
      name: "[GOAL 3]"
      kpis:
        - name: "[KPI 3.1]"
          current: "[BASELINE]"
          target: "[TARGET]"
          segments: ["[SEGMENT A]", "[SEGMENT B]"]
```

### DMMM Example: E-commerce

```yaml
dmmm_example_ecommerce:

  business_objective: "Aumentar revenue online em 30%"

  goals:

    goal_1:
      name: "Aumentar tráfego qualificado"
      kpis:
        - name: "Sessions from qualified sources"
          current: "50,000/month"
          target: "75,000/month"
          segments:
            - "By channel"
            - "By device"
            - "By landing page"
        - name: "Bounce rate"
          current: "55%"
          target: "45%"
          segments:
            - "By channel"
            - "By page type"

    goal_2:
      name: "Aumentar conversion rate"
      kpis:
        - name: "Overall conversion rate"
          current: "2.5%"
          target: "3.5%"
          segments:
            - "By traffic source"
            - "By product category"
            - "By customer type (new vs returning)"
        - name: "Add to cart rate"
          current: "8%"
          target: "12%"
          segments:
            - "By product"
            - "By device"

    goal_3:
      name: "Aumentar average order value"
      kpis:
        - name: "AOV"
          current: "R$150"
          target: "R$180"
          segments:
            - "By customer type"
            - "By category"
        - name: "Items per order"
          current: "1.8"
          target: "2.2"
          segments:
            - "By source"
            - "By device"
```

### DMMM Example: SaaS

```yaml
dmmm_example_saas:

  business_objective: "Atingir R$5M ARR"

  goals:

    goal_1:
      name: "Aumentar new MRR"
      kpis:
        - name: "New MRR/month"
          current: "R$50k"
          target: "R$80k"
          segments:
            - "By plan"
            - "By channel"
            - "By deal size"
        - name: "New customers/month"
          current: "100"
          target: "150"
          segments:
            - "By source"
            - "By persona"

    goal_2:
      name: "Aumentar expansion MRR"
      kpis:
        - name: "Expansion MRR/month"
          current: "R$15k"
          target: "R$30k"
          segments:
            - "By upgrade type"
            - "By customer tier"
        - name: "Net Revenue Retention"
          current: "105%"
          target: "120%"
          segments:
            - "By cohort"
            - "By plan"

    goal_3:
      name: "Reduzir churn"
      kpis:
        - name: "Monthly churn rate"
          current: "3%"
          target: "2%"
          segments:
            - "By plan"
            - "By tenure"
            - "By health score"
        - name: "Churn MRR"
          current: "R$20k"
          target: "R$12k"
          segments:
            - "By reason"
            - "By customer size"
```

---

## The So What Test

### What is the So What Test?

```
┌─────────────────────────────────────────────────────────────────┐
│                     THE SO WHAT TEST                             │
│           (Avinash Kaushik's Acid Test for Metrics)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Para TODA métrica no dashboard, pergunte:                      │
│                                                                  │
│  "SO WHAT?"                                                     │
│                                                                  │
│  Se você não consegue explicar:                                  │
│  1. Por que essa métrica importa                                │
│  2. O que fazer se ela subir                                    │
│  3. O que fazer se ela cair                                     │
│                                                                  │
│  → REMOVA DO DASHBOARD                                          │
│                                                                  │
│  Métrica sem ação = vanity metric = desperdício de espaço       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### So What Test Framework

```yaml
so_what_test_framework:

  question_1_relevance:
    question: "Por que essa métrica importa para o negócio?"
    good_answer: "Conversion rate importa porque impacta diretamente revenue"
    bad_answer: "Porque todo mundo mede"
    action_if_bad: "Remover do dashboard"

  question_2_action_up:
    question: "O que fazemos se a métrica SUBIR?"
    good_answer: |
      "Se conversion rate subir 20%, dobrar budget do canal
      que mais contribuiu para a mudança"
    bad_answer: "Comemoramos"
    action_if_bad: "Definir ação específica ou remover"

  question_3_action_down:
    question: "O que fazemos se a métrica CAIR?"
    good_answer: |
      "Se conversion rate cair 10%, ativar investigação:
      checar por device, por page, por segment"
    bad_answer: "Investigamos"
    action_if_bad: "Definir playbook específico"

  question_4_threshold:
    question: "Qual é o threshold que dispara ação?"
    good_answer: "Mudança de 5% week-over-week"
    bad_answer: "Quando parecer significativo"
    action_if_bad: "Definir threshold numérico"
```

### So What Test Examples

```yaml
so_what_test_examples:

  metric_passes:
    metric: "Weekly Active Users (WAU)"
    so_what:
      relevance: "WAU é leading indicator de retention e churn"
      action_up: |
        "Se WAU subir 10%+:
        1. Identificar o que mudou (feature, campaign)
        2. Double down na causa
        3. Documentar para replicar"
      action_down: |
        "Se WAU cair 10%+:
        1. Checar por segment (new vs existing)
        2. Checar por feature
        3. Verificar technical issues
        4. Ativar reengagement campaign"
      threshold: "±10% WoW"
    verdict: "PASS - mantém no dashboard"

  metric_fails:
    metric: "Total Page Views"
    so_what:
      relevance: "Indica... volume de acesso?"
      action_up: "Hmm... bom?"
      action_down: "Hmm... ruim?"
      threshold: "Não definido"
    verdict: "FAIL - remover ou substituir por métrica acionável"

  metric_transformed:
    original: "Total Page Views"
    transformed: "Pages per Session by User Type"
    so_what:
      relevance: "Indica engagement e profundidade de interesse"
      action_up: |
        "Se páginas/sessão subir para new users:
        Otimizar paths para conversão mais rápida"
      action_down: |
        "Se páginas/sessão cair:
        Revisar qualidade do conteúdo, checar bounce"
      threshold: "±15% MoM"
    verdict: "PASS - métrica transformada é acionável"
```

### So What Test Worksheet

```yaml
so_what_worksheet:

  instructions: |
    Para cada métrica proposta para o dashboard,
    preencha todas as células. Se não conseguir,
    a métrica não deve estar no dashboard.

  template:
    metric_name: "[NOME DA MÉTRICA]"

    relevance:
      business_impact: "[COMO IMPACTA O NEGÓCIO]"
      connection_to_objective: "[QUAL GOAL/OBJECTIVE SUPORTA]"

    action_playbooks:
      if_increases:
        threshold: "[X% ou valor absoluto]"
        actions:
          - "[AÇÃO 1]"
          - "[AÇÃO 2]"
        owner: "[QUEM EXECUTA]"

      if_decreases:
        threshold: "[X% ou valor absoluto]"
        actions:
          - "[AÇÃO 1]"
          - "[AÇÃO 2]"
        owner: "[QUEM EXECUTA]"

    alert_settings:
      warning_threshold: "[VALOR]"
      critical_threshold: "[VALOR]"
      notification_channel: "[EMAIL/SLACK/ETC]"

    review_frequency: "[DAILY/WEEKLY/MONTHLY]"
```

### So What Filter for Existing Dashboards

```yaml
dashboard_audit_process:

  step_1_list_all_metrics:
    description: "Liste todas as métricas no dashboard atual"
    output: "Lista de métricas"

  step_2_apply_so_what:
    description: "Para cada métrica, aplique o So What Test"
    categories:
      pass: "Mantém no dashboard"
      transform: "Transformar para versão acionável"
      fail: "Remover"

  step_3_categorize:
    typical_results:
      pass: "20-30% das métricas"
      transform: "30-40% das métricas"
      fail: "30-50% das métricas"

  step_4_redesign:
    description: "Redesenhar com apenas métricas que passam"
    benefit: "Dashboard 50-70% mais limpo"

  example_audit:
    before:
      total_metrics: 24
      distribution:
        pass: 5
        transform: 8
        fail: 11

    after:
      total_metrics: 10
      note: "60% reduction in noise"
```

---

## Dashboard Design Principles

### Principle 1: Information Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│              INFORMATION HIERARCHY IN DASHBOARDS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LEVEL 1: HEADLINE (1-3 metrics)                                │
│  ├── North Star or Business Objective metric                    │
│  ├── Biggest, most prominent                                    │
│  ├── Includes comparison (vs last period, vs target)           │
│  └── Example: MRR with trend arrow and % change                │
│                                                                  │
│  LEVEL 2: KEY PERFORMANCE (3-5 metrics)                         │
│  ├── Primary KPIs that drive the headline                       │
│  ├── Medium prominence                                          │
│  ├── Each with sparkline or mini-trend                         │
│  └── Example: New Customers, Churn Rate, ARPU                  │
│                                                                  │
│  LEVEL 3: SUPPORTING (5-8 metrics)                              │
│  ├── Diagnostic metrics that explain KPIs                       │
│  ├── Smaller prominence                                         │
│  ├── Often in tables or small charts                           │
│  └── Example: By channel, by segment breakdowns                │
│                                                                  │
│  LEVEL 4: DETAIL (on demand)                                    │
│  ├── Deep dive data for investigation                          │
│  ├── Hidden behind drill-down or separate page                 │
│  ├── Not shown by default                                       │
│  └── Example: Individual transaction logs, raw data            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Principle 2: Visual Best Practices

```yaml
visual_best_practices:

  color_usage:
    red: "Bad / Below target / Needs attention"
    yellow: "Warning / Approaching threshold"
    green: "Good / Above target / On track"
    gray: "Neutral / Historical / Context"
    rule: "Use color for meaning, not decoration"

  chart_selection:
    use_line_charts:
      - "Trends over time"
      - "Continuous data"
      - "Showing trajectory"
    use_bar_charts:
      - "Comparisons between categories"
      - "Rankings"
      - "Discrete data"
    use_pie_charts:
      - "NEVER (almost)"
      - "Only for 2-3 segments as % of whole"
      - "Replace with bar chart when possible"
    use_tables:
      - "Precise values needed"
      - "Multiple dimensions"
      - "Raw data for analysis"
    use_kpi_cards:
      - "Single important metrics"
      - "Current values with comparison"
      - "Headline metrics"

  layout:
    reading_pattern: "Left to right, top to bottom"
    most_important: "Top left"
    secondary: "Top right and middle"
    supporting: "Bottom"
    filters: "Top or left sidebar"

  density:
    rule: "Less is more"
    max_metrics_per_screen: 12
    whitespace: "Essential, not waste"
    grouping: "Related metrics together"
```

### Principle 3: Context Always

```yaml
context_principles:

  every_metric_needs:
    comparison: "vs last period, vs target, vs benchmark"
    trend: "Direction (up/down arrow)"
    interpretation: "Good or bad indicator"

  comparison_options:
    vs_target:
      description: "Compare to goal"
      format: "85% of target"
      use_when: "Targets are set"

    vs_previous_period:
      description: "Compare to same period before"
      format: "+15% vs last week"
      use_when: "Tracking progress"

    vs_same_period_last_year:
      description: "YoY comparison"
      format: "+25% vs Jan 2024"
      use_when: "Seasonal business"

    vs_benchmark:
      description: "Compare to industry/internal benchmark"
      format: "120% of benchmark"
      use_when: "External context matters"

  never_show_number_alone:
    bad: "Revenue: R$150,000"
    good: "Revenue: R$150,000 (+12% MoM, 95% of target)"
    excellent: "Revenue: R$150,000 (+12% MoM, 95% of target) ▲ On track"
```

### Principle 4: Actionable Annotations

```yaml
actionable_annotations:

  types_of_annotations:
    alerts:
      purpose: "Call attention to anomalies"
      format: "Red banner or icon"
      example: "⚠️ Churn rate 40% above normal"

    insights:
      purpose: "Explain what's happening"
      format: "Text box or callout"
      example: "Spike due to Black Friday campaign"

    recommendations:
      purpose: "Suggest next action"
      format: "Action button or highlighted text"
      example: "→ Investigate top 3 churning segments"

  annotation_placement:
    inline: "Next to the metric it explains"
    summary_box: "At top for critical issues"
    drill_down: "Available on click for details"

  automation:
    anomaly_detection:
      description: "Auto-detect unusual values"
      threshold: "±2 standard deviations"
      action: "Auto-annotate with alert"

    trend_commentary:
      description: "Auto-generate insight text"
      example: "Revenue up 15%, driven by 20% increase in new customers"
```

### Principle 5: Mobile-First (When Applicable)

```yaml
mobile_considerations:

  if_mobile_access_required:
    simplify:
      - "Reduce to 3-5 key metrics"
      - "One metric per row"
      - "Larger tap targets"
      - "Swipe for more detail"

    prioritize:
      - "Most critical KPIs only"
      - "Alerts and exceptions"
      - "Quick status check"

    avoid:
      - "Complex charts"
      - "Data tables"
      - "Multi-dimensional views"

  responsive_design:
    desktop: "Full dashboard with all levels"
    tablet: "Headline + KPIs, supporting on scroll"
    mobile: "Headline + alerts only, tap for more"
```

---

## Metric Hierarchy

### The Three-Tier Metric Model

```
┌─────────────────────────────────────────────────────────────────┐
│           THREE-TIER METRIC MODEL FOR DASHBOARDS                │
│                  (Acquisition → Behavior → Outcomes)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TIER 1: ACQUISITION METRICS                                    │
│  ├── "How are people finding us?"                               │
│  ├── Leading indicators                                         │
│  ├── Input to the funnel                                        │
│  └── Examples:                                                  │
│      • Traffic / Sessions                                       │
│      • New users                                                │
│      • Sign-ups                                                 │
│      • Leads                                                    │
│      • Cost per acquisition                                     │
│                                                                  │
│                        ↓                                         │
│                                                                  │
│  TIER 2: BEHAVIOR METRICS                                       │
│  ├── "What are people doing?"                                   │
│  ├── Engagement indicators                                      │
│  ├── Middle of the funnel                                       │
│  └── Examples:                                                  │
│      • Activation rate                                          │
│      • Feature adoption                                         │
│      • Time in product                                          │
│      • Pages per session                                        │
│      • Return frequency                                         │
│                                                                  │
│                        ↓                                         │
│                                                                  │
│  TIER 3: OUTCOME METRICS                                        │
│  ├── "What results are we getting?"                             │
│  ├── Lagging indicators                                         │
│  ├── Output of the funnel                                       │
│  └── Examples:                                                  │
│      • Revenue / MRR                                            │
│      • Conversions                                              │
│      • Customer Lifetime Value                                  │
│      • Net Promoter Score                                       │
│      • Retention / Churn                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Metric Selection by Dashboard Type

```yaml
metric_selection_by_type:

  executive_dashboard:
    purpose: "High-level business health"
    audience: "CEO, Board, Leadership"
    frequency: "Weekly/Monthly"
    metrics:
      acquisition:
        - "New customers"
        - "CAC"
        - "Pipeline value"
      behavior:
        - "Activation rate"
        - "Weekly Active Users"
        - "Health Score distribution"
      outcomes:
        - "Revenue / MRR / ARR"
        - "Churn rate"
        - "Net Revenue Retention"
        - "CLTV"

  marketing_dashboard:
    purpose: "Marketing performance"
    audience: "CMO, Marketing team"
    frequency: "Daily/Weekly"
    metrics:
      acquisition:
        - "Traffic by source"
        - "MQLs generated"
        - "CPL by channel"
        - "Brand awareness metrics"
      behavior:
        - "Email engagement (open, click)"
        - "Content engagement"
        - "Landing page performance"
      outcomes:
        - "Conversions by channel"
        - "ROAS by campaign"
        - "Attribution analysis"

  product_dashboard:
    purpose: "Product usage and health"
    audience: "CPO, Product team"
    frequency: "Daily/Weekly"
    metrics:
      acquisition:
        - "New sign-ups"
        - "Trial starts"
        - "Feature discovery rate"
      behavior:
        - "DAU / WAU / MAU"
        - "Feature adoption rates"
        - "Time in product"
        - "Actions per session"
      outcomes:
        - "Activation rate"
        - "Retention curves"
        - "Product-qualified leads"
        - "Feature-level NPS"

  customer_success_dashboard:
    purpose: "Customer health and retention"
    audience: "CCO, CS team"
    frequency: "Daily/Weekly"
    metrics:
      acquisition:
        - "New accounts onboarded"
        - "Expansion opportunities"
      behavior:
        - "Health Score"
        - "Engagement trends"
        - "Support ticket volume"
        - "NPS responses"
      outcomes:
        - "Churn rate"
        - "Net Revenue Retention"
        - "Customer Lifetime Value"
        - "Expansion revenue"

  sales_dashboard:
    purpose: "Sales performance and pipeline"
    audience: "CRO, Sales team"
    frequency: "Daily/Weekly"
    metrics:
      acquisition:
        - "Leads received"
        - "SQLs generated"
        - "Meetings booked"
      behavior:
        - "Pipeline velocity"
        - "Win rate by stage"
        - "Average deal cycle"
        - "Activity metrics"
      outcomes:
        - "Revenue closed"
        - "Average deal size"
        - "Quota attainment"
        - "Forecast accuracy"
```

### Leading vs Lagging Indicator Balance

```yaml
leading_lagging_balance:

  principle: |
    Dashboards should have a mix of leading (predictive)
    and lagging (result) indicators. Leading indicators
    give you time to act before outcomes change.

  ideal_ratio:
    leading: "40-50%"
    lagging: "50-60%"

  examples:

    revenue_dashboard:
      lagging:
        - "Revenue (what happened)"
        - "Churn rate (what happened)"
      leading:
        - "Pipeline value (predicts revenue)"
        - "Health Score (predicts churn)"
        - "NPS (predicts retention)"

    product_dashboard:
      lagging:
        - "Retention rate (what happened)"
        - "CLTV (what happened)"
      leading:
        - "Activation rate (predicts retention)"
        - "Feature adoption (predicts value)"
        - "Weekly Active Users (predicts retention)"

  diagnostic_question: |
    "Can we predict the lagging metrics using the
    leading metrics in this dashboard?"
    If yes → good balance
    If no → add more leading indicators
```

---

## Storytelling with Data

### The Narrative Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                  DATA STORYTELLING FRAMEWORK                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  EVERY DASHBOARD TELLS A STORY:                                 │
│                                                                  │
│  1. SETUP (Context)                                             │
│     "Here's where we are and where we're trying to go"          │
│     → Headline metrics vs targets                               │
│                                                                  │
│  2. CONFLICT (Problem)                                          │
│     "Here's what's not working or needs attention"              │
│     → Anomalies, misses, concerning trends                      │
│                                                                  │
│  3. RESOLUTION (Insight)                                        │
│     "Here's why it's happening"                                 │
│     → Root cause analysis, segment breakdown                    │
│                                                                  │
│  4. CALL TO ACTION (Next Steps)                                 │
│     "Here's what we should do about it"                         │
│     → Specific recommendations                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The So What Framework for Storytelling

```yaml
so_what_storytelling:

  section_1_so_what:
    question: "Por que isso importa?"
    dashboard_element: "Context card or subtitle"
    template: |
      "[METRIC] is currently at [VALUE], which is [X%] [above/below]
      our target of [TARGET]. This matters because [BUSINESS IMPACT]."
    example: |
      "MRR is currently at R$450k, which is 10% below our target
      of R$500k. This matters because we need R$6M ARR by December
      to hit our funding milestone."

  section_2_what_changed:
    question: "O que mudou desde a última análise?"
    dashboard_element: "Comparison indicators and trend lines"
    template: |
      "Compared to [PREVIOUS PERIOD], [METRIC] has [increased/decreased]
      by [X%]. The main changes were:
      • [CHANGE 1]
      • [CHANGE 2]
      • [CHANGE 3]"
    example: |
      "Compared to last month, MRR has decreased by 2%. The main changes were:
      • New MRR down 15% (fewer large deals closed)
      • Churn MRR up 8% (3 enterprise accounts cancelled)
      • Expansion MRR flat (no significant upsells)"

  section_3_why:
    question: "Por que mudou?"
    dashboard_element: "Breakdown charts and diagnostic metrics"
    template: |
      "The [change] is primarily driven by:
      1. [ROOT CAUSE 1] contributing [X%]
      2. [ROOT CAUSE 2] contributing [Y%]
      Evidence: [DATA POINT]"
    example: |
      "The MRR decline is primarily driven by:
      1. Sales team vacancy (2 reps quit) contributing 60%
      2. Enterprise churn (lost 3 accounts to competitor) contributing 40%
      Evidence: Win rate dropped from 35% to 22%, and churn was
      concentrated in accounts with <6 months tenure."

  section_4_now_what:
    question: "O que vamos fazer?"
    dashboard_element: "Recommendation box or action items"
    template: |
      "Recommended actions:
      1. [ACTION 1] - Owner: [NAME] - Due: [DATE]
      2. [ACTION 2] - Owner: [NAME] - Due: [DATE]
      Expected impact: [PROJECTED CHANGE]"
    example: |
      "Recommended actions:
      1. Accelerate sales hiring (2 reps by March) - Owner: CRO - Due: Mar 15
      2. Executive review of 3 churned accounts for learnings - Owner: CCO - Due: This week
      3. Implement early warning system for <6mo accounts - Owner: CS Ops - Due: Mar 1
      Expected impact: Return to target MRR growth by Q2"
```

### Visual Storytelling Techniques

```yaml
visual_storytelling:

  technique_1_progressive_disclosure:
    description: "Reveal information in layers"
    implementation:
      level_1: "Summary (the answer)"
      level_2: "Supporting data (the evidence)"
      level_3: "Detail (the raw data)"
    benefit: "Audience can go as deep as they want"

  technique_2_annotation_layers:
    description: "Add context to charts"
    types:
      events: "Mark when campaigns launched, features shipped"
      anomalies: "Highlight unusual data points"
      explanations: "Add text explaining changes"
    implementation: "Overlay on line charts, callout boxes"

  technique_3_guided_analysis:
    description: "Lead viewer through the story"
    elements:
      numbers: "1, 2, 3... sequence of attention"
      arrows: "Visual flow between elements"
      highlighting: "Bold important numbers"
      summary_box: "Key takeaway at top"

  technique_4_comparison_framing:
    description: "Make changes obvious"
    techniques:
      before_after: "Side by side comparison"
      target_vs_actual: "Bar chart with target line"
      indexed_charts: "Start at 100, show relative change"
      sparklines: "Inline trend context"

  technique_5_emotional_cues:
    description: "Use visual cues for meaning"
    colors:
      red: "Needs attention, bad"
      green: "Good, on track"
      yellow: "Warning, watch"
    icons:
      up_arrow: "Increasing (add color for good/bad)"
      down_arrow: "Decreasing (add color for good/bad)"
      warning: "Alert, needs investigation"
      checkmark: "Target hit, goal achieved"
```

### Dashboard Narrative Templates

```yaml
narrative_templates:

  executive_update:
    structure:
      - title: "Performance Summary"
        content: "1-3 sentence headline of status"
      - title: "Key Wins"
        content: "2-3 positive highlights with evidence"
      - title: "Areas of Concern"
        content: "2-3 issues with root cause"
      - title: "Recommended Actions"
        content: "Prioritized list with owners"
      - title: "Outlook"
        content: "Forecast for next period"

  anomaly_alert:
    structure:
      - title: "What Happened"
        content: "[METRIC] [increased/decreased] by [X%]"
      - title: "Impact"
        content: "This affects [BUSINESS OUTCOME] by [HOW]"
      - title: "Root Cause"
        content: "[EXPLANATION] based on [EVIDENCE]"
      - title: "Recommended Action"
        content: "[SPECIFIC ACTION] by [OWNER] by [DATE]"

  weekly_digest:
    structure:
      - title: "Week in Numbers"
        content: "5-7 key metrics with WoW change"
      - title: "Biggest Mover"
        content: "Highlight of most significant change"
      - title: "Trend Watch"
        content: "Patterns developing over multiple weeks"
      - title: "This Week's Focus"
        content: "What to prioritize based on data"
```

---

## Dashboard Types and Templates

### Executive Dashboard Template

```yaml
executive_dashboard_template:

  layout:
    header:
      - company_name
      - date_range
      - refresh_timestamp

    row_1_headline:
      elements:
        - north_star_metric:
            size: "large"
            comparisons: ["vs target", "vs last period"]
            trend: "sparkline"
        - secondary_metric_1:
            size: "medium"
            comparison: "vs target"
        - secondary_metric_2:
            size: "medium"
            comparison: "vs target"

    row_2_kpis:
      title: "Key Performance Indicators"
      elements:
        - kpi_1: "with target gauge"
        - kpi_2: "with target gauge"
        - kpi_3: "with target gauge"
        - kpi_4: "with target gauge"

    row_3_trends:
      elements:
        - trend_chart_1:
            type: "line"
            period: "last 12 weeks"
            annotations: "major events"
        - trend_chart_2:
            type: "line"
            period: "last 12 weeks"

    row_4_breakdowns:
      elements:
        - breakdown_1:
            type: "bar chart"
            dimension: "by channel"
        - breakdown_2:
            type: "table"
            dimension: "top 5 segments"

    footer:
      - insights_summary
      - recommended_actions
      - data_freshness_note

  metrics_checklist:
    headline:
      - "Primary business objective metric"
    kpis:
      - "Revenue/ARR/MRR"
      - "Customer count"
      - "Growth rate"
      - "Retention/Churn"
    supporting:
      - "By segment breakdown"
      - "Trend over time"
      - "Pipeline/forecast"
```

### Marketing Dashboard Template

```yaml
marketing_dashboard_template:

  layout:
    header:
      - period_selector
      - channel_filter
      - campaign_filter

    row_1_funnel:
      elements:
        - funnel_visualization:
            stages: ["Traffic", "Leads", "MQLs", "SQLs", "Customers"]
            show_conversion_rates: true
        - summary_stats:
            - "Total spend"
            - "Total leads"
            - "Cost per lead"

    row_2_channels:
      title: "Performance by Channel"
      elements:
        - channel_comparison:
            type: "bar chart"
            metrics: ["Traffic", "Conversions", "ROAS"]
        - channel_trend:
            type: "line chart"
            period: "last 8 weeks"

    row_3_campaigns:
      title: "Campaign Performance"
      elements:
        - campaign_table:
            columns: ["Campaign", "Spend", "Leads", "CPL", "Conversions", "ROAS"]
            sort: "by ROAS descending"
            highlight: "top and bottom performers"

    row_4_content:
      title: "Content Performance"
      elements:
        - top_performing_content:
            metrics: ["Views", "Engagement", "Conversions"]
        - landing_page_performance:
            metrics: ["Traffic", "Bounce Rate", "Conversion Rate"]

    footer:
      - "Attribution note"
      - "Next actions"

  metrics_checklist:
    acquisition:
      - "Traffic by source"
      - "Cost per click"
      - "Impressions/Reach"
    behavior:
      - "Bounce rate"
      - "Pages per session"
      - "Email open/click rates"
    outcomes:
      - "Leads generated"
      - "Cost per lead"
      - "ROAS by channel"
      - "Attribution analysis"
```

### Product Dashboard Template

```yaml
product_dashboard_template:

  layout:
    header:
      - period_selector
      - user_segment_filter
      - feature_filter

    row_1_engagement:
      elements:
        - dau_wau_mau:
            type: "line chart"
            show_ratios: true
        - stickiness:
            metric: "DAU/MAU"
            trend: "sparkline"
        - time_in_product:
            metric: "avg session duration"
            comparison: "vs last week"

    row_2_activation:
      title: "Activation & Onboarding"
      elements:
        - activation_funnel:
            stages: ["Signup", "Setup Complete", "First Value", "Habit"]
        - time_to_value:
            metric: "median time to first value"
            trend: "over time"

    row_3_features:
      title: "Feature Adoption"
      elements:
        - feature_adoption_matrix:
            type: "heatmap"
            dimensions: ["Feature", "User Segment"]
        - feature_usage_trend:
            type: "line chart"
            top_features: 5

    row_4_retention:
      title: "Retention"
      elements:
        - retention_curve:
            type: "cohort retention chart"
            cohorts: "last 6 months"
        - retention_by_segment:
            type: "bar chart"
            segments: ["by plan", "by acquisition source"]

    footer:
      - "Recent releases impact"
      - "Experiment results"
      - "Product roadmap link"

  metrics_checklist:
    acquisition:
      - "New signups"
      - "Trial starts"
    behavior:
      - "DAU/WAU/MAU"
      - "Feature adoption %"
      - "Session duration"
      - "Actions per session"
    outcomes:
      - "Activation rate"
      - "Retention curves"
      - "NPS score"
      - "Product-qualified leads"
```

### Customer Success Dashboard Template

```yaml
customer_success_dashboard_template:

  layout:
    header:
      - period_selector
      - customer_segment_filter
      - csm_filter

    row_1_health:
      elements:
        - health_score_distribution:
            type: "stacked bar or donut"
            segments: ["Healthy", "At Risk", "Critical"]
        - health_trend:
            type: "line chart"
            metric: "average health score"
        - accounts_needing_attention:
            type: "count"
            filter: "health < threshold"

    row_2_retention:
      title: "Retention & Churn"
      elements:
        - churn_rate:
            metric: "monthly churn %"
            comparisons: ["vs target", "vs last month"]
        - nrr:
            metric: "Net Revenue Retention"
            trend: "sparkline"
        - churn_reasons:
            type: "bar chart"
            dimension: "by reason"

    row_3_engagement:
      title: "Customer Engagement"
      elements:
        - engagement_metrics:
            - "Login frequency"
            - "Feature usage"
            - "Support tickets"
        - nps_trend:
            type: "line chart"
            show_response_rate: true

    row_4_accounts:
      title: "Account Details"
      elements:
        - at_risk_accounts:
            type: "table"
            columns: ["Account", "MRR", "Health", "Last Activity", "Owner"]
            sort: "by health ascending"
        - expansion_opportunities:
            type: "table"
            columns: ["Account", "Current MRR", "Potential", "Stage"]

    footer:
      - "CSM performance summary"
      - "Playbook execution status"
      - "Quarterly review schedule"

  metrics_checklist:
    health:
      - "Health score distribution"
      - "Engagement metrics"
      - "Support sentiment"
    retention:
      - "Churn rate"
      - "NRR"
      - "Renewal rate"
    expansion:
      - "Expansion MRR"
      - "Upsell pipeline"
      - "CLTV"
```

---

## Implementation Process

### Phase 1: Discovery (Week 1)

```yaml
phase_1_discovery:

  day_1_2_stakeholder_interviews:
    participants:
      - "Executive sponsor"
      - "Primary dashboard users"
      - "Data team"
    questions:
      - "What decisions do you make with data?"
      - "What questions do you ask most often?"
      - "What's missing from current dashboards?"
      - "What's the most important metric to you?"
      - "How often do you check metrics?"
    output: "Stakeholder needs summary"

  day_3_4_current_state_audit:
    tasks:
      - "Inventory existing dashboards"
      - "Identify data sources"
      - "Assess data quality"
      - "Document technical constraints"
    output: "Current state assessment"

  day_5_dmmm_workshop:
    participants: "Key stakeholders"
    agenda:
      - "Define business objectives"
      - "Identify goals per objective"
      - "Select KPIs per goal"
      - "Set targets"
      - "Define segments"
    output: "Completed DMMM framework"
```

### Phase 2: Design (Week 2)

```yaml
phase_2_design:

  day_1_2_metric_selection:
    tasks:
      - "Apply So What Test to all proposed metrics"
      - "Remove metrics that fail"
      - "Transform metrics where possible"
      - "Define calculation logic for each"
    output: "Final metric list with definitions"

  day_3_wireframing:
    tasks:
      - "Sketch layout options"
      - "Apply information hierarchy"
      - "Determine drill-down paths"
      - "Plan mobile view (if needed)"
    output: "Wireframe mockups"

  day_4_design_review:
    participants: "Stakeholders"
    agenda:
      - "Present wireframes"
      - "Validate metric selection"
      - "Confirm hierarchy"
      - "Gather feedback"
    output: "Approved design"

  day_5_technical_spec:
    tasks:
      - "Define data requirements"
      - "Specify calculations"
      - "Document refresh logic"
      - "Plan alerts/notifications"
    output: "Technical specification"
```

### Phase 3: Build (Week 3-4)

```yaml
phase_3_build:

  week_3_data_layer:
    tasks:
      - "Create/validate data sources"
      - "Build metrics calculations"
      - "Implement refresh jobs"
      - "Set up data quality checks"
    output: "Working data layer"

  week_4_day_1_3_visualization:
    tasks:
      - "Build charts and visualizations"
      - "Implement filters"
      - "Add comparisons and trends"
      - "Apply styling and branding"
    output: "Visual dashboard"

  week_4_day_4_interactivity:
    tasks:
      - "Add drill-down functionality"
      - "Implement alerts"
      - "Set up scheduled delivery"
      - "Configure permissions"
    output: "Interactive dashboard"

  week_4_day_5_qa:
    tasks:
      - "Validate calculations"
      - "Test all filters"
      - "Check performance"
      - "User acceptance testing"
    output: "QA sign-off"
```

### Phase 4: Launch & Iterate (Week 5+)

```yaml
phase_4_launch:

  soft_launch:
    tasks:
      - "Deploy to pilot users"
      - "Gather feedback"
      - "Fix issues"
      - "Document learnings"
    duration: "1 week"

  full_launch:
    tasks:
      - "Train all users"
      - "Document usage guide"
      - "Set up support channel"
      - "Announce to organization"
    duration: "1 day"

  iteration:
    weekly:
      - "Monitor usage metrics"
      - "Collect user feedback"
      - "Quick fixes and improvements"
    monthly:
      - "Review metric relevance"
      - "Add/remove metrics based on So What Test"
      - "Update targets"
    quarterly:
      - "Deep review of dashboard effectiveness"
      - "Major redesign if needed"
      - "Alignment with new business priorities"
```

---

## Common Pitfalls and Solutions

### Dashboard Pitfalls

```yaml
dashboard_pitfalls:

  pitfall_1_too_many_metrics:
    symptom: "Dashboard has 20+ metrics"
    problem: "Users don't know where to look"
    solution:
      - "Apply So What Test ruthlessly"
      - "Move detail to drill-down"
      - "Target: 8-12 metrics on main view"
    kaushik_quote: |
      "If everything is important, nothing is important.
      Choose or lose."

  pitfall_2_no_context:
    symptom: "Numbers without comparison"
    problem: "Can't tell if good or bad"
    solution:
      - "Add vs target comparison"
      - "Add vs previous period"
      - "Add directional indicators"
    example:
      bad: "Revenue: R$150,000"
      good: "Revenue: R$150,000 (+12% MoM, 95% of target)"

  pitfall_3_no_story:
    symptom: "Just numbers on a page"
    problem: "No insight, no action"
    solution:
      - "Add narrative sections"
      - "Include recommendations"
      - "Explain the 'why'"
    example:
      bad: "Churn: 5%"
      good: "Churn: 5% (up from 3%) - driven by enterprise segment, recommend executive review of top 3 accounts"

  pitfall_4_wrong_audience:
    symptom: "CEO dashboard has SQL queries"
    problem: "Mismatch between data and user"
    solution:
      - "Define audience clearly"
      - "Adjust detail level"
      - "Create role-specific views"

  pitfall_5_stale_data:
    symptom: "Data updated monthly for daily decisions"
    problem: "Decisions based on outdated info"
    solution:
      - "Increase refresh frequency"
      - "Show data freshness"
      - "Alert when data is stale"

  pitfall_6_vanity_metrics:
    symptom: "Tracking likes, page views, impressions"
    problem: "Feel good, no business impact"
    solution:
      - "Apply So What Test"
      - "Replace with actionable metrics"
      - "Focus on outcomes, not outputs"
    example:
      vanity: "10,000 page views"
      actionable: "500 leads generated (5% conversion)"

  pitfall_7_no_ownership:
    symptom: "Beautiful dashboard no one uses"
    problem: "No accountability for metrics"
    solution:
      - "Assign owner to each metric"
      - "Include in regular reviews"
      - "Tie to goals/OKRs"

  pitfall_8_all_green_syndrome:
    symptom: "Every metric shows green"
    problem: "Targets too easy or wrong thresholds"
    solution:
      - "Review and adjust targets"
      - "Use relative comparisons"
      - "Highlight biggest movers, not just status"
```

### Quality Assurance Checklist

```yaml
dashboard_qa_checklist:

  data_quality:
    - [ ] All metrics calculated correctly
    - [ ] Data refresh working as expected
    - [ ] No null or missing values in key metrics
    - [ ] Historical data complete
    - [ ] Filters working correctly

  design_quality:
    - [ ] Information hierarchy clear
    - [ ] Most important metrics most prominent
    - [ ] Consistent color coding
    - [ ] Readable on target devices
    - [ ] Load time acceptable (<5 seconds)

  actionability:
    - [ ] Every metric passes So What Test
    - [ ] Comparisons included (vs target, vs period)
    - [ ] Trends visible
    - [ ] Drill-down available
    - [ ] Recommendations included

  usability:
    - [ ] Primary audience validated design
    - [ ] Navigation intuitive
    - [ ] Labels clear
    - [ ] Help/documentation available
    - [ ] Mobile view works (if required)

  governance:
    - [ ] Metric definitions documented
    - [ ] Data sources documented
    - [ ] Owners assigned
    - [ ] Review cadence defined
    - [ ] Feedback mechanism in place
```

---

## Dashboard SQL Patterns

### KPI Calculation Patterns

```sql
-- Pattern 1: Period over Period Comparison
WITH current_period AS (
  SELECT
    SUM(revenue) as current_revenue,
    COUNT(DISTINCT customer_id) as current_customers
  FROM transactions
  WHERE transaction_date >= DATE_TRUNC('month', CURRENT_DATE)
),
previous_period AS (
  SELECT
    SUM(revenue) as previous_revenue,
    COUNT(DISTINCT customer_id) as previous_customers
  FROM transactions
  WHERE transaction_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
    AND transaction_date < DATE_TRUNC('month', CURRENT_DATE)
)
SELECT
  c.current_revenue,
  p.previous_revenue,
  ROUND(100.0 * (c.current_revenue - p.previous_revenue) / NULLIF(p.previous_revenue, 0), 1) as pct_change,
  CASE
    WHEN c.current_revenue > p.previous_revenue THEN 'up'
    WHEN c.current_revenue < p.previous_revenue THEN 'down'
    ELSE 'flat'
  END as direction
FROM current_period c, previous_period p;
```

```sql
-- Pattern 2: Target vs Actual
WITH actuals AS (
  SELECT
    DATE_TRUNC('month', date) as month,
    SUM(value) as actual_value
  FROM metrics
  WHERE metric_name = 'mrr'
  GROUP BY 1
),
targets AS (
  SELECT
    month,
    target_value
  FROM metric_targets
  WHERE metric_name = 'mrr'
)
SELECT
  a.month,
  a.actual_value,
  t.target_value,
  ROUND(100.0 * a.actual_value / NULLIF(t.target_value, 0), 1) as pct_of_target,
  CASE
    WHEN a.actual_value >= t.target_value THEN 'on_track'
    WHEN a.actual_value >= t.target_value * 0.9 THEN 'at_risk'
    ELSE 'off_track'
  END as status
FROM actuals a
LEFT JOIN targets t ON a.month = t.month
ORDER BY a.month;
```

```sql
-- Pattern 3: Trend with Moving Average
WITH daily_metrics AS (
  SELECT
    date,
    SUM(value) as daily_value
  FROM metrics
  WHERE metric_name = 'signups'
    AND date >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY date
)
SELECT
  date,
  daily_value,
  AVG(daily_value) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as seven_day_avg,
  AVG(daily_value) OVER (
    ORDER BY date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) as thirty_day_avg
FROM daily_metrics
ORDER BY date;
```

```sql
-- Pattern 4: Distribution/Segmentation
WITH health_scores AS (
  SELECT
    customer_id,
    health_score,
    CASE
      WHEN health_score >= 80 THEN 'Healthy'
      WHEN health_score >= 50 THEN 'At Risk'
      ELSE 'Critical'
    END as health_status
  FROM customer_health
  WHERE snapshot_date = CURRENT_DATE
)
SELECT
  health_status,
  COUNT(*) as customer_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) as pct_of_total,
  SUM(CASE WHEN health_status = 'Healthy' THEN 1 ELSE 0 END) OVER() as healthy_total,
  SUM(CASE WHEN health_status = 'At Risk' THEN 1 ELSE 0 END) OVER() as at_risk_total,
  SUM(CASE WHEN health_status = 'Critical' THEN 1 ELSE 0 END) OVER() as critical_total
FROM health_scores
GROUP BY health_status
ORDER BY
  CASE health_status
    WHEN 'Healthy' THEN 1
    WHEN 'At Risk' THEN 2
    WHEN 'Critical' THEN 3
  END;
```

```sql
-- Pattern 5: Funnel Conversion
WITH funnel AS (
  SELECT
    'Traffic' as stage,
    1 as stage_order,
    COUNT(DISTINCT session_id) as count
  FROM sessions
  WHERE date >= CURRENT_DATE - INTERVAL '30 days'

  UNION ALL

  SELECT
    'Signups' as stage,
    2 as stage_order,
    COUNT(DISTINCT user_id) as count
  FROM users
  WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'

  UNION ALL

  SELECT
    'Activated' as stage,
    3 as stage_order,
    COUNT(DISTINCT user_id) as count
  FROM users
  WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    AND activated = true

  UNION ALL

  SELECT
    'Converted' as stage,
    4 as stage_order,
    COUNT(DISTINCT customer_id) as count
  FROM customers
  WHERE first_payment_date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT
  stage,
  count,
  LAG(count) OVER (ORDER BY stage_order) as previous_stage_count,
  ROUND(100.0 * count / NULLIF(LAG(count) OVER (ORDER BY stage_order), 0), 1) as conversion_rate,
  ROUND(100.0 * count / NULLIF(FIRST_VALUE(count) OVER (ORDER BY stage_order), 0), 1) as cumulative_conversion
FROM funnel
ORDER BY stage_order;
```

### Alert Query Patterns

```sql
-- Pattern 6: Anomaly Detection (Simple)
WITH daily_metrics AS (
  SELECT
    date,
    value,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) as avg_30d,
    STDDEV(value) OVER (ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) as stddev_30d
  FROM metrics
  WHERE metric_name = 'daily_signups'
    AND date >= CURRENT_DATE - INTERVAL '60 days'
)
SELECT
  date,
  value,
  avg_30d,
  stddev_30d,
  CASE
    WHEN value > avg_30d + 2 * stddev_30d THEN 'high_anomaly'
    WHEN value < avg_30d - 2 * stddev_30d THEN 'low_anomaly'
    ELSE 'normal'
  END as status,
  ROUND((value - avg_30d) / NULLIF(stddev_30d, 0), 2) as z_score
FROM daily_metrics
WHERE date = CURRENT_DATE - INTERVAL '1 day'
  AND (value > avg_30d + 2 * stddev_30d OR value < avg_30d - 2 * stddev_30d);
```

```sql
-- Pattern 7: Threshold Alerts
SELECT
  metric_name,
  current_value,
  warning_threshold,
  critical_threshold,
  target,
  CASE
    WHEN current_value <= critical_threshold THEN 'critical'
    WHEN current_value <= warning_threshold THEN 'warning'
    WHEN current_value >= target THEN 'on_track'
    ELSE 'below_target'
  END as status,
  owner_email
FROM (
  SELECT
    'health_score_avg' as metric_name,
    AVG(health_score) as current_value,
    60 as warning_threshold,
    50 as critical_threshold,
    75 as target,
    'cs@company.com' as owner_email
  FROM customer_health
  WHERE snapshot_date = CURRENT_DATE

  UNION ALL

  SELECT
    'churn_rate' as metric_name,
    churn_rate as current_value,
    4 as warning_threshold,
    5 as critical_threshold,
    2 as target,
    'cco@company.com' as owner_email
  FROM monthly_churn
  WHERE month = DATE_TRUNC('month', CURRENT_DATE)
) alerts
WHERE status IN ('critical', 'warning');
```

---

## Tool Recommendations

### BI Tool Selection

```yaml
bi_tool_selection:

  for_small_teams:
    google_data_studio:
      pros: ["Free", "Google ecosystem integration", "Easy sharing"]
      cons: ["Limited customization", "Performance with large data"]
      best_for: "Marketing dashboards, basic reporting"

    metabase:
      pros: ["Open source", "SQL-friendly", "Self-hostable"]
      cons: ["Limited enterprise features", "Fewer visualizations"]
      best_for: "Product/engineering teams, SQL-savvy users"

  for_mid_market:
    tableau:
      pros: ["Best visualizations", "Powerful analytics", "Large community"]
      cons: ["Expensive", "Steep learning curve"]
      best_for: "Data-heavy organizations, complex analysis"

    looker:
      pros: ["Data modeling layer", "Embedded analytics", "Google integration"]
      cons: ["Complex setup", "Expensive"]
      best_for: "Companies with data teams, product analytics"

    power_bi:
      pros: ["Microsoft integration", "Affordable", "Good for enterprise"]
      cons: ["Less flexible", "Best with MS stack"]
      best_for: "Microsoft shops, corporate environments"

  for_enterprise:
    domo:
      pros: ["All-in-one platform", "Executive-friendly", "Alerts"]
      cons: ["Very expensive", "Can be overwhelming"]
      best_for: "Large enterprises, executive dashboards"

    sisense:
      pros: ["Embedded analytics", "Complex data handling"]
      cons: ["Expensive", "Complex implementation"]
      best_for: "Product analytics, embedded BI"

  build_vs_buy:
    build_custom:
      when:
        - "Highly specific requirements"
        - "Need full control"
        - "Strong engineering team"
      tech_stack: "React + D3.js + SQL backend"

    buy_tool:
      when:
        - "Standard dashboarding needs"
        - "Quick time to value"
        - "Limited engineering resources"
```

### Integration Patterns

```yaml
integration_patterns:

  data_warehouse_first:
    description: "All data flows to warehouse, BI reads from warehouse"
    architecture:
      sources: ["CRM", "Product DB", "Marketing tools"]
      etl: ["Fivetran", "Airbyte", "Custom scripts"]
      warehouse: ["BigQuery", "Snowflake", "Redshift"]
      bi_tool: "Connects to warehouse"
    pros: ["Single source of truth", "Consistent metrics"]
    cons: ["More complex", "Latency"]

  direct_connection:
    description: "BI tool connects directly to sources"
    architecture:
      bi_tool: "Connects to each source"
    pros: ["Simple", "Real-time"]
    cons: ["No single source of truth", "Metric inconsistency"]

  hybrid:
    description: "Critical metrics in warehouse, real-time direct"
    architecture:
      historical: "Warehouse"
      real_time: "Direct connections"
    pros: ["Balance of consistency and freshness"]
    cons: ["More complex to manage"]
```

---

## Output Deliverables

```yaml
deliverables:

  primary:
    dmmm_framework_document:
      description: |
        Completed DMMM framework with:
        - Business objectives
        - Goals per objective
        - KPIs per goal
        - Targets per KPI
        - Segments per target

    dashboard_specification:
      description: |
        Complete specification including:
        - Metric definitions
        - Calculation logic
        - Data sources
        - Refresh frequency
        - Alert thresholds

    functional_dashboard:
      description: |
        Working dashboard with:
        - All specified metrics
        - Proper hierarchy
        - Drill-down capability
        - Mobile view (if required)

  secondary:
    so_what_audit:
      description: |
        Documentation of So What Test results:
        - Metrics that passed
        - Metrics transformed
        - Metrics removed
        - Action playbooks per metric

    user_guide:
      description: |
        Documentation for users:
        - How to read the dashboard
        - What each metric means
        - How to drill down
        - Who to contact for issues

  optional:
    alert_configuration:
      description: |
        Automated alerts setup:
        - Threshold definitions
        - Notification channels
        - Escalation paths

    training_materials:
      description: |
        Materials for user training:
        - Walkthrough video
        - FAQ document
        - Best practices guide
```

---

## Quality Checklist

### Pre-Build Checklist

```yaml
pre_build_checklist:
  - [ ] DMMM framework completed with stakeholders
  - [ ] So What Test applied to all metrics
  - [ ] Primary audience defined
  - [ ] Data sources identified and validated
  - [ ] Wireframes approved
  - [ ] Technical spec completed
  - [ ] Refresh frequency agreed
  - [ ] Alert thresholds defined
```

### Post-Build Checklist

```yaml
post_build_checklist:
  - [ ] All metrics calculating correctly
  - [ ] Comparisons (vs target, vs period) working
  - [ ] Filters functional
  - [ ] Drill-down paths working
  - [ ] Mobile view acceptable (if required)
  - [ ] Load time acceptable (<5 seconds)
  - [ ] Alerts firing correctly
  - [ ] User acceptance testing complete
```

### Ongoing Checklist

```yaml
ongoing_checklist:
  weekly:
    - [ ] Data refreshing correctly
    - [ ] No broken visualizations
    - [ ] Alerts reviewed
  monthly:
    - [ ] Metrics still passing So What Test
    - [ ] User feedback collected
    - [ ] Targets reviewed
  quarterly:
    - [ ] Full review of dashboard effectiveness
    - [ ] Alignment with current business priorities
    - [ ] Consider redesign if needed
```

---

## Integration with Other Tasks

### Related Data Pack Tasks

```yaml
related_tasks:

  calculate_clv:
    integration: "CLV metrics in customer dashboard"
    value: "Show customer value segmentation"

  segment_rfm:
    integration: "RFM segments as filter/breakdown"
    value: "Understand behavior by customer type"

  design_health_score:
    integration: "Health score distribution in CS dashboard"
    value: "Monitor customer health trends"

  predict_churn:
    integration: "Churn predictions as alert source"
    value: "Proactive intervention"

  build_attribution:
    integration: "Attribution in marketing dashboard"
    value: "Understand channel contribution"

  define_north_star:
    integration: "North Star as headline metric"
    value: "Focus entire dashboard around key metric"
```

---

## Glossary

```yaml
glossary:

  dmmm:
    full_name: "Digital Marketing & Measurement Model"
    definition: "Framework de Avinash Kaushik para estruturar métricas de negócio"

  so_what_test:
    definition: "Teste para validar se uma métrica gera ação"

  north_star_metric:
    definition: "A única métrica mais importante que reflete valor entregue ao cliente"

  kpi:
    full_name: "Key Performance Indicator"
    definition: "Métrica chave que indica progresso em um objetivo"

  vanity_metric:
    definition: "Métrica que parece boa mas não indica sucesso real"

  leading_indicator:
    definition: "Métrica preditiva que antecipa resultados futuros"

  lagging_indicator:
    definition: "Métrica de resultado que mostra o que já aconteceu"

  dashboard_hierarchy:
    definition: "Organização visual de métricas por importância"

  drill_down:
    definition: "Capacidade de ir de visão geral para detalhe"

  sparkline:
    definition: "Mini gráfico de tendência inline com métrica"

  data_storytelling:
    definition: "Técnica de apresentar dados como narrativa com início, conflito e resolução"
```

---

## Version History

```yaml
version: "1.0"
created: "2026-01-23"
primary_agent: "Avinash Kaushik"
lines: "1600+"

changelog:
  - "1.0: Task inicial criado com DMMM framework completo"
  - "1.0: So What Test framework com exemplos"
  - "1.0: Dashboard design principles detalhados"
  - "1.0: Metric hierarchy (acquisition, behavior, outcomes)"
  - "1.0: Storytelling with data framework"
  - "1.0: Templates para Executive, Marketing, Product, CS dashboards"
  - "1.0: SQL patterns para KPIs e alertas"
  - "1.0: Implementation process completo"
  - "1.0: Common pitfalls e solutions"
```

---

*Data Intelligence Pack - Task: Create Dashboard*
*Primary Agent: Avinash Kaushik*
*Framework: DMMM + So What Test + Data Storytelling*
