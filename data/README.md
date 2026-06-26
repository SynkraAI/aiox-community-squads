# Data Intelligence Squad

> Squad de analytics orientado por especialistas, organizado em 3 tiers e operando em modo `workspace_first`.

**Slug:** `data`  
**Entry agent:** `data-chief`  
**Versão:** `2.0.0`  
**Readiness owner:** `@coo`  
**Governance handoff:** `squads/c-level`

## Propósito

O squad `data` existe para transformar contexto de negócio em decisões analíticas acionáveis.
Ele combina:

- fundamentação estratégica sobre quem importa e como crescer
- operacionalização de health, churn, comunidade e learning
- comunicação executiva de métricas, attribution e recomendações

A regra central do squad é simples:

> Nunca implementar uma métrica sem passar por pelo menos 1 fundamentador do Tier 0.

## Modelo Operacional

### Tier 0: Fundamentação

- `@peter-fader`
  - CLV, RFM, segmentação por valor, customer centricity
- `@sean-ellis`
  - PMF, AARRR, growth, referral, North Star

Use antes de qualquer desenho de métrica, dashboard ou automação analítica.

### Tier 1: Operacionalização

- `@nick-mehta`
  - Health Score, churn, playbooks de CS
- `@david-spinks`
  - Community metrics, SPACES, ROI de comunidade
- `@wes-kao`
  - Learning outcomes, completion rate, cohort-based learning

Use depois da fundamentação, quando o problema já estiver bem definido.

### Tier 2: Comunicação

- `@avinash-kaushik`
  - Attribution, DMMM, So What, síntese executiva

Use para transformar análise em relatório, priorização e ação.

### Orquestração

- `@data-chief`
  - roteia para o especialista correto
  - força sequência por tiers
  - protege o contrato `workspace_first`

## Quick Start

### Sequência mínima recomendada

```text
/Data:agents:data-chief
*workspace-preflight
*workspace-context {slug}
```

### Ativar especialistas diretamente

```text
/Data:agents:data-chief
/Data:agents:peter-fader
/Data:agents:sean-ellis
/Data:agents:nick-mehta
/Data:agents:david-spinks
/Data:agents:wes-kao
/Data:agents:avinash-kaushik
```

### Tasks principais

```text
/Data:tasks:load-workspace-context
/Data:tasks:calculate-clv
/Data:tasks:segment-rfm
/Data:tasks:design-health-score
/Data:tasks:predict-churn
/Data:tasks:measure-community
/Data:tasks:design-learning-outcomes
/Data:tasks:build-attribution
/Data:tasks:create-dashboard
```

### Workflows principais

```text
/Data:workflows:implement-customer-360
/Data:workflows:create-churn-system
/Data:workflows:implement-attribution
/Data:workflows:fix-completion-rate
/Data:workflows:cohort-analysis-workflow
/Data:workflows:optimize-community-workflow
/Data:workflows:cohorts-diagnostic
```

## Workspace-First

O squad declara `workspace_integration.level: workspace_first` em [config.yaml](squads/data/config.yaml).

### Preflight obrigatório

```bash
bash squads/data/scripts/bootstrap-data-workspace.sh {slug}
bash squads/data/scripts/validate-data-essentials.sh
```

Se o preflight falhar, a execução analítica deve parar.

### Leituras canônicas

- `workspace/businesses/{slug}/`
- `workspace/domains/brand/`
- `workspace/domains/content/`
- `workspace/domains/movement/`
- `workspace/_templates/analytics/`
- `workspace/_templates/business-template/`
- `docs/data/`

### Escritas permitidas

Canonical:

- `workspace/businesses/{slug}/analytics/{artifact}.yaml`
- `workspace/businesses/{slug}/analytics/cohorts/{artifact}.yaml`

Condição:

- o template correspondente precisa existir em `workspace/_templates/analytics/` ou `workspace/_templates/analytics/cohorts/`

Custom:

- `docs/data/{slug}/{artifact}.md`

Use custom apenas para exploração, diagnóstico ad-hoc ou relatório fora do contrato canônico.

