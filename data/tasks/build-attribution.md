# Build Attribution Model Task

## Purpose

Construir modelos de attribution marketing completos para entender como diferentes canais e touchpoints contribuem para conversões. Este task guia a implementação de múltiplos modelos de attribution (first-touch, last-touch, linear, time-decay, position-based e data-driven), mapeamento de canais, definição de janelas de conversão e metodologia multi-touch attribution (MTA).

## Workspace Output Contract

- Preflight: `*workspace-preflight` + `*workspace-context {slug}`
- Output canônico (template-first): `workspace/businesses/{slug}/analytics/attribution-report.yaml`
- Output canônico adicional: `workspace/businesses/{slug}/analytics/dmmm.yaml`
- Output custom (ad-hoc): `docs/data/{slug}/attribution-analysis-{date}.md`
- Regra: escrita canônica só se existir template correspondente em `workspace/_templates/analytics/`

---

## Primary Agent

**Avinash Kaushik** - Digital Analytics Evangelist, ex-Google

> "A maioria das empresas está data-rich e insight-poor. Não faltam dados, faltam decisões."

Kaushik argumenta que attribution existe para gerar AÇÃO, não relatórios. Se um modelo de attribution não muda uma decisão de budget, é ruído.

---

## Tier 0: Diagnostic Questions

Antes de construir qualquer modelo de attribution, responda estas perguntas diagnósticas:

```yaml
tier_0_diagnosis:

  business_context:
    - Qual é o objetivo principal? (awareness, leads, vendas, retention)
    - Qual é o ticket médio do produto/serviço?
    - Qual é o ciclo de vendas típico? (dias, semanas, meses)
    - Qual é o volume de conversões mensal?

  channel_landscape:
    - Quais canais de marketing estão ativos?
    - Qual é o mix de investimento atual por canal?
    - Existem canais offline que precisam ser considerados?
    - Há dados de todos os canais em um único lugar?

  data_availability:
    - Existe tracking cross-device?
    - Os cookies first-party estão implementados?
    - Há integração CRM <-> Marketing?
    - Qual é a qualidade do UTM tagging?

  maturity_assessment:
    - Qual modelo está em uso hoje? (nenhum, last-click, etc.)
    - Há histórico de dados de pelo menos 6 meses?
    - A equipe tem capacidade de agir nos insights?
    - Existe buy-in executivo para mudar alocação de budget?
```

---

## Inputs

```yaml
required:
  - business_objective: "O objetivo de negócio principal"
  - conversion_event: "Definição exata do que é uma conversão"
  - channels_list: "Lista de todos os canais de marketing ativos"
  - historical_data: "Período de dados disponível (mínimo 3 meses)"
  - budget_by_channel: "Investimento atual por canal"

optional:
  - customer_journey_data: "Dados de jornada do cliente se disponíveis"
  - crm_integration: "Se há integração com CRM"
  - offline_touchpoints: "Canais offline a considerar"
  - existing_attribution: "Modelo atual em uso"
  - conversion_window: "Janela de conversão desejada (padrão: 30 dias)"
  - cross_device_capability: "Se há tracking cross-device"
  - seasonality_factors: "Fatores sazonais do negócio"
```

---

## Why Attribution Matters

### The Attribution Problem

```yaml
attribution_problem:

  reality:
    - "Cliente vê ad no Instagram"
    - "Pesquisa no Google"
    - "Lê review em blog"
    - "Recebe email promocional"
    - "Converte via link do email"

  last_click_view: "Email recebe 100% do crédito"
  first_click_view: "Instagram recebe 100% do crédito"
  truth: "Todos contribuíram - mas em que proporção?"

business_impact:
  wrong_attribution:
    - "Cortar budget de canais que iniciam jornadas"
    - "Over-invest em canais que só fecham"
    - "Ignorar touchpoints de nurturing"
    - "Decisões baseadas em dados incompletos"

  correct_attribution:
    - "Entender papel de cada canal no funnel"
    - "Otimizar investimento por estágio da jornada"
    - "Identificar sinergias entre canais"
    - "ROI real por canal"
```

### Kaushik's Attribution Philosophy

> "Use first-touch para otimizar awareness. Use last-touch para otimizar conversão. Compare os dois para encontrar oportunidades."

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  FIRST-TOUCH:  "O que traz pessoas?"                           │
│  LAST-TOUCH:   "O que fecha vendas?"                           │
│  COMPARAÇÃO:   "Onde estão as oportunidades?"                  │
│                                                                 │
│  Gap entre first e last = canais subvalorizados                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Attribution Models Overview

### Model Comparison Matrix

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     ATTRIBUTION MODELS COMPARISON                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  MODELO          │ DISTRIBUIÇÃO     │ COMPLEXIDADE │ MELHOR PARA            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  First-Touch     │ 100% primeiro    │ Baixa        │ Awareness, top funnel  │
│  Last-Touch      │ 100% último      │ Baixa        │ Conversão, bottom      │
│  Linear          │ Igual para todos │ Baixa        │ Jornadas longas        │
│  Time-Decay      │ Mais p/ recentes │ Média        │ Ciclos de venda curtos │
│  Position-Based  │ 40/20/40         │ Média        │ Balance geral          │
│  Data-Driven     │ Algorítmico      │ Alta         │ Alto volume de dados   │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

### Visual: Credit Distribution by Model

```
Jornada: [Paid Search] → [Display] → [Social] → [Email] → [Conversão]

FIRST-TOUCH:
  Paid Search: ████████████████████ 100%
  Display:
  Social:
  Email:

LAST-TOUCH:
  Paid Search:
  Display:
  Social:
  Email:       ████████████████████ 100%

LINEAR:
  Paid Search: █████ 25%
  Display:     █████ 25%
  Social:      █████ 25%
  Email:       █████ 25%

TIME-DECAY (7 dias):
  Paid Search: ██ 10%
  Display:     ███ 15%
  Social:      █████ 25%
  Email:       ██████████ 50%

POSITION-BASED:
  Paid Search: ████████ 40%
  Display:     ██ 10%
  Social:      ██ 10%
  Email:       ████████ 40%
```

---

## Model 1: First-Touch Attribution

### Definition

