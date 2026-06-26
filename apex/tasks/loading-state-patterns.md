---
id: loading-state-patterns
version: "1.0.0"
title: "Loading State UX Patterns"
description: "Design loading experiences: skeleton screens, shimmer effects, progressive loading, optimistic UI, and perceived performance patterns"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - loading-patterns-spec.md
  - loading-component-specs.yaml
---

# Loading State UX Patterns

## When This Task Runs

- Component needs loading/skeleton state design
- Page has perceived performance issues (feels slow)
- New data-fetching flow needs loading UX
- Optimistic UI pattern needed for form submissions

## Execution Steps

### Step 1: Audit Current Loading States
```
SCAN project for loading patterns:
- Existing skeleton components
- Spinner/loader usage
- Conditional rendering (isLoading && ...)
- Suspense boundaries and fallbacks
- Empty loading states (blank screens)

OUTPUT: Loading pattern inventory + gaps
```

### Step 2: Classify Loading Scenarios

**elicit: true** — Present scenarios for user prioritization:

| Scenario | Current | Recommended |
|----------|---------|-------------|
| **Initial page load** | ? | Skeleton matching final layout |
| **Data refresh** | ? | Keep stale + subtle refresh indicator |
| **Form submission** | ? | Optimistic UI + rollback on error |
| **Image loading** | ? | Blur-up placeholder → sharp image |
| **Infinite scroll** | ? | Skeleton rows at bottom |
| **Navigation** | ? | Instant shell + streaming content |
| **Background sync** | ? | Toast/indicator only, no blocking UI |

### Step 3: Design Skeleton Components

For each identified loading scenario:

```yaml
skeleton:
  name: "{ComponentName}Skeleton"
  matches_layout: true  # MUST match final component dimensions
  animation: "shimmer"  # shimmer | pulse | wave | none
  shimmer_direction: "ltr"
  reduced_motion: "pulse"  # Fallback for vestibular safety
  elements:
    - type: "rect"  # rect | circle | text-line
      width: "{exact or range}"
      height: "{exact or range}"
      radius: "{border-radius}"
  transition_to_content: "fade-crossfade"  # fade | instant | morph
  duration: "200ms"
```

### Step 4: Design Optimistic UI Patterns

For mutation operations (create, update, delete):

```yaml
optimistic_ui:
  action: "{mutation type}"
  immediate_feedback: "{what user sees instantly}"
  pending_indicator: "{subtle indicator: opacity, badge, spinner}"
  success_confirmation: "{toast, animation, state change}"
  failure_rollback: "{revert UI + error message}"
  retry_mechanism: "{auto-retry with exponential backoff or manual}"
```

### Step 5: Define Loading Hierarchy

```
Priority 1: Content skeleton (above-the-fold)
Priority 2: Navigation shell (instant)
Priority 3: Secondary content (below-fold, lazy)
Priority 4: Background data (silent refresh)
Priority 5: Prefetch (anticipatory loading)
```

### Step 6: Validate Loading Experience

- [ ] No blank screens during data loading
- [ ] Skeleton matches final layout dimensions (no layout shift)
- [ ] Optimistic UI rolls back cleanly on error
- [ ] Loading states respect `prefers-reduced-motion`
- [ ] Perceived performance: content visible within 200ms (skeleton or cached)
- [ ] No content flash (skeleton shows for minimum 200ms to avoid flicker)

## Quality Criteria

- Every async operation has a designed loading state
- Skeletons are exact geometric matches of final content
- Optimistic UI includes error rollback path
- CLS impact is zero (skeleton → content transition)
- Minimum display time prevents flash-of-skeleton

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Coverage | Every async flow has loading design |
| Layout stability | CLS = 0 during skeleton→content |
| Optimistic UI | Rollback tested for every mutation |
| A11y | `aria-busy`, `aria-live` on loading regions |

## Handoff

- Skeleton specs feed `@react-eng` for Suspense boundary design
- Optimistic UI specs feed `@react-eng` for server action patterns
- Performance metrics feed `@perf-eng` for CWV impact assessment
