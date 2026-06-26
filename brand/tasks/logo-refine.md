# Task: Logo Refinement (Cross-Squad Bridge)

## Metadata

```yaml
id: logo-refine
name: Refine Selected Logo Concept
executor: nano-banana-generator
elicit: false
estimated_duration: "15-25 min"
cross_squad: true
source_squad: brand
target_squad: design
```

**Responsible Executor:** Agent (@nano-banana-generator) from Design Squad
**Dependencies:** depends_on: `[logo-curate]` · enables: `[logo-deliverable]` · workflow: `wf-logo-brainstorm`

## Objective

Aplicar o framework PRIO (Prompt Refinement & Iteration Optimization) no conceito de logo aprovado, gerando 5-8 variações refinadas em resolução 2K. Foca nos ajustes específicos do feedback de curação.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| selected_direction | string | yes | ID da direção conceitual selecionada |
| selected_images | list | yes | Paths das imagens base selecionadas |
| refinement_notes | string | yes | Feedback específico do que ajustar |
| brand_name | string | yes | Nome da marca |
| prompt_brief | file | yes | `logo-prompt-brief.yaml` para referência do prompt original |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| Refined images | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/refinements/` | 5-8 variações refinadas |
| Refinement log | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/refinement-log.yaml` | Log PRIO completo |

## Execution Steps

### Step 1: Analyze Source

- Ler imagens base selecionadas
- Ler prompt original do `logo-prompt-brief.yaml` para a direção selecionada
- Ler feedback de refinamento do `curation-report.md`
- Categorizar ajustes solicitados:
  - **Compositional:** layout, balance, spacing
  - **Chromatic:** cor, saturação, contraste
  - **Stylistic:** estilo, mood, acabamento
  - **Typographic:** fonte, peso, espaçamento (se wordmark/combination)
  - **Semantic:** metáfora, conceito, significado

### Step 2: Apply PRIO Framework

Executar 2-3 ciclos PRIO (via `prompt-refine` task):

**Ciclo 1: Ajuste Primário**
- Variável: O ajuste mais impactante do feedback
- Gerar 3 variações
- Resolução: 2K
- Selecionar melhor

**Ciclo 2: Ajuste Secundário**
- Variável: Segundo ajuste do feedback
- Partir do melhor do Ciclo 1
- Gerar 3 variações
- Selecionar melhor

**Ciclo 3 (se necessário): Polish**
- Variável: Refinamento fino (detalhe, cor exata, proporção)
- Partir do melhor do Ciclo 2
- Gerar 2-3 variações finais

### Step 3: Generate Final Variations

Com o prompt refinado dos ciclos PRIO, gerar variações finais:
- 5-8 variações com pequenas mudanças (cor, composição, peso)
- Resolução: 2K
- Usar modelo `gemini-3-pro-image-preview` para máxima qualidade
- Salvar em `refinements/`

### Step 4: Create Refinement Log

```yaml
# Refinement Log — {{brand_name}}
refinement_session:
  id: "{{session_id}}"
  timestamp: "{{ISO-8601}}"
  brand_name: "{{brand_name}}"
  selected_direction: "{{direction_id}}"
  source_images: ["{{img_1}}", "{{img_2}}"]
  feedback_applied: "{{refinement_notes}}"
  model_used: "gemini-3-pro-image-preview"

prio_cycles:
  - cycle: 1
    variable: "{{var}}"
    hypothesis: "{{hyp}}"
    variations_generated: {{n}}
    best_variation: "{{path}}"
    improvement_score: {{score}}
    learning: "{{learning}}"

  - cycle: 2
    ...

final_variations:
  total: {{n}}
  files:
    - path: "refinements/{{filename}}.png"
      prompt: "{{prompt}}"
      variation_axis: "{{what_changed}}"

  recommended_top_3:
    - "{{path_1}}"
    - "{{path_2}}"
    - "{{path_3}}"
```

---

## Failure Handling

- **No improvement after PRIO:** Document what was tried, present best available
- **API failures:** Use `prompt-refine` task recovery procedures
- **Quality below source:** Revert to source images, try different refinement approach

## Veto Conditions

- [ ] No source images provided
- [ ] Refinement feedback is empty/unclear
- [ ] All refined images are worse than source

---

## Handoff

```yaml
to: wheeler-brand-design
task: logo-deliverable
squad: brand
protocol: cross-squad-return
pass:
  - refinements_dir: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/refinements/"
  - refinement_log: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/refinement-log.yaml"
  - recommended_top_3: ["{{path_1}}", "{{path_2}}", "{{path_3}}"]
  - brand_name: "{{brand_name}}"
  - logo_brief: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brief.md"
  - logo_concepts: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-concepts.md"
  - curation_report: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/curation-report.md"
```
