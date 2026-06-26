> **DEPRECATED** — Scope absorbed into `rsc-architecture.md`. See `data/task-consolidation-map.yaml`.

---
id: suspense-architecture
version: "1.0.0"
title: "Suspense & Streaming Architecture"
description: "Design Suspense boundary placement, nested loading strategies, streaming SSR configuration, error boundary integration, and fallback hierarchy"
elicit: true
owner: react-eng
executor: react-eng
outputs:
  - suspense-architecture-spec.md
  - boundary-placement-map.yaml
---

# Suspense & Streaming Architecture

## When This Task Runs

- Page has multiple async data sources with different speeds
- Loading experience needs improvement (all-or-nothing → progressive)
- Nested Suspense strategy needed for complex layouts
- Error boundary + Suspense integration required

## Execution Steps

### Step 1: Map Async Dependencies
```
For target page/feature:
- List all async data sources (DB queries, API calls, external services)
- Measure/estimate latency for each source
- Identify dependencies (does B need A's result?)
- Identify independent data (can load in parallel)

OUTPUT: Async dependency graph with latency estimates
```

### Step 2: Design Boundary Placement

**elicit: true** — Review proposed Suspense tree:

```yaml
boundary_strategy:
  principles:
    - "One Suspense per independent data source"
    - "Shared skeleton for co-dependent data"
    - "Instant shell first, stream content progressively"
    - "Error boundaries at same level as Suspense"

  anti_patterns:
    - "Single Suspense wrapping entire page (all-or-nothing)"
    - "Suspense inside loops (N fallbacks flickering)"
    - "Nested Suspense without meaningful intermediate state"

  placement_rules:
    - trigger: "Independent async content"
      action: "Separate Suspense boundary"
      example: "Product details vs reviews — load independently"

    - trigger: "Co-dependent async content"
      action: "Single Suspense boundary"
      example: "User profile + user's recent activity"

    - trigger: "Below-fold content"
      action: "Lazy load + Suspense"
      example: "Comments section, related products"
```

### Step 3: Design Fallback Hierarchy

```yaml
fallback_hierarchy:
  level_1_page_shell:
    shows: "Navigation, sidebar, footer (instant, static)"
    hides: "All async content"
    skeleton: "Full page skeleton matching layout"

  level_2_section:
    shows: "Section container with skeleton"
    hides: "Section content"
    skeleton: "Section-specific skeleton (cards, list items)"

  level_3_component:
    shows: "Component placeholder"
    hides: "Component content"
    skeleton: "Inline skeleton (text lines, avatar circle)"

  rules:
    - "Higher-level Suspense has coarser skeleton"
    - "Lower-level Suspense has finer, more specific skeleton"
    - "Minimum display time: 200ms (prevent flash)"
    - "Maximum display time: alert if >3s (fallback to error state)"
```

### Step 4: Integrate Error Boundaries

```yaml
error_boundary_integration:
  pattern: "ErrorBoundary wraps Suspense"

  structure: |
    <ErrorBoundary fallback={<SectionError onRetry={retry} />}>
      <Suspense fallback={<SectionSkeleton />}>
        <AsyncSection />
      </Suspense>
    </ErrorBoundary>

  retry_strategy:
    mechanism: "Key prop change to remount"
    max_retries: 3
    backoff: "None for user-initiated, exponential for auto"

  granularity:
    - "Page-level: catches unrecoverable errors"
    - "Section-level: isolates failures (rest of page works)"
    - "Component-level: only for critical inline content"
```

### Step 5: Configure Streaming SSR

```yaml
streaming_ssr:
  next_js:
    loading_tsx: "Page-level Suspense fallback (automatic)"
    inline_suspense: "Section-level streaming"
    generateStaticParams: "Pre-render known routes"

  performance:
    ttfb: "Instant (shell sent immediately)"
    fcp: "Shell content painted before data"
    lcp: "Streams when primary content resolves"
    inp: "Interactive before all data loaded"

  cache:
    full_route: "Static pages (revalidate: 3600)"
    partial: "Dynamic with cached sections"
    no_cache: "User-specific content"
```

### Step 6: Validate Suspense Architecture

- [ ] No all-or-nothing loading (progressive streaming)
- [ ] Independent data sources have separate Suspense boundaries
- [ ] Error boundaries catch and recover from failures
- [ ] Skeletons match final layout (no CLS)
- [ ] Streaming SSR configured (check with React DevTools)
- [ ] TTFB under 200ms (shell response)

## Quality Criteria

- Progressive loading: content appears as available
- Error isolation: section failure doesn't crash page
- Skeleton-to-content transition is smooth (no CLS)
- Streaming SSR verified in production build

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Progressive | Content streams independently |
| Error isolation | Section failure doesn't crash page |
| CLS | Zero layout shift during streaming |
| TTFB | Shell response under 200ms |

## Handoff

- Skeleton specs feed `@interaction-dsgn` for loading state design
- Error boundaries feed error-boundary-architecture task
- Performance metrics feed `@perf-eng` for CWV validation
