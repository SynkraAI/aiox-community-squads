# Calculate Customer Lifetime Value (CLV) Task

## Purpose

Calcular o Customer Lifetime Value (CLV) usando metodologias rigorosas de Peter Fader e Bruce Hardie (Wharton/LBS). Esta task implementa múltiplos métodos de cálculo - do histórico simples aos modelos probabilísticos avançados (BG/NBD, Gamma-Gamma) - permitindo escolher a abordagem adequada baseada nos dados disponíveis e maturidade analítica da organização.

## Workspace Output Contract

- Preflight: `*workspace-preflight` + `*workspace-context {slug}`
- Output canônico (template-first): `workspace/businesses/{slug}/analytics/clv-report.yaml`
- Output custom (ad-hoc): `docs/data/{slug}/clv-investigation-{date}.md`
- Regra: escrita canônica só se existir template em `workspace/_templates/analytics/clv-report.yaml`

## When to Use

- Precisa determinar quanto vale cada cliente para o negócio
- Quer segmentar clientes por valor (não apenas por comportamento)
- Precisa calcular CAC máximo aceitável (CLV deve ser > CAC)
- Quer projetar receita futura baseada em clientes existentes
- Precisa justificar investimento em retenção vs aquisição
- Quer identificar quais clientes merecem mais investimento
- Precisa valuar a empresa baseada em customer equity
- Está fazendo análise de cohort por valor
- Precisa prever comportamento futuro de compra

## Core Methodology

Esta task integra três níveis de sofisticação:

1. **CLV Histórico** - Análise retroativa simples
2. **CLV Preditivo Tradicional** - Projeções com fórmulas determinísticas
3. **CLV Probabilístico** - Modelos BG/NBD + Gamma-Gamma (Fader/Hardie)

---

## Task Metadata

```yaml
task:
  name: Calculate Customer Lifetime Value
  id: calculate-clv
  version: "1.0"
  category: customer_analytics
  difficulty: intermediate_to_advanced
  primary_agents:
    - peter-fader
  supporting_agents:
    - nick-mehta  # Para integração com Health Score
    - sean-ellis  # Para conexão com métricas de growth
  estimated_time: "2-4 hours (dados prontos) | 1-2 semanas (coleta + análise)"

  prerequisites:
    - Dados transacionais de clientes (mínimo 6 meses)
    - Identificação única por cliente
    - Timestamps das transações
    - Valores monetários das transações

  outputs:
    - CLV por cliente individual
    - CLV por segmento/cohort
    - Distribuição de valor (Pareto analysis)
    - Projeções de receita futura
    - Recomendações de estratégia por valor

  frameworks_used:
    - Customer Centricity (Fader)
    - RFM Analysis
    - BG/NBD Model
    - Gamma-Gamma Model
    - Pareto/NBD Model (reference)
```

---

## Phase 0: Pre-Flight Check (Tier 0 Diagnostic)

**MANDATORY: Antes de calcular qualquer CLV, complete este diagnóstico.**

### Block A: Entendimento do Contexto de Negócio

```yaml
questions:
  A1_business_model:
    question: "Qual é o modelo de negócio?"
    options:
      contractual:
        description: "Assinaturas, SaaS, memberships"
        implication: "Churn é observável diretamente"
        clv_approach: "Retention-based CLV"
      non_contractual:
        description: "E-commerce, varejo, compras recorrentes opcionais"
        implication: "Churn é latente (não sabemos quando cliente 'morreu')"
        clv_approach: "BG/NBD + Gamma-Gamma (probabilístico)"
      hybrid:
        description: "Mix de transacional com elementos contratuais"
        implication: "Requer análise separada por stream"
        clv_approach: "Modelo híbrido"

  A2_transaction_frequency:
    question: "Com que frequência clientes compram?"
    options:
      high_frequency: "Múltiplas vezes por mês (daily/weekly)"
      medium_frequency: "1-2x por mês"
      low_frequency: "Algumas vezes por ano"
      very_low: "1-2x por ano ou menos"
    implication: |
      Alta frequência = mais dados = modelos mais precisos
      Baixa frequência = requer período de análise mais longo

  A3_customer_tenure:
    question: "Quanto tempo você tem dados de clientes?"
    validation:
      minimum_recommended: "12 meses (ideal 24-36)"
      minimum_viable: "6 meses"
      if_less_than_6_months: "CLV histórico apenas, modelos preditivos instáveis"

  A4_objective:
    question: "Qual é o objetivo principal do cálculo de CLV?"
    options:
      segmentation: "Segmentar base por valor para estratégias diferenciadas"
      acquisition: "Determinar CAC máximo aceitável"
      valuation: "Calcular customer equity para valuation"
      retention: "Identificar quem vale a pena reter"
      forecasting: "Projetar receita futura"
      all_above: "Análise completa de Customer Centricity"
```

### Block B: Disponibilidade de Dados

```yaml
data_requirements:
  minimum_fields:
    - customer_id: "Identificador único do cliente"
    - transaction_date: "Data de cada transação"
    - transaction_amount: "Valor de cada transação"

  enhanced_fields:
    - first_purchase_date: "Data da primeira compra"
    - product_category: "Para CLV por categoria"
    - acquisition_channel: "Para CLV por fonte"
    - cost_of_goods: "Para CLV baseado em margem"
    - cohort_id: "Para análise de cohort"

  data_quality_check:
    - "Há duplicatas de customer_id?"
    - "Há transações com valor zero ou negativo?"
    - "Há gaps temporais nos dados?"
    - "Refunds/chargebacks estão identificados?"
    - "B2B e B2C estão separados?"

questions:
  B1_data_format:
    question: "Em que formato estão os dados?"
    options:
      - "Database SQL (Postgres, MySQL, etc.)"
      - "CSV/Excel"
      - "Data Warehouse (BigQuery, Snowflake, etc.)"
      - "CRM export"
      - "Multiple sources (need integration)"

  B2_data_completeness:
    question: "Os dados cobrem 100% das transações?"
    warning: |
      Se não, CLV será subestimado.
      Exemplo: Se loja física não está integrada, CLV de omnichannel será incorreto.

  B3_margin_availability:
    question: "Você tem dados de margem/custo por transação?"
    options:
      yes_per_transaction: "Margem calculada por transação"
      yes_average: "Margem média conhecida (ex: 40%)"
      no: "Apenas receita disponível"
    implication: |
      CLV baseado em receita superestima valor real.
      CLV baseado em margem é mais preciso para decisões.
```

### Block C: Premissas de Negócio

