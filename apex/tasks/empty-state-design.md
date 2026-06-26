---
id: empty-state-design
version: "1.0.0"
title: "Empty State Design System"
description: "Design empty states for all scenarios: first-use, no-results, error-cleared, filtered-empty, and data-deleted with appropriate CTAs and illustrations"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - empty-state-catalog.md
  - empty-state-specs.yaml
---

# Empty State Design System

## When This Task Runs

- Component/page needs empty state design
- Audit reveals blank screens where data is absent
- New feature needs first-use onboarding state
- Search/filter results in zero matches

## Execution Steps

### Step 1: Inventory Empty State Scenarios
```
SCAN project for empty state opportunities:
- Pages/components that render lists/collections
- Search results areas
- Dashboard widgets with no data
- First-time user screens
- Error recovery screens (after clearing error)
- Filtered views that can return zero results

OUTPUT: Empty state opportunity map
```

### Step 2: Classify Empty State Types

**elicit: true** — Confirm which types apply to the project:

| Type | Trigger | Goal |
|------|---------|------|
| **First-use** | User just signed up, no data yet | Guide to first action |
| **No results** | Search/filter returns empty | Help refine or suggest alternatives |
| **Error-cleared** | After error recovery, data lost | Explain and guide to re-create |
| **Data deleted** | User deleted all items | Confirm action, suggest next |
| **Permission denied** | User lacks access to content | Explain and provide path to access |
| **Maintenance** | Feature temporarily unavailable | Set expectations, provide ETA |
| **Offline** | No network connection | Show cached or explain limitation |

### Step 3: Design Each Empty State

For each applicable type:

```yaml
empty_state:
  type: "{first-use | no-results | error-cleared | ...}"
  context: "{where this appears}"
  visual:
    illustration: "{description of illustration/icon}"
    style: "{consistent with project design language}"
    size: "{proportional to container}"
  copy:
    headline: "{clear, empathetic headline}"
    description: "{1-2 sentences explaining why empty and what to do}"
    tone: "{friendly, not blaming the user}"
  cta:
    primary: "{main action to resolve empty state}"
    secondary: "{alternative action or learn more}"
  a11y:
    role: "status"
    aria_live: "polite"
    focus_management: "{where focus goes}"
```

### Step 4: Define Empty State Hierarchy

```
1. Illustration/icon (visual anchor)
2. Headline (what happened)
3. Description (why + what to do)
4. Primary CTA (resolve the empty state)
5. Secondary link (alternative path)
```

### Step 5: Validate Empty States

- [ ] Every list/collection has an empty state designed
- [ ] CTAs are actionable and lead to resolution
- [ ] Copy is empathetic (no "Nothing found" or blank screens)
- [ ] Illustrations match project design language
- [ ] Empty states are responsive (work on mobile)
- [ ] Screen readers announce empty state with context

## Quality Criteria

- No blank screens in any data-absent scenario
- Every empty state has at least one actionable CTA
- Copy is user-friendly, not developer-centric
- Illustrations are consistent across all empty states
- A11y: proper `role`, `aria-live` for dynamic empty states

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Coverage | Every data-dependent view has empty state |
| CTA | All empty states have actionable next step |
| Copy quality | No technical jargon in user-facing text |
| A11y | Screen reader announces empty state contextually |

## Handoff

- Visual specs feed `@css-eng` for styling implementation
- Illustration requests feed `@design-sys-eng` for icon/illustration system
- A11y requirements feed `@a11y-eng` for screen reader testing
