> **DEPRECATED** — Scope absorbed into `visual-regression-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: responsive-visual-testing

```yaml
id: responsive-visual-testing
version: "1.0.0"
title: "Responsive Visual Testing"
description: >
  Designs and implements visual testing across multiple viewports,
  device pixel ratios, and orientations. Covers breakpoint-specific
  screenshot capture, viewport matrix configuration, responsive
  layout validation, mobile/tablet/desktop coverage, and
  orientation change testing. Ensures visual consistency across
  the entire responsive spectrum.
elicit: false
owner: qa-visual
executor: qa-visual
outputs:
  - Viewport matrix (breakpoints × DPR × orientation)
  - Responsive test suite configuration
  - Breakpoint-specific test patterns
  - Orientation change validation patterns
  - Responsive visual testing specification document
```

---

## When This Task Runs

This task runs when:
- Responsive design implementation needs visual validation
- New breakpoints are added to the design system
- Mobile-specific layouts need screenshot testing
- Orientation change behavior needs validation
- `*responsive-test` or `*viewport-test` is invoked

This task does NOT run when:
- Setting up visual regression infrastructure (use `visual-regression-setup`)
- Configuring diff algorithms (use `screenshot-comparison-automation`)
- Cross-browser testing (use `cross-browser-validation`)

---

## Execution Steps

### Step 1: Define Viewport Matrix

Map all viewport combinations to test.

**Standard breakpoints:**

| Name | Width | Device Class | Priority |
|------|-------|-------------|----------|
| Mobile S | 320px | iPhone SE | HIGH |
| Mobile M | 375px | iPhone 14 | HIGH |
| Mobile L | 428px | iPhone 14 Pro Max | MEDIUM |
| Tablet Portrait | 768px | iPad | HIGH |
| Tablet Landscape | 1024px | iPad landscape | MEDIUM |
| Desktop | 1280px | Laptop | HIGH |
| Desktop L | 1440px | External monitor | MEDIUM |
| Desktop XL | 1920px | Full HD | HIGH |
| Ultrawide | 2560px | Ultrawide monitor | LOW |

**Device Pixel Ratios (DPR):**

| DPR | Devices | Test Priority |
|-----|---------|---------------|
| 1x | Desktop monitors, older devices | HIGH |
| 2x | Retina Mac, iPhone, modern Android | HIGH |
| 3x | iPhone Pro, Galaxy S series | MEDIUM |

**Test matrix (breakpoints × DPR):**
```
Priority matrix = breakpoints.HIGH × DPR.HIGH
  = [320, 375, 768, 1280, 1920] × [1x, 2x]
  = 10 core combinations

Full matrix = all breakpoints × all DPRs
  = 9 × 3 = 27 combinations (too many for CI)
