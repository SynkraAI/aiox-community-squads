# Task: apex-greenfield

```yaml
id: apex-greenfield
version: "1.0.0"
title: "Apex Greenfield — Create Frontend Project from Scratch"
description: >
  Full workflow to create a complete frontend project from zero.
  From stack selection to deployed app with design system, components,
  pages, animations, and accessibility. Uses ALL squad agents in sequence.
  The user describes WHAT they want (in their own words), Apex builds everything.
elicit: true
owner: apex-lead
executor: apex-lead
dependencies:
  - tasks/apex-route-request.md
  - tasks/apex-fix.md
  - tasks/apex-pipeline-executor.md
  - data/vocabulary-bridge.yaml
  - data/veto-conditions.yaml
  - data/design-presets.yaml
  - data/context-dna-framework.yaml
outputs:
  - Complete frontend project with src/, components, pages, design system
  - Running dev server
  - All quality gates passing
```

---

## Command

### `*apex-greenfield {description}`

Create a complete frontend project from scratch. The user describes what they want in natural language — Apex handles all technical decisions.

**Aliases:** `*apex-new`, `*apex-create-project`, `*apex-init`

---

## When to Use

- Starting a brand new frontend project (no existing codebase)
- User wants a complete app built from their description
- Creating a new app within a monorepo
- Rebuilding an existing app from scratch with new stack

## When NOT to Use

- Adding features to existing project → `*apex-go` or `*apex-fix`
- Just scaffolding with no design/components → use `npm create vite` directly
- Backend-only project → delegate to `@dev`

---

## Execution Phases

### Phase 0: Vision Gathering (elicit: true)

**Emil gathers the project vision using non-technical language.**

```
⚡ Emil — Greenfield Mode

Vou construir seu projeto do zero. Me conta:

1. **O que e o projeto?**
   (Ex: "site de clinica medica", "dashboard de vendas", "app de tarefas")

2. **Quantas paginas/telas?**
   (Ex: "home, sobre, contato", "dashboard com graficos e lista")

3. **Tem algum estilo que gosta?**
   (Ex: "clean e moderno", "dark com neon", "estilo Apple", "minimalista")
   💡 Posso mostrar estilos: *apex-inspire

4. **Funcionalidades especiais?**
   (Ex: "formulario de contato", "login", "agenda", "chat")

5. **Tem referencia visual?**
   (Ex: link de site, print de app, ou "parecido com o Stripe")

Responde o que souber — o que nao souber eu defino com base nas melhores praticas.
```

**Rules:**
- NEVER ask technical questions (no "React or Vue?", no "Tailwind or CSS Modules?")
- ALL technical decisions are made by Apex based on best practices
- User can answer partially — Apex fills gaps with smart defaults
- If user provides a visual reference (print/URL), use it as the north star

