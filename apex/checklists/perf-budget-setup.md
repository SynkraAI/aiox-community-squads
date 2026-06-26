# Checklist: Performance Budget Setup

> **Purpose:** One-time setup of performance budget monitoring. Define budgets per metric, configure Lighthouse CI, set up bundle size monitoring, configure RUM, and define violation thresholds.

---

## Prerequisites

- [ ] Project has a build step that produces measurable bundles
- [ ] CI/CD pipeline exists
- [ ] Decision on RUM approach: web-vitals library / GA4 / Datadog / other

## Step 1: Define Performance Budgets

### Core Web Vitals

| Metric | Budget | Google "Good" |
|--------|--------|---------------|
| LCP | < 2.5s | < 2.5s |
| INP | < 200ms | < 200ms |
| CLS | < 0.1 | < 0.1 |

- [ ] Core Web Vitals budgets defined

### Resource Budgets

| Resource | Budget |
|----------|--------|
| Total JS (initial, gzipped) | < 100KB |
| Total JS (all, gzipped) | < 250KB |
| Total CSS (gzipped) | < 50KB |
| Total images (above fold) | < 200KB |
| Total page weight | < 1MB |
| Largest JS chunk | < 60KB |
| Third-party JS | < 80KB |
| Web fonts | < 100KB |

- [ ] Resource budgets defined (adjust values per project needs)

### Timing Budgets

| Metric | Budget |
|--------|--------|
| TTFB | < 600ms |
| FCP | < 1.8s |
| TTI | < 3.5s |
| TBT | < 200ms |

- [ ] Timing budgets defined

### Per-Route Budgets (SPAs)

- [ ] Critical routes identified with individual JS and LCP budgets
- [ ] Homepage has strictest budget

## Step 2: Configure Lighthouse CI

- [ ] Install: `npm install -g @lhci/cli`
- [ ] Create `lighthouserc.js` with:
  - URLs to test (at least homepage + critical routes)
  - `numberOfRuns: 3` (median for stability)
  - Assertions: `categories:performance >= 0.9`, LCP error at 2500, CLS error at 0.1, TBT error at 200
  - Upload target configured (temporary-public-storage or self-hosted)
- [ ] CI step added: `lhci autorun`
- [ ] `error` assertions block merge, `warn` assertions show warnings only

## Step 3: Set Up Bundle Size Monitoring

Choose one tool:
- **size-limit**: `npm install --save-dev size-limit @size-limit/preset-app`
- **bundlewatch**: `npm install --save-dev bundlewatch`

- [ ] Config file created with per-chunk budgets
- [ ] Compression set to gzip
- [ ] CI step added: `npx size-limit` (or `npx bundlewatch`)
- [ ] PR comment bot configured to show bundle size diff

## Step 4: Configure Real User Monitoring (RUM)

- [ ] Install `web-vitals`: `npm install web-vitals`
- [ ] Register all CWV metrics: `onLCP`, `onINP`, `onCLS`, `onFCP`, `onTTFB`
- [ ] Send metrics to analytics endpoint (sendBeacon recommended)
- [ ] Include context: page path, connection type, device memory
- [ ] Track p75 (75th percentile — Google's ranking metric)
- [ ] Segment by: route, device type, connection speed

## Step 5: Define Violation Thresholds

| Level | Condition | Action |
|-------|-----------|--------|
| Green | Within budget | No action |
| Yellow (Warning) | Within 10% of budget | Add to tech debt backlog |
| Orange (Approaching) | Within 5% of budget | Must address this sprint |
| Red (Violation) | Exceeds budget | Blocks deployment |

- [ ] Threshold levels defined for each metric
- [ ] CI failures post to team channel
- [ ] RUM threshold violations trigger alerts
- [ ] Weekly performance digest configured

## Step 6: Document Escalation Process

- [ ] Escalation flow documented:
  1. CI check fails → PR author notified
  2. Author reviews report → can fix? → fix and re-push
  3. Cannot fix → @perf-eng reviews
  4. @perf-eng determines: fix guidance / budget adjustment / architecture escalation
  5. Resolution documented in PR
- [ ] Budget exception process defined (document why, @perf-eng approves, follow-up optimization task created)
- [ ] Weekly review cadence established (RUM trends, lab vs field data, approaching thresholds)

## Quality Gate

- [ ] Budgets defined for all 3 Core Web Vitals (LCP, INP, CLS)
- [ ] Resource budgets include JS, CSS, images, total page weight
- [ ] Lighthouse CI runs on every PR and blocks on violations
- [ ] Bundle size tracked per chunk, not just total
- [ ] RUM collects and segments data by route and device type
- [ ] Escalation process has clear owner at each step

---

*Converted from `tasks/perf-budget-setup.md` — Squad Apex v1.0.0*
