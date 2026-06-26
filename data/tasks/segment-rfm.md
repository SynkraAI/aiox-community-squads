# RFM Customer Segmentation Task

## Purpose

Segmentar clientes usando análise RFM (Recency, Frequency, Monetary) - a metodologia mais consagrada e prática para classificar clientes por comportamento de compra. Esta task implementa múltiplos sistemas de scoring, 11 segmentos comportamentais detalhados, e playbooks de ação específicos para cada grupo, seguindo a filosofia de Peter Fader: "Trate clientes proporcionalmente ao seu valor."

## When to Use

- Precisa classificar clientes rapidamente sem modelos probabilísticos complexos
- Quer criar campanhas de marketing direcionadas por segmento
- Precisa identificar clientes em risco antes que seja tarde
- Quer descobrir seus melhores clientes (Champions) para tratamento VIP
- Precisa priorizar esforços de retenção com recursos limitados
- Quer criar programas de loyalty com benefícios diferenciados
- Precisa de baseline antes de implementar CLV probabilístico
- Quer entender a composição da sua base de clientes
- Precisa segmentar para A/B tests de campanhas
- Quer criar personas baseadas em comportamento real (não demográfico)

## Core Methodology

RFM é um framework de segmentação comportamental que classifica clientes por três dimensões:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          RFM FRAMEWORK                                    │
│                    "O passado prediz o futuro"                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  R - RECENCY (Recência)                                                  │
│  ─────────────────────                                                   │
│  Pergunta: "Quando foi a última compra?"                                 │
│  Por que importa: Clientes que compraram recentemente têm maior          │
│  probabilidade de comprar novamente. É o preditor mais forte.            │
│                                                                           │
│  F - FREQUENCY (Frequência)                                              │
│  ─────────────────────────                                               │
│  Pergunta: "Quantas vezes comprou no período?"                           │
│  Por que importa: Alta frequência indica hábito formado,                 │
│  lealdade comportamental (não apenas atitudinal).                        │
│                                                                           │
│  M - MONETARY (Monetário)                                                │
│  ─────────────────────────                                               │
│  Pergunta: "Quanto gastou no total?"                                     │
│  Por que importa: Indica capacidade e disposição de gastar.              │
│  Nem sempre o mais importante - frequência pode ser melhor preditor.     │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Peter Fader's Insight on RFM

> "RFM não é apenas uma ferramenta de segmentação - é uma janela para entender heterogeneidade de clientes. O erro mais comum é tratar todos os clientes igualmente. RFM revela quão diferentes eles realmente são."

---

## Task Metadata

```yaml
task:
  name: RFM Customer Segmentation
  id: segment-rfm
  version: "1.0"
  category: customer_analytics
  difficulty: basic_to_intermediate
  primary_agents:
    - peter-fader
  supporting_agents:
    - nick-mehta     # Integração com Health Score
    - avinash-kaushik  # Visualização e storytelling
  estimated_time: "2-4 hours"

  prerequisites:
    - Dados transacionais de clientes (mínimo 6 meses ideal, 3 meses mínimo)
    - Identificação única por cliente (customer_id)
    - Timestamps das transações
    - Valores monetários das transações

  outputs:
    - Score RFM por cliente (1-5 ou percentil)
    - Segmento atribuído (Champions, At Risk, etc.)
    - Distribuição de clientes por segmento
    - Recomendações de ação por segmento
    - Queries SQL/código Python para automação

  frameworks_used:
    - RFM Analysis (tradicional)
    - RFM Scoring (quintile-based)
    - RFM Segmentation Matrix
    - Customer Centricity (Fader)
```

---

## Phase 0: Pre-Flight Check

### Block A: Validação de Dados

```yaml
data_requirements:
  minimum_fields:
    customer_id:
      type: "string ou integer"
      description: "Identificador único do cliente"
      validation: "Não pode haver NULLs, deve ser consistente"

    transaction_date:
      type: "datetime ou date"
      description: "Data de cada transação"
      validation: "Formato consistente, sem datas futuras"

    transaction_amount:
      type: "numeric"
      description: "Valor de cada transação"
      validation: "Valores positivos (ou identificar refunds)"

  nice_to_have_fields:
    - order_id: "Para identificar transações únicas"
    - product_category: "Para RFM por categoria"
    - channel: "Para RFM por canal"
    - customer_segment_current: "Para validar contra segmentação existente"

data_quality_checklist:
  - question: "Há duplicatas de transações?"
    why: "Duplicatas inflam Frequency e Monetary"
    fix: "DISTINCT por order_id ou dedupe por timestamp+amount"

  - question: "Como refunds/chargebacks estão representados?"
    why: "Valores negativos afetam Monetary"
    options:
      - "Excluir da análise"
      - "Agregar (soma pode ser negativa)"
      - "Tratar separadamente"

  - question: "Há clientes B2B e B2C misturados?"
    why: "Comportamento muito diferente, RFM separado"
    fix: "Filtrar ou analisar separadamente"

  - question: "Qual período de análise?"
    guidance: |
      - Curto (3-6 meses): Captura tendências recentes, risco de sazonalidade
      - Médio (12 meses): Balanceado, um ciclo completo
      - Longo (24+ meses): Mais dados, mas comportamento antigo pode não ser relevante
    recommendation: "12 meses é o sweet spot para maioria dos negócios"
```

### Block B: Perguntas de Contexto

```yaml
context_questions:
  Q1_business_model:
    question: "Qual é a frequência típica de compra do seu negócio?"
    options:
      high_frequency:
        description: "Múltiplas vezes por mês (supermercado, app de delivery)"
        implication: "Recency em dias, Frequency alta é norma"
      medium_frequency:
        description: "1-2x por mês (e-commerce geral, SaaS mensal)"
        implication: "Recency em semanas, Frequency moderada"
      low_frequency:
        description: "Algumas vezes por ano (móveis, eletrônicos, cursos)"
        implication: "Recency em meses, Frequency baixa é normal"
      very_low:
        description: "1-2x por ano ou menos (carros, imóveis)"
        implication: "RFM tradicional menos aplicável"

  Q2_analysis_date:
    question: "Qual data usar como referência para Recency?"
    options:
      - "Hoje (análise em tempo real)"
      - "Fim do último mês fechado (consistência)"
      - "Data específica (comparabilidade histórica)"
    default: "Fim do último mês fechado"
    why: "Garante que análise pode ser reproduzida"

  Q3_scoring_method:
    question: "Qual método de scoring usar?"
    options:
      quintile:
        description: "Divide em 5 grupos de tamanho igual (20% cada)"
        pros: "Simples, sempre balanceado"
        cons: "Ignora distribuição real dos dados"

      percentile:
        description: "Score baseado no percentil exato"
        pros: "Mais preciso, captura nuances"
        cons: "Mais complexo de interpretar"

      fixed_thresholds:
        description: "Limiares fixos definidos pelo negócio"
        pros: "Consistente ao longo do tempo"
        cons: "Pode ficar desatualizado"

    recommendation: "Quintile para começar, evoluir para percentil"

  Q4_segment_count:
    question: "Quantos segmentos deseja?"
    options:
      simple_4:
        segments: ["Best", "Loyal", "At Risk", "Lost"]
        when: "Recursos limitados, começando"

      standard_8:
        segments: ["Champions", "Loyal", "Potential Loyalists", "Recent",
                   "Promising", "Need Attention", "At Risk", "Lost"]
        when: "Balanceado, recomendado"

      detailed_11:
        segments: ["Champions", "Loyal", "Potential Loyalists", "New Customers",
                   "Promising", "Need Attention", "About to Sleep", "At Risk",
                   "Cannot Lose", "Hibernating", "Lost"]
        when: "Marketing sofisticado, recursos para personalização"

    recommendation: "Standard 8 ou Detailed 11"
```

