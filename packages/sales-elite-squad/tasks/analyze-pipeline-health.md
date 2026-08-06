---
task: "Analyze Pipeline Health"
responsavel: "@sales-manager"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - pipeline_data
  - historical_conversion_rates
Saida: |
  - pipeline_health_report
  - bottleneck_findings
Checklist:
  - "[ ] Mapear volume e valor de oportunidades por estagio"
  - "[ ] Comparar tempo medio por estagio contra o ciclo historico"
  - "[ ] Identificar estagio com acumulo anormal de oportunidades"
  - "[ ] Identificar oportunidade estagnada alem do ciclo medio"
  - "[ ] Classificar gargalo por severidade (CRITICAL, HIGH, MEDIUM, LOW)"
  - "[ ] Recomendar acao para destravar cada gargalo identificado"
---

# *analyze-pipeline-health

## Objetivo

Diagnosticar a saúde do pipeline por estágio e apontar gargalo concreto — não apenas
descrever números.

## Procedimento

1. Puxar `pipeline_data` organizado por estágio (ex.: prospecção, qualificado,
   descoberta, proposta, negociação, fechado).
2. Para cada estágio, calcular volume (número de deals) e valor total em pipeline.
3. Comparar o tempo médio que os deals levam em cada estágio contra o ciclo histórico
   esperado (`historical_conversion_rates`) — estágio muito acima do normal é gargalo.
4. Identificar acúmulo anormal: estágio com volume desproporcional acumulado indica que
   os deals não estão avançando na velocidade esperada.
5. Listar individualmente as oportunidades estagnadas além do ciclo médio esperado por
   estágio — não basta o agregado, cada deal parado precisa de nome.
6. Classificar cada gargalo por severidade: CRITICAL (trava o forecast do período), HIGH
   (risco relevante ao resultado), MEDIUM/LOW (observação a monitorar).
7. Para cada gargalo, recomendar ação concreta (ex.: revisar critério de qualificação do
   SDR, reforçar objection handling do Closer, escalar deal parado).

## Modelo de relatório

| Estágio | Volume | Valor | Tempo médio vs. histórico | Gargalo (S/N) | Severidade | Ação recomendada |
|---|---|---|---|---|---|---|

## Erros comuns a evitar

- Analisar só o agregado por estágio sem listar os deals individuais estagnados.
- Classificar todo desvio como CRITICAL, perdendo a priorização real.
- Apontar gargalo sem recomendar ação — diagnóstico sem ação não move o pipeline.

## Usage

```
@sales-manager
*analyze-pipeline-health
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pipeline_data` | string | Yes | deals por estagio |
| `historical_conversion_rates` | string | Yes | taxas de conversao historicas |

## Output

- **pipeline_health_report**: pipeline health report
- **bottleneck_findings**: bottleneck findings

## Origin

Confidence: 87%
