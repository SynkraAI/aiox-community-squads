# Checklist: Visual Regression Testing Setup

> **Purpose:** One-time setup of visual regression testing infrastructure. Select tooling, capture baselines, define viewports, integrate with CI, and configure pixel-diff thresholds.

---

## Prerequisites

- [ ] Project has a running dev server or build output
- [ ] CI/CD pipeline exists (GitHub Actions, GitLab CI, etc.)
- [ ] Decision: using Storybook? `{YES/NO}` (affects tool choice)

## Step 1: Choose Tool

| Tool | Best For | Cost |
|------|----------|------|
| **Playwright Screenshots** | Budget-conscious, full control | Free |
| **Chromatic** | Storybook-based projects, team review UI | Free tier (5K snapshots/mo) |
| **Percy** | Cross-browser visual testing | Paid |
| **BackstopJS** | Simple URL-based testing | Free |

Decision criteria:
- [ ] If using Storybook → Chromatic (best integration)
- [ ] If budget-constrained → Playwright screenshots
- [ ] If cross-browser critical → Percy
- [ ] Document chosen tool and rationale

## Step 2: Configure Baseline Capture

- [ ] List pages/components to capture baselines for
- [ ] Disable animations during capture (`animations: 'disabled'`)
- [ ] Wait for fonts and images to fully load
- [ ] Mask dynamic content (timestamps, avatars, ads)
- [ ] Set fixed system date for date-dependent content
- [ ] Generate initial baseline screenshots
- [ ] Commit baselines to repository (e.g., `__screenshots__/` directory)

## Step 3: Define Viewports

Minimum viewport set (for faster CI):

| Name | Width | Height | Represents |
|------|-------|--------|------------|
| mobile | 375px | 812px | iPhone 13/14 |
| tablet | 768px | 1024px | iPad |
| desktop | 1440px | 900px | Common desktop |

Extended set (if needed):
- [ ] mobile-landscape: 812x375
- [ ] desktop-fhd: 1920x1080
- [ ] desktop-wide: 2560x1440

- [ ] Configure viewports in test runner config (Playwright projects, Chromatic viewports, etc.)

## Step 4: Set Up CI Integration

- [ ] Visual regression tests run on every pull request
- [ ] Install browsers in CI (e.g., `npx playwright install --with-deps chromium`)
- [ ] Build application before running tests
- [ ] Start server and wait for it to be ready
- [ ] Upload diff artifacts on failure (retention: 7 days)
- [ ] Baseline management: require human review for baseline updates
- [ ] NEVER auto-update baselines — always require manual `--update-snapshots`

## Step 5: Configure Pixel-Diff Threshold

| Strictness | maxDiffPixelRatio | threshold | Use For |
|-----------|-------------------|-----------|---------|
| Strict | 0 | 0.1 | Design system components |
| Standard | 0.001 (0.1%) | 0.2 | Full pages |
| Relaxed | 0.01 (1%) | 0.3 | Pages with dynamic content |

- [ ] Choose threshold per test category
- [ ] Set `threshold: 0.2` to account for anti-aliasing differences across environments
- [ ] Mask dynamic content selectors to prevent false failures

## Step 6: Document Workflow

Developer workflow:
1. Make changes
2. Run visual tests locally
3. If tests fail: review diff → intentional? update baseline : fix regression
4. Commit code + updated baselines
5. CI runs visual tests on PR
6. Reviewer verifies baseline changes are intentional

- [ ] Workflow documented and shared with team
- [ ] Baseline update process documented (never update just to "make tests pass")
- [ ] Stale baseline refresh process defined

## Quality Gate

- [ ] Baselines captured at minimum 3 viewport sizes
- [ ] Animations disabled during capture
- [ ] CI runs visual tests on every PR
- [ ] Threshold strict enough to catch regressions, not cause false positives
- [ ] Baseline updates require human review before merging
- [ ] Dynamic content is masked

---

*Converted from `tasks/visual-regression-setup.md` — Squad Apex v1.0.0*
