# Task: apex-asset-pipeline

```yaml
id: apex-asset-pipeline
version: "1.0.0"
title: "Brand Asset Pipeline — Logo & Icon Recreation"
description: >
  End-to-end pipeline for handling brand visual assets. Three modes:
  GEOMETRIC (recreate logo as geometric SVG), ENHANCE (optimize existing asset),
  and COMPOSE (create new icon/logo from design tokens + geometric primitives).
  Includes brand color extraction from images, geometric simplification,
  quality gates for brand fidelity, and integration with design system tokens.
elicit: true
owner: apex-lead
executor: design-sys-eng
delegates_to: [css-eng, web-intel, qa-visual]
inputs:
  - source: "Image file (PNG/SVG/JPG), URL, or description"
  - mode: "geometric | enhance | compose (default: auto-detect)"
outputs:
  - Processed asset (SVG preferred, PNG fallback)
  - Brand color palette extracted
  - Design token integration map
  - Quality report (fidelity score)
veto_conditions:
  - "Asset used without license verification → BLOCK"
  - "SVG with >50 path nodes without simplification attempt → PAUSE"
  - "Brand colors not extracted to tokens → BLOCK"
  - "No reduced-motion alternative for animated assets → BLOCK"
  - "Hardcoded colors in SVG (not using currentColor or tokens) → PAUSE"
  - "Asset >100KB without optimization → BLOCK"
  - "Claiming pixel-perfect reproduction of complex brand logo → BLOCK (honesty gate)"
```

---

## Command

### `*asset-pipeline {source}`

Process brand assets through the full pipeline.

**Aliases:** `*logo`, `*icon-create`

---

## Execution Steps

### Step 1: Analyze Source

```yaml
source_analysis:
  if_image_file: "Extract: dimensions, format, file size, color count, complexity score"
  if_url: "Fetch image, then analyze as above"
  if_description: "Skip to Step 3 (Compose mode)"

complexity_classification:
  simple: "< 5 distinct shapes, < 8 colors → Geometric recreation viable"
  moderate: "5-15 shapes, 8-20 colors → Geometric with simplification"
  complex: "> 15 shapes, > 20 colors → Enhance mode recommended"
  photographic: "Continuous tones detected → Optimize only, no recreation"
```

**Elicitation:**
```
Source analyzed:
- Complexity: {simple|moderate|complex|photographic}
- Colors detected: {count}
- Recommendation: {geometric|enhance|compose}

Proceed with {recommendation}?
1. Yes, proceed
2. Switch to {alternative mode}
3. Show me the extracted colors first
```

### Step 2: Extract Brand Palette

For any image input, extract the dominant color palette:

```yaml
palette_extraction:
  method: "Dominant color clustering (k-means, k=5-8)"
  output:
    primary: "Most dominant non-neutral color"
    secondary: "Second most dominant"
    accent: "Most saturated color"
    neutrals: "Background/text colors"
  token_mapping:
    - Map each extracted color to nearest design token
    - Create new tokens if no match within deltaE < 5
    - Generate both light and dark mode variants
  format:
    css_variables: true
    tailwind_extend: true
    hex_and_oklch: true
```

### Step 3: Process by Mode

#### Mode A: GEOMETRIC (recreate as SVG)