```yaml
questions:
  C1_discount_rate:
    question: "Qual taxa de desconto usar para NPV?"
    guidance: |
      Típico: 10-15% ao ano
      Conservador: 15-20%
      Agressivo: 5-10%
    default: "12% (1% ao mês)"

  C2_time_horizon:
    question: "Por quanto tempo projetar CLV?"
    options:
      - "12 meses (CLV curto prazo)"
      - "24 meses (CLV médio prazo)"
      - "36 meses (CLV padrão)"
      - "60 meses (CLV longo prazo)"
      - "Lifetime (até churn esperado)"
    recommendation: |
      Para maioria dos negócios digitais: 36 meses
      Para SaaS com churn alto: 24 meses
      Para mercados estáveis com alta retenção: 60+ meses

  C3_acquisition_cost:
    question: "Qual é o CAC médio atual?"
    purpose: "Para calcular CLV:CAC ratio e payback period"
    healthy_ratio: "CLV:CAC >= 3:1"
    minimum_ratio: "CLV:CAC >= 1:1 (breakeven)"
```

### Pre-Flight Output

```yaml
diagnostic_summary:
  business_model: "[contractual/non_contractual/hybrid]"
  recommended_method: "[histórico/preditivo_tradicional/probabilístico]"
  data_readiness: "[ready/needs_preparation/insufficient]"
  time_horizon: "[X] meses"
  discount_rate: "[X]%"

  data_gaps:
    - "[Gap 1 identificado]"
    - "[Gap 2 identificado]"

  recommended_actions_before_clv:
    - "[Ação 1 para preparar dados]"
    - "[Ação 2]"

proceed_to_phase: "[1/2/3]"  # Baseado em maturidade e dados
```

---

## Phase 1: CLV Histórico (Retroativo)

**Quando usar:** Primeiro passo para qualquer análise, baseline para validar modelos mais complexos.

### Método 1A: CLV Histórico Simples

```yaml
formula:
  name: "Simple Historical CLV"
  calculation: |
    CLV_histórico = Σ (Transações do cliente no período)

  code_sql: |
    SELECT
      customer_id,
      COUNT(*) as total_transactions,
      SUM(amount) as total_revenue,
      MIN(transaction_date) as first_purchase,
      MAX(transaction_date) as last_purchase,
      DATEDIFF(MAX(transaction_date), MIN(transaction_date)) as customer_age_days,
      SUM(amount) as historical_clv
    FROM transactions
    WHERE transaction_date >= DATE_SUB(NOW(), INTERVAL 36 MONTH)
    GROUP BY customer_id
    ORDER BY historical_clv DESC

  limitations:
    - "Não projeta futuro"
    - "Novos clientes têm CLV baixo artificialmente"
    - "Não considera tempo de relacionamento"
    - "Não diferencia cliente ativo de churned"
```

### Método 1B: CLV Histórico Normalizado

```yaml
formula:
  name: "Normalized Historical CLV (ARPU-based)"
  calculation: |
    CLV_normalizado = (Receita Total / Meses de Vida) × Expectativa de Vida

    Onde:
    - Receita Total = soma de todas transações
    - Meses de Vida = diferença entre primeira e última transação
    - Expectativa de Vida = estimativa de quanto tempo cliente fica ativo (ex: 24 meses)

  code_sql: |
    WITH customer_metrics AS (
      SELECT
        customer_id,
        SUM(amount) as total_revenue,
        MIN(transaction_date) as first_purchase,
        MAX(transaction_date) as last_purchase,
        TIMESTAMPDIFF(MONTH, MIN(transaction_date), MAX(transaction_date)) + 1 as tenure_months
      FROM transactions
      GROUP BY customer_id
    )
    SELECT
      customer_id,
      total_revenue,
      tenure_months,
      total_revenue / tenure_months as monthly_revenue,
      (total_revenue / tenure_months) * 24 as projected_clv_24m,  -- Assumindo 24 meses de vida
      (total_revenue / tenure_months) * 36 as projected_clv_36m   -- Assumindo 36 meses de vida
    FROM customer_metrics
    WHERE tenure_months >= 3  -- Mínimo 3 meses para estabilidade
    ORDER BY projected_clv_36m DESC

  advantages:
    - "Normaliza por tempo de relacionamento"
    - "Permite comparar clientes novos e antigos"

  limitations:
    - "Assume comportamento linear no tempo"
    - "Não considera variações sazonais"
    - "Expectativa de vida é estimativa arbitrária"
```

### Método 1C: CLV Histórico por Cohort

```yaml
formula:
  name: "Cohort-Based Historical CLV"
  purpose: "Comparar valor de diferentes safras de clientes"

  code_sql: |
    WITH customer_cohort AS (
      SELECT
        customer_id,
        DATE_FORMAT(MIN(transaction_date), '%Y-%m') as cohort_month
      FROM transactions
      GROUP BY customer_id
    ),
    cohort_revenue AS (
      SELECT
        cc.cohort_month,
        t.customer_id,
        TIMESTAMPDIFF(MONTH, STR_TO_DATE(CONCAT(cc.cohort_month, '-01'), '%Y-%m-%d'), t.transaction_date) as month_number,
        SUM(t.amount) as revenue
      FROM transactions t
      JOIN customer_cohort cc ON t.customer_id = cc.customer_id
      GROUP BY cc.cohort_month, t.customer_id, month_number
    )
    SELECT
      cohort_month,
      month_number,
      COUNT(DISTINCT customer_id) as customers,
      SUM(revenue) as total_revenue,
      SUM(revenue) / COUNT(DISTINCT customer_id) as revenue_per_customer,
      SUM(SUM(revenue)) OVER (PARTITION BY cohort_month ORDER BY month_number) /
        FIRST_VALUE(COUNT(DISTINCT customer_id)) OVER (PARTITION BY cohort_month ORDER BY month_number) as cumulative_clv
    FROM cohort_revenue
    GROUP BY cohort_month, month_number
    ORDER BY cohort_month, month_number

  output_interpretation: |
    - Compare CLV cumulativo entre cohorts
    - Identifique se cohorts recentes estão melhores ou piores
    - Use como baseline para projetar CLV de novos cohorts
```

### Phase 1 Output Template

```yaml
historical_clv_report:
  summary_metrics:
    total_customers_analyzed: "[N]"
    analysis_period: "[data início] a [data fim]"
    total_revenue_period: "$[X]"

  distribution:
    average_clv: "$[X]"
    median_clv: "$[X]"
    std_deviation: "$[X]"

    percentiles:
      p10: "$[X]"
      p25: "$[X]"
      p50: "$[X]"
      p75: "$[X]"
      p90: "$[X]"
      p99: "$[X]"

  pareto_analysis:
    top_1_percent_customers: "[N] clientes"
    top_1_percent_revenue: "[X]% da receita total"
    top_10_percent_revenue: "[X]% da receita total"
    top_20_percent_revenue: "[X]% da receita total (Pareto check)"
    bottom_50_percent_revenue: "[X]% da receita total"

  cohort_comparison:
    best_cohort: "[cohort] com CLV médio de $[X]"
    worst_cohort: "[cohort] com CLV médio de $[X]"
    trend: "[melhorando/piorando/estável]"

  insights:
    - "[Insight 1 sobre distribuição de valor]"
    - "[Insight 2 sobre concentração]"
    - "[Insight 3 sobre cohorts]"
```

