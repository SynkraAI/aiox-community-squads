# Task: visual-intelligence-sweep

```yaml
id: visual-intelligence-sweep
version: "1.0.0"
title: "Visual Intelligence Sweep"
description: >
  Orquestra uma varredura visual completa do app/site usando TODOS os
  agentes do squad em paralelo. Aceita 3 tipos de entrada: screenshots
  (prints), URLs (sites ao vivo), ou ambos. Detecta automaticamente
  a estrutura da página (header, hero, body sections, footer, cards,
  CTAs, forms), executa análise multi-agente em 14 dimensões, e
  apresenta resultado unificado com Apex Score + Navigator interativo.
  O usuário navega com linguagem natural + opções numeradas.
elicit: false
owner: apex-lead
executor: apex-lead
outputs:
  - Page structure map (regiões semânticas detectadas)
  - Multi-agent sweep results (14 dimensões)
  - Apex Score (0-100) com breakdown por domínio
  - Finding list (HIGH/MEDIUM/LOW) com fix recommendations
  - Interactive Navigator session
  - Sweep context cache (para comandos subsequentes)
```

---

## When This Task Runs

This task runs when:
- User sends 1+ screenshots/prints of the app
- User provides a URL to analyze a live site
- User sends print + URL for cross-reference analysis
- User asks "como ta meu app?", "analisa isso", "faz uma varredura"
- `*apex-vision` is invoked
- `*apex-go` is invoked without prior sweep context

This task does NOT run when:
- Single-domain fix (use `*apex-fix` — but sweep context enriches it)
- Code-only analysis without visual (use `full-codebase-sweep`)
- Quick component fix (use `*apex-quick`)

---

## Input Detection (Fase 0)

Before any analysis, detect what the user provided.

### Input Types

| Input | Detection | What Apex Does |
|-------|-----------|----------------|
| **Screenshot/print** | Image file in message | Read image, detect structure, analyze visually |
| **URL** | `http://` or `https://` pattern | Navigate to URL, capture screenshots automatically, analyze |
| **URL + print** | Both detected | Cross-reference: live site vs screenshot (find drift) |
| **Multiple prints** | 2+ images | Multi-page consistency analysis + individual sweep |
| **Text only** | No image, no URL | Ask: "Manda um print ou URL para análise completa, ou prefere sweep só por código?" |

### URL Handling

When a URL is provided:

```
1. Navigate to URL (playwright or browser tool)
2. Capture full-page screenshot at 3 viewports:
   - Desktop (1920×1080)
   - Tablet (768×1024)
   - Mobile (375×812)
3. Scroll through page, capture each viewport section
4. Extract: page title, meta description, favicon, OG tags
5. Check: SSL, load time, response headers
6. Feed all captures into Structure Detection (Fase 1)
```

**Progressive capture for long pages:**
```
Homepage: scroll in 100vh increments, capture each "fold"
  Fold 1 (above the fold): header + hero
  Fold 2: first body section
  Fold 3: second body section
  ...
  Last fold: footer
```

### Cross-Reference Mode (URL + Print)

When user provides BOTH a URL and a print:
```
1. Capture live site at same viewport as print
2. Compare: print vs live site (visual diff)
3. Report: what changed since the print was taken
4. Run full sweep on BOTH versions
5. Show delta: "Print score: 72 → Live score: 78 (+6)"
```

---

## Execution Steps

### Fase 1: Structure Detection

Automatically identify every semantic region of the page.

**Detection patterns (from `data/structure-detection-patterns.yaml`):**

| Region | Visual Cues | Common Patterns |
|--------|------------|-----------------|
| **Header/Nav** | Top of page, horizontal bar, logo + links | Fixed/sticky, dark/glass, hamburger on mobile |
| **Hero** | Large heading, subtext, CTA, above the fold | Full-width, background image/gradient, centered |
| **Feature Cards** | Grid/flex of similar items, icons + text | 2-4 columns, equal height, hover effects |
| **Testimonials** | Quotes, avatars, stars | Carousel or grid, italic text |
| **Pricing** | Cards with prices, feature lists, CTAs | 3 tiers, highlighted "popular" |
| **CTA Section** | Large button, contrasting background | Full-width band, urgent copy |
| **Form** | Input fields, labels, submit button | Contact, signup, scheduling |
| **About/Bio** | Photo + text, credentials | Split layout, circular photo |
| **Stats/Numbers** | Large numbers, labels | Counter animation, grid |
| **Footer** | Bottom, links, copyright, social icons | Dark background, multi-column |
| **Sidebar** | Vertical panel, navigation or filters | Desktop only, collapsible |
| **Modal/Overlay** | Centered panel, backdrop | Glass effect, close button |