```yaml
geometric_recreation:
  approach:
    1. "Identify primary geometric shapes (circles, rectangles, triangles, arcs)"
    2. "Map brand typography to closest available web font or geometric letterforms"
    3. "Simplify complex curves to geometric approximations"
    4. "Apply extracted brand colors"
    5. "Ensure viewBox and aspect ratio match original"

  techniques:
    shapes: "Use SVG primitives: rect, circle, ellipse, polygon, path (minimal nodes)"
    text: "Convert to geometric paths OR use web-safe font approximation"
    gradients: "Preserve key gradients using SVG linearGradient/radialGradient"
    effects: "Glass, glow, shadow via SVG filters (feGaussianBlur, feDropShadow)"

  quality_gate:
    - "Side-by-side comparison with original"
    - "Brand essence preserved (colors, proportions, character)"
    - "SVG file size < 10KB (simple), < 30KB (moderate)"
    - "Renders correctly at 16px, 32px, 64px, 128px, 256px"

  honesty_clause: >
    CRITICAL: If the original logo has complex proprietary typography,
    intricate illustrations, or photographic elements that CANNOT be
    faithfully reproduced as geometric SVG, INFORM the user immediately.
    Offer alternatives: simplified geometric interpretation, icon-only
    version, or typography-only with brand colors. NEVER claim fidelity
    that doesn't exist.
```

#### Mode B: ENHANCE (optimize existing)

```yaml
enhance_pipeline:
  steps:
    1. "Convert to optimal format (SVG if vector, WebP/AVIF if raster)"
    2. "Generate responsive variants (srcset: 1x, 2x, 3x)"
    3. "Add proper metadata (alt text, aria-label)"
    4. "Integrate with design system (currentColor, token references)"
    5. "Generate dark mode variant if applicable"
    6. "Optimize file size (SVGO for SVG, sharp for raster)"
```

#### Mode C: COMPOSE (create from scratch)

```yaml
compose_workflow:
  inputs:
    description: "What the icon/logo should represent"
    style: "geometric | outlined | filled | duotone | 3d"
    brand_tokens: "Colors, typography from design system"

  approach:
    1. "Generate 3 concept options using geometric primitives"
    2. "Present options with rationale"
    3. "User selects or provides feedback"
    4. "Refine selected option"
    5. "Generate multi-size variants (16, 24, 32, 48, 64, 128)"
    6. "Export as React component with currentColor support"

  output_format:
    svg_file: true
    react_component: true
    design_tokens: "Icon-specific tokens (stroke-width, corner-radius)"
```

### Step 4: Integration

```yaml
integration:
  design_system:
    - "Register asset in project's asset catalog"
    - "Map colors to existing design tokens"
    - "Generate usage examples"

  react_component:
    - "Create typed React component wrapper"
    - "Support: size, color (currentColor), className, aria-label"
    - "Include loading/error states for remote assets"

  documentation:
    - "Add to asset catalog with metadata"
    - "Include original source reference"
    - "Document any simplification decisions"
```

### Step 5: Quality Review

```yaml
quality_review:
  visual_check:
    - "Renders at all target sizes without artifacts"
    - "Colors match extracted palette (deltaE < 3)"
    - "Proportions match original within 2%"
    - "Works in both light and dark modes"

  technical_check:
    - "SVG is accessible (role, aria-label, title)"
    - "No hardcoded dimensions (uses viewBox)"
    - "Colors use currentColor or CSS variables"
    - "File size within budget"

  brand_check:
    - "Captures the ESSENCE of the brand (even if simplified)"
    - "Professional quality — not a crude approximation"
    - "Harmonizes with the project's design system"
```

---

## Limitations (Honesty Protocol)

This pipeline is HONEST about what it can and cannot do:

| CAN DO | CANNOT DO |
|--------|-----------|
| Geometric logo recreation (shapes + colors) | Pixel-perfect reproduction of complex brand logos |
| Brand color palette extraction | Access proprietary brand fonts |
| Icon composition from geometric primitives | Reproduce intricate illustrations |
| SVG optimization and enhancement | Convert photographs to vector art |
| Design system integration | Replace professional brand design tools |
| Multi-size responsive variants | Generate logos that violate trademark law |

**When in doubt:** Present the limitation honestly and offer the best achievable alternative.

---

## Intent Chaining

```yaml
after_completion:
  options:
    - "Create more assets with same brand palette"
    - "Integrate into design system (*export-tokens)"
    - "Run visual QA (*apex-analyze)"
    - "Done"
```
