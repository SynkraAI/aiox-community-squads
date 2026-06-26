---
version: "1.0"
date: "2026-02-28"
author:
  agent: "claude-code"
  squad: "brand"
---

# Brand Identity — Identidade Visual Completa

## Task Definition

| Field | Value |
|-------|-------|
| **ID** | BR_ID_001 |
| **task_name** | Brand Identity |
| **status** | pending |
| **responsible_executor** | wheeler-brand-design |
| **execution_type** | Agent |
| **complexity** | high |
| **estimated_time** | 60-90min |

## Descricao

Criacao da identidade visual completa da marca em 5 fases: pesquisa visual, conceito criativo, sistema de logo, paleta de cores + tipografia, e sistema de imagem. Segue a metodologia de Alina Wheeler (Designing Brand Identity) adaptada para execucao por agentes.

## Pre-requisitos

- brand-positioning.md concluido (task BR_POS_001) — obrigatorio
- brand-messaging.md concluido (task BR_MSG_001) — recomendado
- Briefing visual do cliente — recomendado

## Input

```yaml
brand_identity_input:
  positioning_doc: "brand-positioning.md"
  messaging_doc: "brand-messaging.md"
  brandscript: "" # BrandScript do storybrand-narrator
  business_context:
    name: ""
    industry: ""
    personality: ""
    target_audience: ""
    competitors: []
  visual_preferences:
    styles: [] # moderno, classico, minimalista, etc.
    colors_liked: []
    colors_disliked: []
    references: [] # marcas que admira visualmente
  existing_assets:
    has_logo: false
    has_colors: false
    has_typography: false
```

## Output

```yaml
brand_identity_output:
  report_path: "brand-identity.md"

  phase_1_research:
    visual_audit: ""
    competitor_visual_analysis: []
    mood_board_description: ""
    design_principles: []

  phase_2_concept:
    creative_concept: ""
    concept_rationale: ""
    visual_metaphors: []
    design_direction: ""

  phase_3_logo:
    primary_logo:
      description: ""
      concept: ""
      type: "" # wordmark, lettermark, symbol, combination, emblem
    variations:
      horizontal: ""
      vertical: ""
      icon_only: ""
      monochrome: ""
      reversed: ""
    clear_space: ""
    minimum_size: ""
    incorrect_usage: []

  phase_4_color_typography:
    color_palette:
      primary:
        - name: ""
          hex: ""
          rgb: ""
          cmyk: ""
          pantone: ""
      secondary: []
      accent: []
      neutral: []
      ratios: "60/30/10"
      accessibility: ""
    typography:
      primary_font:
        name: ""
        weight: ""
        usage: ""
        fallback: ""
        license: ""
      secondary_font:
        name: ""
        weight: ""
        usage: ""
        fallback: ""
        license: ""
      hierarchy:
        h1: ""
        h2: ""
        h3: ""
        body: ""
        caption: ""

  phase_5_imagery:
    photography_style: ""
    illustration_style: ""
    iconography_style: ""
    image_treatment: ""
    do_list: []
    dont_list: []
```

## Action Items

### Fase 1: Pesquisa Visual (Research)

Analisar o contexto visual:
- **Auditoria visual** do mercado/industria
- Analise visual dos concorrentes (o que funciona, o que e generico)
- Descricao de mood board conceitual
- Definir principios de design (3-5 principios que guiam todas as decisoes)

### Fase 2: Conceito Criativo (Concept)

Desenvolver a direcao criativa:
- Conceito central que conecta estrategia (posicionamento) com visual
- Racional do conceito (por que essa direcao)
- Metaforas visuais que traduzem a personalidade da marca
- Direcao de design aprovada antes de prosseguir

### Fase 3: Sistema de Logo (Logo System)

Criar o sistema completo:
- Logo principal com descricao detalhada e conceito por tras
- Tipo de logo (wordmark, lettermark, symbol, combination, emblem)
- Todas as variacoes necessarias (horizontal, vertical, icone, monocromatico, reverso)
- Regras de clear space (proporcional ao elemento do logo)
- Tamanho minimo por midia
- **Minimo 4 exemplos de uso incorreto** com explicacao