```

**Recommended CI matrix:** 10 core combinations (HIGH × HIGH).

**Output:** Viewport matrix.

### Step 2: Configure Responsive Test Suite

Set up Playwright projects for each viewport.

**Playwright configuration:**
```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // Mobile
    {
      name: 'mobile-320',
      use: { viewport: { width: 320, height: 568 }, deviceScaleFactor: 2 },
    },
    {
      name: 'mobile-375',
      use: { viewport: { width: 375, height: 812 }, deviceScaleFactor: 3 },
    },
    // Tablet
    {
      name: 'tablet-768',
      use: { viewport: { width: 768, height: 1024 }, deviceScaleFactor: 2 },
    },
    {
      name: 'tablet-1024-landscape',
      use: { viewport: { width: 1024, height: 768 }, deviceScaleFactor: 2 },
    },
    // Desktop
    {
      name: 'desktop-1280',
      use: { viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 },
    },
    {
      name: 'desktop-1920',
      use: { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 },
    },
  ],
});
```

**Test file pattern:**
```typescript
// tests/visual/header.visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Header responsive', () => {
  test('renders correctly', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Disable animations for consistent screenshots
    await page.emulateMedia({ reducedMotion: 'reduce' });

    await expect(page).toHaveScreenshot('header.png', {
      fullPage: false,
      clip: { x: 0, y: 0, width: page.viewportSize()!.width, height: 80 },
    });
  });
});
```

**Output:** Responsive test suite configuration.

### Step 3: Breakpoint-Specific Tests

Write tests that validate layout behavior at breakpoints.

**Critical transitions to test:**

| Transition | From | To | What Changes |
|-----------|------|-----|-------------|
| Desktop → Tablet | 1280px | 768px | Grid cols 3→2, sidebar collapses |
| Tablet → Mobile | 768px | 375px | Stack layout, hamburger menu |
| Mobile S edge | 375px | 320px | Text wrapping, overflow |

**Breakpoint transition test:**
```typescript
test('navigation collapses to hamburger on mobile', async ({ page }) => {
  // Desktop: nav links visible
  await page.setViewportSize({ width: 1280, height: 800 });
  await expect(page.locator('nav a')).toBeVisible();
  await expect(page.locator('[data-testid="hamburger"]')).not.toBeVisible();

  // Mobile: nav links hidden, hamburger visible
  await page.setViewportSize({ width: 375, height: 812 });
  await expect(page.locator('nav a')).not.toBeVisible();
  await expect(page.locator('[data-testid="hamburger"]')).toBeVisible();
});
```

**Content overflow tests:**
```typescript
test('no horizontal overflow on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 568 });
  await page.goto('/');

  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);

  expect(scrollWidth).toBeLessThanOrEqual(clientWidth);
});
```

**Text truncation tests:**
```typescript
test('long text truncates properly on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 568 });

  const card = page.locator('.card-title').first();
  const box = await card.boundingBox();
  expect(box!.width).toBeLessThanOrEqual(280); // 320 - padding
});
```

**Output:** Breakpoint-specific test patterns.

### Step 4: Orientation Change Testing

Validate layout behavior during orientation changes.

**Orientation scenarios:**

| Scenario | From | To | Issues |
|----------|------|-----|--------|
| Portrait → Landscape | 375×812 | 812×375 | Layout reflow, fixed elements |
| Landscape → Portrait | 812×375 | 375×812 | Scroll position, form state |
| Tablet rotation | 768×1024 | 1024×768 | Grid reflow |

**Orientation test:**
```typescript
test('layout adapts to orientation change', async ({ page }) => {
  // Portrait
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/');
  await expect(page).toHaveScreenshot('portrait.png');

  // Landscape
  await page.setViewportSize({ width: 812, height: 375 });
  await page.waitForTimeout(300); // Allow layout to reflow
  await expect(page).toHaveScreenshot('landscape.png');

  // Validate no overflow
  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(scrollWidth).toBeLessThanOrEqual(812);
});
```

**Orientation-specific issues to test:**
- Fixed/sticky elements repositioning
- Viewport height changes (100vh → shorter)
- Keyboard dismissal after rotation
- Form state preservation during rotation
- Modal/overlay resizing

**Output:** Orientation change validation patterns.

### Step 5: Document Responsive Visual Testing

Compile the complete specification.

**Documentation includes:**
- Viewport matrix (from Step 1)
- Test suite config (from Step 2)
- Breakpoint tests (from Step 3)
- Orientation tests (from Step 4)
- CI sharding strategy (parallel viewport testing)
- Debugging flaky responsive tests
- Threshold tuning per viewport

**Output:** Responsive visual testing specification document.

---

## Quality Criteria

- All HIGH priority viewport combinations tested in CI
- Zero horizontal overflow on any viewport
- Breakpoint transitions produce correct layout changes
- Orientation changes preserve content and functionality
- CI runs complete in < 5 minutes with sharding
- False positive rate < 2% across all viewports

---

*Squad Apex — Responsive Visual Testing Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-responsive-visual-testing
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "HIGH priority viewports all tested"
    - "Zero horizontal overflow"
    - "Orientation change tests pass"
    - "False positive rate < 2%"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@css-eng` or `@apex-lead` |
| Artifact | Responsive visual test suite with viewport matrix and breakpoint tests |
| Next action | Fix responsive issues via `@css-eng` or integrate into CI via `@devops` |
