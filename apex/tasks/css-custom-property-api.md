> **DEPRECATED** — Scope absorbed into `css-architecture-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: css-custom-property-api

```yaml
id: css-custom-property-api
version: "1.0.0"
title: "CSS Custom Property API Design"
description: >
  Designs a CSS Custom Property API for the design system. Defines
  property naming conventions, creates typed properties with @property,
  builds theming primitives, implements component-scoped tokens,
  and documents the complete custom property architecture. Transforms
  CSS variables from ad-hoc values into a typed, documented, discoverable
  API surface.
elicit: false
owner: css-eng
executor: css-eng
outputs:
  - Custom property naming convention
  - @property type registration
  - Theme switching architecture (light/dark/custom)
  - Component-scoped token patterns
  - Custom property API reference document
  - Property API specification
```

---

## When This Task Runs

This task runs when:
- Design system needs structured CSS variable architecture
- Custom properties are scattered without naming convention
- Theme switching (dark mode, brand themes) needs implementation
- Component-level tokens needed (e.g., button-specific colors)
- Animations need typed custom properties (for `@property` transitions)
- `*css-api` or `*custom-props` is invoked

This task does NOT run when:
- Tailwind config handles all token needs (no raw CSS vars needed)
- The task is about JavaScript-driven theming (CSS-in-JS)
- Token architecture design (use `token-architecture`)

---

## Execution Steps

### Step 1: Define Naming Convention

Establish a consistent naming system for all custom properties.

**Naming pattern:** `--{scope}-{category}-{variant}-{state}`

```css
/* Global tokens (design system level) */
--color-primary-500: #3b82f6;
--color-neutral-100: #f1f5f9;
--spacing-4: 16px;
--radius-md: 8px;
--font-sans: 'Inter', system-ui;
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

/* Semantic tokens (intent-based, theme-dependent) */
--color-surface: var(--color-neutral-100);
--color-content: var(--color-neutral-900);
--color-accent: var(--color-primary-500);
--color-border: var(--color-neutral-200);
--color-error: var(--color-red-500);
--color-success: var(--color-green-500);

/* Component tokens (component-scoped) */
--btn-bg: var(--color-accent);
--btn-text: var(--color-white);
--btn-radius: var(--radius-md);
--btn-padding-x: var(--spacing-4);
--btn-padding-y: var(--spacing-2);

/* State tokens (interaction states) */
--btn-bg-hover: var(--color-primary-600);
--btn-bg-active: var(--color-primary-700);
--btn-bg-disabled: var(--color-neutral-200);
```

**Naming rules:**
| Prefix | Scope | Example |
|--------|-------|---------|
| `--color-*` | Global color palette | `--color-primary-500` |
| `--spacing-*` | Global spacing scale | `--spacing-4` |
| `--radius-*` | Global border radius | `--radius-lg` |
| `--shadow-*` | Global shadows | `--shadow-md` |
| `--font-*` | Global typography | `--font-sans` |
| `--{component}-*` | Component-scoped | `--btn-bg`, `--card-padding` |
| `--*-hover/active/focus` | State variants | `--btn-bg-hover` |

**Output:** Complete naming convention reference.

### Step 2: Register Typed Properties with @property

Use CSS `@property` for type safety, inheritance control, and animation.

```css
/* @property enables CSS to know the TYPE of a custom property */

@property --color-accent {
  syntax: '<color>';
  inherits: true;
  initial-value: #3b82f6;
}

@property --progress {
  syntax: '<percentage>';
  inherits: false;
  initial-value: 0%;
}

@property --angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

