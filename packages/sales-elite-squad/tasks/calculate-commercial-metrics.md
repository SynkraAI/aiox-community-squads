---
task: "Calculate Commercial Metrics"
responsavel: "@sales-manager"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - revenue_data
  - marketing_and_sales_cost
  - customer_data
Saida: |
  - metrics_report
Checklist:
  - "[ ] Calcular CAC por canal de aquisicao"
  - "[ ] Calcular LTV e a relacao LTV/CAC"
  - "[ ] Calcular ticket medio e sua variacao por segmento"
  - "[ ] Calcular taxa de conversao por estagio do funil"
  - "[ ] Calcular ciclo medio de venda por segmento e por porte de conta"
  - "[ ] Comparar cada metrica contra meta e contra periodo anterior"
---

# *calculate-commercial-metrics

## Objetivo

Calcular CAC, LTV, ticket médio, conversão e ciclo de venda com comparação contra meta
e período anterior — número sem comparação não orienta decisão.

## Procedimento

1. **CAC** — somar custo total de marketing e vendas do período e dividir pelo número de
   clientes fechados no período; calcular também por canal quando houver dado de origem
   do lead.
2. **LTV** — receita média por cliente × margem × tempo médio de retenção; calcular a
   relação LTV/CAC (referência saudável costuma ser ≥ 3).
3. **Ticket médio** — receita total fechada dividida pelo número de deals fechados;
   calcular a variação por segmento/porte de conta.
4. **Taxa de conversão por estágio** — deals que avançaram de um estágio para o
   seguinte dividido pelos deals que entraram naquele estágio.
5. **Ciclo de venda** — tempo médio entre criação do deal e fechamento, segmentado por
   porte de conta (enterprise tende a ciclo mais longo que PME).
6. Comparar cada métrica calculada contra a meta definida e contra o período anterior —
   sem essa comparação, o número não orienta nenhuma decisão.

## Fórmulas de referência

```
CAC = (Custo Marketing + Custo Vendas) / Clientes novos no período
LTV = Ticket médio × Margem × Tempo médio de retenção
LTV / CAC ideal ≳ 3
Ciclo de venda = média(data de fechamento - data de criação do deal)
```

## Erros comuns a evitar

- Calcular CAC sem incluir todo o custo de vendas (só marketing), subestimando o número.
- Reportar ticket médio agregado sem segmentar por porte, escondendo distorção.
- Apresentar a métrica isolada, sem meta e sem comparação histórica.

## Usage

```
@sales-manager
*calculate-commercial-metrics
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `revenue_data` | string | Yes | dados de receita |
| `marketing_and_sales_cost` | string | Yes | custo de marketing e vendas |
| `customer_data` | string | Yes | dados de clientes |

## Output

- **metrics_report**: metrics report (CAC, LTV, ticket medio, taxa de conversao, ciclo de venda)

## Origin

Confidence: 89%