### Fase 4: Cores e Tipografia

Definir paleta e sistema tipografico:

**Cores:**
- Cada cor com valores em 4 sistemas: HEX, RGB, CMYK, Pantone
- Categorias: primaria, secundaria, accent, neutros
- Proporcao de uso (60/30/10)
- Verificacao de contraste WCAG AA/AAA
- Combinacoes permitidas e proibidas

**Tipografia:**
- Fonte primaria e secundaria com licenca/link
- Hierarquia completa (H1-H3, body, caption)
- Especificacoes: tamanho, peso, line-height, letter-spacing
- Fallbacks para cada fonte
- Diferencas digital vs impresso (se aplicavel)

### Fase 5: Sistema de Imagem

Definir diretrizes de imagem:
- Estilo fotografico (iluminacao, composicao, tratamento)
- Estilo de ilustracao (se aplicavel)
- Estilo de iconografia (outline, filled, duotone, etc.)
- Tratamento de imagem (filtros, overlay, crop)
- Do's e don'ts com justificativa clara

## Quality Gate: BR-QG-004

```yaml
quality_gate:
  id: "BR-QG-004"
  name: "Brand Identity Review"
  checks:
    - "5 fases completas (Research, Concept, Logo, Colors/Type, Imagery)"
    - "Logo tem conceito conectado ao posicionamento"
    - "Minimo 4 exemplos de uso incorreto do logo"
    - "Cores em 4 sistemas (HEX, RGB, CMYK, Pantone)"
    - "Contraste WCAG verificado"
    - "Tipografia com hierarquia e fallbacks"
    - "Sistema de imagem com do/don't"
    - "Principios de design definidos e aplicados"
    - "Conceito criativo tem racional documentado"
```

## Acceptance Criteria

```yaml
acceptance_criteria:
  - "5 fases completas e documentadas"
  - "Logo principal com conceito e racional"
  - "Todas as variacoes de logo documentadas"
  - "Minimo 4 usos incorretos do logo"
  - "Paleta com cores em HEX, RGB, CMYK, Pantone"
  - "Proporcao de uso definida (60/30/10)"
  - "Contraste WCAG AA verificado"
  - "Tipografia com hierarquia completa"
  - "Fontes com fallbacks e licencas"
  - "Sistema de imagem com do/don't"
  - "brand-identity.md gerado"
```

## Veto Conditions

```yaml
veto_conditions:
  - "Logo sem conceito/racional = INCOMPLETO"
  - "Cores sem HEX/RGB/CMYK = INCOMPLETO"
  - "Sem variacoes de logo = INCOMPLETO"
  - "Sem uso incorreto do logo = INCOMPLETO"
  - "Tipografia sem hierarquia = INCOMPLETO"
  - "Sem principios de design = INCOMPLETO"
  - "brand-positioning.md nao concluido = NAO INICIAR"
```

## Handoff

| Direcao | Agent | Condicao |
|---------|-------|----------|
| **From** | storybrand-narrator (brand-messaging) | Messaging concluido para alinhar visual |
| **From** | brand-chief (positioning) | Posicionamento aprovado |
| **To** | wheeler-brand-design (brand-book) | Para compilacao do Brand Book |
| **To** | brand-chief | Revisao final e entrega ao cliente |

## Error Handling

| Erro | Acao |
|------|------|
| Posicionamento nao definido | Retornar para brand-positioning.md (obrigatorio) |
| BrandScript ausente | Prosseguir com posicionamento; recomendar storybrand-narrator |
| Preferencias visuais nao coletadas | Usar elicitation para coletar antes de iniciar |
| Conceito rejeitado pelo usuario | Voltar para Fase 2 com novo approach |
| Fonte nao disponivel/licenca restrita | Sugerir alternativa gratuita equivalente |

---
*Task: BR_ID_001 | Agent: wheeler-brand-design | Version: 1.0*
