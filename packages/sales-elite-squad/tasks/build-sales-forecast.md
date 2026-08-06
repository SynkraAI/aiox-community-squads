---
task: "Build Sales Forecast"
responsavel: "@sales-manager"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - pipeline_health_report
  - metrics_report
Saida: |
  - sales_forecast
  - confidence_scenarios
Checklist:
  - "[ ] Aplicar taxa de conversao historica por estagio ao pipeline atual"
  - "[ ] Construir cenario conservador, realista e otimista"
  - "[ ] Justificar cada oportunidade incluida no forecast comitado"
  - "[ ] Excluir do comitado oportunidade sem BANT/MEDDICC confirmado"
  - "[ ] Definir nivel de confianca do forecast com racional explicito"
  - "[ ] Publicar o forecast com data de corte e responsavel"
---

# *build-sales-forecast

## Objetivo

Construir um forecast defensável — baseado em taxa de conversão histórica e
qualificação real de cada deal, não em otimismo do time.

## Procedimento

1. Aplicar a taxa de conversão histórica por estágio (de `metrics_report`) sobre o valor
   em pipeline atual, estágio por estágio.
2. Construir três cenários:
   - **Conservador** — só deals com alta probabilidade e MEDDICC completo.
   - **Realista** — aplicando a taxa histórica média por estágio.
   - **Otimista** — incluindo deals com sinal forte mas ainda não fechado.
3. Para cada oportunidade incluída no forecast comitado, exigir justificativa individual
   — não basta o deal estar "no estágio de proposta" para entrar no número comitado.
4. Excluir do comitado qualquer oportunidade sem BANT/MEDDICC confirmado por `@closer`
   — estágio avançado sem qualificação real é forecast inflado.
5. Definir o nível de confiança do forecast (alto/médio/baixo) com o racional explícito
   (ex.: "baixo porque 40% do valor comitado depende de 2 deals sem economic buyer
   confirmado").
6. Publicar o forecast com data de corte e responsável pela atualização — forecast sem
   data de corte fica obsoleto sem ninguém perceber.

## Modelo de forecast

```
Cenário conservador: R$ ___ (deals: ___)
Cenário realista: R$ ___ (deals: ___)
Cenário otimista: R$ ___ (deals: ___)
Nível de confiança: alto / médio / baixo — motivo:
Data de corte: ___  Responsável: ___
```

## Erros comuns a evitar

- Incluir no comitado deal em estágio avançado mas sem qualificação documentada.
- Reportar um único número "realista" sem mostrar os três cenários e o racional.
- Deixar o forecast desatualizado sem data de corte visível.

## Usage

```
@sales-manager
*build-sales-forecast
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pipeline_health_report` | string | Yes | pipeline health report |
| `metrics_report` | string | Yes | metrics report |

## Output

- **sales_forecast**: sales forecast
- **confidence_scenarios**: confidence scenarios (conservador, realista, otimista)

## Origin

Confidence: 83%
