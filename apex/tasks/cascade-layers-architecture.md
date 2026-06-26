> **DEPRECATED** — Scope absorbed into `css-architecture-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: cascade-layers-architecture

```yaml
id: cascade-layers-architecture
version: "1.0.0"
title: "CSS Cascade Layers Architecture"
description: >
  Designs the CSS Cascade Layers (@layer) architecture for predictable
  specificity management. Defines layer ordering, integrates with
  Tailwind CSS, handles third-party CSS, eliminates specificity wars,
  and produces a cascade architecture that makes CSS maintainable
  at scale without !important hacks.
elicit: false
owner: css-eng
executor: css-eng
outputs:
  - Layer hierarchy design
  - Layer ordering declaration
  - Tailwind integration strategy
  - Third-party CSS isolation
  - Migration plan from specificity-based to layer-based cascade
  - Cascade layers specification document
```

---

## When This Task Runs

This task runs when:
- CSS specificity conflicts are frequent (`!important` appearing regularly)
- Third-party CSS overrides project styles unpredictably
- Tailwind utilities need guaranteed override of component styles
- Design system needs clear style hierarchy (tokens → base → components → utilities)
- `*cascade-layers` or `*layers-arch` is invoked

This task does NOT run when:
- Small project with minimal CSS conflicts
- CSS-in-JS exclusively (styled-components manages specificity)
- The issue is about container queries (use `container-queries-setup`)

---

## Execution Steps

### Step 1: Design Layer Hierarchy

Define the cascade layer order from lowest to highest priority.

**Recommended layer hierarchy:**
```css
/* Layer declaration — ORDER defines priority (last = highest) */
@layer reset, base, tokens, components, patterns, utilities, overrides;
```

| Layer | Priority | Contents | Example |
|-------|----------|----------|---------|
| `reset` | Lowest | CSS reset / normalize | `*, *::before { box-sizing: border-box }` |
| `base` | Low | HTML element defaults | `body { font-family: var(--font-sans) }` |
| `tokens` | Low-mid | Design token variables | `:root { --color-primary: #3b82f6 }` |
| `components` | Mid | Component styles | `.card { border-radius: var(--radius-md) }` |
| `patterns` | Mid-high | Layout patterns | `.stack { display: flex; flex-direction: column }` |
| `utilities` | High | Utility classes (Tailwind) | `.text-center { text-align: center }` |
| `overrides` | Highest | Forced overrides (rare) | Dark mode, RTL, print styles |

**Key insight:** Unlayered CSS has higher priority than ALL layered CSS. This is critical for Tailwind integration.

**Output:** Layer hierarchy with rationale for each layer.

### Step 2: Configure Layer Ordering

Implement the layer declaration and organize existing CSS.

**Global CSS entry point:**
```css
/* global.css — single source of layer ordering */

/* 1. Declare layer order */
@layer reset, base, tokens, components, patterns, utilities, overrides;

/* 2. Import third-party CSS into isolated layers */
@import url('normalize.css') layer(reset);

/* 3. Project styles */
@layer base {
  body {
    font-family: var(--font-sans);
    color: var(--color-content);
    background: var(--color-surface);
  }
  a { color: var(--color-primary); }
}

@layer tokens {
  :root {
    --color-primary: #3b82f6;
    --color-surface: #ffffff;
    --font-sans: 'Inter', system-ui, sans-serif;
    --radius-md: 8px;
  }
  .dark {
    --color-surface: #0f172a;
  }
}

@layer components {
  .btn { /* button styles */ }
  .card { /* card styles */ }
  .input { /* input styles */ }
}

@layer overrides {
  /* Print styles */
  @media print {
    .no-print { display: none; }
  }
}
```

**Output:** Layer ordering declaration with style distribution.

### Step 3: Integrate with Tailwind CSS

Ensure Tailwind utilities always override component styles.

**Tailwind + Layers configuration:**
```css
/* With Tailwind v3.4+ */
@layer base {
  @tailwind base;
}

@layer components {
  @tailwind components;
}

@layer utilities {
  @tailwind utilities;
}
```

**How this solves specificity:**
```css
/* Component layer — lower priority */
@layer components {
  .btn { color: blue; }
}

/* Utility layer — higher priority (always wins) */
@layer utilities {
  .text-red-500 { color: red; }
}

/* <button class="btn text-red-500"> → red (utility wins, no !important needed) */
```

**Tailwind config integration:**
```javascript
// tailwind.config.js
module.exports = {
  important: false, // No need for !important with layers
  corePlugins: {
    preflight: true, // Goes into reset/base layer
  },
};
```

**Output:** Tailwind integration with cascade layers.

### Step 4: Isolate Third-Party CSS

Prevent third-party styles from interfering with project styles.

**Import third-party CSS into dedicated layers:**
```css
/* Third-party CSS gets lowest priority automatically */
@import url('some-library/styles.css') layer(vendor);

/* Update layer order to include vendor */
@layer reset, vendor, base, tokens, components, patterns, utilities, overrides;
```

**Handling inline third-party styles:**
```css
/* If library injects styles at runtime, wrap with layer */
@layer vendor {
  /* Paste or @import library CSS here */
  .third-party-widget { /* their styles */ }
}
```

**Specificity comparison:**
| Without layers | With layers |
|---------------|-------------|
| Third-party `.btn` (specificity 0,1,0) vs your `.btn` (specificity 0,1,0) → source order wins (fragile) | Third-party in `vendor` layer vs your `components` layer → your layer wins (predictable) |
| Fix: `!important` or increase specificity | Fix: not needed, layers handle it |

**Output:** Third-party CSS isolation strategy.

### Step 5: Create Migration Plan

Migrate existing CSS from specificity-based to layer-based cascade.

**Migration steps:**
1. Add `@layer` declaration at top of global CSS
2. Wrap existing reset/normalize in `@layer reset`
3. Wrap design token variables in `@layer tokens`
4. Wrap component styles in `@layer components`
5. Configure Tailwind to output into `utilities` layer
6. Remove all `!important` declarations (layers make them unnecessary)
7. Remove specificity hacks (double-class `.btn.btn`, ID selectors for override)
8. Test each layer in isolation (disable higher layers, verify lower layers work)

**Audit checklist before migration:**
- Count `!important` declarations (all should be removable)
- Identify specificity conflicts in browser DevTools
- Map third-party CSS injection points
- Verify browser support (Chrome 99+, Firefox 97+, Safari 15.4+)

**Output:** Step-by-step migration plan with rollback points.

### Step 6: Document Cascade Layers Architecture

Compile the complete specification.

**Documentation includes:**
- Layer hierarchy diagram (from Step 1)
- Layer ordering code (from Step 2)
- Tailwind integration guide (from Step 3)
- Third-party isolation patterns (from Step 4)
- Migration plan (from Step 5)
- Debugging guide (Chrome DevTools → Styles → Layer badges)
- Common mistakes (unlayered CSS beats layered, nested layer specificity)

**Output:** Complete cascade layers specification document.

---

## Quality Criteria

- Layer ordering must be declared once in a single file
- No `!important` declarations in layered CSS
- Tailwind utilities must always override component styles without hacks
- Third-party CSS must be isolated in its own layer
- All specificity conflicts must be resolved by layer order, not selector weight

---

*Squad Apex — CSS Cascade Layers Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-cascade-layers-architecture
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Layer ordering declared once in single file"
    - "Zero !important declarations in project CSS"
    - "Tailwind utilities override components without hacks"
    - "Third-party CSS isolated in dedicated layer"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@design-sys-eng` or `@apex-lead` |
| Artifact | Cascade layers architecture with hierarchy, Tailwind integration, and migration plan |
| Next action | Apply to design system via `@design-sys-eng` or validate via `@qa-visual` |
