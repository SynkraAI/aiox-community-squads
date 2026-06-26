# Template: Asset Catalog

```yaml
id: asset-catalog-tmpl
version: "1.0.0"
description: "Curated asset catalog template with metadata, quality scores, and licensing"
owner: web-intel
usage: "Used by web-asset-hunt task"
```

---

## Asset Catalog: {query or url}

**Curated:** {date}
**Source:** {URL extraction | Web search | Mixed}
**Filter:** {all | photos | icons | illustrations | 3d}

---

### Photos ({N} curated from {M} found)

| # | Description | Resolution | Format | Size | License | Quality | Context |
|---|-------------|-----------|--------|------|---------|---------|---------|
| 1 | {desc} | {W}x{H} | {format} | {KB} | {license} | {score}/10 | {hero/card/bg} |
| 2 | {desc} | {W}x{H} | {format} | {KB} | {license} | {score}/10 | {context} |

---

### Icons ({N} found)

| # | Name | Format | Source | Style | License |
|---|------|--------|--------|-------|---------|
| 1 | {name} | SVG | {source} | {outline/solid/duotone} | {license} |

---

### Illustrations ({N} found)

| # | Description | Format | Source | Customizable | License |
|---|-------------|--------|--------|-------------|---------|
| 1 | {desc} | {SVG/PNG} | {source} | {yes/no} | {license} |

---

### 3D Assets ({N} found)

| # | Description | Format | Polygons | Textures | License | Source |
|---|-------------|--------|----------|----------|---------|--------|
| 1 | {desc} | {GLB/GLTF/OBJ} | {count} | {yes/no} | {license} | {source} |

---

### Optimization Recommendations

| Asset | Current | Recommended | Estimated Saving |
|-------|---------|-------------|-----------------|
| {name} | {format}, {size} | {new format}, {new size} | -{percent}% |

**General recommendations:**
- [ ] Convert to WebP for photos (40-60% smaller)
- [ ] Generate srcset variants (375w, 768w, 1440w, 2880w)
- [ ] Add lazy loading for below-fold assets
- [ ] Add explicit width/height to prevent CLS
- [ ] Consider AVIF for modern browser targets

---

### License Summary

| License Type | Count | Commercial Use | Attribution |
|-------------|-------|---------------|-------------|
| CC0 / Public Domain | {n} | Yes | No |
| Unsplash / Pexels | {n} | Yes | No |
| MIT | {n} | Yes | Include license |
| CC-BY | {n} | Yes | Required |
| CC-BY-SA | {n} | Yes | Required + ShareAlike |
| CC-NC | {n} | No (non-commercial) | Required |
| Unknown | {n} | Verify before use | — |

---

### Options

1. **Select assets** — choose which to add to project
2. **Optimize** — run optimization pipeline (→ @perf-eng)
3. **3D integration** — prepare for Three.js/R3F (→ @spatial-eng)
4. **Search more** — refine query and search again
5. **Generate srcset** — create responsive variants
6. **Done**
