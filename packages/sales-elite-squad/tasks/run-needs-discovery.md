---
task: "Run Needs Discovery"
responsavel: "@closer"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - meeting_plan
  - live_conversation
Saida: |
  - discovery_findings
  - meddicc_summary
Checklist:
  - "[ ] Confirmar dor real versus dor hipotetica levantada antes da reuniao"
  - "[ ] Levantar orcamento, autoridade, necessidade e urgencia (BANT/MEDDICC)"
  - "[ ] Identificar criterio de decisao e processo de compra do cliente"
  - "[ ] Identificar todos os envolvidos na decisao (economic buyer, influenciador, usuario)"
  - "[ ] Identificar concorrente considerado e criterio de comparacao"
  - "[ ] Registrar tudo separando fato de hipotese"
---

# *run-needs-discovery

## Objetivo

Conduzir a descoberta ao vivo e registrar dor, orçamento, autoridade, urgência e
critério de decisão — separando sempre fato de hipótese.

## Procedimento

1. Abrir a reunião confirmando a agenda já combinada pelo SDR — gera continuidade e
   comprometimento.
2. Validar as hipóteses de dor levantadas no `meeting_plan`; se a dor real divergir da
   hipótese, seguir a dor real e não forçar a hipótese original.
3. Aprofundar BANT/MEDDICC ao vivo:
   - **Metrics** — como o cliente mede sucesso hoje.
   - **Economic buyer** — quem assina o investimento.
   - **Decision criteria** — o que pesa na escolha (preço, risco, integração, suporte).
   - **Decision process** — etapas e prazos internos de aprovação.
   - **Identify pain** — dor real, quantificada sempre que possível.
   - **Champion** — quem, dentro da empresa, vai defender a compra internamente.
4. Mapear todos os envolvidos na decisão além do interlocutor atual, perguntando
   diretamente — nunca presumir que só ele decide.
5. Perguntar sobre concorrente ou alternativa considerada, incluindo "não fazer nada
   agora", e qual é o critério real de comparação usado pelo cliente.
6. Fechar a descoberta resumindo em voz alta o que foi entendido e pedindo confirmação
   explícita do cliente — evita mal-entendido e gera acordo tácito para a próxima etapa.
7. Registrar tudo em `discovery_findings` separando claramente fato (dito pelo cliente)
   de hipótese (interpretação do Closer).

## Estrutura de discovery_findings

```
Dor confirmada (fato):
Dor hipotética ainda não confirmada:
Metrics (como ele mede sucesso):
Economic buyer:
Decision criteria:
Decision process e prazos:
Champion identificado:
Concorrente/alternativa considerada:
Resumo confirmado com o cliente ao final da call:
```

## Erros comuns a evitar

- Aceitar a primeira resposta superficial sem perguntar "por quê" ou "como isso afeta X".
- Não confirmar quem mais participa da decisão, assumindo que o interlocutor decide sozinho.
- Encerrar a call sem resumir e validar o entendimento com o cliente.

## Usage

```
@closer
*run-needs-discovery
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `meeting_plan` | string | Yes | meeting plan |
| `live_conversation` | string | Yes | notas ou transcricao da conversa |

## Output

- **discovery_findings**: discovery findings
- **meddicc_summary**: MEDDICC summary

## Origin

Confidence: 86%
