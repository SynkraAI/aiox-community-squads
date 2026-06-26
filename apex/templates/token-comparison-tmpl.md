# Template: Token Comparison Report

```yaml
id: token-comparison-tmpl
version: "1.0.0"
description: "Side-by-side comparison template for external vs project design tokens"
owner: web-intel
usage: "Used by web-compare-systems task"
```

---

## Design System Comparison: {external_url} vs {project_name}

**Compared:** {date}
**External:** {url}
**Project:** {project root}

---

### Overview

| Category | Matches | Similar | Different | Gaps (theirs) | Gaps (ours) |
|----------|---------|---------|-----------|---------------|-------------|
| Colors | {n} | {n} | {n} | {n} | {n} |
| Typography | {n} | {n} | {n} | {n} | {n} |
| Spacing | {match/diff} | — | — | — | — |
| Shadows | {n} | {n} | {n} | {n} | {n} |
| Radius | {n} | {n} | {n} | {n} | {n} |
| Motion | {n} | {n} | {n} | {n} | {n} |

---

### Colors Comparison

| Role | Ours | Theirs | Status | Recommendation |
|------|------|--------|--------|----------------|
| bg-primary | {hex} | {hex} | {match/similar/different} | {keep/adopt/adapt} |
| fg-primary | {hex} | {hex} | {match/similar/different} | {keep/adopt/adapt} |
| accent | {hex} | {hex} | {match/similar/different} | {keep/adopt/adapt} |
| — | — | {hex} | gap (theirs) | {adopt/ignore} |
| {name} | {hex} | — | gap (ours) | keep |

---

### Typography Comparison

| Level | Ours (size/weight/font) | Theirs (size/weight/font) | Status |
|-------|------------------------|--------------------------|--------|
| h1 | {size}/{weight}/{font} | {size}/{weight}/{font} | {status} |
| body | {size}/{weight}/{font} | {size}/{weight}/{font} | {status} |

**Our scale ratio:** {ratio}
**Their scale ratio:** {ratio}

---

### Spacing Comparison

| Dimension | Ours | Theirs | Status |
|-----------|------|--------|--------|
| Base unit | {n}px | {n}px | {match/different} |
| Scale | {array} | {array} | {compatible/incompatible} |

---

### Adoption Recommendations

| # | Category | Item | Action | Impact | Priority |
|---|----------|------|--------|--------|----------|
| 1 | {cat} | {item} | ADOPT | {impact} | {high/med/low} |
| 2 | {cat} | {item} | ADAPT | {impact} | {high/med/low} |
| 3 | {cat} | {item} | KEEP OURS | {reason} | — |
| 4 | {cat} | {item} | IGNORE | {reason} | — |

---

### Options

1. **Adopt all recommendations** (→ @design-sys-eng)
2. **Cherry-pick** — select specific items
3. **Export** — comparison as markdown
4. **Full detail** — token-by-token breakdown
5. **Done**
