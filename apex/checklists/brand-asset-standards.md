# Checklist: Brand Asset Standards

```yaml
id: brand-asset-standards
version: "1.0.0"
description: "Quality standards for brand assets (logos, icons, visual identity elements)"
owner: apex-lead
usage: "Run during apex-asset-pipeline quality review before presenting assets to user"
gate: QG-AX-BRAND
```

---

## Visual Fidelity

- [ ] **Brand colors match extracted palette** — deltaE < 3 for all primary and secondary brand colors
- [ ] **Proportions match original within 2%** — aspect ratio and element spacing preserved
- [ ] **Renders without artifacts at all target sizes** — clean at 16px, 32px, 64px, 128px, 256px
- [ ] **Works in both light and dark modes** — no invisible elements or clashing backgrounds
- [ ] **Geometric simplification preserves brand essence** — recognizable at a glance, key shapes intact
- [ ] **Professional quality** — not a crude approximation; suitable for production use

---

## Technical Standards

- [ ] **SVG uses viewBox** — no hardcoded width/height attributes on root element
- [ ] **Colors use currentColor or CSS custom properties** — no hardcoded hex values in markup
- [ ] **File size within budget** — SVG < 10KB for simple icons, < 30KB for moderate complexity
- [ ] **No inline styles** — use classes or presentational attributes (fill, stroke) instead
- [ ] **Optimized with SVGO** — no editor metadata, no empty groups, no unused defs
- [ ] **Accessible** — has `role="img"` + `aria-label` for meaningful icons, OR `aria-hidden="true"` for decorative
- [ ] **No raster images embedded in SVG** — no `<image>` elements with base64 or external bitmap references
- [ ] **Valid SVG markup** — no deprecated elements, well-formed XML, no namespace pollution

---

## Design System Integration

- [ ] **Brand colors extracted and mapped to design tokens** — CSS custom properties or Tailwind config entries created
- [ ] **Icon sizes follow project's size scale** — xs/sm/md/lg/xl matching existing icon library conventions
- [ ] **Stroke width matches existing icon library** — consistent with Lucide, Heroicons, or project standard
- [ ] **Visual weight consistent with other project icons** — optical balance, not just dimensional match
- [ ] **React component created with typed props** — exported with TypeScript interface (size, color, className, aria-label)

---

## Brand Honesty Gate

- [ ] **Geometric recreation clearly identified as "inspired by"** — not presented as official brand asset
- [ ] **Complex logos that cannot be faithfully reproduced are flagged** — user informed before effort is invested
- [ ] **Original asset preserved alongside geometric version** — both versions available for comparison
- [ ] **User informed of fidelity level before approval** — explicit disclosure of simplification trade-offs

---

## Cross-Platform

- [ ] **Renders correctly on Web** — verified in Chrome, Safari, and Firefox (no rendering differences)
- [ ] **Scales properly on mobile** — responsive sizing, tested in React Native context if applicable
- [ ] **Supports reduced-motion** — no animated SVG without static fallback; respects `prefers-reduced-motion`
