> **DEPRECATED** — Scope absorbed into `accessibility-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: color-contrast-automation

```yaml
id: color-contrast-automation
version: "1.0.0"
title: "Color Contrast Automation"
description: >
  Automates WCAG color contrast validation across the entire codebase.
  Extracts foreground/background color pairs from CSS/Tailwind, computes
  contrast ratios per WCAG 2.2 (AA: 4.5:1 normal, 3:1 large; AAA: 7:1),
  flags violations, suggests nearest compliant alternatives, and generates
  a contrast compliance report. Handles opacity, gradients, and dark mode.
elicit: false
owner: a11y-eng
executor: a11y-eng
outputs:
  - Color pair inventory (fg/bg per component)
  - Contrast ratio report (pass/fail per pair)
  - Violation list with suggested fixes
  - Dark mode contrast delta report
  - Gradient/opacity edge case analysis
  - Contrast compliance specification document
```

---

## When This Task Runs

This task runs when:
- Design system tokens change (new colors, theme update)
- Dark mode implementation needs contrast validation
- Accessibility audit reveals contrast issues
- New color palette is introduced
- `*color-contrast` or `*contrast-audit` is invoked

This task does NOT run when:
- Focus management issues (use `focus-management-design`)
- Screen reader testing (use `screen-reader-testing`)
- General accessibility audit (use `accessibility-audit`)

---

## Execution Steps

### Step 1: Extract Color Pairs

Scan the codebase for all foreground/background color combinations.

**Sources to scan:**
- CSS custom properties (`--color-*`)
- Tailwind config (`theme.colors`)
- Inline styles and class combinations
- Component-level style overrides

**For each element, extract:**

| Field | Example |
|-------|---------|
| Component | `Header.tsx` |
| Element | `<h1>` |
| Foreground | `#1e293b` (slate-800) |
| Background | `rgba(255,255,255,0.8)` |
| Font size | `24px` |
| Font weight | `700` |
| Context | Light mode / Dark mode |

**Edge cases:**
- Opacity < 1: flatten against parent background
- Gradients: test against lightest and darkest stops
- Backdrop-filter/blur: estimate effective background
- CSS variables: resolve full chain to final value

**Output:** Color pair inventory.

### Step 2: Compute Contrast Ratios

Calculate WCAG 2.2 contrast ratios for every pair.

**WCAG thresholds:**

| Level | Normal text (<18px/14px bold) | Large text (>=18px/14px bold) | Non-text (icons, borders) |
|-------|------|------|------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | — |

**Algorithm:**
1. Convert hex/rgb/hsl to relative luminance
2. `ratio = (L1 + 0.05) / (L2 + 0.05)` where L1 > L2
3. Classify as PASS (AA), PASS (AAA), or FAIL

**Output:** Contrast ratio report with pass/fail per pair.

### Step 3: Generate Violation Report

For each failing pair, provide actionable fixes.

**Violation entry format:**
```
FAIL: Header.tsx <p class="text-slate-400 bg-white">
  Ratio: 2.8:1 (needs 4.5:1 for AA)
  Fix: Change text-slate-400 → text-slate-600 (ratio: 5.3:1)
  Alt: Change bg-white → bg-slate-100 (ratio: 4.7:1)
```

**Fix algorithm:**
- Find nearest Tailwind/token color that meets threshold
- Prefer darkening foreground over lightening background
- Preserve design intent (warm stays warm, cool stays cool)
- Minimize perceptual color shift (deltaE < 10)

**Output:** Violation list with suggested fixes.

### Step 4: Dark Mode Contrast Delta

Compare contrast ratios between light and dark mode.

**Report includes:**
- Pairs that PASS in light but FAIL in dark (common!)
- Pairs that PASS in dark but FAIL in light (rare)
- Ratio delta per pair (how much contrast changes)
- Dark mode specific recommendations

**Output:** Dark mode contrast delta report.

### Step 5: Document Contrast Architecture

Compile the complete specification.

**Documentation includes:**
- Color pair inventory (from Step 1)
- Contrast ratio report (from Step 2)
- Violation list with fixes (from Step 3)
- Dark mode delta (from Step 4)
- WCAG 2.2 quick reference
- Guidelines for adding new colors safely
- CI integration recommendations (axe-core, Storybook a11y addon)

**Output:** Contrast compliance specification document.

---

## Quality Criteria

- Zero FAIL pairs at AA level for all text elements
- Dark mode contrast ratios within 10% of light mode equivalents
- All suggested fixes maintain design language consistency
- Gradient and opacity edge cases explicitly handled
- Report covers 100% of color pairs in codebase

---

*Squad Apex — Color Contrast Automation Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-color-contrast-automation
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Zero FAIL pairs at WCAG AA level"
    - "Dark mode coverage matches light mode"
    - "All fixes preserve design language"
    - "Gradient/opacity edge cases documented"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@css-eng` or `@design-sys-eng` |
| Artifact | Contrast compliance report with violation fixes |
| Next action | Apply fixes via `@css-eng` or update tokens via `@design-sys-eng` |
