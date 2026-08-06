---
task: "Coach Sales Rep"
responsavel: "@sales-manager"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - call_or_meeting_transcript
  - rep_performance_history
Saida: |
  - coaching_plan
  - skill_gap_findings
Checklist:
  - "[ ] Avaliar a conversa contra a metodologia adotada (SPIN, Challenger, MEDDICC)"
  - "[ ] Identificar o que funcionou e deve ser reforcado"
  - "[ ] Identificar lacuna especifica de habilidade, nao julgamento generico"
  - "[ ] Definir de uma a tres acoes praticas de melhoria, priorizadas"
  - "[ ] Definir prazo e forma de acompanhamento da evolucao"
  - "[ ] Registrar o coaching de forma construtiva e documentada"
---

# *coach-sales-rep

## Objetivo

Transformar uma conversa real em plano de coaching específico e construtivo — nunca
julgamento genérico sobre o vendedor.

## Procedimento

1. Ouvir ou ler a transcrição completa da ligação/reunião antes de formar qualquer
   opinião — não julgar pelo resultado (fechou ou não) sem ver a condução.
2. Avaliar a condução contra a metodologia adotada pela squad (SPIN na descoberta,
   Challenger no reframe, MEDDICC no mapeamento) — não contra preferência pessoal do gestor.
3. Identificar o que funcionou bem e merece reforço explícito — coaching que só aponta
   erro desmotiva e não fixa o que já é bom.
4. Identificar de 1 a 3 lacunas específicas e observáveis (ex.: "não perguntou sobre
   decision process", "aceitou a primeira objeção sem investigar a raiz") — nunca
   julgamento genérico como "precisa ser mais assertivo".
5. Definir ações práticas de melhoria, priorizadas pela de maior impacto no resultado.
6. Definir prazo e forma de acompanhamento (ex.: revisar a próxima call do mesmo rep em
   2 semanas usando o mesmo checklist de avaliação).
7. Registrar o coaching de forma construtiva e documentada, acessível ao próprio rep —
   coaching não registrado não gera evolução rastreável.

## Modelo de coaching

```
O que funcionou bem (reforçar):
Lacuna 1 (observável, com trecho da conversa):
Lacuna 2:
Lacuna 3:
Ação prática de melhoria (priorizada):
Prazo de acompanhamento:
```

## Erros comuns a evitar

- Dar feedback só sobre o resultado do deal, ignorando a qualidade da condução.
- Listar mais de 3 lacunas de uma vez, diluindo o foco do rep.
- Não definir prazo de acompanhamento, deixando o coaching sem continuidade.

## Usage

```
@sales-manager
*coach-sales-rep
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_or_meeting_transcript` | string | Yes | transcricao ou notas da ligacao/reuniao |
| `rep_performance_history` | string | No | historico de performance do vendedor |

## Output

- **coaching_plan**: coaching plan
- **skill_gap_findings**: skill gap findings

## Origin

Confidence: 78%
