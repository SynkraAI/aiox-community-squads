# Run Growth Experiment Task

## Purpose

Executar experimentos de growth de forma estruturada e científica para validar hipóteses, medir impacto real e construir conhecimento organizacional. Este task guia o processo completo desde a priorização com ICE framework, design do experimento, cálculo de sample size, análise de significância estatística até a documentação de learnings para futuros experimentos.

---

## Primary Agent

**Sean Ellis** - Growth Hacking Pioneer, CEO GrowthHackers.com

> "Growth hacking é simplesmente o método científico aplicado ao crescimento."

Ellis argumenta que crescimento sustentável vem de experimentação de alta velocidade, não de palpites. O objetivo não é ter ideias brilhantes, mas testar ideias rapidamente e aprender sistematicamente.

---

## Core Philosophy

### The Growth Experiment Mindset

```yaml
growth_experiment_mindset:

  reality_in_most_companies:
    - "Ideias são implementadas baseadas em quem grita mais alto"
    - "Ninguém sabe qual mudança causou qual resultado"
    - "Mesmos erros são repetidos porque learnings não são documentados"
    - "Budget de marketing muda baseado em gut feeling"
    - "Sucesso é atribuído a sorte, fracasso a circunstâncias"

  ellis_diagnosis: |
    "A maioria das empresas está adivinhando. Elas chamam de 'estratégia',
    mas é apenas intuição sem validação. Growth real vem de testar
    hipóteses específicas, medir resultados reais, e aprender rápido."

  the_fix:
    principle_1: "Toda ideia é uma hipótese até ser testada"
    principle_2: "Velocidade de aprendizado > velocidade de execução"
    principle_3: "Um experimento fracassado que ensina é um sucesso"
    principle_4: "Documentar learnings é tão importante quanto rodar o experimento"
```

### High Tempo Testing

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIGH TEMPO TESTING                            │
│              (Sean Ellis - GrowthHackers)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  OBJETIVO: Maximizar aprendizado por unidade de tempo           │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  BAIXO TEMPO DE EXPERIMENTAÇÃO                          │    │
│  │  • 1 experimento por mês                                │    │
│  │  • 12 learnings por ano                                 │    │
│  │  • Crescimento lento                                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ALTO TEMPO DE EXPERIMENTAÇÃO                           │    │
│  │  • 2-3 experimentos por semana                          │    │
│  │  • 100+ learnings por ano                               │    │
│  │  • Vantagem competitiva exponencial                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  FÓRMULA DO CRESCIMENTO:                                        │
│  Growth = Velocidade de Experimentos × Taxa de Sucesso × Impacto│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tier 0: Diagnostic Questions

Antes de rodar qualquer experimento, responda estas perguntas diagnósticas:

```yaml
tier_0_diagnosis:

  experiment_readiness:
    - "Temos tracking implementado para medir o resultado?"
    - "Temos volume suficiente para atingir significância estatística?"
    - "O experimento pode rodar por tempo suficiente sem interferência?"
    - "Há buy-in do time para não mudar nada durante o teste?"

  hypothesis_quality:
    - "A hipótese é específica e testável?"
    - "Definimos claramente o que significa sucesso?"
    - "Sabemos quanto impacto seria significativo?"
    - "Temos uma teoria de por que isso funcionaria?"

  resource_assessment:
    - "Temos recursos para implementar a variante?"
    - "Quanto tempo levará para implementar?"
    - "Qual é o custo de oportunidade?"
    - "O que acontece se funcionar? Conseguimos escalar?"

  risk_evaluation:
    - "Qual é o downside se não funcionar?"
    - "Pode prejudicar clientes existentes?"
    - "Há riscos legais ou de compliance?"
    - "Podemos reverter facilmente se der errado?"

  maturity_check:
    - "Já temos Product-Market Fit confirmado?"
    - "Sabemos qual é nossa North Star Metric?"
    - "Temos histórico de dados para baseline?"
    - "O time tem cultura de experimentação?"
```

---

## Inputs

```yaml
required:
  - experiment_idea: "A ideia ou mudança a ser testada"
  - hypothesis: "Por que acreditamos que isso funcionará"
  - primary_metric: "A métrica principal que será impactada"
  - baseline_value: "Valor atual da métrica"
  - minimum_detectable_effect: "Menor mudança que seria significativa"
  - available_traffic: "Volume disponível para o experimento"

optional:
  - secondary_metrics: "Métricas secundárias a monitorar"
  - guardrail_metrics: "Métricas que não podem piorar"
  - target_audience: "Segmento específico para o teste"
  - experiment_duration: "Duração desejada"
  - implementation_effort: "Esforço estimado"
  - previous_experiments: "Experimentos relacionados já realizados"
  - business_context: "Contexto de negócio relevante"
```

---

## The ICE Prioritization Framework

### What is ICE?

```
┌─────────────────────────────────────────────────────────────────┐
│                      ICE FRAMEWORK                               │
│              (Sean Ellis - GrowthHackers)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  I = IMPACT (Impacto)                                           │
│  ├── "Se funcionar, quão grande será o impacto?"                │
│  ├── Scale: 1-10                                                │
│  └── Pergunta: "Isso move a North Star Metric?"                 │
│                                                                  │
│  C = CONFIDENCE (Confiança)                                     │
│  ├── "Quão confiantes estamos que vai funcionar?"               │
│  ├── Scale: 1-10                                                │
│  └── Pergunta: "Temos evidências de que isso funciona?"         │
│                                                                  │
│  E = EASE (Facilidade)                                          │
│  ├── "Quão fácil é implementar e testar?"                       │
│  ├── Scale: 1-10                                                │
│  └── Pergunta: "Podemos fazer isso esta semana?"                │
│                                                                  │
│  ICE Score = (I + C + E) / 3                                    │
│  ou                                                              │
│  ICE Score = I × C × E (para maior diferenciação)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### ICE Scoring Detailed Criteria

```yaml
ice_scoring_criteria:

  impact_scale:
    10: "Move North Star Metric em 20%+ | Afeta todos os usuários"
    9: "Move North Star em 15-20% | Afeta maioria dos usuários"
    8: "Move North Star em 10-15% | Grande segmento impactado"
    7: "Move North Star em 5-10% | Impacto significativo"
    6: "Move metric secundária significativamente"
    5: "Melhoria moderada em metric importante"
    4: "Melhoria pequena em metric importante"
    3: "Melhoria em metric secundária"
    2: "Impacto marginal"
    1: "Impacto negligenciável"

  confidence_scale:
    10: "A/B test anterior comprovou | Dados internos sólidos"
    9: "Case study de empresa similar | Benchmark forte"
    8: "Pesquisa com usuários confirmou | Dados qualitativos fortes"
    7: "Best practice da indústria | Múltiplas fontes concordam"
    6: "Um case study relevante | Alguma evidência"
    5: "Teoria sólida baseada em princípios | Faz sentido lógico"
    4: "Hipótese informada | Intuição baseada em experiência"
    3: "Palpite educado | Pouca evidência"
    2: "Ideia especulativa | Sem evidência"
    1: "Completo shot in the dark | Contrário à evidência"

  ease_scale:
    10: "Menos de 1 hora | Sem dev necessário | Já temos tudo"
    9: "Algumas horas | Configuração simples"
    8: "1 dia de trabalho | Um recurso necessário"
    7: "2-3 dias | Desenvolvimento leve"
    6: "1 semana | Alguma complexidade"
    5: "2 semanas | Múltiplos recursos"
    4: "1 mês | Coordenação cross-team"
    3: "2+ meses | Projeto significativo"
    2: "Trimestre | Grande iniciativa"
    1: "6+ meses | Transformação massiva"
