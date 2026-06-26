# Task: sweep-navigator

```yaml
id: sweep-navigator
version: "1.0.0"
title: "Sweep Navigator"
description: >
  Engine de navegação interativa para resultados de sweep (visual ou
  código). Permite zoom in/out entre níveis (overview → domínio →
  seção → finding → fix), aceita input híbrido (números + linguagem
  natural), mantém contexto via breadcrumb, e re-calcula scores após
  cada fix aplicado. É o "cockpit" do usuário para navegar findings.
elicit: true
owner: apex-lead
executor: apex-lead
outputs:
  - Interactive navigation session
  - Progress tracking (resolved/total)
  - Score deltas after fixes
  - Session history log
```

---

## When This Task Runs

This task runs automatically after:
- `visual-intelligence-sweep` completes (Fase 4)
- `full-codebase-sweep` completes (Step 3)
- `*apex-status` is invoked (resume from cache)

This task does NOT run standalone — it's always part of a sweep.

---

## Navigation Architecture

### 4 Levels of Depth

```
Level 0: OVERVIEW
  Apex Score + domain breakdown + finding count
  └─ Level 1: DOMAIN
       Score + findings for one domain (e.g., A11y: 58/100)
       └─ Level 2: REGION or FINDING LIST
            Findings in one page section OR one domain
            └─ Level 3: INDIVIDUAL FINDING
                 Full detail + fix options + apply
```

### Navigation Commands

**Universal (work at any level):**

| Command | Action |
|---------|--------|
| `back` | Go up one level |
| `overview` | Jump to Level 0 |
| `status` | Show progress: "8/22 resolved, score 74→81" |
| `done` / `pronto` | Exit navigator, save state |
| `help` | Show available commands at current level |

**Level 0 (Overview):**

| Input | Action |
|-------|--------|
| Number (1-N) | Select numbered option |
| Domain name ("a11y", "css", "perf") | Jump to Level 1 for that domain |
| Section name ("hero", "header") | Jump to Level 2 for that section |
| "fix all HIGH" | Apply all HIGH severity fixes |
| "compare" / manda print | Enter comparison mode |
| "report" | Generate full markdown report |

**Level 1 (Domain):**

| Input | Action |
|-------|--------|
| Number (1-N) | Select specific finding |
| "fix all" | Fix all findings in this domain |
| "fix HIGH" | Fix only HIGH findings here |
| Section name | Filter findings by region |
| "back" | Return to Overview |

**Level 2 (Region/Findings):**

| Input | Action |
|-------|--------|
| Number (1-N) | View finding detail |
| "fix" | Fix the displayed finding |
| "fix all" | Fix all findings in this region |
| "skip" | Mark finding as intentional |
| "back" | Return to Domain or Overview |

**Level 3 (Individual Finding):**

| Input | Action |
|-------|--------|
| "fix" / "apply" / "1" | Apply the suggested fix |
| "alt" / "2" | Show alternative fix |
| "skip" | Mark as intentional, don't flag again |
| "explain" | Detailed explanation of why this matters |
| "back" | Return to finding list |

### Natural Language Parsing

The Navigator ALWAYS tries to understand natural language before falling back to "I don't understand":

| User Says | Navigator Does |
|-----------|---------------|
| "melhora o hero" | Filter findings by region "hero", offer batch fix |
| "corrige o contraste" | Filter findings by type "contrast", offer fix |
| "como ta o mobile?" | Show responsive/mobile findings across all domains |
| "quero estilo Apple" | Suggest `*apex-transform --style apple-liquid-glass` |
| "compara com esse" + print | Enter comparison mode with new print |
| "mostra só o que importa" | Filter to HIGH severity only |
| "quanto falta?" | Show status: remaining findings and projected score |
| "aplica tudo" | Apply all remaining fixes (with confirmation) |
| "próximo" | Move to next finding or next domain |

**Fallback:**
```
Não entendi. Você pode:
  - Digitar um número para selecionar opção
  - Dizer o nome de uma seção (hero, header, footer)
  - Dizer o nome de um domínio (a11y, css, perf)
  - Dizer "fix", "back", "overview", "done"
```

---

## Display Templates

### Breadcrumb (always visible)

```
 📍 Overview > Accessibility (58/100) > Finding #2
 Progress: 8/22 resolved │ Score: 74 → 79 (+5)
```

