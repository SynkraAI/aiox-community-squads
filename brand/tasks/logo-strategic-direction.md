# Task: Logo Strategic Direction

## Metadata

```yaml
id: logo-strategic-direction
name: Generate Strategic Logo Directions
executor: wheeler-brand-design
co_executor: archetype-consultant
elicit: false
estimated_duration: "15-25 min"
```

**Responsible Executor:** Agent (@wheeler-brand-design) com input de @archetype-consultant
**Dependencies:** depends_on: `[logo-intake]` · enables: `[logo-prompt-engineering]` · workflow: `wf-logo-brainstorm`

## Objective

Gerar 3-5 direções conceituais estratégicas para o logo, cada uma com metáfora visual, rationale, shape/color/typography territory. Estas direções guiarão a geração de prompts SCDS na próxima fase.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| logo_brief | file | yes | `logo-brief.md` da fase de intake |
| brand_name | string | yes | Nome da marca |
| archetype | string | yes | Arquétipo primário (do brief ou archetype-consultant) |
| pivot_reason | string | no | Motivo do pivot (se vindo de logo-curate) |
| what_worked | string | no | Elementos visuais que funcionaram (se pivot) |
| what_to_avoid | string | no | Elementos visuais a evitar (se pivot) |
| iteration | number | no | Contador de iteração do workflow (se pivot) |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `logo-concepts.md` | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-concepts.md` | 3-5 direções conceituais com rationale |

## Execution Steps

### Step 1: Análise do Brief

- Ler `logo-brief.md` completamente
- Extrair: valores, personalidade, posicionamento, diferenciadores, público
- Identificar tensões criativas (ex: "inovador MAS confiável", "premium MAS acessível")
- **Se PIVOT:** Incorporar `pivot_reason`, `what_worked`, e `what_to_avoid` para direcionar novas direções. Preservar elementos que funcionaram, evitar os que não funcionaram

### Step 2: Consultar Style Library

- Ler `squads/brand/data/logo-style-library.yaml`
- Extrair visual DNA do arquétipo primário
- Se houver arquétipo secundário, calcular mix 70/30
- Documentar: shape_language, color_territory, typography_feel, style_keywords

### Step 3: Gerar Direções Conceituais

Para cada direção (3-5), definir:

1. **Nome do Conceito** — Título criativo (ex: "Shield of Trust", "Pulse of Innovation")
2. **Metáfora Visual** — O que o logo representará visualmente (ex: "escudo geométrico simbolizando proteção")
3. **Rationale** — Por que esta direção faz sentido para a marca (conectar com valores/posicionamento)
4. **Logo Types Recomendados** — Quais tipos de logo servem esta direção (1-3 tipos)
5. **Shape Territory** — Linguagem de formas específica para esta direção
6. **Color Territory** — Paleta cromática específica
7. **Typography Territory** — Direção tipográfica
8. **Style Keywords** — 5-7 palavras-chave para injetar nos prompts
9. **Mood** — Tom emocional em uma frase
10. **Referências Visuais** — Logos existentes que evocam sensação similar (para calibração, NÃO para cópia)

### Step 4: Diversificação

Garantir que as direções cubram espectro diverso:
- Pelo menos 1 direção conservadora (segura, alinhada com setor)
- Pelo menos 1 direção ousada (diferenciação radical)
- Pelo menos 1 direção intermediária (equilíbrio)
- Variar tipos de logo entre direções (não todas icon, não todas wordmark)
- Variar paletas cromáticas entre direções

### Step 5: Compilar Concepts Document

---

## Output Template

```markdown
# Logo Concepts — {{brand_name}}

**Data:** {{date}}
**Baseado em:** logo-brief.md
**Arquétipo:** {{archetype_primary}} ({{archetype_secondary}})

---

## Direção 1: {{concept_name_1}}

**Metáfora Visual:** {{metaphor_1}}

**Rationale:** {{rationale_1}}

**Logo Types:** {{logo_types_1}}

| Atributo | Direção |
|---|---|
| Shape Territory | {{shapes_1}} |
| Color Territory | {{colors_1}} |
| Typography | {{typography_1}} |
| Style Keywords | {{keywords_1}} |
| Mood | {{mood_1}} |

**Referências Visuais:** {{references_1}}

---

## Direção 2: {{concept_name_2}}
...

## Direção 3: {{concept_name_3}}
...

---

## Matriz Comparativa

| Atributo | Dir. 1 | Dir. 2 | Dir. 3 |
|---|---|---|---|
| Tipo de Logo | {{type_1}} | {{type_2}} | {{type_3}} |
| Tom | {{tone_1}} | {{tone_2}} | {{tone_3}} |
| Risco | {{risk_1}} | {{risk_2}} | {{risk_3}} |
| Diferenciação | {{diff_1}} | {{diff_2}} | {{diff_3}} |

## Recomendação

{{recommendation_summary}}
```

---

## Veto Conditions

- [ ] Menos de 3 direções geradas
- [ ] Todas as direções usam o mesmo tipo de logo
- [ ] Nenhuma direção se conecta com os valores do brief
- [ ] Direções são genéricas demais (aplicáveis a qualquer marca)

---

## Handoff

```yaml
to: wheeler-brand-design
task: logo-prompt-engineering
pass:
  - logo_concepts: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-concepts.md"
  - logo_brief: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brief.md"
  - brand_name: "{{brand_name}}"
```
