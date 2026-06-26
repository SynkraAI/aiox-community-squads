# Health Score Validation Checklist

## Visao Geral

Este checklist guia a validacao completa de um sistema de Health Score para clientes. Baseado nos frameworks de Nick Mehta (Gainsight DEAR, Health Score) e Peter Fader (Customer Centricity, CLV correlation).

> "Health Score nao e sobre prever churn - e sobre identificar oportunidades de intervencao proativa antes que seja tarde." — Inspirado em Nick Mehta

---

## REGRA DE OURO

**Nunca lance um Health Score sem validar:**
1. Cada componente tem justificativa de negocio? (Component Validation)
2. Os pesos refletem impacto real no outcome? (Weight Justification)
3. Os thresholds diferenciam acoes distintas? (Threshold Testing)
4. Os alertas sao acionaveis e acurados? (Alert Accuracy)
5. O score prediz o outcome desejado? (Correlation with Outcomes)

---

## FASE 0: PRE-FLIGHT CHECK

### Definicao de Objetivo
- [ ] Qual outcome o Health Score deve predizer? (churn, expansion, NPS?)
- [ ] Janela de predicao definida? (30, 60, 90 dias?)
- [ ] Definicao de "healthy" e "at risk" alinhada com stakeholders?
- [ ] Baseline de churn/outcome atual documentado?
- [ ] Success metric do projeto Health Score definida?

### Dados Disponiveis
- [ ] Dados de usage/produto disponiveis?
- [ ] Dados de engagement/marketing disponiveis?
- [ ] Dados de suporte disponiveis?
- [ ] Dados de relacionamento/NPS disponiveis?
- [ ] Dados de contrato/financeiros disponiveis?
- [ ] Historico de churn/outcome para validacao disponivel?

### Stakeholders
- [ ] CS team envolvido na definicao?
- [ ] Product team consultado sobre usage metrics?
- [ ] Finance alinhado sobre definicao de churn?
- [ ] Executive sponsor identificado?

**Gate Check:** Todos os itens acima devem estar completos antes de avancar.

---

## FASE 1: COMPONENT VALIDATION

### 1.1 Identificacao de Componentes

#### Framework DEAR como Base (Nick Mehta)

| Componente | Descricao | Dados Necessarios | Status |
|------------|-----------|-------------------|--------|
| **D - Deployment** | Cliente implementou o produto? | Setup completion, feature activation | [ ] |
| **E - Engagement** | Cliente esta ativo? | Login frequency, DAU/MAU | [ ] |
| **A - Adoption** | Cliente usa features avancadas? | Feature usage depth, expansion | [ ] |
| **R - ROI** | Cliente ve valor? | NPS, CSAT, testimonials | [ ] |

### 1.2 Mapeamento de Componentes

Para CADA componente proposto, documentar:

```yaml
component_documentation:
  name: "[Nome do Componente]"
  category: "[Deployment | Engagement | Adoption | ROI | Support | Growth]"
  business_justification: "[Por que este componente importa?]"
  data_source: "[Sistema de origem]"
  metric_definition: "[Definicao precisa da metrica]"
  calculation: "[Formula de calculo]"
  refresh_frequency: "[Real-time | Daily | Weekly]"
  data_quality_score: "[1-10]"
  correlation_hypothesis: "[Como esperamos que correlacione com outcome?]"
```

### 1.3 Checklist por Categoria de Componente

#### Product Usage
- [ ] Login/session frequency definido?
- [ ] Feature adoption metrics mapeados?
- [ ] Usage depth vs breadth distinguido?
- [ ] Time-in-app ou similar disponivel?
- [ ] Dados em frequencia adequada (daily minimum)?

#### Engagement
- [ ] Email open/click rates incluidos?
- [ ] Event attendance tracking disponivel?
- [ ] Webinar participation medido?
- [ ] Community engagement mapeado?
- [ ] Marketing touchpoints registrados?

#### Support
- [ ] Ticket volume tracking disponivel?
- [ ] Ticket sentiment analysis possivel?
- [ ] Resolution time medido?
- [ ] Escalation rate rastreado?
- [ ] CSAT pos-ticket coletado?