### Pre-Flight Output

```yaml
pre_flight_summary:
  analysis_period: "[Data início] a [Data fim]"
  reference_date: "[Data de referência para Recency]"
  total_customers: "[N]"
  total_transactions: "[N]"
  scoring_method: "[quintile/percentile/fixed]"
  segment_model: "[4/8/11 segments]"

  data_quality:
    duplicates_found: "[Sim/Não]"
    refunds_handling: "[Método escolhido]"
    outliers_handling: "[Método escolhido]"

  proceed: "[Sim/Não - com justificativa se não]"
```

---

## Phase 1: Calculate RFM Metrics

### Step 1.1: Raw RFM Calculation

```yaml
rfm_definitions:
  recency:
    definition: "Dias desde a última transação até a data de referência"
    formula: "reference_date - MAX(transaction_date)"
    interpretation: "Quanto MENOR, MELHOR (comprou mais recentemente)"

  frequency:
    definition: "Número total de transações no período"
    formula: "COUNT(transactions)"
    interpretation: "Quanto MAIOR, MELHOR"
    note: "Alguns usam COUNT - 1 para excluir primeira compra (BG/NBD style)"

  monetary:
    definition: "Valor total gasto no período"
    formula: "SUM(transaction_amount)"
    interpretation: "Quanto MAIOR, MELHOR"
    alternatives:
      - "Média por transação (para normalizar por frequência)"
      - "Margem em vez de receita (mais preciso)"
```

### SQL: Calculate Raw RFM

```sql
-- =============================================================================
-- RFM METRICS CALCULATION
-- Adaptável para PostgreSQL, MySQL, BigQuery, Snowflake
-- =============================================================================

-- Definir data de referência
-- PostgreSQL/Snowflake:
SET reference_date = '2026-01-23';  -- ou CURRENT_DATE

-- Alternativa MySQL:
-- SET @reference_date = '2026-01-23';

-- =============================================================================
-- STEP 1: Calculate Raw RFM Values
-- =============================================================================

WITH raw_rfm AS (
    SELECT
        customer_id,

        -- RECENCY: Dias desde última compra
        DATE_DIFF(
            '2026-01-23'::DATE,  -- reference_date
            MAX(transaction_date)::DATE,
            DAY
        ) AS recency_days,

        -- FREQUENCY: Total de transações
        COUNT(DISTINCT transaction_id) AS frequency,
        -- Nota: Use COUNT(*) se não tiver transaction_id único

        -- MONETARY: Total gasto
        SUM(amount) AS monetary_total,

        -- Métricas auxiliares
        MIN(transaction_date) AS first_purchase_date,
        MAX(transaction_date) AS last_purchase_date,
        AVG(amount) AS avg_order_value,
        DATE_DIFF(
            MAX(transaction_date)::DATE,
            MIN(transaction_date)::DATE,
            DAY
        ) AS customer_tenure_days

    FROM transactions
    WHERE
        transaction_date >= DATE_SUB('2026-01-23', INTERVAL 12 MONTH)
        AND transaction_date <= '2026-01-23'
        AND amount > 0  -- Excluir refunds se necessário
        -- AND customer_type = 'B2C'  -- Filtro se necessário
    GROUP BY customer_id
)

SELECT * FROM raw_rfm;

-- =============================================================================
-- VERIFICAÇÃO: Distribuição dos valores raw
-- =============================================================================

SELECT
    'Recency' AS metric,
    MIN(recency_days) AS min_val,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY recency_days) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY recency_days) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY recency_days) AS p75,
    MAX(recency_days) AS max_val,
    AVG(recency_days) AS avg_val
FROM raw_rfm

UNION ALL

SELECT
    'Frequency' AS metric,
    MIN(frequency),
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY frequency),
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY frequency),
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY frequency),
    MAX(frequency),
    AVG(frequency)
FROM raw_rfm

UNION ALL

SELECT
    'Monetary' AS metric,
    MIN(monetary_total),
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monetary_total),
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY monetary_total),
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monetary_total),
    MAX(monetary_total),
    AVG(monetary_total)
FROM raw_rfm;
```

---

## Phase 2: RFM Scoring

### Method 2A: Quintile Scoring (1-5)

O método mais comum e simples. Divide cada métrica em 5 grupos de tamanho igual.

```yaml
quintile_scoring:
  description: "Cada métrica é dividida em 5 quintis"

  scores:
    recency:
      # NOTA: Para Recency, MENOR é MELHOR, então invertemos
      score_5: "Top 20% (compraram mais recentemente)"
      score_4: "20-40%"
      score_3: "40-60%"
      score_2: "60-80%"
      score_1: "Bottom 20% (compraram há mais tempo)"

    frequency:
      score_5: "Top 20% (maior frequência)"
      score_4: "20-40%"
      score_3: "40-60%"
      score_2: "60-80%"
      score_1: "Bottom 20% (menor frequência)"

    monetary:
      score_5: "Top 20% (maior gasto)"
      score_4: "20-40%"
      score_3: "40-60%"
      score_2: "60-80%"
      score_1: "Bottom 20% (menor gasto)"

  result: "Cada cliente tem RFM score de 111 a 555"
```

### SQL: Quintile Scoring

```sql
-- =============================================================================
-- RFM QUINTILE SCORING
-- =============================================================================

WITH raw_rfm AS (
    SELECT
        customer_id,
        DATE_DIFF('2026-01-23'::DATE, MAX(transaction_date)::DATE, DAY) AS recency_days,
        COUNT(*) AS frequency,
        SUM(amount) AS monetary_total
    FROM transactions
    WHERE transaction_date >= DATE_SUB('2026-01-23', INTERVAL 12 MONTH)
      AND amount > 0
    GROUP BY customer_id
),

rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_total,

        -- RECENCY SCORE (invertido: menor recency = maior score)
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,

        -- FREQUENCY SCORE
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,

        -- MONETARY SCORE
        NTILE(5) OVER (ORDER BY monetary_total ASC) AS m_score

    FROM raw_rfm
)

SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_total,
    r_score,
    f_score,
    m_score,

    -- RFM Score combinado (string)
    CONCAT(r_score, f_score, m_score) AS rfm_score,

    -- RFM Score numérico (para ordenação)
    (r_score * 100) + (f_score * 10) + m_score AS rfm_score_numeric,

    -- Score médio ponderado (opcional)
    ROUND((r_score * 0.4 + f_score * 0.4 + m_score * 0.2), 2) AS rfm_weighted_score

FROM rfm_scores
ORDER BY rfm_score_numeric DESC;
```

### Method 2B: Percentile Scoring (0-100)

Mais preciso, captura nuances dentro dos grupos.