---

## Phase 2: CLV Preditivo Tradicional

**Quando usar:** Modelos mais simples que probabilísticos, bons para contextos contratuais.

### Método 2A: CLV Contratual (Subscription-Based)

```yaml
formula:
  name: "Contractual CLV (SaaS/Subscription)"
  calculation: |
    CLV = ARPU × Gross Margin × (1 / Churn Rate)

    Ou com desconto:
    CLV = ARPU × Gross Margin × (1 / (Churn Rate + Discount Rate))

    Onde:
    - ARPU = Average Revenue Per User (mensal ou anual)
    - Gross Margin = Margem bruta (ex: 0.70 para 70%)
    - Churn Rate = Taxa de churn (mensal ou anual, consistente com ARPU)
    - Discount Rate = Taxa de desconto para NPV

  example:
    arpu_monthly: "$100"
    gross_margin: "70%"
    monthly_churn: "3%"
    discount_rate: "1% ao mês"

    calculation: |
      CLV = $100 × 0.70 × (1 / (0.03 + 0.01))
      CLV = $70 × (1 / 0.04)
      CLV = $70 × 25
      CLV = $1,750

  code_python: |
    def calculate_contractual_clv(arpu, gross_margin, churn_rate, discount_rate=0):
        """
        Calculate CLV for subscription/contractual businesses.

        Args:
            arpu: Average Revenue Per User (same period as churn)
            gross_margin: Gross margin as decimal (0.70 = 70%)
            churn_rate: Churn rate as decimal (0.03 = 3%)
            discount_rate: Discount rate for NPV (same period as churn)

        Returns:
            CLV value
        """
        if churn_rate == 0:
            return float('inf')

        clv = (arpu * gross_margin) / (churn_rate + discount_rate)
        return clv

    # Example usage
    clv = calculate_contractual_clv(
        arpu=100,
        gross_margin=0.70,
        churn_rate=0.03,
        discount_rate=0.01
    )
    print(f"CLV: ${clv:,.2f}")  # CLV: $1,750.00

  variations:
    with_expansion_revenue: |
      CLV = (ARPU × GM × (1 + Expansion Rate)) / (Churn Rate + Discount Rate - Expansion Rate)

      Onde Expansion Rate = taxa de crescimento de receita em clientes existentes (upsells)

    with_retention_curve: |
      CLV = Σ (Revenue_t × Retention_t × GM) / (1 + d)^t

      Para t de 1 até N períodos
      Mais preciso quando retenção não é constante
```

### Método 2B: CLV por Fórmula de Segmentos (RFM-Based)

```yaml
formula:
  name: "RFM-Weighted CLV"
  approach: |
    Calcular CLV diferenciado por segmento RFM,
    usando comportamento histórico de cada segmento para projetar.

  steps:
    step_1_calculate_rfm:
      description: "Calcular scores RFM para cada cliente"
      code_sql: |
        WITH rfm_base AS (
          SELECT
            customer_id,
            DATEDIFF(NOW(), MAX(transaction_date)) as recency_days,
            COUNT(*) as frequency,
            SUM(amount) as monetary
          FROM transactions
          WHERE transaction_date >= DATE_SUB(NOW(), INTERVAL 24 MONTH)
          GROUP BY customer_id
        ),
        rfm_scores AS (
          SELECT
            customer_id,
            recency_days,
            frequency,
            monetary,
            NTILE(5) OVER (ORDER BY recency_days DESC) as R_score,
            NTILE(5) OVER (ORDER BY frequency ASC) as F_score,
            NTILE(5) OVER (ORDER BY monetary ASC) as M_score
          FROM rfm_base
        )
        SELECT
          customer_id,
          R_score,
          F_score,
          M_score,
          CONCAT(R_score, F_score, M_score) as RFM_segment,
          CASE
            WHEN R_score >= 4 AND F_score >= 4 AND M_score >= 4 THEN 'Champions'
            WHEN R_score >= 4 AND F_score >= 3 THEN 'Loyal Customers'
            WHEN R_score >= 4 AND F_score <= 2 THEN 'Recent Customers'
            WHEN R_score >= 3 AND F_score >= 3 AND M_score >= 3 THEN 'Potential Loyalists'
            WHEN R_score <= 2 AND F_score >= 4 AND M_score >= 4 THEN 'At Risk'
            WHEN R_score <= 2 AND F_score <= 2 THEN 'Lost'
            ELSE 'Others'
          END as segment_name
        FROM rfm_scores

    step_2_segment_behavior:
      description: "Analisar comportamento histórico por segmento"
      code_sql: |
        SELECT
          segment_name,
          COUNT(*) as customer_count,
          AVG(monetary) as avg_historical_value,
          AVG(frequency) as avg_frequency,
          AVG(recency_days) as avg_recency,
          -- Estimar retention baseado em recency
          SUM(CASE WHEN recency_days <= 90 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as retention_proxy
        FROM rfm_with_segments
        GROUP BY segment_name

    step_3_project_clv:
      description: "Projetar CLV por segmento"
      formula: |
        CLV_segment = AVG_historical_value × Retention_proxy × Growth_factor × Time_horizon

        Onde Growth_factor varia por segmento:
        - Champions: 1.2 (espera-se crescimento)
        - Loyal: 1.1
        - At Risk: 0.5 (espera-se queda)
        - Lost: 0.1 (baixa probabilidade de retorno)
```

### Método 2C: Markov Chain CLV

```yaml
formula:
  name: "Markov Chain CLV Model"
  description: |
    Modelo estados onde clientes transitam entre níveis de engajamento.
    Útil para negócios com jornadas de cliente bem definidas.

  states:
    - "New" (recém adquirido)
    - "Active" (comprou recentemente)
    - "At Risk" (não comprou há X dias)
    - "Dormant" (não comprou há Y dias)
    - "Churned" (estado absorvente)

  transition_matrix_example: |
    De/Para    | New   | Active | At Risk | Dormant | Churned |
    -----------|-------|--------|---------|---------|---------|
    New        | 0.00  | 0.60   | 0.25    | 0.10    | 0.05    |
    Active     | 0.00  | 0.70   | 0.20    | 0.05    | 0.05    |
    At Risk    | 0.00  | 0.20   | 0.40    | 0.25    | 0.15    |
    Dormant    | 0.00  | 0.05   | 0.10    | 0.50    | 0.35    |
    Churned    | 0.00  | 0.00   | 0.00    | 0.00    | 1.00    |

  revenue_per_state:
    New: "$50 (primeira compra)"
    Active: "$100 (compras regulares)"
    At Risk: "$30 (compras reduzidas)"
    Dormant: "$0"
    Churned: "$0"

  clv_calculation: |
    CLV = Σ (Probabilidade de estar em estado S no tempo t) × (Receita do estado S)

    Implementado através de multiplicação matricial:
    CLV = r × (I - Q)^(-1) × 1

    Onde:
    - r = vetor de receitas por estado
    - Q = submatriz de transição (sem estado absorvente)
    - I = matriz identidade
```