O primeiro touchpoint recebe 100% do crédito pela conversão.

### When to Use

```yaml
first_touch_use_cases:

  ideal_for:
    - "Medir eficácia de canais de awareness"
    - "Entender o que traz novos visitantes"
    - "Avaliar canais de topo de funil"
    - "Campanhas de brand awareness"

  not_ideal_for:
    - "Medir eficácia de fechamento"
    - "Otimizar conversões diretas"
    - "Jornadas curtas (1-2 touchpoints)"

  questions_it_answers:
    - "Qual canal traz mais pessoas?"
    - "Onde devemos investir para awareness?"
    - "Quais canais iniciam jornadas de sucesso?"
```

### Implementation

```sql
-- First-Touch Attribution Query
WITH first_touch AS (
  SELECT
    user_id,
    conversion_id,
    MIN(touchpoint_timestamp) as first_touch_time
  FROM touchpoints
  WHERE touchpoint_timestamp <= conversion_timestamp
    AND touchpoint_timestamp >= conversion_timestamp - INTERVAL '30 days'
  GROUP BY user_id, conversion_id
)
SELECT
  t.channel,
  t.source,
  t.medium,
  COUNT(DISTINCT ft.conversion_id) as attributed_conversions,
  SUM(c.revenue) as attributed_revenue
FROM first_touch ft
JOIN touchpoints t ON ft.user_id = t.user_id
  AND ft.first_touch_time = t.touchpoint_timestamp
JOIN conversions c ON ft.conversion_id = c.conversion_id
GROUP BY t.channel, t.source, t.medium
ORDER BY attributed_conversions DESC;
```

### Report Template

```yaml
first_touch_report:

  header:
    title: "First-Touch Attribution Report"
    period: "[DATA INICIO] - [DATA FIM]"
    total_conversions: "[TOTAL]"

  metrics_by_channel:
    columns:
      - channel
      - first_touch_conversions
      - percentage_of_total
      - attributed_revenue
      - cpa_first_touch
      - roas_first_touch

  insights_section:
    - "Top 3 canais que iniciam jornadas"
    - "Canais subvalorizados vs last-touch"
    - "Recomendações de budget para awareness"
```

---

## Model 2: Last-Touch Attribution

### Definition

O último touchpoint antes da conversão recebe 100% do crédito.

### When to Use

```yaml
last_touch_use_cases:

  ideal_for:
    - "Medir eficácia de fechamento"
    - "Otimizar canais de conversão direta"
    - "Avaliar campanhas de retargeting"
    - "ROI de canais de resposta direta"

  not_ideal_for:
    - "Entender jornadas complexas"
    - "Avaliar canais de awareness"
    - "Negócios com ciclo de venda longo"

  questions_it_answers:
    - "Qual canal fecha mais vendas?"
    - "Onde devemos investir para conversão?"
    - "Qual é o ROI direto por canal?"
```

### Implementation

```sql
-- Last-Touch Attribution Query
WITH last_touch AS (
  SELECT
    user_id,
    conversion_id,
    MAX(touchpoint_timestamp) as last_touch_time
  FROM touchpoints
  WHERE touchpoint_timestamp <= conversion_timestamp
    AND touchpoint_timestamp >= conversion_timestamp - INTERVAL '30 days'
  GROUP BY user_id, conversion_id
)
SELECT
  t.channel,
  t.source,
  t.medium,
  COUNT(DISTINCT lt.conversion_id) as attributed_conversions,
  SUM(c.revenue) as attributed_revenue,
  SUM(c.revenue) / NULLIF(SUM(spend.cost), 0) as roas
FROM last_touch lt
JOIN touchpoints t ON lt.user_id = t.user_id
  AND lt.last_touch_time = t.touchpoint_timestamp
JOIN conversions c ON lt.conversion_id = c.conversion_id
LEFT JOIN channel_spend spend ON t.channel = spend.channel
GROUP BY t.channel, t.source, t.medium
ORDER BY attributed_conversions DESC;
```

### First vs Last Touch Comparison

```sql
-- Compare First vs Last Touch
WITH first_last AS (
  SELECT
    user_id,
    conversion_id,
    MIN(touchpoint_timestamp) as first_touch,
    MAX(touchpoint_timestamp) as last_touch
  FROM touchpoints
  WHERE touchpoint_timestamp <= conversion_timestamp
  GROUP BY user_id, conversion_id
)
SELECT
  ft.channel as first_touch_channel,
  lt.channel as last_touch_channel,
  COUNT(*) as conversions,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM first_last fl
JOIN touchpoints ft ON fl.first_touch = ft.touchpoint_timestamp AND fl.user_id = ft.user_id
JOIN touchpoints lt ON fl.last_touch = lt.touchpoint_timestamp AND fl.user_id = lt.user_id
GROUP BY ft.channel, lt.channel
ORDER BY conversions DESC;
```

---

## Model 3: Linear Attribution

### Definition

Todos os touchpoints na jornada recebem crédito igual.

### When to Use

```yaml
linear_use_cases:

  ideal_for:
    - "Jornadas longas e complexas"
    - "Quando todos os touchpoints importam igualmente"
    - "B2B com múltiplos stakeholders"
    - "Produtos de consideração alta"

  not_ideal_for:
    - "Jornadas curtas"
    - "Quando há touchpoints claramente mais importantes"
    - "Negócios de impulso"

  questions_it_answers:
    - "Qual é a contribuição média de cada canal?"
    - "Quais canais aparecem mais frequentemente?"
    - "Como distribuir budget igualmente?"
```

### Implementation

```sql
-- Linear Attribution Query
WITH touchpoint_counts AS (
  SELECT
    user_id,
    conversion_id,
    COUNT(*) as total_touchpoints
  FROM touchpoints
  WHERE touchpoint_timestamp <= conversion_timestamp
    AND touchpoint_timestamp >= conversion_timestamp - INTERVAL '30 days'
  GROUP BY user_id, conversion_id
)
SELECT
  t.channel,
  t.source,
  COUNT(*) as total_touchpoints,
  SUM(1.0 / tc.total_touchpoints) as attributed_conversions,
  SUM(c.revenue / tc.total_touchpoints) as attributed_revenue
FROM touchpoints t
JOIN touchpoint_counts tc ON t.user_id = tc.user_id
  AND t.conversion_id = tc.conversion_id
JOIN conversions c ON tc.conversion_id = c.conversion_id
WHERE t.touchpoint_timestamp <= c.conversion_timestamp
GROUP BY t.channel, t.source
ORDER BY attributed_conversions DESC;
```

