> **DEPRECATED** — Scope absorbed into `visual-regression-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: screenshot-comparison-automation

```yaml
id: screenshot-comparison-automation
version: "1.0.0"
title: "Screenshot Comparison Automation"
description: >
  Automates pixel-level and perceptual screenshot comparison for
  visual regression detection. Configures diff algorithms (pixel,
  perceptual, structural), threshold tuning, anti-aliasing handling,
  baseline management, and CI integration. Produces actionable diff
  reports with highlighted regions, not just pass/fail verdicts.
elicit: false
owner: qa-visual
executor: qa-visual
outputs:
  - Comparison algorithm selection guide
  - Threshold tuning configuration
  - Baseline management workflow
  - Diff report format specification
  - CI integration patterns
  - Screenshot comparison specification document
```

---

## When This Task Runs

This task runs when:
- Visual regression infrastructure needs diff algorithm tuning
- False positives/negatives in screenshot comparisons
- Baseline images need management strategy (update, review, approve)
- CI pipeline needs visual diff reporting
- `*screenshot-compare` or `*diff-automation` is invoked

This task does NOT run when:
- Initial visual regression setup (use `visual-regression-setup`)
- Cross-browser testing (use `cross-browser-validation`)
- Theme testing (use `theme-visual-testing`)

---

## Execution Steps

### Step 1: Select Comparison Algorithm

Choose the right diff algorithm for the project.

**Algorithm comparison:**

| Algorithm | How It Works | False Positives | Speed | Best For |
|-----------|-------------|-----------------|-------|----------|
| Pixel-by-pixel | Compare each pixel RGB | High (AA, subpixel) | Fast | Exact match needed |
| Perceptual (SSIM) | Structural similarity index | Low | Medium | General UI testing |
| Anti-aliased aware | Ignore AA boundary pixels | Very low | Medium | Cross-platform |
| Region-based | Compare defined regions | Lowest | Slow | Complex layouts |

**Recommended default:** Perceptual (SSIM) with anti-aliasing tolerance.

**Playwright visual comparison:**
```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,  // 1% pixel tolerance
      threshold: 0.2,           // Per-pixel color threshold (0-1)
      animations: 'disabled',   // Freeze animations for consistency
    },
  },
});
```

**Custom comparison with pixelmatch:**
```typescript
import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';

function compareScreenshots(baseline: Buffer, current: Buffer) {
  const img1 = PNG.sync.read(baseline);
  const img2 = PNG.sync.read(current);
  const { width, height } = img1;
  const diff = new PNG({ width, height });

  const mismatchCount = pixelmatch(
    img1.data, img2.data, diff.data,
    width, height,
    {
      threshold: 0.1,          // Color distance threshold
      includeAA: false,        // Ignore anti-aliasing
      alpha: 0.1,              // Background opacity in diff
      diffColor: [255, 0, 0],  // Highlight color for diffs
      diffMask: false,         // Full image with highlights
    }
  );

  const diffPercent = (mismatchCount / (width * height)) * 100;
  return { mismatchCount, diffPercent, diffImage: PNG.sync.write(diff) };
}
```

**Output:** Comparison algorithm selection guide.

### Step 2: Tune Thresholds

Configure thresholds per component type.

**Threshold strategy:**

| Component Type | Pixel Ratio | Color Threshold | Rationale |
|---------------|-------------|-----------------|-----------|
| Icons/logos | 0.001 (0.1%) | 0.05 | Pixel-perfect expected |
| Text content | 0.02 (2%) | 0.15 | Font rendering varies |
| Gradients/shadows | 0.03 (3%) | 0.2 | Sub-pixel rendering |
| Animations (frozen) | 0.05 (5%) | 0.25 | Timing micro-variations |
| Full page | 0.01 (1%) | 0.15 | Balanced default |

**Dynamic viewport thresholds:**

| Viewport | Additional Tolerance | Reason |
|----------|---------------------|--------|
| Desktop 1920px | Baseline (0%) | Reference viewport |
| Tablet 768px | +0.5% | Layout reflow |
| Mobile 375px | +1% | More layout variation |

**Configuration file:**
```json
{
  "comparison": {
    "defaultThreshold": 0.15,
    "defaultMaxDiffPixelRatio": 0.01,
    "componentOverrides": {
      "icons": { "maxDiffPixelRatio": 0.001 },
      "text-heavy": { "maxDiffPixelRatio": 0.02 },
      "gradients": { "threshold": 0.2, "maxDiffPixelRatio": 0.03 }
    },
    "viewportOverrides": {
      "375": { "maxDiffPixelRatio": 0.02 },
      "768": { "maxDiffPixelRatio": 0.015 }
    }
  }
}
```

**Output:** Threshold tuning configuration.

### Step 3: Design Baseline Management

Workflow for maintaining baseline screenshots.

**Baseline lifecycle:**

```
1. Capture   → New baseline created (first run or explicit update)
2. Compare   → Current vs baseline comparison
3. Review    → Human reviews diff (if threshold exceeded)
4. Approve   → Baseline updated to new version
5. Reject    → Fix code, re-run test
```

**Baseline storage:**

| Option | Pros | Cons |
|--------|------|------|
| Git (in repo) | Versioned, reviewable in PR | Repo size grows |
| Git LFS | Versioned, repo stays small | LFS setup needed |
| Cloud storage (S3) | No repo impact | Extra infra, no PR preview |
| Chromatic/Percy | Managed service, built-in review | Cost per snapshot |

**Recommended:** Git LFS for baselines < 500, cloud for larger projects.

**Update workflow:**
```bash
# Update specific baseline
npx playwright test --update-snapshots tests/header.spec.ts

