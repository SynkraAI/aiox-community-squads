---
task: "Book Meeting"
responsavel: "@sdr"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - qualified_conversation
  - purchase_probability_score
Saida: |
  - scheduled_meeting
  - handoff_brief
Checklist:
  - "[ ] Confirmar horario, participantes e canal da reuniao"
  - "[ ] Definir e comunicar a agenda da reuniao ao lead"
  - "[ ] Registrar contexto, dores e BANT levantado para o Closer"
  - "[ ] Enviar confirmacao e lembrete antes da reuniao"
  - "[ ] Definir plano de contingencia para no-show"
  - "[ ] Entregar o handoff completo ao Closer antes do horario marcado"
---

# *book-meeting

## Objetivo

Conduzir a conversa qualificada até o agendamento e entregar ao Closer um handoff
completo — não apenas um horário na agenda.

## Procedimento

1. Assim que houver sinal de interesse qualificado (nota BANT ≥ 40 e abertura
   confirmada pelo lead), propor 2-3 opções concretas de horário — nunca "quando você
   tiver disponibilidade".
2. Confirmar duração, formato (call ou presencial) e quem mais deveria participar do
   lado do cliente, com base no que foi levantado em Authority.
3. Definir e comunicar a agenda da reunião em 1-2 linhas do que será tratado — gera
   comprometimento e reduz a taxa de no-show.
4. Registrar o `handoff_brief` com: contexto e gatilho, dores levantadas (separando fato
   de hipótese), resumo do BANT, perfil comportamental identificado (se houver),
   objeções já tratadas na prospecção e a expectativa combinada com o lead.
5. Enviar confirmação por escrito (e-mail ou WhatsApp) imediatamente após marcar, com
   lembrete 24h e 1h antes da reunião.
6. Definir o plano de contingência para no-show: reagendamento automático em até 24h; a
   partir do segundo no-show seguido, desqualificar temporariamente e mover para nutrição.
7. Entregar o handoff ao Closer com a antecedência mínima definida pelo squad (ex.: 30
   minutos antes da reunião) para que ele possa rodar `*plan-discovery-meeting`.

## Estrutura do handoff_brief

```
Lead / Empresa:
Cargo / Autoridade:
Gatilho identificado:
Dores levantadas (fato):
Dores levantadas (hipótese):
BANT resumido (nota e justificativa):
Perfil comportamental (se houver):
Objeções já tratadas:
Expectativa combinada com o lead para a reunião:
```

## Erros comuns a evitar

- Marcar reunião sem confirmar antecipadamente quem decide do lado do cliente.
- Entregar handoff incompleto ou de última hora ao Closer.
- Não ter um plano definido para no-show, tratando cada caso de forma improvisada.

## Usage

```
@sdr
*book-meeting
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `qualified_conversation` | string | Yes | conversa ja qualificada com o lead |
| `purchase_probability_score` | string | Yes | purchase probability score |

## Output

- **scheduled_meeting**: scheduled meeting
- **handoff_brief**: handoff brief para o Closer

## Origin

Confidence: 90%