### Linear Attribution Formula

```
Credit por Touchpoint = 1 / N

Onde N = número total de touchpoints na jornada

Exemplo:
- Jornada com 4 touchpoints
- Cada touchpoint recebe 25% (1/4)
- Se conversão vale R$100, cada touchpoint recebe R$25
```

---

## Model 4: Time-Decay Attribution

### Definition

Touchpoints mais próximos da conversão recebem mais crédito, com decaimento exponencial.

### When to Use

```yaml
time_decay_use_cases:

  ideal_for:
    - "Ciclos de venda com prazo definido"
    - "Promoções e ofertas limitadas"
    - "Quando recência importa"
    - "E-commerce com decisão rápida"

  not_ideal_for:
    - "Ciclos de venda muito longos (6+ meses)"
    - "Quando touchpoints iniciais são cruciais"
    - "Brand building de longo prazo"

  questions_it_answers:
    - "Quais canais influenciam no momento da decisão?"
    - "Qual é o impacto da recência?"
    - "Como otimizar os últimos touchpoints?"
```

### Time-Decay Formula

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIME-DECAY FORMULA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Credit = 2^(-t/half_life)                                     │
│                                                                 │
│  Onde:                                                         │
│  - t = dias entre touchpoint e conversão                       │
│  - half_life = período de meia-vida (padrão: 7 dias)          │
│                                                                 │
│  Exemplo (half_life = 7 dias):                                 │
│  - Touchpoint no dia da conversão: 2^0 = 1.00 (100%)          │
│  - Touchpoint 7 dias antes: 2^-1 = 0.50 (50%)                 │
│  - Touchpoint 14 dias antes: 2^-2 = 0.25 (25%)                │
│  - Touchpoint 21 dias antes: 2^-3 = 0.125 (12.5%)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```sql
-- Time-Decay Attribution Query
WITH decay_weights AS (
  SELECT
    t.user_id,
    t.conversion_id,
    t.channel,
    t.touchpoint_timestamp,
    c.conversion_timestamp,
    -- Half-life de 7 dias
    POWER(2, -1.0 * EXTRACT(DAY FROM (c.conversion_timestamp - t.touchpoint_timestamp)) / 7) as weight
  FROM touchpoints t
  JOIN conversions c ON t.user_id = c.user_id
  WHERE t.touchpoint_timestamp <= c.conversion_timestamp
    AND t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '30 days'
),
normalized_weights AS (
  SELECT
    *,
    weight / SUM(weight) OVER (PARTITION BY conversion_id) as normalized_weight
  FROM decay_weights
)
SELECT
  channel,
  COUNT(DISTINCT conversion_id) as conversions_touched,
  SUM(normalized_weight) as attributed_conversions,
  AVG(normalized_weight) as avg_attribution_per_conversion
FROM normalized_weights
GROUP BY channel
ORDER BY attributed_conversions DESC;
```

### Half-Life Recommendations

```yaml
half_life_recommendations:

  7_days:
    use_for: "E-commerce, impulse purchases"
    rationale: "Decisão rápida, recência muito importante"

  14_days:
    use_for: "SaaS trials, mid-ticket products"
    rationale: "Período de consideração moderado"

  30_days:
    use_for: "B2B, high-ticket products"
    rationale: "Ciclo de venda mais longo"

  custom:
    formula: "Analise tempo médio entre primeiro touchpoint e conversão"
    recommendation: "Half-life = tempo médio / 2"
```

---

## Model 5: Position-Based (U-Shaped) Attribution

### Definition

40% para primeiro touchpoint, 40% para último, 20% distribuído entre os do meio.

### When to Use

```yaml
position_based_use_cases:

  ideal_for:
    - "Valorizar tanto discovery quanto closing"
    - "Balance entre awareness e conversão"
    - "Jornadas com 3+ touchpoints"
    - "Quando início e fim são claramente importantes"

  not_ideal_for:
    - "Jornadas muito curtas (1-2 touchpoints)"
    - "Quando touchpoints do meio são cruciais"
    - "Nurturing intensivo"

  questions_it_answers:
    - "Quais canais trazem E convertem?"
    - "Qual é o valor combinado de cada canal?"
    - "Como balancear budget entre awareness e conversão?"
```

### Position-Based Formula

```
┌─────────────────────────────────────────────────────────────────┐
│                 POSITION-BASED (40/20/40)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PRIMEIRO TOUCHPOINT:  40% do crédito                          │
│  ÚLTIMO TOUCHPOINT:    40% do crédito                          │
│  TOUCHPOINTS DO MEIO:  20% dividido igualmente                 │
│                                                                 │
│  Exemplo: 5 touchpoints                                        │
│                                                                 │
│  [1]────[2]────[3]────[4]────[5]                              │
│   40%    6.67%  6.67%  6.67%  40%                              │
│                                                                 │
│  Se apenas 2 touchpoints:                                      │
│  [1]────[2]                                                    │
│   50%    50%                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```sql
-- Position-Based Attribution Query
WITH ordered_touchpoints AS (
  SELECT
    t.*,
    ROW_NUMBER() OVER (PARTITION BY t.conversion_id ORDER BY t.touchpoint_timestamp) as position,
    COUNT(*) OVER (PARTITION BY t.conversion_id) as total_touchpoints
  FROM touchpoints t
  JOIN conversions c ON t.user_id = c.user_id
  WHERE t.touchpoint_timestamp <= c.conversion_timestamp
    AND t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '30 days'
),
weighted_touchpoints AS (
  SELECT
    *,
    CASE
      WHEN total_touchpoints = 1 THEN 1.0
      WHEN total_touchpoints = 2 THEN 0.5
      WHEN position = 1 THEN 0.4
      WHEN position = total_touchpoints THEN 0.4
      ELSE 0.2 / (total_touchpoints - 2)
    END as weight
  FROM ordered_touchpoints
)
SELECT
  channel,
  SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) as first_touch_count,
  SUM(CASE WHEN position = total_touchpoints THEN 1 ELSE 0 END) as last_touch_count,
  SUM(weight) as attributed_conversions,
  AVG(weight) as avg_weight
