# Task: web-analyze-patterns

```yaml
id: web-analyze-patterns
version: "1.0.0"
title: "Frontend Pattern Analysis from URL"
description: >
  Analyze component patterns, layout structures, and interaction patterns from an
  external URL. Identifies reusable UI patterns (cards, headers, forms, modals),
  layout strategies (grid, flex, container queries), and interaction patterns
  (hover, scroll, click behaviors).
elicit: false
owner: web-intel
executor: web-intel
inputs:
  - url: "Target URL"
outputs:
  - Component pattern inventory
  - Layout strategy analysis
  - Interaction pattern catalog
veto_conditions:
  - "Pattern identification without DOM evidence → BLOCK"
  - "Auto-replicate patterns without user decision → BLOCK"
```

---

## Command

### `*analyze-patterns {url}`

Analyze component and layout patterns from an external site.

---

## Execution Steps

### Step 1: Navigate & Capture DOM

Navigate with playwright. Capture:
- Full DOM structure with semantic analysis
- CSS layout properties (display, grid-template, flex-direction)
- Event listeners and interaction hints (hover states, transitions)

### Step 2: Identify Component Boundaries

```yaml
component_detection:
  signals:
    - "Repeated DOM structures (same class pattern, same child structure)"
    - "Semantic HTML (header, nav, main, section, article, aside, footer)"
    - "ARIA landmarks and roles"
    - "BEM-like or utility class patterns"
  categories:
    navigation: "nav, header menus, breadcrumbs, tabs"
    content: "cards, lists, grids, tables, timelines"
    forms: "inputs, selects, checkboxes, form groups"
    feedback: "modals, toasts, tooltips, alerts"
    layout: "containers, sidebars, split views"
    media: "hero sections, galleries, carousels"
```

### Step 3: Analyze Layout Strategy

```yaml
layout_analysis:
  detect:
    - "CSS Grid usage (grid-template-columns, grid-template-areas)"
    - "Flexbox patterns (direction, wrap, gap)"
    - "Container queries (@container)"
    - "Responsive breakpoints (media queries)"
    - "Fluid sizing (clamp, min, max, vw units)"
  output:
    strategy: "grid-first | flex-first | hybrid"
    breakpoints: "list of detected breakpoints"
    fluid_patterns: "list of fluid/clamp values"
```

### Step 4: Catalog Interaction Patterns

```yaml
interaction_detection:
  - "Hover states (color changes, transforms, shadows)"
  - "Focus indicators (outline, box-shadow, border)"
  - "Scroll behaviors (sticky, parallax, reveal-on-scroll)"
  - "Click/tap feedback (scale, color, ripple)"
  - "Loading patterns (skeleton, spinner, progressive)"
  - "State transitions (open/close, expand/collapse)"
```

### Step 5: Present Pattern Report

```
## Pattern Analysis: {url}

### Components Detected ({N} unique patterns)
| # | Pattern | Instances | Structure | Reusable? |
|---|---------|-----------|-----------|-----------|
| 1 | Card | 12 | div > img + h3 + p + button | Yes |
| 2 | Header | 1 | header > nav > logo + links + cta | Yes |
| ... | ... | ... | ... | ... |

### Layout Strategy: {grid-first | flex-first | hybrid}
- Breakpoints: {list}
- Fluid patterns: {list}
- Container queries: {yes/no}

### Interaction Patterns
| Pattern | Trigger | Effect | CSS/JS |
|---------|---------|--------|--------|
| Hover lift | :hover | translateY(-2px) + shadow | CSS |
| ... | ... | ... | ... |

---

Options:
1. REPLICATE — Recreate pattern in our project
2. INSPIRE — Use as reference for design
3. COMPARE — With our existing components
4. DETAIL — Deep dive into specific pattern
5. Done
```
