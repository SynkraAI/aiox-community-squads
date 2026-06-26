# Template: Figma Sync Setup

> **Purpose:** One-time bootstrap of the Figma-to-code token sync pipeline using Style Dictionary. Fill in the placeholders (`{PLACEHOLDER}`) for your project.

---

## Prerequisites

- [ ] Figma file URL: `{FIGMA_FILE_URL}`
- [ ] Figma Personal Access Token generated (for API method)
- [ ] Node.js 18+ installed
- [ ] `style-dictionary` installed: `npm install --save-dev style-dictionary`

---

## Step 1: Structure Figma Variables

Organize variables into collections:

| Collection | Contents | Example |
|-----------|----------|---------|
| **Primitives** | Raw scales | `color/blue/500`, `spacing/4` |
| **Semantic** | Purpose-driven | `color/bg/default`, `color/text/muted` |
| **Component** | Component-scoped | `button/bg/primary`, `input/border/default` |

Modes per collection:
- [ ] Light mode (default)
- [ ] Dark mode
- [ ] High-contrast mode (if needed): `{YES/NO}`
- [ ] Dark high-contrast mode (if needed): `{YES/NO}`

Naming convention in Figma: use `/` as separator (e.g., `color/bg/default`)

- [ ] All variables have values for ALL modes (no unset values)
- [ ] Variable structure documented

## Step 2: Configure Export Method

Choose one:

### Option A: Figma REST API (recommended)

- [ ] API endpoint: `GET /v1/files/{FIGMA_FILE_KEY}/variables/local`
- [ ] Create fetch script at: `{PROJECT_ROOT}/tools/figma-sync/fetch-tokens.ts`
- [ ] Script normalizes API response to Style Dictionary JSON format:

```json
{
  "color": {
    "bg": {
      "default": {
        "$value": "{VALUE}",
        "$type": "color",
        "$description": "{DESCRIPTION}"
      }
    }
  }
}
```

### Option B: Tokens Studio Plugin

- [ ] Plugin installed in Figma file
- [ ] Sync target configured: `{GITHUB_REPO_OR_JSON_PATH}`
- [ ] Token format matches Style Dictionary input
- [ ] Push/pull behavior: `{MANUAL/AUTO}`

## Step 3: Style Dictionary Configuration

Create config at `{PROJECT_ROOT}/tokens/config.js`:

```javascript
module.exports = {
  source: ['tokens/input/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'tokens/output/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables',
        options: { outputReferences: true }
      }]
    },
    ts: {
      transformGroup: 'js',
      buildPath: 'tokens/output/ts/',
      files: [{
        destination: 'tokens.ts',
        format: 'javascript/es6'
      }]
    }
  }
};
```

- [ ] Custom name transform configured: `/` to `-` for CSS, `/` to `.` for JS
- [ ] Mode transform: per-mode files or `data-attribute` selectors
- [ ] Build script added to package.json: `"tokens:build": "style-dictionary build"`
- [ ] Pipeline tested with sample token data

## Step 4: CI Build Step

Add to CI config (e.g., `.github/workflows/tokens.yml`):

```yaml
tokens:
  runs-on: ubuntu-latest
  steps:
    - name: Fetch tokens from Figma
      run: npm run tokens:fetch
    - name: Build token artifacts
      run: npm run tokens:build
    - name: Check for drift
      run: npm run tokens:drift-check
```

Triggers:
- [ ] On push: when files in `tokens/` change
- [ ] On schedule: `{CRON_SCHEDULE}` (e.g., daily drift check)
- [ ] On manual dispatch
- [ ] Build failure blocks PR merge
- [ ] Drift detected creates issue or PR comment
- [ ] Coordinated with `@devops` for pipeline integration

## Step 5: Drift Detection

Create script at `{PROJECT_ROOT}/tools/figma-sync/drift-check.ts`:

Detects:
- **Added** — token in Figma but not in code
- **Removed** — token in code but not in Figma
- **Changed** — value differs between Figma and code
- **Missing mode** — mode value exists in Figma but not in code

- [ ] Script compares Figma API response vs committed JSON files
- [ ] Drift report generated in markdown format
- [ ] Alerting configured: CI comment on PR if drift detected
- [ ] Thresholds set:
  - Semantic + component tokens: 0 drift (strict)
  - Primitive tokens: allowed drift during active design iteration

## Maintenance Workflow

Once set up:
1. Designers update Figma Variables and notify team
2. CI fetches, transforms, and commits updated token files
3. Drift detection runs on schedule to catch manual code changes
4. `@design-sys-eng` reviews and resolves drift reports

---

*Converted from `tasks/figma-sync-setup.md` — Squad Apex v1.0.0*