```sql
-- =============================================================================
-- RFM PERCENTILE SCORING
-- =============================================================================

WITH raw_rfm AS (
    SELECT
        customer_id,
        DATE_DIFF('2026-01-23'::DATE, MAX(transaction_date)::DATE, DAY) AS recency_days,
        COUNT(*) AS frequency,
        SUM(amount) AS monetary_total
    FROM transactions
    WHERE transaction_date >= DATE_SUB('2026-01-23', INTERVAL 12 MONTH)
    GROUP BY customer_id
),

rfm_percentiles AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_total,

        -- RECENCY PERCENTILE (invertido)
        100 - PERCENT_RANK() OVER (ORDER BY recency_days ASC) * 100 AS r_percentile,

        -- FREQUENCY PERCENTILE
        PERCENT_RANK() OVER (ORDER BY frequency ASC) * 100 AS f_percentile,

        -- MONETARY PERCENTILE
        PERCENT_RANK() OVER (ORDER BY monetary_total ASC) * 100 AS m_percentile

    FROM raw_rfm
)

SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_total,
    ROUND(r_percentile, 1) AS r_percentile,
    ROUND(f_percentile, 1) AS f_percentile,
    ROUND(m_percentile, 1) AS m_percentile,

    -- Percentile médio
    ROUND((r_percentile + f_percentile + m_percentile) / 3, 1) AS rfm_avg_percentile,

    -- Converter para score 1-5 se necessário
    CASE
        WHEN r_percentile >= 80 THEN 5
        WHEN r_percentile >= 60 THEN 4
        WHEN r_percentile >= 40 THEN 3
        WHEN r_percentile >= 20 THEN 2
        ELSE 1
    END AS r_score
    -- ... repetir para F e M

FROM rfm_percentiles;
```

### Method 2C: Fixed Thresholds

Para consistência ao longo do tempo - os limites não mudam.

```yaml
fixed_thresholds_example:
  recency_days:
    score_5: "<= 7 dias"
    score_4: "8-30 dias"
    score_3: "31-60 dias"
    score_2: "61-90 dias"
    score_1: "> 90 dias"

  frequency:
    score_5: ">= 10 compras"
    score_4: "6-9 compras"
    score_3: "3-5 compras"
    score_2: "2 compras"
    score_1: "1 compra"

  monetary:
    score_5: ">= $1000"
    score_4: "$500-$999"
    score_3: "$200-$499"
    score_2: "$50-$199"
    score_1: "< $50"

  note: |
    Thresholds devem ser calibrados para SEU negócio.
    Revisar trimestralmente para ajustar se necessário.
```

```sql
-- =============================================================================
-- RFM FIXED THRESHOLD SCORING
-- =============================================================================

SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_total,

    -- RECENCY SCORE (fixed thresholds)
    CASE
        WHEN recency_days <= 7 THEN 5
        WHEN recency_days <= 30 THEN 4
        WHEN recency_days <= 60 THEN 3
        WHEN recency_days <= 90 THEN 2
        ELSE 1
    END AS r_score,

    -- FREQUENCY SCORE (fixed thresholds)
    CASE
        WHEN frequency >= 10 THEN 5
        WHEN frequency >= 6 THEN 4
        WHEN frequency >= 3 THEN 3
        WHEN frequency >= 2 THEN 2
        ELSE 1
    END AS f_score,

    -- MONETARY SCORE (fixed thresholds)
    CASE
        WHEN monetary_total >= 1000 THEN 5
        WHEN monetary_total >= 500 THEN 4
        WHEN monetary_total >= 200 THEN 3
        WHEN monetary_total >= 50 THEN 2
        ELSE 1
    END AS m_score

FROM raw_rfm;
```

---

## Phase 3: Segment Assignment

### 3.1: Standard 11-Segment Model

O modelo mais completo e utilizado, baseado em combinações de R e FM scores.

```yaml
segment_definitions:
  note: |
    Segmentos baseados principalmente em combinação de R (Recency) com
    F+M médio. A lógica: Recency é o preditor mais forte de comportamento
    futuro, F+M indica valor/engajamento.

segments:
  champions:
    rfm_criteria:
      r_score: [5]
      f_score: [4, 5]
      m_score: [4, 5]
    alternative: "R=5 AND (F+M)/2 >= 4"
    description: "Melhores clientes - compram frequentemente, gastam muito, compraram recentemente"
    typical_percentage: "~5-10%"
    characteristics:
      - "Highest CLV"
      - "Brand advocates"
      - "Low price sensitivity"
      - "High engagement"

  loyal_customers:
    rfm_criteria:
      r_score: [3, 4, 5]
      f_score: [4, 5]
      m_score: [3, 4, 5]
    alternative: "R>=3 AND F>=4"
    description: "Compram consistentemente com boa frequência"
    typical_percentage: "~10-15%"
    characteristics:
      - "Reliable repeat purchasers"
      - "Respond well to loyalty programs"
      - "May become Champions"

  potential_loyalists:
    rfm_criteria:
      r_score: [4, 5]
      f_score: [2, 3]
      m_score: [2, 3, 4]
    alternative: "R>=4 AND F in (2,3)"
    description: "Clientes recentes com frequência crescente - podem virar Loyal"
    typical_percentage: "~10-15%"
    characteristics:
      - "Recent purchasers"
      - "Building relationship"
      - "Responsive to engagement"

  new_customers:
    rfm_criteria:
      r_score: [5]
      f_score: [1]
      m_score: [1, 2, 3, 4, 5]
    alternative: "R=5 AND F=1"
    description: "Primeira compra recente - momento crítico de nurturing"
    typical_percentage: "~5-10%"
    characteristics:
      - "Just acquired"
      - "Unknown future value"
      - "Critical onboarding window"

  promising:
    rfm_criteria:
      r_score: [4]
      f_score: [1]
      m_score: [1, 2, 3]
    alternative: "R=4 AND F=1"
    description: "Compra recente única mas não tão recente quanto New"
    typical_percentage: "~5-10%"
    characteristics:
      - "Single purchase, relatively recent"
      - "Need second purchase push"

  need_attention:
    rfm_criteria:
      r_score: [3]
      f_score: [3]
      m_score: [3]
    alternative: "R=3 AND F=3 AND M=3"
    description: "Clientes medianos que podem ir para qualquer direção"
    typical_percentage: "~15-20%"
    characteristics:
      - "Average in all dimensions"
      - "Require targeted campaigns"
      - "Swing segment"

  about_to_sleep:
    rfm_criteria:
      r_score: [3]
      f_score: [1, 2]
      m_score: [1, 2, 3]
    alternative: "R=3 AND F<=2"
    description: "Frequência baixa e começando a ficar distante"
    typical_percentage: "~10-15%"
    characteristics:
      - "Slipping away"
      - "Need reactivation soon"
      - "Time-sensitive intervention"

  at_risk:
    rfm_criteria:
      r_score: [2]
      f_score: [3, 4, 5]
      m_score: [3, 4, 5]
    alternative: "R=2 AND F>=3"
    description: "Eram bons clientes (alta frequência) mas pararam de comprar"
    typical_percentage: "~10-15%"
    characteristics:
      - "Former high-value customers"
      - "Something went wrong"
      - "Worth investigating and recovering"

  cannot_lose:
    rfm_criteria:
      r_score: [1, 2]
      f_score: [5]
      m_score: [5]
    alternative: "(R<=2) AND F=5 AND M=5"
    description: "Top clientes históricos que pararam - prioridade máxima de recuperação"
    typical_percentage: "~2-5%"
    characteristics:
      - "Highest historical value"
      - "Now inactive"
      - "Top priority for win-back"

  hibernating:
    rfm_criteria:
      r_score: [2]
      f_score: [1, 2]
      m_score: [1, 2]
    alternative: "R=2 AND F<=2 AND M<=2"
    description: "Compraram pouco, há bastante tempo"
    typical_percentage: "~15-20%"
    characteristics:
      - "Low engagement historically"
      - "Dormant but not lost"
      - "Low-cost reactivation worth trying"

  lost:
    rfm_criteria:
      r_score: [1]
      f_score: [1, 2]
      m_score: [1, 2]
    alternative: "R=1 AND F<=2 AND M<=2"
    description: "Não compram há muito tempo, baixo valor histórico"
    typical_percentage: "~10-20%"
    characteristics:
      - "Long inactive"
      - "Low historical value"
      - "May not be worth recovery effort"
```