```

### ICE Scoring Template

```yaml
ice_scoring_template:

  experiment_info:
    name: "[NOME DO EXPERIMENTO]"
    description: "[DESCRIÇÃO BREVE]"
    owner: "[RESPONSÁVEL]"
    date_scored: "[DATA]"

  impact_assessment:
    score: "[1-10]"
    rationale: |
      [Por que este score? Qual métrica será impactada?
      Quantos usuários serão afetados? Qual a magnitude esperada?]
    north_star_connection: "[Como conecta com North Star Metric]"

  confidence_assessment:
    score: "[1-10]"
    rationale: |
      [Que evidências suportam esta hipótese?
      Há dados internos? Cases externos? Pesquisa com usuários?]
    evidence_sources:
      - "[FONTE 1]"
      - "[FONTE 2]"

  ease_assessment:
    score: "[1-10]"
    rationale: |
      [Quanto tempo levará? Quais recursos são necessários?
      Há dependências? Complexidade técnica?]
    estimated_effort: "[TEMPO ESTIMADO]"
    resources_needed: "[RECURSOS]"

  final_calculation:
    average_method: "(I + C + E) / 3 = [SCORE]"
    multiplicative_method: "I × C × E = [SCORE]"

  recommendation:
    priority: "[HIGH/MEDIUM/LOW]"
    next_action: "[PRÓXIMO PASSO]"
```

### ICE Scoring Examples

```yaml
ice_examples:

  example_1_high_priority:
    name: "Adicionar social proof na página de checkout"
    description: "Mostrar número de compras recentes e reviews"

    impact:
      score: 8
      rationale: "Checkout é gargalo principal. 2000 usuários/dia passam por lá."

    confidence:
      score: 7
      rationale: "Baymard Institute mostra 15% lift médio com social proof em checkout"

    ease:
      score: 9
      rationale: "Já temos os dados, só precisa de frontend change"

    ice_average: 8.0
    ice_multiplicative: 504
    verdict: "HIGH PRIORITY - Rodar esta semana"

  example_2_medium_priority:
    name: "Redesign completo do onboarding"
    description: "Novo fluxo de onboarding com gamification"

    impact:
      score: 9
      rationale: "Activation é nosso maior problema"

    confidence:
      score: 5
      rationale: "Gamification funciona em alguns casos, não em outros"

    ease:
      score: 3
      rationale: "2 meses de desenvolvimento, design, QA"

    ice_average: 5.7
    ice_multiplicative: 135
    verdict: "MEDIUM PRIORITY - Validar com protótipo primeiro"

  example_3_low_priority:
    name: "Mudar cor do botão de CTA de azul para verde"
    description: "Testar se verde converte mais"

    impact:
      score: 2
      rationale: "Cor do botão raramente tem impacto significativo isoladamente"

    confidence:
      score: 2
      rationale: "Nenhuma evidência de que funcionaria para nosso público"

    ease:
      score: 10
      rationale: "5 minutos de trabalho"

    ice_average: 4.7
    ice_multiplicative: 40
    verdict: "LOW PRIORITY - Só fazer se não tiver nada melhor"
```

### ICE vs Other Frameworks Comparison

```yaml
prioritization_frameworks_comparison:

  ice:
    factors: ["Impact", "Confidence", "Ease"]
    formula: "(I + C + E) / 3 ou I × C × E"
    best_for: "Growth teams, experimentos rápidos"
    pros:
      - "Simples e rápido de aplicar"
      - "Fácil de entender"
      - "Bom para priorização inicial"
    cons:
      - "Subjetivo sem guidelines claros"
      - "Não considera reach explicitamente"

  rice:
    factors: ["Reach", "Impact", "Confidence", "Effort"]
    formula: "(R × I × C) / E"
    best_for: "Product teams, features maiores"
    pros:
      - "Considera reach explicitamente"
      - "Penaliza esforço mais claramente"
    cons:
      - "Mais complexo"
      - "Requer mais dados"

  pie:
    factors: ["Potential", "Importance", "Ease"]
    formula: "(P + I + E) / 3"
    best_for: "CRO, otimização de conversão"
    pros:
      - "Foco em potencial de melhoria"
      - "Considera importância da página/fluxo"
    cons:
      - "Similar ao ICE na prática"

  recommendation: |
    Use ICE para experimentos de growth e marketing.
    Use RICE para features de produto.
    Use PIE para CRO específico.
    O importante é ser consistente dentro do time.
```

### ICE Prioritization Process

```yaml
ice_prioritization_process:

  step_1_brainstorm:
    description: "Coletar todas as ideias de experimentos"
    sources:
      - "Dados de analytics"
      - "Feedback de clientes"
      - "Ideias do time"
      - "Benchmark de concorrentes"
      - "Best practices"
    output: "Lista não filtrada de ideias"

  step_2_quick_filter:
    description: "Remover ideias obviamente ruins"
    criteria:
      - "Impossível de implementar"
      - "Vai contra valores da empresa"
      - "Já testamos e não funcionou"
      - "Não conecta com nenhuma métrica importante"
    output: "Lista filtrada de candidatos"

  step_3_ice_scoring:
    description: "Pontuar cada ideia com ICE"
    method:
      - "Score individual primeiro"
      - "Calibrar em grupo"
      - "Documentar rationale"
    output: "Lista com ICE scores"

  step_4_stack_rank:
    description: "Ordenar por ICE score"
    considerations:
      - "Desempates vão para maior Impact"
      - "Considerar dependências"
      - "Balancear quick wins e big bets"
    output: "Backlog priorizado"

  step_5_select_sprint:
    description: "Escolher experimentos para o sprint"
    guidelines:
      - "2-3 experimentos simultâneos máximo"
      - "Mix de alto e baixo risco"
      - "Não competir por mesmo tráfego"
    output: "Sprint plan de experimentos"
