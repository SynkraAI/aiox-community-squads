> **DEPRECATED** — Scope absorbed into `visual-intelligence-sweep.md`. See `data/task-consolidation-map.yaml`.

# Task: full-codebase-sweep

```yaml
id: full-codebase-sweep
version: "1.0.0"
title: "Full Codebase Sweep"
description: >
  Orquestra uma varredura completa do codebase usando TODOS os 11
  discovery tools em paralelo, sem necessidade de input visual.
  Analisa código, estrutura, dependências, padrões, e produz
  Apex Score baseado puramente na qualidade do código. Complementar
  ao visual-intelligence-sweep (que usa prints/URLs).
elicit: false
owner: apex-lead
executor: apex-lead
outputs:
  - Full discovery results (11 dimensions)
  - Apex Code Score (0-100) com breakdown
  - Finding list with fix recommendations
  - Codebase health dashboard
  - Sweep context cache
```

---

## When This Task Runs

This task runs when:
- User wants code analysis without visual input
- User asks "como ta o código?", "audita o projeto", "health check"
- `*apex-full` is invoked
- `*apex-audit` is invoked for comprehensive analysis

This task does NOT run when:
- Visual analysis needed (use `visual-intelligence-sweep`)
- Single discovery needed (use individual `*discover-*` command)
- Quick fix needed (use `*apex-fix`)

---

## Execution Steps

### Step 1: Run All Discovery Tools in Parallel

Execute all 11 discoveries simultaneously.

**Discovery matrix:**

| Discovery | Agent | Analyzes |
|-----------|-------|----------|
| `*discover-components` | @react-eng | Component tree, orphans, complexity, test coverage |
| `*discover-design` | @design-sys-eng | Tokens, violations, near-duplicates, DS score |
| `*discover-routes` | @frontend-arch | Route map, orphans, dead routes, SEO gaps |
| `*discover-dependencies` | @perf-eng | Outdated, vulnerable, heavy, unused packages |
| `*discover-motion` | @motion-eng | Animation inventory, CSS→spring violations, reduced-motion |
| `*discover-a11y` | @a11y-eng | Contrast, labels, ARIA, keyboard traps, heading structure |
| `*discover-performance` | @perf-eng | Lazy loading, images, re-renders, bundle, CWV |
| `*discover-state` | @react-eng | Context sprawl, prop drilling, unused state |
| `*discover-types` | @frontend-arch | TypeScript coverage, any usage, unsafe casts |
| `*discover-forms` | @interaction-dsgn | Validation gaps, error states, double submit |
| `*discover-security` | @frontend-arch | XSS vectors, exposed secrets, insecure storage |

**Parallel execution:**
- All 11 run simultaneously
- Each produces: health score (0-100) + findings list
- Timeout: 30 seconds per discovery
- If a discovery is not applicable (no forms → skip discover-forms), score = N/A

**Output:** Full discovery results.

### Step 2: Compute Apex Code Score

Aggregate discovery scores into unified code health score.

**Score weights:**

| Discovery | Weight | Rationale |
|-----------|--------|-----------|
| Components | 12% | Core building blocks |
| Design System | 10% | Visual consistency |
| Routes | 8% | Navigation health |
| Dependencies | 10% | Supply chain health |
| Motion | 5% | Animation quality |
| A11y | 18% | Accessibility (highest priority) |
| Performance | 15% | User experience |
| State | 8% | Data flow health |
| Types | 6% | Type safety |
| Forms | 5% | Input reliability |
| Security | 3% | Security posture (critical but binary) |

**Score = Σ(discovery_score × weight)**

**Output:** Apex Code Score.

### Step 3: Present Dashboard + Enter Navigator

Show unified dashboard and enter interactive navigation.

**Dashboard format:**
```
═══════════════════════════════════════════════════
 📊 APEX FULL — Codebase Sweep
 Project: my-app │ Stack: React + Vite + Tailwind
═══════════════════════════════════════════════════

 APEX CODE SCORE: 78/100  ██████████████████░░

 ┌─────────────────────────────────────────────┐
 │  Components     █████████████░░░░ 80       │
 │  Design System  █████████████░░░░ 81       │
 │  Routes         ██████████████░░░ 88       │
 │  Dependencies   ████████████░░░░░ 72  ⚠   │
 │  Motion         █████████████░░░░ 82       │
 │  Accessibility  ██████████░░░░░░░ 58  ⚠   │
 │  Performance    ████████████░░░░░ 76       │
 │  State          █████████████░░░░ 83       │
 │  Types          ██████████████░░░ 85       │
 │  Forms          ████████████░░░░░ 74       │
 │  Security       ██████████████░░░ 90       │
 └─────────────────────────────────────────────┘

 34 findings: 8 HIGH │ 14 MEDIUM │ 12 LOW

 ─────────────────────────────────────────────
 1. Fix all HIGH (8 fixes)
 2. Detalhar por domínio
 3. Focar em domínio específico
 4. Comparar com último sweep (se existir)
 5. Gerar relatório completo
 6. Combinar com *apex-vision (manda print)
 7. Done

 Ou: "corrige a11y", "atualiza dependências",
 "mostra components orphans", "foca em perf"
═══════════════════════════════════════════════════
```

**Navigator behavior:** Same as `sweep-navigator.md` — zoom in/out, natural language + options.

**Option 6 (Combinar com vision):** Launches `visual-intelligence-sweep` and merges results into a unified score that combines visual + code analysis = maximum coverage.

**Output:** Interactive Navigator session.

### Step 4: Cache Results

Store for use by subsequent commands.

**Cache at:** `.aios/apex-context/code-sweep-cache.yaml`

**Merged cache:** If `visual-intelligence-sweep` was also run, caches merge into `.aios/apex-context/unified-sweep-cache.yaml` with combined Apex Score.

**Output:** Sweep context cache.

---

## Quality Criteria

- All 11 discoveries complete within 60 seconds total
- Score reproducible (same code → same score ±2)
- Findings deduplicated across discoveries
- Navigator correctly enters/exits domain drill-downs
- Cache correctly consumed by subsequent *apex-fix calls
- N/A domains excluded from score calculation

---

*Squad Apex — Full Codebase Sweep Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-full-codebase-sweep
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All applicable discoveries complete"
    - "Score calculated per scoring model"
    - "Navigator functional with zoom in/out"
    - "Cache generated for subsequent commands"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | User (interactive) or `@apex-lead` |
| Artifact | Apex Code Score + findings + code sweep cache |
| Next action | User navigates via Navigator, or combine with `*apex-vision` for full coverage |