### SQL: Complete Segment Assignment

```sql
-- =============================================================================
-- COMPLETE RFM SEGMENTATION QUERY
-- =============================================================================

WITH raw_rfm AS (
    SELECT
        customer_id,
        DATE_DIFF('2026-01-23'::DATE, MAX(transaction_date)::DATE, DAY) AS recency_days,
        COUNT(*) AS frequency,
        SUM(amount) AS monetary_total,
        MIN(transaction_date) AS first_purchase,
        MAX(transaction_date) AS last_purchase
    FROM transactions
    WHERE transaction_date >= DATE_SUB('2026-01-23', INTERVAL 12 MONTH)
      AND amount > 0
    GROUP BY customer_id
),

rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_total,
        first_purchase,
        last_purchase,

        -- Quintile Scores
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_total ASC) AS m_score
    FROM raw_rfm
),

rfm_with_combined AS (
    SELECT
        *,
        CONCAT(r_score, f_score, m_score) AS rfm_cell,
        (f_score + m_score) / 2.0 AS fm_avg
    FROM rfm_scores
),

rfm_segmented AS (
    SELECT
        *,
        CASE
            -- Champions: R=5, F>=4, M>=4
            WHEN r_score = 5 AND f_score >= 4 AND m_score >= 4
                THEN 'Champions'

            -- Loyal Customers: R>=3, F>=4
            WHEN r_score >= 3 AND f_score >= 4
                THEN 'Loyal Customers'

            -- Potential Loyalists: R>=4, F in (2,3)
            WHEN r_score >= 4 AND f_score IN (2, 3)
                THEN 'Potential Loyalists'

            -- New Customers: R=5, F=1
            WHEN r_score = 5 AND f_score = 1
                THEN 'New Customers'

            -- Promising: R=4, F=1
            WHEN r_score = 4 AND f_score = 1
                THEN 'Promising'

            -- Cannot Lose: R<=2, F=5, M=5
            WHEN r_score <= 2 AND f_score = 5 AND m_score = 5
                THEN 'Cannot Lose'

            -- At Risk: R=2, F>=3
            WHEN r_score = 2 AND f_score >= 3
                THEN 'At Risk'

            -- About to Sleep: R=3, F<=2
            WHEN r_score = 3 AND f_score <= 2
                THEN 'About to Sleep'

            -- Need Attention: R=3, F=3
            WHEN r_score = 3 AND f_score = 3
                THEN 'Need Attention'

            -- Hibernating: R=2, F<=2
            WHEN r_score = 2 AND f_score <= 2
                THEN 'Hibernating'

            -- Lost: R=1
            WHEN r_score = 1
                THEN 'Lost'

            ELSE 'Other'
        END AS segment
    FROM rfm_with_combined
)

SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_total,
    first_purchase,
    last_purchase,
    r_score,
    f_score,
    m_score,
    rfm_cell,
    fm_avg,
    segment
FROM rfm_segmented
ORDER BY
    CASE segment
        WHEN 'Champions' THEN 1
        WHEN 'Loyal Customers' THEN 2
        WHEN 'Cannot Lose' THEN 3
        WHEN 'At Risk' THEN 4
        WHEN 'Potential Loyalists' THEN 5
        WHEN 'New Customers' THEN 6
        WHEN 'Promising' THEN 7
        WHEN 'Need Attention' THEN 8
        WHEN 'About to Sleep' THEN 9
        WHEN 'Hibernating' THEN 10
        WHEN 'Lost' THEN 11
        ELSE 12
    END,
    monetary_total DESC;
```

### SQL: Segment Summary Statistics

```sql
-- =============================================================================
-- SEGMENT SUMMARY REPORT
-- =============================================================================

WITH segmented_customers AS (
    -- (Use query anterior como CTE)
    ...
)

SELECT
    segment,

    -- Counts
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_customers,

    -- Monetary
    SUM(monetary_total) AS total_revenue,
    ROUND(SUM(monetary_total) * 100.0 / SUM(SUM(monetary_total)) OVER (), 2) AS pct_of_revenue,
    ROUND(AVG(monetary_total), 2) AS avg_revenue,
    ROUND(MEDIAN(monetary_total), 2) AS median_revenue,

    -- Frequency
    ROUND(AVG(frequency), 2) AS avg_frequency,

    -- Recency
    ROUND(AVG(recency_days), 0) AS avg_recency_days,

    -- RFM Scores
    ROUND(AVG(r_score), 2) AS avg_r_score,
    ROUND(AVG(f_score), 2) AS avg_f_score,
    ROUND(AVG(m_score), 2) AS avg_m_score

FROM segmented_customers
GROUP BY segment
ORDER BY
    CASE segment
        WHEN 'Champions' THEN 1
        WHEN 'Loyal Customers' THEN 2
        WHEN 'Cannot Lose' THEN 3
        WHEN 'At Risk' THEN 4
        WHEN 'Potential Loyalists' THEN 5
        WHEN 'New Customers' THEN 6
        WHEN 'Promising' THEN 7
        WHEN 'Need Attention' THEN 8
        WHEN 'About to Sleep' THEN 9
        WHEN 'Hibernating' THEN 10
        WHEN 'Lost' THEN 11
    END;
```

---

## Phase 4: Action Playbooks by Segment

### 4.1: Champions

```yaml
segment: Champions
priority: PROTECT
investment_level: PREMIUM

understanding:
  who_they_are: |
    Seus melhores clientes. Compram frequentemente, gastam muito,
    compraram recentemente. Eles AMAM sua marca.

  typical_behavior:
    - "Responde emails rapidamente"
    - "Compra novos produtos"
    - "Dá feedback positivo"
    - "Indica para amigos"

  risk_if_lost: |
    CATASTRÓFICO. Perder um Champion = perder múltiplos clientes
    regulares em valor. Além disso, eles são influenciadores.

goals:
  primary: "Manter engajamento e advocacia"
  secondary: "Extrair insights para melhorar produtos/serviços"
  avoid: "Não alienar com ofertas agressivas ou comunicação excessiva"

tactics:
  communication:
    frequency: "Personalizada, quando relevante"
    channels: ["Email pessoal", "WhatsApp direto", "Telefone"]
    tone: "VIP, exclusivo, grato"

  offers:
    - name: "Early Access"
      description: "Acesso antecipado a novos produtos"
      goal: "Fazer sentir especial, coletar feedback"

    - name: "VIP Events"
      description: "Eventos exclusivos (webinars, meetups)"
      goal: "Networking, community building"

    - name: "Co-Creation"
      description: "Envolver no desenvolvimento de produtos"
      goal: "Aumentar ownership, feedback valioso"

    - name: "Surprise & Delight"
      description: "Presentes inesperados, upgrades"
      goal: "Reforçar relação emocional"

  programs:
    - "Programa VIP/Top Tier de loyalty"
    - "Linha direta de suporte"
    - "Entrevistas para case studies"
    - "Referral program com benefícios premium"

  avoid:
    - "Descontos agressivos (desvaloriza a marca)"
    - "Comunicação genérica de massa"
    - "Pedir demais (surveys longos)"
    - "Mudar experiência que eles amam"

kpis_to_track:
  - "Retention rate deste segmento (meta: >95%)"
  - "NPS deste segmento (meta: >70)"
  - "Share of wallet"
  - "Referrals gerados"
  - "Qualquer sinal de queda em frequência (ALARME)"

alert_trigger: |
  SE um Champion não compra há 30+ dias (ou 2x o intervalo médio):
  → ALERTA IMEDIATO para equipe de CS
  → Outreach pessoal em 48h
```

