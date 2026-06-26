# Task: web-asset-optimize

```yaml
id: web-asset-optimize
version: "1.0.0"
title: "Asset Optimization Pipeline"
description: >
  Optimize visual assets for web delivery. Handles format conversion (WebP, AVIF),
  responsive srcset generation, lazy-load setup, and quality assessment.
  Works on project files or URLs from asset-hunt results.
elicit: true
owner: web-intel
executor: web-intel
delegates_to: perf-eng
inputs:
  - source: "File path(s) or URL(s)"
outputs:
  - Optimization report (before/after sizes)
  - Converted files (WebP, AVIF)
  - srcset configuration
  - Lazy-load implementation plan
veto_conditions:
  - "Optimization that reduces visual quality below acceptable threshold → BLOCK"
  - "Replacing original files without backup → BLOCK"
```

---

## Command

### `*asset-optimize {path|url}`

Optimize visual assets for web performance.

---

## Execution Steps

### Step 1: Inventory Assets

Scan target path/URL for visual assets. Catalog:
- File format, dimensions, file size
- Color depth, compression level
- Current loading strategy (eager/lazy)

### Step 2: Analyze Optimization Opportunities

```yaml
analysis:
  format:
    - "JPEG/PNG → WebP (30-50% smaller, wide support)"
    - "JPEG/PNG → AVIF (50-70% smaller, growing support)"
    - "Large SVG → optimized SVG (SVGO)"
    - "GIF → WebP/MP4 (animated)"
  responsive:
    - "Missing srcset → generate variants (375w, 768w, 1440w, 2880w)"
    - "Missing sizes attribute → add viewport-based sizes"
    - "Missing width/height → add to prevent CLS"
  loading:
    - "Above-fold without eager → ensure eager"
    - "Below-fold without lazy → add loading=lazy"
    - "Large hero images → consider progressive JPEG or LQIP"
  quality:
    - "Over-compressed → suggest higher quality"
    - "Under-compressed (>500KB) → suggest optimization"
    - "Wrong dimensions (2x+ larger than display) → suggest resize"
```

**Elicitation:**
```
Found {N} assets to optimize.

Optimization level:
1. Conservative (format only, keep quality)
2. Balanced (format + responsive + lazy load)
3. Aggressive (all optimizations, max compression)

Which level? (1/2/3, default: 2)
```

### Step 3: Generate Optimization Plan

```
## Optimization Plan

| Asset | Current | Optimized | Saving | Actions |
|-------|---------|-----------|--------|---------|
| hero.jpg | 1.2MB JPEG | 380KB WebP | -68% | Convert + resize |
| card.png | 450KB PNG | 120KB WebP | -73% | Convert |
| logo.svg | 45KB SVG | 12KB SVG | -73% | SVGO |

Total saving: {X}MB → {Y}MB (-{Z}%)

Additional:
- {N} images need srcset variants
- {N} images need lazy loading
- {N} images need width/height

Proceed? (yes / adjust / cancel)
```

### Step 4: Execute or Delegate

```yaml
routing:
  simple_optimizations: "Execute directly (format notes, srcset suggestions)"
  complex_optimizations: "Delegate to @perf-eng with optimization plan"
  3d_assets: "Delegate to @spatial-eng for poly reduction"
```
