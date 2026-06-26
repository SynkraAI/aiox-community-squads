# Task: apex-discover-types

```yaml
id: apex-discover-types
version: "1.0.0"
title: "TypeScript Coverage Discovery"
description: >
  Scans TypeScript coverage and type safety across the project.
  Detects any usage, unsafe casts, missing types, untyped props,
  implicit any, and generic misuse. Code-level type health analysis.
  Transforms "is our TypeScript strict?" into "I already scanned
  every file — here's the exact type safety landscape."
elicit: false
owner: apex-lead
executor: react-eng
dependencies:
  - tasks/apex-scan.md
outputs:
  - tsconfig strictness analysis
  - Per-file type coverage metrics
  - Explicit any usage inventory
  - Unsafe cast inventory (as any, as unknown as T)
  - ts-ignore and ts-nocheck file list
  - Untyped component props
  - Missing return types on exports
  - Type health score (0-100)
```

---

## Command

### `*discover-types`

Scans the project and analyzes TypeScript coverage and type safety. Runs as part of `*apex-audit` or independently.

---

## Discovery Phases

### Phase 1: Scan TypeScript Config

```yaml
tsconfig_analysis:
  scan:
    - "tsconfig.json"
    - "tsconfig.app.json"
    - "tsconfig.node.json"
    - "packages/*/tsconfig.json"

  check_strict_flags:
    - strict: "master flag — enables all strict checks"
    - noImplicitAny: "error on implicit any"
    - strictNullChecks: "null/undefined must be handled"
    - strictFunctionTypes: "contravariant function params"
    - strictBindCallApply: "correct bind/call/apply types"
    - noUncheckedIndexedAccess: "array/object index returns T | undefined"
    - exactOptionalPropertyTypes: "undefined vs missing"
    - noImplicitReturns: "all code paths return"
    - noFallthroughCasesInSwitch: "switch cases must break/return"
    - noImplicitOverride: "override keyword required"

  classify_strictness:
    full_strict: "strict: true AND noUncheckedIndexedAccess AND exactOptionalPropertyTypes"
    strict: "strict: true (default strict flags)"
    partial: "some strict flags enabled but not all"
    loose: "strict: false or missing"

  extract:
    - target: "ESNext, ES2022, etc"
    - module: "ESNext, CommonJS, etc"
    - jsx: "react-jsx, react, preserve"
    - paths: "path aliases configured"
    - include_exclude: "what files are covered"
```

### Phase 2: Analyze Type Coverage

```yaml
type_coverage:
  scan:
    - "src/**/*.tsx"
    - "src/**/*.ts"
    - "app/**/*.tsx"
    - "app/**/*.ts"
    - "packages/**/src/**/*.ts"
    - "packages/**/src/**/*.tsx"
  exclude:
    - "**/*.test.ts"
    - "**/*.test.tsx"
    - "**/*.spec.ts"
    - "**/*.d.ts"
    - "**/node_modules/**"

  for_each_file:
    count:
      - explicit_any: "occurrences of `: any`, `<any>`, `any[]`"
      - as_any: "occurrences of `as any`"
      - as_unknown_cast: "occurrences of `as unknown as T`"
      - ts_ignore: "`@ts-ignore` comments"
      - ts_expect_error: "`@ts-expect-error` comments (with or without explanation)"
      - ts_nocheck: "`// @ts-nocheck` at file top"
      - untyped_params: "function parameters without type annotation"
      - missing_return_type: "exported functions without explicit return type"

    react_specific:
      - untyped_props: "React.FC without generic, or function component without Props type"
      - untyped_state: "useState without type parameter on complex values"
      - untyped_ref: "useRef without type parameter"
      - untyped_event_handler: "event handlers with implicit `any` event"

    extract:
      - file_path: "relative path"
      - total_issues: "sum of all type issues"
      - severity: "critical (ts_nocheck) | high (any, unsafe cast) | medium | low"
