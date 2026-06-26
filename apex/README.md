<p align="center">
  <strong>⚡ APEX SQUAD</strong><br>
  <em>Autonomous Frontend Intelligence</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/agents-15-blue?style=flat-square" alt="15 agents" />
  <img src="https://img.shields.io/badge/tasks-161-green?style=flat-square" alt="161 tasks" />
  <img src="https://img.shields.io/badge/veto_conditions-154-red?style=flat-square" alt="154 veto conditions" />
  <img src="https://img.shields.io/badge/design_presets-52-purple?style=flat-square" alt="52 presets" />
  <img src="https://img.shields.io/badge/discovery_tools-13-teal?style=flat-square" alt="13 discoveries" />
  <img src="https://img.shields.io/badge/intent_chains-50-yellow?style=flat-square" alt="50 intent chains" />
  <img src="https://img.shields.io/badge/version-1.7.0-orange?style=flat-square" alt="v1.7.0" />
</p>

---

> **15 specialized agents** with DNA from elite frontend minds.
> **154 veto conditions** across 37 quality gates — physical blocks, not suggestions.
> **50 conditional intent chains** — "what's next?" after every operation.
> **18 formal handoff protocols** — explicit inter-agent delegation with conflict resolution.
> **101 heuristics** with centralized source attribution (93 OURO, 1 MIXED, 7 INFERRED).
> **13 discovery tools** scanning every frontend dimension.
> **7 workflows with standardized rollback** — 6-step recovery protocol per phase.
> **14 web intelligence commands** — scrape, extract, compare, fuse from any URL.
> **Vocabulary bridge** — zero technical jargon required from users.
> **Greenfield to polish** — create entire projects from a single description.
> Everything the user sees and touches: design systems, components, animations, 3D/spatial, accessibility, performance.

---

## Quick Start

```
@apex "the header layout breaks on mobile viewports"
```

That's it. Apex automatically:

1. **Scans** the project (stack, structure, design patterns)
2. **Classifies** the intent (fix, improve, create, redesign, audit)
3. **Selects** the pipeline (`*apex-fix` → single agent)
4. **Routes** to the right specialist (`Josh @css-eng`)
5. **Confirms** understanding in plain language before executing
6. **Suggests** the next logical step after completion

**Zero friction. Describe the outcome, Apex handles the implementation.**

---

## Table of Contents