FROM weighted_touchpoints
GROUP BY channel
ORDER BY attributed_conversions DESC;
```

### Variations

```yaml
position_based_variations:

  standard_u_shaped:
    first: 40%
    last: 40%
    middle: 20%
    best_for: "Balance geral"

  w_shaped:
    first: 30%
    lead_creation: 30%
    last: 30%
    other: 10%
    best_for: "B2B com lead qualification"

  z_shaped:
    first: 22.5%
    lead_creation: 22.5%
    opportunity_creation: 22.5%
    last: 22.5%
    other: 10%
    best_for: "B2B enterprise com múltiplos estágios"

  custom:
    description: "Ajustar pesos baseado em análise de jornadas"
    recommendation: "Testar diferentes distribuições"
```

---

## Model 6: Data-Driven Attribution

### Definition

Modelo algorítmico que calcula a contribuição de cada touchpoint baseado em dados históricos e probabilidades.

### When to Use

```yaml
data_driven_use_cases:

  ideal_for:
    - "Alto volume de conversões (1000+/mês)"
    - "Dados históricos robustos (6+ meses)"
    - "Equipe com capacidade analítica"
    - "Budget significativo de marketing"

  not_ideal_for:
    - "Baixo volume de conversões"
    - "Dados incompletos ou inconsistentes"
    - "Necessidade de simplicidade"
    - "Mudanças frequentes no mix de canais"

  requirements:
    - "Mínimo 15.000 cliques por canal"
    - "Mínimo 600 conversões no período"
    - "Tracking consistente cross-channel"
```

### Methodology: Shapley Value

```
┌─────────────────────────────────────────────────────────────────┐
│                    SHAPLEY VALUE METHOD                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Origem: Teoria dos jogos (Lloyd Shapley, 1953)                │
│                                                                 │
│  Conceito:                                                      │
│  - Calcula a contribuição marginal de cada "jogador" (canal)   │
│  - Considera todas as combinações possíveis de canais          │
│  - Atribui crédito baseado em quanto cada canal adiciona       │
│                                                                 │
│  Fórmula Simplificada:                                         │
│  φᵢ = Σ [|S|!(n-|S|-1)!/n!] × [v(S∪{i}) - v(S)]               │
│                                                                 │
│  Onde:                                                          │
│  - φᵢ = valor Shapley do canal i                               │
│  - S = subconjunto de canais sem i                             │
│  - v(S) = taxa de conversão do subconjunto S                   │
│  - n = número total de canais                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Methodology: Markov Chain

```yaml
markov_chain_attribution:

  concept:
    description: |
      Modela a jornada do cliente como uma cadeia de Markov,
      onde cada estado (canal) tem probabilidades de transição
      para outros estados ou para conversão/abandono.

  process:
    step_1: "Mapear todas as jornadas como sequências de estados"
    step_2: "Calcular matriz de transição entre estados"
    step_3: "Calcular probabilidade de conversão com cada canal"
    step_4: "Calcular removal effect (o que acontece se remover o canal)"
    step_5: "Atribuir crédito baseado no removal effect"

  removal_effect:
    formula: |
      RE(i) = P(conversão com canal i) - P(conversão sem canal i)
    interpretation: |
      Quanto maior o removal effect, mais importante o canal
      para a probabilidade de conversão.
```

### Implementation Approach

```python
# Pseudo-código para Data-Driven Attribution
# Usando Markov Chain com Removal Effect

def calculate_markov_attribution(journeys):
    """
    journeys: lista de jornadas, cada uma sendo uma lista de canais
    Retorna: dicionário com atribuição por canal
    """

    # 1. Construir matriz de transição
    transition_matrix = build_transition_matrix(journeys)

    # 2. Calcular probabilidade base de conversão
    base_conversion_prob = calculate_conversion_probability(
        transition_matrix,
        all_channels
    )

    # 3. Para cada canal, calcular removal effect
    removal_effects = {}
    for channel in channels:
        # Remover canal da matriz
        modified_matrix = remove_channel(transition_matrix, channel)

        # Calcular nova probabilidade de conversão
        new_conversion_prob = calculate_conversion_probability(
            modified_matrix,
            channels_without(channel)
        )

        # Removal effect
        removal_effects[channel] = base_conversion_prob - new_conversion_prob

    # 4. Normalizar para somar 100%
    total_effect = sum(removal_effects.values())
    attribution = {
        channel: effect / total_effect
        for channel, effect in removal_effects.items()
    }

    return attribution
```

### Data Requirements

```yaml
data_driven_requirements:

  minimum_data:
    conversions: "600+ conversões no período de análise"
    clicks_per_channel: "15.000+ cliques por canal"
    time_period: "6+ meses de dados históricos"

  data_quality:
    - "UTM tagging consistente"
    - "User ID unificado cross-device"
    - "Timestamps precisos"
    - "Sem gaps de dados"

  recommended_tools:
    google: "Google Analytics 4 Data-Driven Attribution"
    custom: "Python (Markov Chain libraries)"
    enterprise: "Adobe Analytics, Salesforce"
```

---

## Channel Mapping

### Standard Channel Definitions

