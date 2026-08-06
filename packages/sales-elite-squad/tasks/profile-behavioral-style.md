---
task: "Profile Behavioral Style"
responsavel: "@sdr"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - lead_signals
Saida: |
  - behavioral_profile
  - communication_recommendation
Checklist:
  - "[ ] Classificar sinais no perfil DISC (dominante, influente, estavel, analitico)"
  - "[ ] Identificar velocidade de resposta e nivel de formalidade"
  - "[ ] Identificar nivel tecnico e nivel executivo do interlocutor"
  - "[ ] Levantar motivador e medo provavel, marcados como hipotese"
  - "[ ] Recomendar tom, ritmo e canal preferencial de comunicacao"
  - "[ ] Marcar explicitamente o que e hipotese versus confirmado pelo proprio lead"
---

# *profile-behavioral-style

## Objetivo

Inferir o perfil comportamental (DISC) e o estilo de comunicação do lead a partir de
sinais indiretos disponíveis, para calibrar tom e canal — sempre como hipótese revisável,
nunca como rótulo definitivo.

## Procedimento

1. Reunir os sinais disponíveis: cargo, conteúdo publicado (LinkedIn), tom e velocidade
   das respostas anteriores, formalidade da linguagem usada pelo lead.
2. Confrontar os sinais com a tabela DISC de `templates/opportunity-diagnostic.md`
   (dominante, influente, estável, analítico) e apontar o perfil com sinais mais fortes —
   nunca forçar um encaixe quando a evidência é fraca.
3. Se os sinais forem insuficientes ou contraditórios, declarar explicitamente "dado
   insuficiente para perfil comportamental" em vez de arriscar uma classificação.
4. Usar cargo como ponto de partida fraco, nunca como regra: C-level tende a
   Dominante/Analítico; Marketing/Comercial tende a Influente; Operações/Financeiro
   tende a Estável/Analítico. Substituir por sinal real assim que houver interação direta.
5. Levantar motivador e medo prováveis associados ao perfil e ao cargo, marcados
   claramente como hipótese.
6. Recomendar tom, ritmo, extensão de mensagem e canal preferencial resultante da leitura.
7. Reavaliar o perfil a cada nova interação direta (call, reunião) — hipótese vira fato
   confirmado ou é descartada e substituída.

## Sinais e leitura rápida

| Sinal observado | Leitura provável |
|---|---|
| Responde rápido, mensagens curtas, vai direto ao ponto | Dominante |
| Publica bastante, tom pessoal e caloroso, menciona relações | Influente |
| Demora para responder, tom cauteloso, evita compromisso rápido | Estável |
| Pede dado, comparação, especificação técnica antes de decidir | Analítico |

## Erros comuns a evitar

- Apresentar o perfil inferido como fato confirmado para o Closer.
- Basear a leitura só no cargo, ignorando o comportamento real observado.
- Não atualizar o perfil depois da primeira interação direta com o lead.

## Usage

```
@sdr
*profile-behavioral-style
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lead_signals` | string | Yes | sinais disponiveis do lead (conteudo publicado, tom de resposta, cargo, historico) |

## Output

- **behavioral_profile**: behavioral profile (DISC + estilo de comunicacao)
- **communication_recommendation**: communication recommendation

## Origin

Confidence: 75%
