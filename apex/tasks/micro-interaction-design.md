> **DEPRECATED** — Scope absorbed into `animation-architecture.md`. See `data/task-consolidation-map.yaml`.

---
id: micro-interaction-design
version: "1.0.0"
title: "Micro-Interaction Design Library"
description: "Design and catalog micro-interactions: hover states, button feedback, state transitions, skeleton-to-content reveals, and subtle cues that communicate system status"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - micro-interaction-catalog.md
  - interaction-tokens.yaml
---

# Micro-Interaction Design Library

## When This Task Runs

- User requests hover/click/press feedback design
- New component needs state transition animations
- Design system needs standardized micro-interactions
- Apex routes interaction refinement requests here

## Execution Steps

### Step 1: Inventory Current Micro-Interactions
```
SCAN project for existing micro-interactions:
- CSS :hover, :focus, :active pseudo-classes
- Framer Motion/React Spring inline animations
- Tailwind transition-* / animate-* usage
- onClick/onPress visual feedback patterns

OUTPUT: Current interaction inventory with gaps
```

### Step 2: Define Interaction Categories

**elicit: true** — Ask user which categories to prioritize:

| Category | Examples | Priority |
|----------|----------|----------|
| **Hover feedback** | Scale, glow, color shift, underline reveal | - |
| **Press/click** | Depress, ripple, flash, haptic-visual | - |
| **State transitions** | Loading→content, enabled→disabled, open→closed | - |
| **Skeleton reveals** | Shimmer→content, progressive disclosure | - |
| **Scroll cues** | Parallax, fade-in, sticky transitions | - |
| **Drag & drop** | Ghost, snap, drop zone highlight | - |
| **Toggle** | Switch morph, checkbox animation, radio pulse | - |

### Step 3: Design Each Micro-Interaction

For each prioritized category:

```yaml
interaction:
  name: "{descriptive-name}"
  trigger: "{user action or system event}"
  duration: "{ms range — 100-300ms for micro, 300-600ms for transitions}"
  easing: "{spring config or cubic-bezier}"
  properties_animated:
    - "{transform, opacity, color, etc.}"
  reduced_motion_fallback: "{instant state change or opacity-only}"
  implementation:
    css: "{Tailwind classes or custom CSS}"
    motion_lib: "{Framer Motion / React Spring config}"
  a11y_notes: "{vestibular safety, focus visibility, ARIA}"
```

### Step 4: Create Interaction Token System

Map micro-interactions to design tokens:
```css
--interaction-hover-scale: 1.02;
--interaction-hover-duration: 150ms;
--interaction-press-scale: 0.98;
--interaction-press-duration: 100ms;
--interaction-transition-duration: 300ms;
--interaction-skeleton-shimmer-duration: 1.5s;
```

### Step 5: Validate Micro-Interactions

For each designed interaction:
- [ ] Duration within range (no jarring or sluggish feel)
- [ ] `prefers-reduced-motion` fallback defined
- [ ] GPU-accelerated properties only (transform, opacity)
- [ ] No layout shift during interaction
- [ ] Works with keyboard focus (not hover-only)
- [ ] Touch target preserved during animation

## Quality Criteria

- All micro-interactions have reduced-motion fallback
- No interaction exceeds 600ms (perceptual instant threshold)
- Animations use GPU-composited properties only
- Interaction tokens are extractable for design system
- Each interaction has clear trigger → feedback → completion arc

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Duration budget | All under 600ms |
| A11y | reduced-motion fallback for every interaction |
| Performance | Only transform/opacity animated |
| Consistency | Shared tokens, not ad-hoc values |

## Handoff

- Interaction catalog feeds `@motion-eng` for spring configs
- Tokens feed `@design-sys-eng` for design system integration
- A11y notes feed `@a11y-eng` for vestibular safety review