---

## Phase 3: CLV Probabilístico (Fader/Hardie)

**Quando usar:** Setting não-contratual onde churn é latente. Estado da arte para e-commerce, varejo.

### Fundamentação Teórica

```yaml
peter_fader_philosophy:
  core_insight: |
    "Em negócios não-contratuais, não sabemos quando um cliente 'morre'.
    Devemos modelar probabilisticamente se ele ainda está 'vivo' e qual
    será seu comportamento futuro."

  key_distinction: |
    ERRADO: "Este cliente não comprou há 6 meses, está churned"
    CERTO: "Este cliente tem 23% de probabilidade de ainda estar ativo"

  quote: |
    "Most companies focus too much on 'How many customers do we have?'
    when the better question is 'How valuable are our customers?'"
    - Peter Fader

model_overview:
  bg_nbd:
    full_name: "Beta-Geometric/Negative Binomial Distribution"
    purpose: "Modelar frequência de transações futuras"
    paper: "Fader, Hardie, Lee (2005) - 'Counting Your Customers the Easy Way'"

  gamma_gamma:
    full_name: "Gamma-Gamma Model"
    purpose: "Modelar valor monetário das transações"
    paper: "Fader & Hardie (2013)"

  combined:
    clv_formula: "E[CLV] = E[Transactions] × E[Average Order Value]"
    where: |
      E[Transactions] vem do BG/NBD
      E[Average Order Value] vem do Gamma-Gamma
```

### Preparação de Dados para BG/NBD

```yaml
data_preparation:
  required_format:
    name: "RFM Summary Format"
    columns:
      - frequency: "Número de transações REPETIDAS (excluindo primeira)"
      - recency: "Tempo desde primeira até última transação"
      - T: "Tempo desde primeira transação até hoje (age)"
      - monetary_value: "Valor médio por transação (excluindo primeira)"

  important_notes:
    - "Frequency exclui a primeira transação (é count of repeat purchases)"
    - "Recency é tempo entre PRIMEIRA e ÚLTIMA transação, não entre última e hoje"
    - "T é a 'idade' do cliente desde aquisição"
    - "Todas as medidas de tempo devem ser na mesma unidade (dias, semanas, etc.)"

  code_sql: |
    WITH customer_transactions AS (
      SELECT
        customer_id,
        transaction_date,
        amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date) as txn_order
      FROM transactions
    ),
    customer_first AS (
      SELECT customer_id, transaction_date as first_date
      FROM customer_transactions
      WHERE txn_order = 1
    ),
    customer_last AS (
      SELECT customer_id, MAX(transaction_date) as last_date
      FROM customer_transactions
      GROUP BY customer_id
    ),
    repeat_purchases AS (
      SELECT
        customer_id,
        COUNT(*) as frequency,
        AVG(amount) as monetary_value
      FROM customer_transactions
      WHERE txn_order > 1  -- Excluindo primeira transação
      GROUP BY customer_id
    )
    SELECT
      cf.customer_id,
      COALESCE(rp.frequency, 0) as frequency,
      CASE
        WHEN rp.frequency > 0 THEN DATEDIFF(cl.last_date, cf.first_date)
        ELSE 0
      END as recency,
      DATEDIFF(CURDATE(), cf.first_date) as T,
      COALESCE(rp.monetary_value, 0) as monetary_value
    FROM customer_first cf
    LEFT JOIN customer_last cl ON cf.customer_id = cl.customer_id
    LEFT JOIN repeat_purchases rp ON cf.customer_id = rp.customer_id

  code_python_pandas: |
    import pandas as pd
    from lifetimes.utils import summary_data_from_transaction_data

    # Preparar dados
    df = pd.read_sql(query, connection)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Criar summary data para lifetimes
    summary = summary_data_from_transaction_data(
        df,
        customer_id_col='customer_id',
        datetime_col='transaction_date',
        monetary_value_col='amount',
        observation_period_end='2026-01-23'  # Data de análise
    )

    # Resultado: DataFrame com frequency, recency, T, monetary_value
    print(summary.head())
```

### BG/NBD Model Implementation

```yaml
bg_nbd_model:
  assumptions:
    - "Enquanto ativo, cliente transaciona conforme Poisson com taxa λ"
    - "Taxa λ varia entre clientes seguindo distribuição Gamma"
    - "Após cada transação, cliente 'morre' com probabilidade p"
    - "Probabilidade p varia entre clientes seguindo distribuição Beta"
    - "Heterogeneidade capturada por distribuições Gamma e Beta"

  parameters:
    r: "Shape parameter da Gamma (frequência)"
    alpha: "Scale parameter da Gamma (frequência)"
    a: "Shape parameter da Beta (dropout)"
    b: "Shape parameter da Beta (dropout)"

  code_python: |
    from lifetimes import BetaGeoFitter

    # Fit BG/NBD model
    bgf = BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(
        summary['frequency'],
        summary['recency'],
        summary['T']
    )

    # View fitted parameters
    print(bgf.summary)

    # Predict expected transactions in next 30 days for each customer
    summary['predicted_purchases_30d'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        30,
        summary['frequency'],
        summary['recency'],
        summary['T']
    )

    # Probability of being alive
    summary['prob_alive'] = bgf.conditional_probability_alive(
        summary['frequency'],
        summary['recency'],
        summary['T']
    )

    # Expected purchases for whole customer base
    expected_total_30d = bgf.expected_number_of_purchases_up_to_time(30)

  interpretation:
    prob_alive: |
      - prob_alive > 0.8: Likely still active customer
      - prob_alive 0.5-0.8: At risk, may need reactivation
      - prob_alive 0.2-0.5: Probably churned, win-back needed
      - prob_alive < 0.2: Almost certainly churned

    predicted_purchases: |
      - Use para forecasting de demanda
      - Aggregate para projeção de receita
      - Individual para prioritização de outreach
```

### Gamma-Gamma Model Implementation

