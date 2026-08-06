---
task: "Run Churn Risk Gate"
responsavel: "@customer-success"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - health_score
  - risk_signals
  - renewal_strategy
Saida: |
  - verdict
  - findings
  - documented_debt
Checklist:
  - "[ ] Verificar que toda conta com risco alto tem plano de acao registrado"
  - "[ ] Verificar que o marco de valor do onboarding foi de fato atingido"
  - "[ ] Verificar que a renovacao proxima tem estrategia documentada"
  - "[ ] Classificar cada achado como CRITICAL, HIGH, MEDIUM ou LOW"
  - "[ ] Emitir FAIL se houver achado CRITICAL ou HIGH sem plano de resgate"
  - "[ ] Registrar achados MEDIUM e LOW como debito documentado"
---

# *run-churn-risk-gate

## Objetivo

Consolidar health score, sinais de risco e estratégia de renovação num verdict único —
FAIL aciona plano de resgate imediato, não espera o próximo ciclo de revisão.

## Procedimento

1. Cruzar `health_score`, `risk_signals` e `renewal_strategy` para todas as contas em
   janela de risco.
2. Verificar que toda conta classificada com risco alto tem um plano de ação registrado
   e responsável definido — risco sem plano é achado.
3. Verificar que o marco de valor definido em `*plan-onboarding` foi de fato atingido
   para cada conta — "onboarding concluído" sem marco de valor real é achado.
4. Verificar que toda conta com renovação próxima tem estratégia documentada em
   `*plan-renewal` — não apenas "vamos conversar quando chegar a hora".
5. Classificar cada achado por severidade (CRITICAL, HIGH, MEDIUM, LOW), seguindo o
   mesmo padrão de gate usado por `@sales-manager` (`*run-pipeline-review-gate`).
6. Emitir **FAIL** se houver achado CRITICAL ou HIGH sem plano de resgate — isso aciona
   ação imediata, não espera o próximo ciclo de revisão.
7. Registrar achados MEDIUM e LOW como débito documentado.

## Modelo de verdict

```
Verdict: PASS / FAIL
Contas com risco CRITICAL sem plano: [lista]
Contas com risco HIGH sem plano: [lista]
Débito documentado (MEDIUM/LOW): [lista]
```

## Erros comuns a evitar

- Emitir PASS para conta com risco alto só porque a renovação ainda está distante.
- Não cruzar o marco de valor real do onboarding, aceitando "concluído" de nome.
- Deixar achado CRITICAL registrado sem acionar o plano de resgate no mesmo ciclo.

## Usage

```
@customer-success
*run-churn-risk-gate
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `health_score` | string | Yes | health score |
| `risk_signals` | string | Yes | risk signals |
| `renewal_strategy` | string | No | renewal strategy |

## Output

- **verdict**: PASS ou FAIL
- **findings**: findings classificados por severidade
- **documented_debt**: debito documentado (achados MEDIUM/LOW)

## Origin

Confidence: 90%
