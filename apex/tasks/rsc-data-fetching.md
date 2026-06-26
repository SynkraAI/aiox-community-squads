> **DEPRECATED** — Scope absorbed into `rsc-architecture.md`. See `data/task-consolidation-map.yaml`.

---
id: rsc-data-fetching
version: "1.0.0"
title: "RSC Data Fetching Patterns"
description: "Design data fetching architecture for React Server Components: caching strategies, revalidation, optimistic updates, parallel fetching, and waterfall prevention"
elicit: false
owner: react-eng
executor: react-eng
outputs:
  - data-fetching-spec.md
  - cache-strategy.yaml
---

# RSC Data Fetching Patterns

## When This Task Runs

- Designing data fetching for new RSC-based pages
- Migrating from client-side fetching (useEffect/SWR/React Query)
- Optimizing data loading waterfall
- Configuring cache and revalidation strategy
- `*data-fetch` command invoked

## Execution Steps

### Step 1: Inventory Data Requirements
```
For each page/feature:
- List all data sources (DB, external API, CMS, auth)
- Classify: static vs dynamic vs user-specific
- Map dependencies: does fetch B need result of fetch A?
- Identify parallel opportunities

OUTPUT: Data dependency graph
```

### Step 2: Select Fetching Strategy Per Source

```yaml
strategies:
  static_data:
    pattern: "Build-time fetch with ISR"
    cache: "{ next: { revalidate: 3600 } }"
    example: "Blog posts, product catalog, CMS content"
    benefit: "Instant response, CDN-cached"

  dynamic_shared:
    pattern: "Server-side fetch with time-based revalidation"
    cache: "{ next: { revalidate: 60 } }"
    example: "Dashboard metrics, live inventory"
    benefit: "Fresh within revalidation window"

  user_specific:
    pattern: "Server-side fetch with no cache"
    cache: "{ cache: 'no-store' }"
    example: "User profile, cart, notifications"
    benefit: "Always fresh, personalized"

  mutation:
    pattern: "Server Action"
    revalidation: "revalidatePath or revalidateTag"
    example: "Form submission, CRUD operations"
    benefit: "No API route, progressive enhancement"
```

### Step 3: Prevent Waterfalls

```yaml
waterfall_prevention:
  problem: |
    Sequential fetches: fetch A → await → fetch B → await → fetch C
    Total time = A + B + C (waterfall)

  solutions:
    parallel_fetch:
      code: |
        async function Page() {
          const [products, categories, featured] = await Promise.all([
            fetchProducts(),
            fetchCategories(),
            fetchFeatured(),
          ])
          return <Layout products={products} categories={categories} featured={featured} />
        }
      benefit: "Total time = max(A, B, C)"

    streaming:
      code: |
        async function Page() {
          const categories = await fetchCategories()  // Fast, needed for layout
          return (
            <Layout categories={categories}>
              <Suspense fallback={<ProductsSkeleton />}>
                <ProductList />  {/* Fetches own data, streams when ready */}
              </Suspense>
            </Layout>
          )
        }
      benefit: "Shell instant, content streams"

    preloading:
      code: |
        import { preload } from 'react'
        // Preload in layout, consume in page
        function Layout({ children }) {
          preload(fetchProducts)  // Start fetch early
          return <div>{children}</div>
        }
      benefit: "Data starts loading before component renders"
```

### Step 4: Design Cache Strategy

```yaml
cache_strategy:
  per_route:
    - route: "/"
      cache: "revalidate: 60"
      reason: "Homepage content changes hourly"

    - route: "/products/[id]"
      cache: "revalidate: 3600"
      reason: "Product details change infrequently"
      tags: ["products"]

    - route: "/dashboard"
      cache: "no-store"
      reason: "User-specific, always fresh"

  tag_based_revalidation:
    example: |
      // In server action after product update:
      revalidateTag('products')  // Invalidates all routes tagged 'products'

  deduplication:
    note: "React 19 auto-deduplicates same fetch() calls in render tree"
    benefit: "Multiple components can call same fetch, only 1 network request"
```

### Step 5: Handle Mutations

```yaml
mutation_patterns:
  server_action:
    code: |
      'use server'
      async function updateProduct(formData: FormData) {
        const data = Object.fromEntries(formData)
        await db.products.update(data.id, data)
        revalidatePath('/products/' + data.id)
      }

  optimistic_update:
    code: |
      'use client'
      function LikeButton({ productId, initialLikes }) {
        const [likes, setLikes] = useOptimistic(initialLikes)
        async function handleLike() {
          setLikes(prev => prev + 1)  // Instant UI update
          await likeProduct(productId)  // Server action
        }
        return <button onClick={handleLike}>❤️ {likes}</button>
      }

  form_with_status:
    code: |
      'use client'
      function SubmitButton() {
        const { pending } = useFormStatus()
        return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
      }
```

### Step 6: Validate Data Architecture

- [ ] No client-side fetch for server-available data
- [ ] No waterfall patterns (parallel or streaming)
- [ ] Cache strategy defined per route
- [ ] Revalidation triggers defined for each mutation
- [ ] Optimistic updates for user-facing mutations
- [ ] Error handling for failed fetches

## Quality Criteria

- Zero unnecessary client-side data fetching
- No sequential waterfall for independent data
- Cache strategy documented per route/resource
- Mutations use server actions with revalidation

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| No waterfall | Independent fetches are parallel or streamed |
| Cache | Every route has defined cache strategy |
| Mutations | Server actions with revalidation |
| Errors | Every fetch has error handling |

## Handoff

- Cache strategy feeds `@perf-eng` for CDN and CWV optimization
- Loading patterns feed `@interaction-dsgn` for skeleton design
- Form mutations feed `@a11y-eng` for progressive enhancement validation
