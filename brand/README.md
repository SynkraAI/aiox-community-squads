# Brand Squad

> Brasil-first para Naming, Branding e Ativação de Marca.
> Base principal: **Igor Pinterich (SNP)** + **Ana Couto (É, Faz e Fala)**.
> Expansão: 11 especialistas globais para cobrir fundamentos, posicionamento, narrativa e operação.

## Quick Start

```bash
@brand                 # Orquestrador
*workspace-preflight {brand_slug}
*workspace-context {brand_slug}
@brand:naming          # Naming + domínio
@brand:strategy        # Estratégia de marca (Ana Couto)
@brand:domain          # Só domínio
@brand:all-hands       # Ativa fluxo máximo (todos os especialistas)
```

## Method Stack

### Core Brasil
- **Naming:** SNP - Strategic Naming Process (Igor Pinterich)
- **Brand Strategy:** É, Faz e Fala + Ondas de Valor (Ana Couto)

### Foundations (diagnóstico e arquitetura)
- Kevin Lane Keller - CBBE
- David Aaker - Brand Vision
- Byron Sharp - Mental/Physical Availability

### Positioning & Narrative
- Marty Neumeier - Zag/Onlyness
- Al & Laura Ries - Positioning
- Donald Miller - StoryBrand SB7
- Mark & Pearson - 12 Archetypes

### Activation & Operations
- Alina Wheeler - 5-Phase Process
- Denise Lee Yohn - FUSION
- Emily Heyward - Brand Obsession
- Jeremy Miller - Sticky Branding

## Core Agents (15 local agents + 1 cross-squad bridge)

| Agent | Layer | Uso principal |
|---|---|---|
| `brand-chief` | Orchestration | Triage + routing |
| `naming-strategist` | Brasil Core | Naming por SNP |
| `brand-strategist` | Brasil Core | Estratégia É/Faz/Fala |
| `domain-scout` | Brasil Core | Domínio e handles |
| `keller-brand-equity` | Foundations | Diagnóstico de equity |
| `aaker-brand-identity` | Foundations | Identidade/arquitetura |
| `sharp-brand-science` | Foundations | Estratégia de crescimento |
| `neumeier-differentiation` | Positioning | Diferenciação |
| `ries-positioning` | Positioning | Posição competitiva |
| `storybrand-narrator` | Narrative | Mensagem SB7 |
| `archetype-consultant` | Narrative | Arquétipos |
| `wheeler-brand-design` | Activation | Sistema de identidade |
| `yohn-brand-culture` | Activation | Cultura + marca |
| `heyward-dtc-brand` | Activation | Startup/DTC |
| `miller-sticky-brand` | Activation | PME/B2B |

Local composition:

- `brand-chief` as orchestrator
- 14 domain specialists across naming, foundations, positioning, narrative, and activation

Cross-squad bridge:

- `nano-banana-generator` -> canonical agent in `squads/design/agents/nano-banana-generator.md`

## Activation Matrix

| Command | Routes to |
|---|---|
| `@brand` | `brand-chief` |
| `@brand:brand-chief` | `brand-chief` |
| `@brand:naming` / `@brand:naming-strategist` | `naming-strategist` |
| `@brand:domain` / `@brand:domain-scout` | `domain-scout` |
| `@brand:strategy` / `@brand:brand-strategist` | `brand-strategist` |
| `@brand:keller` / `@brand:keller-brand-equity` | `keller-brand-equity` |
| `@brand:aaker` / `@brand:aaker-brand-identity` | `aaker-brand-identity` |
| `@brand:sharp` / `@brand:sharp-brand-science` | `sharp-brand-science` |
| `@brand:neumeier` / `@brand:neumeier-differentiation` | `neumeier-differentiation` |
| `@brand:positioning` / `@brand:ries` / `@brand:ries-positioning` | `ries-positioning` |
| `@brand:story` / `@brand:storybrand-narrator` | `storybrand-narrator` |
| `@brand:archetype` / `@brand:archetype-consultant` | `archetype-consultant` |
| `@brand:wheeler` / `@brand:wheeler-brand-design` | `wheeler-brand-design` |
| `@brand:yohn` / `@brand:yohn-brand-culture` | `yohn-brand-culture` |
| `@brand:heyward` / `@brand:heyward-dtc-brand` | `heyward-dtc-brand` |
| `@brand:miller` / `@brand:miller-sticky-brand` | `miller-sticky-brand` |
| `@brand:all-hands` | `brand-chief` (workflow `wf-brand-all-hands`) |

