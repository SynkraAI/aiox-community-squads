---
task: "Write Cold Outreach"
responsavel: "@sdr"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - lead_profile
  - trigger_signals
  - behavioral_profile
Saida: |
  - outreach_messages
Checklist:
  - "[ ] Rodar a sequencia mental de 10 passos do template antes de escrever"
  - "[ ] Referenciar dor ou gatilho especifico do lead na primeira linha"
  - "[ ] Adaptar tom e extensao ao perfil comportamental identificado"
  - "[ ] Escrever call-to-action unico e de baixo atrito por mensagem"
  - "[ ] Evitar jargao de venda generico e promessa nao sustentavel"
  - "[ ] Revisar contra as regras de PNL etica antes de enviar"
---

# *write-cold-outreach

## Objetivo

Escrever a mensagem de um toque específico da cadência (e-mail, WhatsApp, LinkedIn ou
script de ligação), sempre calibrada ao lead — nunca um template genérico disparado em massa.

## Procedimento

1. Antes de escrever, rodar a sequência mental de 10 passos de
   `templates/opportunity-diagnostic.md` (quem é o cliente, cargo, empresa, segmento,
   dores, objetivos, riscos, ganhos, linguagem, estratégia).
2. **E-mail** — estrutura recomendada:
   - Assunto curto e específico (nunca clickbait ou genérico tipo "Parceria").
   - Abertura com o gatilho ou contexto real e verificável (1 linha).
   - Dor nomeada em termos do negócio dele, não do produto vendido.
   - Um insight ou prova relevante (1 linha, sem inflar).
   - CTA de baixo atrito: pergunta sim/não ou escolha entre dois horários — nunca
     "podemos marcar uma call?" solto.
3. **WhatsApp** — mais curto que e-mail, tom conversacional; nunca abrir com link ou
   discurso institucional; usar somente após algum sinal de abertura (conexão aceita,
   resposta anterior em outro canal).
4. **LinkedIn** — quando possível, interagir com o conteúdo do lead antes de conectar;
   mensagem de conexão sem pitch; a segunda mensagem (pós-aceite) traz valor, não pedido.
5. **Script de ligação** — abertura de 10-15s (nome, empresa, motivo específico da
   ligação), pergunta de permissão ("faz sentido eu tomar 2 minutos?"), pergunta de
   qualificação; nunca pitch de produto na primeira ligação.
6. Adaptar tom e extensão ao `behavioral_profile` quando disponível: Dominante → curto e
   direto ao resultado; Analítico → dado e comparação; Influente → tom pessoal,
   entusiasmado, com história; Estável → tom calmo, sem pressão de tempo.
7. Revisar a mensagem final contra as regras de PNL ética do template: nenhuma urgência
   falsa, nenhuma omissão relevante, nenhuma alegação não verificável.

## Modelo de e-mail frio

```
Assunto: {gatilho ou contexto especifico}

Oi {nome},

vi que {gatilho/contexto especifico e verificavel sobre a empresa dele}.

Empresas parecidas com a {empresa} costumam sentir {dor especifica ligada ao gatilho}
nesse momento.

{insight ou prova de 1 linha — dado, resultado de cliente parecido, ou observacao real}

Faz sentido conversarmos 15 minutos {opcao de horario A} ou {opcao de horario B}?
```

## Erros comuns a evitar

- Abrir com apresentação da empresa vendedora em vez do contexto do lead.
- CTA pedindo tempo indefinido ("quando puder", "se tiver interesse").
- Reaproveitar o mesmo texto em canais diferentes sem adaptar tom e extensão.

## Usage

```
@sdr
*write-cold-outreach
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lead_profile` | string | Yes | lead profile |
| `trigger_signals` | string | No | trigger signals |
| `behavioral_profile` | string | No | behavioral profile |

## Output

- **outreach_messages**: outreach messages (e-mail, WhatsApp, LinkedIn, script de ligacao)

## Origin

Confidence: 86%