#### Relationship
- [ ] NPS coletado com frequencia adequada?
- [ ] Executive sponsor identified?
- [ ] Champion strength measured?
- [ ] Stakeholder changes tracked?
- [ ] Meeting/QBR attendance logged?

#### Growth Signals
- [ ] Upsell/cross-sell tracking?
- [ ] Contract expansion history?
- [ ] Referral activity?
- [ ] Case study willingness?
- [ ] Advocacy signals?

#### Financial
- [ ] Payment timeliness tracked?
- [ ] Contract value relative to usage?
- [ ] Discount dependency measured?
- [ ] Revenue trend analyzed?

### 1.4 Validacao de Componentes

Para CADA componente, verificar:

| Check | Descricao | Status |
|-------|-----------|--------|
| **Data Available** | Dados existem e sao acessiveis? | [ ] |
| **Data Quality** | Completeness >90%, accuracy verified? | [ ] |
| **Business Rationale** | Stakeholder concorda que importa? | [ ] |
| **Variance** | Componente varia entre clientes? (nao e constante) | [ ] |
| **Freshness** | Dados atualizados com frequencia adequada? | [ ] |
| **Measurable** | Pode ser calculado de forma consistente? | [ ] |
| **Actionable** | Time pode agir com base neste componente? | [ ] |

### 1.5 Red Flags de Componentes

Componentes a EVITAR ou usar com cuidado:

```yaml
red_flags:
  vanity_metrics:
    - "Pageviews sem contexto"
    - "Total logins (sem frequencia)"
    - "Emails enviados (sem engagement)"
    reason: "Nao indicam valor real para cliente"

  lagging_indicators:
    - "Churn request (ja e tarde)"
    - "Contract cancellation"
    - "Data export request"
    reason: "Nao permitem intervencao proativa"

  unstable_data:
    - "Dados de terceiros com baixa cobertura"
    - "Metricas com alta variancia diaria"
    - "Dados com gaps frequentes"
    reason: "Geram ruido no score"

  proxy_metrics:
    - "Company size como proxy de engagement"
    - "Industry como proxy de health"
    reason: "Podem introduzir bias"
```

### 1.6 Componentes Minimos Recomendados

```yaml
minimum_viable_health_score:
  required:
    - "Product usage frequency (DAU/WAU/MAU)"
    - "Core feature adoption"
    - "Support ticket sentiment"
    - "Relationship strength (NPS ou similar)"
  recommended:
    - "Engagement com comunicacoes"
    - "Growth signals (expansion interest)"
    - "Payment health"
  optional:
    - "Community participation"
    - "Event attendance"
    - "Advocacy signals"
```

---

## FASE 2: WEIGHT JUSTIFICATION

### 2.1 Metodologia de Pesos

#### Opcao A: Expert-Based (Rapido, Menos Preciso)
- [ ] Stakeholders listados para input?
- [ ] Votacao/ranking realizado?
- [ ] Consenso documentado?
- [ ] Justificativa por peso registrada?

#### Opcao B: Data-Driven (Preciso, Requer Historico)
- [ ] Dados historicos de churn disponiveis (min 100 eventos)?
- [ ] Correlacao por componente calculada?
- [ ] Regressao logistica ou similar executada?
- [ ] Feature importance extraida?

#### Opcao C: Hibrido (Recomendado)
- [ ] Pesos iniciais definidos por experts?
- [ ] Validacao com dados historicos realizada?
- [ ] Ajustes baseados em correlacao aplicados?
- [ ] Ciclo de refinamento planejado?

### 2.2 Template de Justificativa de Pesos

```yaml
weight_justification:
  component: "[Nome]"
  proposed_weight: "[%]"

  expert_rationale:
    stakeholder_votes:
      - stakeholder: "[Nome]"
        weight: "[%]"
        reasoning: "[Justificativa]"
    consensus_weight: "[%]"

  data_validation:
    correlation_with_outcome: "[r value]"
    statistical_significance: "[p-value]"
    feature_importance_rank: "[1-N]"

  final_weight: "[%]"
  adjustment_reason: "[Se diferente do consensus, por que?]"
```

### 2.3 Checklist de Validacao de Pesos