@property --card-opacity {
  syntax: '<number>';
  inherits: false;
  initial-value: 1;
}
```

**Why @property matters:**

| Without @property | With @property |
|-------------------|---------------|
| `transition` on custom property: doesn't animate | Animates smoothly between values |
| No type validation | Browser validates type |
| Inherits by default (sometimes unwanted) | Control inheritance explicitly |
| No initial value guarantee | Always has defined initial value |

**Animation with @property:**
```css
@property --gradient-angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.gradient-animated {
  background: linear-gradient(var(--gradient-angle), #3b82f6, #8b5cf6);
  transition: --gradient-angle 0.3s ease;
}
.gradient-animated:hover {
  --gradient-angle: 180deg; /* Smoothly animates! */
}
```

**Output:** @property registrations for all animatable tokens.

### Step 3: Build Theme Switching Architecture

Design the theme system using custom property layers.

**Three-layer token architecture:**
```css
/* Layer 1: Primitive tokens (never change) */
:root {
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --slate-50: #f8fafc;
  --slate-900: #0f172a;
}

/* Layer 2: Semantic tokens (change per theme) */
:root, [data-theme="light"] {
  --color-surface: var(--slate-50);
  --color-content: var(--slate-900);
  --color-accent: var(--blue-500);
}

[data-theme="dark"] {
  --color-surface: var(--slate-900);
  --color-content: var(--slate-50);
  --color-accent: var(--blue-400);
}

/* Layer 3: Component tokens (reference semantic tokens) */
.btn-primary {
  background: var(--color-accent);
  color: var(--color-surface);
}
/* Button works in BOTH themes without modification */
```

**System preference detection:**
```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    /* Apply dark theme when no explicit theme set */
    --color-surface: var(--slate-900);
    --color-content: var(--slate-50);
  }
}
```

**Brand theming (multiple brands):**
```css
[data-brand="clinic-a"] {
  --color-accent: #10b981; /* Emerald */
  --color-accent-hover: #059669;
}

[data-brand="clinic-b"] {
  --color-accent: #8b5cf6; /* Violet */
  --color-accent-hover: #7c3aed;
}
```

**Output:** Theme switching architecture with light/dark/brand support.

### Step 4: Implement Component-Scoped Tokens

Design component-level custom properties for encapsulated styling.

```css
/* Component defines its own API surface */
.card {
  /* Component tokens with smart defaults */
  --card-padding: var(--spacing-4);
  --card-radius: var(--radius-md);
  --card-bg: var(--color-surface);
  --card-border: var(--color-border);
  --card-shadow: var(--shadow-md);

  padding: var(--card-padding);
  border-radius: var(--card-radius);
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  box-shadow: var(--card-shadow);
}

/* Consumers override via custom properties, not classes */
.card--compact {
  --card-padding: var(--spacing-2);
  --card-radius: var(--radius-sm);
  --card-shadow: none;
}

.card--featured {
  --card-bg: var(--color-accent);
  --card-border: transparent;
}
```

**Component API benefits:**
- Consumer overrides only the property, not the entire rule
- Internal implementation can change without breaking consumers
- Components are self-documenting (list of `--component-*` vars)
- Composition: parent sets child's tokens without specificity fights

**Output:** Component-scoped token patterns with override examples.

### Step 5: Document Custom Property API

Compile the complete API reference.

**Documentation includes:**
- Naming convention reference (from Step 1)
- @property registrations catalog (from Step 2)
- Theme switching guide (from Step 3)
- Component token patterns (from Step 4)
- Quick reference: all available custom properties
- Migration guide: hardcoded values → custom properties
- DevTools debugging tips

**Output:** Complete custom property API specification.

---

## Quality Criteria

- All custom properties must follow the naming convention
- @property must be registered for all animatable properties
- Theme switching must work without JavaScript (CSS-only)
- Component tokens must have smart defaults (work without explicit override)
- No hardcoded color/spacing values in component CSS

---

*Squad Apex — CSS Custom Property API Design Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-css-custom-property-api
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All properties follow naming convention"
    - "@property registered for animatable properties"
    - "Theme switching works CSS-only"
    - "Component tokens have smart defaults"
    - "No hardcoded values in component CSS"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@design-sys-eng` or `@apex-lead` |
| Artifact | CSS Custom Property API with naming convention, @property registrations, theme architecture, and component patterns |
| Next action | Integrate with design system tokens via `@design-sys-eng` or audit adherence via `*discover-design` |