```

### Phase 3: Detect Issues

```yaml
issue_detection:
  - id: explicit_any
    condition: "Direct use of `any` type (`: any`, `any[]`, `<any>`)"
    severity: HIGH
    impact: "Disables type checking for that value and all downstream usage"
    suggestion: "Replace with `unknown`, specific type, or generic"

  - id: unsafe_cast
    condition: "`as any` or `as unknown as T` cast"
    severity: HIGH
    impact: "Bypasses type system entirely, hides real type errors"
    suggestion: "Fix the underlying type mismatch or use type guard"

  - id: ts_ignore
    condition: "`@ts-ignore` without explanation comment"
    severity: MEDIUM
    impact: "Silences errors that may indicate real bugs"
    suggestion: "Use `@ts-expect-error` with explanation, or fix the error"
    note: "`@ts-expect-error` with comment is acceptable (documents known limitation)"

  - id: ts_nocheck
    condition: "Entire file has `// @ts-nocheck`"
    severity: CRITICAL
    impact: "Entire file has zero type safety — equivalent to JavaScript"
    suggestion: "Remove @ts-nocheck and fix type errors incrementally"

  - id: untyped_props
    condition: "React component without Props interface or type parameter"
    severity: MEDIUM
    impact: "Component accepts any props without validation"
    suggestion: "Define Props interface and apply to component"

  - id: implicit_any
    condition: "Function parameter without type (when noImplicitAny is off)"
    severity: MEDIUM
    impact: "Parameter treated as any, no autocompletion or type checking"
    suggestion: "Add type annotation or enable noImplicitAny in tsconfig"

  - id: missing_return_type
    condition: "Exported function without explicit return type"
    severity: LOW
    impact: "Return type inferred — safe but less explicit for API consumers"
    suggestion: "Add explicit return type for exported functions"

  - id: loose_tsconfig
    condition: "strict mode disabled or key strict checks off"
    severity: HIGH
    impact: "Entire project has weakened type checking"
    suggestion: "Enable strict: true in tsconfig.json"
```

### Phase 4: Health Score

```yaml
health_score:
  formula: >
    100 - (ts_nocheck_count * 15) - (explicit_any_count * 2)
    - (unsafe_cast_count * 3) - (ts_ignore_count * 2)
    - (untyped_props_count * 3) - (loose_tsconfig * 10)
    - (implicit_any_count * 1) - (missing_return_type_count * 0.5)
  max: 100
  min: 0
  thresholds:
    strict: ">= 90 — strong type safety, well maintained"
    typed: "70-89 — good coverage with some gaps"
    loose: "50-69 — significant type safety issues"
    unsafe: "< 50 — type system effectively disabled in many areas"
```

---

## Output Format

```
TYPESCRIPT COVERAGE DISCOVERY
===============================
Project: {name}
TypeScript: {version}
Strictness: {full_strict | strict | partial | loose}
Health Score: {score}/100 ({strict | typed | loose | unsafe})

TSCONFIG ANALYSIS
------------------
 Flag                          | Status | Impact
-------------------------------|--------|-------
 strict                        | ON     | Master strict flag
 noImplicitAny                 | ON     | No implicit any
 strictNullChecks              | ON     | Null safety
 noUncheckedIndexedAccess      | OFF    | Array index returns T (not T|undefined)
 exactOptionalPropertyTypes    | OFF    | Optional props strict

 Strictness Level: strict (2 flags could be stricter)

FILE COVERAGE
--------------
 Total .ts/.tsx files: {count}
 Files with issues: {count} ({percentage}%)
 Files with @ts-nocheck: {count}

TYPE ISSUES BY CATEGORY
-------------------------
 Category              | Count | Severity | Top Files
