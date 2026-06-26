# Epic: {{EPIC_TITLE}}

> {{EPIC_GOAL_1_FRASE}}

---

## Epic Metadata

```yaml
epic_id: {{EPIC_ID}}
title: "{{EPIC_TITLE}}"
status: Planning
created: {{DATE_ISO}}
squad: brand
workflow: wf-brand-epic

yaml_sources:
  - "{{YAML_SOURCE_1}}"
  # - "{{YAML_SOURCE_2}}"

brand_name: "{{BRAND_SLUG}}"
```

---

## Context

{{CONTEXTO_2_3_PARAGRAFOS}}

---

## YAML Sources (Fontes da Verdade)

> **YAML E LEI.** Toda story deste epic DEVE derivar de um YAML canonico.
> Se o YAML diverge do artefato downstream, o YAML vence.

| YAML | Path | Dono de |
|------|------|---------|
| {{YAML_NAME}} | `{{YAML_PATH}}` | {{O_QUE_CONTEM}} |

---

## Stories

### Wave 1 — {{WAVE_1_TITULO}}

| Story | Titulo | Executor | Gate | Priority | Status |
|-------|--------|----------|------|----------|--------|
| {{EPIC_ID}}-EP01 | {{TITULO}} | @{{EXECUTOR}} | @keller-brand-equity | {{PRIORITY}} | {{STATUS}} |

### Wave 2 — {{WAVE_2_TITULO}}

| Story | Titulo | Executor | Gate | Priority | Status | Blocked By |
|-------|--------|----------|------|----------|--------|------------|
| {{EPIC_ID}}-EP02 | {{TITULO}} | @{{EXECUTOR}} | @keller-brand-equity | {{PRIORITY}} | {{STATUS}} | EP01 |

---

## Brand Agent Workflow

```
@brand-chief define escopo
  -> @brand-strategist valida escopo e prioriza
  -> Agente especialista executa story
  -> @keller-brand-equity executa brand-quality-gate
  -> @brand-chief aprova e libera proxima onda
```

### Agentes envolvidos

| Agente | Papel neste epic | Stories |
|--------|-----------------|---------|
| @brand-chief | Orquestrador | Todas |
| @keller-brand-equity | Gate de brand equity | Todas |
| @{{EXECUTOR_1}} | Executor | EP01, EP02 |

---

## Scope

### In Scope

{{LISTA_DO_QUE_ESTA_DENTRO}}

### Out of Scope

{{LISTA_DO_QUE_ESTA_FORA}}

---

## Target Files

```
{{TREE_DE_ARQUIVOS_ALVO}}
```

---

## Dependencies Graph

```
EP01 --blocks--> EP02 --blocks--> EP03
```

---

## Success Criteria

- [ ] Todas as stories com status Done
- [ ] Todos os brand-quality-gates com PASS ou WAIVED
- [ ] Zero divergencia entre YAMLs canonicos e artefatos downstream
- [ ] Memoria persistente atualizada

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| {{RISCO}} | {{IMPACTO}} | {{MITIGACAO}} |

---

*Epic criado por @brand-chief via create-brand-epic*
