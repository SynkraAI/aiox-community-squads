# Task: Brand Quality Gate

## Metadata

```yaml
id: brand-quality-gate
name: Gate de Qualidade de Brand Equity
executor: keller-brand-equity
elicit: false
estimated_duration: "10-20 min"
```

**Responsible Executor:** Agent (@keller-brand-equity)
**Dependencies:** depends_on: `[create-brand-story]` · enables: `[story approval]` · workflow: `wf-brand-epic`

## Objective

Validar que o trabalho de brand preserva ou fortalece brand equity. NAO e um gate de codigo — e um gate de MARCA. Substitui o qa-gate.md convencional para stories de brand.

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `story_id` | string | sim | ID da story sendo avaliada |
| `yaml_source` | string | sim | YAML canonico de referencia |
| `acceptance_criteria` | array | sim | ACs da story |
| `changed_files` | array | sim | Arquivos modificados pela story |

---

## Output

| Artifact | Location | Description |
|----------|----------|-------------|
| `{epic}.{story}-brand-gate.yml` | `docs/qa/gates/` | Gate file com decisao e issues |

---

## Veto Conditions

- [ ] VETO se nao leu o YAML canonico antes de avaliar
- [ ] VETO se gate NAO verifica consistencia YAML → artefatos
- [ ] VETO se emite PASS sem verificar vocabulario proibido

---

## Gate Schema

```yaml
schema: 1
type: brand-equity-gate
story: '{epic}.{story}'
gate: PASS | CONCERNS | FAIL | WAIVED
status_reason: '1-2 frases explicando decisao'
reviewer: '@keller-brand-equity'
updated: '{ISO-8601 timestamp}'
yaml_source: '{path do YAML canonico}'
brand_checks:
  yaml_consistency: PASS | FAIL
  archetype_alignment: PASS | FAIL
  vocabulary_compliance: PASS | FAIL
  tone_consistency: PASS | FAIL
  trueline_consistency: PASS | FAIL
  category_consistency: PASS | FAIL
top_issues: []
waiver: { active: false }
```

---

## Brand Check Criteria

### 1. YAML Consistency (obrigatorio)

```
Ler YAML canonico (yaml_source)
Para cada arquivo modificado:
  Verificar se dados derivam do YAML
  SE divergencia encontrada -> issue BRAND-YAML-{NNN}
```

### 2. Archetype Alignment (obrigatorio)

```
Verificar archetype_mix no brandbook.yaml:
  Outlaw 50% | Magician 35% | Explorer 15%
  SE referencia Sage ou Ruler -> issue BRAND-ARCH-{NNN} (high)
  SE percentuais divergem -> issue BRAND-ARCH-{NNN} (medium)
  SE tom nao e consistente com outlaw primary -> issue BRAND-ARCH-{NNN} (medium)
```

### 3. Vocabulary Compliance (obrigatorio)

```
Ler brandbook.yaml > voice > always_use + never_use
Para cada arquivo modificado:
  Grep termos proibidos (never_use)
  SE encontrado -> issue BRAND-VOC-{NNN}
  Verificar presenca de termos obrigatorios em contextos relevantes
```

### 4. Trueline Consistency

```
Trueline canonica: brandbook.yaml > essence > trueline
SE arquivo usa trueline antiga ("A IA e a seta...") -> issue BRAND-TL-{NNN} (high)
SE arquivo nao referencia trueline onde deveria -> issue BRAND-TL-{NNN} (low)
```

### 5. Tone Consistency

```
Verificar brandbook.yaml > voice > tone_sliders
SE conteudo e excessivamente formal (casual < 50%) -> issue BRAND-TONE-{NNN}
SE conteudo e passivo/sage-like (empoderamento < 50%) -> issue BRAND-TONE-{NNN}
```

### 6. Category Consistency

```
Categoria canonica: brandbook.yaml ou strategic-positioning.yaml
SE arquivo usa categoria antiga -> issue BRAND-CAT-{NNN} (high)
```

---

## Issue Prefixes

| Prefix | Domain |
|--------|--------|
| `BRAND-YAML-` | Divergencia com YAML canonico |
| `BRAND-ARCH-` | Arquetipo incorreto ou removido |
| `BRAND-VOC-` | Vocabulario proibido ou ausente |
| `BRAND-TL-` | Trueline divergente |
| `BRAND-TONE-` | Tom de voz inconsistente |
| `BRAND-CAT-` | Categoria divergente |
| `BRAND-EQ-` | Brand equity enfraquecida (generico) |

## Severity Scale

- `low`: Inconsistencia menor, nao afeta percepcao de marca
- `medium`: Inconsistencia que pode confundir publico, corrigir em breve
- `high`: Divergencia ativa com YAML canonico, bloqueia aprovacao

---

## Gate Decision Criteria

### PASS

- Todos os 6 brand checks passam
- Nenhuma issue high-severity
- ACs da story atendidos

### CONCERNS

- Issues medium presentes mas nao bloqueantes
- Brand equity preservada no geral
- Recomendacoes de melhoria documentadas

### FAIL

- Pelo menos 1 brand check falhou com high-severity
- Divergencia ativa com YAML canonico
- Recomendacao: nova story de fix (NAO reabrir story atual)

### WAIVED

- Issues aceitas com aprovacao do @brand-chief
- Motivo documentado
- Prazo para correcao definido

---

## Output: Story Update

Apos criar gate file, appendar na story:

```markdown
## Brand Gate Results

### Review Date: {data}
### Reviewed By: @keller-brand-equity

| Check | Result |
|-------|--------|
| YAML Consistency | PASS/FAIL |
| Archetype Alignment | PASS/FAIL |
| Vocabulary Compliance | PASS/FAIL |
| Trueline Consistency | PASS/FAIL |
| Tone Consistency | PASS/FAIL |
| Category Consistency | PASS/FAIL |

### Gate Status

Gate: {STATUS} -> docs/qa/gates/{epic}.{story}-brand-gate.yml
```

---

## Escalation

```
SE 2 stories consecutivas FAIL -> escalar para @brand-chief
SE issue BRAND-ARCH com Sage/Ruler -> escalar imediatamente (decisao de marca)
SE waiver solicitado -> @brand-chief deve aprovar com justificativa
```

---

*Task do Squad Brand - @keller-brand-equity*
