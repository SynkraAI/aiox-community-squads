> **DEPRECATED** — Scope absorbed into `bundle-optimization.md`. See `data/task-consolidation-map.yaml`.

# Task: hydration-optimization

```yaml
id: hydration-optimization
version: "1.0.0"
title: "SSR Hydration Optimization"
description: >
  Optimizes React SSR/SSG hydration to minimize TTI and eliminate
  hydration mismatches. Implements selective hydration, progressive
  hydration, React Server Components boundaries, and islands
  architecture patterns. Reduces client-side JavaScript by maximizing
  server-rendered content that doesn't need hydration.
elicit: false
owner: perf-eng
executor: perf-eng
outputs:
  - Hydration audit (current mismatch count, TTI impact)
  - Server vs Client component boundary map
  - Selective hydration strategy
  - Progressive hydration patterns
  - Hydration error resolution guide
  - Hydration optimization specification document
```

---

## When This Task Runs

This task runs when:
- TTI is significantly higher than FCP (hydration is the bottleneck)
- Hydration mismatch warnings appear in console
- Large pages take too long to become interactive
- Client bundle includes code that could be server-only
- React Server Components (RSC) adoption needs planning
- `*hydration-opt` or `*ssr-hydration` is invoked

This task does NOT run when:
- The app is client-side only (SPA — no SSR/SSG)
- React Native app (no SSR)
- The issue is pre-rendering, not hydration (use SSG/ISR config)

---

## Execution Steps

### Step 1: Audit Current Hydration

Profile hydration performance and identify issues.

**Metrics to capture:**
| Metric | How | Target |
|--------|-----|--------|
| FCP → TTI gap | Chrome DevTools Performance | <500ms |
| Hydration time | React Profiler | <200ms |
| Mismatch count | Browser console warnings | 0 |
| Client JS that could be server | Source map analysis | Minimize |

**Common hydration mismatches:**
| Cause | Example | Fix |
|-------|---------|-----|
| Date/time rendering | `new Date().toLocaleString()` | Use `useEffect` for client-only values |
| Window/document access | `window.innerWidth` | Guard with `typeof window !== 'undefined'` |
| Random values | `Math.random()` in render | Use `useId()` or seed |
| Browser extensions | Extension injects DOM nodes | Use `suppressHydrationWarning` (rare) |
| CSS-in-JS class mismatch | Different class on server vs client | Ensure deterministic class generation |

**Output:** Hydration audit with mismatch inventory and TTI impact.

### Step 2: Define Server/Client Component Boundaries

Map which components should be Server Components vs Client Components.

**Decision matrix (Next.js App Router):**
| Component does... | Server Component | Client Component |
|-------------------|-----------------|------------------|
| Fetch data | Yes | No (use server action) |
| Access backend resources | Yes | No |
| Use hooks (useState, useEffect) | No | Yes |
| Use browser APIs | No | Yes |
| Handle user interactions | No | Yes |
| Render static content | Yes | Unnecessary |
| Use context | No | Yes |

**Boundary placement strategy:**
```
Server Component (no JS sent to client)
├── Static header content
├── Data-fetched article content
├── Static sidebar
└── Client Component boundary ('use client')
    ├── Interactive search bar
    ├── Like button with state
    └── Comments with real-time updates
```

**Key principle:** Push `'use client'` boundaries as far DOWN the tree as possible. Only the interactive leaf components should be Client Components.

```typescript
// GOOD: Small client boundary
// page.tsx (Server Component)
export default async function ArticlePage({ params }) {
  const article = await fetchArticle(params.id); // Server-side fetch

  return (
    <article>
      <h1>{article.title}</h1>       {/* Server: no JS */}
      <p>{article.content}</p>        {/* Server: no JS */}
      <LikeButton id={article.id} />  {/* Client: interactive */}
      <CommentSection id={article.id} /> {/* Client: interactive */}
    </article>
  );
}

// LikeButton.tsx
'use client';
export function LikeButton({ id }) {
  const [liked, setLiked] = useState(false);
  // Only this component's JS is sent to client
}
```

**Output:** Server/Client component boundary map.

### Step 3: Implement Selective Hydration

Prioritize hydration of interactive elements.