```yaml
gamma_gamma_model:
  purpose: "Modelar valor monetário das transações"

  assumption_critical: |
    IMPORTANTE: Gamma-Gamma assume que frequência e valor são INDEPENDENTES.

    Verificar com correlação:
    correlation = df[['frequency', 'monetary_value']].corr()

    Se correlação > 0.3, resultados podem ser imprecisos.

  code_python: |
    from lifetimes import GammaGammaFitter

    # Filtrar clientes com ao menos 1 repeat purchase
    returning_customers = summary[summary['frequency'] > 0]

    # Fit Gamma-Gamma model
    ggf = GammaGammaFitter(penalizer_coef=0.0)
    ggf.fit(
        returning_customers['frequency'],
        returning_customers['monetary_value']
    )

    # Expected average profit (conditional)
    summary['expected_avg_profit'] = ggf.conditional_expected_average_profit(
        summary['frequency'],
        summary['monetary_value']
    )

    print(f"Expected avg order value: ${summary['expected_avg_profit'].mean():,.2f}")
```

### Combined CLV Calculation

```yaml
combined_clv:
  formula: |
    CLV = E[Purchases in period] × E[Average Order Value] × Margin

    Com desconto (NPV):
    CLV = Σ (E[Purchases_t] × E[AOV] × Margin) / (1 + d)^t

  code_python: |
    from lifetimes import BetaGeoFitter, GammaGammaFitter

    # Fit models
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])

    ggf = GammaGammaFitter(penalizer_coef=0.001)
    ggf.fit(
        summary[summary['frequency'] > 0]['frequency'],
        summary[summary['frequency'] > 0]['monetary_value']
    )

    # Calculate CLV for 12 months
    summary['clv_12m'] = ggf.customer_lifetime_value(
        bgf,
        summary['frequency'],
        summary['recency'],
        summary['T'],
        summary['monetary_value'],
        time=12,  # months
        freq='D',  # frequency of T is in days
        discount_rate=0.01  # monthly discount rate
    )

    # Top 10 most valuable customers
    top_customers = summary.nlargest(10, 'clv_12m')[
        ['customer_id', 'frequency', 'monetary_value', 'prob_alive', 'clv_12m']
    ]
    print(top_customers)

    # Aggregate metrics
    print(f"Total 12-month CLV: ${summary['clv_12m'].sum():,.2f}")
    print(f"Average 12-month CLV: ${summary['clv_12m'].mean():,.2f}")
    print(f"Median 12-month CLV: ${summary['clv_12m'].median():,.2f}")

  model_validation:
    holdout_test: |
      # Split data: calibration vs holdout
      # Fit model on calibration period
      # Compare predictions vs actual in holdout

      from lifetimes.utils import calibration_and_holdout_data

      summary_cal_holdout = calibration_and_holdout_data(
          df,
          'customer_id',
          'transaction_date',
          calibration_period_end='2025-06-30',
          observation_period_end='2026-01-23'
      )

      # Fit on calibration
      bgf.fit(
          summary_cal_holdout['frequency_cal'],
          summary_cal_holdout['recency_cal'],
          summary_cal_holdout['T_cal']
      )

      # Predict for holdout period
      summary_cal_holdout['predicted'] = bgf.conditional_expected_number_of_purchases_up_to_time(
          summary_cal_holdout['duration_holdout'],
          summary_cal_holdout['frequency_cal'],
          summary_cal_holdout['recency_cal'],
          summary_cal_holdout['T_cal']
      )

      # Compare predicted vs actual
      from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases
      plot_calibration_purchases_vs_holdout_purchases(bgf, summary_cal_holdout)
```

---

## Phase 4: Segmentação por CLV

### Criar Segmentos de Valor

```yaml
segmentation_approach:
  principle: |
    "Not all customers are created equal. Treat them unequally
    (proportionally to their value)." - Peter Fader

  methodology:
    step_1: "Calcular CLV para cada cliente"
    step_2: "Ordenar por CLV"
    step_3: "Criar segmentos (decis, quintis, ou custom)"
    step_4: "Analisar características de cada segmento"
    step_5: "Definir estratégias diferenciadas"

segment_definitions:
  by_deciles:
    top_10: "Champions - 10% mais valiosos"
    top_10_30: "Gold - Próximos 20%"
    top_30_60: "Silver - Próximos 30%"
    bottom_40: "Bronze - 40% de menor valor"

  by_value_thresholds:
    example: |
      VIP: CLV > $5,000
      High: CLV $1,000-$5,000
      Medium: CLV $200-$1,000
      Low: CLV $50-$200
      Minimal: CLV < $50

code_python: |
  # Criar segmentos por percentil
  summary['clv_segment'] = pd.qcut(
      summary['clv_12m'],
      q=[0, 0.4, 0.6, 0.8, 0.9, 1.0],
      labels=['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
  )

  # Análise por segmento
  segment_analysis = summary.groupby('clv_segment').agg({
      'customer_id': 'count',
      'clv_12m': ['sum', 'mean', 'median'],
      'frequency': 'mean',
      'monetary_value': 'mean',
      'prob_alive': 'mean',
      'recency': 'mean'
  }).round(2)

  print(segment_analysis)

  # Pareto analysis
  total_clv = summary['clv_12m'].sum()
  summary_sorted = summary.sort_values('clv_12m', ascending=False)
  summary_sorted['cumulative_clv'] = summary_sorted['clv_12m'].cumsum()
  summary_sorted['cumulative_pct'] = summary_sorted['cumulative_clv'] / total_clv * 100

  # Find what % of customers = 80% of CLV
  pct_for_80 = (summary_sorted['cumulative_pct'] <= 80).sum() / len(summary_sorted) * 100
  print(f"{pct_for_80:.1f}% dos clientes representam 80% do CLV total")
```

### Estratégias por Segmento

```yaml
segment_strategies:
  champions_diamond:
    clv_range: "Top 10% (maior CLV)"
    characteristics:
      - "Alta frequência de compra"
      - "Alto ticket médio"
      - "Alta prob_alive"
      - "Compra recente"

    strategy:
      retention_focus: "MÁXIMO"
      investment_level: "Premium"

      tactics:
        - "Gerente de conta dedicado"
        - "Acesso antecipado a novos produtos"
        - "Programa VIP exclusivo"
        - "Pesquisas qualitativas (entender o que funciona)"
        - "Never let them churn - alarmes para qualquer sinal"

      kpis_to_track:
        - "Retention rate deste segmento"
        - "Share of wallet"
        - "NPS/CSAT"
        - "Frequency trend"

    warning: |
      "Estes clientes já são valiosos. Foco é MANTER, não tentar
      extrair mais valor de forma agressiva (pode alienar)."

  gold_platinum:
    clv_range: "Top 10-30%"
    characteristics:
      - "Boa frequência"
      - "Ticket médio bom"
      - "Potencial de subir para Champions"

    strategy:
      focus: "DEVELOPMENT"
      goal: "Aumentar CLV para nível Champion"

      tactics:
        - "Upsell/cross-sell estratégico"
        - "Programa de loyalty com benefícios escaláveis"
        - "Educação sobre portfolio completo"
        - "Ofertas exclusivas para aumentar frequência"

      kpis_to_track:
        - "Migration rate para Champions"
        - "Aumento de frequency"
        - "Aumento de basket size"

  silver:
    clv_range: "30-60%"
    characteristics:
      - "Frequência moderada"
      - "Ticket médio"
      - "Potencial variado"

    strategy:
      focus: "EFFICIENCY"
      goal: "Maximizar valor com custo proporcional"

      tactics:
        - "Automações de marketing (email, push)"
        - "Ofertas sazonais"
        - "Programa de pontos básico"
        - "Self-service predominante"

      kpis_to_track:
        - "ROI de campanhas"
        - "Cost per retained customer"

  bronze_minimal:
    clv_range: "Bottom 40%"
    characteristics:
      - "Baixa frequência"
      - "Baixo ticket"
      - "Muitos one-time purchasers"

    strategy:
      focus: "MINIMUM VIABLE"
      goal: "Não perder dinheiro servindo estes clientes"

      tactics:
        - "Comunicação apenas automatizada"
        - "Sem investimento em retenção proativa"
        - "Self-service apenas"
        - "Identificar potenciais 'diamonds in rough'"

      important_note: |
        "NUNCA trate mal estes clientes - eles podem virar valiosos
        ou influenciar outros. Apenas não invista mais do que retorna."

      reactivation_strategy: |
        "Testar ofertas agressivas (deep discounts) para identificar
        quem pode ser reativado. Se não responder, deprioritizar."
```

