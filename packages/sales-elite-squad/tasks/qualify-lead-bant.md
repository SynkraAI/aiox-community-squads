---
task: "Qualify Lead BANT"
responsavel: "@sdr"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - lead_conversation_notes
  - behavioral_profile
Saida: |
  - bant_assessment
  - purchase_probability_score
Checklist:
  - "[ ] Levantar orcamento disponivel ou faixa aproximada"
  - "[ ] Levantar autoridade real de decisao do interlocutor"
  - "[ ] Levantar necessidade declarada e necessidade oculta"
  - "[ ] Levantar urgencia e prazo real de decisao"
  - "[ ] Atribuir nota de 0 a 100 de probabilidade de compra com justificativa"
  - "[ ] Classificar o lead como pronto, em maturacao ou desqualificado"
---

# *qualify-lead-bant

## Objetivo

Aplicar BANT/GPCT sobre a conversa com o lead e atribuir uma nota de 0 a 100 de
probabilidade de compra, sempre justificada.

## Procedimento

1. **Budget** — perguntar, direta ou indiretamente, a faixa de investimento já
   considerada ou o orçamento do time/área; na ausência de resposta, inferir por porte e
   faturamento do ICP e marcar como hipótese.
2. **Authority** — identificar se o interlocutor decide, influencia ou só coleta
   informação. Perguntar diretamente quando não estiver claro: "quem mais participa
   dessa decisão?".
3. **Need** — distinguir necessidade declarada (o que ele diz precisar) de necessidade
   oculta (dor inferida do contexto e do segmento, ainda não nomeada pelo lead).
4. **Timing** — perguntar pelo gatilho e pelo prazo real: "o que motivou vocês a olhar
   isso agora?", "até quando isso precisa estar resolvido?".
5. Pontuar cada dimensão de 0 a 25 (total 0-100), ou aplicar peso diferente por
   dimensão quando o motion de vendas exigir (ex.: Authority pesa mais em venda enterprise).
6. Classificar o resultado:
   - **70-100** — pronto para o Closer, segue para `*book-meeting`.
   - **40-69** — em maturação, volta para a cadência de nutrição.
   - **< 40** — desqualificado; registrar o motivo para não reabordar sem gatilho novo.
7. Registrar a origem de cada resposta (dito pelo lead vs. inferido pelo SDR) — nunca
   apresentar inferência como fato confirmado.

## Modelo de registro

| Dimensão | Nota (0-25) | Evidência | Fonte (dito/inferido) |
|---|---|---|---|
| Budget | | | |
| Authority | | | |
| Need | | | |
| Timing | | | |
| **Total** | **/100** | | |

## Erros comuns a evitar

- Marcar Authority alta só porque o interlocutor foi simpático ou engajado na conversa.
- Pontuar Need sem diferenciar dor declarada de dor presumida.
- Empurrar lead com nota abaixo de 40 para o Closer só para bater meta de agendamento.

## Usage

```
@sdr
*qualify-lead-bant
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lead_conversation_notes` | string | Yes | notas da conversa com o lead |
| `behavioral_profile` | string | No | behavioral profile |

## Output

- **bant_assessment**: BANT/GPCT assessment
- **purchase_probability_score**: nota de 0-100 com justificativa

## Origin

Confidence: 89%
