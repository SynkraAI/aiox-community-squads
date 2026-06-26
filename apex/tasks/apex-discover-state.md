# Task: apex-discover-state

```yaml
id: apex-discover-state
version: "1.0.0"
title: "State Management Discovery"
description: >
  Scans state management patterns across the project. Detects context
  sprawl, prop drilling chains, unused stores, re-render risks from
  context, and state colocation issues. Transforms "how is state
  managed?" into "I already mapped every state source — here's what
  needs attention."
elicit: false
owner: apex-lead
executor: react-eng
dependencies:
  - tasks/apex-scan.md
outputs:
  - State library inventory and classification
  - Consumer map (which components subscribe to which state)
  - Context sprawl analysis (providers at root)
  - Prop drilling chains (3+ levels)
  - Re-render risk assessment (context without slicing)
  - Unused state detection
  - State health score (0-100)
```

---

## Command

### `*discover-state`

Scans the project and maps all state management patterns. Runs as part of `*apex-audit` or independently.

---

## Discovery Phases

### Phase 1: Detect State Libraries

```yaml
library_detection:
  scan:
    - "package.json"
    - "src/**/*.tsx"
    - "src/**/*.ts"
    - "app/**/*.tsx"
    - "packages/**/src/**/*.tsx"

  classify:
    global:
      detect: "zustand, redux, @reduxjs/toolkit, recoil"
      note: "Single global store, selectors for slicing"
    atomic:
      detect: "jotai, nanostores"
      note: "Atom-based, granular subscriptions"
    state_machine:
      detect: "xstate, @xstate/react, robot3"
      note: "Finite state machines, explicit transitions"
    built_in_context:
      detect: "React.createContext, useContext"
      note: "Built-in, no external dep, re-render risk"
    built_in_local:
      detect: "useState, useReducer"
      note: "Component-local state, no sharing"
    server_state:
      detect: "@tanstack/react-query, swr, trpc"
      note: "Server cache, not client state"

  extract:
    - library: "name and version from package.json"
    - usage_count: "number of imports across codebase"
    - primary_lib: "most-used state library"
    - mixing: "true if 2+ global state libs detected"
```

### Phase 2: Map State Usage

```yaml
state_mapping:
  for_each_state_source:
    context_providers:
      scan: "createContext declarations"
      extract:
        - name: "context name"
        - provider_location: "file where <Provider> is rendered"
        - provider_level: "root | route | component"
        - value_shape: "what data the context holds"
        - consumers: "list of components using useContext"
        - consumer_count: "number of unique consumers"
        - has_useMemo: "true if value is memoized"

    zustand_stores:
      scan: "create() or createStore() calls"
      extract:
        - name: "store name"
        - slice_count: "number of selectors defined"
        - consumers: "components using useStore"
        - actions: "state mutations defined"
        - middleware: "persist, devtools, immer, etc"

    redux_slices:
      scan: "createSlice() or reducer definitions"
      extract:
        - name: "slice name"
        - selectors: "useSelector calls"
        - dispatchers: "useDispatch calls"
        - consumers: "components using this slice"

    local_state:
      scan: "useState and useReducer calls"
      extract:
        - component: "component name"
        - state_count: "number of useState calls"
        - reducer_count: "number of useReducer calls"
        - lifted_candidates: "state used in children via props"

  prop_drilling:
    detect: "same prop name passed through 3+ component levels"
    extract:
      - prop_name: "the drilled prop"
      - chain: "ComponentA → ComponentB → ComponentC → ComponentD"
      - depth: "number of levels"
      - suggestion: "context, zustand, or composition"
```

### Phase 3: Detect Issues

```yaml
issue_detection:
  - id: context_sprawl
    condition: "More than 5 context providers at root level"
    severity: HIGH
    impact: "Every provider re-renders all consumers on any change"
    suggestion: "Consolidate related contexts or migrate to zustand"

  - id: prop_drilling
    condition: "Same prop passed through 3+ component levels"
    severity: MEDIUM
    impact: "Tight coupling, hard to refactor"
    suggestion: "Extract to context or state library"

  - id: context_no_slice
    condition: "Component subscribes to large context but uses only 1-2 fields"
    severity: HIGH
    impact: "Full re-render on any context change (causes jank)"
    feeds_gate: "QG-AX-007 indirectly (performance)"
    suggestion: "Split context or use zustand with selectors"

  - id: unused_state
    condition: "State variable set via setState but never read"
    severity: LOW
    impact: "Dead code, unnecessary re-renders"
    suggestion: "Remove unused state"

  - id: missing_memoization
    condition: "Context value is new object every render (no useMemo)"
    severity: HIGH
    impact: "All consumers re-render on every parent render"
    suggestion: "Wrap value in useMemo"

  - id: state_in_wrong_layer
    condition: "Server data managed with client state lib (should use react-query/SWR)"
    severity: MEDIUM
    impact: "Missing cache, stale data, manual refetch logic"
    suggestion: "Migrate to @tanstack/react-query or SWR"

  - id: excessive_useEffect
    condition: "More than 3 useEffect in one component for state sync"
    severity: MEDIUM
    impact: "Complex state sync, race conditions, hard to debug"
    suggestion: "Consider useReducer or xstate for complex flows"
```

### Phase 4: Health Score