```yaml
channel_mapping:

  paid_search:
    definition: "Anúncios pagos em buscadores"
    sources: ["google", "bing", "yahoo"]
    mediums: ["cpc", "ppc", "paid_search"]
    utm_pattern: "utm_medium=cpc OR utm_medium=ppc"
    role: "Intent capture, bottom funnel"

  organic_search:
    definition: "Tráfego não-pago de buscadores"
    sources: ["google", "bing", "yahoo", "duckduckgo"]
    mediums: ["organic"]
    utm_pattern: "No UTM, referrer from search engine"
    role: "Brand awareness, mid-funnel"

  paid_social:
    definition: "Anúncios em redes sociais"
    sources: ["facebook", "instagram", "linkedin", "tiktok", "twitter"]
    mediums: ["paid_social", "cpc", "cpm"]
    utm_pattern: "utm_medium=paid_social"
    role: "Awareness, demand generation"

  organic_social:
    definition: "Tráfego não-pago de redes sociais"
    sources: ["facebook", "instagram", "linkedin", "tiktok", "twitter"]
    mediums: ["social", "organic_social"]
    utm_pattern: "No UTM, referrer from social"
    role: "Engagement, brand building"

  email:
    definition: "Campanhas de email marketing"
    sources: ["newsletter", "campaign", "automation"]
    mediums: ["email"]
    utm_pattern: "utm_medium=email"
    role: "Nurturing, retention, conversion"

  display:
    definition: "Banners e anúncios display"
    sources: ["google", "programmatic", "direct"]
    mediums: ["display", "banner", "cpm"]
    utm_pattern: "utm_medium=display"
    role: "Awareness, retargeting"

  affiliate:
    definition: "Tráfego de parceiros afiliados"
    sources: ["affiliate_name"]
    mediums: ["affiliate", "referral"]
    utm_pattern: "utm_medium=affiliate"
    role: "Acquisition, performance"

  referral:
    definition: "Links de outros sites"
    sources: ["[domain]"]
    mediums: ["referral"]
    utm_pattern: "No UTM, referrer from external site"
    role: "PR, partnerships"

  direct:
    definition: "Acesso direto sem referrer"
    sources: ["direct", "(direct)"]
    mediums: ["(none)", "direct"]
    utm_pattern: "No referrer, no UTM"
    role: "Brand recall, bookmarks"

  video:
    definition: "Anúncios em plataformas de vídeo"
    sources: ["youtube", "vimeo"]
    mediums: ["video", "pre-roll"]
    utm_pattern: "utm_medium=video"
    role: "Awareness, education"
```

### Channel Grouping SQL

```sql
-- Channel Grouping Logic
SELECT
  CASE
    -- Paid Search
    WHEN LOWER(utm_medium) IN ('cpc', 'ppc', 'paid_search')
      AND LOWER(utm_source) IN ('google', 'bing', 'yahoo')
    THEN 'Paid Search'

    -- Organic Search
    WHEN LOWER(utm_medium) = 'organic'
      OR (utm_medium IS NULL AND referrer LIKE '%google%' AND referrer NOT LIKE '%googleads%')
    THEN 'Organic Search'

    -- Paid Social
    WHEN LOWER(utm_medium) IN ('paid_social', 'paidsocial')
      OR (LOWER(utm_medium) IN ('cpc', 'cpm')
          AND LOWER(utm_source) IN ('facebook', 'instagram', 'linkedin', 'tiktok'))
    THEN 'Paid Social'

    -- Organic Social
    WHEN LOWER(utm_medium) IN ('social', 'organic_social')
      OR (utm_medium IS NULL
          AND referrer ~* '(facebook|instagram|linkedin|twitter|tiktok)')
    THEN 'Organic Social'

    -- Email
    WHEN LOWER(utm_medium) = 'email'
    THEN 'Email'

    -- Display
    WHEN LOWER(utm_medium) IN ('display', 'banner', 'cpm')
    THEN 'Display'

    -- Affiliate
    WHEN LOWER(utm_medium) = 'affiliate'
    THEN 'Affiliate'

    -- Referral
    WHEN LOWER(utm_medium) = 'referral'
      OR (utm_medium IS NULL AND referrer IS NOT NULL AND referrer != '')
    THEN 'Referral'

    -- Direct
    WHEN utm_medium IS NULL AND (referrer IS NULL OR referrer = '')
    THEN 'Direct'

    ELSE 'Other'
  END as channel_group,
  *
FROM touchpoints;
```

### Channel Role in Funnel

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHANNEL ROLE BY FUNNEL STAGE                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AWARENESS (SEE)                                               │
│  ├── Display Ads                                               │
│  ├── Video Ads                                                 │
│  ├── Paid Social (prospecting)                                 │
│  └── PR / Influencer                                           │
│                                                                 │
│  CONSIDERATION (THINK)                                         │
│  ├── Organic Search                                            │
│  ├── Content Marketing                                         │
│  ├── Email (nurturing)                                         │
│  └── Organic Social                                            │
│                                                                 │
│  DECISION (DO)                                                 │
│  ├── Paid Search (brand + non-brand)                           │
│  ├── Retargeting                                               │
│  ├── Email (promotional)                                       │
│  └── Affiliate                                                 │
│                                                                 │
│  LOYALTY (CARE)                                                │
│  ├── Email (retention)                                         │
│  ├── Direct (bookmarks)                                        │
│  └── Organic Social                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conversion Window Definition

### What is a Conversion Window?

O período de tempo antes de uma conversão em que touchpoints são considerados para atribuição.

### Window Selection Guidelines

```yaml
conversion_window_guidelines:

  factors_to_consider:
    - "Ciclo de venda típico"
    - "Valor do produto/serviço"
    - "Complexidade da decisão"
    - "Frequência de compra"

  recommendations_by_business:

    ecommerce_low_ticket:
      window: "7 dias"
      rationale: "Decisão rápida, impulso"

    ecommerce_high_ticket:
      window: "30 dias"
      rationale: "Período de consideração"

    saas_b2b:
      window: "60-90 dias"
      rationale: "Múltiplos stakeholders, avaliação"

    enterprise_sales:
      window: "180 dias"
      rationale: "Ciclo longo, múltiplas interações"

    subscription_services:
      window: "14-30 dias"
      rationale: "Trial period + decisão"
```

### Multi-Window Analysis

