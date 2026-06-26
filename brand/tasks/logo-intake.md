# Task: Logo Intake

## Metadata

```yaml
id: logo-intake
name: Logo Brief Collection
executor: wheeler-brand-design
elicit: true
estimated_duration: "10-20 min"
```

**Responsible Executor:** Agent (@wheeler-brand-design)
**Dependencies:** depends_on: `[load-workspace-context]` · enables: `[logo-strategic-direction]` · workflow: `wf-logo-brainstorm`

## Objective

Coletar todas as informações necessárias para o brainstorm de logo: marca, indústria, valores, personalidade, preferências visuais, referências e concorrentes. Produzir um logo-brief.md completo e estruturado.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| brand_name | string | yes | Nome da marca |
| industry | string | yes | Setor/indústria da marca |
| brand_context | string | yes | Contexto de negócio (o que é, para quem) |
| archetype | string | no | Arquétipo definido (se já existir via archetype-consultant) |
| brandbook_path | string | no | Path do brandbook.yaml existente (se houver) |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `logo-brief.md` | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brief.md` | Brief completo para brainstorm de logo |

## Execution Steps

### Step 1: Load Existing Context

- Se `brandbook_path` existir, ler e extrair: propósito, valores, arquétipo, tom de voz, público-alvo
- Se já existir output de `archetype-consultant`, usar como base
- Se não houver contexto prévio, coletar tudo via elicitação

### Step 2: Elicitação — Identidade da Marca

Perguntar ao usuário (agrupar em blocos):

**Bloco 1: Essência**
- Qual a missão/propósito da marca?
- Quais são os 3-5 valores centrais?
- Se a marca fosse uma pessoa, como seria sua personalidade?
- Qual a proposta de valor única (differentiator)?

**Bloco 2: Público e Mercado**
- Quem é o público-alvo? (demografia, psicografia)
- Em qual indústria/categoria atua?
- Quem são os 3 principais concorrentes? (listar URLs se possível)
- Qual o posicionamento desejado? (premium, acessível, disruptivo, etc.)

### Step 3: Elicitação — Preferências Visuais

**Bloco 3: Direção Visual**
- Tem preferência de tipo de logo? (wordmark, ícone, combinação, emblema, abstrato, lettermark)
- Cores preferidas ou cores a EVITAR?
- Tem referências visuais? (logos que admira, mood boards, screenshots)
- Qual o tom visual? (moderno, clássico, minimalista, bold, orgânico, geométrico)

**Bloco 4: Uso e Aplicação**
- Onde o logo será mais usado? (digital, impresso, app, redes sociais)
- Precisa funcionar em tamanho muito pequeno? (favicon, app icon)
- Existe marca existente a ser substituída ou evoluída?
- Há restrições legais ou de marca registrada?

### Step 4: Análise de Concorrentes

- Se URLs fornecidas: analisar estilo visual dos concorrentes
- Mapear padrões visuais do setor (cores dominantes, tipos de logo comuns)
- Identificar oportunidades de diferenciação visual

### Step 5: Compilar Logo Brief

Gerar `logo-brief.md` com todas as seções preenchidas.

---

## Output Template

```markdown
# Logo Brief — {{brand_name}}

**Data:** {{date}}
**Responsável:** @wheeler-brand-design

## 1. Identidade da Marca
- **Missão:** {{mission}}
- **Valores:** {{values}}
- **Personalidade:** {{personality}}
- **Proposta de valor:** {{value_prop}}
- **Arquétipo primário:** {{archetype_primary}}
- **Arquétipo secundário:** {{archetype_secondary}}

## 2. Público e Mercado
- **Público-alvo:** {{target_audience}}
- **Indústria:** {{industry}}
- **Concorrentes:**
  - {{competitor_1}} — {{visual_analysis_1}}
  - {{competitor_2}} — {{visual_analysis_2}}
  - {{competitor_3}} — {{visual_analysis_3}}
- **Posicionamento:** {{positioning}}

## 3. Direção Visual
- **Tipo de logo preferido:** {{logo_type_preference}}
- **Cores preferidas:** {{preferred_colors}}
- **Cores a evitar:** {{avoid_colors}}
- **Tom visual:** {{visual_tone}}
- **Referências:** {{references}}

## 4. Aplicação
- **Uso primário:** {{primary_use}}
- **Necessita favicon/app icon:** {{needs_small}}
- **Marca existente:** {{existing_brand}}
- **Restrições:** {{restrictions}}

## 5. Resumo para Brainstorm
{{executive_summary}}
```

---

## Veto Conditions

- [ ] Usuário não forneceu nome da marca
- [ ] Nenhum contexto de negócio disponível (nem via workspace, nem via elicitação)
- [ ] Brief resultante tem menos de 50% dos campos preenchidos

---

## Handoff

```yaml
to: wheeler-brand-design
task: logo-strategic-direction
pass:
  - logo_brief: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brief.md"
  - brand_name: "{{brand_name}}"
  - archetype: "{{archetype_primary}}"
```