```

---

## Experiment Design Template

### Experiment Document Structure

```yaml
experiment_document:

  header:
    experiment_id: "[AUTO-GENERATED ou MANUAL]"
    name: "[NOME DESCRITIVO]"
    owner: "[RESPONSÁVEL]"
    status: "[PLANNING/RUNNING/ANALYZING/COMPLETE]"
    created_date: "[DATA]"
    ice_score: "[SCORE]"

  section_1_problem:
    title: "Problem Statement"
    questions:
      - "Qual problema estamos resolvendo?"
      - "Qual métrica mostra que é um problema?"
      - "Quem é afetado?"
    template: |
      Atualmente, [MÉTRICA] está em [VALOR ATUAL].
      Isso é um problema porque [IMPACTO NO NEGÓCIO].
      Isso afeta [QUEM/QUANTOS] usuários.

  section_2_hypothesis:
    title: "Hypothesis"
    structure: "If [CHANGE], then [OUTCOME], because [REASON]"
    template: |
      Se [FIZERMOS ESTA MUDANÇA],
      então [ESTA MÉTRICA] vai [AUMENTAR/DIMINUIR] em [X%],
      porque [RAZÃO BASEADA EM EVIDÊNCIA].
    examples:
      good: |
        "Se adicionarmos depoimentos de clientes na página de pricing,
        então a taxa de conversão vai aumentar em 15%,
        porque social proof reduz ansiedade de compra conforme
        estudos de Cialdini e dados do Baymard Institute."
      bad: |
        "Vamos testar mudar a cor do botão."

  section_3_metrics:
    title: "Success Metrics"
    primary_metric:
      name: "[NOME DA MÉTRICA]"
      current_value: "[BASELINE]"
      target_value: "[META]"
      minimum_detectable_effect: "[MDE]"
    secondary_metrics:
      - name: "[MÉTRICA 2]"
        purpose: "Entender mecanismo"
      - name: "[MÉTRICA 3]"
        purpose: "Detectar efeitos colaterais"
    guardrail_metrics:
      - name: "[MÉTRICA QUE NÃO PODE PIORAR]"
        threshold: "[LIMITE ACEITÁVEL]"

  section_4_design:
    title: "Experiment Design"
    type: "[A/B | A/B/n | MVT | Holdout]"
    variants:
      control: "[DESCRIÇÃO DO CONTROLE]"
      treatment: "[DESCRIÇÃO DO TRATAMENTO]"
    traffic_split: "[50/50 | 90/10 | etc]"
    targeting:
      included: "[QUEM VAI VER]"
      excluded: "[QUEM NÃO VAI VER]"
    randomization: "[USER | SESSION | DEVICE]"

  section_5_sample_size:
    title: "Sample Size & Duration"
    baseline_conversion: "[%]"
    minimum_detectable_effect: "[%]"
    statistical_power: "[80% ou 95%]"
    significance_level: "[95% ou 99%]"
    calculated_sample_size: "[N per variant]"
    daily_traffic: "[VISITORS/DAY]"
    estimated_duration: "[DAYS]"

  section_6_implementation:
    title: "Implementation Details"
    technical_approach: "[COMO SERÁ IMPLEMENTADO]"
    tracking_events: "[EVENTOS A RASTREAR]"
    qa_checklist:
      - "Variantes funcionam corretamente"
      - "Tracking está funcionando"
      - "Não há vazamento entre grupos"
    launch_checklist:
      - "Aprovação do design"
      - "Código revisado"
      - "QA completo"
      - "Stakeholders informados"

  section_7_analysis_plan:
    title: "Analysis Plan"
    when_to_analyze: "[CRITÉRIOS PARA ANÁLISE]"
    statistical_method: "[Z-TEST | T-TEST | CHI-SQUARE]"
    segmentation_planned:
      - "[SEGMENTO 1]"
      - "[SEGMENTO 2]"
    decision_criteria:
      winner: "[QUANDO DECLARAR VENCEDOR]"
      loser: "[QUANDO PARAR O EXPERIMENTO]"
      inconclusive: "[O QUE FAZER SE INCONCLUSIVO]"

  section_8_results:
    title: "Results" # Preenchido após experimento
    data:
      control:
        visitors: "[N]"
        conversions: "[N]"
        rate: "[%]"
      treatment:
        visitors: "[N]"
        conversions: "[N]"
        rate: "[%]"
    statistical_analysis:
      lift: "[%]"
      confidence: "[%]"
      p_value: "[VALUE]"
    verdict: "[WINNER | LOSER | INCONCLUSIVE]"

  section_9_learnings:
    title: "Learnings & Next Steps"
    key_learnings:
      - "[LEARNING 1]"
      - "[LEARNING 2]"
    unexpected_findings: "[SURPRESAS]"
    next_experiments: "[IDEIAS GERADAS]"
    implementation_plan: "[SE VENCEDOR, COMO ESCALAR]"
