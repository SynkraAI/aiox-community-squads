# Workflow: Cohorts Diagnostic

```yaml
workflow:
  id: cohorts-diagnostic
  name: Diagnostico Integrado de Cohorts
  version: 1.0.0
  category: cohort-analytics
  orchestrator: data-chief
  participants:
    - peter-fader
    - wes-kao
    - david-spinks
    - nick-mehta
    - narrative-strategist
    - avinash-kaushik
```

## Workflow Wiring

```yaml
state_machine:
  states: [preflight, specialist-execution, synthesis, complete]
  transitions:
    - trigger: preflight_complete
      source: preflight
      dest: specialist-execution
    - trigger: specialist_outputs_ready
      source: specialist-execution
      dest: synthesis
    - trigger: executive_summary_ready
      source: synthesis
      dest: complete
task_ref:
  primary:
    - segment-rfm
    - design-learning-outcomes
    - measure-community
    - design-health-score
  supporting:
    - analyze-cohort
    - create-dashboard
```

## Workspace Execution Contract

### Preflight (obrigatorio)

1. `*workspace-preflight` (executa `bootstrap-data-workspace.sh` + `validate-data-essentials.sh`)
2. `*workspace-context {slug}`
3. Confirmar templates em `workspace/_templates/analytics/cohorts/`

### Output Routing

- **Canonical (template-first):**
  - `workspace/businesses/{slug}/analytics/cohorts/segmentation-rfm.yaml`
  - `workspace/businesses/{slug}/analytics/cohorts/learning-journey.yaml`
  - `workspace/businesses/{slug}/analytics/cohorts/community-health.yaml`
  - `workspace/businesses/{slug}/analytics/cohorts/student-health-score.yaml`
  - `workspace/businesses/{slug}/analytics/cohorts/icp-deep-analysis.yaml`
  - `workspace/businesses/{slug}/analytics/cohorts/executive-summary.yaml`
- **Custom (ad-hoc):**
  - `docs/data/{slug}/cohorts-diagnostic-{date}.md`

### Hard Rules

- Proibido gravar em `workspace/businesses/{slug}/analytics/cohorts/` sem template correspondente em `workspace/_templates/analytics/cohorts/`.
- Relatorios em `docs/data/{slug}/` sao complementares e nao substituem artefatos canonicos.

## Governance Ownership

- `marketing-lead` (owner executivo)
- `narrative-strategist` (owner de leitura narrativa/copy)
- `data-chief` (owner operacional de analytics)

## Execucao por Especialista

1. `@peter-fader`
   - produzir `segmentation-rfm.yaml`
2. `@wes-kao`
   - produzir `learning-journey.yaml`
3. `@david-spinks`
   - produzir `community-health.yaml`
4. `@nick-mehta`
   - produzir `student-health-score.yaml`
5. `narrative-strategist`
   - produzir `icp-deep-analysis.yaml`
6. `@avinash-kaushik`
   - consolidar `executive-summary.yaml`

## Completion Checklist

- [ ] Todos os 6 artefatos canonicos foram gerados em `analytics/cohorts/`.
- [ ] Todos os artefatos usam o padrao `analytics-template-v1`.
- [ ] `executive-summary.yaml` referencia os 5 artefatos de base.
- [ ] Ownership (`marketing-lead`, `narrative-strategist`, `data-chief`) registrado.