| Check | Descricao | Status |
|-------|-----------|--------|
| **Sum to 100%** | Todos os pesos somam 100%? | [ ] |
| **No Dominance** | Nenhum componente >50%? | [ ] |
| **Minimum Threshold** | Todos componentes >=5%? (se incluido, deve importar) | [ ] |
| **Business Alignment** | Pesos refletem prioridades de negocio? | [ ] |
| **Data Support** | Pesos maiores tem maior correlacao com outcome? | [ ] |
| **Documented** | Toda justificativa esta registrada? | [ ] |

### 2.4 Distribuicao Tipica de Pesos (Benchmark)

```yaml
typical_weights:
  product_usage:
    range: "25-40%"
    rationale: "Indicador mais direto de valor"

  support_health:
    range: "15-25%"
    rationale: "Leading indicator de friccao"

  engagement:
    range: "10-20%"
    rationale: "Sinal de interesse continuo"

  relationship:
    range: "10-20%"
    rationale: "NPS/CSAT como proxy de satisfacao"

  growth_signals:
    range: "10-15%"
    rationale: "Indica interesse em expansao"

  financial:
    range: "5-15%"
    rationale: "Saude financeira do relacionamento"
```

### 2.5 Sensitivity Analysis

- [ ] Pesos alterados em +-10% mudam significativamente a distribuicao?
- [ ] Remover um componente muda dramaticamente o score?
- [ ] Score e robusto a pequenas variacoes?

```yaml
sensitivity_test:
  baseline_distribution:
    healthy: "[%]"
    at_risk: "[%]"
    critical: "[%]"

  test_1_increase_usage_weight:
    change: "+10% usage, -10% support"
    new_distribution:
      healthy: "[%]"
      at_risk: "[%]"
      critical: "[%]"
    significant_change: "[yes/no]"

  test_2_remove_engagement:
    change: "Remove engagement, redistribute"
    new_distribution:
      healthy: "[%]"
      at_risk: "[%]"
      critical: "[%]"
    significant_change: "[yes/no]"
```

---

## FASE 3: THRESHOLD TESTING

### 3.1 Definicao de Thresholds

#### Ranges Padrao (Escala 0-100)

```yaml
default_thresholds:
  healthy:
    range: "70-100"
    color: "Verde"
    action: "Candidato a upsell/advocacy"

  at_risk:
    range: "40-69"
    color: "Amarelo"
    action: "Intervencao proativa"

  critical:
    range: "0-39"
    color: "Vermelho"
    action: "Resgate imediato"
```

### 3.2 Validacao de Thresholds

#### Teste de Distribuicao
- [ ] Distribuicao inicial calculada?
- [ ] % em cada categoria esta razoavel?

```yaml
distribution_check:
  expected:
    healthy: "50-70%"
    at_risk: "20-35%"
    critical: "5-15%"

  actual:
    healthy: "[%]"
    at_risk: "[%]"
    critical: "[%]"

  assessment: "[OK | Thresholds muito altos | Thresholds muito baixos]"
```

#### Teste de Acionabilidade
- [ ] Time consegue atender todos os "critical"?
- [ ] "At risk" tem intervencoes escalaveis?
- [ ] "Healthy" nao esta sendo ignorado?

```yaml
actionability_test:
  critical_count: "[N]"
  cs_capacity_per_week: "[N]"
  weeks_to_address_all: "[N]"
  is_feasible: "[yes/no]"

  at_risk_count: "[N]"
  automated_actions_available: "[yes/no]"

  healthy_count: "[N]"
  upsell_capacity: "[N/month]"
```

#### Teste de Diferenciacao
- [ ] Churn rate difere significativamente entre categorias?
- [ ] Expansion rate difere entre categorias?
- [ ] NPS difere entre categorias?

```yaml
differentiation_test:
  metric: "churn_rate"
  healthy_value: "[%]"
  at_risk_value: "[%]"
  critical_value: "[%]"
  statistical_significance: "[p-value]"

  metric: "nps"
  healthy_value: "[score]"
  at_risk_value: "[score]"
  critical_value: "[score]"
  statistical_significance: "[p-value]"
```

### 3.3 Ajuste de Thresholds