### After Fix Applied

```
 ✅ Fixed: Hero subtitle contrast 2.8:1 → 5.3:1
 File: src/components/Hero.tsx:42

 Accessibility: 58 → 64 (+6)  │  Apex Score: 74 → 76 (+2)

 Remaining in A11y: 5 findings (1 HIGH, 2 MED, 2 LOW)

 1. Next finding (CTA touch target)
 2. Fix remaining HIGH (1 left)
 3. Back to A11y overview
 4. Back to Overview
 5. Done
```

### Batch Fix Summary

```
 ✅ Batch Fix Complete — 6 HIGH findings resolved

 Files modified: 4
  - src/components/Hero.tsx (2 changes)
  - src/components/Header.tsx (1 change)
  - src/components/ServiceCard.tsx (2 changes)
  - src/components/ScheduleForm.tsx (1 change)

 Score: 74 → 84 (+10)  │  Remaining: 16 findings (0H, 9M, 7L)

 typecheck: ✅ PASS  │  lint: ✅ PASS

 1. Continue with MEDIUM findings
 2. Overview (see new scores)
 3. Commit changes
 4. Done
```

### Multi-Page View (multiple prints)

```
 📸 3 pages analyzed

 Page 1: Home (/)           Score: 78/100  │  8 findings
 Page 2: Services (/servicos) Score: 71/100  │  12 findings
 Page 3: About (/sobre)      Score: 82/100  │  5 findings

 Cross-page consistency: 85/100
  - 3 inconsistencies (1 HIGH: different header height)

 1. Analyze Page 1 (Home)
 2. Analyze Page 2 (Services)
 3. Analyze Page 3 (About)
 4. Fix cross-page inconsistencies
 5. Overview (all pages combined)
 6. Done
```

---

## State Management

### Session State

```yaml
navigator_state:
  level: 1  # current depth (0-3)
  breadcrumb: ["overview", "a11y"]
  current_domain: "a11y"
  current_region: null
  current_finding: null

  progress:
    total_findings: 22
    resolved: 8
    skipped: 2
    remaining: 12

  score_history:
    - { timestamp: "15:30:00", score: 74, event: "initial" }
    - { timestamp: "15:32:15", score: 76, event: "fixed A11Y-001" }
    - { timestamp: "15:33:40", score: 79, event: "batch fix 3 HIGH" }

  files_modified:
    - "src/components/Hero.tsx"
    - "src/components/Header.tsx"
```

### Resume (`*apex-status`)

When user invokes `*apex-status` or returns to conversation:

```
 📍 Sweep ativo (iniciado há 12 min)

 Score: 74 → 79 (+5)  │  8/22 resolved  │  14 remaining
 Último: Fixed contrast in Hero.tsx

 1. Continuar de onde parei (A11y > Finding #3)
 2. Ver overview atualizado
 3. Done (salvar progresso)
```

---

## Interaction Rules

1. **NEVER auto-execute fixes** — always present options first
2. **ALWAYS show breadcrumb** — user never loses context
3. **ALWAYS show score delta after fix** — instant feedback
4. **ALWAYS run typecheck/lint after fix** — catch regressions
5. **Max 1 batch fix per confirmation** — user approves each batch
6. **"done" saves state** — user can resume later
7. **Natural language has priority** over number parsing when ambiguous
8. **Numbers are 1-indexed** — option "1" is always the first displayed
9. **Pressing Enter with no input** shows current level options again
10. **"commit" at any point** triggers commit flow for modified files

---

## Quality Criteria

- User can reach any finding in ≤ 3 interactions from overview
- Breadcrumb accurately reflects current position
- Score re-calculation completes in < 2 seconds after fix
- Natural language parsing handles 90%+ of common requests
- Session state correctly persists for resume
- Batch fixes never leave code in broken state (typecheck after each)

---

*Squad Apex — Sweep Navigator Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-sweep-navigator
  blocker: true
  criteria:
    - "Navigator supports all 4 depth levels"
    - "Natural language + number input both work"
    - "Breadcrumb always accurate"
    - "Score delta shown after every fix"
    - "State persists for resume"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | User (interactive session) |
| Artifact | Navigation session with progress tracking |
| Next action | User continues navigating, or "done" to exit with state saved |