**Smart Defaults (when user doesn't specify):**

| Decision | Default | Rationale |
|----------|---------|-----------|
| Framework | React + Vite | Fastest DX, no SSR overhead for most projects |
| Styling | Tailwind CSS 4 | Utility-first, fast iteration, responsive built-in |
| Animation | Framer Motion | Spring physics, reduced-motion, gesture support |
| Icons | Lucide | Consistent, tree-shakeable, large set |
| Routing | React Router v7 | Standard for Vite SPAs |
| State | React built-in (useState/useContext) | No external deps unless complex state needed |
| TypeScript | Yes, always | Type safety is non-negotiable |
| Testing | Vitest | Fast, Vite-native |
| Linting | ESLint + Prettier | Standard |

---

### Phase 1: Architecture (@frontend-arch or Emil)

**Define project structure, stack, and design system foundation.**

Based on Phase 0 answers, Emil defines:

```yaml
project_definition:
  name: "{project-name}"
  type: "{spa | landing | dashboard | portal}"
  stack:
    framework: "React 19 + Vite"
    styling: "Tailwind CSS 4"
    animation: "Framer Motion (motion)"
    icons: "Lucide"
    router: "React Router v7"
    language: "TypeScript"
  pages:
    - { path: "/", name: "Home", sections: [...] }
    - { path: "/about", name: "Sobre", sections: [...] }
  design_direction:
    preset: "{from design-presets.yaml or custom}"
    primary_color: "{hex}"
    font: "{font family}"
    style: "{glass | minimal | material | custom}"
    dark_mode: "{yes | no | auto}"
  components_needed:
    layout: [Header, Footer, Layout, Container]
    ui: [Button, Card, Input, Modal, ...]
    pages: [HomePage, AboutPage, ...]
```

**Present to user for confirmation:**
```
⚡ Seu projeto:

📁 {project-name}
⚛️ React 19 + Vite + TypeScript
🎨 Tailwind CSS 4, estilo {direction}
✨ Animacoes com Framer Motion
📄 {N} paginas: {list}
🧩 {N} componentes: {list}

Cor principal: {color swatch description}
Fonte: {font name}
Tema: {light | dark | auto}

Vamos construir? (sim / ajustar)
```

**Veto:** `VC-GREEN-001` — Cannot proceed without user confirming project definition.

---

### Phase 2: Scaffold (@react-eng via Emil)

**Create the project structure and install dependencies.**

```bash
# 1. Create project
npm create vite@latest {name} -- --template react-ts

# 2. Install dependencies
cd {name}
npm install {dependencies based on stack}

# 3. Create directory structure
mkdir -p src/{components/{layout,ui,pages},hooks,lib,styles,assets}

# 4. Configure TypeScript, ESLint, Prettier
# 5. Configure Tailwind CSS
# 6. Configure path aliases (@/ → src/)
```

**Output:**
```
src/
├── components/
│   ├── layout/      # Header, Footer, Layout, Container
│   ├── ui/          # Button, Card, Input, Modal, etc.
│   └── pages/       # HomePage, AboutPage, etc.
├── hooks/           # Custom hooks
├── lib/             # Utilities, helpers
├── styles/          # Global styles, design tokens
├── assets/          # Images, fonts, icons
├── App.tsx          # Root component with router
├── main.tsx         # Entry point
└── index.css        # Design tokens, global styles
```

**Gate:** `QG-GREEN-SCAFFOLD`
- `npm run dev` starts without errors
- TypeScript compiles without errors
- Tailwind processes without errors

---

### Phase 3: Design System (@css-eng + @design-sys-eng via Emil)

**Create the design foundation — tokens, theme, typography.**

Based on the design direction from Phase 1:

```css
/* src/index.css — Design Tokens */
:root {
  /* Colors */
  --color-primary: {from preset or user choice};
  --color-primary-hover: {computed};
  --color-background: {from preset};
  --color-surface: {from preset};
  --color-text: {from preset};
  --color-text-muted: {computed};

  /* Typography */
  --font-sans: '{font}', system-ui, sans-serif;
  --font-heading: '{heading-font}', var(--font-sans);

  /* Spacing (4px grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... */

  /* Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.07);
  --shadow-lg: 0 10px 15px rgb(0 0 0 / 0.1);

  /* Motion */
  --spring-gentle: /* encoded spring config */;
  --spring-responsive: /* encoded spring config */;
  --spring-snappy: /* encoded spring config */;
}

/* Dark mode (if enabled) */
[data-theme="dark"] {
  --color-background: {dark variant};
  --color-surface: {dark variant};
  --color-text: {dark variant};
  /* ... */
}
```

**Gate:** `QG-GREEN-DESIGN`
- All colors use CSS variables (zero hardcoded hex)
- Typography scale follows 4px grid
- Dark mode tokens defined (if enabled)
- Contrast ratios meet WCAG AA (4.5:1 minimum)

---

### Phase 4: Layout Components (@css-eng + @react-eng via Emil)

**Build the structural components — the bones of every page.**

| Component | Purpose | Features |
|-----------|---------|----------|
| `Layout.tsx` | Page wrapper | Slot for header, content, footer |
| `Header.tsx` | Top navigation | Logo, nav links, CTA, sticky by default |
| `Footer.tsx` | Page footer | Links, copyright, contact |
| `Container.tsx` | Content width | max-width + padding, responsive |
| `Section.tsx` | Page section | Vertical padding, optional background |

**Rules:**
- Header is `position: sticky` by DEFAULT (user's feedback: "fixo" should be the standard)
- All layout components use design tokens (zero hardcoded values)
- Responsive from day 1 (mobile-first breakpoints)
- Semantic HTML (header, main, footer, section, nav)

**Gate:** `QG-GREEN-LAYOUT`
- Layout renders correctly at 320px, 768px, 1024px, 1440px
- Header stays visible on scroll (sticky)
- Semantic HTML validated
- Keyboard navigation works

---

### Phase 5: UI Components (@react-eng + @css-eng via Emil)

**Build the reusable UI components.**

| Component | States | A11y |
|-----------|--------|------|
| `Button.tsx` | default, hover, active, disabled, loading | aria-label, focus ring |
| `Card.tsx` | default, hover (if clickable) | role, keyboard |
| `Input.tsx` | default, focus, error, disabled | label, aria-describedby |
| `Modal.tsx` | open, closing | focus trap, ESC close, aria-modal |
| `Badge.tsx` | variants (success, warning, error, info) | aria-label |

**Additional components based on user's requirements** (forms, charts, lists, etc.)

**Rules:**
- Every component has: default, hover, active, disabled, loading, error states
- Every component uses design tokens
- Every interactive component has keyboard support
- Every component has TypeScript props interface

**Gate:** `QG-GREEN-COMPONENTS`
- All states implemented
- TypeScript strict (no `any`)
- A11y basics (labels, roles, keyboard)
- Design tokens used (zero hardcoded)

---

### Phase 6: Pages (@react-eng + @css-eng + @motion-eng via Emil)

**Build the actual pages using layout and UI components.**

For each page defined in Phase 1:
1. Create page component in `src/components/pages/`
2. Add route in `App.tsx`
3. Compose using Layout + Section + UI components
4. Add content (text, images, data)
5. Add page transitions (spring enter animation)
6. Add scroll animations (if appropriate)

**Rules:**
- Pages are COMPOSITION of components — minimal custom CSS
- Each page has a loading state (skeleton)
- Page transitions use spring physics (Motion)
- Scroll-triggered animations use IntersectionObserver + Motion
- SEO basics: title, meta description per page

**Gate:** `QG-GREEN-PAGES`
- All pages render without errors
- All routes accessible via navigation
- Page transitions smooth (spring)
- Loading states present
- Responsive at all breakpoints

---

### Phase 7: Polish (@motion-eng + @a11y-eng + @perf-eng via Emil)

**The layer that separates "works" from "feels right".**

1. **Motion pass** (@motion-eng)
   - Entrance animations for sections (staggered, scroll-triggered)
   - Hover effects on interactive elements
   - Page transitions between routes
   - Reduced-motion fallbacks for ALL animations

2. **Accessibility pass** (@a11y-eng)
   - Tab order and focus management
   - Screen reader compatibility
   - Color contrast validation
   - Touch target sizes (minimum 44x44)

3. **Performance pass** (@perf-eng)
   - Lazy loading for below-fold content
   - Image optimization (if any)
   - Bundle size check
   - Core Web Vitals baseline

**Gate:** `QG-GREEN-POLISH`
- All animations have reduced-motion fallback
- WCAG AA compliance
- LCP < 1.2s
- No layout shift (CLS < 0.1)

---

### Phase 8: Final Review & Ship (Emil)

**Emil does final visual review across all pages and breakpoints.**

```
⚡ Projeto finalizado!

📁 {project-name}
📄 {N} paginas criadas
🧩 {N} componentes criados
🎨 Design system: {N} tokens definidos
✨ {N} animacoes com spring physics
♿ WCAG AA compliant
🚀 Performance: LCP {value}

Checks:
  TypeScript: PASS
  Lint: PASS
  A11y: PASS
  Responsive: PASS (320px → 1440px)

Dev server: npm run dev → http://localhost:5173

Proximo passo:
1. Testar no browser (npm run dev)
2. Ajustar algo (*apex-fix)
3. Deploy (*apex-ship → @devops)
4. Done

— Emil, crafting pixel by pixel ⚡
```

---

## Full Quality Gate Sequence

| Phase | Gate | Blocks |
|-------|------|--------|
| 0 | VC-GREEN-001 (user confirms vision) | Phase 1 |
| 2 | QG-GREEN-SCAFFOLD (dev server runs) | Phase 3 |
| 3 | QG-GREEN-DESIGN (tokens, contrast) | Phase 4 |
| 4 | QG-GREEN-LAYOUT (responsive, semantic) | Phase 5 |
| 5 | QG-GREEN-COMPONENTS (states, a11y, types) | Phase 6 |
| 6 | QG-GREEN-PAGES (routes, transitions) | Phase 7 |
| 7 | QG-GREEN-POLISH (motion, a11y, perf) | Phase 8 |
| 8 | QG-AX-010 (final review) | Ship |

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-GREEN-001
    condition: "Greenfield proceeds without user confirming project definition"
    action: "VETO — Must get user 'sim' on project definition before scaffolding"
    blocking: true

  - id: VC-GREEN-002
    condition: "Technical questions asked to non-technical user"
    action: "VETO — Make the technical decision yourself, present in visual language"
    blocking: true

  - id: VC-GREEN-003
    condition: "Hardcoded values in any component (color, spacing, font-size)"
    action: "VETO — All values must reference design tokens"
    blocking: true

  - id: VC-GREEN-004
    condition: "Component without all states (default, hover, active, disabled, loading, error)"
    action: "WARN — Add missing states before Phase 7"
    blocking: false

  - id: VC-GREEN-005
    condition: "Page without loading state/skeleton"
    action: "WARN — Add skeleton before Phase 7"
    blocking: false

  - id: VC-GREEN-006
    condition: "Animation without prefers-reduced-motion fallback"
    action: "VETO — Every animation needs a fallback"
    blocking: true

  - id: VC-GREEN-007
    condition: "Header not sticky by default"
    action: "WARN — Headers should be sticky unless user explicitly says otherwise"
    blocking: false
```

---

## Examples

**Example 1 — Simple landing page:**
```
User: *apex-greenfield "site pra minha clinica medica, com home, servicos e contato"

Emil: [Phase 0 — gathers: 3 pages, medical, clean style]
      [Phase 1 — defines: React+Vite, Tailwind, healthcare preset, sky-500 primary]
      [Presents definition, user confirms]
      [Phase 2-8 — builds everything]
      → Complete site with 3 pages, design system, animations, responsive
```

**Example 2 — Dashboard:**
```
User: *apex-greenfield "dashboard pra gerenciar tarefas da equipe, estilo dark com cards"

Emil: [Phase 0 — gathers: dashboard, task management, dark theme, card-based]
      [Phase 1 — defines: React+Vite, Tailwind, dark-elegant preset, data table + cards]
      [Presents definition, user confirms]
      [Phase 2-8 — builds everything]
      → Complete dashboard with sidebar, task cards, filters, dark theme
```

**Example 3 — With visual reference:**
```
User: *apex-greenfield "quero um site parecido com esse" [sends print of Stripe.com]

Emil: [Phase 0 — analyzes print: clean, gradient hero, card sections, light theme]
      [Phase 1 — defines: stripe-style preset, Inter font, gradient primary]
      [Presents definition, user confirms]
      [Phase 2-8 — builds everything]
      → Site inspired by Stripe's design language
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | User (complete project running locally) |
| Next action | User tests, requests fixes, or ships |
| External | @devops for deployment when ready |

---

*Apex Squad — Greenfield Task v1.0.0 — Build complete frontend projects from scratch*
