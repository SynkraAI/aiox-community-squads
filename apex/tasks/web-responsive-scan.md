# Task: web-responsive-scan

```yaml
id: web-responsive-scan
version: "1.0.0"
title: "Multi-Viewport Responsive Analysis"
description: >
  Extract responsive behavior from a URL across multiple viewports. Detects
  breakpoints, fluid values, layout shifts, and responsive patterns. Captures
  how the design adapts across mobile, tablet, and desktop.
elicit: false
owner: web-intel
executor: web-intel
inputs:
  - url: "Target URL"
outputs:
  - Breakpoint map
  - Fluid value inventory (clamp, vw, min/max)
  - Layout shift analysis per viewport
  - Responsive pattern catalog
veto_conditions:
  - "Analysis from single viewport only → BLOCK"
```

---

## Command

### `*responsive-scan {url}`

Multi-viewport responsive extraction.

---

## Execution Steps

### Step 1: Capture Across Viewports

Navigate with playwright to the URL. Capture at 6 widths:
- 320px (mobile-s)
- 375px (mobile)
- 768px (tablet)
- 1024px (desktop-s)
- 1440px (desktop)
- 1920px (desktop-l)

Per viewport: screenshot + computed styles for key elements.

### Step 2: Detect Breakpoints

```yaml
breakpoint_detection:
  method: "Compare computed layout properties across viewport steps"
  signals:
    - "display value changes (block → flex → grid)"
    - "grid-template-columns changes"
    - "visibility/display:none toggles"
    - "font-size jumps"
    - "padding/margin jumps"
  output: "List of breakpoints with what changes at each"
```

### Step 3: Extract Fluid Values

```yaml
fluid_detection:
  scan_for:
    - "clamp() in font-size, padding, margin, gap"
    - "vw/vh/vmin/vmax units"
    - "min()/max() functions"
    - "calc() with viewport units"
  output: "Fluid value inventory with min/preferred/max"
```

### Step 4: Analyze Layout Shifts

```yaml
layout_shift_analysis:
  compare_between_viewports:
    - "Navigation: horizontal → hamburger?"
    - "Grid columns: 3 → 2 → 1?"
    - "Sidebar: visible → hidden?"
    - "Images: aspect ratio changes?"
    - "Typography: size jumps?"
  output: "Layout shift table per breakpoint"
```

### Step 5: Present Report

```
## Responsive Analysis: {url}

### Breakpoints Detected
| Breakpoint | Width | Changes |
|-----------|-------|---------|
| mobile | 375px | Single column, hamburger nav |
| tablet | 768px | 2-column grid, nav visible |
| desktop | 1024px | 3-column grid, sidebar |

### Fluid Values
| Property | Min | Preferred | Max | Used On |
|----------|-----|-----------|-----|---------|
| font-size h1 | 24px | 5vw | 48px | .hero-title |
| padding | 16px | 4vw | 64px | .container |

### Layout Strategy
- Approach: {mobile-first | desktop-first}
- Grid: {CSS Grid | Flexbox | Hybrid}
- Container queries: {yes | no}

Options:
1. Adopt breakpoint strategy
2. Adopt fluid values
3. Compare with our responsive setup
4. Done
```