-----------------------|-------|----------|----------
 explicit_any          | 12    | HIGH     | api.ts (5), utils.ts (3)
 unsafe_cast (as any)  | 4     | HIGH     | ServiceForm.tsx (2)
 @ts-ignore            | 3     | MEDIUM   | legacy.ts (2)
 @ts-nocheck           | 1     | CRITICAL | oldModule.ts
 untyped_props         | 6     | MEDIUM   | Card.tsx, Modal.tsx, ...
 implicit_any          | 8     | MEDIUM   | handlers.ts (4)
 missing_return_type   | 15    | LOW      | (various exported fns)

TOP OFFENDERS (most issues per file)
--------------------------------------
 #  | File                    | Issues | Worst
----|-------------------------|--------|------
 1  | src/api/api.ts          | 8      | 5x explicit_any
 2  | src/utils/legacy.ts     | 5      | 2x @ts-ignore, 1x @ts-nocheck
 3  | src/components/Form.tsx | 4      | 2x as any, untyped props
 4  | src/handlers.ts         | 4      | 4x implicit_any

REACT-SPECIFIC
---------------
 Components without typed props: 6
   - Card.tsx (no Props interface)
   - Modal.tsx (React.FC without generic)
   - Badge.tsx (inline props, untyped)
   - ... (3 more)

 Untyped hooks:
   - useState without type: 3 occurrences
   - useRef without type: 2 occurrences

===============================
Next steps:
  1. Fix @ts-nocheck file (oldModule.ts) — highest impact
  2. Replace 12 explicit `any` with proper types
  3. Add Props interfaces to 6 components
  4. Enable noUncheckedIndexedAccess for stricter safety

What do you want to do?
```

---

## Integration with Other Tasks

```yaml
feeds_into:
  apex-suggest:
    what: "Type safety issues become proactive suggestions"
    how: "any usage, unsafe casts, loose tsconfig flagged automatically"

  apex-audit:
    what: "Type health score feeds audit report"
    how: "Health score becomes part of project readiness assessment"

  react-eng:
    what: "Kent receives full type coverage map"
    how: "Knows which files need type improvements before touching them"

  apex-code-review:
    what: "Type safety dimension in code review"
    how: "Review checks new code against project type standards"

  smart_defaults:
    what: "Auto-suggest strict tsconfig for new projects"
    how: "If loose_tsconfig detected, suggest enabling strict mode"
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-DISC-TYPES-001
    condition: "No tsconfig.json found (JavaScript project)"
    action: ADAPT
    severity: MEDIUM
    blocking: false
    feeds_gate: null
    available_check: "test -f tsconfig.json"
    on_unavailable: SKIP_WITH_WARNING

  - id: VC-DISC-TYPES-002
    condition: "strict mode disabled in tsconfig.json"
    action: WARN
    severity: HIGH
    blocking: false
    feeds_gate: QG-AX-010
    available_check: "test -f tsconfig.json"
    on_unavailable: SKIP_WITH_WARNING
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | apex-lead (routing enrichment), react-eng (type improvement targets) |
| Next action | User fixes type issues by severity, enables strict flags, or continues to other commands |

---

## Cache

```yaml
cache:
  location: ".aios/apex-context/types-cache.yaml"
  ttl: "Until TypeScript files change"
  invalidate_on:
    - "Any .ts/.tsx file created, deleted, or modified"
    - "tsconfig.json modified"
    - "User runs *discover-types explicitly"
```

---

## Edge Cases

```yaml
edge_cases:
  - condition: "JavaScript project (no TypeScript)"
    action: "ADAPT — scan .js/.jsx files for JSDoc type annotations, report coverage"
  - condition: "No tsconfig.json found"
    action: "WARN — report as untyped project, suggest adding TypeScript"
  - condition: "Monorepo with multiple tsconfig files"
    action: "ADAPT — scan each tsconfig independently, report per-package scores"
  - condition: "Project uses both .ts and .js files"
    action: "ADAPT — report TS coverage percentage, flag .js files as migration candidates"
```

---

`schema_ref: data/discovery-output-schema.yaml`

---

*Apex Squad — TypeScript Coverage Discovery Task v1.0.0*