**Structure map output:**
```yaml
page_structure:
  url: "https://my-app.vercel.app"
  viewport: "1920x1080"
  folds: 4
  regions:
    - id: "header"
      type: "navigation"
      position: { top: 0, height: 64 }
      elements: ["logo", "nav-links", "cta-button"]
      agents: ["@css-eng", "@a11y-eng"]

    - id: "hero"
      type: "hero-section"
      position: { top: 64, height: 680 }
      elements: ["badge", "heading-h1", "subtitle", "cta-primary", "background-effect"]
      agents: ["@css-eng", "@motion-eng", "@a11y-eng", "@interaction-dsgn"]

    - id: "services"
      type: "feature-cards"
      position: { top: 744, height: 520 }
      elements: ["section-title", "card-grid-3col", "card-icons", "card-descriptions"]
      agents: ["@css-eng", "@react-eng", "@a11y-eng", "@design-sys-eng"]

    - id: "footer"
      type: "footer"
      position: { top: 1800, height: 200 }
      elements: ["logo", "links", "contact-info", "copyright"]
      agents: ["@css-eng", "@a11y-eng"]
```

**Output:** Page structure map with agent assignments.

### Fase 2: Multi-Agent Sweep

Run ALL agents in parallel, each analyzing their domain.

**Agent sweep matrix:**

| Agent | Analyzes | Produces |
|-------|----------|----------|
| `@css-eng` | Layout, spacing, responsive, tokens, z-index, overflow | CSS findings + score |
| `@react-eng` | Component patterns, hooks, state, error boundaries | React findings + score |
| `@motion-eng` | Transitions, animations, springs, scroll effects, reduced-motion | Motion findings + score |
| `@a11y-eng` | Contrast, touch targets, labels, headings, ARIA, keyboard | A11y findings + score |
| `@perf-eng` | Images, lazy load, bundle, LCP, CLS, fonts | Perf findings + score |
| `@design-sys-eng` | Token consistency, near-duplicates, design language | DS findings + score |
| `@interaction-dsgn` | UX patterns, CTAs, user flow, states, feedback | UX findings + score |
| `@qa-visual` | Alignment, pixel consistency, spacing uniformity | Visual QA findings + score |
| `@frontend-arch` | Component structure, file organization, patterns | Arch findings + score |
| `@spatial-eng` | 3D opportunities, spatial UI potential | Spatial findings + score |
| `@mobile-eng` | Mobile/RN readiness, gesture patterns | Mobile findings + score |
| `@cross-plat-eng` | Universal patterns, platform parity | Cross-plat findings + score |
| `@i18n-eng` | Translation readiness, hardcoded strings, RTL | i18n findings + score |
| `@error-eng` | Error boundaries, fallback UI, crash recovery | Error findings + score |

**Each agent produces:**
```yaml
agent_result:
  agent: "@a11y-eng"
  score: 58
  findings:
    - id: "A11Y-001"
      severity: HIGH
      region: "hero"
      element: "subtitle"
      issue: "Contrast ratio 2.8:1 (needs 4.5:1)"
      fix: "Change text-slate-400 → text-slate-700"
      file: "src/components/Hero.tsx"
      line: 42
    - id: "A11Y-002"
      severity: HIGH
      region: "header"
      element: "cta-button"
      issue: "Touch target 32×32px (needs 44×44px)"
      fix: "Add min-h-11 min-w-11 padding"
      file: "src/components/Header.tsx"
      line: 18
```

**Parallel execution:**
- All 14 agents run simultaneously
- Each agent receives: structure map + print/URL data + codebase access
- Timeout: 60 seconds per agent (graceful degradation if one fails)
- If an agent's domain is not present (e.g., no 3D → @spatial-eng), skip silently

**Output:** Multi-agent sweep results.

### Fase 3: Aggregation + Apex Score

Compute unified score and organize findings.

**Apex Score calculation (from `data/sweep-scoring-model.yaml`):**

```
Apex Score = Σ (domain_score × domain_weight)

Weights (total = 100%):
  CSS/Layout:     15%
  React:          10%
  Motion:          8%
  A11y:           18%  ← highest weight (accessibility is critical)
  Performance:    15%
  Design System:  10%
  UX/Interaction: 10%
  Visual QA:       8%
  Architecture:    6%

Optional domains (if detected):
  Spatial:     bonus +2
  Mobile:      bonus +2
  Cross-plat:  bonus +2
  i18n:        bonus +2
  Error:       bonus +2
```

