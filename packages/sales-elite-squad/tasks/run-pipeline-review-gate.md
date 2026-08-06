---
task: "Run Pipeline Review Gate"
responsavel: "@sales-manager"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - pipeline_health_report
  - sales_forecast
  - conversion_audit
Saida: |
  - verdict
  - findings
  - documented_debt
Checklist:
  - "[ ] Verificar que todo deal comitado tem BANT/MEDDICC documentado"
  - "[ ] Verificar que nao ha gargalo CRITICAL sem plano de acao"
  - "[ ] Verificar que o forecast tem nivel de confianca justificado"
  - "[ ] Classificar cada achado como CRITICAL, HIGH, MEDIUM ou LOW"
  - "[ ] Emitir FAIL se houver achado CRITICAL ou HIGH no forecast do periodo"
  - "[ ] Registrar achados MEDIUM e LOW como debito documentado"
---

# *run-pipeline-review-gate

## Objetivo

Consolidar saúde do pipeline, forecast e auditoria de conversão num verdict único —
FAIL bloqueia o forecast do período até que os achados críticos sejam tratados.

## Procedimento

1. Cruzar `pipeline_health_report`, `sales_forecast` e `conversion_audit` numa visão
   única do período.
2. Verificar que todo deal incluído no forecast comitado tem BANT/MEDDICC documentado
   pelo `@closer` — sem isso, é achado.
3. Verificar que nenhum gargalo classificado como CRITICAL em `*analyze-pipeline-health`
   está sem plano de ação atribuído.
4. Verificar que o forecast tem nível de confiança justificado, não apenas um número
   solto sem racional.
5. Classificar cada achado por severidade (CRITICAL, HIGH, MEDIUM, LOW), seguindo o
   mesmo padrão de gate usado por `@customer-success` (`*run-churn-risk-gate`).
6. Emitir **FAIL** se houver qualquer achado CRITICAL ou HIGH sem tratamento — isso
   bloqueia o forecast do período até resolução.
7. Registrar achados MEDIUM e LOW como débito documentado, não como bloqueio.

## Modelo de verdict

```
Verdict: PASS / FAIL
Achados CRITICAL: [lista, com plano de ação de cada]
Achados HIGH: [lista, com plano de ação de cada]
Débito documentado (MEDIUM/LOW): [lista]
```

## Erros comuns a evitar

- Emitir PASS com achado CRITICAL "porque o time está confiante" sem evidência.
- Deixar achado HIGH sem plano de ação atribuído a alguém específico.
- Rodar o gate sem revisar os três relatórios de entrada de forma integrada.

## Usage

```
@sales-manager
*run-pipeline-review-gate
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pipeline_health_report` | string | Yes | pipeline health report |
| `sales_forecast` | string | Yes | sales forecast |
| `conversion_audit` | string | No | conversion audit |

## Output

- **verdict**: PASS ou FAIL
- **findings**: findings classificados por severidade
- **documented_debt**: debito documentado (achados MEDIUM/LOW)

## Origin

Confidence: 91%
