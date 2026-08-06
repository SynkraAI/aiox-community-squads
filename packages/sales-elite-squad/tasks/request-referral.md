---
task: "Request Referral"
responsavel: "@customer-success"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - health_score
  - satisfaction_signals
Saida: |
  - referral_request_plan
  - social_proof_assets
Checklist:
  - "[ ] Confirmar que o cliente esta em momento de satisfacao comprovada (nao presumida)"
  - "[ ] Escolher o canal e o momento certo para o pedido (marco de sucesso, NPS alto)"
  - "[ ] Preparar o pedido de indicacao especifico, nao generico"
  - "[ ] Preparar pedido de depoimento ou case como ativo reutilizavel"
  - "[ ] Nunca pedir indicacao a conta com sinal de risco aberto"
  - "[ ] Registrar o resultado do pedido e agradecer independente da resposta"
---

# *request-referral

## Objetivo

Pedir indicação no momento certo, com pedido específico — nunca genérico ou em conta
com relação fragilizada.

## Procedimento

1. Confirmar satisfação comprovada, não presumida — usar NPS alto recente, marco de
   sucesso atingido ou elogio espontâneo do cliente como gatilho, nunca "achismo" do CS.
2. Escolher o canal e o momento certo (logo após um marco de sucesso, ou logo após
   feedback positivo espontâneo) — pedir em momento neutro reduz a taxa de resposta.
3. Preparar um pedido específico (ex.: "conhece outra empresa de {segmento} que sente
   {dor} como vocês sentiam?") em vez de um pedido genérico de indicação.
4. Preparar em paralelo o pedido de depoimento/case como ativo reutilizável, mesmo que o
   cliente não tenha uma indicação imediata disponível.
5. Nunca pedir indicação a conta com sinal de risco aberto em `health_score` — isso
   associa a marca a um pedido em momento de fragilidade da relação.
6. Registrar o resultado do pedido (indicou, não indicou, deu depoimento) e agradecer de
   forma genuína, independentemente da resposta.

## Modelo de pedido

```
Gatilho de satisfação confirmado (NPS/marco/elogio espontâneo):
Canal e momento escolhido:
Pedido específico (segmento/dor a buscar na indicação):
Pedido de depoimento/case (paralelo):
Resultado registrado:
```

## Erros comuns a evitar

- Pedir indicação genérica ("conhece alguém que possa se interessar?") sem direcionar.
- Pedir indicação a conta com ticket de suporte ou risco de churn ainda em aberto.
- Não registrar nem agradecer quando o cliente responde negativamente ao pedido.

## Usage

```
@customer-success
*request-referral
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `health_score` | string | Yes | health score |
| `satisfaction_signals` | string | Yes | sinais de satisfacao do cliente |

## Output

- **referral_request_plan**: referral request plan
- **social_proof_assets**: social proof assets

## Origin

Confidence: 79%
