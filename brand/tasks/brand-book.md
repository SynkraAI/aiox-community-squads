---
version: "1.0"
date: "2026-02-28"
author:
  agent: "claude-code"
  squad: "brand"
---

# Brand Book — Manual de Marca Completo

## Task Definition

| Field | Value |
|-------|-------|
| **ID** | BR_BOOK_001 |
| **task_name** | Brand Book |
| **status** | pending |
| **responsible_executor** | wheeler-brand-design |
| **execution_type** | Agent |
| **complexity** | high |
| **estimated_time** | 60-90min |

## Descricao

Compilacao do Brand Book completo — documento oficial de guidelines da marca com 7 secoes obrigatorias. Consolida todos os outputs anteriores (diagnostico, posicionamento, messaging, identidade visual) em um unico documento de referencia que qualquer pessoa ou equipe pode usar para aplicar a marca corretamente.

## Pre-requisitos

- brand-identity.md concluido (task BR_ID_001) — obrigatorio
- BrandScript (brand-messaging.md) — obrigatorio
- brand-positioning.md — recomendado

## Input

```yaml
brand_book_input:
  identity_doc: "brand-identity.md"
  messaging_doc: "brand-messaging.md"
  positioning_doc: "brand-positioning.md"
  additional_assets: []
  format: "markdown"
```

## Output

```yaml
brand_book_output:
  report_path: "brand-book.md"

  sections:
    1_foundation:
      brand_story: ""
      mission: ""
      vision: ""
      values: []
      personality: ""
      onlyness_statement: ""
      positioning_statement: ""

    2_logo_system:
      primary_logo: ""
      variations: []
      clear_space: ""
      minimum_size: ""
      backgrounds: ""
      incorrect_usage: []

    3_color_palette:
      primary: []
      secondary: []
      accent: []
      ratios: ""
      combinations: []
      accessibility: ""

    4_typography:
      primary_font: ""
      secondary_font: ""
      hierarchy: ""
      digital_specs: ""
      print_specs: ""

    5_imagery:
      photography_style: ""
      illustration_style: ""
      iconography: ""
      do_list: []
      dont_list: []

    6_touchpoints:
      digital:
        website: ""
        social_media: ""
        email: ""
      print:
        business_card: ""
        stationery: ""
        packaging: ""
      environmental: ""

    7_voice_messaging:
      brand_voice: ""
      voice_attributes: []
      do_say: []
      dont_say: []
      one_liner: ""
      elevator_pitch: ""
      brandscript_summary: ""
```

## Action Items

### 1. Reunir Todos os Artefatos

Carregar e consolidar:
- brand-identity.md (logo, cores, tipografia, fotografia)
- brand-messaging.md (BrandScript, One-Liner, voice)
- brand-positioning.md (Onlyness, posicionamento)
- Assets visuais adicionais

### 2. Secao 1: Foundation

Compilar a base estrategica:
- Historia da marca (origem, por que existe)
- Missao, visao, valores (com descricao de cada valor)
- Personalidade da marca
- Onlyness Statement e Positioning Statement

### 3. Secao 2: Logo System

Documentar o sistema de logo completo:
- Logo principal com contexto de uso
- Todas as variacoes e quando usar cada uma
- Clear space com medidas proporcionais
- Tamanho minimo por midia (digital vs impresso)
- **Minimo 4 exemplos de uso incorreto**

### 4. Secao 3: Color Palette

Documentar paleta completa:
- Cada cor com valores em 4 sistemas: HEX, RGB, CMYK, Pantone
- Proporcao de uso recomendada (60/30/10)
- Combinacoes permitidas e proibidas
- Verificacao de contraste WCAG

### 5. Secao 4: Typography

Documentar sistema tipografico:
- Cada fonte com nome, licenca/link e fallback
- Hierarquia completa com tamanhos, pesos, line-height, letter-spacing
- Especificacoes separadas para digital e impresso

### 6. Secao 5: Imagery

Documentar diretrizes de imagem:
- Estilo fotografico com exemplos de referencia
- Estilo de ilustracao/icones (se aplicavel)
- Do's e don'ts com justificativa

### 7. Secao 6: Touchpoints

Aplicacao pratica em cada ponto de contato:
- Digital: site, redes sociais, email
- Impresso: cartao, papelaria, embalagem
- Ambiental (se aplicavel)

### 8. Secao 7: Voice & Messaging

Compilar diretrizes de comunicacao:
- Tom de voz com atributos
- Exemplos de como falar e como NAO falar
- One-liner e elevator pitch oficiais
- Resumo do BrandScript

### 9. Revisao de Consistencia

Verificar que todas as secoes sao consistentes entre si

## Acceptance Criteria

```yaml
acceptance_criteria:
  - "7 secoes completas (Foundation, Logo, Colors, Typography, Imagery, Touchpoints, Voice)"
  - "Cada secao tem exemplos visuais/praticos"
  - "Logo tem secao de uso incorreto com pelo menos 4 exemplos"
  - "Valores de cor em 4 sistemas (HEX, RGB, CMYK, Pantone)"
  - "Tipografia com hierarquia completa e fallbacks"
  - "Secao de Voice tem exemplos de do/don't com contexto"
  - "Touchpoints tem pelo menos 3 aplicacoes documentadas"
  - "brand-book.md gerado e consolidado"
  - "Documento e autocontido"
```

## Veto Conditions

```yaml
veto_conditions:
  - "Menos de 7 secoes completas = INCOMPLETO"
  - "Secao de logo sem uso incorreto = INCOMPLETO"
  - "Cores sem HEX/RGB/CMYK = INCOMPLETO"
  - "Tipografia sem hierarquia = INCOMPLETO"
  - "brand-identity.md nao concluido = NAO INICIAR"
  - "BrandScript nao concluido = NAO INICIAR"
```

## Handoff

| Direcao | Agent | Condicao |
|---------|-------|----------|
| **From** | wheeler-brand-design (brand-identity) | Identidade visual concluida |
| **From** | storybrand-narrator (brand-messaging) | Messaging concluido |
| **To** | brand-chief | Revisao final e entrega ao cliente |

## Error Handling

| Erro | Acao |
|------|------|
| brand-identity.md incompleto | Listar gaps e retornar para task BR_ID_001 |
| BrandScript incompleto | Listar elementos faltantes e retornar para task BR_MSG_001 |
| Inconsistencia entre secoes | Priorizar brand-identity como fonte de verdade visual |
| Formato PDF solicitado | Gerar markdown primeiro, converter como etapa separada |

---
*Task: BR_BOOK_001 | Agent: wheeler-brand-design | Version: 1.0*
