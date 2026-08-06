---
task: "Monitor Customer Health"
responsavel: "@customer-success"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - product_usage_data
  - support_history
  - nps_data
Saida: |
  - health_score
  - risk_signals
Checklist:
  - "[ ] Definir os componentes do health score (uso, suporte, satisfacao, engajamento)"
  - "[ ] Calcular o score por conta com peso explicito de cada componente"
  - "[ ] Identificar sinal de risco (queda de uso, ticket recorrente, silencio)"
  - "[ ] Classificar risco por severidade e por proximidade da renovacao"
  - "[ ] Definir gatilho automatico de alerta para conta em risco"
  - "[ ] Publicar o painel de health score para o time e para o Gestor Comercial"
---

# *monitor-customer-health

## Objetivo

Calcular um health score consistente e repetível por conta, com sinal de risco
acionável antes que vire cancelamento.

## Procedimento

1. Definir os componentes do health score: uso do produto (frequência e profundidade),
   histórico de suporte (volume e tipo de ticket), satisfação (NPS/CSAT), engajamento
   (resposta a comunicação, presença em QBR).
2. Definir o peso de cada componente conforme o que mais prediz churn no histórico da
   base (ex.: queda de uso costuma pesar mais que atraso em responder e-mail).
3. Calcular o score por conta de forma consistente e repetível — nunca uma nota subjetiva
   sem componente explícito por trás.
4. Identificar sinais de risco específicos: queda de uso mês a mês, ticket de suporte
   recorrente sobre o mesmo problema, silêncio prolongado do ponto de contato principal.
5. Classificar o risco por severidade e por proximidade da renovação — o mesmo sinal de
   risco pesa mais perto do vencimento do contrato.
6. Definir o gatilho automático de alerta (ex.: score cai abaixo de um limiar, ou 2
   sinais de risco simultâneos) para acionar `@customer-success` sem depender de
   percepção manual do time.
7. Publicar o painel de health score, visível ao time e a `@sales-manager` para
   cruzamento com o forecast de renovação.

## Modelo de health score

| Conta | Uso (peso) | Suporte (peso) | Satisfação (peso) | Engajamento (peso) | Score total | Risco |
|---|---|---|---|---|---|---|

## Erros comuns a evitar

- Calcular o score só com dado de uso, ignorando suporte e satisfação.
- Não definir gatilho automático, dependendo só de o CS "perceber" o risco a tempo.
- Deixar o score desatualizado sem frequência de recálculo definida.

## Usage

```
@customer-success
*monitor-customer-health
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_usage_data` | string | Yes | dados de uso do produto |
| `support_history` | string | Yes | historico de suporte |
| `nps_data` | string | No | dados de NPS/satisfacao |

## Output

- **health_score**: health score por conta
- **risk_signals**: risk signals

## Origin

Confidence: 85%
