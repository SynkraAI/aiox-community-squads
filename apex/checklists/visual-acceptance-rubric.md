# Visual Acceptance Rubric — Asset Quality Gate

> **Purpose:** Objective, measurable criteria for approving visual assets (logos, icons, brand marks). Eliminates subjective "looks good" approvals with quantifiable checks.
>
> **Gate:** QG-AX-ASSET (see `data/veto-conditions.yaml`)
> **Used by:** apex-lead (final review), design-sys-eng (asset craft mode)

## Scoring

Each criterion scores 0 (fail), 1 (partial), or 2 (pass). **Minimum to ship: 18/26 (70%).**
Critical items (marked **[C]**) must ALL score >= 1 or asset is blocked.

---

## 1. Geometric Fidelity (max 6)

| # | Criterion | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 1.1 **[C]** | Grid alignment | Elements off-grid | Most on 4px grid | All on 4px grid |
| 1.2 | Symmetry | Visibly asymmetric (unintended) | Minor asymmetry | Perfect symmetry or intentional asymmetry |
| 1.3 | Simplicity | > 20 SVG path segments | 10-20 segments | < 10 segments |

## 2. Scalability (max 6)

| # | Criterion | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 2.1 **[C]** | Minimum size | Unrecognizable at 16px | Recognizable at 16px | Clear at 16px |
| 2.2 | Maximum size | Artifacts at 512px | Minor artifacts at 512px | Clean at 512px |
| 2.3 | Aspect ratio | Distorts on resize | Slight distortion | viewBox correct, no distortion |

## 3. Token Compliance (max 6)

| # | Criterion | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 3.1 **[C]** | Color source | Hardcoded hex values | Mix of tokens + hardcoded | All colors from design tokens |
| 3.2 | Dark mode | Broken in dark mode | Partially works | Full dark mode support |
| 3.3 | currentColor | No currentColor support | Partial | Uses currentColor for monochrome variant |

## 4. Brand Coherence (max 6)

| # | Criterion | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 4.1 | Palette match | Colors don't match brand | Close match (< 10% HSL delta) | Exact match (< 2% HSL delta) |
| 4.2 | Style consistency | Doesn't match existing assets | Partially consistent | Indistinguishable from existing assets |
| 4.3 | Weight balance | Visually unbalanced | Minor imbalance | Optically balanced |

## 5. Technical Quality (max 4)

| # | Criterion | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 5.1 **[C]** | SVG validity | Invalid SVG / raster fallback | Valid with warnings | Valid, optimized, no redundant nodes |
| 5.2 | File size | > 10KB | 5-10KB | < 5KB |

---

## Verdict Table

| Score | Verdict | Action |
|-------|---------|--------|
| 22-26 | **SHIP** | Asset approved, integrate into project |
| 18-21 | **POLISH** | Minor fixes needed, re-score after |
| 14-17 | **REWORK** | Significant issues, iterate on approach |
| 0-13 | **REJECT** | Does not meet quality bar, start over or use alternative |

## Critical Gate

If ANY **[C]** criterion scores 0 → **BLOCKED** regardless of total score.

Critical items:
- 1.1: Grid alignment
- 2.1: Minimum size legibility
- 3.1: Color token compliance
- 5.1: SVG validity

## Usage

```
After *asset-pipeline or *asset-craft completes:
1. Run rubric against output
2. Score each criterion (0/1/2)
3. Check critical items first
4. Calculate total
5. Apply verdict
6. If POLISH or REWORK → iterate → re-score
```