#### Processo de Ajuste
1. [ ] Distribuicao inicial analisada?
2. [ ] Outcome por categoria verificado?
3. [ ] Thresholds ajustados se necessario?
4. [ ] Nova distribuicao recalculada?
5. [ ] Novo outcome por categoria verificado?
6. [ ] Ciclo repetido ate convergencia?

#### Criterios para Ajuste

```yaml
adjustment_criteria:
  lower_threshold_if:
    - "Muito poucos clientes em 'critical'"
    - "Churn rate em 'at risk' similar a 'critical'"
    - "Team tem capacidade para mais intervencoes"

  raise_threshold_if:
    - "Muitos clientes em 'critical' (>20%)"
    - "Team nao consegue atender todos"
    - "Churn rate em 'critical' similar a 'at risk'"
```

### 3.4 Banda de Tolerancia (Hysteresis)

- [ ] Banda de tolerancia definida para evitar flip-flop?
- [ ] Cliente precisa cruzar threshold + banda para mudar categoria?

```yaml
hysteresis_band:
  purpose: "Evitar mudancas frequentes de categoria"
  band_size: "5 pontos"

  example:
    threshold: 70
    move_to_at_risk: "<= 65 (threshold - band)"
    move_to_healthy: ">= 75 (threshold + band)"
```

### 3.5 Sub-Thresholds (Opcional)

```yaml
sub_thresholds:
  critical:
    critical_high: "30-39"
    critical_low: "0-29"
    action_difference: "Low = executive escalation"

  at_risk:
    at_risk_high: "55-69"
    at_risk_low: "40-54"
    action_difference: "Low = immediate outreach"

  healthy:
    healthy_high: "85-100"
    healthy_low: "70-84"
    action_difference: "High = advocacy candidates"
```

---

## FASE 4: ALERT ACCURACY

### 4.1 Tipos de Alertas

```yaml
alert_types:
  threshold_breach:
    trigger: "Score cruza threshold"
    example: "Cliente X caiu de 72 para 68 (healthy -> at_risk)"
    urgency: "Medium"

  rapid_decline:
    trigger: "Score cai >X pontos em Y dias"
    example: "Cliente Y caiu 15 pontos em 7 dias"
    urgency: "High"

  component_spike:
    trigger: "Componente individual em nivel critico"
    example: "Support tickets aumentaram 3x"
    urgency: "High"

  trend_alert:
    trigger: "Tendencia negativa por Z semanas"
    example: "Score declinando por 4 semanas consecutivas"
    urgency: "Medium"

  positive_signal:
    trigger: "Score subiu significativamente"
    example: "Cliente Z subiu de 55 para 75"
    urgency: "Low (opportunity)"
```

### 4.2 Configuracao de Alertas

Para CADA tipo de alerta, configurar:

```yaml
alert_configuration:
  alert_name: "[Nome]"
  trigger_condition: "[Condicao]"
  threshold_value: "[Valor]"
  lookback_period: "[Periodo]"
  min_confidence: "[% ou score]"
  recipients: "[Roles ou individuals]"
  channel: "[Email | Slack | In-app | SMS]"
  action_required: "[Acao esperada]"
  sla_response: "[Tempo para resposta]"
  escalation_if_no_response: "[Sim/Nao]"
```

### 4.3 Validacao de Alertas

#### Teste de Volume
- [ ] Quantos alertas sao gerados por dia/semana?
- [ ] Time consegue processar todos?
- [ ] Ha alert fatigue?

```yaml
volume_test:
  alerts_per_day: "[N]"
  team_capacity_per_day: "[N]"
  ratio: "[%]"
  assessment: "[OK | Too many | Too few]"

  target:
    critical_alerts: "<5/day per CSM"
    warning_alerts: "<10/day per CSM"
```

#### Teste de Relevancia
- [ ] Alertas criticos realmente viram churn se ignorados?
- [ ] Alertas de oportunidade realmente convertem?
- [ ] Ha alertas ignorados consistentemente?

```yaml
relevance_test:
  critical_alerts_last_90_days: "[N]"
  critical_alerts_that_churned: "[N]"
  true_positive_rate: "[%]"

  opportunity_alerts_last_90_days: "[N]"
  opportunity_alerts_that_converted: "[N]"
  true_positive_rate: "[%]"

  alerts_marked_false_positive: "[N]"
  false_positive_rate: "[%]"
```

