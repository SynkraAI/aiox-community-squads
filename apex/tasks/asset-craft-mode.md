# Asset Craft Mode — Diana (design-sys-eng)

> **Owner:** design-sys-eng (Diana)
> **Trigger:** `*asset-craft`, `*brand-palette {source}`
> **Dependencies:** `data/asset-viability-matrix.yaml`, `checklists/visual-acceptance-rubric.md`

## Purpose

Diana's specialized mode for brand asset work: palette extraction, geometric mark creation, and brand token validation. This is NOT a general-purpose design tool — it's scoped to token-level brand work that Diana already owns.

## Modes

### Mode 1: Palette Extraction (`*brand-palette {source}`)

**Input:** URL, screenshot, description, or existing brand reference
**Output:** Design tokens (primitive + semantic) for the brand palette

#### Steps

1. **Identify source type**
   - URL → attempt screenshot via Playwright (fallback: ask user for screenshot)
   - Screenshot → analyze colors directly
   - Description → generate palette from text
   - Existing file → extract from CSS/tokens

2. **Extract dominant colors**
   - Identify 5-8 dominant colors from source
   - Classify: primary, secondary, accent, background, surface, text
   - Measure contrast ratios for all text/background combinations

3. **Generate token layers**
   ```yaml
   primitive:
     color.brand.100: "#extracted_light"
     color.brand.500: "#extracted_primary"
     color.brand.900: "#extracted_dark"
   semantic:
     color.accent.emphasis: "{color.brand.500}"
     color.accent.fg: "{color.brand.700}"
     color.accent.subtle: "{color.brand.100}"
   ```

4. **Validate**
   - All contrast ratios >= 4.5:1 (WCAG AA)
   - Light AND dark mode variants generated
   - No hardcoded values — all mapped to tokens

5. **Present to user**
   - Show palette swatch (visual)
   - Show token mapping (code)
   - Options: Apply / Adjust / Export / Done

### Mode 2: Geometric Mark (`*asset-craft`)

**Pre-flight:** Consult `data/asset-viability-matrix.yaml` FIRST.

#### Steps

1. **Run viability check**
   - Score the request across 5 dimensions
   - GREEN (< 2.5) → proceed
   - YELLOW (2.5-3.5) → show caveats, proceed if user confirms
   - RED (> 3.5) → honesty gate: inform limitation, suggest alternatives

2. **If proceeding — gather requirements**
   - What does the mark represent?
   - Geometric style preference (angular, rounded, mixed)?
   - Monochrome or brand colors?
   - Sizes needed (favicon, header, social)?

3. **Create geometric SVG**
   - Build from primitive shapes (circle, rect, path)
   - Align to 4px grid
   - Use `currentColor` for monochrome variant
   - Keep under 10 path segments
   - Ensure viewBox is correct for scaling

4. **Validate against rubric**
   - Run `checklists/visual-acceptance-rubric.md`
   - Score must be >= 18/26
   - All critical items must pass

5. **Present to user**
   - Show SVG inline
   - Show at 3 sizes (16px, 64px, 256px)
   - Options: Accept / Iterate / Simplify / Done

### Mode 3: Brand Token Audit (`*asset-craft` with existing project)

#### Steps

1. **Scan project for brand tokens**
   - Find all color tokens with "brand" or "accent" in name
   - Find logo/icon files (SVG, PNG in public/ or assets/)
   - Find CSS variables with brand-related names

2. **Check coherence**
   - Do logo colors match token values?
   - Are tokens used consistently across components?
   - Any hardcoded brand colors bypassing tokens?

3. **Report**
   - Coherence score (0-100%)
   - Drift list (token vs actual usage)
   - Recommendations (fix token / update logo / consolidate)

## Veto Conditions

| ID | Condition | Block |
|----|-----------|-------|
| VC-CRAFT-001 | Viability check RED zone, user not informed | Cannot proceed |
| VC-CRAFT-002 | Hardcoded hex in output (not tokenized) | Cannot ship |
| VC-CRAFT-003 | No dark mode variant generated | Cannot ship |
| VC-CRAFT-004 | Contrast ratio < 4.5:1 on any text pair | Cannot ship |

## Intent Chain

After completion → `after_asset_check` or `after_asset_pipeline` in `apex-intelligence.yaml`

## What This Task Does NOT Do

- Complex illustrations (delegate to human designer)
- Photo-realistic logos (honesty gate blocks this)
- Typography design / custom fonts
- Full brand identity guides (scope creep)
