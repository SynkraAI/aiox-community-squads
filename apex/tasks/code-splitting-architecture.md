> **DEPRECATED** — Scope absorbed into `bundle-optimization.md`. See `data/task-consolidation-map.yaml`.

# Task: code-splitting-architecture

```yaml
id: code-splitting-architecture
version: "1.0.0"
title: "Code Splitting Architecture"
description: >
  Designs the code splitting strategy for optimal JavaScript loading.
  Identifies split points, implements route-based and component-based
  splitting, configures dynamic imports with Suspense boundaries,
  designs prefetching strategy, and produces a loading architecture
  that minimizes TTI and maximizes INP responsiveness.
elicit: false
owner: perf-eng
executor: perf-eng
outputs:
  - Bundle analysis report (current state)
  - Split point identification
  - Route-based splitting implementation
  - Component-based splitting patterns
  - Prefetch/preload strategy
  - Code splitting specification document
```

---

## When This Task Runs

This task runs when:
- Initial JavaScript bundle exceeds 200KB (gzipped)
- TTI (Time to Interactive) is too slow
- Pages load code they don't need (wasted bytes)
- Dynamic imports are not used or used incorrectly
- Suspense boundaries are missing for lazy-loaded components
- `*code-splitting` or `*split-arch` is invoked

This task does NOT run when:
- Bundle is already well-split and within budget
- The issue is image/font loading (use other perf tasks)
- React Native bundle (use `rn-performance-optimization`)

---

## Execution Steps

### Step 1: Analyze Current Bundle

Profile the JavaScript bundle to identify splitting opportunities.

**Analysis tools:**
```bash
# Webpack Bundle Analyzer
npx webpack-bundle-analyzer stats.json

# Next.js built-in
ANALYZE=true next build

# Vite
npx vite-bundle-visualizer
```

**Metrics to capture:**
| Metric | Target | Tool |
|--------|--------|------|
| Total JS (gzipped) | <200KB initial | Bundle analyzer |
| Largest chunk | <100KB | Bundle analyzer |
| Unused JS | <20% of loaded | Chrome Coverage |
| Number of chunks | Route-aligned | Build output |
| Tree-shaking effectiveness | No dead code in bundle | Source map explorer |

**Identify heavy modules:**
- Sort by size in bundle analyzer
- Flag modules >50KB (candidate for lazy loading)
- Identify modules used on only 1-2 routes (candidate for route splitting)
- Check for full library imports (`import lodash` vs `import debounce from 'lodash/debounce'`)

**Output:** Bundle analysis report with splitting opportunities.

### Step 2: Design Route-Based Splitting

Split code by route — each page loads only its code.

**Next.js (automatic):**
```typescript
// Next.js App Router splits by default per page.tsx
// Each route segment is a separate chunk
app/
├── page.tsx           // → chunk: main
├── about/page.tsx     // → chunk: about (lazy)
├── dashboard/page.tsx // → chunk: dashboard (lazy)
└── settings/page.tsx  // → chunk: settings (lazy)
```

**React + Vite (manual):**
```typescript
import { lazy, Suspense } from 'react';

// Route-level code splitting
const HomePage = lazy(() => import('./pages/Home'));
const DashboardPage = lazy(() => import('./pages/Dashboard'));
const SettingsPage = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Routes>
      <Route path="/" element={
        <Suspense fallback={<PageSkeleton />}>
          <HomePage />
        </Suspense>
      } />
      <Route path="/dashboard" element={
        <Suspense fallback={<PageSkeleton />}>
          <DashboardPage />
        </Suspense>
      } />
    </Routes>
  );
}
```

**Splitting rules:**
- Every route should be a separate chunk
- Shared layout components stay in main bundle
- Route-specific components are in route chunks
- Common dependencies (React, UI library) stay in vendor chunk

**Output:** Route-based splitting implementation.

### Step 3: Design Component-Based Splitting

Split heavy components that aren't needed immediately.

**Candidates for component splitting:**
| Component Type | When to Split | Example |
|---------------|--------------|---------|
| Modal/dialog content | Loaded on user action | `<SettingsModal />` |
| Below-the-fold content | Loaded on scroll | `<CommentsSection />` |
| Conditional features | Loaded on feature flag | `<AdminPanel />` |
| Heavy visualizations | Loaded when visible | `<Chart />`, `<Map />` |
| Rich text editors | Loaded on focus | `<RichTextEditor />` |