---

## Phase 5: Output e Relatório Final

### Template de Relatório CLV

```yaml
clv_report_structure:
  executive_summary:
    total_customer_equity: "$[X] (soma de todos CLVs)"
    average_clv: "$[X]"
    median_clv: "$[X]"
    clv_cac_ratio: "[X]:1"
    payback_period: "[X] meses"

    key_findings:
      finding_1: "[Concentração de valor: X% clientes = Y% valor]"
      finding_2: "[Trend: CLV de novos cohorts está melhorando/piorando]"
      finding_3: "[Segment insight mais importante]"

    strategic_implications:
      - "[Implicação 1 para estratégia]"
      - "[Implicação 2]"
      - "[Implicação 3]"

  methodology_section:
    model_used: "[BG/NBD + Gamma-Gamma / Contratual / Histórico]"
    time_period_analyzed: "[X] a [Y]"
    time_horizon_projected: "[N] meses"
    discount_rate: "[X]%"

    data_quality_notes:
      - "[Nota sobre qualidade dos dados]"
      - "[Limitações conhecidas]"

    model_validation:
      holdout_test_result: "MAPE = [X]%"
      confidence_level: "[Alta/Média/Baixa]"

  segment_analysis:
    segment_1:
      name: "[Champions/Diamond]"
      customer_count: "[N] ([X]% do total)"
      total_clv: "$[X] ([Y]% do total)"
      average_clv: "$[X]"
      key_characteristics:
        - "Freq média: [X]"
        - "AOV médio: $[X]"
        - "Prob alive: [X]%"
      recommended_strategy: "[Resumo da estratégia]"

    # ... repeat for each segment

  pareto_analysis:
    top_1_pct: "[N] clientes representam [X]% do CLV"
    top_5_pct: "[N] clientes representam [X]% do CLV"
    top_10_pct: "[N] clientes representam [X]% do CLV"
    top_20_pct: "[N] clientes representam [X]% do CLV"

    visualization: "[Lorenz curve / Pareto chart]"

  cohort_comparison:
    best_cohort:
      cohort_id: "[YYYY-MM]"
      average_clv: "$[X]"
      notable_traits: "[O que diferencia este cohort]"

    worst_cohort:
      cohort_id: "[YYYY-MM]"
      average_clv: "$[X]"
      possible_reasons: "[Hipóteses]"

    trend_analysis: "[CLV está melhorando/piorando ao longo do tempo]"

  actionable_recommendations:
    immediate_actions:
      - action: "[Ação 1]"
        segment_impacted: "[Segmento]"
        expected_impact: "[X]% aumento em CLV"
        effort: "[Alto/Médio/Baixo]"

      - action: "[Ação 2]"
        # ...

    medium_term_initiatives:
      - "[Iniciativa 1]"
      - "[Iniciativa 2]"

    metrics_to_track:
      - "CLV médio por cohort (mensal)"
      - "Distribuição de segmentos (quarterly)"
      - "CLV:CAC ratio"
      - "Payback period"

  appendix:
    detailed_sql_queries: "[Link para queries]"
    model_parameters: "[Parâmetros fitted do BG/NBD e Gamma-Gamma]"
    full_segment_breakdown: "[Tabela completa]"
    customer_level_export: "[Link para arquivo com CLV individual]"
```

---

## Elicitation Questions (Perguntas de Descoberta)

```yaml
discovery_questions:
  business_context:
    - "Qual é o seu modelo de negócio? (subscription, e-commerce, híbrido)"
    - "Qual é a frequência típica de compra dos seus clientes?"
    - "Você tem dados de margem por transação?"
    - "Há quanto tempo você coleta dados transacionais?"

  analytical_maturity:
    - "Você já calculou CLV antes? Qual método usou?"
    - "Você tem times de analytics/data science?"
    - "Quais ferramentas de BI você usa?"
    - "Os dados estão centralizados em um data warehouse?"

  strategic_goals:
    - "O principal objetivo é segmentação, previsão, ou valuation?"
    - "Você quer CLV por cliente individual ou por segmento?"
    - "Qual é o CAC atual? Você sabe o CLV:CAC ratio?"
    - "Existe pressão para mostrar ROI de iniciativas de retenção?"

  data_specifics:
    - "Quantos clientes únicos você tem no histórico?"
    - "Qual é o período de dados disponível?"
    - "Há clientes B2B e B2C misturados?"
    - "Transações canceladas/reembolsadas estão marcadas?"
```

---

## Common Pitfalls e Como Evitar

```yaml
pitfalls:
  pitfall_1_confusing_revenue_with_margin:
    problem: "Calcular CLV em receita bruta superestima valor real"
    solution: "Sempre usar margem quando possível"
    if_no_margin: "Aplicar margem média conhecida ao resultado final"

  pitfall_2_ignoring_time_value_money:
    problem: "CLV sem desconto ignora custo de capital"
    solution: "Sempre aplicar discount rate (10-15% anual é razoável)"

  pitfall_3_treating_all_customers_equal:
    problem: "Métricas agregadas escondem heterogeneidade"
    solution: "Sempre analisar distribuição e segmentos, não apenas média"

  pitfall_4_using_wrong_recency_definition:
    problem: "BG/NBD usa recency diferente do RFM tradicional"
    solution: "Para BG/NBD: recency = tempo entre PRIMEIRA e ÚLTIMA compra"

  pitfall_5_not_validating_model:
    problem: "Confiar cegamente em projeções sem validação"
    solution: "Sempre fazer holdout test comparando previsão vs realidade"

  pitfall_6_over_engineering_for_small_data:
    problem: "Usar BG/NBD com poucos clientes ou curto histórico"
    solution: "Para <1000 clientes ou <12 meses, usar métodos simples"

  pitfall_7_mixing_b2b_b2c:
    problem: "B2B tem comportamento muito diferente de B2C"
    solution: "Sempre analisar separadamente ou com modelos distintos"
```

