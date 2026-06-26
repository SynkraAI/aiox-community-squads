---
id: custom-hook-library
version: "1.0.0"
title: "Custom Hook Library Design"
description: "Design and catalog reusable custom hooks: useDebounce, useMediaQuery, useIntersection, useLocalStorage, and composition patterns for hook architecture"
elicit: true
owner: react-eng
executor: react-eng
outputs:
  - hook-library-spec.md
  - hook-catalog.yaml
---

# Custom Hook Library Design

## When This Task Runs

- Project needs shared hooks across components
- Duplicate hook logic detected across components
- New feature needs a reusable behavior abstraction
- `*hook` command invoked

## Execution Steps

### Step 1: Inventory Existing Hooks
```
SCAN project for custom hooks:
- Files matching use*.ts / use*.tsx
- Hook definitions inside components (inline hooks)
- Duplicate hook logic across components
- Third-party hooks used (from libraries)

OUTPUT: Hook inventory + duplication report
```

### Step 2: Identify Hook Candidates

**elicit: true** — Confirm which hooks to create/standardize:

| Hook | Purpose | Priority |
|------|---------|----------|
| `useDebounce` | Debounce value changes (search, resize) | - |
| `useThrottle` | Throttle event handlers (scroll, mousemove) | - |
| `useMediaQuery` | Responsive breakpoint detection | - |
| `useIntersection` | Intersection Observer (lazy load, infinite scroll) | - |
| `useLocalStorage` | Persistent state in localStorage | - |
| `useClickOutside` | Detect clicks outside element (dropdowns, modals) | - |
| `usePrevious` | Track previous value of state/prop | - |
| `useToggle` | Boolean toggle with stable callbacks | - |
| `useAsync` | Async operation state (loading, error, data) | - |
| `useCopyToClipboard` | Copy text to clipboard with feedback | - |
| `useDocumentTitle` | Dynamic page title | - |
| `useEventListener` | Typed event listener with cleanup | - |

### Step 3: Design Hook API

For each selected hook, follow Kent's principles:

```yaml
hook_design:
  name: "use{HookName}"

  api:
    input: "{config object or primitive}"
    output: "{state + actions tuple or object}"

  design_rules:
    - "Single responsibility — one hook, one concern"
    - "Return what consumers need, hide what they don't"
    - "Stable references for callbacks (useMemo/useCallback)"
    - "Generic — works with any component"
    - "SSR-safe — check typeof window before browser APIs"

  example:
    useDebounce:
      input: "value: T, delay: number"
      output: "debouncedValue: T"
      implementation: |
        function useDebounce<T>(value: T, delay: number): T {
          const [debouncedValue, setDebouncedValue] = useState(value)
          useEffect(() => {
            const timer = setTimeout(() => setDebouncedValue(value), delay)
            return () => clearTimeout(timer)
          }, [value, delay])
          return debouncedValue
        }

    useMediaQuery:
      input: "query: string"
      output: "matches: boolean"
      ssr_safe: true
      implementation: |
        function useMediaQuery(query: string): boolean {
          const [matches, setMatches] = useState(false)
          useEffect(() => {
            const mql = window.matchMedia(query)
            setMatches(mql.matches)
            const handler = (e: MediaQueryListEvent) => setMatches(e.matches)
            mql.addEventListener('change', handler)
            return () => mql.removeEventListener('change', handler)
          }, [query])
          return matches
        }
```

### Step 4: Define Testing Strategy

```yaml
testing_approach:
  rule: "Test hooks through components that use them (Kent's principle)"

  exception: "Pure utility hooks (useDebounce, useThrottle) can use renderHook"

  pattern: |
    // Test through a consumer component
    function TestComponent() {
      const debouncedValue = useDebounce(searchTerm, 300)
      return <div data-testid="result">{debouncedValue}</div>
    }

    test('debounces value changes', async () => {
      // Render, update, advance timers, assert on DOM
    })
```

### Step 5: Define Hook Architecture

```yaml
hook_architecture:
  file_structure:
    - "hooks/useDebounce.ts" (hook + types)
    - "hooks/useDebounce.test.ts" (test)
    - "hooks/index.ts" (barrel export — only if <10 hooks)

  composition_pattern:
    example: |
      // Composing hooks
      function useSearchResults(query: string) {
        const debouncedQuery = useDebounce(query, 300)
        const { data, isLoading } = useQuery(
          ['search', debouncedQuery],
          () => fetchSearch(debouncedQuery),
          { enabled: debouncedQuery.length > 2 }
        )
        return { results: data, isLoading }
      }

  naming_conventions:
    - "use{Noun} — for state (useToggle, useCounter)"
    - "use{Noun} — for observation (useMediaQuery, useIntersection)"
    - "use{Verb}{Noun} — for actions (useCopyToClipboard)"
```

### Step 6: Validate Hook Library

- [ ] Each hook has single responsibility
- [ ] No duplicate logic across hooks
- [ ] All hooks are SSR-safe (or documented as client-only)
- [ ] Stable callback references (no re-creation on every render)
- [ ] Tests cover core behavior
- [ ] TypeScript generics where applicable

## Quality Criteria

- Single responsibility per hook
- SSR-safe (no window/document access without guard)
- Stable references for returned callbacks
- Test coverage for each hook

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Single responsibility | One concern per hook |
| SSR safe | No unguarded browser API access |
| Stable refs | Callbacks don't change on re-render |
| Tests | Each hook has behavior tests |

## Handoff

- Hook library feeds all agents using React components
- Composition patterns feed `@frontend-arch` for architecture review
- SSR safety feeds server-component-patterns task
