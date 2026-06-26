# Task: web-scrape-analyze

```yaml
id: web-scrape-analyze
version: "1.0.0"
title: "Full Design Intelligence Extraction"
description: >
  Complete scrape and analysis pipeline for an external URL. Extracts design tokens
  (colors, typography, spacing, shadows, radius), component patterns, layout structures,
  visual assets, and responsive behavior across 3 viewports. Outputs a structured
  Design Intelligence Report with human-in-the-loop options.
elicit: true
owner: web-intel
executor: web-intel
inputs:
  - url: "Target URL to analyze"
  - scope: "full | tokens-only | patterns-only | assets-only (default: full)"
outputs:
  - Design Intelligence Report (structured)
  - Token map with source traceability
  - Pattern inventory
  - Asset catalog
  - Comparison with current project (if applicable)
veto_conditions:
  - "Output without [SOURCE: url, selector, property] tags → BLOCK"
  - "Auto-apply without user approval → BLOCK"
  - "Raw unsorted data delivery → BLOCK"
  - "Extraction from URL without rendering the page → BLOCK (computed styles require render)"
```

---

## Command

### `*scrape {url}`

Full design intelligence extraction from a URL. Captures everything visible.

---

## Execution Steps

### Step 1: Validate & Scope

```yaml
validations:
  - check: "URL is valid and accessible"
    on_fail: "Report error, suggest alternatives"
  - check: "URL responds within 10 seconds"
    on_fail: "Report timeout, suggest retry or cached version"
```

**Elicitation:**
```
Target: {url}

Scope options:
1. Full analysis (tokens + patterns + assets + responsive) — ~3 min
2. Tokens only (colors, typography, spacing, shadows) — ~1 min
3. Patterns only (components, layout, interactions) — ~1 min
4. Assets only (images, icons, illustrations) — ~1 min

Which scope? (1/2/3/4, default: 1)
```

### Step 2: Navigate & Capture

Use playwright to navigate to the URL and capture across 3 viewports:

```yaml
viewports:
  mobile:
    width: 375
    height: 812
    captures: [screenshot, computed_styles, dom_structure]
  tablet:
    width: 768
    height: 1024
    captures: [screenshot, computed_styles, dom_structure]
  desktop:
    width: 1440
    height: 900
    captures: [screenshot, computed_styles, dom_structure]

capture_method:
  - "Navigate to URL with playwright"
  - "Wait for full render (networkidle or 5s timeout)"
  - "Capture full-page screenshot per viewport"
  - "Extract computed styles via getComputedStyle() on all visible elements"
  - "Extract DOM structure for component identification"
```

### Step 3: Extract & Categorize

Parse captured data into structured categories:

```yaml
categories:
  colors:
    extract_from: [color, background-color, border-color, box-shadow, outline-color]
    output_format:
      - value: "hex/rgba"
      - usage_count: "number"
      - context: "bg | fg | border | accent | shadow"
      - source: "[SOURCE: url, selector, property]"
    dedup_threshold: "HSL distance < 5% = near-duplicate"

  typography:
    extract_from: [font-family, font-size, font-weight, line-height, letter-spacing]
    output_format:
      - level: "h1 | h2 | h3 | body | caption | label"
      - font_family: "string"
      - size: "px/rem"
      - weight: "number"
      - line_height: "ratio"
      - source: "[SOURCE: url, selector, property]"

  spacing:
    extract_from: [padding, margin, gap, grid-gap]
    output_format:
      - scale_detection: "Find base unit (4px, 8px, etc.)"
      - values: "sorted unique values with usage count"
      - source: "[SOURCE: url, selector, property]"

  shadows:
    extract_from: [box-shadow, text-shadow]
    output_format:
      - level: "elevation name (sm, md, lg, xl)"
      - value: "full shadow string"
      - usage_count: "number"
      - source: "[SOURCE: url, selector, property]"

  radius:
    extract_from: [border-radius]
    output_format:
      - values: "sorted unique values"
      - usage_count: "per value"
      - source: "[SOURCE: url, selector, property]"

  motion:
    extract_from: [transition, animation, transform]
    output_format:
      - type: "transition | animation | transform"
      - properties: "what animates"
      - duration: "ms"
      - easing: "string or spring config"
      - source: "[SOURCE: url, selector, property]"

  assets:
    extract_from: [img[src], svg, background-image, picture source]
    output_format:
      - url: "asset URL"
      - dimensions: "width x height"
      - format: "jpg | png | svg | webp | avif"
      - context: "hero | card | icon | background | logo"
      - alt_text: "string or missing"
      - file_size: "estimated KB"
```

### Step 4: Analyze & Deduplicate

```yaml
analysis:
  colors:
    - "Cluster by HSL distance (< 5% = near-duplicate)"
    - "Identify intentional palette vs noise"
    - "Map roles: primary, secondary, accent, bg, fg, border, success, warning, danger"
    - "Report: N extracted → M intentional (N-M consolidated)"

  typography:
    - "Detect type scale ratio (1.2, 1.25, 1.333, 1.414, 1.5, 1.618)"
    - "Map heading hierarchy (h1-h6)"
    - "Identify body, caption, label sizes"
    - "Report: font families, scale ratio, hierarchy"

  spacing:
    - "Detect base unit (most common divisor)"
    - "Build scale: base × multipliers"
    - "Report: base unit, scale, outliers"

  motion:
    - "Identify spring vs bezier usage"
    - "Categorize by interaction type (enter, exit, hover, feedback)"
    - "Report: animation inventory with timing"
```

### Step 5: Compare with Project (if applicable)

```yaml
comparison:
  condition: "If current project has design tokens (CSS vars, Tailwind config, theme)"
  method:
    - "Load project tokens from src/index.css, tailwind.config.*, or theme files"
    - "Map extracted tokens to project token categories"
    - "Generate delta: matches, differences, gaps, conflicts"
  output: "Comparison table with adoption recommendations"
```

### Step 6: Generate Report & Present Options

Use `templates/extraction-report-tmpl.md` for the report format.

**Present options:**
```
## Design Intelligence Report: {url}

[... structured report ...]

---

Options:
1. **ADOPT** — Import compatible tokens into project
2. **ADAPT** — Map to existing token names (→ @design-sys-eng)
3. **COMPARE** — Side-by-side with current design system
4. **DEEP DIVE** — Analyze specific category further
5. **EXPORT** — Export tokens as CSS/SCSS/JSON/Figma
6. **Done**

What would you like to do? (1-6)
```

### Step 7: Execute User Decision

```yaml
decision_routing:
  adopt:
    - "Generate token file in project format"
    - "Handoff to @design-sys-eng for integration"
  adapt:
    - "Map extracted names to project conventions"
    - "Handoff to @design-sys-eng for fusion"
  compare:
    - "Generate side-by-side comparison table"
    - "Highlight matches, differences, gaps"
  deep_dive:
    - "Ask which category to explore"
    - "Show detailed breakdown with all values"
  export:
    - "Ask format: CSS | SCSS | JSON | Figma Variables"
    - "Generate export file"
```

---

## Handoff Protocol

```yaml
handoff_to_design_sys_eng:
  format: "EXTRACTION_READY"
  contents:
    tokens: "Structured token map with categories"
    sources: "All [SOURCE] tags preserved"
    user_decisions: "Which tokens were marked ADOPT or ADAPT"
    comparison: "Delta with current project tokens (if generated)"
  message: "Kilian extracted tokens from {url}. User approved {N} tokens for integration. Fuse with project design system."
```
