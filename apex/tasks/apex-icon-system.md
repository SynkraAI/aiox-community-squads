# Task: apex-icon-system

```yaml
id: apex-icon-system
version: "1.0.0"
title: "Icon System Design & Management"
description: >
  Design, audit, and manage icon systems for frontend projects. Handles
  icon library selection, custom icon creation, icon component architecture,
  and consistency auditing. Supports Lucide, Heroicons, Phosphor, custom SVG,
  and hybrid approaches.
elicit: true
owner: design-sys-eng
executor: design-sys-eng
delegates_to: [css-eng, react-eng, a11y-eng, perf-eng]
inputs:
  - mode: "audit | setup | create | migrate"
outputs:
  - Icon system architecture document
  - Icon component (if create mode)
  - Audit report with recommendations (if audit mode)
veto_conditions:
  - "Icons without aria-label or aria-hidden → BLOCK"
  - "Inline SVG > 5KB without tree-shaking setup → PAUSE"
  - "Icon color not using currentColor → PAUSE"
  - "Mixed icon libraries without documented rationale → PAUSE"
  - "Icons below 24x24 touch target without padding wrapper → BLOCK"
```

---

## Command

### `*icon-system {mode}`

Design, audit, or manage the project's icon system.

**Aliases:** `*icons`, `*icon-audit`

---

## Execution Steps

### Step 1: Detect Current State

```yaml
detection:
  scan_for:
    - "Icon libraries in package.json (lucide-react, @heroicons/react, phosphor-react, etc.)"
    - "Custom SVG files in project (src/icons/, src/assets/icons/, public/icons/)"
    - "Inline SVG components in React files"
    - "Icon usage patterns (component import vs img src vs CSS background)"
    - "Icon sizing conventions (px, rem, em, Tailwind classes)"
    - "Color application method (currentColor, hardcoded, prop-based)"

  output:
    library_count: "Number of icon libraries detected"
    custom_count: "Number of custom SVG icons"
    usage_pattern: "component | img | css | mixed"
    consistency_score: "0-100 based on uniformity of approach"
```

### Step 2: Execute by Mode

#### Mode: AUDIT

```yaml
audit:
  checks:
    inventory:
      - "Total icons used across project"
      - "Icons per library (if multiple)"
      - "Custom vs library ratio"
      - "Unused icon imports (tree-shaking check)"

    consistency:
      - "Size uniformity (are all icons using same scale?)"
      - "Color approach (currentColor vs hardcoded)"
      - "Stroke width consistency"
      - "Corner radius consistency"
      - "Visual weight balance across icon set"

    accessibility:
      - "Decorative icons: have aria-hidden='true'"
      - "Meaningful icons: have aria-label or sr-only text"
      - "Interactive icons: wrapped in button with label"
      - "Touch targets: >= 44x44 with padding if needed"

    performance:
      - "Bundle impact of icon libraries"
      - "Tree-shaking effectiveness"
      - "SVG sprite vs individual imports"
      - "Icons loaded above the fold vs lazy"

  scoring:
    formula: "consistency(40%) + accessibility(30%) + performance(20%) + coverage(10%)"
    thresholds:
      excellent: ">= 85"
      good: "70-84"
      needs_work: "50-69"
      critical: "< 50"

  output: "Icon System Health Report with prioritized recommendations"
```

#### Mode: SETUP

```yaml
setup:
  elicitation: |
    Project scan complete. Let me help you set up an icon system.

    1. **Lucide** — 1500+ icons, MIT, tree-shakeable, React-first (recommended for most projects)
    2. **Heroicons** — 300+ icons, MIT, by Tailwind team, outline + solid
    3. **Phosphor** — 7000+ icons, MIT, 6 weights, highly consistent
    4. **Custom-only** — All icons are custom SVG (for brand-heavy projects)
    5. **Hybrid** — Library base + custom additions (most flexible)

    Which approach? (1-5)

  architecture:
    component_wrapper: |
      Create a unified Icon component that:
      - Accepts name, size, color, className, aria-label
      - Maps to the chosen library internally
      - Supports custom SVG override
      - Uses currentColor by default
      - Exports typed icon names for autocomplete

    file_structure: |
      src/components/ui/Icon/
      ├── Icon.tsx          # Unified component
      ├── Icon.types.ts     # TypeScript types
      ├── custom/           # Custom SVG icons
      │   ├── logo.svg
      │   └── brand-mark.svg
      └── index.ts          # Barrel export

    design_tokens: |
      icon.size.xs: 16px
      icon.size.sm: 20px
      icon.size.md: 24px (default)
      icon.size.lg: 32px
      icon.size.xl: 48px
      icon.stroke-width: 1.5 (default for outline)
      icon.color: currentColor
```

#### Mode: CREATE

```yaml
create:
  elicitation: |
    What icon do you need?
    1. Describe the concept (e.g., "medical cross with heartbeat line")
    2. Provide style reference (outline, filled, duotone)
    3. Specify size grid (16, 24, 32, or all)

  workflow:
    1. "Generate 3 geometric concepts using SVG primitives"
    2. "Present side-by-side with rationale"
    3. "User selects or refines"
    4. "Generate final SVG at all target sizes"
    5. "Create React component with currentColor"
    6. "Register in icon system (types, exports)"

  constraints:
    - "Use only geometric primitives (rect, circle, line, polyline, path)"
    - "Maximum 20 path nodes for simple icons, 50 for complex"
    - "Must look crisp at 16px (pixel-hinting)"
    - "Stroke-width must match existing icon library"
    - "Visual weight must be consistent with other project icons"

  output:
    - "icon-name.svg (optimized)"
    - "IconName.tsx (React component)"
    - "Updated type definitions"
```

#### Mode: MIGRATE

```yaml
migrate:
  purpose: "Switch icon library or consolidate mixed usage"

  steps:
    1. "Audit current usage (auto-runs audit mode)"
    2. "Map current icons to target library equivalents"
    3. "Identify unmapped icons (need custom creation)"
    4. "Generate migration plan with file list"
    5. "Execute migration (batch rename + import update)"
    6. "Verify: visual regression check on all pages"

  safety:
    - "NEVER delete original icons until migration verified"
    - "Create visual regression snapshots before migration"
    - "Migrate in batches of 10, verify each batch"
```

---

## Intent Chaining

```yaml
after_completion:
  audit_complete:
    - "Fix critical issues found"
    - "Setup icon system from scratch"
    - "Create custom icons for gaps"
    - "Done"
  setup_complete:
    - "Create first custom icon"
    - "Migrate from existing approach"
    - "Run audit to verify"
    - "Done"
  create_complete:
    - "Create another icon"
    - "Run audit on icon system"
    - "Export tokens"
    - "Done"
```
