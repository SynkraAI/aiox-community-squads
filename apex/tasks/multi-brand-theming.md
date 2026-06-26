> **DEPRECATED** — Scope absorbed into `token-architecture.md`. See `data/task-consolidation-map.yaml`.

---
id: multi-brand-theming
version: "1.0.0"
title: "Multi-Brand Theming Architecture"
description: "Design brand-aware token system supporting runtime theme switching, white-label architecture, and multi-tenant color/typography customization"
elicit: true
owner: design-sys-eng
executor: design-sys-eng
outputs:
  - multi-brand-theme-spec.md
  - brand-token-structure.yaml
---

# Multi-Brand Theming Architecture

## When This Task Runs

- Product needs white-label support
- Multiple brands share same codebase
- Runtime theme switching required (beyond light/dark)
- Client customization of colors/typography needed

## Execution Steps

### Step 1: Define Brand Dimensions

**elicit: true** — Confirm what varies per brand:

| Dimension | Varies? | Example |
|-----------|---------|---------|
| **Primary/accent colors** | Yes/No | Brand A: blue, Brand B: green |
| **Typography** | Yes/No | Brand A: Inter, Brand B: Poppins |
| **Logo & icons** | Yes/No | Different logos per tenant |
| **Spacing scale** | Yes/No | Usually consistent across brands |
| **Border radius** | Yes/No | Sharp vs rounded per brand |
| **Shadows** | Yes/No | Flat vs elevated per brand |
| **Motion** | Yes/No | Subtle vs expressive per brand |
| **Dark mode** | Yes/No | All brands support dark? |

### Step 2: Design Token Layering

```yaml
token_layers:
  # Layer 1: Global (same for all brands)
  global:
    purpose: "Universal constants"
    examples:
      - "--spacing-1: 4px"
      - "--font-weight-bold: 700"
      - "--radius-full: 9999px"
    mutability: "NEVER changes per brand"

  # Layer 2: Brand (varies per brand)
  brand:
    purpose: "Brand identity tokens"
    examples:
      - "--brand-primary: var(--color-blue-500)"
      - "--brand-font-heading: 'Inter'"
      - "--brand-radius-default: 8px"
    mutability: "Set per brand config"
    storage: "CSS custom properties on :root[data-brand]"

  # Layer 3: Semantic (maps brand to intent)
  semantic:
    purpose: "Intent-based tokens referencing brand"
    examples:
      - "--color-action: var(--brand-primary)"
      - "--color-surface: var(--brand-surface)"
      - "--font-heading: var(--brand-font-heading)"
    mutability: "NEVER changes — always references brand layer"

  # Layer 4: Component (references semantic)
  component:
    purpose: "Component-specific tokens"
    examples:
      - "--button-bg: var(--color-action)"
      - "--card-radius: var(--brand-radius-default)"
    mutability: "Can override per component variant"
```

### Step 3: Implement Brand Switching

```yaml
brand_switching:
  mechanism: "CSS custom property swap via data-brand attribute"
  trigger: "Route param, subdomain, or user preference"

  implementation:
    css: |
      :root[data-brand="clinic-a"] {
        --brand-primary: #0ea5e9;
        --brand-font-heading: 'Inter', sans-serif;
        --brand-radius-default: 8px;
      }
      :root[data-brand="clinic-b"] {
        --brand-primary: #10b981;
        --brand-font-heading: 'Poppins', sans-serif;
        --brand-radius-default: 12px;
      }

    runtime: |
      // Set brand at app level
      document.documentElement.setAttribute('data-brand', brand)

    ssr: |
      // Set in layout.tsx for SSR
      <html data-brand={tenant.brand} data-theme={theme}>

  dark_mode_interaction:
    strategy: "Brand + theme are independent axes"
    css: |
      :root[data-brand="clinic-a"][data-theme="dark"] {
        --brand-surface: #0f172a;
        --brand-text: #e2e8f0;
      }
```

### Step 4: Create Brand Configuration Schema

```yaml
brand_config_schema:
  brand_id: "string (unique identifier)"
  display_name: "string"
  colors:
    primary: "hex"
    secondary: "hex"
    accent: "hex"
    surface: "hex"
    surface_dark: "hex"
  typography:
    heading_family: "string"
    body_family: "string"
    heading_weight: "number"
  shape:
    radius_default: "px"
    radius_large: "px"
  motion:
    style: "subtle | standard | expressive"
  assets:
    logo_light: "url"
    logo_dark: "url"
    favicon: "url"
```

### Step 5: Validate Multi-Brand

- [ ] Brand switching works without page reload
- [ ] Dark mode works independently for each brand
- [ ] No hardcoded brand-specific values in components
- [ ] New brand addable via config only (no code changes)
- [ ] Contrast ratios valid for all brand color combinations
- [ ] Typography renders correctly with all brand fonts

## Quality Criteria

- Zero brand-specific code in components (only tokens)
- Brand switching is instant (CSS-only, no JS re-render)
- New brands addable via configuration file only
- All brand + theme combinations pass contrast checks

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Isolation | Zero brand-specific code in components |
| Extensibility | New brand via config only |
| A11y | Contrast valid for all brand+theme combos |
| Runtime | Switch without reload |

## Handoff

- Brand tokens feed `@css-eng` for CSS custom property implementation
- Contrast validation feeds `@a11y-eng` for WCAG compliance per brand
- Brand config feeds `@react-eng` for provider/context design
