---
task: "Build Outreach Cadence"
responsavel: "@sdr"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - lead_score_sheet
  - temperature_classification
Saida: |
  - cadence_plan
  - channel_sequence
Checklist:
  - "[ ] Definir numero de toques e intervalo por canal (e-mail, WhatsApp, LinkedIn, telefone)"
  - "[ ] Sequenciar os canais conforme a temperatura do lead"
  - "[ ] Definir gatilho de parada (resposta, reuniao marcada, opt-out)"
  - "[ ] Definir criterio de reciclagem para lead que nao respondeu"
  - "[ ] Validar a cadencia contra a capacidade real do time"
  - "[ ] Publicar a cadencia como playbook reutilizavel por segmento"
---

# *build-outreach-cadence

## Objetivo

Transformar `lead_score_sheet` e `temperature_classification` numa cadência multicanal
documentada — não uma sequência de toques aleatórios.

## Procedimento

1. Classificar o lead por temperatura (fria/morna/quente, vinda de `*score-lead-fit`) —
   a intensidade e a duração da cadência mudam conforme a temperatura:
   - **Quente**: 5-7 toques em 10-14 dias.
   - **Morno**: 8-10 toques em 14-21 dias.
   - **Frio**: 10-14 toques em 21-30 dias.
   (Ajustar os intervalos ao ciclo de venda real do ICP — B2B enterprise pede janelas
   maiores que PME/self-service.)
2. Sequenciar os canais intercalando, nunca repetindo o mesmo canal em toques seguidos:
   - **E-mail** — assíncrono, fica registrado, bom para abrir e para conteúdo mais longo.
   - **LinkedIn** — autoridade e prova social, bom para aquecer antes do primeiro contato direto.
   - **Telefone** — maior taxa de resposta em lead quente, mas mais invasivo em lead frio.
   - **WhatsApp** — só depois de algum sinal de permissão (o lead respondeu em outro
     canal, veio de indicação, ou é prática comum aceita no segmento do ICP).
3. Definir o gatilho de "Dia 0" — o evento que inicia a cadência (entrada na lista
   qualificada, gatilho de compra identificado por `*identify-buying-triggers`).
4. Definir o gatilho de parada: resposta explícita (positiva ou negativa), reunião
   marcada, ou pedido de não contato. Parar imediatamente em qualquer recusa explícita —
   nunca insistir além disso.
5. Definir a regra de reciclagem: lead que completou o ciclo sem resposta entra em
   nutrição de baixa frequência (ex.: 1 toque por mês) ou volta para
   `@commercial-intelligence` reavaliar fit e gatilho.
6. Documentar a cadência como tabela reutilizável (dia, canal, objetivo da mensagem,
   call-to-action) — não como texto solto.

## Modelo de cadência (lead morno, exemplo)

| Dia | Canal | Objetivo da mensagem | CTA |
|---|---|---|---|
| 0 | LinkedIn (conexão) | Aparecer no radar com contexto do gatilho | Nenhum — sem pitch |
| 2 | E-mail 1 | Nomear a dor a partir do gatilho identificado | Pergunta de qualificação leve |
| 5 | Telefone 1 | Validar a dor ao vivo, testar abertura | Agendar 15 min |
| 8 | E-mail 2 (breakup leve) | Trazer um insight/dado novo | Escolha entre 2 horários |
| 12 | LinkedIn (comentário/DM) | Reforçar relevância com prova social | Reabrir a conversa |
| 16 | Telefone 2 / WhatsApp | Última tentativa ativa do ciclo | Sim/não direto |

## Erros comuns a evitar

- Cadência idêntica para todo lead, ignorando temperatura e ICP.
- Dois ou mais toques seguidos no mesmo canal.
- Nenhum critério explícito de quando parar ou reciclar.
- WhatsApp usado como primeiro toque sem sinal de permissão.

## Usage

```
@sdr
*build-outreach-cadence
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lead_score_sheet` | string | Yes | lead score sheet |
| `temperature_classification` | string | Yes | temperature classification |

## Output

- **cadence_plan**: cadence plan
- **channel_sequence**: channel sequence

## Origin

Confidence: 88%