#### Teste de Timing
- [ ] Alertas chegam com tempo suficiente para acao?
- [ ] Alertas nao sao tardios demais?
- [ ] Lead time medio ate outcome?

```yaml
timing_test:
  avg_lead_time_before_churn: "[dias]"
  min_acceptable_lead_time: "[dias]"
  is_sufficient: "[yes/no]"

  avg_time_from_alert_to_action: "[horas]"
  target_time_to_action: "[horas]"
  is_meeting_sla: "[yes/no]"
```

### 4.4 Metricas de Qualidade de Alertas

```yaml
alert_quality_metrics:
  precision:
    definition: "% de alertas que sao relevantes"
    formula: "True Positives / (True Positives + False Positives)"
    target: ">80%"
    current: "[%]"

  recall:
    definition: "% de eventos capturados por alertas"
    formula: "True Positives / (True Positives + False Negatives)"
    target: ">70%"
    current: "[%]"

  lead_time:
    definition: "Tempo medio entre alerta e outcome"
    target: ">30 days"
    current: "[days]"

  actioned_rate:
    definition: "% de alertas que resultam em acao"
    target: ">90%"
    current: "[%]"
```

### 4.5 Feedback Loop para Alertas

- [ ] Mecanismo de feedback configurado?
- [ ] CSMs podem marcar alertas como util/nao util?
- [ ] Alertas com baixo rating sao revisados?
- [ ] Thresholds de alertas sao ajustados baseado em feedback?

```yaml
feedback_loop:
  collection_method: "[Como feedback e coletado]"
  review_frequency: "[Weekly | Monthly]"
  adjustment_authority: "[Quem pode mudar thresholds]"
  documentation: "[Onde mudancas sao registradas]"
```

---

## FASE 5: CORRELATION WITH OUTCOMES

### 5.1 Definicao de Outcomes

```yaml
primary_outcomes:
  churn:
    definition: "[Definicao precisa de churn]"
    measurement_window: "[Periodo]"
    data_source: "[Sistema]"

  expansion:
    definition: "[Definicao de expansion]"
    measurement_window: "[Periodo]"
    data_source: "[Sistema]"

  nps:
    definition: "[NPS score]"
    measurement_frequency: "[Quando coletado]"
    data_source: "[Sistema]"
```

### 5.2 Analise de Correlacao

#### Correlacao Score vs Outcome
- [ ] Correlacao calculada entre Health Score e churn?
- [ ] Correlacao calculada entre Health Score e expansion?
- [ ] Correlacao calculada entre Health Score e NPS?

```yaml
correlation_analysis:
  health_score_vs_churn:
    correlation: "[r value]"
    p_value: "[significance]"
    direction: "[negative expected]"
    strength: "[weak | moderate | strong]"

  health_score_vs_expansion:
    correlation: "[r value]"
    p_value: "[significance]"
    direction: "[positive expected]"
    strength: "[weak | moderate | strong]"

  health_score_vs_nps:
    correlation: "[r value]"
    p_value: "[significance]"
    direction: "[positive expected]"
    strength: "[weak | moderate | strong]"
```

#### Correlacao por Componente
- [ ] Qual componente tem maior correlacao com churn?
- [ ] Qual componente tem maior correlacao com expansion?
- [ ] Ha componentes sem correlacao significativa?

```yaml
component_correlation:
  - component: "[Nome]"
    weight: "[%]"
    correlation_with_churn: "[r]"
    correlation_with_expansion: "[r]"
    assessment: "[Keep | Increase weight | Decrease weight | Remove]"
```

### 5.3 Poder Preditivo

#### Lift Analysis
- [ ] Health Score melhora predicao vs baseline?
- [ ] Quanto lift o score fornece?

```yaml
lift_analysis:
  baseline_churn_rate: "[%]"
  churn_rate_critical_segment: "[%]"
  lift: "[X times baseline]"

  baseline_expansion_rate: "[%]"
  expansion_rate_healthy_segment: "[%]"
  lift: "[X times baseline]"
```