```yaml
health_score:
  formula: >
    100 - (context_sprawl * 10) - (prop_drilling_count * 3)
    - (context_no_slice_count * 5) - (missing_memoization_count * 8)
    - (unused_state_count * 1) - (state_wrong_layer_count * 5)
    - (excessive_useEffect_count * 3)
  max: 100
  min: 0
  thresholds:
    clean: ">= 90 — state architecture is solid"
    good: "70-89 — minor issues, mostly healthy"
    tangled: "50-69 — significant state management problems"
    spaghetti: "< 50 — state architecture needs overhaul"
```

---

## Output Format

```
STATE MANAGEMENT DISCOVERY
===========================
Project: {name}
Primary State Lib: {zustand | redux | jotai | context-only | none}
Libraries: {list with versions}
Health Score: {score}/100 ({clean | good | tangled | spaghetti})

STATE SOURCES
--------------
 #  | Source                | Type     | Consumers | Memoized | Status
----|----------------------|----------|-----------|----------|--------
 1  | AuthContext           | context  | 8         | Yes      | OK
 2  | ThemeContext          | context  | 12        | No       | WARN
 3  | useAppStore           | zustand  | 5         | n/a      | OK
 4  | ScheduleContext       | context  | 3         | No       | WARN
 5  | ToastContext          | context  | 2         | Yes      | OK
 6  | ModalContext          | context  | 4         | No       | WARN
 7  | FilterContext         | context  | 1         | No       | WARN

CONTEXT PROVIDERS AT ROOT ({count})
-------------------------------------
 AppProvider
   ├── AuthProvider
   ├── ThemeProvider
   ├── ScheduleProvider
   ├── ToastProvider
   ├── ModalProvider
   └── FilterProvider
 STATUS: SPRAWL (6 providers — consolidate related ones)

PROP DRILLING ({count} chains)
-------------------------------
 selectedDate: App → Dashboard → KanbanView → KanbanCard (depth: 3)
   → Suggest: Extract to context or zustand selector

RE-RENDER RISKS ({count})
---------------------------
 WARN  ThemeContext — value not memoized, 12 consumers re-render on every parent render
 WARN  ScheduleContext — component ScheduleList uses only `selectedDate` but subscribes to full context
 WARN  ModalContext — value not memoized, 4 consumers affected

ISSUES ({count})
-----------------
 HIGH   Context sprawl: 6 providers at root (max recommended: 5)
 HIGH   ThemeContext, ModalContext, FilterContext — missing useMemo on value
 HIGH   ScheduleList subscribes to full ScheduleContext but uses 1 field
 MEDIUM selectedDate prop drilled through 3 levels
 LOW    `isExpanded` state set but never read in ServiceCard.tsx

===========================
Next steps:
  1. Add useMemo to context values (3 contexts)
  2. Split ScheduleContext or use zustand
  3. Fix prop drilling with context extraction

What do you want to do?
```

---

## Integration with Other Tasks

```yaml
feeds_into:
  apex-suggest:
    what: "State issues become proactive suggestions"
    how: "Context sprawl, missing memoization, prop drilling flagged automatically"

  apex-audit:
    what: "State health score feeds audit report"
    how: "Health score becomes part of project readiness assessment"

  react-eng:
    what: "Kent receives full state architecture map"
    how: "No manual exploration needed — state sources pre-loaded"

  perf-eng:
    what: "Addy receives re-render risk data"
    how: "Context without slicing, missing memoization flagged for perf review"

  smart_defaults:
    what: "Auto-suggest zustand when context sprawl detected"
    how: "If sprawl detected, suggest migration path in apex-suggest"
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-DISC-STATE-001
    condition: "No React files found in project"
    action: BLOCK
    severity: HIGH
    blocking: true
    feeds_gate: null
    available_check: "test -d src/components || test -d src/ || test -d app/"
    on_unavailable: BLOCK

  - id: VC-DISC-STATE-002
    condition: "Context provider at root without useMemo on value"
    action: WARN
    severity: HIGH
    blocking: false
    feeds_gate: QG-AX-007
    available_check: "manual"
    on_unavailable: MANUAL_CHECK
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | apex-lead (routing enrichment), react-eng (state decisions), perf-eng (re-render data) |
| Next action | User fixes memoization, refactors context, or continues to other commands |

---

## Cache

```yaml
cache:
  location: ".aios/apex-context/state-cache.yaml"
  ttl: "Until state-related files change"
  invalidate_on:
    - "Any .tsx/.jsx file created, deleted, or modified"
    - "package.json modified (new state dependencies)"
    - "User runs *discover-state explicitly"
```

---

## Edge Cases

```yaml
edge_cases:
  - condition: "No state management library (useState only)"
    action: "REPORT as minimal state architecture, score 100 if no issues"
  - condition: "Monorepo with multiple packages"
    action: "ADAPT — scan each packages/*/src/ independently, merge results"
  - condition: "Server components (no client state)"
    action: "ADAPT — skip server component files, only scan 'use client' files"
  - condition: "Mixed state libs (zustand + redux + context)"
    action: "WARN — report mixing as architectural smell, suggest consolidation"
```

---

`schema_ref: data/discovery-output-schema.yaml`

---

*Apex Squad — State Management Discovery Task v1.0.0*
