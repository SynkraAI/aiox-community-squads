---
id: rtl-layout-patterns
version: "1.0.0"
title: "RTL & Bidirectional Layout Patterns"
description: "Design RTL-safe layouts using CSS logical properties, bidirectional text handling, mirrored UI patterns, and locale-aware component variants"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - rtl-readiness-report.md
  - rtl-migration-plan.yaml
---

# RTL & Bidirectional Layout Patterns

## When This Task Runs

- App needs to support RTL locales (Arabic, Hebrew, Persian, Urdu)
- `*apex-i18n-audit` identified RTL gaps
- New component needs bidirectional support
- Design system audit for logical properties

## Execution Steps

### Step 1: Audit Current Layout Direction Support
```
SCAN project for RTL readiness:
- CSS physical properties (margin-left, padding-right, text-align: left, float: left)
- CSS logical properties (margin-inline-start, padding-inline-end)
- Tailwind directional classes (ml-4 vs ms-4)
- Hardcoded directional icons (arrows, chevrons)
- Transform: translateX (needs flip in RTL)
- Absolute positioning (left: 0 → inset-inline-start: 0)

OUTPUT: RTL readiness score + migration list
```

### Step 2: Define RTL Strategy

**elicit: true** — Confirm RTL approach:

| Strategy | Complexity | Best For |
|----------|-----------|----------|
| **CSS logical properties** | Low | New projects, modern browsers |
| **Tailwind RTL plugin** | Low | Tailwind projects |
| **CSS [dir="rtl"] overrides** | Medium | Legacy CSS migration |
| **Dedicated RTL stylesheet** | High | Large legacy projects |

### Step 3: Migrate to Logical Properties

```yaml
migration_map:
  # Margin/Padding
  - physical: "margin-left / ml-*"
    logical: "margin-inline-start / ms-*"
  - physical: "margin-right / mr-*"
    logical: "margin-inline-end / me-*"
  - physical: "padding-left / pl-*"
    logical: "padding-inline-start / ps-*"
  - physical: "padding-right / pr-*"
    logical: "padding-inline-end / pe-*"

  # Position
  - physical: "left: 0"
    logical: "inset-inline-start: 0"
  - physical: "right: 0"
    logical: "inset-inline-end: 0"

  # Text
  - physical: "text-align: left"
    logical: "text-align: start"
  - physical: "text-align: right"
    logical: "text-align: end"

  # Border
  - physical: "border-left"
    logical: "border-inline-start"

  # Size
  - physical: "width / height"
    logical: "inline-size / block-size"  # When directionally relevant
```

### Step 4: Handle Bidirectional Content

```yaml
bidi_patterns:
  mixed_direction_text:
    approach: "Use <bdi> element for user-generated content"
    css: "unicode-bidi: isolate"
  numbers_in_rtl:
    note: "Numbers are always LTR even in RTL context"
    approach: "Use <bdi> or dir='ltr' for number sequences"
  icons_and_arrows:
    mirrored: ["back arrow", "forward arrow", "chevron-left/right", "undo/redo"]
    not_mirrored: ["checkmark", "plus", "close", "search", "clock"]
  transforms:
    flip: "translateX values need sign flip in RTL"
    approach: "Use CSS logical properties or calc with dir-aware multiplier"
```

### Step 5: Component-Level RTL Support

```yaml
component_patterns:
  layout:
    - "Use flexbox/grid (auto-flip with dir attribute)"
    - "Avoid float (doesn't flip)"
  icons:
    - "Use transform: scaleX(-1) for mirrored icons via [dir='rtl'] selector"
    - "Or use separate icon assets per direction"
  forms:
    - "Input text direction: auto (detects content direction)"
    - "Labels: follow document direction"
    - "Validation icons: fixed position (not directional)"
  navigation:
    - "Sidebar: auto-flips with flexbox row-reverse in RTL"
    - "Breadcrumbs: separator direction flips"
    - "Progress indicators: direction-aware"
```

### Step 6: Validate RTL Layout

- [ ] All physical CSS properties migrated to logical equivalents
- [ ] `dir="rtl"` on `<html>` produces correct layout
- [ ] Icons that should mirror do mirror; universal icons don't
- [ ] Numbers display correctly in RTL context
- [ ] Forms work bidirectionally (input direction auto-detected)
- [ ] No overflow or broken layouts in RTL mode

## Quality Criteria

- Zero physical directional CSS properties (all logical)
- Layout flips correctly with `dir="rtl"` attribute
- Mixed-direction content handled with `<bdi>` or `unicode-bidi`
- Icon mirroring rules documented and applied

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Logical properties | Zero physical margin/padding/position |
| Visual flip | Layout mirrors correctly in RTL |
| Icons | Directional icons mirror, universal don't |
| Content | BiDi text renders correctly |

## Handoff

- Logical property migration feeds `@css-eng` for implementation
- Component RTL variants feed `@react-eng` for conditional rendering
- Visual validation feeds `@qa-visual` for RTL screenshot tests