## Workflows

### `wf-naming-to-domain`
```text
naming-strategist -> domain-scout
Output: nome + domínio validado
```

### `wf-brand-foundations`
```text
keller -> aaker -> sharp
Output: baseline de marca + tese estratégica
```

### `wf-brand-positioning-narrative`
```text
neumeier -> ries -> archetype -> storybrand
Output: posicionamento + personalidade + mensagem
```

### `wf-brand-activation-system`
```text
wheeler -> yohn -> heyward -> miller
Output: sistema operacional de marca
```

### `wf-brand-complete` (default)
```text
Naming/Domain -> Foundations -> Positioning/Narrative -> Activation
Output: pacote completo de marca
```

### `wf-brand-all-hands` (max agents)
```text
naming -> domain -> brand-strategist -> keller -> aaker -> sharp ->
neumeier -> ries -> archetype -> storybrand -> wheeler -> yohn ->
heyward -> miller
Output: execução completa com todos os especialistas
```

## Tasks

- `naming-generation` - geração e triagem de nomes (SNP)
- `domain-check` - disponibilidade, preço e handles
- `brand-diagnosis` - baseline de equity e identidade
- `positioning-narrative` - onlyness, positioning e storytelling
- `brand-activation` - implementação de marca por canais e cultura
- `load-workspace-context` - preflight e snapshot de contexto workspace-first

## Workspace Contract

- Base path canônico: `workspace/businesses/{brand_name}/L2-tactical/brand/`
- owner do readiness: `COO`
- resolver canônico: `workspace/scripts/resolve-squad-workspace-readiness.cjs`
- Estrutura operacional:
  - `naming/`
  - `foundations/`
  - `positioning/`
  - `narrative/`
  - `activation/`
- Templates canônicos: `workspace/_templates/business-template/L2-tactical/brand/` (24 arquivos, sem dados)
- Bootstrap zero:
  - `bash squads/brand/scripts/bootstrap-brand-workspace.sh {brand_slug}`
  - `bash squads/brand/scripts/validate-brand-essentials.sh`
  - `node workspace/scripts/resolve-squad-workspace-readiness.cjs --squad=brand --business={brand_slug} --context-type=brand`
- Preflight recomendado em toda execução:
  - `*workspace-preflight {brand_slug}`
  - `*workspace-context {brand_slug}`

O contrato `workspace_first` só permite output final depois do handoff/readiness do
`COO`/`c-level`. Exploração fora do contrato canônico continua em
`docs/brand/{brand_slug}/`.

## Exemplos

```bash
@brand quero criar marca completa para minha startup B2B
@brand:naming preciso de nome para software de contabilidade em PT-BR
@brand:strategy preciso reposicionar minha marca no segmento premium
@brand:domain verificar disponibilidade para Nutrix e Verdi
```

## Directory

```text
squads/brand/
├── agents/
│   ├── brand-chief.md
│   ├── naming-strategist.md
│   ├── brand-strategist.md
│   ├── domain-scout.md
│   ├── keller-brand-equity.md
│   ├── aaker-brand-identity.md
│   ├── sharp-brand-science.md
│   ├── neumeier-differentiation.md
│   ├── ries-positioning.md
│   ├── storybrand-narrator.md
│   ├── archetype-consultant.md
│   ├── wheeler-brand-design.md
│   ├── yohn-brand-culture.md
│   ├── heyward-dtc-brand.md
│   └── miller-sticky-brand.md
├── tasks/
│   ├── naming-generation.md
│   ├── domain-check.md
│   ├── brand-diagnosis.md
│   ├── positioning-narrative.md
│   ├── brand-activation.md
│   └── load-workspace-context.md
├── workflows/
│   ├── wf-naming-to-domain.yaml
│   ├── wf-brand-foundations.yaml
│   ├── wf-brand-positioning-narrative.yaml
│   ├── wf-brand-activation-system.yaml
│   ├── wf-brand-complete.yaml
│   └── wf-brand-all-hands.yaml
├── data/
│   └── swipe-file.yaml
├── config.yaml
└── README.md
```