```sql
-- Compare Attribution Across Different Windows
WITH touchpoints_by_window AS (
  SELECT
    t.channel,
    c.conversion_id,
    CASE
      WHEN t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '7 days' THEN '7_days'
      WHEN t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '14 days' THEN '14_days'
      WHEN t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '30 days' THEN '30_days'
      WHEN t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '60 days' THEN '60_days'
      WHEN t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '90 days' THEN '90_days'
    END as window_period
  FROM touchpoints t
  JOIN conversions c ON t.user_id = c.user_id
  WHERE t.touchpoint_timestamp <= c.conversion_timestamp
)
SELECT
  channel,
  COUNT(DISTINCT CASE WHEN window_period = '7_days' THEN conversion_id END) as conv_7d,
  COUNT(DISTINCT CASE WHEN window_period = '14_days' THEN conversion_id END) as conv_14d,
  COUNT(DISTINCT CASE WHEN window_period = '30_days' THEN conversion_id END) as conv_30d,
  COUNT(DISTINCT CASE WHEN window_period = '60_days' THEN conversion_id END) as conv_60d,
  COUNT(DISTINCT CASE WHEN window_period = '90_days' THEN conversion_id END) as conv_90d
FROM touchpoints_by_window
GROUP BY channel
ORDER BY conv_30d DESC;
```

### Finding Optimal Window

```yaml
optimal_window_analysis:

  method_1_percentile:
    description: "Usar percentil 90 do tempo entre primeiro touchpoint e conversão"
    steps:
      - "Calcular tempo entre primeiro touchpoint e conversão para cada jornada"
      - "Encontrar percentil 90"
      - "Usar como janela de conversão"
    sql: |
      SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (
        ORDER BY EXTRACT(DAY FROM conversion_timestamp - first_touchpoint_timestamp)
      ) as p90_window
      FROM journey_summary;

  method_2_diminishing_returns:
    description: "Encontrar ponto onde adicionar mais dias não adiciona conversões significativas"
    steps:
      - "Calcular conversões por janela (7, 14, 30, 60, 90 dias)"
      - "Calcular incremento percentual"
      - "Parar quando incremento < 5%"
```

---

## Multi-Touch Attribution (MTA) Methodology

### MTA Implementation Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                MTA IMPLEMENTATION FRAMEWORK                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: DATA FOUNDATION (Semanas 1-2)                         │
│  ├── Audit de tracking atual                                   │
│  ├── Padronização de UTMs                                      │
│  ├── Unificação de user IDs                                    │
│  └── Criação de tabela de touchpoints                          │
│                                                                 │
│  FASE 2: MODEL SELECTION (Semanas 3-4)                         │
│  ├── Análise de jornadas existentes                            │
│  ├── Teste de múltiplos modelos                                │
│  ├── Comparação de resultados                                  │
│  └── Seleção do modelo primário                                │
│                                                                 │
│  FASE 3: IMPLEMENTATION (Semanas 5-6)                          │
│  ├── Queries de produção                                       │
│  ├── Dashboard de attribution                                  │
│  ├── Automação de reports                                      │
│  └── Documentação                                              │
│                                                                 │
│  FASE 4: OPTIMIZATION (Ongoing)                                │
│  ├── Revisão mensal de resultados                              │
│  ├── Ajustes de modelo se necessário                           │
│  ├── Correlação com budget decisions                           │
│  └── Refinamento contínuo                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Journey Reconstruction

```sql
-- Reconstruct Customer Journeys
WITH journeys AS (
  SELECT
    c.user_id,
    c.conversion_id,
    c.conversion_timestamp,
    c.revenue,
    STRING_AGG(
      t.channel || ' (' || t.touchpoint_timestamp::date || ')',
      ' -> '
      ORDER BY t.touchpoint_timestamp
    ) as journey_path,
    COUNT(t.touchpoint_id) as touchpoint_count,
    MIN(t.touchpoint_timestamp) as first_touch,
    MAX(t.touchpoint_timestamp) as last_touch,
    EXTRACT(DAY FROM c.conversion_timestamp - MIN(t.touchpoint_timestamp)) as journey_length_days
  FROM conversions c
  JOIN touchpoints t ON c.user_id = t.user_id
  WHERE t.touchpoint_timestamp <= c.conversion_timestamp
    AND t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '30 days'
  GROUP BY c.user_id, c.conversion_id, c.conversion_timestamp, c.revenue
)
SELECT
  journey_path,
  COUNT(*) as occurrence_count,
  AVG(revenue) as avg_revenue,
  AVG(touchpoint_count) as avg_touchpoints,
  AVG(journey_length_days) as avg_journey_days
FROM journeys
GROUP BY journey_path
ORDER BY occurrence_count DESC
LIMIT 50;
```

### Assisted vs Direct Conversions

```sql
-- Assisted vs Direct Conversions
WITH journey_stats AS (
  SELECT
    t.channel,
    c.conversion_id,
    CASE
      WHEN t.touchpoint_timestamp = (
        SELECT MAX(touchpoint_timestamp)
        FROM touchpoints
        WHERE user_id = t.user_id
          AND touchpoint_timestamp <= c.conversion_timestamp
      ) THEN 'last_touch'
      ELSE 'assisted'
    END as touch_type
  FROM touchpoints t
  JOIN conversions c ON t.user_id = c.user_id
  WHERE t.touchpoint_timestamp <= c.conversion_timestamp
    AND t.touchpoint_timestamp >= c.conversion_timestamp - INTERVAL '30 days'
)
SELECT
  channel,
  COUNT(DISTINCT CASE WHEN touch_type = 'last_touch' THEN conversion_id END) as direct_conversions,
  COUNT(DISTINCT CASE WHEN touch_type = 'assisted' THEN conversion_id END) as assisted_conversions,
  ROUND(
    COUNT(DISTINCT CASE WHEN touch_type = 'assisted' THEN conversion_id END)::numeric /
    NULLIF(COUNT(DISTINCT CASE WHEN touch_type = 'last_touch' THEN conversion_id END), 0),
    2
  ) as assist_to_direct_ratio
FROM journey_stats
GROUP BY channel
ORDER BY direct_conversions DESC;
```

---

## Reporting Recommendations

### Executive Dashboard

```yaml
executive_dashboard:

  headline_metrics:
    - total_conversions: "Total de conversões no período"
    - total_revenue: "Receita total atribuída"
    - avg_touchpoints: "Média de touchpoints por conversão"
    - avg_journey_days: "Dias médios até conversão"

  model_comparison_chart:
    type: "Stacked bar chart"
    x_axis: "Canais"
    y_axis: "Conversões atribuídas"
    series: ["First-Touch", "Last-Touch", "Position-Based"]
    insight: "Highlight canais com maior diferença entre modelos"

  channel_performance_table:
    columns:
      - channel
      - first_touch_conversions
      - last_touch_conversions
      - position_based_conversions
      - spend
      - cpa_by_model
      - roas_by_model

  journey_insights:
    - top_10_journeys: "Jornadas mais comuns"
    - avg_touchpoints_by_conversion_value: "Correlação touchpoints x valor"
    - channel_overlap: "Quais canais aparecem juntos"
```

