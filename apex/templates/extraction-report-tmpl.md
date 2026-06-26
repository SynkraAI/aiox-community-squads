# Template: Design Intelligence Report

```yaml
id: extraction-report-tmpl
version: "1.0.0"
description: "Structured report template for design intelligence extraction results"
owner: web-intel
usage: "Used by web-scrape-analyze and web-extract-tokens tasks"
```

---

## Design Intelligence Report: {url}

**Extracted:** {date}
**Viewports:** {mobile (375px) | tablet (768px) | desktop (1440px)}
**Scope:** {full | tokens-only | patterns-only | assets-only}

---

### Color Palette ({N} intentional from {M} extracted)

| Role | Value | Hex | Uses | Source |
|------|-------|-----|------|--------|
| bg-primary | {desc} | {hex} | {n}x | [SOURCE: {url}, {selector}, {property}] |
| fg-primary | {desc} | {hex} | {n}x | [SOURCE: {url}, {selector}, {property}] |
| accent | {desc} | {hex} | {n}x | [SOURCE: {url}, {selector}, {property}] |
| ... | ... | ... | ... | ... |

**Near-duplicates consolidated:** {N} values merged into {M} intentional colors.
**Color noise:** {N} one-off colors excluded (used < 2 times).

---

### Typography Scale (ratio: {ratio})

| Level | Size | Weight | Line-height | Font | Source |
|-------|------|--------|-------------|------|--------|
| h1 | {px/rem} | {weight} | {ratio} | {font} | [SOURCE: ...] |
| h2 | {px/rem} | {weight} | {ratio} | {font} | [SOURCE: ...] |
| h3 | {px/rem} | {weight} | {ratio} | {font} | [SOURCE: ...] |
| body | {px/rem} | {weight} | {ratio} | {font} | [SOURCE: ...] |
| caption | {px/rem} | {weight} | {ratio} | {font} | [SOURCE: ...] |

**Fonts detected:** {list}
**Fallback stacks:** {list}

---

### Spacing Scale (base: {N}px)

```
{scale values separated by →}
Example: 4 → 8 → 12 → 16 → 24 → 32 → 48 → 64
```

**Base unit:** {N}px
**Scale type:** {linear | exponential | custom}

---

### Shadows ({N} elevation levels)

| Level | Value | Uses | Source |
|-------|-------|------|--------|
| sm | {value} | {n}x | [SOURCE: ...] |
| md | {value} | {n}x | [SOURCE: ...] |
| lg | {value} | {n}x | [SOURCE: ...] |

---

### Border Radius

| Value | Uses | Context | Source |
|-------|------|---------|--------|
| {px} | {n}x | {buttons, cards, inputs} | [SOURCE: ...] |

---

### Motion (if scope includes motion)

| Element | Type | Duration | Easing | Category |
|---------|------|----------|--------|----------|
| {selector} | {transition/animation} | {ms} | {easing} | {enter/exit/feedback} |

**Spring vs Bezier:** {N}% spring, {M}% bezier
**Reduced motion:** {handled | partial | not handled}

---

### Assets (if scope includes assets)

| # | Type | Dimensions | Format | Size | Context |
|---|------|-----------|--------|------|---------|
| 1 | {photo/icon/svg} | {WxH} | {format} | {KB} | {hero/card/bg} |

---

### Summary

| Category | Extracted | Intentional | Signal/Noise |
|----------|-----------|-------------|--------------|
| Colors | {M} | {N} | {ratio}% |
| Typography | {N} levels | {N} in scale | — |
| Spacing | {N} values | {base}px base | — |
| Shadows | {N} levels | — | — |
| Radius | {N} values | — | — |

---

### Options

1. **ADOPT** — Import compatible tokens into project
2. **ADAPT** — Map to existing token names (→ @design-sys-eng)
3. **COMPARE** — Side-by-side with current design system
4. **DEEP DIVE** — Analyze specific category further
5. **EXPORT** — Export as CSS / SCSS / JSON / Figma Variables
6. **Done**

What would you like to do? (1-6)
