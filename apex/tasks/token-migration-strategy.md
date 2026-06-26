> **DEPRECATED** — Scope absorbed into `token-architecture.md`. See `data/task-consolidation-map.yaml`.

---
id: token-migration-strategy
version: "1.0.0"
title: "Design Token Migration Strategy"
description: "Plan and execute migration from hardcoded values to design tokens: automated codemods, phased rollout, validation gates, and rollback strategy"
elicit: true
owner: design-sys-eng
executor: design-sys-eng
outputs:
  - token-migration-plan.md
  - codemod-config.yaml
---

# Design Token Migration Strategy

## When This Task Runs

- `*discover-design` reveals high hardcoded value count
- Design system adoption needs acceleration
- New token system replacing legacy values
- Brand refresh requires systematic value updates

## Execution Steps

### Step 1: Audit Hardcoded Values
```
SCAN project using *discover-design output:
- Hardcoded hex colors (#fff, #000, rgb())
- Hardcoded pixel values (12px, 16px, 24px)
- Hardcoded font sizes (14px, 1rem)
- Hardcoded shadows, border-radius
- Near-duplicate values (colors within 5% HSL distance)

OUTPUT: Value inventory + token mapping candidates
```

### Step 2: Create Token Mapping Table

**elicit: true** — Confirm token mappings:

| Hardcoded Value | Occurrences | Proposed Token | Confidence |
|-----------------|-------------|----------------|------------|
| `#0ea5e9` | 14 | `--color-accent` | High |
| `#1e293b` | 8 | `--color-surface-dark` | High |
| `16px` | 23 | `--spacing-4` | Medium |
| `0.75rem` | 5 | `--font-size-sm` | Medium |

### Step 3: Design Migration Phases

```yaml
migration_phases:
  phase_1:
    name: "Foundation tokens"
    scope: "Colors only (highest impact, easiest to validate)"
    files: "CSS custom properties, Tailwind config"
    validation: "Visual diff — no pixel changes"
    rollback: "Git revert phase-1 commit"

  phase_2:
    name: "Spacing & typography"
    scope: "Spacing scale, font sizes, line heights"
    files: "Component styles, utility classes"
    validation: "Layout regression tests"
    rollback: "Git revert phase-2 commit"

  phase_3:
    name: "Component tokens"
    scope: "Shadows, border-radius, z-index, transitions"
    files: "Component-specific styles"
    validation: "Full visual regression suite"
    rollback: "Git revert phase-3 commit"

  phase_4:
    name: "Cleanup & enforcement"
    scope: "Remove all remaining hardcoded values"
    files: "Entire codebase"
    validation: "Lint rule blocks new hardcoded values"
    rollback: "N/A — enforcement only"
```

### Step 4: Design Codemod Rules

```yaml
codemods:
  - name: "color-to-token"
    match: "color: #0ea5e9"
    replace: "color: var(--color-accent)"
    scope: "*.css, *.tsx (inline styles)"

  - name: "spacing-to-token"
    match: "margin: 16px"
    replace: "margin: var(--spacing-4)"
    scope: "*.css"

  - name: "tailwind-arbitrary-to-config"
    match: "text-[#0ea5e9]"
    replace: "text-accent"
    scope: "*.tsx"
    requires: "Tailwind config updated with accent color"
```

### Step 5: Define Validation Gates

```yaml
validation_per_phase:
  pre_migration:
    - "Screenshot baseline of all pages"
    - "Token mapping table approved by user"

  post_migration:
    - "Visual diff: zero pixel differences"
    - "Lint: no new hardcoded values introduced"
    - "TypeScript: no type errors from token changes"
    - "Dark mode: tokens resolve correctly in both themes"

  enforcement:
    - "ESLint rule: no-hardcoded-colors"
    - "Stylelint rule: no-hardcoded-spacing"
    - "CI: blocks PRs with hardcoded values"
```

### Step 6: Validate Migration

- [ ] All hardcoded values mapped to tokens
- [ ] Visual regression: zero pixel changes after migration
- [ ] Dark mode works with new tokens
- [ ] Lint rules prevent new hardcoded values
- [ ] Each phase is independently revertible

## Quality Criteria

- Zero visual changes after token migration
- 100% of color values use tokens (no hardcoded hex)
- Lint enforcement prevents regression
- Each phase has rollback procedure

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Visual | Zero pixel diff pre/post migration |
| Coverage | 100% color values tokenized |
| Enforcement | Lint blocks new hardcoded values |
| Dark mode | Tokens resolve in all themes |

## Handoff

- Token system feeds `@css-eng` for CSS architecture
- Visual validation feeds `@qa-visual` for regression testing
- Lint rules feed `@frontend-arch` for CI configuration