### 4.2: Loyal Customers

```yaml
segment: Loyal Customers
priority: DEVELOP
investment_level: HIGH

understanding:
  who_they_are: |
    Clientes consistentes com boa frequência de compra.
    Podem não ser os maiores gastadores, mas são confiáveis.

  potential: "Podem se tornar Champions com o nurturing certo"

goals:
  primary: "Aumentar engajamento para elevar a Champions"
  secondary: "Aumentar ticket médio / cross-sell"

tactics:
  communication:
    frequency: "Regular mas não intrusiva"
    channels: ["Email segmentado", "App notifications"]
    tone: "Valor, reconhecimento de lealdade"

  offers:
    - name: "Loyalty Points Bonus"
      description: "Multiplicadores de pontos"
      goal: "Incentivar próxima compra"

    - name: "Bundle Offers"
      description: "Combos com desconto"
      goal: "Aumentar basket size"

    - name: "Category Expansion"
      description: "Introduzir categorias não compradas"
      goal: "Cross-sell, aumentar share of wallet"

    - name: "Tier Upgrade Path"
      description: "Mostrar benefícios do próximo tier"
      goal: "Motivar aumento de frequência"

kpis_to_track:
  - "Migration rate para Champions"
  - "AOV trend"
  - "Categories purchased"
  - "Response rate a campanhas"

alert_trigger: |
  SE frequência cair 2 períodos seguidos:
  → Entrar em campanha de reativação
```

### 4.3: Potential Loyalists

```yaml
segment: Potential Loyalists
priority: ACCELERATE
investment_level: MEDIUM-HIGH

understanding:
  who_they_are: |
    Clientes recentes que já mostraram interesse com 2-3 compras.
    Estão construindo o hábito. Momento crítico.

goals:
  primary: "Converter em Loyal antes que esfrie"
  secondary: "Entender o que os fez comprar repetidamente"

tactics:
  offers:
    - name: "Second Purchase Incentive"
      description: "Desconto na próxima compra com prazo"
      goal: "Acelerar formação de hábito"

    - name: "Onboarding Sequence"
      description: "Série de emails educativos"
      goal: "Aumentar value perception"

    - name: "Product Recommendations"
      description: "Baseado no que compraram"
      goal: "Cross-sell relevante"

kpis_to_track:
  - "Conversion rate para Loyal"
  - "Time to third purchase"
  - "Email engagement rate"
```

### 4.4: New Customers

```yaml
segment: New Customers
priority: ONBOARD
investment_level: HIGH (ROI future)

understanding:
  who_they_are: |
    Acabaram de fazer primeira compra. Momento mais crítico
    do ciclo de vida. A experiência agora define o futuro.

goals:
  primary: "Garantir excelente primeira experiência"
  secondary: "Gerar segunda compra rapidamente"

tactics:
  immediate_post_purchase:
    - "Email de agradecimento personalizado"
    - "Tracking transparente do pedido"
    - "Checkin pós-entrega"

  first_30_days:
    - name: "Welcome Sequence"
      description: "3-5 emails de onboarding"
      content: ["Brand story", "How to use", "Community invite", "Recommended products"]

    - name: "Second Purchase Discount"
      description: "10-15% off na segunda compra"
      timing: "14 dias após primeira compra"

    - name: "Feedback Request"
      description: "Survey curto sobre experiência"
      timing: "7 dias após receber produto"

kpis_to_track:
  - "Second purchase rate (meta: >30% em 60 dias)"
  - "Time to second purchase"
  - "First purchase NPS"
  - "Welcome email open rate"

critical_window: |
  30-60 dias. Se não comprar novamente neste período,
  probabilidade de virar Lost aumenta drasticamente.
```

### 4.5: Promising

```yaml
segment: Promising
priority: NURTURE
investment_level: MEDIUM

understanding:
  who_they_are: |
    Uma compra, relativamente recente (não tão recente quanto New).
    Precisam de um empurrãozinho para a segunda compra.

goals:
  primary: "Converter em Potential Loyalist"
  secondary: "Entender barreiras para segunda compra"

tactics:
  - "Reminder do valor da marca"
  - "Desconto com urgência (expira em X dias)"
  - "Produtos relacionados à primeira compra"
  - "Social proof (reviews, testimonials)"
```

### 4.6: Need Attention

```yaml
segment: Need Attention
priority: ENGAGE
investment_level: MEDIUM

understanding:
  who_they_are: |
    Clientes medianos em todas as métricas. Podem ir para
    qualquer direção - são o "swing vote" da sua base.

goals:
  primary: "Mover para cima (Loyal/Potential)"
  secondary: "Pelo menos não deixar cair"

tactics:
  - "Campanhas de reengajamento"
  - "Ofertas personalizadas baseadas em histórico"
  - "Survey para entender preferências"
  - "A/B test de abordagens"

approach: |
  Este segmento é bom para testar. Resultados aqui podem
  informar estratégias para outros segmentos.
```

### 4.7: About to Sleep

```yaml
segment: About to Sleep
priority: REACTIVATE (urgente)
investment_level: MEDIUM

understanding:
  who_they_are: |
    Frequência baixa e começando a ficar distante.
    Janela de oportunidade está fechando.

goals:
  primary: "Acordar antes que durma de vez"

tactics:
  urgency_based:
    - "Desconto significativo (15-25%) com prazo curto"
    - "'We miss you' campaign"
    - "Highlight novidades desde última compra"

  value_based:
    - "Relembrar benefícios não utilizados (pontos, créditos)"
    - "Conteúdo educativo sobre uso do produto"

timing: |
  CRITICAL: Intervenção deve acontecer AGORA.
  A cada dia, probabilidade de recuperação diminui.
```

### 4.8: At Risk

```yaml
segment: At Risk
priority: RECOVER (alta)
investment_level: HIGH

understanding:
  who_they_are: |
    Eram bons clientes (alta frequência passada) mas pararam
    de comprar. Algo aconteceu. Vale investigar.

goals:
  primary: "Descobrir o que deu errado e consertar"
  secondary: "Recuperar antes que vire Cannot Lose"

tactics:
  investigation:
    - "Pesquisa direta: Por que parou de comprar?"
    - "Análise de última interação (reclamação? problema?)"
    - "Comparar com comportamento anterior"

  recovery:
    - name: "Personal Outreach"
      description: "Contato direto (telefone/email pessoal)"
      goal: "Entender e resolver"

    - name: "Win-Back Offer"
      description: "Oferta agressiva + pedido de desculpas se aplicável"
      goal: "Dar razão para voltar"

    - name: "VIP Treatment"
      description: "Upgrade temporário, benefícios extras"
      goal: "Mostrar que são valorizados"

alert: |
  Prioridade alta. Estes clientes têm valor comprovado.
  Perder eles é perder investimento já feito.
```

### 4.9: Cannot Lose