---

## Ferramentas e Bibliotecas Recomendadas

```yaml
python_libraries:
  lifetimes:
    description: "Biblioteca mais usada para BG/NBD e Gamma-Gamma"
    install: "pip install lifetimes"
    docs: "https://lifetimes.readthedocs.io/"
    status: "Mature but no longer actively maintained"

  pymc_marketing:
    description: "Implementação Bayesiana moderna dos modelos"
    install: "pip install pymc-marketing"
    docs: "https://www.pymc-marketing.io/"
    advantages:
      - "Quantificação de incerteza"
      - "Mais flexível"
      - "Ativamente mantida"

  btyd:
    description: "Pacote R com implementações clássicas"
    install: "install.packages('BTYD')"

sql_approaches:
  description: "Para empresas que preferem não usar Python/R"
  recommendation: "Implementar CLV histórico e por cohort em SQL"
  note: "Modelos probabilísticos são complexos para SQL puro"

bi_tools:
  - "Looker com custom measures para CLV"
  - "Tableau com calculated fields"
  - "Power BI com DAX measures"
  - "Metabase com custom questions"
```

---

## Quick Reference: Fórmulas

```yaml
formulas_summary:
  historical_simple:
    formula: "CLV = Σ Transações do cliente"
    use_case: "Baseline, análise retroativa"

  historical_normalized:
    formula: "CLV = (Receita Total / Meses de Vida) × Expectativa de Vida"
    use_case: "Comparar clientes novos e antigos"

  contractual_basic:
    formula: "CLV = ARPU × Margin / Churn Rate"
    use_case: "SaaS, subscriptions"

  contractual_npv:
    formula: "CLV = ARPU × Margin / (Churn Rate + Discount Rate)"
    use_case: "SaaS com valor presente"

  probabilistic:
    formula: "CLV = E[Purchases] × E[AOV] × Margin"
    where: "E[Purchases] de BG/NBD, E[AOV] de Gamma-Gamma"
    use_case: "E-commerce, varejo, não-contratual"

  key_ratios:
    clv_cac_ratio:
      formula: "CLV:CAC = CLV / CAC"
      healthy: ">= 3:1"
      minimum: ">= 1:1"

    payback_period:
      formula: "Payback = CAC / (ARPU × Margin)"
      healthy: "<= 12 meses"
```

---

## References

```yaml
academic_sources:
  - title: "Counting Your Customers the Easy Way: An Alternative to the Pareto/NBD Model"
    authors: "Fader, Hardie, Lee"
    year: 2005
    journal: "Marketing Science"
    importance: "Paper original do BG/NBD"

  - title: "Customer-Base Analysis in a Discrete-Time Noncontractual Setting"
    authors: "Fader, Hardie, Shang"
    year: 2010
    journal: "Marketing Science"
    importance: "Extensão para discrete time"

  - title: "Probability Models for Customer-Base Analysis"
    authors: "Fader, Hardie"
    year: 2009
    importance: "Overview completo dos modelos"

books:
  - title: "Customer Centricity: Focus on the Right Customers for Strategic Advantage"
    author: "Peter Fader"
    year: 2012
    importance: "Filosofia por trás de CLV"

  - title: "The Customer Centricity Playbook"
    authors: "Fader, Toms"
    year: 2018
    importance: "Implementação prática"

online_resources:
  - "brucehardie.com - Papers e tutoriais"
  - "petefader.com - Recursos adicionais"
  - "Lifetimes documentation"
  - "PyMC-Marketing documentation"
```

---

*Task Version: 1.0*
*Primary Agent: Peter Fader*
*Supporting Agents: Nick Mehta (Health Score integration), Sean Ellis (Growth metrics)*
*Lines: 900+*
*Research Base: Fader/Hardie papers, Wharton research, lifetimes library*

---

# Appendix: Complete Python Implementation

