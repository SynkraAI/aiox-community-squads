# Task: Create Brand Epic

## Metadata

```yaml
id: create-brand-epic
name: Criar Epic de Brand com Agentes Nativos
executor: brand-chief
elicit: true
estimated_duration: "15-30 min"
```

**Responsible Executor:** Agent (@brand-chief)
**Dependencies:** depends_on: `[load-workspace-context]` · enables: `[create-brand-story]` · workflow: `wf-brand-epic`

## Objective

Criar um epic formalizado para trabalho de brand usando agentes nativos do squad (nao o ciclo convencional dev/QA). O epic define ondas de stories com executores de brand, gates de brand equity, e veto conditions de marca.

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `epic_name` | string | sim | Nome descritivo do epic |
| `epic_goal` | string | sim | Objetivo em 1-2 frases |
| `yaml_sources` | array | sim | YAMLs canonicos que sao fonte da verdade |
| `brand_name` | string | sim | Slug do business em workspace/ |
| `scope` | string | sim | Descricao do escopo (o que esta dentro e fora) |

---

## Output

| Artifact | Location | Description |
|----------|----------|-------------|
| `epic.md` | `docs/stories/epics/epic-{slug}/epic.md` | Epic com metadata, stories, workflow, grafo |

---

## Veto Conditions

- [ ] VETO se epic nao referencia pelo menos 1 YAML canonico como fonte da verdade
- [ ] VETO se alguma story tem executor que nao pertence ao brand squad
- [ ] VETO se nao tem brand-quality-gate definido como gate de cada story
- [ ] VETO se grafo de dependencias permite ciclo (nada volta)
- [ ] VETO se escopo e vago demais (sem lista de arquivos/artefatos alvo)

---

## Steps

### Step 1: Carregar contexto workspace

```
Executar load-workspace-context para brand_name
Ler YAMLs canonicos listados em yaml_sources
Mapear estado atual vs estado desejado
```

### Step 2: Definir stories do epic

Para cada unidade de trabalho identificada:

```yaml
story:
  id: "{EPIC_ID}-EP{NN}"
  title: "{titulo descritivo}"
  executor: "{agent-id do brand squad}"
  gate: "@keller-brand-equity via brand-quality-gate"
  yaml_source: "{YAML canonico que esta story deriva}"
  priority: "CRITICAL | P1 | P2"
  status: "Draft | Ready | Blocked"
  blocked_by: [] # IDs de stories que devem completar antes
```

### Step 3: Definir ondas de execucao

Agrupar stories em ondas respeitando dependencias:

```
Wave 1: Stories sem dependencias (podem rodar em paralelo)
Wave 2: Stories que dependem da Wave 1
Wave N: ...
```

### Step 4: Definir workflow do epic

```
@brand-chief define escopo
  -> @brand-strategist valida escopo e prioriza stories
  -> Agente especialista executa story
  -> @keller-brand-equity executa brand-quality-gate
  -> @brand-chief aprova e libera proxima onda
```

### Step 5: Gerar epic.md usando template

Usar `squads/brand/templates/brand-epic-tmpl.md` como base.
Preencher com dados das Steps 1-4.

### Step 6: Validacao final

Checklist antes de salvar:

- [ ] Todas as stories tem executor do brand squad
- [ ] Todas as stories tem gate de brand equity
- [ ] Todas as stories referenciam YAML canonico
- [ ] Grafo de dependencias e DAG (sem ciclos)
- [ ] Escopo de cada story e mensuravel (lista de arquivos/artefatos)
- [ ] Nenhuma story depende de agente externo ao squad sem justificativa

---

## Handoff

```yaml
to: brand-chief
task: create-brand-story
pass:
  - epic_id: "{EPIC_ID}"
  - stories: "array de stories definidas"
  - first_story: "{ID da primeira story Ready}"
```

---

*Task do Squad Brand - Brand Chief*
