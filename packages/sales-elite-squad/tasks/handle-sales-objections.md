---
task: "Handle Sales Objections"
responsavel: "@closer"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - discovery_findings
  - roi_case
  - observed_objections
Saida: |
  - objection_response_playbook
Checklist:
  - "[ ] Listar objecoes tipicas de preco, prazo, concorrente e prioridade interna"
  - "[ ] Investigar a objecao antes de responder (e preco ou e outra coisa?)"
  - "[ ] Responder com dado, caso analogo ou reformulacao, nunca com pressao"
  - "[ ] Diferenciar objecao de decisor de objecao de influenciador"
  - "[ ] Definir quando trazer o Gestor Comercial para apoiar a negociacao"
  - "[ ] Validar cada resposta contra as regras de PNL etica"
---

# *handle-sales-objections

## Objetivo

Montar o roteiro de resposta às objeções de fechamento com base em dado e reformulação
— nunca em pressão ou desconto reflexo.

## Procedimento

1. Mapear as objeções mais comuns nesta fase: preço ("está caro"), prazo ("não é o
   momento"), concorrente ("estamos vendo outra opção"), prioridade interna ("temos
   outros projetos primeiro"), confiança ("como sabemos que funciona").
2. Antes de responder, investigar a raiz da objeção: "quando você diz que está caro, é
   caro comparado a quê?" — quase toda objeção de preço esconde uma dúvida de valor,
   orçamento ou prioridade, não o preço em si.
3. Responder com dado (o `roi_case` já construído), caso análogo (cliente parecido com
   resultado real) ou reformulação (reconectar com a dor e o custo de não agir) — nunca
   com desconto reflexo ou pressão de tempo artificial.
4. Diferenciar objeção do decisor (peso real, exige resposta robusta e dado) de objeção
   do influenciador (pode precisar só de mais informação para levar adiante internamente).
5. Definir o gatilho para acionar o `@sales-manager`: objeção de preço em conta
   estratégica, objeção que exige aprovação de exceção comercial, ou negociação travada
   há mais de um número de dias definido pelo squad.
6. Validar cada resposta contra a regra de PNL ética: reformular para gerar clareza,
   nunca para neutralizar a objeção por manipulação ou omissão.

## Modelo de objeção → resposta

| Objeção | Investigação | Resposta |
|---|---|---|
| "Está caro" | Caro comparado a quê? Falta de orçamento ou de valor percebido? | Voltar ao `roi_case`: "Comparado ao custo de {dor quantificada}, o payback é de {X meses}." |
| "Não é o momento" | Timing real ou objeção disfarçada de outra coisa? | "O que precisaria ser diferente pra ser o momento certo?" |
| "Vendo outra opção" | Qual critério está sendo usado pra comparar? | "O que mais pesa nessa comparação pra você?" |
| "Temos outros projetos primeiro" | Prioridade real ou dor ainda não urgente pro decisor? | Reforçar a implicação levantada na descoberta (custo de adiar). |

## Erros comuns a evitar

- Oferecer desconto como primeira resposta a uma objeção de preço.
- Tratar objeção de influenciador com o mesmo peso de objeção do economic buyer.
- Responder sem investigar, assumindo que já sabe qual é a objeção real.

## Usage

```
@closer
*handle-sales-objections
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `discovery_findings` | string | Yes | discovery findings |
| `roi_case` | string | No | ROI case |
| `observed_objections` | string | Yes | objecoes ja observadas na negociacao |

## Output

- **objection_response_playbook**: objection response playbook

## Origin

Confidence: 85%
