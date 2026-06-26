# Task: web-asset-hunt

```yaml
id: web-asset-hunt
version: "1.0.0"
title: "Visual Asset Discovery & Curation"
description: >
  Discover and curate visual assets from external sources. Two modes:
  URL mode (extract assets from a specific page) and Search mode (find assets
  matching a query across stock libraries and 3D repositories). Includes
  quality filtering, license checking, and optimization recommendations.
elicit: true
owner: web-intel
executor: web-intel
inputs:
  - source: "URL (page assets) or query string (web search)"
  - type: "all | photos | icons | illustrations | 3d (default: all)"
outputs:
  - Curated asset catalog with metadata
  - Quality scores per asset
  - License information
  - Optimization recommendations
veto_conditions:
  - "Assets without license status noted → PAUSE"
  - "Assets below quality threshold without flag → BLOCK"
  - "Auto-download without user selection → BLOCK"
  - "More than 20 assets presented without prioritization → BLOCK"
```

---

## Command

### `*asset-hunt {url|query}`

Discover and curate visual assets from URL or search query.

---

## Execution Steps

### Step 1: Determine Mode

```yaml
mode_detection:
  if_starts_with_http: "URL mode — extract assets from page"
  else: "Search mode — find assets matching query"
```

**Elicitation:**
```
Mode detected: {URL | Search}

Asset types:
1. All types (photos + icons + illustrations + 3D)
2. Photos only (stock, lifestyle, product)
3. Icons only (SVG, icon fonts)
4. Illustrations only (vector, hand-drawn)
5. 3D assets only (models, textures, HDRIs)

Which types? (1-5, default: 1)
```

### Step 2A: URL Mode — Extract Page Assets

```yaml
extraction:
  scan_elements:
    - "img[src] — standard images"
    - "picture > source — responsive images"
    - "svg (inline and referenced)"
    - "background-image in computed styles"
    - "canvas elements (3D/WebGL)"
    - "video[poster] — video thumbnails"
  capture_metadata:
    - url: "full asset URL"
    - dimensions: "natural width × height"
    - format: "jpg | png | svg | webp | avif | gif"
    - file_size: "estimated from headers"
    - alt_text: "alt attribute or aria-label"
    - context: "hero | card | thumbnail | icon | background | logo | decorative"
    - loading: "eager | lazy"
    - srcset: "responsive variants if available"
```

### Step 2B: Search Mode — Web Search

```yaml
search_sources:
  photos:
    - "Unsplash (free, high-quality)"
    - "Pexels (free, diverse)"
    - "Pixabay (free, large catalog)"
  icons:
    - "Lucide (open-source, consistent)"
    - "Heroicons (Tailwind ecosystem)"
    - "Phosphor (flexible weights)"
  illustrations:
    - "unDraw (open-source, customizable)"
    - "Humaaans (mix-and-match)"
    - "Open Doodles (hand-drawn)"
  3d_assets:
    - "Sketchfab (CC models)"
    - "Poly Haven (CC0 HDRIs, textures, models)"
    - "Quaternius (free low-poly)"
  search_method: "Use EXA web search to find matching assets"
```

### Step 3: Quality Filter

```yaml
quality_gates:
  photos:
    min_resolution: "1920x1080 (HD) for hero, 800x600 for cards"
    format_preference: "WebP > AVIF > JPEG > PNG"
    reject_if: "watermarked, heavily compressed, < 72dpi"
  icons:
    format_preference: "SVG (always)"
    consistency: "same style/weight family"
    reject_if: "raster format, inconsistent stroke width"
  3d:
    poly_budget: "< 50K for web, < 200K for spatial"
    format_preference: "GLB > GLTF > OBJ"
    reject_if: "no textures, broken normals"
```

### Step 4: License Check

```yaml
license_categories:
  free_commercial: "CC0, Unsplash License, MIT — safe for production"
  attribution_required: "CC-BY, CC-BY-SA — note attribution requirement"
  restricted: "CC-NC, proprietary — flag for review"
  unknown: "No license found — flag as risky"
```

### Step 5: Present Curated Catalog

```
## Asset Curation: {query or url}

### Photos ({N} curated from {M} found)
| # | Preview | Resolution | Format | License | Context |
|---|---------|-----------|--------|---------|---------|
| 1 | [desc] | 4000×2667 | JPEG | Unsplash | Hero |
| 2 | [desc] | 3840×2560 | JPEG | Pexels | Card |

### Icons ({N} found)
| # | Name | Format | Source | License |
|---|------|--------|--------|---------|
| 1 | stethoscope | SVG | Lucide | MIT |

### Optimization Recommendations
- Convert JPEG → WebP (40-60% smaller)
- Generate srcset: 375w, 768w, 1440w, 2880w (retina)
- Lazy load all below-fold images
- Add explicit width/height to prevent CLS

---

Options:
1. Select assets to add to project
2. Optimize selected assets (→ @perf-eng)
3. Search for more
4. Generate srcset variants
5. Done
```

### Step 6: Execute Selection

```yaml
on_select:
  - "Note selected assets with metadata"
  - "If optimization requested → handoff to @perf-eng"
  - "If 3D assets → handoff to @spatial-eng"
  - "Generate import recommendations for project"
```