```

### Hypothesis Writing Framework

```yaml
hypothesis_framework:

  structure:
    template: "If [CHANGE], then [OUTCOME], because [REASON]"

  components:
    change:
      description: "A mudança específica que será feita"
      good: "Adicionarmos um progress bar no checkout"
      bad: "Melhorarmos o checkout"

    outcome:
      description: "O resultado mensurável esperado"
      good: "Taxa de conclusão de checkout aumentará 8%"
      bad: "Mais pessoas vão comprar"

    reason:
      description: "A teoria por trás da expectativa"
      good: "Porque progress bars reduzem abandono (Cialdini - Commitment)"
      bad: "Porque vai ser mais bonito"

  quality_checklist:
    - [ ] É específica (não vaga)
    - [ ] É testável (podemos medir)
    - [ ] É falsificável (pode estar errada)
    - [ ] Tem uma teoria por trás
    - [ ] Conecta com uma métrica de negócio

  examples:
    conversion:
      hypothesis: |
        Se simplificarmos o formulário de cadastro de 8 para 3 campos,
        então a taxa de cadastro aumentará em 25%,
        porque cada campo adicional aumenta friction em ~10% (Baymard).

    retention:
      hypothesis: |
        Se enviarmos um email de check-in 7 dias após signup,
        então D30 retention aumentará em 10%,
        porque touchpoints early in lifecycle aumentam habit formation.

    activation:
      hypothesis: |
        Se mostrarmos um tutorial interativo no primeiro login,
        então a taxa de ativação aumentará em 20%,
        porque guided onboarding reduz time-to-value (Grover's Law).
```

### Minimum Viable Test (MVT) Approach

```yaml
minimum_viable_test:

  philosophy: |
    Antes de construir algo elaborado, teste a hipótese
    da forma mais simples possível. O objetivo é aprender
    rápido, não impressionar com complexidade.

  mvt_ladder:
    level_1_smoke_test:
      description: "Testar se há interesse antes de construir"
      examples:
        - "Fake door test: botão que leva a waitlist"
        - "Landing page antes do produto"
        - "Anúncio antes de ter o produto"
      effort: "Horas"
      confidence: "Baixa mas informativa"

    level_2_wizard_of_oz:
      description: "Simular funcionalidade manualmente"
      examples:
        - "Concierge: fazer manualmente o que seria automático"
        - "Humano por trás da 'AI'"
        - "Email manual antes de automação"
      effort: "Dias"
      confidence: "Média"

    level_3_prototype:
      description: "Versão simplificada mas funcional"
      examples:
        - "Feature com UI básica"
        - "MVP da funcionalidade"
        - "Versão sem todas as edge cases"
      effort: "Semanas"
      confidence: "Alta"

    level_4_full_build:
      description: "Implementação completa"
      examples:
        - "Feature polida"
        - "Toda a UX pensada"
        - "Edge cases cobertos"
      effort: "Meses"
      confidence: "Muito alta"

  decision_framework: |
    Sempre comece no nível mais baixo possível.
    Só suba de nível se:
    1. O teste anterior foi positivo
    2. Precisamos de mais confiança para investir mais
    3. Não há como testar no nível inferior
```

---

## Sample Size Calculator

### Statistical Foundations

```
┌─────────────────────────────────────────────────────────────────┐
│                SAMPLE SIZE FUNDAMENTALS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONCEITOS CHAVE:                                               │
│                                                                  │
│  1. BASELINE CONVERSION RATE (p₁)                               │
│     Taxa de conversão atual (controle)                          │
│     Exemplo: 3% de visitantes convertem                         │
│                                                                  │
│  2. MINIMUM DETECTABLE EFFECT (MDE)                             │
│     Menor mudança que queremos detectar                         │
│     Pode ser absoluto (3% → 4%) ou relativo (+33%)             │
│                                                                  │
│  3. STATISTICAL SIGNIFICANCE (α)                                │
│     Probabilidade de falso positivo (Type I Error)              │
│     Padrão: 95% (α = 0.05)                                     │
│     Significa: 5% chance de declarar vencedor quando não há     │
│                                                                  │
│  4. STATISTICAL POWER (1-β)                                     │
│     Probabilidade de detectar efeito real quando existe         │
│     Padrão: 80% (β = 0.20)                                     │
│     Significa: 80% chance de encontrar efeito se existir        │
│                                                                  │
│  TRADEOFFS:                                                     │
│  • Menor MDE → Mais sample size necessário                      │
│  • Maior confidence → Mais sample size necessário               │
│  • Maior power → Mais sample size necessário                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Sample Size Formula

```yaml
sample_size_formula:

  for_proportions:
    description: "Para métricas de conversão (taxas)"
    formula: |
      n = 2 × [(Zα/2 + Zβ)² × p × (1-p)] / (p₁ - p₂)²

      Onde:
      n = sample size por variante
      Zα/2 = z-score para significance level (1.96 para 95%)
      Zβ = z-score para power (0.84 para 80%)
      p = (p₁ + p₂) / 2 (pooled proportion)
      p₁ = baseline conversion rate
      p₂ = expected conversion rate (baseline + MDE)

  z_scores_reference:
    significance_95: "Zα/2 = 1.96"
    significance_99: "Zα/2 = 2.576"
    significance_90: "Zα/2 = 1.645"
    power_80: "Zβ = 0.84"
    power_90: "Zβ = 1.28"
    power_95: "Zβ = 1.645"

  for_continuous_metrics:
    description: "Para métricas contínuas (revenue, time, etc)"
    formula: |
      n = 2 × [(Zα/2 + Zβ)² × σ²] / δ²

      Onde:
      σ = standard deviation da métrica
      δ = minimum detectable difference
```

### Sample Size Calculator Reference Table

```yaml
sample_size_reference:

  description: |
    Sample size por variante necessário para detectar
    diferentes MDEs com 95% confidence e 80% power.

  baseline_1_percent:
    mde_10_percent_relative: 31000
    mde_20_percent_relative: 7800
    mde_30_percent_relative: 3500
    mde_50_percent_relative: 1300

  baseline_3_percent:
    mde_10_percent_relative: 10300
    mde_20_percent_relative: 2600
    mde_30_percent_relative: 1200
    mde_50_percent_relative: 430

  baseline_5_percent:
    mde_10_percent_relative: 6100
    mde_20_percent_relative: 1550
    mde_30_percent_relative: 700
    mde_50_percent_relative: 260

  baseline_10_percent:
    mde_10_percent_relative: 2900
    mde_20_percent_relative: 730
    mde_30_percent_relative: 330
    mde_50_percent_relative: 120

  baseline_20_percent:
    mde_10_percent_relative: 1300
    mde_20_percent_relative: 330
    mde_30_percent_relative: 150
    mde_50_percent_relative: 55

  interpretation: |
    Para baseline de 3% e querendo detectar 20% relative lift (3% → 3.6%):
    Precisa de ~2600 visitors POR VARIANTE.
    Com 50/50 split: 5200 visitors total.
    Se tem 500 visitors/dia: ~10 dias de experimento.
```

### Sample Size Python Calculator

```python
# Sample Size Calculator for A/B Tests
import math
from scipy import stats

def calculate_sample_size(
    baseline_rate: float,
    minimum_detectable_effect: float,  # Relative (e.g., 0.10 for 10%)
    alpha: float = 0.05,  # Significance level
    power: float = 0.80,  # Statistical power
    two_sided: bool = True
) -> int:
    """
    Calculate required sample size per variant for A/B test.

    Parameters:
    -----------
    baseline_rate : float
        Current conversion rate (e.g., 0.03 for 3%)
    minimum_detectable_effect : float
        Minimum relative lift to detect (e.g., 0.10 for 10% relative lift)
    alpha : float
        Significance level (default 0.05 for 95% confidence)
    power : float
        Statistical power (default 0.80 for 80% power)
    two_sided : bool
        Whether to use two-sided test (default True)

    Returns:
    --------
    int : Required sample size per variant
    """

    # Calculate expected treatment rate
    treatment_rate = baseline_rate * (1 + minimum_detectable_effect)

    # Get z-scores
    if two_sided:
        z_alpha = stats.norm.ppf(1 - alpha / 2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)
    z_beta = stats.norm.ppf(power)

    # Pooled proportion
    p_pooled = (baseline_rate + treatment_rate) / 2

    # Sample size formula
    numerator = 2 * ((z_alpha + z_beta) ** 2) * p_pooled * (1 - p_pooled)
    denominator = (treatment_rate - baseline_rate) ** 2

    n = numerator / denominator

    return math.ceil(n)


def calculate_test_duration(
    sample_size_per_variant: int,
    daily_traffic: int,
    traffic_allocation: float = 1.0,
    num_variants: int = 2
) -> int:
    """
    Calculate how many days the test needs to run.

    Parameters:
    -----------
    sample_size_per_variant : int
        Required sample size per variant
    daily_traffic : int
        Average daily visitors to the page/feature
    traffic_allocation : float
        Percentage of traffic in the experiment (default 100%)
    num_variants : int
        Number of variants including control (default 2)

    Returns:
    --------
    int : Number of days needed
    """
    total_sample_needed = sample_size_per_variant * num_variants
    daily_experiment_traffic = daily_traffic * traffic_allocation

    days = total_sample_needed / daily_experiment_traffic

    return math.ceil(days)


# Example Usage
if __name__ == "__main__":
    # Current conversion rate: 3%
    # Want to detect: 15% relative lift (3% → 3.45%)
    # 95% confidence, 80% power

    sample_size = calculate_sample_size(
        baseline_rate=0.03,
        minimum_detectable_effect=0.15,
        alpha=0.05,
        power=0.80
    )

    print(f"Sample size per variant: {sample_size:,}")
    print(f"Total sample size (2 variants): {sample_size * 2:,}")

    # If 1000 visitors per day
    days = calculate_test_duration(
        sample_size_per_variant=sample_size,
        daily_traffic=1000
    )

    print(f"Days needed: {days}")
```

### Sample Size Decision Matrix

```yaml
sample_size_decisions:

  scenario_1_low_traffic:
    situation: "< 1000 visitors/day"
    challenge: "Dificuldade de atingir sample size"
    recommendations:
      - "Aumentar MDE (testar mudanças maiores)"
      - "Reduzir variants (apenas A/B, não A/B/C)"
      - "Focar em páginas de maior tráfego"
      - "Considerar métodos Bayesianos"
      - "Estender duração (cuidado com sazonalidade)"

  scenario_2_high_traffic:
    situation: "> 100,000 visitors/day"
    opportunity: "Pode detectar efeitos pequenos rapidamente"
    recommendations:
      - "Usar MDE menor (5-10%)"
      - "Aumentar power para 95%"
      - "Testar múltiplas variantes"
      - "Segmentar análises"

  scenario_3_low_conversion:
    situation: "Baseline < 1%"
    challenge: "Precisa de muito tráfego"
    recommendations:
      - "Focar em etapas anteriores do funnel"
      - "Usar métricas secundárias (clicks, engagement)"
      - "Considerar composite metrics"
      - "Testar mudanças maiores"

  scenario_4_high_conversion:
    situation: "Baseline > 20%"
    opportunity: "Sample size menor necessário"
    recommendations:
      - "Pode testar otimizações finas"
      - "Atenção: ceiling effect pode limitar upside"
      - "Considerar guardrail metrics"
```

### Duration Considerations

```yaml
duration_considerations:

  minimum_duration:
    rule: "Sempre rodar pelo menos 1 semana completa"
    reason: "Capturar variação dia-da-semana"

  maximum_duration:
    rule: "Não exceder 4-6 semanas sem boa razão"
    reason: "External factors começam a contaminar"

  full_business_cycles:
    rule: "Incluir ciclos completos relevantes"
    examples:
      - "E-commerce: incluir fim de semana"
      - "B2B: incluir semana completa (pular feriados)"
      - "Sazonal: cuidado com eventos atípicos"

  stopping_rules:
    never_stop_early:
      - "Porque está ganhando (peeking problem)"
      - "Porque está perdendo (pode reverter)"
      - "Por pressão de stakeholders"

    ok_to_stop_early:
      - "Guardrail metric violado significativamente"
      - "Bug crítico descoberto"
      - "Usando sequential testing com regras pré-definidas"
```

---

## Statistical Significance

### Understanding Statistical Significance

```
┌─────────────────────────────────────────────────────────────────┐
│              STATISTICAL SIGNIFICANCE EXPLAINED                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  O QUE SIGNIFICA "95% CONFIDENCE"?                              │
│                                                                  │
│  NÃO significa: "95% de chance de que B é melhor que A"         │
│                                                                  │
│  SIGNIFICA: "Se A e B fossem iguais, haveria apenas 5%          │
│  de chance de observar uma diferença tão grande quanto esta"    │
│                                                                  │
│  ───────────────────────────────────────────────────────────    │
│                                                                  │
│  P-VALUE EXPLICADO:                                             │
│                                                                  │
│  p = 0.03 significa:                                            │
│  "Se não houvesse diferença real, teríamos 3% de chance         │
│  de ver esta diferença (ou maior) por acaso"                    │
│                                                                  │
│  Se p < α (0.05), rejeitamos a hipótese nula                   │
│  Se p ≥ α, não temos evidência suficiente                      │
│                                                                  │
│  ───────────────────────────────────────────────────────────    │
│                                                                  │
│  ERROS POSSÍVEIS:                                               │
│                                                                  │
│  TYPE I (False Positive):                                       │
│  Declarar vencedor quando não há diferença real                 │
│  Controlado por α (significance level)                          │
│                                                                  │
│  TYPE II (False Negative):                                      │
│  Não detectar diferença quando ela existe                       │
│  Controlado por β (1 - power)                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Significance Calculation

```yaml
significance_calculation:

  z_test_for_proportions:
    description: "Teste mais comum para taxas de conversão"
    formula: |
      z = (p₂ - p₁) / √[p̂(1-p̂)(1/n₁ + 1/n₂)]

      Onde:
      p₁ = conversion rate do controle
      p₂ = conversion rate do tratamento
      p̂ = pooled proportion = (x₁ + x₂) / (n₁ + n₂)
      n₁, n₂ = sample sizes

    interpretation:
      z_greater_than_196: "Significante a 95% (p < 0.05)"
      z_greater_than_258: "Significante a 99% (p < 0.01)"

  chi_square_test:
    description: "Alternativa para dados categóricos"
    when_to_use: "Múltiplas categorias ou variantes"

  t_test:
    description: "Para métricas contínuas (revenue, time)"
    when_to_use: "Média de valores, não proporções"
```

### Significance Python Calculator

```python
# Statistical Significance Calculator
import math
from scipy import stats

def calculate_significance(
    control_visitors: int,
    control_conversions: int,
    treatment_visitors: int,
    treatment_conversions: int,
    one_sided: bool = False
) -> dict:
    """
    Calculate statistical significance of A/B test results.

    Returns dict with:
    - control_rate: Control conversion rate
    - treatment_rate: Treatment conversion rate
    - relative_lift: Percentage lift
    - z_score: Z-statistic
    - p_value: P-value
    - significant_95: Whether significant at 95%
    - significant_99: Whether significant at 99%
    - confidence_interval: 95% CI for the difference
    """

    # Calculate conversion rates
    p1 = control_conversions / control_visitors
    p2 = treatment_conversions / treatment_visitors

    # Relative lift
    relative_lift = (p2 - p1) / p1 if p1 > 0 else 0

    # Pooled proportion
    p_pooled = (control_conversions + treatment_conversions) / (control_visitors + treatment_visitors)

    # Standard error
    se = math.sqrt(p_pooled * (1 - p_pooled) * (1/control_visitors + 1/treatment_visitors))

    # Z-score
    z_score = (p2 - p1) / se if se > 0 else 0

    # P-value
    if one_sided:
        p_value = 1 - stats.norm.cdf(z_score)
    else:
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    # Confidence interval for difference
    se_diff = math.sqrt(
        (p1 * (1 - p1) / control_visitors) +
        (p2 * (1 - p2) / treatment_visitors)
    )
    ci_95 = (
        (p2 - p1) - 1.96 * se_diff,
        (p2 - p1) + 1.96 * se_diff
    )

    return {
        'control_rate': p1,
        'treatment_rate': p2,
        'absolute_difference': p2 - p1,
        'relative_lift': relative_lift,
        'z_score': z_score,
        'p_value': p_value,
        'significant_95': p_value < 0.05,
        'significant_99': p_value < 0.01,
        'confidence_interval_95': ci_95
    }


def interpret_results(results: dict) -> str:
    """
    Generate human-readable interpretation of results.
    """
    interpretation = []

    interpretation.append(f"Control: {results['control_rate']:.2%}")
    interpretation.append(f"Treatment: {results['treatment_rate']:.2%}")
    interpretation.append(f"Lift: {results['relative_lift']:+.1%}")
    interpretation.append(f"P-value: {results['p_value']:.4f}")

    if results['significant_99']:
        interpretation.append("✅ WINNER - Statistically significant at 99% confidence")
    elif results['significant_95']:
        interpretation.append("✅ WINNER - Statistically significant at 95% confidence")
    else:
        interpretation.append("❌ NOT SIGNIFICANT - No clear winner")

    ci = results['confidence_interval_95']
    interpretation.append(f"95% CI for difference: [{ci[0]:.2%}, {ci[1]:.2%}]")

    return "\n".join(interpretation)


# Example Usage
if __name__ == "__main__":
    results = calculate_significance(
        control_visitors=5000,
        control_conversions=150,  # 3.0%
        treatment_visitors=5000,
        treatment_conversions=180  # 3.6%
    )

    print(interpret_results(results))
```

### Common Significance Mistakes

```yaml
significance_mistakes:

  mistake_1_peeking:
    description: "Checar resultados repetidamente durante o teste"
    problem: |
      Cada vez que você olha os resultados, aumenta a chance
      de um falso positivo. Se checar 5x com α=0.05, a chance
      real de falso positivo é ~19%, não 5%.
    solution:
      - "Definir sample size/duração antes"
      - "Não olhar até completar"
      - "Ou usar sequential testing com correção"

  mistake_2_stopping_early:
    description: "Parar o teste quando atinge significância"
    problem: |
      Significância flutuará durante o teste. Parar quando
      atinge 95% artificialmente infla resultados.
    solution:
      - "Rodar até sample size calculado"
      - "Ignorar resultados intermediários"

  mistake_3_multiple_metrics:
    description: "Testar muitas métricas sem correção"
    problem: |
      Se testar 20 métricas com α=0.05, espera-se 1 falso
      positivo por acaso (20 × 0.05 = 1).
    solution:
      - "Definir UMA métrica primária"
      - "Usar Bonferroni correction para secundárias"
      - "Tratar outras como exploratórias"

  mistake_4_ignoring_practical_significance:
    description: "Celebrar qualquer resultado estatisticamente significante"
    problem: |
      Um lift de 0.1% pode ser estatisticamente significante
      com sample grande, mas não vale a pena implementar.
    solution:
      - "Definir MDE baseado em impacto de negócio"
      - "Perguntar: vale o esforço de implementar?"

  mistake_5_conflating_significance_and_certainty:
    description: "Pensar que 95% confidence = 95% chance de estar certo"
    problem: |
      Confidence level NÃO é a probabilidade de que o tratamento
      é melhor. É a probabilidade de observar este resultado
      se não houvesse diferença real.
    solution:
      - "Entender interpretação Frequentist corretamente"
      - "Ou usar métodos Bayesianos se quer probabilidades"
```

### Bayesian vs Frequentist

```yaml
bayesian_vs_frequentist:

  frequentist:
    philosophy: "Probabilidade como frequência de longo prazo"
    output: "P-value e confidence interval"
    interpretation: |
      "Se repetíssemos este experimento infinitas vezes,
      5% das vezes veríamos este resultado por acaso"
    pros:
      - "Padrão da indústria"
      - "Bem entendido"
      - "Ferramentas abundantes"
    cons:
      - "P-value mal interpretado"
      - "Não pode parar early facilmente"
      - "Não dá probabilidade direta"

  bayesian:
    philosophy: "Probabilidade como grau de crença"
    output: "Probability of being best"
    interpretation: |
      "Dado os dados observados, há 92% de probabilidade
      de que o tratamento é melhor que o controle"
    pros:
      - "Interpretação intuitiva"
      - "Pode parar early com correções"
      - "Incorpora prior knowledge"
    cons:
      - "Menos padronizado"
      - "Requires choosing priors"
      - "Ferramentas menos maduras"

  when_to_use_what:
    frequentist:
      - "Quando stakeholders esperam p-values"
      - "Para publicação científica"
      - "Quando há tráfego suficiente para sample size"
    bayesian:
      - "Quando precisa parar early"
      - "Quando tráfego é limitado"
      - "Quando quer probabilidade direta"

  tools:
    frequentist: ["Optimizely", "VWO", "Google Optimize"]
    bayesian: ["Dynamic Yield", "Convert", "Custom implementations"]
```

---

## Learning Documentation

### Why Documentation Matters

```yaml
documentation_importance:

  sean_ellis_quote: |
    "O experimento que não é documentado não aconteceu.
    Se não sabemos o que aprendemos, vamos repetir os mesmos erros."

  problems_without_documentation:
    - "Mesmos experimentos são repetidos"
    - "Learnings são perdidos quando pessoas saem"
    - "Padrões não são identificados"
    - "Decisões não têm justificativa"
    - "Novos membros não têm contexto"

  benefits_of_documentation:
    - "Conhecimento institucional acumulado"
    - "Evita repetição de erros"
    - "Identifica padrões de sucesso"
    - "Acelera onboarding"
    - "Suporta decisões futuras"
```

### Experiment Learning Template

```yaml
learning_template:

  header:
    experiment_id: "[ID]"
    experiment_name: "[NOME]"
    date_completed: "[DATA]"
    owner: "[RESPONSÁVEL]"
    verdict: "[WINNER/LOSER/INCONCLUSIVE]"

  section_1_summary:
    title: "Executive Summary"
    template: |
      ## O que testamos
      [Uma frase sobre a mudança testada]

      ## Resultado
      [WINNER/LOSER/INCONCLUSIVE] com [X%] lift e [Y%] confidence.

      ## Impacto
      Se implementado permanentemente, esperamos [IMPACTO ANUALIZADO].

      ## Decisão
      [IMPLEMENTAR/NÃO IMPLEMENTAR/ITERAR]

  section_2_results_detail:
    title: "Results Detail"
    data_table:
      columns: ["Variant", "Visitors", "Conversions", "Rate", "vs Control"]
    statistical_summary:
      - primary_metric_lift: "[%]"
      - confidence_level: "[%]"
      - p_value: "[VALUE]"
    secondary_metrics: "[RESULTADOS DE MÉTRICAS SECUNDÁRIAS]"
    segmentation_analysis: "[DIFERENÇAS POR SEGMENTO]"

  section_3_learnings:
    title: "Key Learnings"
    what_we_learned:
      - "[LEARNING 1 - específico e acionável]"
      - "[LEARNING 2]"
      - "[LEARNING 3]"

    hypothesis_validation:
      original_hypothesis: "[HIPÓTESE ORIGINAL]"
      validated: "[SIM/NÃO/PARCIALMENTE]"
      explanation: "[POR QUE]"

    unexpected_findings:
      - "[SURPRESA 1]"
      - "[SURPRESA 2]"

    what_worked: "[O QUE FUNCIONOU]"
    what_didnt_work: "[O QUE NÃO FUNCIONOU]"

  section_4_implications:
    title: "Implications & Next Steps"
    for_this_area:
      - "[IMPLICAÇÃO 1]"
      - "[IMPLICAÇÃO 2]"

    for_other_areas:
      - "[INSIGHT APLICÁVEL EM OUTRO LUGAR]"

    follow_up_experiments:
      - name: "[EXPERIMENTO SUGERIDO]"
        rationale: "[POR QUE TESTAR]"
        priority: "[HIGH/MEDIUM/LOW]"

    implementation_plan:
      decision: "[IMPLEMENTAR/NÃO]"
      timeline: "[QUANDO]"
      owner: "[QUEM]"
      dependencies: "[DEPENDÊNCIAS]"

  section_5_meta:
    title: "Experiment Meta"
    experiment_quality:
      sample_size_achieved: "[SIM/NÃO]"
      duration_sufficient: "[SIM/NÃO]"
      implementation_issues: "[DESCRIÇÃO]"
      tracking_issues: "[DESCRIÇÃO]"

    process_learnings:
      what_went_well: "[PROCESSO]"
      what_could_improve: "[MELHORIA]"

    tags: ["[TAG1]", "[TAG2]", "[TAG3]"]
```

### Experiment Repository Structure

```yaml
experiment_repository:

  organization:
    by_area:
      - "acquisition/"
      - "activation/"
      - "retention/"
      - "referral/"
      - "revenue/"
    by_quarter:
      - "2024-Q1/"
      - "2024-Q2/"
    by_status:
      - "completed/"
      - "running/"
      - "planned/"

  naming_convention:
    pattern: "[DATE]-[AREA]-[NAME]"
    examples:
      - "2024-01-15-activation-onboarding-progress-bar"
      - "2024-02-03-revenue-checkout-social-proof"

  required_documents:
    per_experiment:
      - "design.md: Documento de design do experimento"
      - "results.md: Resultados e learnings"
      - "assets/: Screenshots, dados brutos"

  index_file:
    description: "README com tabela de todos experimentos"
    columns:
      - "ID"
      - "Name"
      - "Status"
      - "Primary Metric"
      - "Result"
      - "Lift"
      - "Link"

  search_capabilities:
    by_metric: "Encontrar todos experimentos que afetaram X"
    by_result: "Encontrar todos winners/losers"
    by_tag: "Encontrar experimentos sobre pricing"
    by_date: "Experimentos de Q1 2024"
```

### Learning Synthesis Process

```yaml
learning_synthesis:

  monthly_review:
    description: "Reunião mensal para sintetizar learnings"
    agenda:
      - "Review de experimentos completados"
      - "Identificar padrões"
      - "Atualizar best practices"
      - "Priorizar próximos experimentos"
    participants:
      - "Growth lead"
      - "Product manager"
      - "Data analyst"

  quarterly_retrospective:
    description: "Deep dive trimestral"
    questions:
      - "Quais foram nossos maiores wins?"
      - "Quais foram nossos maiores learnings?"
      - "Que padrões estamos vendo?"
      - "O que mudar no processo?"
    output:
      - "Updated playbook"
      - "New experiment ideas"
      - "Process improvements"

  pattern_identification:
    description: "Identificar o que consistentemente funciona/não funciona"
    categories:
      always_works:
        - "Social proof em checkout"
        - "Progress indicators em forms longos"
      never_works:
        - "Apenas mudar cores de botão"
        - "Pop-ups agressivos"
      depends:
        - "Urgency messaging (funciona short-term, prejudica long-term)"
        - "Discounts (funciona aquisição, prejudica retention)"
```

---

## Experiment Workflow

### End-to-End Process

```
┌─────────────────────────────────────────────────────────────────┐
│                GROWTH EXPERIMENT WORKFLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PHASE 1: IDEATION                                              │
│  ├── Coletar ideias de múltiplas fontes                        │
│  ├── Quick filter (remover obviamente ruins)                   │
│  └── Adicionar ao backlog                                       │
│                                                                  │
│  PHASE 2: PRIORITIZATION                                        │
│  ├── Score com ICE framework                                   │
│  ├── Stack rank                                                │
│  └── Selecionar para sprint                                    │
│                                                                  │
│  PHASE 3: DESIGN                                                │
│  ├── Escrever hipótese clara                                   │
│  ├── Definir métricas                                          │
│  ├── Calcular sample size                                      │
│  └── Documentar experiment design                              │
│                                                                  │
│  PHASE 4: IMPLEMENTATION                                        │
│  ├── Desenvolver variantes                                     │
│  ├── Setup tracking                                            │
│  ├── QA completo                                               │
│  └── Launch checklist                                          │
│                                                                  │
│  PHASE 5: MONITORING                                            │
│  ├── Health checks (tracking funcionando)                      │
│  ├── Guardrail metrics                                         │
│  └── NÃO olhar resultados primários                           │
│                                                                  │
│  PHASE 6: ANALYSIS                                              │
│  ├── Calcular significância                                    │
│  ├── Análise de segmentos                                      │
│  └── Interpretar resultados                                    │
│                                                                  │
│  PHASE 7: DOCUMENTATION                                         │
│  ├── Documentar learnings                                      │
│  ├── Atualizar repository                                      │
│  └── Comunicar resultados                                      │
│                                                                  │
│  PHASE 8: ACTION                                                │
│  ├── Implementar winners                                       │
│  ├── Gerar novos experimentos                                  │
│  └── Atualizar backlog                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Weekly Experiment Cadence

```yaml
weekly_cadence:

  monday:
    meeting: "Experiment Standup (15 min)"
    agenda:
      - "Status de experimentos running"
      - "Qualquer issue de tracking"
      - "Experimentos prontos para launch"

  tuesday_wednesday:
    activities:
      - "Design de novos experimentos"
      - "Implementation"
      - "QA"

  thursday:
    meeting: "Experiment Review (30 min)"
    agenda:
      - "Review de experimentos completados"
      - "Decisões de go/no-go"
      - "Document learnings"

  friday:
    meeting: "Prioritization (30 min)"
    agenda:
      - "ICE score novas ideias"
      - "Select experiments para próxima semana"
      - "Update backlog"

  ongoing:
    - "Launches: Tuesday ou Wednesday (evitar Monday/Friday)"
    - "No launches: Antes de feriados ou eventos"
```

---

## Common Pitfalls and Solutions

### Experiment Pitfalls

```yaml
experiment_pitfalls:

  pitfall_1_no_hypothesis:
    description: "Testar sem hipótese clara"
    symptom: "Não sabemos por que funcionou ou não"
    solution: "Sempre começar com 'If X, then Y, because Z'"

  pitfall_2_wrong_metric:
    description: "Medir a coisa errada"
    symptom: "Ganhou no teste, perdeu no negócio"
    solution: |
      Definir métrica primária que conecta com North Star.
      Incluir guardrail metrics.

  pitfall_3_too_many_changes:
    description: "Testar múltiplas mudanças de uma vez"
    symptom: "Não sabemos qual mudança causou o efeito"
    solution: "Uma mudança por experimento (ou MVT formal)"

  pitfall_4_insufficient_sample:
    description: "Parar antes de atingir sample size"
    symptom: "Resultados não replicam"
    solution: "Calcular sample size antes, rodar até completar"

  pitfall_5_ignoring_segments:
    description: "Só olhar resultado agregado"
    symptom: "Perder insights importantes"
    solution: |
      Analisar por segmento (new vs returning, mobile vs desktop,
      high value vs low value)

  pitfall_6_no_documentation:
    description: "Não documentar learnings"
    symptom: "Repetir mesmos erros"
    solution: "Template obrigatório para cada experimento"

  pitfall_7_hippo_overrule:
    description: "Highest Paid Person's Opinion anula dados"
    symptom: "Experimentos que perdem são implementados anyway"
    solution: |
      Culture shift. Dados > opinião.
      Se override, documentar razão.

  pitfall_8_winner_fatigue:
    description: "Só implementar winners, ignorar learnings de losers"
    symptom: "Não aprender com fracassos"
    solution: |
      Losers são igualmente valiosos para aprendizado.
      Document o que NÃO funciona.
```

### Quality Assurance Checklist

```yaml
experiment_qa_checklist:

  pre_launch:
    design:
      - [ ] Hipótese documentada (If/Then/Because)
      - [ ] Métrica primária definida
      - [ ] Baseline conhecido
      - [ ] MDE definido
      - [ ] Sample size calculado
      - [ ] Duration estimada
      - [ ] Guardrail metrics definidos

    implementation:
      - [ ] Variantes implementadas corretamente
      - [ ] Visual QA em todos devices
      - [ ] Funcionalidade testada
      - [ ] Não há bugs óbvios
      - [ ] Experience é consistente

    tracking:
      - [ ] Eventos de tracking funcionando
      - [ ] Dados chegando na ferramenta
      - [ ] Segmentação correta
      - [ ] Não há vazamento entre grupos

    launch:
      - [ ] Stakeholders notificados
      - [ ] Rollback plan existe
      - [ ] Monitoring setup

  during_experiment:
    - [ ] Tracking continua funcionando
    - [ ] Sample está crescendo conforme esperado
    - [ ] Guardrail metrics estáveis
    - [ ] Nenhum bug reportado

  post_experiment:
    - [ ] Sample size atingido
    - [ ] Duration mínima completada
    - [ ] Análise estatística feita
    - [ ] Segmentation analysis
    - [ ] Learnings documentados
    - [ ] Results comunicados
    - [ ] Next steps definidos
```

---

## Output Deliverables

```yaml
deliverables:

  primary:
    prioritized_backlog:
      description: |
        Backlog de experimentos priorizado com ICE scores,
        pronto para execução por ordem de prioridade.
      includes:
        - "Lista de experimentos com ICE scores"
        - "Rationale para cada score"
        - "Sprint selection"

    experiment_document:
      description: |
        Documento completo do experimento com todos os
        detalhes necessários para execução.
      includes:
        - "Hypothesis"
        - "Metrics"
        - "Sample size calculation"
        - "Design details"
        - "Analysis plan"

    results_report:
      description: |
        Relatório de resultados com análise estatística
        e interpretação de negócio.
      includes:
        - "Statistical analysis"
        - "Confidence intervals"
        - "Segmentation"
        - "Verdict"

  secondary:
    learning_document:
      description: |
        Documentação de learnings para repositório
        de conhecimento.
      includes:
        - "Key learnings"
        - "Implications"
        - "Next experiments"

    process_improvements:
      description: |
        Melhorias no processo de experimentação
        baseado em retrospectiva.

  optional:
    dashboard:
      description: "Dashboard de experimentos running/completed"

    playbook_updates:
      description: "Atualizações no playbook de growth baseado em learnings"
```

---

## Integration with Other Tasks

### Related Data Pack Tasks

```yaml
related_tasks:

  define_north_star:
    integration: "North Star Metric é o alvo dos experimentos"
    value: "Garantir que experimentos conectam com métrica principal"

  run_pmf_test:
    integration: "PMF Test antes de experimentos de scale"
    value: "Não otimizar produto sem PMF confirmado"

  calculate_clv:
    integration: "CLV como guardrail metric"
    value: "Garantir que wins de curto prazo não prejudicam CLV"

  design_health_score:
    integration: "Health Score como guardrail"
    value: "Monitorar se experimentos afetam saúde de clientes"

  create_dashboard:
    integration: "Dashboard de experimentos"
    value: "Visualizar pipeline e resultados de experimentos"

  analyze_cohort:
    integration: "Cohort analysis para experimentos de retention"
    value: "Entender impacto de longo prazo de experimentos"
```

---

## Glossary

```yaml
glossary:

  ice_framework:
    definition: "Framework de priorização: Impact × Confidence × Ease"
    creator: "Sean Ellis"

  minimum_detectable_effect:
    definition: "Menor mudança que o experimento pode detectar com confiança"
    abbreviation: "MDE"

  statistical_significance:
    definition: "Probabilidade de que resultado não é devido ao acaso"
    common_threshold: "95% (p < 0.05)"

  statistical_power:
    definition: "Probabilidade de detectar efeito real quando existe"
    common_threshold: "80%"

  p_value:
    definition: "Probabilidade de observar este resultado se não houvesse diferença real"

  type_i_error:
    definition: "Falso positivo - declarar vencedor quando não há diferença"
    alias: "False positive"

  type_ii_error:
    definition: "Falso negativo - não detectar diferença quando existe"
    alias: "False negative"

  peeking:
    definition: "Checar resultados repetidamente durante o teste"
    problem: "Aumenta falsos positivos"

  guardrail_metric:
    definition: "Métrica que não pode piorar durante experimento"

  mvt:
    definition: "Minimum Viable Test - testar hipótese da forma mais simples"

  high_tempo_testing:
    definition: "Maximizar velocidade de experimentos para acelerar aprendizado"

  hypothesis:
    definition: "Afirmação testável sobre o que esperamos que aconteça"
    format: "If [CHANGE], then [OUTCOME], because [REASON]"

  sample_size:
    definition: "Número de observações necessárias para conclusões confiáveis"

  conversion_rate:
    definition: "Porcentagem de visitantes que completam ação desejada"

  lift:
    definition: "Mudança percentual entre tratamento e controle"
    types:
      absolute: "Diferença em pontos percentuais (3% → 4% = 1pp)"
      relative: "Diferença percentual ((4-3)/3 = 33%)"

  confidence_interval:
    definition: "Range onde o verdadeiro valor provavelmente está"
    common: "95% CI"

  north_star_metric:
    definition: "A única métrica mais importante que reflete valor entregue"

  aarrr:
    definition: "Pirate Metrics: Acquisition, Activation, Retention, Referral, Revenue"
```

---

## Version History

```yaml
version: "1.0"
created: "2026-01-23"
primary_agent: "Sean Ellis"
lines: "1900+"

changelog:
  - "1.0: Task inicial criado com ICE framework completo"
  - "1.0: Experiment design template detalhado"
  - "1.0: Sample size calculator com fórmulas e Python code"
  - "1.0: Statistical significance methodology completa"
  - "1.0: Learning documentation framework"
  - "1.0: End-to-end experiment workflow"
  - "1.0: Common pitfalls e solutions"
  - "1.0: QA checklist completo"
  - "1.0: Integration com outros Data Pack tasks"
```

---

*Data Intelligence Pack - Task: Run Growth Experiment*
*Primary Agent: Sean Ellis*
*Framework: ICE + High Tempo Testing + Scientific Method*
