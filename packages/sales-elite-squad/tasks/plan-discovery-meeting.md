---
task: "Plan Discovery Meeting"
responsavel: "@closer"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - handoff_brief
  - icp_definition
Saida: |
  - meeting_plan
  - spin_questions
Checklist:
  - "[ ] Revisar o handoff do SDR e o historico do lead"
  - "[ ] Formular hipoteses de dor a validar na reuniao"
  - "[ ] Preparar perguntas SPIN (situacao, problema, implicacao, necessidade)"
  - "[ ] Preparar pergunta Challenger para trazer perspectiva nova"
  - "[ ] Definir o objetivo minimo e o objetivo ideal da reuniao"
  - "[ ] Rodar a sequencia mental de 10 passos do template antes da reuniao"
---

# *plan-discovery-meeting

## Objetivo

Preparar a reunião de descoberta com hipóteses e perguntas prontas — nunca entrar na
call para "conhecer o cliente" sem plano.

## Procedimento

1. Revisar o `handoff_brief` do SDR por completo antes de qualquer preparação: gatilho,
   dores levantadas, BANT, perfil comportamental, objeções já tratadas.
2. Formular de 3 a 5 hipóteses de dor específicas (nunca genéricas) a validar na
   reunião — marcadas como hipótese, nunca apresentadas como fato ao cliente.
3. Montar as perguntas SPIN:
   - **Situação** — confirmar contexto já levantado pelo SDR sem redundância excessiva.
   - **Problema** — expor a dor sem assumir a resposta.
   - **Implicação** — levar o próprio cliente a calcular o custo de não resolver.
   - **Necessidade de solução** — levar o cliente a verbalizar o valor de resolver.
4. Preparar ao menos 1 pergunta Challenger: trazer um dado ou ponto de vista que
   reformula o problema do cliente, ensinando algo que ele ainda não sabia sobre o
   próprio negócio.
5. Definir o objetivo mínimo da reunião (ex.: confirmar BANT e agendar a próxima etapa)
   e o objetivo ideal (ex.: já alinhar critério de decisão e demais stakeholders).
6. Rodar a sequência mental de 10 passos de `templates/opportunity-diagnostic.md` antes
   de entrar na call.

## Banco de perguntas SPIN (exemplo)

| Tipo | Pergunta |
|---|---|
| Situação | "Hoje como vocês fazem {processo relacionado à dor}?" |
| Problema | "O que tem sido mais difícil nesse processo?" |
| Implicação | "Isso impacta {métrica citada pelo cliente} de que forma?" |
| Necessidade | "Se isso estivesse resolvido, o que mudaria pra vocês?" |

## Erros comuns a evitar

- Levar hipótese de dor pronta e tentar confirmá-la a qualquer custo, ignorando sinal
  contrário do cliente.
- Pular perguntas de Implicação e Necessidade e ir direto para o pitch do produto.
- Não ter objetivo mínimo definido, deixando a reunião sem critério de sucesso.

## Usage

```
@closer
*plan-discovery-meeting
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `handoff_brief` | string | Yes | handoff brief recebido do SDR |
| `icp_definition` | string | No | ICP definition |

## Output

- **meeting_plan**: meeting plan
- **spin_questions**: perguntas SPIN e Challenger

## Origin

Confidence: 88%
