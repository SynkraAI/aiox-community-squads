# Story: {{STORY_ID}} — {{STORY_TITLE}}

> {{OBJETIVO_1_FRASE}}

---

## Story Metadata

```yaml
story_id: {{STORY_ID}}
epic_id: {{EPIC_ID}}
title: "{{STORY_TITLE}}"
status: Draft
created: {{DATE_ISO}}

executor: @{{EXECUTOR_ID}}
gate: @keller-brand-equity
gate_task: brand-quality-gate

yaml_source: "{{YAML_SOURCE_PATH}}"
priority: {{PRIORITY}}
blocked_by: [{{BLOCKED_BY}}]
```

---

## Context

{{CONTEXTO_1_2_PARAGRAFOS}}

---

## YAML Source (Fonte da Verdade)

> **YAML E LEI.** Esta story deriva de `{{YAML_SOURCE_PATH}}`.
> Qualquer divergencia: o YAML vence.

Secoes relevantes do YAML para esta story:

```yaml
# Copiar aqui as secoes do YAML que esta story vai usar/propagar
{{YAML_SECTIONS_RELEVANTES}}
```

---

## Acceptance Criteria

- [ ] **AC1:** {{VERBO_INFINITIVO}} {{ARTEFATO}} {{CONDICAO_MENSURAVEL}}
  - {{detalhe}}
- [ ] **AC2:** {{VERBO_INFINITIVO}} {{ARTEFATO}} {{CONDICAO_MENSURAVEL}}
- [ ] **AC3:** {{VERBO_INFINITIVO}} {{ARTEFATO}} {{CONDICAO_MENSURAVEL}}

---

## Brand Veto Conditions

> Condicoes que BLOQUEIAM aprovacao desta story.

- [ ] VETO se artefato diverge do YAML canonico (`{{YAML_SOURCE_PATH}}`)
- [ ] VETO se referencia arquetipo removido (Sage, Ruler)
- [ ] VETO se usa termo proibido pelo brandbook.yaml > voice > never_use
- [ ] {{VETO_ESPECIFICO_DA_STORY}}

---

## Scope

### Files Alvo

| # | Arquivo | Acao | Status |
|---|---------|------|--------|
| 1 | `{{PATH}}` | {{ACAO}} | A fazer |

### Fora do Escopo

- {{O_QUE_NAO_SERA_TOCADO}}

---

## Tasks

### T1. {{TITULO_DESCRITIVO}} (AC: {{LISTA_ACS}})

- [ ] {{acao_atomica_1}}
- [ ] {{acao_atomica_2}}

### T2. {{TITULO_DESCRITIVO}} (AC: {{LISTA_ACS}})

- [ ] {{acao_atomica_1}}
- [ ] {{acao_atomica_2}}

---

## Brand Story Lifecycle

```
Draft      -> @brand-strategist valida escopo  -> Ready
Ready      -> @{{EXECUTOR_ID}} executa         -> InProgress
InProgress -> @keller-brand-equity brand-gate  -> InReview
InReview   -> @brand-chief aprova              -> Done
```

**Fluxo unidirecional. Nada volta. NUNCA.**

---

## File List

> Atualizar conforme checkboxes sao marcados.

- [ ] `{{PATH_1}}`
- [ ] `{{PATH_2}}`

---

## Brand Gate Results

> Preenchido por @keller-brand-equity apos execucao do brand-quality-gate.

_(pendente)_

---

## Change Log

| Data | Autor | Mudanca |
|------|-------|---------|
| {{DATE}} | @brand-chief | Story criada |

---

*Story criada por @brand-chief via create-brand-story*
