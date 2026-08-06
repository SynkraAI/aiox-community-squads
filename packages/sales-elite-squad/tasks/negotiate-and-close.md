---
task: "Negotiate and Close"
responsavel: "@closer"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - roi_case
  - objection_response_playbook
  - meddicc_summary
Saida: |
  - negotiation_plan
  - closing_plan
  - deal_terms
Checklist:
  - "[ ] Definir a faixa de negociacao aceitavel (preco, escopo, prazo, condicao)"
  - "[ ] Priorizar concessao que custa pouco e vale muito para o cliente"
  - "[ ] Preparar pelo menos uma alternativa alem do desconto direto"
  - "[ ] Definir o proximo passo formal apos o 'sim' (contrato, onboarding, kickoff)"
  - "[ ] Confirmar autoridade de quem esta assinando o acordo"
  - "[ ] Registrar os termos finais e a justificativa de cada concessao"
---

# *negotiate-and-close

## Objetivo

Conduzir a negociação final até o acordo, protegendo margem e relação de longo prazo —
fechar não é o objetivo em si, é a consequência de um acordo bom pros dois lados.

## Procedimento

1. Definir previamente a faixa aceitável de negociação: preço mínimo, escopo mínimo,
   prazo de pagamento e quais condições podem ou não ser cedidas.
2. Priorizar concessões de baixo custo e alto valor percebido (ex.: onboarding
   estendido, treinamento extra, suporte prioritário por um período) antes de mexer em preço.
3. Preparar ao menos uma alternativa ao desconto direto — ajuste de escopo, prazo de
   contrato mais longo em troca de desconto, ou implementação faseada.
4. Confirmar que quem está fechando tem autoridade real de assinatura (o Authority
   levantado no BANT/MEDDICC) antes de tratar o acordo como fechado.
5. Definir e comunicar o próximo passo formal assim que houver acordo verbal: contrato,
   data de assinatura, kickoff de onboarding — nunca deixar um "sim" sem próximo passo
   concreto marcado.
6. Registrar os termos finais e justificar cada concessão dada (o que foi trocado por
   quê) — isso vira input direto para `@sales-manager` (forecast) e para
   `@customer-success` (onboarding).

## Estrutura de deal_terms

```
Preço e condição de pagamento final:
Escopo acordado:
Concessões dadas e o que foi trocado por elas:
Quem assinou / autoridade confirmada:
Próximo passo formal e data:
```

## Erros comuns a evitar

- Ceder em preço sem pedir nada em troca (prazo, referência, caso de sucesso).
- Fechar verbalmente sem confirmar autoridade real de quem está do outro lado.
- Deixar o "sim" sem data e responsável definidos para o próximo passo.

## Usage

```
@closer
*negotiate-and-close
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `roi_case` | string | Yes | ROI case |
| `objection_response_playbook` | string | No | objection response playbook |
| `meddicc_summary` | string | Yes | MEDDICC summary |

## Output

- **negotiation_plan**: negotiation plan
- **closing_plan**: closing plan
- **deal_terms**: deal terms

## Origin

Confidence: 84%
