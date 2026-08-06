---
task: "Plan Renewal"
responsavel: "@customer-success"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - health_score
  - contract_data
  - expansion_opportunities
Saida: |
  - renewal_strategy
  - churn_prevention_plan
Checklist:
  - "[ ] Iniciar o planejamento de renovacao com antecedencia definida (nao no ultimo mes)"
  - "[ ] Revisar valor entregue versus valor prometido na venda original"
  - "[ ] Tratar todo sinal de risco antes de abrir a conversa de renovacao"
  - "[ ] Preparar argumento de renovacao ancorado em resultado mensuravel"
  - "[ ] Definir plano B para objecao de preco ou de troca de fornecedor"
  - "[ ] Registrar a probabilidade de renovacao com justificativa"
---

# *plan-renewal

## Objetivo

Preparar a renovação com antecedência e evidência de valor entregue — nunca abrir a
conversa de renovação no último mês, no escuro.

## Procedimento

1. Iniciar o planejamento de renovação com antecedência definida pelo squad (ex.: 90
   dias antes do vencimento) — nunca no último mês.
2. Revisar o valor efetivamente entregue no período contra o que foi prometido na venda
   original — identificar o gap antes que o cliente o traga como objeção.
3. Tratar qualquer sinal de risco identificado em `*monitor-customer-health` antes de
   abrir formalmente a conversa de renovação.
4. Preparar o argumento de renovação ancorado em resultado mensurável e específico da
   conta — nunca discurso genérico de "parceria" sem número por trás.
5. Definir um plano B para objeção de preço ou de troca de fornecedor (ex.: ajuste de
   escopo, condição de pagamento, prova de ROI adicional).
6. Registrar a probabilidade de renovação com justificativa explícita, compartilhada com
   `@sales-manager` para entrar no forecast.

## Modelo de estratégia de renovação

```
Antecedência do início do planejamento:
Valor entregue vs. prometido (gap, se houver):
Sinal de risco tratado antes da conversa (sim/não):
Argumento de renovação (resultado mensurável):
Plano B para objeção de preço/troca:
Probabilidade de renovação e justificativa:
```

## Erros comuns a evitar

- Abrir a conversa de renovação sem antes tratar sinal de risco já conhecido.
- Argumentar com discurso genérico em vez de resultado específico da conta.
- Deixar o planejamento para o último mês, sem tempo de reação a objeção.

## Usage

```
@customer-success
*plan-renewal
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `health_score` | string | Yes | health score |
| `contract_data` | string | Yes | dados do contrato |
| `expansion_opportunities` | string | No | expansion opportunities |

## Output

- **renewal_strategy**: renewal strategy
- **churn_prevention_plan**: churn prevention plan

## Origin

Confidence: 84%
