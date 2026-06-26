> **DEPRECATED** — Converted to checklist at `checklists/container-queries-setup.md`. See `data/task-consolidation-map.yaml` for details.

---

# Task: container-queries-setup

```yaml
id: container-queries-setup
version: "1.0.0"
title: "Container Queries Architecture"
description: >
  Designs and implements CSS Container Queries for component-level
  responsive design. Migrates from viewport-based @media to container-based
  @container queries where appropriate. Defines containment strategy,
  establishes naming conventions, handles fallbacks for older browsers,
  and produces responsive components that adapt to their container, not
  the viewport.
elicit: false
owner: css-eng
executor: css-eng
outputs:
  - Container query adoption strategy
  - Containment type selection guide
  - Named container conventions
  - Browser fallback strategy
  - Migration plan from @media to @container
  - Container queries specification document
```

---

## When This Task Runs

This task runs when:
- Components need to respond to their container size, not the viewport
- A component is reused in different layout contexts (sidebar, main, modal)
- Card layouts need to adapt their internal layout based on available space
- Design system components need intrinsic responsive behavior
- `*container-queries` or `*cq-setup` is invoked

This task does NOT run when:
- Page-level layout changes (use `@media` queries)
- Only viewport breakpoints needed (standard responsive design)
- React Native styling (container queries are CSS-only)

---

## Execution Steps

### Step 1: Identify Container Query Candidates

Audit components to determine which benefit from container queries vs media queries.

**Decision matrix:**
| Scenario | Use @media | Use @container |
|----------|-----------|---------------|
| Page layout (2-col → 1-col) | Yes | No |
| Card adapts in sidebar vs main | No | Yes |
| Navigation collapses on small screen | Yes | No |
| Widget works in any panel size | No | Yes |
| Typography scales with viewport | Yes (or clamp) | No |
| Component in modal vs full page | No | Yes |

**Candidate identification checklist:**
- Is the component used in multiple layout contexts? → Container query
- Does the component's layout depend on its own width, not the page? → Container query
- Is the component a design system primitive (Card, Panel, Widget)? → Container query
- Is it a page-level scaffold (Header, Sidebar, Main)? → Media query

**Output:** List of components to migrate to container queries.

### Step 2: Define Containment Strategy

Choose the correct containment type for each container.

**Containment types:**
| Type | CSS | What it does | When to use |
|------|-----|-------------|-------------|
| `size` | `container-type: size` | Width AND height containment | Rare — only if querying height |
| `inline-size` | `container-type: inline-size` | Width containment only | Most common — responsive width |
| `normal` | `container-type: normal` | Style containment only | Style queries without size |

**Why `inline-size` is default:**
- `size` containment breaks auto-height (element collapses)
- `inline-size` only constrains width, height remains natural
- 99% of responsive design is width-based

**Container setup pattern:**
```css
/* Define the container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container */
@container card (min-width: 400px) {
  .card-content {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (max-width: 399px) {
  .card-content {
    display: flex;
    flex-direction: column;
  }
}
```

**Tailwind CSS container queries:**
```html
<!-- With @tailwindcss/container-queries plugin -->
<div class="@container">
  <div class="flex flex-col @md:flex-row @lg:grid @lg:grid-cols-3">
    <!-- Adapts to container, not viewport -->
  </div>
</div>
```

**Output:** Containment type selection for each identified container.

### Step 3: Establish Naming Conventions

Create consistent naming for containers across the design system.

**Naming rules:**
```css
/* Pattern: [component]-container */
.card-container { container-name: card; }
.sidebar-container { container-name: sidebar; }
.widget-container { container-name: widget; }
.panel-container { container-name: panel; }
```

**Container breakpoint tokens:**
```css
:root {
  --cq-sm: 320px;   /* Compact: single column, stacked */
  --cq-md: 480px;   /* Medium: side-by-side possible */
  --cq-lg: 640px;   /* Large: full layout with details */
  --cq-xl: 800px;   /* Extra large: expanded layout */
}

@container card (min-width: 480px) { /* md breakpoint */ }
@container card (min-width: 640px) { /* lg breakpoint */ }
```

**Tailwind convention:**
```html
<!-- @sm = 320px, @md = 480px, @lg = 640px (container-relative) -->
<div class="@container/card">
  <div class="@md/card:flex-row">...</div>
</div>
```

**Output:** Container naming conventions and breakpoint tokens.

### Step 4: Design Browser Fallback Strategy

Handle browsers that don't support container queries.

**Browser support (2024+):** Chrome 105+, Firefox 110+, Safari 16+
- ~95% global support — fallbacks needed for older browsers only

**Fallback strategies:**
| Strategy | Complexity | Reliability |
|----------|-----------|-------------|
| `@supports` with media query fallback | Low | High |
| ResizeObserver polyfill | Medium | Medium |
| Progressive enhancement (no fallback) | None | Depends on audience |

**@supports fallback pattern:**
```css
/* Default: media query fallback */
@media (min-width: 768px) {
  .card-content { flex-direction: row; }
}

/* Enhancement: container query overrides media query */
@supports (container-type: inline-size) {
  .card-container { container-type: inline-size; }

  @container card (min-width: 400px) {
    .card-content { flex-direction: row; }
  }

  /* Remove the media query behavior */
  @media (min-width: 768px) {
    .card-content { flex-direction: column; } /* Reset */
  }
}
```

**Output:** Browser fallback strategy with progressive enhancement.

### Step 5: Create Migration Plan

Plan migration from @media to @container for identified components.

**Migration steps per component:**
1. Add `container-type: inline-size` to parent element
2. Add `container-name` for clarity
3. Convert `@media (min-width: Xpx)` to `@container name (min-width: Xpx)`
4. Adjust breakpoint values (container width ≠ viewport width)
5. Test in all layout contexts (sidebar, main, modal, full-width)
6. Add `@supports` fallback if needed
7. Remove old `@media` rule once verified

**Breakpoint mapping (viewport → container):**
| Viewport @media | Container @container | Rationale |
|-----------------|---------------------|-----------|
| 768px (md) | 480px | Component is never viewport-width |
| 1024px (lg) | 640px | Adjusted for container context |
| 1280px (xl) | 800px | Full-width container rare |

**Output:** Migration plan with per-component steps and timeline.

### Step 6: Document Container Queries Architecture

Compile the complete container queries specification.

**Documentation includes:**
- Candidate audit results (from Step 1)
- Containment strategy guide (from Step 2)
- Naming conventions (from Step 3)
- Browser fallback strategy (from Step 4)
- Migration plan (from Step 5)
- Quick reference: @media vs @container decision tree
- Common pitfalls (height collapse, nested containers, specificity)

**Output:** Complete container queries specification document.

---

## Quality Criteria

- Containment type must be `inline-size` unless height queries are explicitly needed
- All containers must have a `container-name` for clarity
- Fallback strategy must maintain usable layout on older browsers
- Components must be tested in at least 3 different container sizes
- No viewport-based media queries inside container-queried components

---

*Squad Apex — Container Queries Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-container-queries-setup
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Containment type justified for each container"
    - "All containers have named container-name"
    - "Fallback strategy tested on target browsers"
    - "Components tested in 3+ container sizes"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@design-sys-eng` or `@apex-lead` |
| Artifact | Container queries architecture with naming conventions, fallback strategy, and migration plan |
| Next action | Integrate with design system via `@design-sys-eng` or validate responsiveness via `@qa-visual` |