### So What Framework for Attribution Reports

```yaml
attribution_so_what:

  section_1_so_what:
    question: "Por que isso importa?"
    template: |
      Attribution analysis reveals that [CHANNEL X] brings [Y%] of first touches
      but only [Z%] of last touches, indicating its role as an
      [awareness/nurturing] channel that's currently [undervalued/overvalued]
      by last-click attribution.

  section_2_what_changed:
    question: "O que mudou desde a última análise?"
    template: |
      Compared to [PREVIOUS PERIOD]:
      - [CHANNEL A] first-touch share increased by [X%]
      - [CHANNEL B] assist ratio decreased by [Y%]
      - Average journey length changed from [N] to [M] touchpoints

  section_3_why:
    question: "Por que mudou?"
    template: |
      Key factors:
      - [CAMPAIGN/CHANGE 1] launched in [DATE]
      - [BUDGET SHIFT] from [CHANNEL X] to [CHANNEL Y]
      - [SEASONAL FACTOR] affecting [BEHAVIOR]

  section_4_now_what:
    question: "O que vamos fazer?"
    template: |
      Recommendations:
      1. [INCREASE/DECREASE] [CHANNEL X] budget by [%] because [REASON]
      2. Test [STRATEGY] in [CHANNEL Y] to improve [METRIC]
      3. [ACTION 3]

      Expected impact: [PROJECTED CHANGE] in [METRIC]
```

### Model Selection Report

```yaml
model_selection_report:

  analysis_approach:
    step_1: "Run all models on same dataset"
    step_2: "Compare attribution distribution"
    step_3: "Identify major discrepancies"
    step_4: "Recommend based on business context"

  comparison_table:
    rows: "Channels"
    columns:
      - first_touch_pct
      - last_touch_pct
      - linear_pct
      - time_decay_pct
      - position_based_pct
      - variance: "Max - Min"

  recommendation_criteria:
    high_variance_channels:
      description: "Canais com alta variância entre modelos"
      action: "Investigar mais a fundo, pode ser over/under valued"

    consistent_channels:
      description: "Canais com atribuição similar em todos modelos"
      action: "Confiança alta na performance real"

  final_recommendation:
    template: |
      Based on [BUSINESS CONTEXT], we recommend:

      PRIMARY MODEL: [MODEL NAME]
      Reason: [WHY THIS MODEL FITS]

      SECONDARY MODEL: [MODEL NAME]
      Use for: [SPECIFIC USE CASE]

      AVOID: [MODEL NAME]
      Reason: [WHY NOT APPROPRIATE]
```

---

## Common Pitfalls and Solutions

### Attribution Pitfalls

```yaml
attribution_pitfalls:

  pitfall_1_incomplete_tracking:
    problem: "Touchpoints não trackados corretamente"
    symptoms:
      - "Alto volume de (direct)/(none)"
      - "Canais aparecem com menos conversões que esperado"
      - "Gaps nas jornadas"
    solution:
      - "Audit completo de UTM tagging"
      - "Implementar tracking server-side"
      - "Padronizar nomenclatura cross-team"

  pitfall_2_cross_device_blindness:
    problem: "Mesmo usuário em múltiplos devices não é identificado"
    symptoms:
      - "Jornadas parecem mais curtas que realidade"
      - "Direct/Organic inflados"
      - "Paid undervalued"
    solution:
      - "Implementar login/user ID"
      - "Usar probabilistic matching"
      - "First-party data collection"

  pitfall_3_walled_gardens:
    problem: "Plataformas (FB, Google) não compartilham dados completos"
    symptoms:
      - "Discrepância entre platform reports e analytics"
      - "Conversões duplicadas"
      - "Impossível ver jornada completa"
    solution:
      - "UTM tracking rigoroso"
      - "Server-side tracking (CAPI)"
      - "MMM para validação"

  pitfall_4_single_model_bias:
    problem: "Usar apenas um modelo para todas decisões"
    symptoms:
      - "Budget concentrado em canais de fechamento"
      - "Awareness channels cortados"
      - "Long-term brand building prejudicado"
    solution:
      - "Usar múltiplos modelos"
      - "First-touch para awareness budget"
      - "Last-touch para conversion budget"

  pitfall_5_ignoring_offline:
    problem: "Touchpoints offline não considerados"
    symptoms:
      - "Conversões parecem surgir do nada"
      - "Subestimar impacto de eventos/vendas pessoais"
    solution:
      - "Tracking de offline (QR codes, vanity URLs)"
      - "CRM integration"
      - "Surveys pós-conversão"
```

### Quality Assurance Checklist

```yaml
attribution_qa_checklist:

  data_quality:
    - [ ] UTMs padronizados e consistentes
    - [ ] Sem duplicação de touchpoints
    - [ ] Timestamps corretos (timezone)
    - [ ] User IDs unificados
    - [ ] Conversões linkadas corretamente a touchpoints

  model_validation:
    - [ ] Soma das atribuições = 100%
    - [ ] Nenhum canal com atribuição negativa
    - [ ] Resultados fazem sentido business
    - [ ] Comparação entre modelos realizada

  reporting:
    - [ ] Período de análise definido
    - [ ] Janela de conversão documentada
    - [ ] Definição de conversão clara
    - [ ] Insights acionáveis incluídos

  governance:
    - [ ] Stakeholders alinhados no modelo
    - [ ] Frequência de review definida
    - [ ] Ownership de dados claro
    - [ ] Processo de mudança documentado
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

```yaml
phase_1_foundation:

  week_1:
    tasks:
      - "Audit current tracking implementation"
      - "Document all channels and sources"
      - "Identify data gaps"
      - "Create UTM standards document"
    deliverables:
      - "Tracking audit report"
      - "UTM standards guide"
      - "Gap analysis"

  week_2:
    tasks:
      - "Fix critical tracking issues"
      - "Implement missing UTMs"
      - "Create touchpoints table"
      - "Test data collection"
    deliverables:
      - "Updated tracking implementation"
      - "Touchpoints table schema"
      - "Data quality report"
