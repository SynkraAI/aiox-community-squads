---
task: "Audit Funnel Conversion"
responsavel: "@sales-manager"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - pipeline_data
  - metrics_report
Saida: |
  - conversion_audit
  - improvement_recommendations
Checklist:
  - "[ ] Medir a taxa de conversao entre cada par de estagios consecutivos"
  - "[ ] Comparar a conversao do time contra benchmark interno ou de mercado"
  - "[ ] Identificar se a queda esta na qualificacao, na descoberta ou no fechamento"
  - "[ ] Cruzar queda de conversao com origem do lead (canal, ICP, temperatura)"
  - "[ ] Recomendar ajuste de processo, script ou criterio de qualificacao"
  - "[ ] Priorizar a correcao pelo estagio de maior impacto no forecast"
---

# *audit-funnel-conversion

## Objetivo

Localizar exatamente em qual etapa do funil a conversão está caindo e por quê, para
priorizar a correção de maior impacto.

## Procedimento

1. Calcular a taxa de conversão entre cada par de estágios consecutivos do funil (ex.:
   prospecção → qualificado, qualificado → reunião, reunião → proposta, proposta →
   fechado).
2. Comparar contra benchmark interno (histórico da própria squad) ou de mercado, quando
   disponível.
3. Identificar em qual etapa a queda é mais acentuada: queda entre "reunião" e
   "proposta" aponta para descoberta/qualificação do Closer; queda entre "prospecção" e
   "qualificado" aponta para qualificação do SDR ou para o ICP.
4. Cruzar a queda de conversão com a origem do lead (canal de aquisição, ICP,
   temperatura na entrada) — algumas origens convertem sistematicamente pior e distorcem
   a média geral.
5. Recomendar ajuste concreto: revisão de script, de critério de qualificação, de ICP ou
   de processo de handoff entre `@sdr` e `@closer`.
6. Priorizar a correção pelo estágio de maior impacto no forecast total — não
   necessariamente o de menor taxa de conversão isolada.

## Modelo de auditoria

| Transição de estágio | Taxa atual | Benchmark | Gap | Origem mais afetada | Causa provável | Recomendação |
|---|---|---|---|---|---|---|

## Erros comuns a evitar

- Comparar taxa de conversão sem segmentar por origem do lead, escondendo o real problema.
- Recomendar correção genérica ("melhorar o discurso") sem apontar a etapa exata.
- Priorizar a etapa de pior taxa isolada em vez da etapa de maior impacto no forecast.

## Usage

```
@sales-manager
*audit-funnel-conversion
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pipeline_data` | string | Yes | pipeline data |
| `metrics_report` | string | Yes | metrics report |

## Output

- **conversion_audit**: conversion audit
- **improvement_recommendations**: improvement recommendations

## Origin

Confidence: 82%
