---
task: "Analyze Pricing and Positioning"
responsavel: "@commercial-intelligence"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - competitor_analysis
  - product_value_prop
  - pricing_model
Saida: |
  - positioning_brief
  - price_recommendation
Checklist:
  - "[ ] Comparar preco proprio contra o preco medio do concorrente mapeado"
  - "[ ] Avaliar valor percebido versus preco cobrado"
  - "[ ] Identificar risco de commoditizacao da oferta"
  - "[ ] Recomendar ajuste de posicionamento ou de tabela quando aplicavel"
  - "[ ] Definir a mensagem de diferenciacao para SDR e Closer usarem"
  - "[ ] Registrar hipotese versus dado confirmado de mercado"
---

# *analyze-pricing-and-positioning

## Objetivo

Avaliar preço e posicionamento contra o concorrente real, entregando a mensagem de
diferenciação que `@sdr` e `@closer` devem usar de forma consistente.

## Procedimento

1. Comparar o preço próprio contra a faixa de preço levantada em `competitor_analysis`
   — está acima, na média ou abaixo do mercado?
2. Avaliar valor percebido: o cliente enxerga diferença suficiente para justificar a
   diferença de preço, ou a oferta corre risco de virar commodity (decisão só por preço)?
3. Identificar esse risco de commoditização explicitamente — se presente, a recomendação
   é reforçar diferenciação, não simplesmente baixar preço.
4. Recomendar ajuste de posicionamento (mensagem, público-alvo) ou de tabela (faixa de
   desconto aceitável, novo plano) quando fizer sentido, sempre com justificativa.
5. Definir a mensagem de diferenciação central — curta, específica, defensável — que
   `@sdr` usa na prospecção e `@closer` usa na negociação.
6. Registrar claramente o que é dado confirmado de mercado (preço público, review) versus
   hipótese (suposição sobre percepção do cliente ainda não validada).

## Modelo de brief de posicionamento

```
Preço próprio vs. faixa de mercado:
Valor percebido vs. preço cobrado:
Risco de commoditização (sim/não e por quê):
Mensagem de diferenciação (1-2 frases):
Ajuste recomendado (posicionamento e/ou tabela):
```

## Erros comuns a evitar

- Recomendar desconto como resposta padrão a qualquer sinal de sensibilidade a preço.
- Definir mensagem de diferenciação genérica que qualquer concorrente também alega.
- Não atualizar a análise quando `map-market-and-competitors` mudar significativamente.

## Usage

```
@commercial-intelligence
*analyze-pricing-and-positioning
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `competitor_analysis` | string | Yes | competitor analysis |
| `product_value_prop` | string | Yes | product value proposition |
| `pricing_model` | string | Yes | pricing model |

## Output

- **positioning_brief**: positioning brief
- **price_recommendation**: price recommendation

## Origin

Confidence: 80%
