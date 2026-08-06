---
task: "Plan Onboarding"
responsavel: "@customer-success"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - deal_terms
  - customer_profile
Saida: |
  - onboarding_plan
  - value_milestones
Checklist:
  - "[ ] Definir o primeiro valor que o cliente precisa sentir e em quanto tempo"
  - "[ ] Mapear marcos de onboarding com responsavel e prazo"
  - "[ ] Definir criterio objetivo de 'onboarding concluido'"
  - "[ ] Alinhar expectativa com o que foi vendido pelo Closer (evitar gap)"
  - "[ ] Definir ponto de contato e cadencia de acompanhamento inicial"
  - "[ ] Registrar risco identificado logo na entrada do cliente"
---

# *plan-onboarding

## Objetivo

Planejar o onboarding a partir do que foi realmente vendido, com marco de valor
definido — não um checklist genérico de "reuniões feitas".

## Procedimento

1. Revisar `deal_terms` e o que foi efetivamente prometido por `@closer` durante a
   venda — o onboarding começa alinhando expectativa, não a partir de um template solto.
2. Definir qual é o "primeiro valor" (first value) que o cliente precisa sentir, e em
   quanto tempo (ex.: "primeiro relatório útil gerado em até 7 dias").
3. Mapear os marcos de onboarding em ordem, cada um com responsável (cliente ou
   fornecedor) e prazo definido.
4. Definir o critério objetivo de "onboarding concluído" (ex.: X usuários ativos, Y
   funcionalidade em uso, marco de valor atingido) — nunca "reuniões realizadas" como
   critério de conclusão.
5. Confirmar que a expectativa combinada no onboarding bate com o que foi vendido — se
   houver gap, tratar antes de avançar, não depois que o cliente perceber sozinho.
6. Definir o ponto de contato principal do cliente e a cadência de acompanhamento nas
   primeiras semanas.
7. Registrar qualquer risco já identificado na entrada (ex.: baixo engajamento do time
   do cliente, expectativa desalinhada) para monitorar desde o início em
   `*monitor-customer-health`.

## Modelo de plano

```
Primeiro valor esperado e prazo:
Marco 1 — responsável — prazo:
Marco 2 — responsável — prazo:
Marco 3 — responsável — prazo:
Critério objetivo de "onboarding concluído":
Ponto de contato e cadência de acompanhamento:
Risco identificado na entrada:
```

## Erros comuns a evitar

- Usar o mesmo plano de onboarding padrão sem checar o que foi especificamente vendido.
- Definir "concluído" por atividade realizada em vez de valor efetivamente atingido.
- Ignorar gap entre o vendido e o combinado no onboarding, empurrando o problema pra frente.

## Usage

```
@customer-success
*plan-onboarding
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deal_terms` | string | Yes | termos do acordo fechado |
| `customer_profile` | string | Yes | perfil do cliente |

## Output

- **onboarding_plan**: onboarding plan
- **value_milestones**: value milestones

## Origin

Confidence: 87%
