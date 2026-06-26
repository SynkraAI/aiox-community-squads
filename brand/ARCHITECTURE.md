# Architecture - Brand Squad

## Pipeline Flow

```
                        ┌──────────────┐
                        │  brand-chief │  Tier 0: Orchestrator
                        │  (routing)   │
                        └──────┬───────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────▼──────┐  ┌─────▼──────┐  ┌──────▼───────┐
     │ BRASIL CORE   │  │ FOUNDATIONS │  │ POSITIONING  │
     │ Tier 1        │  │ Tier 0     │  │ Tier 1       │
     ├───────────────┤  ├────────────┤  ├──────────────┤
     │naming-strat.  │  │keller-eq.  │  │neumeier-diff.│
     │brand-strat.   │  │aaker-id.   │  │ries-posit.   │
     │domain-scout   │  │sharp-sci.  │  │storybrand    │
     └───────────────┘  └────────────┘  │archetype     │
                                        └──────────────┘
                                               │
                                     ┌─────────▼─────────┐
                                     │ ACTIVATION        │
                                     │ Tier 2            │
                                     ├───────────────────┤
                                     │wheeler-design     │
                                     │yohn-culture       │
                                     │heyward-dtc        │
                                     │miller-sticky      │
                                     └───────────────────┘
```

## Tier System

| Tier | Role | Agents |
|------|------|--------|
| 0 | Diagnosis & Orchestration | brand-chief, keller-brand-equity, aaker-brand-identity, sharp-brand-science |
| 1 | Core Strategy | naming-strategist, brand-strategist, neumeier-differentiation, ries-positioning, storybrand-narrator, archetype-consultant |
| 2 | Activation & Operations | domain-scout, wheeler-brand-design, yohn-brand-culture, heyward-dtc-brand, miller-sticky-brand |

## Workflow Map

```
wf-naming-to-domain:        naming-strategist → domain-scout
wf-brand-foundations:        keller → aaker → sharp
wf-brand-positioning:        neumeier → ries → archetype → storybrand
wf-brand-activation:         wheeler → yohn → heyward → miller
wf-brand-complete:           [naming] → [foundations] → [positioning] → [activation]
wf-brand-all-hands:          All 14 specialists sequentially
wf-logo-brainstorm:          wheeler + archetype → nano-banana (cross-squad: design)
wf-brand-mockup-generation:  wheeler → nano-banana (cross-squad: design)
```

## Workspace Integration

Level: `workspace_first`

```
workspace/businesses/{brand_name}/L2-tactical/brand/
├── brandbook.yaml          # Canonical brand definition
├── naming/                 # SNP outputs
├── foundations/             # CBBE, Brand Vision, Growth
├── positioning/             # Onlyness, Positioning, SB7, Archetype
├── activation/              # Identity system, culture, DTC, sticky
├── logo/                    # Logo brainstorm outputs
└── mockups/                 # Mockup generation outputs
```

## Cross-Squad Dependencies

| Squad | Agent | Used By |
|-------|-------|---------|
| design | nano-banana-generator | wf-logo-brainstorm, wf-brand-mockup-generation |

## Handoff Protocol

Unidirectional flow. Cada fase produz artefato YAML canônico que alimenta a próxima.
Nenhum output volta para fase anterior. brand-chief consolida no final.
