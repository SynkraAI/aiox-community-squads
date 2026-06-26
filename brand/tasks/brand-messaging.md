---
version: "1.0"
date: "2026-02-28"
author:
  agent: "claude-code"
  squad: "brand"
---

# Brand Messaging — BrandScript & Comunicacao

## Task Definition

| Field | Value |
|-------|-------|
| **ID** | BR_MSG_001 |
| **task_name** | Brand Messaging |
| **status** | pending |
| **responsible_executor** | storybrand-narrator |
| **execution_type** | Agent |
| **complexity** | high |
| **estimated_time** | 45-60min |

## Descricao

Criacao do BrandScript completo usando o framework StoryBrand de Donald Miller. O BrandScript transforma a marca em uma historia clara onde o cliente e o heroi e a marca e o guia. Inclui One-Liner, tagline, elevator pitch e diretrizes de tom de voz.

## Pre-requisitos

- brand-positioning.md concluido (task BR_POS_001) — recomendado
- brand-diagnosis.md concluido (task BR_DIAG_001) — recomendado
- Informacoes basicas do negocio coletadas

## Input

```yaml
brand_messaging_input:
  positioning_doc: "brand-positioning.md"
  diagnosis_doc: "brand-diagnosis.md"
  business_context:
    name: ""
    industry: ""
    target_audience: ""
    main_offer: ""
    competitors: []
  existing_messaging: ""
```

## Output

```yaml
brand_messaging_output:
  report_path: "brand-messaging.md"

  brandscript:
    hero:
      identity: ""
      desire: ""
      internal_problem: ""
      external_problem: ""
      philosophical_problem: ""
    villain: ""
    guide:
      empathy: ""
      authority: ""
    plan:
      step_1: ""
      step_2: ""
      step_3: ""
    call_to_action:
      direct: ""
      transitional: ""
    success:
      description: ""
      transformation: ""
    failure:
      description: ""
      stakes: ""

  one_liner: ""
  tagline: ""
  elevator_pitch: ""

  voice_guidelines:
    tone: ""
    attributes: []
    vocabulary:
      use: []
      avoid: []
    style_rules: []

  messaging_hierarchy:
    primary_message: ""
    secondary_messages: []
    proof_points: []
```

## Action Items

### 1. Coletar Contexto

Reunir informacoes necessarias:
- Quem e o cliente ideal (hero)
- Qual o problema principal que resolve
- O que o cliente quer (desejo)
- O que acontece se nao resolver (stakes)

### 2. Construir o BrandScript

Preencher os 7 elementos do framework SB7:
1. **Hero** — O cliente, nao a marca. Definir desejo claro
2. **Problem** — Externo (tangivel), interno (emocional), filosofico (injustica)
3. **Villain** — O antagonista (pessoa, coisa, sentimento que causa o problema)
4. **Guide** — A marca como guia. Demonstrar empatia + autoridade
5. **Plan** — 3 passos simples para o cliente seguir
6. **Call to Action** — Direto (compre agora) + Transitional (saiba mais)
7. **Success/Failure** — O que muda na vida do cliente (positivo e negativo)

### 3. Criar One-Liner

Formula: [Problema] + [Solucao] + [Resultado]
- Maximo 1 frase
- Claro para qualquer pessoa
- Testavel: "Se alguem perguntar o que voce faz..."

### 4. Criar Tagline

Criterios:
- Memoravel e curta (3-7 palavras ideal)
- Diferenciada dos concorrentes
- Conectada ao BrandScript
- 3 opcoes para escolha

### 5. Criar Elevator Pitch

Versao expandida do One-Liner:
- 30-60 segundos de fala
- Inclui problema, solucao, prova social, CTA
- Tom conversacional

### 6. Definir Diretrizes de Voz

Documentar como a marca fala:
- Tom (formal/informal, tecnico/acessivel)
- Atributos de personalidade na comunicacao
- Vocabulario preferido e proibido
- Regras de estilo (tamanho de frase, uso de jargao, etc.)

### 7. Hierarquia de Mensagens

Organizar mensagens por prioridade:
- Mensagem principal (1 frase)
- Mensagens secundarias (suporte)
- Proof points (evidencias)

### 8. Validacao de Consistencia

Verificar que todos os elementos se conectam:
- BrandScript alinhado com posicionamento
- One-liner reflete o BrandScript
- Tom de voz consistente em todos os assets

## Quality Gate: BR-QG-003

```yaml
quality_gate:
  id: "BR-QG-003"
  name: "Messaging Complete"
  checks:
    - "BrandScript com todos os 7 elementos preenchidos"
    - "Hero definido como cliente (nao a marca)"
    - "3 niveis de problema (externo, interno, filosofico)"
    - "Plan com exatamente 3 passos"
    - "One-liner testavel (problema + solucao + resultado)"
    - "Tagline com 3 opcoes"
    - "Tom de voz com exemplos de do/don't"
    - "Elevator pitch em 30-60 segundos"
```

## Acceptance Criteria

```yaml
acceptance_criteria:
  - "BrandScript completo com 7 elementos SB7"
  - "Hero e o cliente, nao a marca"
  - "Problema tem 3 niveis (externo, interno, filosofico)"
  - "Plan tem exatamente 3 passos claros"
  - "One-liner em 1 frase (problema + solucao + resultado)"
  - "Tagline com pelo menos 3 opcoes"
  - "Elevator pitch de 30-60 segundos"
  - "Tom de voz documentado com exemplos"
  - "brand-messaging.md gerado"
```

## Veto Conditions

```yaml
veto_conditions:
  - "BrandScript sem villain definido = INCOMPLETO"
  - "Hero definido como a marca (nao o cliente) = INCORRETO"
  - "Plan com mais de 3 passos = SIMPLIFICAR"
  - "One-liner com mais de 2 frases = REESCREVER"
  - "Sem exemplos de tom de voz = INCOMPLETO"
  - "Messaging nao conectado ao posicionamento = REVISAR"
```

## Handoff

| Direcao | Agent | Condicao |
|---------|-------|----------|
| **From** | brand-chief (consulting/diagnosis) | Diagnostico e posicionamento concluidos |
| **To** | wheeler-brand-design | Para identidade visual alinhada ao messaging |
| **To** | storybrand-narrator | Para aprofundamento narrativo (storytelling) |
| **To** | brand-chief | Revisao final e entrega ao cliente |

## Error Handling

| Erro | Acao |
|------|------|
| Contexto insuficiente do cliente | Solicitar elicitation com perguntas direcionadas |
| Posicionamento nao definido | Executar brand-positioning.md primeiro ou coletar minimo viavel |
| Cliente confunde hero com marca | Refazer explicacao do framework SB7 |
| One-liner muito longo | Aplicar formula rigida: Problema + Solucao + Resultado |
| Tom de voz inconsistente | Usar brand personality como ancora |

---
*Task: BR_MSG_001 | Agent: storybrand-narrator | Version: 1.0*
