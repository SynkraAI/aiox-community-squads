# Checklist: Source Traceability

```yaml
id: source-traceability
version: "1.0.0"
description: "Verification checklist for source traceability in extracted design intelligence"
owner: web-intel
usage: "Validate that every extracted value can be traced back to its origin"
```

---

## Source Tag Format

Every extracted value MUST have a source tag in this format:

```
[SOURCE: {url}, {selector}, {css-property}]
```

**Examples:**
```
[SOURCE: linear.app, body, background-color]
[SOURCE: stripe.com, .btn-primary, box-shadow]
[SOURCE: github.com, :root, --color-fg-default]
```

---

## Verification Checks

### Tag Presence
- [ ] **100% coverage** — every extracted token has a [SOURCE] tag
- [ ] **No placeholder sources** — no "unknown", "auto", or empty sources
- [ ] **No generic selectors** — avoid "div", "span" — use meaningful selectors

### Tag Accuracy
- [ ] **URL is correct** — matches the actual source page
- [ ] **Selector exists** — the CSS selector is real and findable
- [ ] **Property matches** — the CSS property is correct for the value type
- [ ] **Value matches** — computed value matches what was tagged

### Tag Completeness
- [ ] **Colors** — all have source (selector where color was found)
- [ ] **Typography** — all have source (selector where font was applied)
- [ ] **Spacing** — all have source (selector where padding/margin was found)
- [ ] **Shadows** — all have source (selector where shadow was applied)
- [ ] **Radius** — all have source (selector where radius was found)
- [ ] **Motion** — all have source (selector where transition/animation was found)

### Asset Sources
- [ ] **Image URLs are absolute** — full URL, not relative path
- [ ] **Image context noted** — where on the page (hero, card, bg, icon)
- [ ] **SVG sources identified** — inline vs external reference
- [ ] **License source noted** — where the license info was found

### Cross-Reference
- [ ] **Duplicates reference same source** — if same value appears twice, sources should differ (different selectors)
- [ ] **Overridden values noted** — if CSS cascade overrides a value, note the winning selector
- [ ] **Custom properties traced** — --var values traced to their declaration, not just usage
