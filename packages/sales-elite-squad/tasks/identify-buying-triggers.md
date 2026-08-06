---
task: "Identify Buying Triggers"
responsavel: "@commercial-intelligence"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - qualified_company_list
  - market_map
Saida: |
  - trigger_signals
  - prioritized_accounts
Checklist:
  - "[ ] Identificar evento de contratacao, expansao ou rodada de investimento"
  - "[ ] Identificar troca ou adocao recente de tecnologia relevante"
  - "[ ] Identificar mudanca de lideranca ou reestruturacao"
  - "[ ] Identificar sinal publico de dor (vaga aberta, reclamacao, noticia)"
  - "[ ] Classificar cada gatilho como fato verificavel ou hipotese"
  - "[ ] Priorizar contas por forca do gatilho identificado"
---

# *identify-buying-triggers

## Objetivo

Identificar eventos que indicam janela de compra aberta em cada conta da lista, para
priorizar quem abordar primeiro.

## Procedimento

1. Para cada empresa da lista, checar sinal de evento recente: rodada de investimento,
   expansão de equipe ou de escritório, contratação de cargo relevante para a dor que o
   produto resolve (cargo novo costuma vir com orçamento novo ou prioridade nova).
2. Checar troca ou adoção recente de tecnologia relevante (via vaga pedindo skill em
   determinada ferramenta, anúncio de parceria, notícia de implantação).
3. Checar mudança de liderança — novo executivo costuma trazer disposição real a mudar
   fornecedor ou processo estabelecido.
4. Checar sinal público de dor: vaga aberta relacionada ao problema, reclamação pública,
   notícia de crise ou de crescimento acelerado que estressa o processo atual.
5. Classificar cada gatilho encontrado como **fato verificável** (com fonte concreta) ou
   **hipótese** (dedução razoável sem confirmação direta) — nunca misturar os dois sem rótulo.
6. Priorizar contas com gatilho forte e recente — gatilho de mais de alguns meses atrás
   perde força e deve pesar menos na priorização.

## Modelo de registro

| Empresa | Gatilho identificado | Tipo (contratação/tecnologia/liderança/dor pública) | Fato ou hipótese | Fonte | Força (alta/média/baixa) |
|---|---|---|---|---|---|

## Erros comuns a evitar

- Tratar gatilho antigo como se ainda estivesse quente.
- Apresentar hipótese como fato confirmado ao repassar para `@sdr`.
- Ignorar sinal de dor pública só porque não veio de fonte "oficial".

## Usage

```
@commercial-intelligence
*identify-buying-triggers
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `qualified_company_list` | string | Yes | qualified company list |
| `market_map` | string | Yes | market map |

## Output

- **trigger_signals**: trigger signals
- **prioritized_accounts**: prioritized accounts

## Origin

Confidence: 82%