**Score interpretation:**

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Elite | Production-ready, best practices everywhere |
| 80-89 | Strong | Minor improvements possible |
| 70-79 | Good | Some areas need attention |
| 60-69 | Fair | Several issues, prioritize HIGH findings |
| < 60 | Needs Work | Significant improvements needed |

**Finding aggregation:**
```
All findings sorted by:
  1. Severity (HIGH → MEDIUM → LOW)
  2. Region (header → hero → body → footer)
  3. Agent (grouped by domain)

Deduplication:
  - Same element flagged by multiple agents → merge, keep highest severity
  - Example: @a11y-eng and @css-eng both flag contrast → single finding
```

**Output:** Apex Score + aggregated findings.

### Fase 4: Interactive Navigator

Present results and enter navigation loop.

**Initial presentation:**
```
═══════════════════════════════════════════════════
 📸 APEX VISION — Sweep Completo
 Source: [print] my-app / 1920×1080
═══════════════════════════════════════════════════

 APEX SCORE: 74/100  ████████████████░░░░

 ┌─────────────────────────────────────────────┐
 │  CSS/Layout      ██████████████░░ 85       │
 │  React           █████████████░░░ 82       │
 │  Motion          ████████████░░░░ 76       │
 │  Accessibility   ██████████░░░░░░ 58  ⚠   │
 │  Performance     ████████████░░░░ 79       │
 │  Design System   █████████████░░░ 81       │
 │  UX/Interaction  ████████████░░░░ 78       │
 │  Visual QA       ███████████░░░░░ 68       │
 └─────────────────────────────────────────────┘

 Estrutura detectada:
  Header ✅ │ Hero ⚠ 3 │ Services ⚠ 2 │ Footer ✅

 22 findings: 6 HIGH │ 9 MEDIUM │ 7 LOW

 ─────────────────────────────────────────────
 1. Fix all HIGH (6 fixes)
 2. Detalhar por domínio
 3. Detalhar por seção (header, hero, services...)
 4. Comparar com referência (manda outro print/URL)
 5. Gerar relatório completo
 6. Done

 Ou diga naturalmente: "melhora o hero", "corrige a11y",
 "quero estilo Stripe", "mostra o mobile"
═══════════════════════════════════════════════════
```

**Navigator rules:**
- See `tasks/sweep-navigator.md` for complete navigation logic
- User input is ALWAYS parsed as: number OR natural language
- Context breadcrumb always visible (Overview > A11y > Finding #2)
- "back" goes up one level, "overview" returns to score dashboard
- After each fix: re-score affected domain, show delta
- "status" shows progress: "8/22 findings resolved, score 74→81"

**Output:** Interactive Navigator session.

### Fase 5: Context Cache

Store sweep results for use by subsequent commands.

**Cache location:** `.aios/apex-context/sweep-cache.yaml`

**Cache contains:**
```yaml
sweep_cache:
  timestamp: "2026-03-11T15:30:00Z"
  source: "print + code"
  apex_score: 74
  structure_map: { ... }
  findings: [ ... ]
  resolved: [ ... ]

  # Enriches subsequent commands:
  # *apex-fix → knows which files, which lines
  # *apex-quick → knows priority order
  # *apex-go → skips scan phase, uses cached structure
```

**Cache rules:**
- Valid for current session + 24 hours
- Invalidated if: git commit changes >5 files, or user requests fresh sweep
- Partial invalidation: if user fixes 1 file, only that region re-scans
- `*apex-status` reads from cache without re-running sweep

**Output:** Sweep context cache.

---

## Quality Criteria

- Structure detection identifies 90%+ of page regions correctly
- All 14 agents produce results within 60 seconds
- Apex Score is reproducible (same input → same score ±2)
- Navigator never loses context (breadcrumb always accurate)
- Natural language input correctly routes 90%+ of the time
- URL capture produces consistent screenshots across runs
- Cache correctly enriches subsequent commands
- Print + URL cross-reference shows meaningful drift detection

---

*Squad Apex — Visual Intelligence Sweep Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-visual-intelligence-sweep
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Structure detection covers 90%+ of regions"
    - "All active agents produce results"
    - "Apex Score calculated correctly per scoring model"
    - "Navigator maintains context across interactions"
    - "URL and print inputs both handled"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | User (interactive) or `@apex-lead` (pipeline) |
| Artifact | Apex Score + findings + sweep context cache |
| Next action | User navigates findings via Navigator, or `*apex-fix` / `*apex-go` consumes cache |