# Update all baselines (after intentional redesign)
npx playwright test --update-snapshots

# Review changes in PR
# → Diff images appear as changed files
# → Reviewer approves or requests changes
```

**Branch strategy:**
- Baselines on `main` are source of truth
- Feature branches compare against `main` baselines
- Baseline updates require PR review
- Never auto-update baselines in CI

**Output:** Baseline management workflow.

### Step 4: Design Diff Report Format

Create actionable visual diff reports.

**Report structure:**
```
┌─────────────────────────────────────────┐
│ Visual Regression Report                │
│ Date: 2026-03-11 | Branch: feat/header  │
│ Total: 24 | Pass: 21 | Fail: 3          │
├─────────────────────────────────────────┤
│                                         │
│ ❌ Header.tsx @ 375px                    │
│ Diff: 4.2% (threshold: 1%)             │
│ ┌─────────┬─────────┬─────────┐        │
│ │Baseline │ Current │  Diff   │        │
│ │  [img]  │  [img]  │  [img]  │        │
│ └─────────┴─────────┴─────────┘        │
│ Highlighted regions: nav overflow,      │
│   CTA button position shift             │
│                                         │
│ ❌ Footer.tsx @ 1920px                   │
│ Diff: 2.1% (threshold: 1%)             │
│ ...                                     │
└─────────────────────────────────────────┘
```

**Report formats:**
- HTML (interactive, zoom, toggle overlay)
- JSON (CI consumption, automated processing)
- Markdown (PR comment integration)

**Playwright HTML reporter:**
```typescript
// Custom reporter that generates visual diff HTML
class VisualDiffReporter {
  onTestEnd(test, result) {
    if (result.status === 'failed') {
      const attachments = result.attachments.filter(
        a => a.name.includes('diff') || a.name.includes('actual')
      );
      this.addToReport(test.title, attachments);
    }
  }
}
```

**Output:** Diff report format specification.

### Step 5: CI Integration

Integrate screenshot comparison into CI pipeline.

**GitHub Actions workflow:**
```yaml
visual-regression:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npx playwright install --with-deps chromium

    - name: Run visual tests
      run: npx playwright test --project=visual

    - name: Upload diff report
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: visual-diff-report
        path: test-results/

    - name: Comment on PR
      if: failure() && github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          github.rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.issue.number,
            body: '❌ Visual regression detected. See [diff report](link).'
          });
```

**CI considerations:**
- Use Docker for consistent rendering (same fonts, AA)
- Pin browser version (Chromium snapshot)
- Disable animations before capture
- Set explicit viewport and DPR
- Run on Linux only (cross-OS rendering differs)

**Output:** CI integration patterns.

### Step 6: Document Comparison Architecture

Compile the complete specification.

**Documentation includes:**
- Algorithm guide (from Step 1)
- Threshold config (from Step 2)
- Baseline management (from Step 3)
- Report format (from Step 4)
- CI integration (from Step 5)
- Troubleshooting (false positives, flaky tests)
- Performance notes (parallel execution, sharding)

**Output:** Screenshot comparison specification document.

---

## Quality Criteria

- False positive rate < 2% across all components
- Diff reports show highlighted regions (not just pass/fail)
- Baseline updates require human review
- CI runs complete in < 5 minutes for 100 screenshots
- Cross-platform rendering differences handled by AA tolerance
- Report is actionable (developer knows exactly what changed)

---

*Squad Apex — Screenshot Comparison Automation Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-screenshot-comparison-automation
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "False positive rate < 2%"
    - "Diff reports show highlighted regions"
    - "Baselines require human review"
    - "CI integration functional"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@devops` or `@apex-lead` |
| Artifact | Screenshot comparison pipeline with algorithms, thresholds, and CI integration |
| Next action | Integrate into CI via `@devops` or run audit via `@qa-visual` visual-regression-audit |
