---
task: "Identify Expansion Opportunity"
responsavel: "@customer-success"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - product_usage_data
  - customer_profile
  - health_score
Saida: |
  - expansion_opportunities
  - upsell_cross_sell_plan
Checklist:
  - "[ ] Identificar uso que indica necessidade de mais capacidade ou modulo adicional"
  - "[ ] Cruzar uso real com produtos ou planos ainda nao contratados"
  - "[ ] Priorizar oportunidade por saude da conta (nunca ofertar para conta em risco primeiro)"
  - "[ ] Construir o argumento de expansao com base em valor ja comprovado"
  - "[ ] Definir o momento certo de abordagem dentro do ciclo do cliente"
  - "[ ] Encaminhar a oportunidade qualificada ao Closer quando aplicavel"
---

# *identify-expansion-opportunity

## Objetivo

Identificar upsell/cross-sell a partir de uso real do produto — nunca de meta de
receita isolada do CS.

## Procedimento

1. Analisar o uso real do produto por conta e identificar padrões que indicam
   necessidade de mais capacidade, mais licenças ou módulo adicional.
2. Cruzar esse uso com os produtos/planos que a conta ainda não contratou.
3. Priorizar por saúde da conta: nunca oferecer expansão para conta com sinal de risco
   aberto em `health_score` — resolver o risco primeiro, oferta depois.
4. Construir o argumento de expansão ancorado em valor já comprovado pelo próprio uso da
   conta, não em meta de receita do time de CS.
5. Definir o momento certo dentro do ciclo do cliente (ex.: após atingir um marco de
   sucesso, nunca no meio de um problema de suporte não resolvido).
6. Quando a oportunidade for qualificada, encaminhar formalmente a `@closer` com o
   contexto de uso e o argumento já montado — CS prepara o terreno, não fecha upsell
   complexo sozinho.

## Modelo de oportunidade

```
Conta:
Sinal de uso que indica expansão:
Produto/plano ainda não contratado:
Saúde da conta (confirmar ausência de risco aberto):
Argumento de expansão (ancorado em valor já comprovado):
Momento recomendado de abordagem:
```

## Erros comuns a evitar

- Oferecer expansão a conta com risco de churn aberto, associando a marca a pressão.
- Basear o argumento em benefício genérico do plano superior, não no uso real da conta.
- Pular a etapa de encaminhar ao Closer e tentar fechar upsell complexo diretamente.

## Usage

```
@customer-success
*identify-expansion-opportunity
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_usage_data` | string | Yes | dados de uso do produto |
| `customer_profile` | string | Yes | perfil do cliente |
| `health_score` | string | Yes | health score |

## Output

- **expansion_opportunities**: expansion opportunities
- **upsell_cross_sell_plan**: upsell/cross-sell plan

## Origin

Confidence: 81%