#### ROC/AUC Analysis (se aplicavel)
- [ ] AUC calculado para predicao de churn?
- [ ] AUC > 0.7 para ser util?

```yaml
roc_analysis:
  auc_score: "[0-1]"
  interpretation:
    "0.5": "No better than random"
    "0.6-0.7": "Poor"
    "0.7-0.8": "Acceptable"
    "0.8-0.9": "Good"
    "0.9+": "Excellent"
  current_assessment: "[Poor | Acceptable | Good | Excellent]"
```

### 5.4 Cohort Analysis

- [ ] Cohorts definidos por faixa de Health Score?
- [ ] Outcome por cohort rastreado ao longo do tempo?
- [ ] Diferencas entre cohorts sao significativas?

```yaml
cohort_analysis:
  cohort_healthy:
    initial_size: "[N]"
    churn_90_days: "[%]"
    expansion_90_days: "[%]"

  cohort_at_risk:
    initial_size: "[N]"
    churn_90_days: "[%]"
    expansion_90_days: "[%]"

  cohort_critical:
    initial_size: "[N]"
    churn_90_days: "[%]"
    expansion_90_days: "[%]"

  statistical_test: "[Chi-square | t-test]"
  p_value: "[significance]"
  conclusion: "[Significant difference | No significant difference]"
```

### 5.5 Recalibracao

#### Quando Recalibrar
- [ ] Produto mudou significativamente?
- [ ] Base de clientes mudou (novo segmento)?
- [ ] Correlacao com outcome degradou?
- [ ] Passou 6+ meses desde ultima calibracao?

#### Processo de Recalibracao
1. [ ] Dados historicos atualizados coletados?
2. [ ] Correlacao por componente recalculada?
3. [ ] Pesos ajustados baseado em dados?
4. [ ] Thresholds re-validados?
5. [ ] Nova versao documentada?
6. [ ] Stakeholders informados da mudanca?

```yaml
recalibration_log:
  version: "[N]"
  date: "[YYYY-MM-DD]"
  trigger: "[Por que recalibrar]"
  changes:
    - component: "[Nome]"
      old_weight: "[%]"
      new_weight: "[%]"
      reason: "[Justificativa]"
  validation_results:
    new_correlation: "[r]"
    improvement: "[+/- vs anterior]"
  approved_by: "[Nome]"
```

---

## FASE 6: QUALITY GATES FINAIS

### 6.1 Gate de Componentes
```yaml
gate_components:
  checks:
    - "Todos componentes tem justificativa documentada"
    - "Dados disponiveis com quality >7/10"
    - "Nenhum componente red flag incluido"
    - "Minimo 4 componentes de categorias diferentes"
  all_passed: "[ ]"
```

### 6.2 Gate de Pesos
```yaml
gate_weights:
  checks:
    - "Pesos somam 100%"
    - "Nenhum peso >50%"
    - "Todos pesos >=5%"
    - "Justificativa documentada"
    - "Sensitivity analysis realizado"
  all_passed: "[ ]"
```

### 6.3 Gate de Thresholds
```yaml
gate_thresholds:
  checks:
    - "Distribuicao dentro do esperado"
    - "Diferencas entre categorias sao significativas"
    - "Time consegue atender volume de criticos"
    - "Banda de tolerancia configurada"
  all_passed: "[ ]"
```

### 6.4 Gate de Alertas
```yaml
gate_alerts:
  checks:
    - "Todos tipos de alerta configurados"
    - "Volume de alertas e gerenciavel"
    - "Precision >80%"
    - "Lead time >30 dias"
    - "Feedback loop configurado"
  all_passed: "[ ]"
```

### 6.5 Gate de Correlacao
```yaml
gate_correlation:
  checks:
    - "Correlacao com churn significativa (p<0.05)"
    - "AUC >0.7 (se aplicavel)"
    - "Lift >2x vs baseline"
    - "Cohort analysis confirma diferencas"
    - "Plano de recalibracao definido"
  all_passed: "[ ]"
```

---

## SCORE CARD FINAL

Conte os itens completados e calcule:

| Fase | Items | Completos | % |
|------|-------|-----------|---|
| F0: Pre-Flight | 14 | [ ] | [ ]% |
| F1: Component Validation | 45 | [ ] | [ ]% |
| F2: Weight Justification | 25 | [ ] | [ ]% |
| F3: Threshold Testing | 20 | [ ] | [ ]% |
| F4: Alert Accuracy | 25 | [ ] | [ ]% |
| F5: Correlation | 20 | [ ] | [ ]% |
| F6: Quality Gates | 5 | [ ] | [ ]% |
| **TOTAL** | **154** | [ ] | [ ]% |

| Score | Status | Acao |
|-------|--------|------|
| >90% | Ready for Production | Launch com monitoring |
| 75-89% | Ready with Gaps | Documentar riscos, launch com plano de melhoria |
| 60-74% | Needs Work | Enderear gaps criticos antes de launch |
| <60% | Not Ready | Trabalho significativo necessario |

---

## APPENDIX A: TROUBLESHOOTING COMUM

### Problema: Score Nao Correlaciona com Churn
```
Causas Comuns:
- Componentes nao capturam sinais reais
- Pesos nao refletem importancia
- Definicao de churn inconsistente
- Dados desatualizados

Solucoes:
1. Revisar componentes com dados historicos
2. Recalcular pesos com regressao
3. Alinhar definicao de churn com Finance
4. Verificar freshness de dados
```

### Problema: Muitos Clientes em "Critical"
```
Causas Comuns:
- Threshold muito alto
- Componente com dados ruins puxando score baixo
- Produto com problemas reais de adocao

Solucoes:
1. Revisar threshold com distribuicao real
2. Auditar componentes individualmente
3. Verificar se e problema de dados ou produto
```

### Problema: Alert Fatigue
```
Causas Comuns:
- Threshold de alertas muito sensivel
- Muitos tipos de alertas ativos
- Falta de priorizacao

Solucoes:
1. Aumentar threshold de alertas criticos
2. Consolidar alertas similares
3. Implementar priorizacao por CLV
```

### Problema: Falsos Positivos Altos
```
Causas Comuns:
- Componentes com alta variancia
- Dados ruidosos
- Falta de contexto (ex: sazonalidade)

Solucoes:
1. Suavizar com medias moveis
2. Adicionar bandas de tolerancia
3. Incorporar contexto de negocio
```

---

## APPENDIX B: TEMPLATES

### Template: Health Score Design Document

```markdown
# Health Score Design - [Versao]

## Objetivo
[Qual outcome predizer e janela de tempo]

## Componentes
| Componente | Peso | Justificativa |
|------------|------|---------------|
| ... | ... | ... |

## Thresholds
| Categoria | Range | Acao |
|-----------|-------|------|
| ... | ... | ... |

## Alertas
[Lista de alertas configurados]

## Validacao
| Metrica | Target | Atual |
|---------|--------|-------|
| Correlacao com churn | >0.5 | ... |
| AUC | >0.7 | ... |
| Precision alertas | >80% | ... |

## Proxima Recalibracao
[Data e trigger]

## Aprovado por
[Nome e data]
```

### Template: Monthly Health Score Review

```markdown
# Health Score Review - [Mes/Ano]

## Distribuicao
| Categoria | % | vs Mes Anterior |
|-----------|---|-----------------|
| Healthy | ... | ... |
| At Risk | ... | ... |
| Critical | ... | ... |

## Outcomes do Mes
- Churn em Critical: [%]
- Churn em At Risk: [%]
- Churn em Healthy: [%]
- Expansion em Healthy: [%]

## Alertas
- Total gerados: [N]
- Actioned: [N] ([%])
- True Positive Rate: [%]

## Issues Identificados
- ...

## Acoes para Proximo Mes
- [ ] ...

## Recalibracao Necessaria?
[Sim/Nao + justificativa]
```

---

## PRINCIPIO FINAL

> "Um Health Score e tao bom quanto as acoes que ele habilita. Score sem acao e vaidade analitica. Acao sem score e intuicao sem escala."
> — Inspirado em Nick Mehta e Peter Fader

---

*Checklist Version: 1.0*
*Data Intelligence Pack - Health Score Validation*
*Primary Agent: Nick Mehta*
*Secondary Agent: Peter Fader*