```python
"""
Complete CLV Calculation Pipeline
Based on Fader/Hardie methodology

Requirements:
pip install pandas numpy lifetimes matplotlib seaborn
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# For probabilistic models
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.utils import calibration_and_holdout_data
from lifetimes.plotting import (
    plot_frequency_recency_matrix,
    plot_probability_alive_matrix,
    plot_period_transactions,
    plot_calibration_purchases_vs_holdout_purchases
)


class CLVCalculator:
    """
    Complete CLV calculation following Fader/Hardie methodology.
    """

    def __init__(self, transactions_df,
                 customer_id_col='customer_id',
                 date_col='transaction_date',
                 amount_col='amount',
                 observation_period_end=None):
        """
        Initialize CLV Calculator.

        Args:
            transactions_df: DataFrame with transaction data
            customer_id_col: Column name for customer ID
            date_col: Column name for transaction date
            amount_col: Column name for transaction amount
            observation_period_end: End date for analysis (default: today)
        """
        self.df = transactions_df.copy()
        self.customer_id_col = customer_id_col
        self.date_col = date_col
        self.amount_col = amount_col
        self.observation_period_end = observation_period_end or datetime.now()

        # Convert date column
        self.df[date_col] = pd.to_datetime(self.df[date_col])

        # Initialize models
        self.bgf = None
        self.ggf = None
        self.summary = None

    def prepare_data(self):
        """Prepare data in RFM format for lifetimes."""
        self.summary = summary_data_from_transaction_data(
            self.df,
            customer_id_col=self.customer_id_col,
            datetime_col=self.date_col,
            monetary_value_col=self.amount_col,
            observation_period_end=self.observation_period_end
        )
        return self.summary

    def calculate_historical_clv(self):
        """Calculate simple historical CLV."""
        historical = self.df.groupby(self.customer_id_col).agg({
            self.amount_col: ['sum', 'mean', 'count'],
            self.date_col: ['min', 'max']
        })
        historical.columns = ['total_revenue', 'avg_order_value',
                             'order_count', 'first_purchase', 'last_purchase']
        historical['tenure_days'] = (historical['last_purchase'] -
                                     historical['first_purchase']).dt.days
        return historical

    def fit_bgnbd(self, penalizer_coef=0.001):
        """Fit BG/NBD model for purchase frequency."""
        if self.summary is None:
            self.prepare_data()

        self.bgf = BetaGeoFitter(penalizer_coef=penalizer_coef)
        self.bgf.fit(
            self.summary['frequency'],
            self.summary['recency'],
            self.summary['T']
        )
        return self.bgf

    def fit_gamma_gamma(self, penalizer_coef=0.001):
        """Fit Gamma-Gamma model for monetary value."""
        if self.summary is None:
            self.prepare_data()

        # Filter to returning customers only
        returning = self.summary[self.summary['frequency'] > 0]

        self.ggf = GammaGammaFitter(penalizer_coef=penalizer_coef)
        self.ggf.fit(
            returning['frequency'],
            returning['monetary_value']
        )
        return self.ggf

    def calculate_probabilistic_clv(self, time_months=12,
                                    discount_rate_monthly=0.01,
                                    margin=1.0):
        """
        Calculate probabilistic CLV using BG/NBD + Gamma-Gamma.

        Args:
            time_months: Projection period in months
            discount_rate_monthly: Monthly discount rate
            margin: Gross margin (1.0 = 100%, 0.7 = 70%)

        Returns:
            DataFrame with CLV for each customer
        """
        if self.bgf is None:
            self.fit_bgnbd()
        if self.ggf is None:
            self.fit_gamma_gamma()

        # Calculate CLV
        clv = self.ggf.customer_lifetime_value(
            self.bgf,
            self.summary['frequency'],
            self.summary['recency'],
            self.summary['T'],
            self.summary['monetary_value'],
            time=time_months,
            freq='D',
            discount_rate=discount_rate_monthly
        ) * margin

        # Add to summary
        self.summary['clv'] = clv
        self.summary['prob_alive'] = self.bgf.conditional_probability_alive(
            self.summary['frequency'],
            self.summary['recency'],
            self.summary['T']
        )

        return self.summary

    def segment_customers(self, clv_column='clv',
                         segments=['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond'],
                         quantiles=[0, 0.4, 0.6, 0.8, 0.9, 1.0]):
        """Segment customers by CLV."""
        self.summary['segment'] = pd.qcut(
            self.summary[clv_column],
            q=quantiles,
            labels=segments
        )
        return self.summary.groupby('segment').agg({
            clv_column: ['count', 'sum', 'mean', 'median'],
            'frequency': 'mean',
            'monetary_value': 'mean',
            'prob_alive': 'mean'
        })

    def pareto_analysis(self, clv_column='clv'):
        """Perform Pareto analysis on CLV."""
        sorted_df = self.summary.sort_values(clv_column, ascending=False)
        sorted_df['cumulative_clv'] = sorted_df[clv_column].cumsum()
        sorted_df['cumulative_pct'] = sorted_df['cumulative_clv'] / sorted_df[clv_column].sum()
        sorted_df['customer_pct'] = (range(1, len(sorted_df) + 1)) / len(sorted_df)

        # Find key thresholds
        results = {}
        for pct in [0.1, 0.2, 0.5]:
            n_customers = int(len(sorted_df) * pct)
            value_pct = sorted_df.iloc[:n_customers]['cumulative_pct'].iloc[-1]
            results[f'top_{int(pct*100)}%_customers'] = f"{value_pct*100:.1f}% of CLV"

        return results, sorted_df

    def validate_model(self, calibration_end, holdout_end=None):
        """Validate model using calibration/holdout approach."""
        holdout_end = holdout_end or self.observation_period_end

        summary_cal = calibration_and_holdout_data(
            self.df,
            self.customer_id_col,
            self.date_col,
            calibration_period_end=calibration_end,
            observation_period_end=holdout_end
        )

        # Fit on calibration
        bgf_cal = BetaGeoFitter()
        bgf_cal.fit(
            summary_cal['frequency_cal'],
            summary_cal['recency_cal'],
            summary_cal['T_cal']
        )

        # Predict
        summary_cal['predicted'] = bgf_cal.conditional_expected_number_of_purchases_up_to_time(
            summary_cal['duration_holdout'],
            summary_cal['frequency_cal'],
            summary_cal['recency_cal'],
            summary_cal['T_cal']
        )

        # Calculate MAPE
        actual = summary_cal['frequency_holdout']
        predicted = summary_cal['predicted']
        mape = np.mean(np.abs((actual - predicted) / (actual + 1))) * 100

        return {
            'mape': mape,
            'summary': summary_cal,
            'model': bgf_cal
        }

    def generate_report(self, clv_column='clv'):
        """Generate comprehensive CLV report."""
        report = {
            'total_customers': len(self.summary),
            'total_clv': self.summary[clv_column].sum(),
            'average_clv': self.summary[clv_column].mean(),
            'median_clv': self.summary[clv_column].median(),
            'std_clv': self.summary[clv_column].std(),
            'percentiles': {
                'p10': self.summary[clv_column].quantile(0.10),
                'p25': self.summary[clv_column].quantile(0.25),
                'p50': self.summary[clv_column].quantile(0.50),
                'p75': self.summary[clv_column].quantile(0.75),
                'p90': self.summary[clv_column].quantile(0.90),
                'p99': self.summary[clv_column].quantile(0.99)
            },
            'pareto': self.pareto_analysis(clv_column)[0]
        }
        return report


# Example usage
if __name__ == "__main__":
    # Sample data creation (replace with real data)
    np.random.seed(42)
    n_customers = 1000

    transactions = []
    for cid in range(n_customers):
        n_purchases = np.random.poisson(3) + 1
        for _ in range(n_purchases):
            transactions.append({
                'customer_id': f'C{cid:04d}',
                'transaction_date': pd.Timestamp('2024-01-01') +
                    pd.Timedelta(days=np.random.randint(0, 700)),
                'amount': np.random.lognormal(4, 0.5)
            })

    df = pd.DataFrame(transactions)

    # Initialize calculator
    calc = CLVCalculator(df)

    # Calculate CLV
    calc.prepare_data()
    calc.fit_bgnbd()
    calc.fit_gamma_gamma()
    results = calc.calculate_probabilistic_clv(time_months=12, margin=0.70)

    # Generate segments
    segments = calc.segment_customers()

    # Generate report
    report = calc.generate_report()

    print("="*50)
    print("CLV REPORT")
    print("="*50)
    print(f"Total Customers: {report['total_customers']:,}")
    print(f"Total CLV: ${report['total_clv']:,.2f}")
    print(f"Average CLV: ${report['average_clv']:,.2f}")
    print(f"Median CLV: ${report['median_clv']:,.2f}")
    print("\nPareto Analysis:")
    for k, v in report['pareto'].items():
        print(f"  {k}: {v}")
    print("\nSegment Analysis:")
    print(segments)
```

---

## Acceptance Criteria

- [ ] O modelo de negócio, o horizonte de projeção e as premissas financeiras foram documentados antes do cálculo.
- [ ] O método de CLV escolhido é compatível com a qualidade e a cobertura dos dados disponíveis.
- [ ] O output final separa claramente entregáveis canônicos de outputs ad-hoc.
- [ ] O relatório inclui segmentos de valor, projeções e recomendações acionáveis.

*End of Task: calculate-clv.md*
*Lines: 1000+*
