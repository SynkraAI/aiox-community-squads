---
task: "Handle Prospecting Objections"
responsavel: "@sdr"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - cadence_plan
  - observed_objections
Saida: |
  - objection_playbook
Checklist:
  - "[ ] Listar as objecoes mais frequentes na fase de prospeccao"
  - "[ ] Escrever resposta consultiva para cada objecao, sem pressao"
  - "[ ] Diferenciar objecao real de desculpa de baixo interesse"
  - "[ ] Definir quando insistir e quando desqualificar o lead"
  - "[ ] Validar cada resposta contra as regras de PNL etica"
  - "[ ] Publicar o playbook para reuso do time"
---

# *handle-prospecting-objections

## Objetivo

Montar o playbook de resposta às objeções mais comuns na fase de prospecção, sem
pressão e sem discurso genérico.

## Procedimento

1. Listar as objeções recorrentes observadas por canal (ex.: "não tenho tempo agora",
   "já temos fornecedor", "manda por e-mail que eu vejo", "não é prioridade agora").
2. Para cada objeção, investigar a raiz antes de responder: ela é real (falta de fit ou
   de timing) ou é reflexo automático de defesa? Testar com uma pergunta aberta antes de
   insistir.
3. Responder com reformulação + valor, nunca com pressão: reconhecer a objeção, trazer
   um ângulo novo (dado, caso análogo, pergunta que reabre a conversa) e propor um
   próximo passo pequeno.
4. Regra específica para "já temos fornecedor": não atacar o concorrente. Perguntar o
   que funciona bem e o que não funciona no fornecedor atual — isso abre espaço real ou
   desqualifica o lead honestamente.
5. Definir um limite de insistência: no máximo 1-2 respostas à mesma objeção antes de
   aceitar um "não" e mover o lead para reciclagem — insistir além disso é o tipo de
   pressão que a PNL ética deste squad proíbe.
6. Validar cada resposta escrita contra as regras de PNL ética do template: nenhuma
   tentativa de fazer o lead se sentir mal por recusar, nenhuma urgência artificial.

## Modelo de objeção → resposta

| Objeção | Diagnóstico provável | Resposta sugerida |
|---|---|---|
| "Não tenho tempo agora" | Prioridade real ou recusa educada | "Entendo. Prefere que eu volte em [data] ou que eu mande 3 linhas por e-mail pra você avaliar quando puder?" |
| "Já temos fornecedor" | Pode haver gap real ou não | "Faz sentido. O que funciona bem hoje com eles e o que você trocaria se pudesse?" |
| "Manda por e-mail" | Pedido genuíno ou forma de encerrar a ligação | "Mando sim. Pra eu não te mandar algo genérico, me conta rapidamente: {pergunta de qualificação}?" |
| "Não é prioridade agora" | Timing real ou dor ainda não percebida | "Entendido. O que precisaria mudar pra isso virar prioridade?" |

## Erros comuns a evitar

- Responder à objeção sem investigar a causa por trás dela.
- Insistir mais de duas vezes na mesma objeção.
- Usar frases que geram culpa ou urgência falsa para reverter o "não".

## Usage

```
@sdr
*handle-prospecting-objections
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cadence_plan` | string | No | cadence plan |
| `observed_objections` | string | Yes | objecoes ja observadas na prospeccao |

## Output

- **objection_playbook**: objection playbook

## Origin

Confidence: 83%
