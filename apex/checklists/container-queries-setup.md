# Checklist: Container Queries Setup

> **Purpose:** One-time introduction of CSS Container Queries for component-level responsive design. Migrates from viewport-based `@media` to container-based `@container` where appropriate.

---

## Prerequisites

- [ ] Browser support acceptable: Chrome 105+, Firefox 110+, Safari 16+ (~95% global)
- [ ] Identify whether Tailwind CSS `@tailwindcss/container-queries` plugin is available

## Step 1: Identify Container Query Candidates

Use this decision matrix:

| Use `@media` | Use `@container` |
|-------------|------------------|
| Page layout (2-col to 1-col) | Card adapts in sidebar vs main |
| Navigation collapses on small screen | Widget works in any panel size |
| Typography scales with viewport | Component in modal vs full page |

- [ ] List all components used in multiple layout contexts
- [ ] List all components whose layout depends on own width (not page width)
- [ ] List design system primitives (Card, Panel, Widget) — candidates for `@container`
- [ ] Confirm page-level scaffolds (Header, Sidebar, Main) stay with `@media`

## Step 2: Define Containment Strategy

- [ ] Default to `container-type: inline-size` (width-only, preserves auto-height)
- [ ] Use `container-type: size` ONLY if querying height (rare)
- [ ] Document containment type chosen for each container with rationale

## Step 3: Establish Naming Conventions

- [ ] Pattern: `container-name: {component}` (e.g., `card`, `sidebar`, `widget`)
- [ ] Define container breakpoint tokens:
  - `--cq-sm: 320px` (compact, stacked)
  - `--cq-md: 480px` (side-by-side possible)
  - `--cq-lg: 640px` (full layout with details)
  - `--cq-xl: 800px` (expanded layout)
- [ ] If using Tailwind: use `@container/{name}` syntax (e.g., `@container/card`)

## Step 4: Design Browser Fallback

- [ ] Choose fallback strategy:
  - `@supports` with `@media` fallback (recommended, low complexity)
  - ResizeObserver polyfill (medium complexity)
  - Progressive enhancement / no fallback (if audience supports it)
- [ ] Implement `@supports (container-type: inline-size)` pattern
- [ ] Test: older browsers get usable layout via `@media` fallback

## Step 5: Create Migration Plan

Per component:
- [ ] Add `container-type: inline-size` to parent element
- [ ] Add `container-name` for clarity
- [ ] Convert `@media (min-width: Xpx)` to `@container name (min-width: Xpx)`
- [ ] Adjust breakpoint values (container width != viewport width):
  - 768px viewport ~ 480px container
  - 1024px viewport ~ 640px container
  - 1280px viewport ~ 800px container
- [ ] Test in all layout contexts (sidebar, main, modal, full-width)
- [ ] Add `@supports` fallback if needed
- [ ] Remove old `@media` rule once verified

## Step 6: Document Architecture

- [ ] Candidate audit results
- [ ] Containment strategy guide
- [ ] Naming conventions reference
- [ ] Browser fallback strategy
- [ ] Migration plan with timeline
- [ ] `@media` vs `@container` decision tree
- [ ] Common pitfalls: height collapse, nested containers, specificity

## Quality Gate

- [ ] All containers use `inline-size` unless height queries are explicitly needed
- [ ] All containers have a `container-name`
- [ ] Fallback strategy maintains usable layout on older browsers
- [ ] Components tested in at least 3 different container sizes
- [ ] No viewport-based media queries inside container-queried components

---

*Converted from `tasks/container-queries-setup.md` — Squad Apex v1.0.0*