```yaml
segment: Cannot Lose
priority: RECOVER (máxima)
investment_level: PREMIUM

understanding:
  who_they_are: |
    SEUS MELHORES CLIENTES HISTÓRICOS que pararam de comprar.
    Top 1% em valor que agora está inativo. EMERGÊNCIA.

goals:
  primary: "Recuperar A QUALQUER CUSTO razoável"

tactics:
  escalation:
    - "Escalar para gerência/founder se necessário"
    - "Contato pessoal de alto nível"
    - "Investigação profunda do que aconteceu"

  offers:
    - "Oferta irresistível personalizada"
    - "Restituição se houve problema"
    - "Tratamento VIP garantido"

  learning:
    - "Documentar razão da saída"
    - "Usar para prevenir com outros Champions"

investment_justification: |
  Se este cliente gerava $10k/ano e você gasta $500 para recuperar,
  ROI é >20x mesmo que retenha por apenas mais 1 ano.
```

### 4.10: Hibernating

```yaml
segment: Hibernating
priority: TEST
investment_level: LOW

understanding:
  who_they_are: |
    Baixo engajamento histórico, distantes mas não perdidos.
    Alguns podem acordar com o estímulo certo.

goals:
  primary: "Testar reativação com baixo custo"
  secondary: "Identificar 'diamonds in rough'"

tactics:
  low_cost_reactivation:
    - "Email automatizado de 'tempo sem ver você'"
    - "Cupom significativo (20-30%)"
    - "Novidades desde última visita"

  testing:
    - "A/B test de ofertas"
    - "Identificar subgrupo que responde"
    - "Mover responsivos para pipeline de nurturing"

budget_rule: |
  Não investir mais do que retorno esperado.
  Se taxa de reativação histórica é 5%, calcular ROI.
```

### 4.11: Lost

```yaml
segment: Lost
priority: MINIMAL
investment_level: VERY LOW

understanding:
  who_they_are: |
    Não compram há muito tempo, baixo valor histórico.
    Provavelmente nunca serão clientes valiosos.

goals:
  primary: "Não desperdiçar recursos"
  secondary: "Última tentativa automatizada de reativação"

tactics:
  automated_only:
    - "Único email de win-back (automatizado)"
    - "Não gastar budget de mídia"
    - "Não incluir em campanhas caras"

  cleanup:
    - "Considerar suprimir de listas após X tentativas"
    - "Manter dados para análise mas não marketing ativo"

philosophy: |
  "Alguns clientes simplesmente não são seus clientes ideais.
  Foco em quem você pode servir bem." - Peter Fader
```

---

## Phase 5: Implementation & Automation

### 5.1: Automation Workflow

```yaml
rfm_automation:
  frequency: "Semanal ou Quinzenal"

  pipeline:
    step_1_extract:
      description: "Extrair dados transacionais do período"
      source: "Data warehouse / CRM"
      output: "raw_transactions.csv"

    step_2_calculate:
      description: "Calcular métricas RFM"
      script: "calculate_rfm.py ou SQL job"
      output: "rfm_scores.csv"

    step_3_segment:
      description: "Atribuir segmentos"
      script: "segment_rfm.py ou SQL"
      output: "rfm_segments.csv"

    step_4_compare:
      description: "Comparar com semana anterior"
      purpose: "Identificar migrações de segmento"
      output: "segment_changes.csv"

    step_5_action:
      description: "Trigger ações por segmento"
      integrations:
        - "CRM: Atualizar campo de segmento"
        - "Email: Adicionar a jornadas automatizadas"
        - "Support: Sinalizar At Risk e Cannot Lose"
        - "Dashboard: Atualizar métricas"

    step_6_alert:
      description: "Alertas para casos críticos"
      triggers:
        - "Champion migrou para At Risk → ALERT"
        - "Cannot Lose identificado → URGENT ALERT"
        - "Grande mudança na distribuição de segmentos → REVIEW"
```

### 5.2: Python Implementation