**React 18 selective hydration (automatic with Suspense):**
```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <>
      {/* Hydrates immediately — above fold, interactive */}
      <Header />

      {/* Hydrates when visible or interacted with */}
      <Suspense fallback={<ArticleSkeleton />}>
        <Article />
      </Suspense>

      {/* Hydrates last — below fold */}
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments />
      </Suspense>

      {/* Hydrates last — footer is rarely interactive */}
      <Suspense fallback={<FooterSkeleton />}>
        <Footer />
      </Suspense>
    </>
  );
}
```

**Selective hydration behavior:**
- React hydrates Suspense boundaries independently
- If user clicks a not-yet-hydrated component, React prioritizes it
- Components further down the page hydrate later
- Each Suspense boundary = independent hydration unit

**Output:** Selective hydration strategy with Suspense boundary placement.

### Step 4: Design Progressive Hydration Patterns

Delay hydration of non-critical components until needed.

**Idle hydration (hydrate when browser is idle):**
```typescript
'use client';
import { useEffect, useState } from 'react';

function useIdleHydration() {
  const [shouldHydrate, setShouldHydrate] = useState(false);

  useEffect(() => {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(() => setShouldHydrate(true));
    } else {
      setTimeout(() => setShouldHydrate(true), 200);
    }
  }, []);

  return shouldHydrate;
}
```

**Visible hydration (hydrate when scrolled into view):**
```typescript
'use client';
function useVisibleHydration(ref: RefObject<HTMLElement>) {
  const [shouldHydrate, setShouldHydrate] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setShouldHydrate(true);
          observer.disconnect();
        }
      },
      { rootMargin: '200px' } // Hydrate 200px before visible
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return shouldHydrate;
}
```

**Interaction hydration (hydrate on first interaction):**
```typescript
// Show server-rendered HTML, hydrate on first click/focus
function InteractionHydrated({ children, fallback }) {
  const [hydrated, setHydrated] = useState(false);

  if (!hydrated) {
    return (
      <div
        onClick={() => setHydrated(true)}
        onFocus={() => setHydrated(true)}
        onMouseEnter={() => setHydrated(true)}
      >
        {fallback}
      </div>
    );
  }

  return children;
}
```

**Output:** Progressive hydration patterns by trigger type.

### Step 5: Resolve Hydration Errors

Fix all hydration mismatches systematically.

**Error resolution patterns:**
| Error | Cause | Fix |
|-------|-------|-----|
| Text content mismatch | Dynamic value differs server/client | `useEffect` for client-only values |
| Extra attributes | Browser normalizes HTML differently | Check self-closing tags, boolean attrs |
| Missing/extra nodes | Conditional rendering differs | Ensure same conditions on both sides |
| `useId()` mismatch | Component order differs | Stable component keys |

**Client-only rendering pattern:**
```typescript
function ClientOnly({ children, fallback = null }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  if (!mounted) return fallback;
  return children;
}

// Usage: values that differ between server and client
<ClientOnly fallback={<span>--:--</span>}>
  <span>{new Date().toLocaleTimeString()}</span>
</ClientOnly>
```

**Output:** Hydration error resolution guide.

### Step 6: Document Hydration Architecture

Compile the complete specification.

**Documentation includes:**
- Hydration audit results (from Step 1)
- Component boundary map (from Step 2)
- Selective hydration strategy (from Step 3)
- Progressive hydration patterns (from Step 4)
- Error resolution guide (from Step 5)
- Performance metrics: before/after (FCP, TTI, TBT)

**Output:** Complete hydration optimization specification.

---

## Quality Criteria

- FCP → TTI gap must be under 500ms
- Zero hydration mismatch warnings
- Client JS must not include server-only code
- Suspense boundaries must be placed for selective hydration
- Below-fold content must use progressive hydration

---

*Squad Apex — SSR Hydration Optimization Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-hydration-optimization
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "FCP → TTI gap under 500ms"
    - "Zero hydration mismatch warnings"
    - "Server-only code excluded from client bundle"
    - "Suspense boundaries placed for selective hydration"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Hydration optimization with component boundaries, selective/progressive patterns, and error fixes |
| Next action | Implement RSC boundaries via `@react-eng` or validate via `performance-audit` |
