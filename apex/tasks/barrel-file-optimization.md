> **DEPRECATED** — Scope absorbed into `bundle-optimization.md`. See `data/task-consolidation-map.yaml`.

---
id: barrel-file-optimization
version: "1.0.0"
title: "Barrel File Audit & Optimization"
description: "Audit barrel files (index.ts re-exports) for tree-shaking impact, circular dependency risks, and bundle size bloat with actionable migration plan"
elicit: false
owner: frontend-arch
executor: frontend-arch
outputs:
  - barrel-file-audit-report.md
  - import-optimization-plan.yaml
---

# Barrel File Audit & Optimization

## When This Task Runs

- Bundle size is larger than expected
- Tree-shaking is not working effectively
- Circular dependency errors appear
- `*discover-dependencies` flags barrel file issues
- Build time is unexpectedly slow

## Execution Steps

### Step 1: Identify All Barrel Files
```
SCAN project for barrel/index files:
- **/index.ts, **/index.tsx
- Files with ONLY export statements (no logic)
- Re-export chains (index.ts → index.ts → index.ts)

OUTPUT:
  barrel_files: [list with re-export count per file]
  re_export_chains: [chains > 2 levels deep]
  total_re_exports: {count}
```

### Step 2: Analyze Tree-Shaking Impact

For each barrel file:

```yaml
analysis:
  file: "{path}/index.ts"
  total_exports: 25
  imports_of_this_barrel:
    - consumer: "ComponentA.tsx"
      uses: 2  # of 25 exports
      tree_shaking_waste: 23  # Unused exports pulled in
    - consumer: "ComponentB.tsx"
      uses: 1  # of 25 exports
      tree_shaking_waste: 24

  impact:
    bundler: "{webpack | vite | esbuild}"
    tree_shakeable: "{yes | partial | no}"
    reason: "{sideEffects not configured | CJS module | dynamic import}"
```

### Step 3: Detect Circular Dependencies

```
TRACE import chains for cycles:
- A → B → C → A (direct cycle)
- A/index → B/index → C/index → A/index (barrel-mediated cycle)

For each cycle:
  - Identify which re-export creates the cycle
  - Determine if it's a barrel-only cycle (fixable by direct import)
  - Classify severity: build-error | runtime-error | warning-only
```

### Step 4: Generate Optimization Plan

```yaml
optimization_plan:
  # Strategy per barrel file
  actions:
    - barrel: "components/index.ts"
      action: "KEEP"  # High-use barrel, most exports consumed
      reason: "80% of exports used by 3+ consumers"

    - barrel: "utils/index.ts"
      action: "SPLIT"  # Low-use barrel, few exports consumed per import
      reason: "25 exports but consumers use 1-2 each"
      migration: "Direct imports: import { formatDate } from '@/utils/date'"

    - barrel: "hooks/index.ts"
      action: "REMOVE"  # Creates circular dependency
      reason: "Barrel creates cycle with components/"
      migration: "Direct imports from individual hook files"

  sideEffects_config:
    package_json:
      sideEffects: false  # Or list specific files with side effects
    webpack:
      optimization:
        usedExports: true
        sideEffects: true
```

### Step 5: Validate Optimization

- [ ] No circular dependencies in import graph
- [ ] Bundle size reduced (measure before/after)
- [ ] All imports resolve correctly after migration
- [ ] `sideEffects: false` configured in package.json
- [ ] Build time not degraded
- [ ] TypeScript paths/aliases updated if barrel removed

## Quality Criteria

- Zero circular dependency chains
- Bundle size reduction measured and documented
- No barrel files with <50% export utilization
- `sideEffects` properly configured for tree-shaking

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Cycles | Zero circular dependencies |
| Bundle | Measurable size reduction |
| Imports | All imports resolve post-migration |
| Tree-shaking | `sideEffects: false` configured |

## Handoff

- Bundle analysis feeds `@perf-eng` for performance budget check
- Import structure feeds `@react-eng` for component organization
- Circular dependency fixes feed `@frontend-arch` monorepo boundaries