```

### Phase 2: Model Selection (Week 3-4)

```yaml
phase_2_model_selection:

  week_3:
    tasks:
      - "Extract historical journey data"
      - "Calculate first-touch attribution"
      - "Calculate last-touch attribution"
      - "Calculate linear attribution"
    deliverables:
      - "Journey dataset"
      - "Basic attribution tables"

  week_4:
    tasks:
      - "Calculate time-decay attribution"
      - "Calculate position-based attribution"
      - "Compare all models"
      - "Recommend primary model"
    deliverables:
      - "Full model comparison report"
      - "Model recommendation document"
```

### Phase 3: Production (Week 5-6)

```yaml
phase_3_production:

  week_5:
    tasks:
      - "Build production queries"
      - "Create automated pipelines"
      - "Design dashboard"
      - "Write documentation"
    deliverables:
      - "Production SQL queries"
      - "Automated data pipeline"
      - "Dashboard wireframe"

  week_6:
    tasks:
      - "Deploy dashboard"
      - "Train stakeholders"
      - "Set up alerts"
      - "Document maintenance procedures"
    deliverables:
      - "Live attribution dashboard"
      - "Training materials"
      - "Maintenance runbook"
```

### Ongoing: Optimization

```yaml
ongoing_optimization:

  monthly:
    - "Review attribution trends"
    - "Compare to budget allocation"
    - "Identify optimization opportunities"
    - "Update model if needed"

  quarterly:
    - "Deep dive analysis"
    - "Model accuracy assessment"
    - "Stakeholder presentation"
    - "Budget reallocation recommendations"

  annually:
    - "Full model audit"
    - "Consider advanced models (data-driven)"
    - "Benchmark against industry"
    - "Technology stack review"
```

---

## Output Deliverables

```yaml
deliverables:

  primary:
    attribution_model: |
      Modelo de attribution implementado com:
      - Queries de produção
      - Channel mapping completo
      - Conversion window definido

    attribution_dashboard: |
      Dashboard interativo com:
      - Comparação de modelos
      - Channel performance
      - Journey analysis

    recommendation_report: |
      Relatório com recomendações de:
      - Budget allocation
      - Channel optimization
      - Model selection rationale

  secondary:
    channel_mapping_document: |
      Documentação de:
      - Definição de cada canal
      - UTM standards
      - Grouping logic

    journey_analysis: |
      Análise de:
      - Top journeys
      - Assist patterns
      - Channel synergies

  optional:
    data_driven_model: |
      Se volume suficiente:
      - Markov chain implementation
      - Shapley value calculation
      - Model comparison
```

---

## Quality Checklist

### Pre-Implementation Checklist

```yaml
pre_implementation_checklist:
  - [ ] Business objective claramente definido
  - [ ] Definição de conversão acordada
  - [ ] Canais ativos listados
  - [ ] Tracking audit completo
  - [ ] Stakeholders alinhados
  - [ ] Timeline definido
```

### Model Quality Checklist

```yaml
model_quality_checklist:
  - [ ] Atribuições somam 100% por conversão
  - [ ] Sem valores negativos
  - [ ] Todos canais representados
  - [ ] Janela de conversão apropriada
  - [ ] Múltiplos modelos comparados
  - [ ] Resultados validados com stakeholders
```

### Report Quality Checklist

```yaml
report_quality_checklist:
  - [ ] So What framework aplicado
  - [ ] Insights acionáveis incluídos
  - [ ] Recomendações específicas
  - [ ] Visualizações claras
  - [ ] Comparação com período anterior
  - [ ] Next steps definidos
```

---

## Integration with Other Tasks

### Related Data Pack Tasks

```yaml
related_tasks:

  calculate_clv:
    integration: "CLV por canal de aquisição (first-touch)"
    value: "Entender quais canais trazem clientes de maior valor"

  segment_rfm:
    integration: "RFM segments por attribution path"
    value: "Identificar quais jornadas produzem melhores clientes"

  design_health_score:
    integration: "Health Score por canal de origem"
    value: "Correlacionar canal de aquisição com retenção"

  create_dashboard:
    integration: "Attribution como módulo do DMMM dashboard"
    value: "Visão unificada de marketing performance"
```

---

## Glossary

```yaml
glossary:

  attribution:
    definition: "Processo de atribuir crédito a touchpoints pelo resultado"

  touchpoint:
    definition: "Qualquer interação do cliente com marketing antes da conversão"

  conversion_window:
    definition: "Período antes da conversão onde touchpoints são considerados"

  first_touch:
    definition: "Primeiro touchpoint na jornada do cliente"

  last_touch:
    definition: "Último touchpoint antes da conversão"

  assisted_conversion:
    definition: "Conversão onde o canal participou mas não foi o last-touch"

  mta_multi_touch_attribution:
    definition: "Atribuição que considera múltiplos touchpoints"

  shapley_value:
    definition: "Método de teoria dos jogos para distribuir crédito"

  markov_chain:
    definition: "Modelo probabilístico de transição entre estados"

  removal_effect:
    definition: "Impacto na conversão se um canal for removido"

  utm_parameters:
    definition: "Tags de URL para tracking de campanhas (source, medium, campaign)"

  walled_garden:
    definition: "Plataforma que limita compartilhamento de dados (FB, Google)"
```

---

## Version History

```yaml
version: "1.0"
created: "2026-01-23"
primary_agent: "Avinash Kaushik"
lines: "1100+"

changelog:
  - "1.0: Task inicial criado com 6 modelos de attribution"
  - "1.0: Channel mapping completo com SQL"
  - "1.0: Conversion window methodology"
  - "1.0: Multi-touch attribution framework"
  - "1.0: Reporting recommendations com So What framework"
  - "1.0: Implementation roadmap"
```

---

*Data Intelligence Pack - Task: Build Attribution*
*Primary Agent: Avinash Kaushik*
*Framework: DMMM + See-Think-Do-Care*