- [Platforms](#platforms)
- [Agents](#agents-15)
- [How It Works](#how-it-works)
- [Commands](#commands)
- [Greenfield — Build from Scratch](#greenfield--build-from-scratch)
- [Web Intelligence](#web-intelligence--web-intel)
- [Intent Clarification](#intent-clarification--vocabulary-bridge)
- [Scope Lock & Rollback](#scope-lock--rollback)
- [Discovery Tools](#discovery-tools-13)
- [Vision Intelligence](#vision-intelligence)
- [Style Presets](#style-presets-31)
- [Intelligence Layer](#intelligence-layer)
- [Implicit Heuristics](#implicit-heuristics-8)
- [Agent Blind Spots](#agent-blind-spots)
- [Quality Gates](#quality-gates)
- [Agent Handoff Matrix](#agent-handoff-matrix)
- [Heuristic Source Map](#heuristic-source-map)
- [Workflow Rollback Protocol](#workflow-rollback-protocol)
- [Pipeline](#pipeline-7-phases)
- [Design Philosophy](#design-philosophy)
- [Performance Standards](#performance-standards)
- [Project Structure](#project-structure)

---

## Platforms

| Platform | Stack |
|----------|-------|
| **Web** | Next.js 15+, React 19+, App Router, RSC-first |
| **Mobile** | React Native New Architecture, Expo SDK 52+ |
| **Spatial** | VisionOS, WebXR, Three.js, React Three Fiber |

---

## Agents (15)

Organized in 5 tiers + orchestrator. Each agent carries the DNA of a real-world frontend reference.

| Icon | Name | ID | Tier | DNA Source | Specialty |
|------|------|----|------|------------|-----------|
| ⚡ | Emil | `apex-lead` | Orchestrator | Emil Kowalski | Design Engineering Lead — routes, coordinates, approves |
| 🏛️ | Arch | `frontend-arch` | T1 | Lee Robinson | Frontend architecture, RSC, monorepo |
| 🎨 | Ahmad | `interaction-dsgn` | T2 | Ahmad Shadeed | UX patterns, interaction design |
| 🎯 | Diana | `design-sys-eng` | T2 | Diana Mounter | Design system, tokens, themes |
| 🔍 | Kilian | `web-intel` | T2 | Kilian Valkhof | Web intelligence, design extraction, asset curation |
| 🎭 | Josh | `css-eng` | T3 | Josh Comeau | CSS architecture, layout, responsive |
| ⚛️ | Kent | `react-eng` | T3 | Kent C. Dodds | React components, hooks, testing |
| 📱 | Krzysztof | `mobile-eng` | T3 | Krzysztof Magiera | React Native, gestures, worklets |
| 🌐 | Fernando | `cross-plat-eng` | T3 | Fernando Rojo | Cross-platform, universal components |
| 🌌 | Paul | `spatial-eng` | T3 | Paul Henschel | 3D, WebXR, VisionOS, shaders |
| 🎬 | Matt | `motion-eng` | T4 | Matt Perry | Spring animations, choreography |
| ♿ | Sara | `a11y-eng` | T4 | Sara Soueidan | WCAG, keyboard, screen readers |
| 🚀 | Addy | `perf-eng` | T4 | Addy Osmani | Core Web Vitals, bundle, loading |
| 👁️ | Andy | `qa-visual` | T5 | Andy Bell | Visual regression, cross-browser |
| 📋 | Michal | `qa-xplatform` | T5 | Michal Pierzchala | Cross-platform device testing |

### Auto-Profile Detection

| Profile | Active Agents | When |
|---------|---------------|------|
| `full` (15) | All | Monorepo web + mobile + spatial |
| `web-next` (11) | No mobile/spatial/cross-plat | Next.js projects |
| `web-spa` (9) | apex-lead, interaction-dsgn, web-intel, css-eng, react-eng, motion-eng, a11y-eng, perf-eng, qa-visual | React + Vite SPA |
| `minimal` (4) | apex-lead, css-eng, react-eng, a11y-eng | Quick fixes |

Detected automatically from `package.json`. No manual configuration.

---

## How It Works

### Agent Handoff — Visible Delegation

Every delegation is **visible**. You always know who is working and why.

```
User: "the header breaks on mobile viewports"

Emil: This is a responsive CSS issue — delegating to 🎭 Josh (@css-eng).
      He specializes in layout algorithms and stacking contexts.

🎭 Josh here. The header uses flexbox without flex-wrap — breaks below 375px.
   [analyzes, fixes]

🎭 Josh — done.
   1 file modified (Header.tsx). Typecheck PASS. Lint PASS.

   Recommend verifying with ♿ Sara (@a11y-eng) — touch targets changed.

   1. Verify a11y with Sara
   2. Run suggestions on Header.tsx
   3. Done

User: "1"

♿ Sara here. Touch targets at 38x38px — below the 44x44 minimum.
   [fixes padding]

♿ Sara — done. 1 file modified. Typecheck PASS.
   1. Run suggestions  2. Done
```

### Common Agent Chains

| Scenario | Sequence |
|----------|----------|
| CSS fix | Josh → Sara (a11y) |
| New animation | Matt → Sara (reduced-motion) → Addy (60fps) |
| New component | Kent → Josh (style) → Matt (motion) → Sara (a11y) |
| Responsive fix | Josh → Andy (cross-browser) |
| Design system | Diana → Josh (CSS tokens) → Andy (visual regression) |
| Dark mode | Diana → Sara (contrast) → Andy (visual test) |
| Design extraction | Kilian (scrape) → Diana (fuse tokens) → Josh (implement) |
| Asset curation | Kilian (hunt) → Addy (optimize) → Paul (3D if needed) |
| Design comparison | Kilian (compare) → Diana (token mapping) → Andy (visual QA) |
| Inspiration flow | Kilian (inspire) → Ahmad (interaction) → Diana (tokens) |

---

## Commands

### Natural Entry (recommended)

```
@apex {any description in natural language}
```

### Pipeline

| Command | What it does |
|---------|-------------|
| `*apex-greenfield {desc}` | **Build entire project from scratch** (8 phases, all agents) |
| `*apex-go {desc}` | Full 7-phase pipeline (autonomous, pauses at 6 checkpoints) |
| `*apex-step {desc}` | Full pipeline, guided (pauses after each phase) |
| `*apex-quick {desc}` | Quick 3-phase pipeline (specify → implement → ship) |
| `*apex-fix {desc}` | Single-agent fix (scope-locked, snapshot-enabled) |
| `*apex-resume` | Resume paused/crashed pipeline |
| `*apex-status` | Current pipeline status |
| `*apex-abort` | Cancel pipeline |
| `*apex-pivot` | Change direction mid-pipeline |
| `*apex-rollback` | Rollback to previous checkpoint (code + state) |
| `*apex-dry-run {desc}` | Preview plan without executing |

### Vision Intelligence

| Command | What it does |
|---------|-------------|
| `*apex-vision` | Full visual sweep — print/URL → 14 agents → Apex Score → Navigator |
| `*apex-full` | Full code sweep — 13 discoveries → Code Score → Navigator |
| `*apex-vision-full` | Maximum power — visual + code combined |
| `*apex-score` | Quick score from last sweep (cached) |
| `*apex-analyze` | Quick visual analysis (1 screenshot, 8 dimensions) |
| `*apex-compare` | Side-by-side comparison (2 screenshots) |
| `*apex-consistency` | Cross-page consistency audit (3+ screenshots) |

### Web Intelligence (14 commands)

| Command | What it does |
|---------|-------------|
| `*scrape {url}` | Full design intelligence extraction (tokens, patterns, assets, system) |
| `*extract-tokens {url}` | Extract design tokens only (colors, typography, spacing, shadows) |
| `*analyze-patterns {url}` | Analyze component and layout patterns |
| `*asset-hunt {url\|query}` | Discover and curate visual assets (images, icons, 3D, stock) |
| `*compare {url}` | Compare external design system with current project |
| `*color-audit {url}` | Deep color palette extraction and analysis |
| `*type-audit {url}` | Typography scale analysis |
| `*responsive-scan {url}` | Multi-viewport extraction (breakpoints, fluid values) |
| `*motion-scan {url}` | Animation and transition extraction |
| `*asset-optimize {path}` | Optimize assets (WebP, AVIF, srcset generation) |
| `*asset-3d {query}` | Search and curate 3D assets |
| `*image-enhance {path}` | Enhance image quality and resolution |
| `*fuse {id}` | Merge extracted tokens with project (handoff to @design-sys-eng) |
| `*inspire {url\|query}` | Inspiration mode — browse, extract, present options |
| `*asset-pipeline {source}` | Brand asset pipeline (geometric recreation, enhance, compose) |
| `*logo {source}` | Alias for asset-pipeline geometric mode |
| `*icon-create {description}` | Create custom icon from description |
| `*icon-system {mode}` | Icon system management (audit, setup, create, migrate) |

### Discovery (13 tools)

| Command | What it maps |
|---------|-------------|
| `*discover-components` | Components, deps, orphans, tests, health score |
| `*discover-design` | Tokens, violations, palette, DS score |
| `*discover-routes` | Routes, orphans, dead routes, SEO gaps |
| `*discover-dependencies` | Outdated, vulnerable, heavy, unused |
| `*discover-motion` | Animations, CSS→spring violations, reduced-motion |
| `*discover-a11y` | WCAG violations, keyboard traps, labels, contrast |
| `*discover-performance` | Lazy loading, images, re-renders, CWV risks |
| `*discover-state` | Context sprawl, prop drilling, re-render risks |
| `*discover-types` | TypeScript coverage: any, unsafe casts, untyped props |
| `*discover-forms` | Validation gaps, error states, double submit |
| `*discover-security` | XSS vectors, exposed secrets, insecure storage |
| `*discover-external-assets` | External asset health: broken links, licenses, optimization, orphans |
| `*discover-token-drift` | Token drift: adopted tokens vs extraction history, staleness, re-sync |

Each discovery produces a **health score 0-100** and suggests the next step.

### Quality & Audit

| Command | What it does |
|---------|-------------|
| `*apex-review` | Multi-agent code review |
| `*apex-dark-mode` | Dark mode audit |
| `*apex-critique` | Design critique (Gestalt, hierarchy) |
| `*apex-export-tokens {fmt}` | Export tokens (Figma, Style Dictionary, CSS, Tailwind) |
| `*apex-refactor {comp}` | Safe refactoring (5 phases with baseline tests) |
| `*apex-i18n-audit` | i18n audit (strings, RTL, overflow, pluralization) |
| `*apex-error-boundary` | Error boundary architecture audit (4 layers) |
| `*apex-gate-status` | Quality gate protection levels |

### Style Presets

| Command | What it does |
|---------|-------------|
| `*apex-inspire` | Browse 52 design presets catalog |
| `*apex-transform --style {id}` | Apply complete style with 1 command |
| `*apex-scan` | Scan project (stack, structure, conventions) |
| `*apex-suggest` | Proactive issue detection |

---

## Greenfield — Build from Scratch

Create entire frontend projects from a natural language description. No technical decisions required from the user.

```
*apex-greenfield "medical clinic website with home, services, and contact pages"
```

### 8 Phases

| Phase | What happens |
|-------|-------------|
| 0. Vision | User describes what they want in their own words |
| 1. Architecture | Stack + structure + design direction (smart defaults) |
| 2. Scaffold | Project created, dev server running |
| 3. Design System | Tokens, theme, typography |
| 4. Layout | Header (sticky by default), Footer, Container |
| 5. UI Components | Button, Card, Input, Modal with all states |
| 6. Pages | All pages with content, transitions, loading states |
| 7. Polish | Animations (spring), a11y (WCAG AA), performance |
| 8. Review | Everything passing, ready to use |

### Smart Defaults

The user never needs to choose technologies. Apex decides based on best practices:

| Decision | Default |
|----------|---------|
| Framework | React 19 + Vite |
| Styling | Tailwind CSS 4 |
| Animation | Framer Motion (spring physics) |
| Icons | Lucide |
| Router | React Router v7 |
| Language | TypeScript (always) |
| Testing | Vitest |

---

## Web Intelligence (@web-intel)

**Kilian** (DNA: Kilian Valkhof, Creator of Polypane & Superposition) — the squad's eyes on the external web. Extracts design intelligence from any URL, curates assets, compares design systems, and fuses findings into the project.

### What It Does

| Capability | Description |
|------------|-------------|
| **Design Extraction** | Scrape tokens (colors, typography, spacing, shadows) from any live URL |
| **Pattern Analysis** | Detect component patterns, layout grids, breakpoints from external sites |
| **Asset Curation** | Hunt images, icons, 3D assets from stock/free sources |
| **Design Comparison** | Compare external design system vs project — token-by-token diff |
| **Token Fusion** | Merge extracted tokens into project via handoff to @design-sys-eng |
| **Inspiration Mode** | Browse, extract, present options from curated URLs |

### Lifecycle

```
*scrape {url}          → Extract everything (tokens, patterns, assets)
*extract-tokens {url}  → Tokens only
*compare {url}         → Diff with project
*fuse {id}             → Merge into project (→ @design-sys-eng)
*discover-token-drift  → Are adopted tokens still in sync?
*discover-external-assets → Are external assets healthy?
```

### Agent Chains with Web Intel

| Flow | Sequence |
|------|----------|
| Full extraction | Kilian → Diana (fuse tokens) → Josh (implement CSS) |
| Asset pipeline | Kilian (hunt) → Addy (optimize) → Paul (3D if needed) |
| Competitive analysis | Kilian (compare) → Diana (token mapping) → Andy (visual QA) |
| Inspiration | Kilian (inspire) → Ahmad (interaction patterns) → Diana (tokens) |

---

## Intent Clarification — Vocabulary Bridge

> **The user never needs to know CSS, React, or any technical term.** Apex automatically translates natural language to technical implementation and **confirms before executing**.

### How It Works

```
User: "remove the header background and keep it fixed"

Emil:
  Here's what I understood:
  → The header background becomes transparent (no solid color)
  → The header remains visible at all times while scrolling
  → Icons and logo stay in place

  Correct? (yes / adjust)

User: "yes"
Emil: [executes exactly that, nothing more]
```

### Supported Vocabulary (50+ patterns)

| User says | Apex understands |
|-----------|-----------------|
| "keep it fixed", "always visible", "sticky" | Element stays visible during scroll |
| "transparent", "no background" | Background removed |
| "glass", "frosted", "blur effect" | Glass morphism effect |
| "glow", "neon", "luminous" | Luminous effect |
| "more space", "breathing room" | Increase spacing |
| "side by side", "horizontal" | Horizontal layout |
| "on mobile", "responsive" | Responsive |
| "slide in", "slide animation" | Slide animation |
| "scrape this site", "extract from" | Scrape design intelligence from URL |
| "make it look like", "similar to" | Compare + inspire from URL |
| "find images", "stock photos for" | Asset hunt |
| "compare with", "check this site" | Design comparison |

Full mapping in `data/vocabulary-bridge.yaml` (expandable).

---

## Scope Lock & Rollback

### Scope Lock Protocol

Before ANY modification, the agent declares exactly what it will touch and locks the scope:

```
Scope Lock:
  Files: Header.tsx (ONLY)
  Modifications: background-color, position (ONLY)
  Do not touch: layout, icons, logo, other components
```

**Veto:** Any change outside the declared scope is BLOCKED.

### Snapshot & Rollback

A `git stash` snapshot is created automatically before any modification begins. Instant recovery if needed:

```
User: "rollback"
Emil: [git stash pop — instantly restores previous state]
```

### Request Adherence Gate

After every fix, Apex validates that changes match the original request:

```
Adherence Check:
  Request: "remove the header background"       ✅ MATCH
  Modified: Header.tsx (background-color)        ✅ IN SCOPE
  Out of scope: none                             ✅ CLEAN
```

---

## Discovery Tools (13)

13 discovery tools scan the real codebase BEFORE any action. The squad never guesses — it diagnoses.

| Tool | Scans | Health Score |
|------|-------|-------------|
| `*discover-components` | Component map, dependency tree, orphans, god components | 0-100 |
| `*discover-design` | Token inventory, violations, near-duplicates, design language | 0-100 |
| `*discover-routes` | Route map, orphans, dead routes, SEO gaps | 0-100 |
| `*discover-dependencies` | Outdated, vulnerable, heavy, unused packages | 0-100 |
| `*discover-motion` | Animation map, CSS→spring violations, reduced-motion gaps | 0-100 |
| `*discover-a11y` | Missing alt/labels, contrast, keyboard traps, ARIA misuse | 0-100 |
| `*discover-performance` | Lazy loading gaps, image audit, CWV risks, bundle risks | 0-100 |
| `*discover-state` | Context sprawl, prop drilling, missing memoization | 0-100 |
| `*discover-types` | `any` usage, unsafe casts, untyped props | 0-100 |
| `*discover-forms` | Validation gaps, double submit, form a11y | 0-100 |
| `*discover-security` | XSS vectors, exposed secrets, insecure storage | 0-100 |
| `*discover-external-assets` | Broken links, licenses, optimization gaps, orphan assets | 0-100 |
| `*discover-token-drift` | Adopted tokens vs extraction history, staleness, fusion health | 0-100 |

The last 2 discoveries close the **@web-intel lifecycle**: bring external assets in → use them → audit their health over time.

---

## Vision Intelligence

### Input Types

| Input | What happens |
|-------|-------------|
| **Screenshot** | Structure detection → 14 agents sweep → Apex Score |
| **URL** | Navigate → capture 3 viewports → full sweep |
| **Screenshot + URL** | Cross-reference: drift detection between print and live |
| **2+ screenshots** | Multi-page consistency audit |

### Navigator

Interactive drill-down with 4 depth levels:

```
Level 0: Overview     ← Apex Score + breakdown
Level 1: Domain       ← "a11y" → domain score + findings
Level 2: Section      ← "hero" → findings in hero section
Level 3: Finding      ← "1" → detail + fix
```

Navigate with numbers or natural language: `"improve the hero"`, `"fix contrast"`, `"show mobile"`.

---

## Style Presets (31)

```
@apex "apply Apple liquid glass style"
```

| Category | Presets | Examples |
|----------|---------|----------|
| **Apple** | 3 | Liquid Glass, HIG Classic, visionOS Spatial |
| **Google** | 2 | Material 3, Material You |
| **Tech Companies** | 7 | Linear, Vercel, Stripe, Notion, GitHub, Spotify, Discord |
| **Design Movements** | 7 | Glassmorphism, Neumorphism, Brutalist, Minimalist, Y2K, Claymorphism, Aurora |
| **Industry** | 5 | Healthcare, Fintech, SaaS, E-commerce, Education |
| **Dark Themes** | 3 | Dark Elegant, OLED Black, Nord |
| **Experimental** | 4 | Neubrutalism, Cyberpunk, Organic, Swiss Grid |
| **Luxury & Haute** | 3 | Maison (Montblanc/Hermes), Atelier (Chanel/Dior), Artisan (Aesop) |
| **Premium Tech** | 2 | Audio (B&O/Bose), Optics (Leica/Hasselblad) |
| **Automotive Premium** | 2 | Electric (Tesla/Rivian), Heritage (Porsche/BMW) |
| **Healthcare Premium** | 2 | Clinical (Mayo Clinic), Wellness (Calm/Headspace) |
| **Digital Marketing** | 2 | SaaS (HubSpot/Webflow), Creative (Mailchimp/Figma) |
| **Food & Hospitality** | 2 | Fine Dining (Alinea/EMP), Modern Cafe (Blue Bottle) |
| **Resort & Travel** | 2 | Luxury (Aman Resorts), Boutique (Aman/Amanpuri) |
| **Big Tech Giants** | 6 | Microsoft Fluent, Meta/Instagram, Netflix, Airbnb, Uber, OpenAI |

Each preset defines complete tokens: colors, typography, spacing, radius, shadows, motion.

---

## Intelligence Layer

### Intent Chaining — "What's next?"

After EVERY operation, Apex suggests the next logical action:

```
🎭 Josh — done. 1 file modified. Typecheck PASS.

1. Run suggestions on the modified file
2. Verify a11y with Sara
3. Done

What's next?
```

50 conditional intent chains cover all scenarios (with loop guards and `max_iterations` on recursive chains). Defined in `data/apex-intelligence.yaml`.

### Smart Defaults

| If the squad already knows... | It won't ask |
|-------------------------------|-------------|
| Only 1 component in scope | "Which component?" |
| Scope is 1 file | "Full pipeline or quick?" |
| Domain maps to 1 agent | "Which agent?" |
| Creating a header | Position: sticky (default) |
| Healthcare project | Prioritize accessibility |

### Context Memory (10 persistent caches)

Scan results, discovery data, and user preferences are cached so the squad doesn't repeat work.

---

## Implicit Heuristics (8)

Codified expert instincts — knowledge that agents "just know" but was never formally documented. Defined in `data/implicit-heuristics.yaml`.

| ID | Heuristic | Agents | Severity |
|----|-----------|--------|----------|
| IH-001 | URL wins over screenshot — URL is source of truth, print is intent reference | apex-lead, web-intel | HIGH |
| IH-002 | Fix what breaks before what irritates — functional > UX > visual > polish | apex-lead, css-eng | HIGH |
| IH-003 | Unused token is dead token — 0 references = suggest removal | design-sys-eng, web-intel | MEDIUM |
| IH-004 | Spring config scales with element size — modal ≠ button ≠ tooltip | motion-eng | HIGH |
| IH-005 | Under construction site = ABORT extraction — don't scrape placeholders | web-intel | CRITICAL |
| IH-006 | Dark mode is not color inversion — redesign surface hierarchy | design-sys-eng, css-eng | HIGH |
| IH-007 | Custom breakpoints need custom viewports — 3 viewports are minimum, not maximum | web-intel | MEDIUM |
| IH-008 | Accessibility is design, not QA — starts in Phase 1, not Phase 7 | interaction-dsgn, a11y-eng | CRITICAL |

---

## Agent Blind Spots

Every agent has domains where their expertise creates bias. The orchestrator uses these to know when to seek a second opinion. Defined in `data/agent-blind-spots.yaml`.

| Agent | Blind Spot | Mitigation |
|-------|-----------|------------|
| Emil (apex-lead) | Backend latency vs frontend timing | Check network tab before adjusting animation timing |
| Arch (frontend-arch) | Mobile-first constraints as afterthought | Require mobile viewport check in architecture review |
| Ahmad (interaction-dsgn) | Technical implementation cost | Validate feasibility with @react-eng before finalizing |
| Diana (design-sys-eng) | Over-systematization of one-offs | Allow documented exceptions for intentional custom values |
| Josh (css-eng) | Prefers pure CSS over simpler JS solutions | Consider JS alternative when CSS exceeds 30 lines |
| Kent (react-eng) | Visual design fidelity (2px misalignment) | Pair with @qa-visual for pixel-level review |
| Matt (motion-eng) | Over-animation — everything wants to animate | Apply motion only when it communicates intent |
| Sara (a11y-eng) | Maximum contrast at expense of design cohesion | Meet WCAG AA, not necessarily AAA |
| Addy (perf-eng) | Premature optimization | Always measure BEFORE optimizing |
| Kilian (web-intel) | Context behind design decisions (WHAT not WHY) | Validate extracted tokens against project brand before fusing |

Full blind spots for all 15 agents in `data/agent-blind-spots.yaml`.

---

## Quality Gates

### 10 Blocking Gates

| Gate | Owner | Phase |
|------|-------|-------|
| QG-AX-001 Token Compliance | @design-sys-eng | Design |
| QG-AX-002 Spec Completeness | @interaction-dsgn | Design |
| QG-AX-003 Architecture | @frontend-arch | Build |
| QG-AX-004 Behavior & States | @react-eng | Build |
| QG-AX-005 Motion & Reduced-Motion | @motion-eng | Build |
| QG-AX-006 A11y (WCAG AA) | @a11y-eng | Build |
| QG-AX-007 Performance Budgets | @perf-eng | Build |
| QG-AX-008 Visual Regression | @qa-visual | Ship |
| QG-AX-009 Cross-Platform | @qa-xplatform | Ship |
| QG-AX-010 Final Review | @apex-lead | Ship (NON-WAIVABLE) |

### 154 Veto Conditions

Physical blocks, not suggestions. Every condition has:
- `available_check` — verify tooling exists before checking
- `on_unavailable` — SKIP with warning (graceful degradation)
- Measurable criteria (grep, test, exit code)
- Specific thresholds where applicable (fps targets, HSL distance, exception rules)

**Adaptive enforcement:** If a tool doesn't exist in the project (Chromatic, Storybook, Playwright), the veto SKIPs with a warning instead of blocking.

---

## Pipeline (7 Phases)

```
Specify → Design → Architect → Implement → Polish → QA → Ship
  CP-01    CP-02    CP-03                   CP-05        CP-04/06
```

- **6 user checkpoints** — creative decisions are never automated
- **10 quality gates** — real blockers, not suggestions
- **State persistence** — pipeline can pause, crash, and resume
- **2 modes:** autonomous (`*apex-go`) or guided (`*apex-step`)
- **Snapshot before changes** — instant rollback capability

---

## Agent Handoff Matrix

Formal inter-agent delegation protocols. Every handoff has explicit rules — no informal "coordinate with @agent" references.

**18 handoff protocols** covering all 15 agents with:
- **Trigger** — when the handoff activates
- **Artifact** — structured data passed between agents (required fields)
- **Conflict resolution** — who arbitrates when agents disagree
- **Precedence** — accessibility > brand fidelity, performance budgets are final

### Key Protocols

| From → To | Trigger | Arbiter |
|-----------|---------|---------|
| Diana → Josh | Token definitions ready for CSS | apex-lead (Diana owns naming, Josh owns implementation) |
| Diana → Sara | Color tokens need contrast validation | apex-lead (Sara's contrast is NON-NEGOTIABLE) |
| Ahmad → Matt | Interaction needs motion design | apex-lead (Ahmad specifies FEEL, Matt owns MECHANISM) |
| Kent → Sara | Interactive elements need a11y review | Sara (a11y requirements NON-NEGOTIABLE) |
| Matt → Addy | Complex animation needs perf validation | Addy (performance budget is final) |
| Kilian → Diana | Extracted tokens ready for integration | Diana (extracted tokens are SUGGESTIONS, not mandates) |
| apex → Aria | New feature needs architecture decision | Aria (owns architecture decisions) |
| Kilian → Paul | 3D assets need spatial preparation | Paul (owns 3D technical decisions) |
| apex → devops | Feature complete, all gates passed | apex-lead (final ship/no-ship decision) |

### Arbitration Hierarchy

1. **Accessibility** (a11y-eng) — NON-NEGOTIABLE, always wins
2. **Performance** (perf-eng) — budgets are final
3. **Architecture** (frontend-arch) — owns system-level decisions
4. **Token naming** (design-sys-eng) — owns token API
5. **CSS implementation** (css-eng) — owns HOW CSS is written
6. **Motion physics** (motion-eng) — owns spring configs
7. **Default arbiter** — apex-lead

Full protocols in `data/agent-handoff-matrix.yaml`.

---

## Heuristic Source Map

Centralized `[SOURCE:]` attribution for all 101 agent heuristics across 15 agents. Every heuristic is traceable to its origin.

### Source Tier Breakdown

| Tier | Count | Description |
|------|-------|-------------|
| **OURO** | 93 | Directly attributable to DNA source (blog posts, talks, open-source code) |
| **MIXED** | 1 | Partially attributable, partially inferred |
| **INFERRED** | 7 | Industry best practices, not directly from DNA source |

### What It Tracks

- `agent_id` — which agent owns the heuristic
- `heuristic_id` — unique identifier (e.g., AX001, RT001)
- `source` — `[SOURCE: url/talk/repo]` or `[INFERRED]`
- `tier` — OURO / MIXED / INFERRED

Full map in `data/heuristic-source-map.yaml`.

---

## Workflow Rollback Protocol

All 7 workflows include a standardized 6-step rollback protocol for recovery from any phase failure.

### 6 Recovery Steps

| Step | Action | Description |
|------|--------|-------------|
| 1 | SNAPSHOT | `git stash` before phase begins |
| 2 | IDENTIFY | Detect which phase failed and the cause |
| 3 | REVERT | `git stash pop` to restore pre-phase state |
| 4 | VERIFY | Confirm codebase matches pre-phase state |
| 5 | REPORT | Document failure cause + rollback action |
| 6 | RETRY/ESCALATE | Retry phase or escalate to apex-lead |

### Per-Phase Scope

Each workflow defines rollback scope per phase:
- **Design phases** — rollback design artifacts only
- **Implementation phases** — rollback code changes via git
- **QA phases** — rollback test configurations
- **Ship phases** — rollback deployment artifacts

### Safeguards

- **User approval** required before rollback execution
- **Escalation** to apex-lead if retry fails twice
- **Audit trail** — every rollback is logged with cause and outcome

Workflows with rollback: `wf-component-create`, `wf-component-refactor`, `wf-cross-platform-sync`, `wf-feature-build`, `wf-polish-cycle`, `wf-ship-validation`, `apex-vision-workflow`.

---

## Design Philosophy

### 1. Feel > Look
An interface that FEELS right is worth more than one that LOOKS right.

### 2. Spring > Ease
`transition: all 0.2s ease` is **prohibited** for interactive elements. Springs have mass, stiffness, damping — they model real physics.

| Preset | Stiffness | Damping | Mass | Use |
|--------|-----------|---------|------|-----|
| `gentle` | 120 | 14 | 1 | Modals, drawers, page transitions |
| `responsive` | 300 | 20 | 1 | Buttons, toggles, accordions |
| `snappy` | 500 | 25 | 0.8 | Micro-interactions, feedback |
| `bouncy` | 200 | 10 | 1 | Celebrations, success states |

> CSS transitions are allowed only for non-interactive decorative elements (opacity, color fades < 100ms).

### 3. Tokens Are Law
No hardcoded values. Every color, spacing, shadow, and radius lives in the design token system.

### 4. Accessibility Is Not Optional
WCAG 2.2 AA minimum. axe-core: 0 violations. Touch targets: 44x44px minimum.

### 5. Header Is Sticky by Default
Headers use `position: sticky` unless explicitly requested otherwise.

---

## Performance Standards

### Web

| Metric | Target |
|--------|--------|
| LCP | < 1.2s |
| INP | < 200ms |
| CLS | < 0.1 |
| First Load JS | < 80KB gzipped |
| Animation FPS | >= 60fps |

### Mobile

| Metric | Target |
|--------|--------|
| Cold startup | < 1s |
| UI/JS thread FPS | >= 60fps |
| ANR rate | 0% |

---

## Project Structure

```
squads/apex/
├── agents/              # 15 agent definitions + lazy-load modules
│   └── modules/         # 5 lazy-loaded modules (voice, thinking, examples, platforms, guide)
├── tasks/               # 161 active tasks
│   └── extensions/      # Platform-specific tasks (RN, 3D, cross-platform)
├── workflows/           # 9 multi-phase workflows
├── checklists/          # 37 quality checklists
├── templates/           # 16 document templates
├── data/                # 29 data files (intelligence, veto, presets, heuristics, handoff matrix, source map)
├── scripts/             # 1 utility script (greeting generator)
├── config/              # Squad configuration
├── squad.yaml           # Manifest
├── CLAUDE.md            # Project integration (856 lines)
├── CHANGELOG.md         # Version history
└── README.md            # This file
```

### Key Data Files

| File | Purpose |
|------|---------|
| `apex-intelligence.yaml` | Intent chaining, smart defaults, context memory |
| `veto-conditions.yaml` | 154 conditions across 37 gates |
| `implicit-heuristics.yaml` | 8 codified expert heuristics |
| `agent-blind-spots.yaml` | Blind spots for all 15 agents |
| `design-presets.yaml` | 31 base style presets |
| `design-presets-premium.yaml` | 15 premium presets (Luxury, Healthcare, Marketing, Resort) |
| `design-presets-bigtech.yaml` | 6 Big Tech presets (Microsoft, Meta, Netflix, Airbnb, Uber, OpenAI) |
| `vocabulary-bridge.yaml` | Natural language → technical translation |
| `health-score-formulas.yaml` | Scoring formulas for all 13 discoveries |
| `scan-score-suggest-framework.yaml` | 3-phase discovery pattern |
| `spring-configs.yaml` | Spring animation presets |
| `agent-handoff-matrix.yaml` | 18 formal handoff protocols with conflict resolution and arbitration |
| `heuristic-source-map.yaml` | Centralized source attribution for all 101 agent heuristics |

---

## Git Authority

Apex agents **can:** `git add`, `git commit`, `git status`, `git diff`, edit files, run tests.

Apex agents **cannot:** `git push`, `gh pr create`, manage CI/CD — delegate to `@devops`.

---

## Usage Examples

```
@apex "the header breaks on mobile viewports"      → *apex-fix → Josh
@apex "add entrance animation to the card"         → *apex-fix → Matt
@apex "create a stats dashboard component"         → *apex-quick → Kent + Josh
@apex "redesign the services page"                 → *apex-go → full pipeline
@apex "medical clinic site with 3 pages"           → *apex-greenfield → 8 phases
@apex "remove header background, keep it fixed"    → vocabulary bridge → confirm → fix
@apex "how's the accessibility?"                   → *discover-a11y
@apex "apply Apple liquid glass style"             → *apex-transform
@apex "extract colors from linear.app"             → *scrape → Kilian
@apex "find premium images for healthcare"         → *asset-hunt → Kilian
@apex "compare our design with Stripe"             → *compare → Kilian → Diana
@apex "have the adopted tokens drifted?"           → *discover-token-drift
@apex "audit external asset health"                → *discover-external-assets
@apex [screenshot of the app]                      → *apex-vision → 14 agents sweep
@apex [screenshot of Stripe]                       → replicate/inspire/compare
```

---

<p align="center">
  <strong>Apex Squad v1.7.0</strong><br>
  <em>"Every pixel is a decision." — Emil ⚡</em>
</p>
