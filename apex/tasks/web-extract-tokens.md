# Task: web-extract-tokens

```yaml
id: web-extract-tokens
version: "1.0.0"
title: "Design Token Extraction from URL"
description: >
  Focused extraction of design tokens (colors, typography, spacing, shadows, radius)
  from an external URL. Lighter than full scrape — skips pattern analysis and asset discovery.
  Outputs structured token map with source traceability.
elicit: false
owner: web-intel
executor: web-intel
inputs:
  - url: "Target URL"
outputs:
  - Structured token map with [SOURCE] tags
  - Near-duplicate report
  - Scale detection results
veto_conditions:
  - "Tokens without [SOURCE] tags → BLOCK"
  - "Auto-apply without user decision → BLOCK"
```

---

## Command

### `*extract-tokens {url}`

Extract design tokens only — colors, typography, spacing, shadows, radius.

---

## Execution Steps

### Step 1: Navigate & Render

Navigate to URL using playwright. Wait for full render (networkidle).
Capture computed styles from all visible elements on desktop viewport (1440px).

### Step 2: Extract CSS Custom Properties

```yaml
primary_extraction:
  - "Scan all stylesheets for --custom-property declarations"
  - "Resolve computed values via getComputedStyle()"
  - "Map: property-name → resolved-value → source-selector"
```

### Step 3: Extract Computed Values

```yaml
categories:
  colors:
    properties: [color, background-color, border-color, outline-color]
    dedup: "HSL distance < 5%"
    classify: [bg, fg, border, accent, success, warning, danger, muted]

  typography:
    properties: [font-family, font-size, font-weight, line-height, letter-spacing]
    detect: "type scale ratio"
    classify: [h1, h2, h3, h4, body, caption, label, code]

  spacing:
    properties: [padding, margin, gap]
    detect: "base unit (GCD of common values)"
    output: "scale array"

  shadows:
    properties: [box-shadow]
    classify: [sm, md, lg, xl]

  radius:
    properties: [border-radius]
    output: "unique values sorted"
```

### Step 4: Deduplicate & Structure

- Cluster near-duplicate colors (HSL < 5%)
- Detect spacing scale base unit
- Detect type scale ratio
- Tag every value with `[SOURCE: url, selector, property]`

### Step 5: Present Results

```
## Token Extraction: {url}

### Colors ({N} intentional from {M} extracted)
| Role | Value | Uses | Source |
|------|-------|------|--------|
| ... | ... | ... | ... |

### Typography (scale ratio: {ratio})
| Level | Size | Weight | Font | Source |
|-------|------|--------|------|--------|
| ... | ... | ... | ... | ... |

### Spacing (base: {N}px)
{scale array}

### Shadows ({N} levels)
| Level | Value | Source |
|-------|-------|--------|
| ... | ... | ... |

### Radius
| Value | Uses | Source |
|-------|------|--------|
| ... | ... | ... |

---

Options:
1. ADOPT — Use these tokens
2. ADAPT — Map to our naming (→ @design-sys-eng)
3. COMPARE — Side-by-side with project
4. EXPORT — CSS/SCSS/JSON
5. Done
```
