# Task: Logo Curation

## Metadata

```yaml
id: logo-curate
name: Curate and Select Logo Directions
executor: wheeler-brand-design
elicit: true
estimated_duration: "10-15 min"
```

**Responsible Executor:** Agent (@wheeler-brand-design)
**Dependencies:** depends_on: `[logo-generate]` · enables: `[logo-refine]` · workflow: `wf-logo-brainstorm`

## Objective

Apresentar as gerações de logo agrupadas por direção conceitual, coletar feedback do usuário, e decidir: aprovar uma direção para refinamento, iterar com novos prompts, ou pivotar uma direção. Máximo 3 loops de iteração.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| generations_dir | string | yes | Diretório com imagens geradas |
| generation_log | file | yes | `generation-log.yaml` com metadata |
| logo_concepts | file | yes | `logo-concepts.md` para referência dos conceitos |
| brand_name | string | yes | Nome da marca |
| iteration | number | no | Número da iteração atual (default: 1, max: 3) |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `curation-report.md` | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/curation-report.md` | Feedback + decisão de curação |

## Execution Steps

### Step 1: Organizar Apresentação

- Ler `generation-log.yaml`
- Agrupar gerações por direção conceitual
- Para cada direção, listar:
  - Nome do conceito + metáfora
  - Imagens geradas (paths)
  - Tipo de logo de cada imagem
  - Prompt utilizado (resumo)

### Step 2: Apresentar ao Usuário

Formato de apresentação (por direção):

```
## Direção: {{concept_name}}
**Metáfora:** {{metaphor}}
**Imagens:**
1. {{path_1}} — {{logo_type_1}}
2. {{path_2}} — {{logo_type_2}}
3. {{path_3}} — {{logo_type_3}}
```

### Step 3: Coletar Feedback (Elicitação)

Para cada direção, perguntar:

1. **Reação geral** — O que funciona? O que não funciona?
2. **Score (1-5):**
   - 1 = Descartar completamente
   - 2 = Direção errada, mas algo interessante
   - 3 = Potencial, precisa iteração
   - 4 = Bom, refinar esta
   - 5 = Excelente, aprovar para refinamento

3. **Feedback específico** — Ajustes desejados (cor, forma, estilo, composição)

Perguntar também:
- Qual direção é a favorita?
- Quer combinar elementos de direções diferentes?
- Quer explorar uma direção completamente nova?

### Step 4: Decisão

Com base no feedback:

| Score Máximo | Ação | Próxima Fase |
|---|---|---|
| 5 | **APPROVE** — Diretamente para refinamento | logo-refine |
| 4 | **APPROVE WITH NOTES** — Refinar com ajustes específicos | logo-refine |
| 3 | **ITERATE** — Voltar para prompt engineering com feedback | logo-prompt-engineering (loop) |
| 1-2 (todas) | **PIVOT** — Novas direções estratégicas | logo-strategic-direction (loop) |

### Step 5: Compilar Curation Report

---

## Output Template

```markdown
# Curation Report — {{brand_name}}

**Data:** {{date}}
**Iteração:** {{iteration}}/3
**Decisão:** {{APPROVE | ITERATE | PIVOT}}

## Avaliação por Direção

### Direção 1: {{concept_name_1}}
- **Score:** {{score}}/5
- **Feedback:** {{feedback}}
- **Elementos que funcionam:** {{positives}}
- **Elementos a ajustar:** {{negatives}}
- **Imagens aprovadas:** {{approved_images}}

### Direção 2: {{concept_name_2}}
...

## Decisão Final

**Direção selecionada:** {{selected_direction}}
**Rationale:** {{selection_rationale}}
**Ajustes para refinamento:**
{{refinement_notes}}

## Próxima Fase
{{next_phase_description}}
```

---

## Iteration Control

- Iteração 1: Feedback normal, todas as opções disponíveis
- Iteração 2: Sugerir que o usuário escolha uma direção
- Iteração 3 (máxima): Forçar decisão — aprovar a melhor ou pausar o workflow

---

## Veto Conditions

- [ ] Nenhuma geração para apresentar
- [ ] Usuário não forneceu feedback em nenhuma direção
- [ ] Máximo de 3 iterações atingido sem aprovação (escalar para brand-chief)

---

## Handoff

```yaml
# Se APPROVE:
to: nano-banana-generator
task: logo-refine
pass:
  - selected_direction: "{{direction_id}}"
  - selected_images: ["{{img_1}}", "{{img_2}}"]
  - refinement_notes: "{{notes}}"
  - brand_name: "{{brand_name}}"
  - prompt_brief: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-prompt-brief.yaml"

# Se ITERATE:
to: wheeler-brand-design
task: logo-prompt-engineering
pass:
  - feedback: "{{feedback}}"
  - iteration: {{iteration + 1}}
  - logo_concepts: "{{logo_concepts_path}}"

# Se PIVOT (max 1 pivot permitido):
to: wheeler-brand-design
task: logo-strategic-direction
pass:
  - pivot_reason: "{{reason}}"
  - what_worked: "{{positives}}"
  - what_to_avoid: "{{negatives}}"
  - iteration: {{iteration + 1}}
  - logo_brief: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brief.md"
  - brand_name: "{{brand_name}}"
```