```python
"""
Complete RFM Segmentation Pipeline
Based on Peter Fader methodology

Requirements:
pip install pandas numpy
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class RFMSegmenter:
    """
    RFM Segmentation following Fader methodology.
    """

    # Segment definitions
    SEGMENT_RULES = {
        'Champions': lambda r, f, m: r == 5 and f >= 4 and m >= 4,
        'Loyal Customers': lambda r, f, m: r >= 3 and f >= 4,
        'Potential Loyalists': lambda r, f, m: r >= 4 and f in [2, 3],
        'New Customers': lambda r, f, m: r == 5 and f == 1,
        'Promising': lambda r, f, m: r == 4 and f == 1,
        'Cannot Lose': lambda r, f, m: r <= 2 and f == 5 and m == 5,
        'At Risk': lambda r, f, m: r == 2 and f >= 3,
        'About to Sleep': lambda r, f, m: r == 3 and f <= 2,
        'Need Attention': lambda r, f, m: r == 3 and f == 3,
        'Hibernating': lambda r, f, m: r == 2 and f <= 2,
        'Lost': lambda r, f, m: r == 1,
    }

    # Segment priority for ordering
    SEGMENT_PRIORITY = {
        'Champions': 1,
        'Loyal Customers': 2,
        'Cannot Lose': 3,
        'At Risk': 4,
        'Potential Loyalists': 5,
        'New Customers': 6,
        'Promising': 7,
        'Need Attention': 8,
        'About to Sleep': 9,
        'Hibernating': 10,
        'Lost': 11,
        'Other': 12
    }

    def __init__(
        self,
        transactions_df: pd.DataFrame,
        customer_id_col: str = 'customer_id',
        date_col: str = 'transaction_date',
        amount_col: str = 'amount',
        reference_date: Optional[datetime] = None,
        analysis_period_months: int = 12
    ):
        """
        Initialize RFM Segmenter.

        Args:
            transactions_df: DataFrame with transaction data
            customer_id_col: Column name for customer ID
            date_col: Column name for transaction date
            amount_col: Column name for transaction amount
            reference_date: Reference date for recency (default: today)
            analysis_period_months: Months of data to analyze
        """
        self.df = transactions_df.copy()
        self.customer_id_col = customer_id_col
        self.date_col = date_col
        self.amount_col = amount_col
        self.reference_date = reference_date or datetime.now()
        self.analysis_period_months = analysis_period_months

        # Convert date column
        self.df[date_col] = pd.to_datetime(self.df[date_col])

        # Filter to analysis period
        cutoff_date = self.reference_date - timedelta(days=analysis_period_months * 30)
        self.df = self.df[
            (self.df[date_col] >= cutoff_date) &
            (self.df[date_col] <= self.reference_date)
        ]

        # Results
        self.rfm_table = None
        self.segment_summary = None

    def calculate_rfm(self) -> pd.DataFrame:
        """Calculate raw RFM metrics for each customer."""

        rfm = self.df.groupby(self.customer_id_col).agg({
            self.date_col: ['max', 'min'],
            self.amount_col: ['sum', 'mean', 'count']
        })

        # Flatten column names
        rfm.columns = [
            'last_purchase', 'first_purchase',
            'monetary_total', 'avg_order_value', 'frequency'
        ]
        rfm = rfm.reset_index()

        # Calculate recency in days
        rfm['recency_days'] = (
            self.reference_date - rfm['last_purchase']
        ).dt.days

        # Customer tenure
        rfm['tenure_days'] = (
            rfm['last_purchase'] - rfm['first_purchase']
        ).dt.days

        self.rfm_table = rfm
        return rfm

    def assign_scores(self, method: str = 'quintile') -> pd.DataFrame:
        """
        Assign RFM scores (1-5).

        Args:
            method: 'quintile' or 'percentile'
        """
        if self.rfm_table is None:
            self.calculate_rfm()

        df = self.rfm_table.copy()

        if method == 'quintile':
            # Recency: lower is better, so reverse the order
            df['r_score'] = pd.qcut(
                df['recency_days'].rank(method='first'),
                q=5,
                labels=[5, 4, 3, 2, 1]
            ).astype(int)

            # Frequency: higher is better
            df['f_score'] = pd.qcut(
                df['frequency'].rank(method='first'),
                q=5,
                labels=[1, 2, 3, 4, 5]
            ).astype(int)

            # Monetary: higher is better
            df['m_score'] = pd.qcut(
                df['monetary_total'].rank(method='first'),
                q=5,
                labels=[1, 2, 3, 4, 5]
            ).astype(int)

        # Create RFM cell string
        df['rfm_cell'] = (
            df['r_score'].astype(str) +
            df['f_score'].astype(str) +
            df['m_score'].astype(str)
        )

        # FM average for segmentation
        df['fm_avg'] = (df['f_score'] + df['m_score']) / 2

        self.rfm_table = df
        return df

    def assign_segments(self) -> pd.DataFrame:
        """Assign segment labels based on RFM scores."""

        if 'r_score' not in self.rfm_table.columns:
            self.assign_scores()

        df = self.rfm_table.copy()

        def get_segment(row):
            r, f, m = row['r_score'], row['f_score'], row['m_score']
            for segment, rule in self.SEGMENT_RULES.items():
                if rule(r, f, m):
                    return segment
            return 'Other'

        df['segment'] = df.apply(get_segment, axis=1)

        # Add segment priority for sorting
        df['segment_priority'] = df['segment'].map(self.SEGMENT_PRIORITY)

        self.rfm_table = df
        return df

    def get_segment_summary(self) -> pd.DataFrame:
        """Generate summary statistics by segment."""

        if 'segment' not in self.rfm_table.columns:
            self.assign_segments()

        summary = self.rfm_table.groupby('segment').agg({
            self.customer_id_col: 'count',
            'monetary_total': ['sum', 'mean', 'median'],
            'frequency': 'mean',
            'recency_days': 'mean',
            'r_score': 'mean',
            'f_score': 'mean',
            'm_score': 'mean'
        }).round(2)

        # Flatten columns
        summary.columns = [
            'customer_count',
            'total_revenue', 'avg_revenue', 'median_revenue',
            'avg_frequency', 'avg_recency_days',
            'avg_r_score', 'avg_f_score', 'avg_m_score'
        ]

        # Calculate percentages
        total_customers = summary['customer_count'].sum()
        total_revenue = summary['total_revenue'].sum()

        summary['pct_customers'] = (
            summary['customer_count'] / total_customers * 100
        ).round(2)
        summary['pct_revenue'] = (
            summary['total_revenue'] / total_revenue * 100
        ).round(2)

        # Sort by priority
        summary['priority'] = summary.index.map(self.SEGMENT_PRIORITY)
        summary = summary.sort_values('priority').drop('priority', axis=1)

        self.segment_summary = summary
        return summary

    def get_segment_transitions(
        self,
        previous_rfm: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Compare current segments with previous period.
        Identify customers who changed segments.
        """
        current = self.rfm_table[[self.customer_id_col, 'segment']].copy()
        current.columns = [self.customer_id_col, 'current_segment']

        previous = previous_rfm[[self.customer_id_col, 'segment']].copy()
        previous.columns = [self.customer_id_col, 'previous_segment']

        merged = current.merge(previous, on=self.customer_id_col, how='outer')
        merged['previous_segment'] = merged['previous_segment'].fillna('New')
        merged['current_segment'] = merged['current_segment'].fillna('Churned')

        # Identify changes
        merged['changed'] = merged['current_segment'] != merged['previous_segment']

        # Create transition matrix
        transition_matrix = pd.crosstab(
            merged['previous_segment'],
            merged['current_segment'],
            margins=True
        )

        return merged[merged['changed']], transition_matrix

    def get_actionable_lists(self) -> Dict[str, pd.DataFrame]:
        """
        Generate actionable customer lists by segment.
        Ready for export to CRM/email systems.
        """
        if 'segment' not in self.rfm_table.columns:
            self.assign_segments()

        lists = {}
        for segment in self.SEGMENT_RULES.keys():
            segment_df = self.rfm_table[
                self.rfm_table['segment'] == segment
            ].copy()

            # Sort by value within segment
            segment_df = segment_df.sort_values(
                'monetary_total', ascending=False
            )

            lists[segment] = segment_df

        return lists

    def export_results(
        self,
        output_path: str,
        format: str = 'csv'
    ) -> None:
        """Export RFM results to file."""

        if format == 'csv':
            self.rfm_table.to_csv(output_path, index=False)
        elif format == 'excel':
            with pd.ExcelWriter(output_path) as writer:
                self.rfm_table.to_excel(
                    writer, sheet_name='RFM_Details', index=False
                )
                if self.segment_summary is not None:
                    self.segment_summary.to_excel(
                        writer, sheet_name='Segment_Summary'
                    )

    def generate_report(self) -> Dict:
        """Generate comprehensive RFM report."""

        if self.segment_summary is None:
            self.get_segment_summary()

        report = {
            'analysis_date': self.reference_date.strftime('%Y-%m-%d'),
            'analysis_period_months': self.analysis_period_months,
            'total_customers': len(self.rfm_table),
            'total_revenue': self.rfm_table['monetary_total'].sum(),

            'segment_distribution': self.segment_summary[[
                'customer_count', 'pct_customers',
                'total_revenue', 'pct_revenue'
            ]].to_dict(),

            'key_metrics': {
                'champions_count': len(
                    self.rfm_table[self.rfm_table['segment'] == 'Champions']
                ),
                'at_risk_count': len(
                    self.rfm_table[self.rfm_table['segment'] == 'At Risk']
                ),
                'cannot_lose_count': len(
                    self.rfm_table[self.rfm_table['segment'] == 'Cannot Lose']
                ),
                'lost_count': len(
                    self.rfm_table[self.rfm_table['segment'] == 'Lost']
                )
            },

            'rfm_score_distribution': {
                'avg_r': self.rfm_table['r_score'].mean(),
                'avg_f': self.rfm_table['f_score'].mean(),
                'avg_m': self.rfm_table['m_score'].mean()
            }
        }

        return report


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    n_customers = 5000

    transactions = []
    for cid in range(n_customers):
        n_purchases = np.random.poisson(3) + 1
        for _ in range(n_purchases):
            transactions.append({
                'customer_id': f'C{cid:05d}',
                'transaction_date': pd.Timestamp('2025-01-01') +
                    pd.Timedelta(days=np.random.randint(0, 365)),
                'amount': np.random.lognormal(4, 0.8)
            })

    df = pd.DataFrame(transactions)

    # Initialize segmenter
    segmenter = RFMSegmenter(
        df,
        reference_date=datetime(2026, 1, 23),
        analysis_period_months=12
    )

    # Run segmentation
    segmenter.calculate_rfm()
    segmenter.assign_scores()
    segmenter.assign_segments()
    summary = segmenter.get_segment_summary()

    # Print results
    print("=" * 60)
    print("RFM SEGMENTATION REPORT")
    print("=" * 60)
    print(f"\nAnalysis Date: 2026-01-23")
    print(f"Total Customers: {len(segmenter.rfm_table):,}")
    print(f"Total Revenue: ${segmenter.rfm_table['monetary_total'].sum():,.2f}")
    print("\nSegment Distribution:")
    print("-" * 60)
    print(summary[['customer_count', 'pct_customers', 'pct_revenue', 'avg_revenue']])

    # Get actionable lists
    lists = segmenter.get_actionable_lists()
    print(f"\n\nChampions ({len(lists['Champions'])} customers):")
    print(lists['Champions'].head())

    print(f"\n\nAt Risk ({len(lists['At Risk'])} customers):")
    print(lists['At Risk'].head())
```

