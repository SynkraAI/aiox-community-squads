---
task: "Map Market and Competitors"
responsavel: "@commercial-intelligence"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - icp_definition
  - industry_segment
Saida: |
  - market_map
  - competitor_analysis
Checklist:
  - "[ ] Mapear concorrentes diretos e indiretos do segmento"
  - "[ ] Levantar posicionamento, preco e proposta de valor de cada concorrente"
  - "[ ] Identificar diferencial defensavel da oferta propria"
  - "[ ] Identificar tendencia e movimento recente do mercado"
  - "[ ] Sinalizar concorrente com maior sobreposicao de ICP"
  - "[ ] Publicar o mapa competitivo com a fonte de cada dado"
---

# *map-market-and-competitors

## Objetivo

Mapear concorrência e mercado com fonte rastreável, para alimentar posicionamento e
argumento competitivo de `@sdr` e `@closer` — nunca opinião sem lastro.

## Procedimento

1. Listar concorrentes diretos (mesma solução, mesmo ICP) e indiretos (solução
   alternativa para o mesmo problema, incluindo "fazer manualmente"/planilha/não fazer nada).
2. Para cada concorrente, levantar: proposta de valor, faixa de preço, pontos fortes e
   fracos declarados por clientes (reviews públicos, redes sociais, notícias) e onde eles
   costumam ganhar ou perder negociação.
3. Identificar o diferencial defensável da oferta própria — algo que o concorrente não
   replica com facilidade, não um genérico "atendimento melhor" que qualquer um alega.
4. Levantar tendência recente do mercado (consolidação, nova regulação, mudança de
   comportamento de compra) que afete o posicionamento.
5. Sinalizar qual concorrente tem maior sobreposição direta com o ICP definido — esse é
   o principal a monitorar e a preparar argumento de comparação.
6. Publicar o mapa com a fonte de cada dado (site do concorrente, review, notícia) —
   nunca registrar "achismo" como se fosse fato de mercado.

## Modelo comparativo

| Concorrente | Proposta de valor | Preço (faixa) | Força | Fraqueza | Sobreposição com ICP |
|---|---|---|---|---|---|

## Erros comuns a evitar

- Descrever o concorrente pela versão de marketing dele, sem checar reclamação real de clientes.
- Misturar concorrente direto e indireto sem diferenciar o tipo de argumento necessário.
- Publicar dado de preço ou posicionamento sem registrar a fonte.

## Usage

```
@commercial-intelligence
*map-market-and-competitors
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `icp_definition` | string | Yes | ICP definition |
| `industry_segment` | string | Yes | industry segment |

## Output

- **market_map**: market map
- **competitor_analysis**: competitor analysis

## Origin

Confidence: 87%
