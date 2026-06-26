# Task: Logo Deliverable Package

## Metadata

```yaml
id: logo-deliverable
name: Compile Logo Deliverable Package
executor: wheeler-brand-design
elicit: true
estimated_duration: "15-20 min"
```

**Responsible Executor:** Agent (@wheeler-brand-design)
**Dependencies:** depends_on: `[logo-refine]` · enables: `[]` · workflow: `wf-logo-brainstorm`

## Objective

Compilar o pacote final de entrega do brainstorm de logo: especificações de uso (logo-spec.md), relatório consolidado (logo-brainstorm-report.md), e conceito estruturado (logo-concept.yaml). Apresentar ao usuário para aprovação final.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| refinements_dir | string | yes | Diretório com variações refinadas |
| refinement_log | file | yes | `refinement-log.yaml` com histórico PRIO |
| recommended_top_3 | list | yes | Paths das 3 melhores variações |
| logo_brief | file | yes | `logo-brief.md` original |
| logo_concepts | file | yes | `logo-concepts.md` com direções |
| curation_report | file | yes | `curation-report.md` com feedback |
| brand_name | string | yes | Nome da marca |

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `logo-spec.md` | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-spec.md` | Especificações de uso do logo |
| `logo-brainstorm-report.md` | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brainstorm-report.md` | Relatório consolidado do processo |
| `logo-concept.yaml` | `workspace/businesses/{{brand_name}}/L2-tactical/brand/logo-concept.yaml` | Conceito estruturado (workspace canonical) |

## Execution Steps

### Step 1: Apresentação Final (Elicitação)

Apresentar top 3 variações ao usuário:
- Mostrar cada variação com path
- Contextualizar: direção conceitual, metáfora, rationale
- Perguntar: qual é a variação final escolhida?
- Coletar nome/apelido para o logo (se houver)

### Step 2: Compilar Logo Spec

Criar `logo-spec.md` com guidelines de uso:

```markdown
# Logo Specification — {{brand_name}}

**Data:** {{date}}
**Versão:** 1.0

## Logo Principal
**Arquivo:** {{selected_logo_path}}
**Tipo:** {{logo_type}}
**Direção Conceitual:** {{concept_name}}

## Conceito
**Metáfora Visual:** {{metaphor}}
**Rationale:** {{rationale}}

## Especificações Técnicas
- **Aspect Ratio:** {{ratio}}
- **Paleta de cores:** {{colors}}
- **Tipografia:** {{typography}} (se aplicável)
- **Estilo:** {{style_description}}

## Regras de Uso
### Área de proteção
- Manter espaço livre ao redor do logo equivalente a {{protection_area}}
- Nunca colocar texto ou elementos dentro da área de proteção

### Tamanho mínimo
- Digital: {{min_size_digital}}px
- Impresso: {{min_size_print}}mm

### O que NÃO fazer
- Não distorcer ou esticar o logo
- Não alterar as cores do logo
- Não adicionar efeitos (sombra, brilho, gradiente)
- Não rotacionar o logo
- Não usar sobre fundos que comprometam a legibilidade

## Variações Aprovadas
1. {{variation_1}} — {{use_case_1}}
2. {{variation_2}} — {{use_case_2}}
3. {{variation_3}} — {{use_case_3}}

## Próximos Passos (Pós-Brainstorm)
- [ ] Vetorização profissional (Illustrator/Figma)
- [ ] Geração de variações (monocromática, negativa, reduzida)
- [ ] Teste em aplicações reais (favicon, card, header)
- [ ] Registro de marca (INPI)
```

### Step 3: Compilar Brainstorm Report

Criar `logo-brainstorm-report.md` — relatório consolidado do processo completo.

Usar template de `workspace/_templates/business-template/L2-tactical/brand/logo-brainstorm-report.yaml` se existir.

Conteúdo:
1. **Resumo Executivo** — Resultado final em 3 linhas
2. **Brief** — Resumo do logo-brief.md
3. **Direções Exploradas** — Resumo das 3-5 direções
4. **Processo de Geração** — Quantas gerações, modelo usado, iterações
5. **Curação** — Feedback por rodada, decisão
6. **Refinamento** — Ciclos PRIO, aprendizados
7. **Resultado Final** — Logo selecionado com rationale
8. **Dados do Processo** — Métricas (total de gerações, iterações, tempo)

### Step 4: Compilar Logo Concept YAML

Criar `logo-concept.yaml` no formato canônico do workspace:

```yaml
# Logo Concept — {{brand_name}}
# Canonical workspace artifact

logo:
  brand_name: "{{brand_name}}"
  version: "1.0"
  created: "{{date}}"
  created_by: "wf-logo-brainstorm"

  concept:
    name: "{{concept_name}}"
    metaphor: "{{metaphor}}"
    archetype: "{{archetype}}"
    mood: "{{mood}}"
    rationale: "{{rationale}}"

  visual_identity:
    logo_type: "{{type}}"
    shape_language: "{{shapes}}"
    color_palette:
      primary: "{{color_1}}"
      secondary: "{{color_2}}"
      accent: "{{color_3}}"
    typography: "{{typography}}"
    style_keywords: ["{{kw1}}", "{{kw2}}", "{{kw3}}"]

  files:
    primary: "{{selected_logo_path}}"
    variations:
      - "{{var_1}}"
      - "{{var_2}}"
      - "{{var_3}}"

  specs:
    aspect_ratio: "{{ratio}}"
    min_size_digital: "{{px}}"
    protection_area: "{{area}}"

  process:
    brief: "logo/logo-brief.md"
    concepts: "logo/logo-concepts.md"
    prompt_brief: "logo/logo-prompt-brief.yaml"
    curation: "logo/curation-report.md"
    refinement: "logo/refinement-log.yaml"
    spec: "logo/logo-spec.md"
    report: "logo/logo-brainstorm-report.md"

  status: "brainstorm-complete"
  next_steps:
    - "vectorization"
    - "color-variations"
    - "application-testing"
    - "trademark-registration"
```

### Step 5: Verificação Final

- [ ] `logo-spec.md` criado com todas as seções
- [ ] `logo-brainstorm-report.md` criado com processo completo
- [ ] `logo-concept.yaml` criado no formato canônico
- [ ] Todos os arquivos referenciados existem
- [ ] Paths relativos corretos

---

## Veto Conditions

- [ ] Usuário não aprovou nenhuma variação final
- [ ] Logo selecionado não existe no filesystem
- [ ] Brief ou concepts files não encontrados

---

## Handoff

```yaml
to: brand-chief
pass:
  - logo_spec: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-spec.md"
  - brainstorm_report: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo/logo-brainstorm-report.md"
  - logo_concept: "workspace/businesses/{{brand_name}}/L2-tactical/brand/logo-concept.yaml"
  - status: "brainstorm-complete"
```