**Implementation pattern:**
```typescript
const Chart = lazy(() => import('./components/Chart'));
const RichTextEditor = lazy(() => import('./components/RichTextEditor'));

// Load chart when visible (intersection observer)
function DashboardMetrics() {
  const [isVisible, ref] = useInView({ triggerOnce: true });

  return (
    <div ref={ref}>
      {isVisible && (
        <Suspense fallback={<ChartSkeleton />}>
          <Chart data={data} />
        </Suspense>
      )}
    </div>
  );
}

// Load editor on user action
function PostForm() {
  const [showEditor, setShowEditor] = useState(false);

  return (
    <>
      {showEditor ? (
        <Suspense fallback={<EditorSkeleton />}>
          <RichTextEditor />
        </Suspense>
      ) : (
        <button onClick={() => setShowEditor(true)}>
          Write a post
        </button>
      )}
    </>
  );
}
```

**Output:** Component splitting patterns with Suspense boundaries.

### Step 4: Design Prefetch Strategy

Preload code before the user needs it for instant navigation.

**Prefetch strategies:**
| Strategy | When | Implementation |
|----------|------|----------------|
| Link hover prefetch | User hovers a navigation link | `<Link prefetch>` or `onMouseEnter` |
| Viewport prefetch | Link scrolls into viewport | Intersection Observer |
| Idle prefetch | Browser is idle | `requestIdleCallback` |
| Route prediction | Based on likely next navigation | Analytics-driven |

**Next.js prefetching (built-in):**
```tsx
// Next.js Link prefetches on viewport intersection by default
import Link from 'next/link';
<Link href="/dashboard">Dashboard</Link>
// → Prefetches /dashboard chunk when link is visible

// Disable for heavy routes
<Link href="/admin" prefetch={false}>Admin</Link>
```

**Manual prefetch (React + Vite):**
```typescript
// Prefetch on hover
const prefetchDashboard = () => {
  import('./pages/Dashboard'); // Browser caches the chunk
};

<Link to="/dashboard" onMouseEnter={prefetchDashboard}>
  Dashboard
</Link>

// Prefetch on idle
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => {
    import('./pages/Dashboard');
    import('./pages/Settings');
  });
}
```

**Output:** Prefetch strategy per route and component.

### Step 5: Configure Chunk Optimization

Optimize how chunks are created and cached.

**Webpack/Next.js chunk optimization:**
```javascript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: [
      'lucide-react',      // Tree-shake icon library
      '@radix-ui/react-*', // Tree-shake UI primitives
      'date-fns',          // Tree-shake date utilities
    ],
  },
};
```

**Import optimization patterns:**
```typescript
// BAD: imports entire library
import { debounce, throttle, cloneDeep } from 'lodash';

// GOOD: imports only used function
import debounce from 'lodash/debounce';

// BAD: barrel file imports everything
import { Button, Card, Modal, Table } from '@/components';

// GOOD: direct imports (tree-shakeable)
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
```

**Output:** Chunk optimization configuration.

### Step 6: Document Code Splitting Architecture

Compile the complete specification.

**Documentation includes:**
- Bundle analysis report (from Step 1)
- Route splitting implementation (from Step 2)
- Component splitting patterns (from Step 3)
- Prefetch strategy (from Step 4)
- Chunk optimization config (from Step 5)
- Suspense boundary placement guide
- Performance metrics: before/after

**Output:** Complete code splitting specification document.

---

## Quality Criteria

- Initial JS bundle must be under 200KB gzipped
- Every route must be a separate chunk
- Heavy components (>50KB) must be lazy-loaded
- Suspense boundaries must show meaningful loading states
- Prefetch must not increase initial page load time

---

*Squad Apex — Code Splitting Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-code-splitting-architecture
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Initial JS bundle under 200KB gzipped"
    - "Every route is a separate chunk"
    - "Heavy components lazy-loaded with Suspense"
    - "Prefetch does not increase initial load time"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Code splitting architecture with route/component splitting, prefetch strategy, and chunk config |
| Next action | Implement Suspense boundaries via `@react-eng` or validate via `performance-audit` |
