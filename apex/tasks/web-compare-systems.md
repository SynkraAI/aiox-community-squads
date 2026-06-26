# Task: web-compare-systems

```yaml
id: web-compare-systems
version: "1.0.0"
title: "Design System Comparison"
description: >
  Compare an external site's design system with the current project's tokens.
  Extracts tokens from the URL, loads project tokens, and generates a delta
  report showing matches, differences, gaps, and conflicts. Supports adoption
  recommendations per category.
elicit: false
owner: web-intel
executor: web-intel
inputs:
  - url: "External site URL"
outputs:
  - Delta report (matches, differences, gaps, conflicts)
  - Adoption recommendations per category
  - Visual comparison table
veto_conditions:
  - "Comparison without loading project tokens first → BLOCK"
  - "Auto-merge without user decision → BLOCK"
```

---

## Command

### `*compare {url}`

Compare external site's design system with current project.

---

## Execution Steps

### Step 1: Extract External Tokens

Run `web-extract-tokens` pipeline on the provided URL.
Capture: colors, typography, spacing, shadows, radius.

### Step 2: Load Project Tokens

```yaml
project_token_sources:
  priority_order:
    1: "src/index.css — CSS custom properties (:root)"
    2: "tailwind.config.* — Tailwind theme extension"
    3: "src/theme.* — Theme object files"
    4: "src/tokens.* — Design token files"
    5: "src/styles/variables.* — Style variable files"
  detection: "Scan for files matching these patterns, load first found per priority"
```

### Step 3: Map & Compare

```yaml
comparison_dimensions:
  colors:
    method: "Match by role (bg, fg, accent, border) and by HSL proximity"
    output: "match | similar (HSL < 10%) | different | gap (exists in one, not other)"
  typography:
    method: "Match by level (h1-h6, body, caption) and compare values"
    output: "match | similar (< 2px diff) | different | gap"
  spacing:
    method: "Compare base units and scale arrays"
    output: "same base | different base | compatible scale | incompatible"
  shadows:
    method: "Compare elevation levels"
    output: "match | similar | different | gap"
  radius:
    method: "Compare unique values"
    output: "match | different | gap"
```

### Step 4: Generate Delta Report

```
## Design System Comparison: {url} vs Current Project

### Summary
| Category | Matches | Similar | Different | Gaps |
|----------|---------|---------|-----------|------|
| Colors | 4 | 2 | 3 | 1 |
| Typography | 3 | 1 | 2 | 0 |
| Spacing | match (4px base) | — | — | — |
| Shadows | 1 | 0 | 1 | 2 |
| Radius | 1 | 1 | 0 | 0 |

### Detailed Comparison
[... per-category tables with values side by side ...]

### Adoption Recommendations
| # | What | Action | Impact |
|---|------|--------|--------|
| 1 | Shadow system (+2 levels) | ADOPT | Adds elevation depth |
| 2 | Accent color variant | ADAPT | Map to our accent scale |
| 3 | Type scale ratio | KEEP OURS | Our 1.25 ratio works better |

---

Options:
1. Adopt recommended changes (→ @design-sys-eng)
2. Cherry-pick specific items
3. Export comparison as markdown
4. Full token-by-token detail
5. Done
```
