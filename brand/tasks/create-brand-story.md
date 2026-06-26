# Task: Create Brand Story

## Metadata

```yaml
id: create-brand-story
name: Criar Story de Brand com Template Nativo
executor: brand-chief
elicit: true
estimated_duration: "10-20 min"
```

**Responsible Executor:** Agent (@brand-chief)
**Dependencies:** depends_on: `[create-brand-epic]` · enables: `[brand-quality-gate]` · workflow: `wf-brand-epic`

## Objective

Criar uma story formal para trabalho de brand usando o template nativo do squad. A story define: executor de brand, YAML canonico de referencia, veto conditions de marca, acceptance criteria mensuráveis, e gate de brand equity.

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `epic_id` | string | sim | ID do epic pai |
| `story_number` | integer | sim | Numero sequencial (EP01, EP02...) |
| `story_title` | string | sim | Titulo descritivo |
| `executor` | string | sim | Agent ID do executor (deve ser do brand squad) |
| `yaml_source` | string | sim | YAML canonico que esta story deriva |
| `scope` | string | sim | Descricao do escopo com lista de arquivos alvo |

---

## Output

| Artifact | Location | Description |
|----------|----------|-------------|
| `{EPIC_ID}-EP{NN}-{slug}.md` | `docs/stories/epics/epic-{epic-slug}/` | Story com template brand completo |

---

## Veto Conditions

- [ ] VETO se executor nao pertence ao brand squad (checar squads/brand/config.yaml agents)
- [ ] VETO se nao referencia YAML canonico como fonte da verdade
- [ ] VETO se acceptance criteria nao sao mensuráveis (deve ter verbo + artefato + condicao)
- [ ] VETO se escopo nao lista arquivos/artefatos alvo explicitamente
- [ ] VETO se nao tem pelo menos 1 veto condition de marca
- [ ] VETO se gate nao e brand-quality-gate (nunca qa-gate generico)

---

## Steps

### Step 1: Validar executor

```
Ler squads/brand/config.yaml > agents
SE executor nao esta na lista -> VETO
SE executor e tier 0 (brand-chief) -> WARN: chief nao executa, chief orquestra
```

### Step 2: Carregar YAML canonico

```
Ler yaml_source completo
Extrair dados relevantes para o escopo da story
Mapear estado atual (o que esta no YAML) vs estado downstream (docs/TSX)
```

### Step 3: Definir acceptance criteria

Para cada AC, usar formato:

```
- [ ] **AC{N}:** {Verbo no infinitivo} {artefato alvo} {condicao mensurável}
  - {sub-item com detalhe se necessario}
```

Regras:
- Minimo 3 ACs por story
- Maximo 7 ACs por story (se mais, quebrar em 2 stories)
- Cada AC deve ser verificavel por grep/read (nao subjetivo)

### Step 4: Definir veto conditions de marca

Veto conditions especificas de brand (nao genericas):

| Tipo | Exemplo |
|------|---------|
| Divergencia YAML | VETO se artefato diverge do YAML canonico |
| Brand equity | VETO se mudanca enfraquece posicionamento |
| Vocabulario | VETO se usa termos proibidos pelo YAML |
| Tom de voz | VETO se tom nao e consistente com archetype_mix |
| Arquetipo | VETO se referencia arquetipo removido (Sage, Ruler) |

### Step 5: Definir tasks

Para cada task:

```markdown
### T{N}. {Titulo descritivo} (AC: {lista de ACs que esta task satisfaz})

- [ ] {acao atomica 1}
- [ ] {acao atomica 2}
```

### Step 6: Gerar story usando template

Usar `squads/brand/templates/brand-story-tmpl.md` como base.
Preencher com dados das Steps 1-5.

### Step 7: Validacao final (self-check)

- [ ] Executor e do brand squad
- [ ] YAML canonico referenciado
- [ ] 3-7 ACs mensuráveis
- [ ] Pelo menos 1 veto condition de marca
- [ ] Gate e brand-quality-gate
- [ ] File List com paths exatos
- [ ] Status lifecycle definido (Draft -> Ready -> InProgress -> InReview -> Done)

---

## Brand Story Lifecycle

```
Draft    -> @brand-strategist valida escopo -> Ready
Ready    -> Agente executor trabalha       -> InProgress
InProgress -> @keller-brand-equity gate    -> InReview
InReview -> @brand-chief aprova            -> Done
```

**Fluxo unidirecional. Nada volta. NUNCA.**

Se gate retorna FAIL: criar nova story de fix, nao reabrir a atual.

---

## Handoff

```yaml
to: "{executor}"
task: "execucao da story"
pass:
  - story_id: "{EPIC_ID}-EP{NN}"
  - yaml_source: "{path do YAML canonico}"
  - scope: "{lista de arquivos alvo}"
  - acceptance_criteria: "array de ACs"
```

---

*Task do Squad Brand - Brand Chief*