---

## Phase 6: Visualization & Reporting

### 6.1: Recommended Visualizations

```yaml
visualizations:
  segment_distribution_pie:
    title: "Customer Distribution by Segment"
    type: "Pie chart or Treemap"
    insight: "Proporção de clientes em cada segmento"

  revenue_concentration:
    title: "Revenue by Segment"
    type: "Bar chart"
    insight: "Champions são X% dos clientes mas Y% da receita"

  rfm_heatmap:
    title: "RFM Score Matrix"
    type: "Heatmap (R vs F, colorido por count)"
    insight: "Onde estão concentrados os clientes"

  recency_distribution:
    title: "Recency Distribution"
    type: "Histogram"
    insight: "Quantos clientes estão ativos vs dormentes"

  segment_migration:
    title: "Segment Migration Over Time"
    type: "Sankey diagram ou flow chart"
    insight: "Como clientes movem entre segmentos"

  pareto_curve:
    title: "Customer Value Concentration"
    type: "Lorenz curve"
    insight: "Confirmar regra 80/20"
```

### 6.2: Dashboard Template

```yaml
rfm_dashboard:
  section_1_overview:
    title: "RFM Overview"
    cards:
      - "Total Customers: {N}"
      - "Total Revenue: ${X}"
      - "Champions: {N} ({X}%)"
      - "At Risk: {N} ({X}%)"

    main_visual: "Segment distribution pie/treemap"

  section_2_segments:
    title: "Segment Deep Dive"
    filter: "Segment selector"

    metrics_per_segment:
      - "Customer count"
      - "Total revenue"
      - "Avg order value"
      - "Avg frequency"
      - "Avg recency"

    customer_list: "Table with top customers of selected segment"

  section_3_trends:
    title: "Trends & Alerts"

    alerts:
      - "Champions → At Risk migrations (RED)"
      - "New Cannot Lose customers (RED)"
      - "At Risk recovery rate (AMBER)"

    charts:
      - "Segment distribution over time (stacked area)"
      - "Migration flow (Sankey)"

  section_4_actions:
    title: "Recommended Actions"

    priority_queue:
      - "Cannot Lose customers for immediate outreach"
      - "At Risk customers for campaign"
      - "Champions with declining frequency"
```

---

## Elicitation Questions

```yaml
discovery_questions:
  business_context:
    - "Qual é o seu modelo de negócio? (e-commerce, SaaS, varejo, etc.)"
    - "Qual é a frequência típica de compra? (diária, mensal, trimestral)"
    - "Você tem sazonalidade significativa?"
    - "Quanto tempo você tem de dados históricos?"

  current_state:
    - "Você já faz algum tipo de segmentação hoje?"
    - "Como você atualmente identifica clientes em risco?"
    - "Existe um programa de loyalty ou VIP?"
    - "Quais canais você usa para comunicação com clientes?"

  goals:
    - "O objetivo principal é retenção, aquisição, ou ambos?"
    - "Você quer segmentação para marketing automation?"
    - "Existe budget diferenciado por tipo de cliente?"
    - "Quem vai usar os resultados? (Marketing, CS, Vendas, Produto)"

  technical:
    - "Onde estão os dados transacionais?"
    - "Qual ferramenta de BI/analytics você usa?"
    - "É possível criar views/tables no warehouse?"
    - "Tem integração com CRM/email marketing?"
```

---

## Common Pitfalls

```yaml
pitfalls:
  pitfall_1_static_analysis:
    problem: "Rodar RFM uma vez e nunca atualizar"
    solution: "Automatizar refresh semanal/quinzenal"

  pitfall_2_ignoring_context:
    problem: "Usar mesmos thresholds para negócios diferentes"
    solution: "Calibrar para frequência natural do seu negócio"

  pitfall_3_over_segmenting:
    problem: "Criar 20+ segmentos sem capacity para agir"
    solution: "Começar com 4-8 segmentos, evoluir gradualmente"

  pitfall_4_treating_rfm_as_clv:
    problem: "RFM é comportamento passado, não valor futuro"
    solution: "Usar RFM como input para CLV, não substituto"

  pitfall_5_ignoring_new_customers:
    problem: "New Customers sempre terão F=1, M baixo"
    solution: "Segmento separado com métricas de onboarding"

  pitfall_6_recency_definition:
    problem: "Usar recency diferente do Fader (BG/NBD style)"
    solution: "Para RFM tradicional: days since last purchase"

  pitfall_7_no_action:
    problem: "Segmentar mas não fazer nada com os segmentos"
    solution: "Cada segmento deve ter playbook de ação definido"
```

---

## Quick Reference

```yaml
rfm_quick_reference:
  segment_summary:
    Champions:
      r: "5"
      f: "4-5"
      action: "PROTECT - VIP treatment"

    Loyal:
      r: "3-5"
      f: "4-5"
      action: "DEVELOP - Upsell, nurture"

    Potential_Loyalists:
      r: "4-5"
      f: "2-3"
      action: "ACCELERATE - Convert to loyal"

    New:
      r: "5"
      f: "1"
      action: "ONBOARD - Great first experience"

    At_Risk:
      r: "2"
      f: "3-5"
      action: "RECOVER - Urgent outreach"

    Cannot_Lose:
      r: "1-2"
      f: "5"
      m: "5"
      action: "RECOVER MAX - Whatever it takes"

    Lost:
      r: "1"
      f: "1-2"
      action: "MINIMAL - Automated only"

  formulas:
    recency: "reference_date - MAX(transaction_date)"
    frequency: "COUNT(transactions)"
    monetary: "SUM(amount)"
    rfm_cell: "CONCAT(r_score, f_score, m_score)"
```

---

## References

```yaml
references:
  primary_sources:
    - title: "Customer Centricity"
      author: "Peter Fader"
      year: 2012
      relevance: "Filosofia por trás de tratar clientes diferentemente"

    - title: "The Customer Centricity Playbook"
      authors: "Fader, Toms"
      year: 2018
      relevance: "Implementação prática de segmentação por valor"

  academic_papers:
    - title: "RFM and CLV: Using Iso-Value Curves for Customer Base Analysis"
      authors: "Fader, Hardie, Lee"
      year: 2005
      relevance: "Conexão matemática entre RFM e CLV"

  online_resources:
    - "brucehardie.com - RFM tutorials"
    - "Wharton Customer Analytics Initiative"
    - "Segment documentation (Personas)"
```

---

## Acceptance Criteria

- [ ] O período de análise, a data de referência e o método de scoring foram definidos antes da segmentação.
- [ ] Regras de tratamento para duplicatas, refunds e mistura de bases foram documentadas.
- [ ] Cada segmento RFM possui lógica de classificação e recomendação de ação correspondente.
- [ ] O output final inclui distribuição por segmento e instruções para operacionalização.

*Task Version: 1.0*
*Primary Agent: Peter Fader*
*Supporting Agents: Nick Mehta (Health Score integration), Avinash Kaushik (Visualization)*
*Lines: 1900+*
*Research Base: Fader methodology, RFM best practices, segment-specific playbooks*

---

*End of Task: segment-rfm.md*
