# Checklist: Extraction Quality

```yaml
id: extraction-quality
version: "1.0.0"
description: "Quality checklist for design intelligence extractions"
owner: web-intel
usage: "Run after every extraction before presenting results to user"
```

---

## Extraction Completeness

- [ ] **URL accessible** — page loaded successfully, no 4xx/5xx errors
- [ ] **Full render** — page fully rendered (JS executed, dynamic content loaded)
- [ ] **Multi-viewport** — captured at minimum mobile (375px) + desktop (1440px)
- [ ] **All categories extracted** — colors, typography, spacing, shadows, radius (for full scope)

## Source Traceability

- [ ] **Every value has [SOURCE] tag** — url, selector, property traced
- [ ] **No orphan values** — no extracted value without a source
- [ ] **Selectors are specific** — not just "div" but meaningful selectors
- [ ] **Source URLs are absolute** — no relative paths in source tags

## Data Quality

- [ ] **Near-duplicates identified** — HSL distance < 5% flagged
- [ ] **One-off values flagged** — values used < 2 times marked as noise
- [ ] **Scales detected** — spacing base unit and type scale ratio identified
- [ ] **Roles assigned** — colors mapped to roles (bg, fg, accent, border, etc.)
- [ ] **Values are computed** — using getComputedStyle, not source CSS

## Deduplication

- [ ] **Colors consolidated** — near-duplicates merged, count reported
- [ ] **Spacing normalized** — all values converted to same unit (px)
- [ ] **Typography deduplicated** — unique combinations only
- [ ] **Signal/noise ratio reported** — "N extracted, M intentional"

## Presentation

- [ ] **Structured output** — categorized tables, not flat lists
- [ ] **Sorted by usage** — most-used values first
- [ ] **Options presented** — ADOPT/ADAPT/COMPARE/IGNORE always shown
- [ ] **No auto-apply** — results are presented, never auto-applied
- [ ] **Prioritized** — max 20 items per category before consolidation

## Edge Cases

- [ ] **Dark mode checked** — if site has dark mode toggle, noted in report
- [ ] **Custom properties captured** — CSS --var declarations extracted
- [ ] **Web fonts identified** — font-family + loading strategy noted
- [ ] **Responsive tokens flagged** — values that change across viewports marked
