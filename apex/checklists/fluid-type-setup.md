# Checklist: Fluid Typography Setup

> **Purpose:** One-time setup of a fluid typography system using CSS `clamp()` that scales smoothly between 320px and 2560px viewports. Eliminates font-size media queries.

---

## Prerequisites

- [ ] Project uses CSS custom properties (or can adopt them)
- [ ] Base font size is 16px (1rem)
- [ ] Minimum supported viewport: 320px
- [ ] Maximum supported viewport: 2560px

## Step 1: Define Minimum Sizes (at 320px)

- [ ] Body (base): 16px min (never smaller for readability)
- [ ] Small text: 14px min (captions, labels)
- [ ] H6: 16px | H5: 18px | H4: 20px
- [ ] H3: 24px | H2: 28px | H1: 32px | Display: 36px
- [ ] Verify: no text below 12px under any circumstance
- [ ] Verify: all minimums meet WCAG readability guidelines

## Step 2: Define Maximum Sizes (at 2560px)

- [ ] Body (base): 20px max
- [ ] Small text: 16px
- [ ] H6: 20px | H5: 24px | H4: 30px
- [ ] H3: 38px | H2: 48px | H1: 64px | Display: 80px
- [ ] Verify: each step is clearly distinguishable from adjacent steps
- [ ] Verify: line-height scales appropriately (tighter for headings, looser for body)

## Step 3: Calculate clamp() Values

Formula: `clamp(min-rem, intercept-rem + slope-vw, max-rem)`

Where:
- slope = (max - min) / (2560 - 320)
- intercept = min - slope * 320
- Round slope to 3 decimal places

- [ ] Calculate each step converting px to rem (base 16px)
- [ ] Example: `--font-size-base: clamp(1rem, 0.929rem + 0.357vw, 1.25rem);`

## Step 4: Create CSS Custom Properties

- [ ] Add all `--font-size-*` custom properties to `:root`
- [ ] Add line-height tokens: `--line-height-tight: 1.1`, `--line-height-snug: 1.25`, `--line-height-normal: 1.5`, `--line-height-relaxed: 1.625`
- [ ] Add letter-spacing adjustments for headings (tighter at larger sizes)
- [ ] Add font-weight mappings if using variable fonts

## Step 5: Test at Viewport Extremes

- [ ] 320px: all text readable, hierarchy clear
- [ ] 768px: smooth fluid scaling
- [ ] 1440px: comfortable desktop sizes
- [ ] 2560px: nothing oversized, hierarchy works
- [ ] 4K (3840px): clamp() caps at maximum (no runaway growth)
- [ ] Body text comfortable in 60-75 character line widths
- [ ] No text overlaps or breaks layout at any size

## Step 6: Document the Scale

- [ ] Visual preview at min, preferred, and max sizes
- [ ] Usage guide: which custom property for each context
- [ ] Integration instructions for existing components
- [ ] How to extend the scale if new steps are needed
- [ ] Explanation of the clamp() formula for future maintenance

## Quality Gate

- [ ] All clamp() values are mathematically correct
- [ ] No font size renders below 12px at any viewport
- [ ] Body text is at least 16px at 320px
- [ ] Scale is usable with a single custom property per element (no media queries needed)
- [ ] Line heights are appropriate for each scale step

---

*Converted from `tasks/fluid-type-setup.md` — Squad Apex v1.0.0*
