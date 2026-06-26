> **DEPRECATED** — Scope absorbed into `storybook-docs.md`. See `data/task-consolidation-map.yaml`.

---
id: ds-documentation-automation
version: "1.0.0"
title: "Design System Documentation Automation"
description: "Auto-generate design system documentation from code: component API docs, token catalogs, usage examples, and interactive showcases"
elicit: true
owner: design-sys-eng
executor: design-sys-eng
outputs:
  - ds-documentation-spec.md
  - documentation-config.yaml
---

# Design System Documentation Automation

## When This Task Runs

- Design system needs living documentation
- Component API documentation is outdated or missing
- Token catalog needs visual representation
- Team needs interactive component playground

## Execution Steps

### Step 1: Audit Current Documentation

```
SCAN project for existing DS docs:
- Storybook stories (.stories.tsx)
- JSDoc/TSDoc on components
- README files in component directories
- Token documentation
- Usage guidelines

OUTPUT: Documentation coverage map + gaps
```

### Step 2: Select Documentation Strategy

**elicit: true** — Choose documentation approach:

| Approach | Auto-generated | Interactive | Best For |
|----------|---------------|-------------|----------|
| **Storybook** | Partial (autodocs) | Yes | Component playground, visual testing |
| **Docusaurus + MDX** | No | Partial | Guidelines, principles, written docs |
| **Styleguidist** | Yes (from props) | Yes | Quick API docs from PropTypes/TS |
| **Custom (Next.js)** | Configurable | Yes | Full control, branded docs site |

### Step 3: Design Component Documentation Template

```yaml
component_doc_template:
  sections:
    - name: "Overview"
      source: "Component TSDoc @description"
      auto: true

    - name: "Props / API"
      source: "TypeScript interface (auto-extracted)"
      auto: true
      format: "Table with name, type, default, description"

    - name: "Variants"
      source: "Storybook stories or manual examples"
      auto: "partial"
      format: "Live preview + code snippet"

    - name: "Usage Guidelines"
      source: "Manual — when to use, when NOT to use"
      auto: false

    - name: "Accessibility"
      source: "ARIA roles, keyboard interaction, screen reader behavior"
      auto: false

    - name: "Related Components"
      source: "Auto-detected from imports"
      auto: true
```

### Step 4: Design Token Documentation

```yaml
token_documentation:
  color_tokens:
    display: "Swatch grid with hex, HSL, contrast ratio"
    grouping: "By semantic category (surface, text, action, status)"
    dark_mode: "Side-by-side light/dark comparison"

  spacing_tokens:
    display: "Visual scale with px values"
    format: "Horizontal bars showing relative sizes"

  typography_tokens:
    display: "Live text samples at each size/weight"
    format: "Font family, size, weight, line-height, letter-spacing"

  shadow_tokens:
    display: "Card previews with each shadow level"

  radius_tokens:
    display: "Shape previews with each radius value"

  auto_generation:
    source: "CSS custom properties or Tailwind config"
    tool: "Custom script or Style Dictionary"
    update_trigger: "On token file change (watch mode)"
```

### Step 5: Set Up Auto-Documentation Pipeline

```yaml
pipeline:
  prop_extraction:
    tool: "react-docgen-typescript | typedoc"
    trigger: "On component file change"
    output: "JSON prop definitions"

  story_generation:
    tool: "Storybook autodocs"
    trigger: "On component export"
    output: "Auto-generated story with controls"

  token_catalog:
    tool: "Style Dictionary | custom script"
    trigger: "On token file change"
    output: "Token documentation page"

  ci_validation:
    check: "Every component has at least 1 story"
    check: "Every exported prop has a description"
    check: "Token catalog is up-to-date"
```

### Step 6: Validate Documentation

- [ ] Every exported component has API documentation
- [ ] All props have type and description
- [ ] Token catalog matches actual CSS custom properties
- [ ] Examples are copy-pasteable and work
- [ ] Documentation builds without errors
- [ ] Auto-update pipeline functional

## Quality Criteria

- 100% prop documentation coverage for exported components
- Token catalog auto-generated from source code
- Examples are tested (compile and render correctly)
- Documentation updates on code changes

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Coverage | Every component has prop docs |
| Tokens | Catalog matches source |
| Examples | All examples compile |
| Pipeline | Auto-update functional |

## Handoff

- Component docs feed team onboarding
- Token catalog feeds `@css-eng` for style reference
- Storybook stories feed `@qa-visual` for visual regression tests
