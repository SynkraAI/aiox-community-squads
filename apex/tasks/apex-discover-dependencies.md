# Task: apex-discover-dependencies

```yaml
id: apex-discover-dependencies
version: "1.1.0"
title: "Apex Discover Dependencies"
description: >
  Audits frontend dependency health. Detects outdated, vulnerable, heavy,
  duplicated, and unused packages. Estimates bundle impact per dependency.
  Feeds performance-audit and bundle-optimization tasks.
elicit: false
owner: apex-lead
executor: perf-eng
dependencies:
  - tasks/apex-scan.md
  - tasks/bundle-optimization.md
  - tasks/performance-audit.md
outputs:
  - Dependency health report
  - Heavy packages list with alternatives
  - Unused packages list
  - Dependency health score
```

---

## Command

### `*discover-dependencies`

Audits all frontend dependencies for health, weight, and security.

---

## Discovery Phases

### Phase 1: Inventory Dependencies

```yaml
inventory:
  sources:
    - package.json (dependencies + devDependencies)
    - package-lock.json / yarn.lock / pnpm-lock.yaml (resolved versions)
    - node_modules (actual installed)

  per_dependency:
    name: "{package name}"
    installed_version: "{current}"
    latest_version: "{latest from registry}"
    versions_behind: N
    type: "production | dev"
    category: "framework | ui | utility | build | test | types"
    size_estimate: "{bundlephobia size}"
    tree_shakeable: true | false
    esm_support: true | false
    last_publish: "{date}"
    weekly_downloads: N
    imported_in: ["{files that import it}"]
    import_count: N
```

### Phase 2: Detect Issues

```yaml
checks:

  outdated:
    description: "Packages behind latest version"
    classification:
      patch_behind: "LOW — minor fixes available"
      minor_behind: "MEDIUM — features/fixes available"
      major_behind: "HIGH — breaking changes, potentially insecure"
      abandoned: "CRITICAL — no publish in 2+ years"
    detection: "Compare installed vs latest from npm registry"

  vulnerable:
    description: "Known security vulnerabilities"
    detection: "npm audit --json OR yarn audit --json"
    classification:
      low: "LOW"
      moderate: "MEDIUM"
      high: "HIGH"
      critical: "CRITICAL"

  heavy:
    description: "Packages that significantly inflate bundle"
    thresholds:
      warning: "> 50KB minified+gzipped"
      critical: "> 150KB minified+gzipped"
    known_heavy:
      - name: "moment"
        size: "~72KB"
        alternative: "dayjs (~2KB), date-fns (tree-shakeable)"
      - name: "lodash"
        size: "~72KB"
        alternative: "lodash-es (tree-shakeable), native methods"
      - name: "axios"
        size: "~14KB"
        alternative: "fetch API (native, 0KB)"
      - name: "jquery"
        size: "~87KB"
        alternative: "Native DOM APIs"
      - name: "chart.js"
        size: "~200KB"
        alternative: "recharts (tree-shakeable), lightweight-charts"
      - name: "antd"
        size: "~1.2MB unpacked"
        alternative: "Import specific components: import Button from 'antd/es/button'"

  duplicated:
    description: "Same package in multiple versions"
    detection: "Multiple entries in lock file for same package name"
    severity: MEDIUM
    impact: "Bundle bloat — same code shipped twice"

  unused:
    description: "Installed but never imported"
    detection: "Package in dependencies but no import/require found in src/"
    exclude:
      - "Packages used in config files (postcss, tailwindcss, vite plugins)"
      - "Type packages (@types/*)"
      - "CLI tools (eslint, prettier)"
      - "Build plugins"
    severity: LOW

  missing_types:
    description: "Package used without TypeScript types"
    detection: "Import exists, package has no built-in types, @types/{name} not installed"
    severity: LOW
```

### Phase 3: Calculate Dependency Health Score

```yaml
health_score:
  formula: "100 - (penalties)"
  penalties:
    critical_vulnerability: -15 each
    high_vulnerability: -10 each
    major_outdated: -5 each
    heavy_package_no_alternative: -3 each
    heavy_package_with_alternative: -5 each
    duplicated_package: -3 each
    unused_package: -1 each
    abandoned_package: -8 each

  classification:
    90-100: "healthy — dependencies well-maintained"
    70-89: "good — some updates needed"
    50-69: "aging — significant maintenance needed"
    0-49: "critical — security and performance risks"
```

### Phase 4: Output

```yaml
output_format: |
  ## Dependency Discovery

  **Package Manager:** {npm|yarn|pnpm}
  **Total Dependencies:** {prod} production + {dev} dev
  **Dependency Health Score:** {score}/100 ({classification})

  ### Issues Found

  | Category | Count | Severity |
  |----------|-------|----------|
  | Vulnerable | {n} | {worst severity} |
  | Major outdated | {n} | HIGH |
  | Heavy (with alternative) | {n} | MEDIUM |
  | Duplicated | {n} | MEDIUM |
  | Unused | {n} | LOW |

  ### Heavy Packages — Swap Recommendations
  | Package | Size | Alternative | Savings |
  |---------|------|-------------|---------|
  | {name} | {size} | {alt} | ~{savings} |

  ### Unused Packages (safe to remove)
  | Package | Installed | Last import |
  |---------|-----------|-------------|
  | {name} | {version} | never |

  ### Options
  1. Remover {unused_count} pacotes nao usados
  2. Atualizar {outdated_count} pacotes desatualizados
  3. Substituir {heavy_count} pacotes pesados por alternativas leves
  4. So quero o relatorio
```

---

## Integration with Other Tasks

```yaml
feeds_into:
  apex-suggest:
    what: "Dependency issues become proactive suggestions"
    how: "Heavy, unused, vulnerable packages flagged"
  apex-audit:
    what: "Dependency health feeds audit report"
    how: "Health score part of project readiness"
  perf-eng:
    what: "Bundle impact data for perf analysis"
    how: "Heavy deps with sizes feed performance decisions"
  veto_gate_QG-AX-007:
    what: "Heavy deps feed bundle budget gate"
    how: "Discovery provides exact list of bundle-impacting packages"
  smart_defaults:
    what: "Auto-suggest alternatives for heavy packages"
    how: "moment → dayjs, lodash → native methods"
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-DISC-DEP-001
    condition: "Critical vulnerability found in production dependency"
    action: "WARN — Update or replace vulnerable package before shipping."
    available_check: "command:npm audit --json"
    on_unavailable: MANUAL_CHECK
    feeds_gate: QG-AX-007
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | apex-lead (overview), perf-eng (bundle decisions) |
| Next action | User removes unused, updates outdated, or swaps heavy packages |

---

## Cache

```yaml
cache:
  location: ".aios/apex-context/dependency-cache.yaml"
  ttl: "Until package.json or lock file changes"
  invalidate_on:
    - "package.json modified"
    - "package-lock.json / yarn.lock / pnpm-lock.yaml modified"
    - "User runs *discover-dependencies explicitly"
```

---

## Edge Cases

```yaml
edge_cases:
  - condition: "Monorepo with multiple package.json"
    action: "ADAPT — scan each workspace root, merge results"
  - condition: "No lock file found"
    action: "WARN — versions may not be pinned, security audit limited"
  - condition: "pnpm workspaces"
    action: "ADAPT — use pnpm list --json instead of npm"
  - condition: "Private registry packages"
    action: "ADAPT — skip version check for private scope, report as unknown"
```

---

`schema_ref: data/discovery-output-schema.yaml`

---

*Apex Squad — Discover Dependencies Task v1.1.0*
