---
task: "Recover Lost Opportunity"
responsavel: "@closer"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - lost_or_stalled_opportunity_data
Saida: |
  - recovery_plan
  - lessons_learned
Checklist:
  - "[ ] Identificar o motivo real da perda ou da estagnacao (nunca supor)"
  - "[ ] Classificar a perda como preco, timing, fit, concorrente ou processo interno"
  - "[ ] Definir gatilho e cadencia de reativacao futura, se fizer sentido"
  - "[ ] Registrar o aprendizado para a Inteligencia Comercial e o SDR ajustarem ICP/abordagem"
  - "[ ] Manter a porta aberta com mensagem de relacionamento, nao de pressao"
  - "[ ] Comunicar a perda ao Gestor Comercial para o forecast"
---

# *recover-lost-opportunity

## Objetivo

Entender a causa real de uma oportunidade perdida ou estagnada e definir se, quando e
como reabrir a conversa — sem pressão e sem enterrar aprendizado.

## Procedimento

1. Nunca assumir o motivo da perda — perguntar diretamente ao lead/cliente sempre que
   possível: "o que pesou mais na decisão?".
2. Classificar a causa real: preço (fora da realidade do orçamento), timing (não era o
   momento certo agora), fit de produto (não resolvia o problema real), concorrente
   ganhou, ou processo interno travou (não decidiram nada, silêncio).
3. Se a causa foi timing ou processo interno (não foi um "não" definitivo), definir uma
   cadência de reativação futura com gatilho claro (ex.: revisitar em 6 meses, ou assim
   que um novo gatilho de compra for identificado por `@commercial-intelligence`).
4. Se a causa foi fit ou preço fora da realidade do ICP, registrar isso como aprendizado
   para `@commercial-intelligence` ajustar o critério de ICP ou para `@sdr` ajustar a
   qualificação futura.
5. Encerrar a conversa com mensagem de relacionamento — agradecimento e disposição a
   ajudar no futuro — nunca com tom de cobrança ou última tentativa de pressão.
6. Comunicar a perda ao `@sales-manager` com a causa já classificada, para entrar no
   forecast e nas métricas de conversão do funil.

## Estrutura de recovery_plan

```
Causa real da perda (confirmada pelo cliente, quando possível):
Classificação (preço / timing / fit / concorrente / processo interno):
É recuperável? Sob qual gatilho ou prazo?
Aprendizado a repassar (ICP, qualificação, script, oferta):
```

## Erros comuns a evitar

- Registrar a perda com causa genérica ("não deu certo") sem investigar.
- Insistir em reabrir a conversa sem um gatilho novo real.
- Não repassar o aprendizado para quem pode corrigir o processo a montante (ICP, SDR).

## Usage

```
@closer
*recover-lost-opportunity
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lost_or_stalled_opportunity_data` | string | Yes | dados da oportunidade perdida ou estagnada |

## Output

- **recovery_plan**: recovery plan
- **lessons_learned**: lessons learned

## Origin

Confidence: 80%