### Governança de promoção canônica

Antes de promover um artefato para `workspace/businesses/{slug}/analytics/`:

- `*workspace-preflight` precisa ter passado
- o template precisa existir
- o handoff de governança para `@coo` / `squads/c-level` precisa estar explícito quando aplicável

## Inventário Real do Squad

Contagem atual baseada no conteúdo do diretório:

- Agents: `7`
- Tasks: `13`
- Workflows: `7`
- Templates: `16`
- Checklists: `7`
- Data references: `9`

### Agents

- `data-chief`
- `peter-fader`
- `sean-ellis`
- `nick-mehta`
- `david-spinks`
- `wes-kao`
- `avinash-kaushik`

### Tasks

- `analyze-cohort`
- `build-attribution`
- `calculate-clv`
- `create-dashboard`
- `define-north-star`
- `design-health-score`
- `design-learning-outcomes`
- `load-workspace-context`
- `measure-community`
- `predict-churn`
- `run-growth-experiment`
- `run-pmf-test`
- `segment-rfm`

### Workflows

- `cohort-analysis-workflow`
- `cohorts-diagnostic`
- `create-churn-system`
- `fix-completion-rate`
- `implement-attribution`
- `implement-customer-360`
- `optimize-community-workflow`

### Templates

Core analytics:

- `customer-360-tmpl.yaml`
- `clv-report-tmpl.yaml`
- `cohort-analysis-tmpl.yaml`
- `health-score-report-tmpl.yaml`
- `churn-alert-tmpl.yaml`
- `attribution-report-tmpl.yaml`
- `dmmm-tmpl.yaml`
- `executive-report-tmpl.yaml`
- `community-health-tmpl.yaml`
- `learning-outcomes-tmpl.yaml`

Cohorts:

- `cohorts/segmentation-rfm-tmpl.yaml`
- `cohorts/learning-journey-tmpl.yaml`
- `cohorts/community-health-cohort-tmpl.yaml`
- `cohorts/student-health-score-tmpl.yaml`
- `cohorts/icp-deep-analysis-tmpl.yaml`
- `cohorts/executive-summary-tmpl.yaml`

### Checklists

- `cbc-readiness-checklist.md`
- `community-health-checklist.md`
- `customer-360-checklist.md`
- `customer-centricity-checklist.md`
- `health-score-checklist.md`
- `pre-implementation-checklist.md`
- `so-what-checklist.md`

### Data References

O diretório [data/](squads/data/data) é a base canônica de conhecimento do squad.

Ele contém:

- `README.md` como índice do knowledge base
- `framework/` com 8 referências estáveis do pack

## Estrutura do Diretório

```text
squads/data/
├── config.yaml
├── README.md
├── agents/
├── tasks/
├── workflows/
├── templates/
├── checklists/
├── data/
│   ├── README.md
│   └── framework/
├── scripts/
├── examples/
├── outputs/
├── projects/
├── .backup/                     # transitório de manutenção, não canônico
└── workspace-hardening-state.json
```

## Regras de Manutenção

- Não recriar `docs/` dentro de `squads/data/`.
- Material de referência estável vai para `data/`.
- Contratos de saída vão para `templates/`.
- Execução vive em `tasks/` e `workflows/`.
- Outputs temporários não devem ser promovidos para conteúdo canônico do squad.
- Se um arquivo de framework for renomeado, atualizar também:
  - [config.yaml](squads/data/config.yaml)
  - [data/README.md](squads/data/data/README.md)
  - [prd.json](squads/data/projects/data-v1-setup/prd.json)
  - [prompt.md](squads/data/projects/data-v1-setup/prompt.md)

## O Que Este README Deve Fazer

Este arquivo é o contrato de entrada do squad.
Ele deve responder rapidamente:

- o que o squad faz
- como operar em `workspace_first`
- quais assets existem de verdade
- onde fica a base de conhecimento
- quais regras de manutenção não podem ser quebradas

Se o README não ajuda nessas 5 perguntas, ele está errado.
