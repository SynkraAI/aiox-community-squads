> **DEPRECATED** — Scope absorbed into `rsc-architecture.md`. See `data/task-consolidation-map.yaml`.

---
id: server-component-patterns
version: "1.0.0"
title: "React Server Component Patterns"
description: "Design RSC architecture: server/client boundaries, async data fetching, streaming, selective hydration, server actions, and composition patterns"
elicit: true
owner: react-eng
executor: react-eng
outputs:
  - rsc-architecture-spec.md
  - boundary-map.yaml
---

# React Server Component Patterns

## When This Task Runs

- Building new pages/features in Next.js App Router
- Migrating from Pages Router to App Router
- Deciding server vs client component boundaries
- Implementing server actions for mutations
- `*server-component` command invoked

## Execution Steps

### Step 1: Audit Current RSC Usage
```
SCAN project for RSC patterns:
- Files with 'use client' directive (count + reasons)
- Async components (server data fetching)
- Server actions ('use server')
- Client-side data fetching (useEffect, React Query, SWR)
- Component tree: server→client boundary locations

OUTPUT: RSC adoption map + optimization opportunities
```

### Step 2: Apply RSC Decision Tree

For each component/page:

```yaml
decision_tree:
  default: "Server Component (no directive)"

  add_use_client_when:
    - "Uses useState, useReducer (interactive state)"
    - "Uses useEffect, useLayoutEffect (side effects)"
    - "Attaches event handlers (onClick, onChange, onSubmit)"
    - "Uses browser APIs (window, document, localStorage)"
    - "Uses React context for runtime values"
    - "Third-party library requires client (no RSC support)"

  keep_server_when:
    - "Fetches data (async/await directly)"
    - "Reads env vars, filesystem, DB"
    - "Renders static or server-computed content"
    - "Heavy dependencies (markdown, syntax highlight)"
    - "No interactivity needed"
```

### Step 3: Design Component Boundaries

**elicit: true** — Review proposed boundaries:

```
Page (Server) ← fetches data, renders layout
├── Header (Server) ← static navigation
│   └── SearchBar (Client) ← needs useState, onChange
├── ProductList (Server) ← fetches products
│   └── AddToCartButton (Client) ← onClick, optimistic UI
├── Sidebar (Server) ← static content
│   └── FilterPanel (Client) ← interactive filters
└── Footer (Server) ← static
```

**Rule:** Push `'use client'` boundary as deep as possible in the tree.

### Step 4: Implement Data Patterns

```yaml
data_patterns:
  server_fetch:
    pattern: "Async Server Component"
    code: |
      async function ProductPage({ params }) {
        const product = await db.products.find(params.id)
        return <ProductDetail product={product} />
      }
    benefits: "No loading state, no waterfall, zero client JS"

  streaming:
    pattern: "Suspense + streaming"
    code: |
      export default function Page() {
        return (
          <div>
            <Header />  {/* Instant */}
            <Suspense fallback={<ProductSkeleton />}>
              <ProductList />  {/* Streams when ready */}
            </Suspense>
            <Suspense fallback={<ReviewsSkeleton />}>
              <Reviews />  {/* Streams independently */}
            </Suspense>
          </div>
        )
      }
    benefits: "Progressive rendering, no all-or-nothing"

  server_action:
    pattern: "Server Action for mutations"
    code: |
      async function addToCart(formData: FormData) {
        'use server'
        const productId = formData.get('productId')
        await db.cart.add({ productId, userId: auth().userId })
        revalidatePath('/cart')
      }
    benefits: "No API route, progressive enhancement, type-safe"

  revalidation:
    strategies:
      - "revalidatePath('/path') — invalidate specific page"
      - "revalidateTag('tag') — invalidate by cache tag"
      - "{ next: { revalidate: 60 } } — time-based"
      - "{ cache: 'no-store' } — always fresh"
```

### Step 5: Handle RSC Edge Cases

```yaml
edge_cases:
  third_party_client_only:
    problem: "Library requires client but used in server tree"
    solution: "Wrap in client component, pass server data as props"

  context_in_server:
    problem: "React context doesn't work in Server Components"
    solution: "Pass data as props from server, use context only in client subtree"

  serialization:
    problem: "Props from server→client must be serializable"
    constraint: "No functions, Dates, Maps, Sets, classes as props"
    solution: "Serialize to plain objects, parse in client component"

  composition:
    pattern: "Server Component wrapping Client Component children"
    code: |
      // Server Component
      function Layout({ children }) {
        const data = await fetchData()
        return (
          <ClientSidebar>
            {children}  {/* Server content passed as children */}
          </ClientSidebar>
        )
      }
```

### Step 6: Validate RSC Architecture

- [ ] `'use client'` only where actually needed
- [ ] No data fetching in client components (useEffect for server data)
- [ ] Suspense boundaries wrap async server components
- [ ] Server actions handle mutations (no API routes for simple CRUD)
- [ ] Props from server to client are serializable
- [ ] Bundle analyzer confirms reduced client JS

## Quality Criteria

- Minimal `'use client'` directives (pushed deep in tree)
- Zero useEffect-based data fetching for server-available data
- Streaming SSR with meaningful Suspense boundaries
- Server actions for all mutations

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Boundaries | `'use client'` justified for each usage |
| Data | No client-side fetch for server data |
| Streaming | Suspense wraps slow async components |
| Bundle | Client JS reduced vs baseline |

## Handoff

- RSC architecture feeds `@perf-eng` for bundle analysis
- Suspense boundaries feed `@interaction-dsgn` for loading state design
- Server actions feed `@a11y-eng` for progressive enhancement validation
