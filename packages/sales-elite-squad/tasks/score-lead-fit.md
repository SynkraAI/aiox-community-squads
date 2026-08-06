---
task: "Score Lead Fit"
responsavel: "@commercial-intelligence"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - qualified_company_list
  - icp_definition
  - trigger_signals
Saida: |
  - lead_score_sheet
  - temperature_classification
Checklist:
  - "[ ] Pontuar fit com o ICP de 0 a 100 por conta"
  - "[ ] Classificar temperatura (fria, morna, quente) com criterio explicito"
  - "[ ] Justificar cada nota com o dado que a sustenta"
  - "[ ] Sinalizar lead com dado insuficiente para pontuar"
  - "[ ] Ordenar a lista por prioridade de abordagem"
  - "[ ] Publicar a planilha de pontuacao para o SDR"
---

# *score-lead-fit

## Objetivo

Pontuar fit e temperatura de cada lead da lista, com nota justificada, para orientar a
priorização de abordagem do `@sdr`.

## Procedimento

1. Definir os critérios de pontuação e o peso de cada um: fit firmográfico com o ICP,
   presença e força do gatilho de compra (`trigger_signals`), qualidade do canal de
   contato disponível.
2. Pontuar o fit com o ICP de 0 a 100 — quanto mais próximo dos critérios documentados em
   `*define-icp`, mais alta a nota.
3. Classificar a temperatura:
   - **Quente** — fit alto + gatilho forte e recente.
   - **Morna** — fit alto sem gatilho claro, ou fit médio com gatilho presente.
   - **Fria** — fit baixo, ou dado insuficiente para avaliar com confiança.
4. Justificar cada nota citando o dado concreto que a sustenta — nunca atribuir nota "no
   olho".
5. Sinalizar explicitamente o lead com dado insuficiente em vez de forçar uma pontuação
   sem base real.
6. Ordenar a lista final por prioridade (nota + temperatura) e publicar a planilha para
   `@sdr` usar em `*build-outreach-cadence`.

## Modelo de pontuação

| Empresa | Fit ICP (0-100) | Gatilho (força) | Temperatura | Justificativa | Prioridade |
|---|---|---|---|---|---|

## Erros comuns a evitar

- Dar nota alta só porque a empresa é grande/conhecida, sem checar fit real com o ICP.
- Classificar como "quente" um lead com gatilho antigo ou não confirmado.
- Não sinalizar lead com dado insuficiente, inflando artificialmente a lista qualificada.

## Usage

```
@commercial-intelligence
*score-lead-fit
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `qualified_company_list` | string | Yes | qualified company list |
| `icp_definition` | string | Yes | ICP definition |
| `trigger_signals` | string | No | trigger signals |

## Output

- **lead_score_sheet**: lead score sheet (0-100 por conta)
- **temperature_classification**: temperature classification

## Origin

Confidence: 84%
