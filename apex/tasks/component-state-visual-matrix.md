> **DEPRECATED** — Scope absorbed into `component-design.md`. See `data/task-consolidation-map.yaml`.

# Task: component-state-visual-matrix

```yaml
id: component-state-visual-matrix
version: "1.0.0"
title: "Component State Visual Matrix"
description: >
  Creates exhaustive visual test matrices for component states.
  Maps every visual permutation of a component (variants × states
  × themes × sizes) and generates screenshot tests for the full
  matrix. Catches visual bugs in rarely-tested state combinations
  like "error + disabled + dark mode + mobile". Uses Storybook
  stories or programmatic rendering for complete coverage.
elicit: false
owner: qa-visual
executor: qa-visual
outputs:
  - State enumeration per component
  - Visual permutation matrix
  - Storybook story generation patterns
  - Programmatic screenshot capture patterns
  - Priority-based testing strategy
  - Component state visual specification document
```

---

## When This Task Runs

This task runs when:
- New component has multiple visual states
- Existing component gains new variants/states
- Theme changes need state-level validation
- QA discovers state-specific visual bugs
- `*state-matrix` or `*visual-matrix` is invoked

This task does NOT run when:
- Cross-browser testing (use `cross-browser-validation`)
- Responsive testing (use `responsive-visual-testing`)
- Diff algorithm configuration (use `screenshot-comparison-automation`)

---

## Execution Steps

### Step 1: Enumerate Component States

Map every visual dimension of the component.

**State dimensions:**

| Dimension | Examples |
|-----------|---------|
| **Variant** | primary, secondary, outline, ghost, destructive |
| **Size** | xs, sm, md, lg, xl |
| **State** | default, hover, focus, active, disabled, loading |
| **Content** | empty, short text, long text, with icon, icon-only |
| **Theme** | light, dark |
| **Validation** | none, success, error, warning |
| **Interactive** | selected, checked, expanded, open |

**Example: Button component**
```
Variants:    [primary, secondary, outline, ghost, destructive]  = 5
Sizes:       [sm, md, lg]                                       = 3
States:      [default, hover, focus, disabled, loading]          = 5
Content:     [text, icon+text, icon-only]                       = 3
Themes:      [light, dark]                                      = 2

Total permutations: 5 × 3 × 5 × 3 × 2 = 450
```

**Output:** State enumeration per component.

### Step 2: Build Permutation Matrix

Generate the full matrix with priority filtering.

**Priority levels:**

| Priority | Coverage | When |
|----------|----------|------|
| P0 Critical | variant × state × theme | Always test (30 combos) |
| P1 Important | + size | CI on every PR (90 combos) |
| P2 Complete | + content | Weekly/pre-release (450 combos) |

**Matrix generation:**
```typescript
interface StateMatrix {
  component: string;
  dimensions: Record<string, string[]>;
  priority: 'P0' | 'P1' | 'P2';
}

function generateMatrix(matrix: StateMatrix): Permutation[] {
  const dimensions = Object.entries(matrix.dimensions);
  return cartesianProduct(dimensions.map(([, values]) => values))
    .map(combo => {
      const permutation: Record<string, string> = {};
      dimensions.forEach(([key], i) => { permutation[key] = combo[i]; });
      return permutation;
    });
}

function cartesianProduct(arrays: string[][]): string[][] {
  return arrays.reduce(
    (acc, arr) => acc.flatMap(combo => arr.map(item => [...combo, item])),
    [[]] as string[][]
  );
}
```

**Exclusion rules (reduce noise):**
- Skip `loading + disabled` (mutually exclusive)
- Skip `icon-only + long text` (impossible)
- Skip `ghost + destructive` (if not in design system)

**Output:** Visual permutation matrix.

### Step 3: Storybook Story Generation

Create Storybook stories for the matrix.

**Story template (CSF3):**
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary', 'outline', 'ghost'] },
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
    disabled: { control: 'boolean' },
    loading: { control: 'boolean' },
  },
};
export default meta;

type Story = StoryObj<typeof Button>;

// P0: Critical state combinations
export const PrimaryDefault: Story = {
  args: { variant: 'primary', children: 'Button' },
};

export const PrimaryDisabled: Story = {
  args: { variant: 'primary', children: 'Button', disabled: true },
};

export const PrimaryLoading: Story = {
  args: { variant: 'primary', children: 'Button', loading: true },
};

// Matrix story (all P0 combinations)
export const StateMatrix: Story = {
  render: () => (
    <div className="grid gap-4">
      {['primary', 'secondary', 'outline', 'ghost'].map(variant =>
        ['default', 'disabled'].map(state => (
          <div key={`${variant}-${state}`} className="flex items-center gap-2">
            <span className="w-32 text-sm">{variant} / {state}</span>
            <Button
              variant={variant}
              disabled={state === 'disabled'}
            >
              Button
            </Button>
          </div>
        ))
      )}
    </div>
  ),
};
```

**Grid layout for visual review:**
```tsx
export const FullMatrix: Story = {
  render: () => (
    <table className="border-collapse">
      <thead>
        <tr>
          <th />
          {states.map(s => <th key={s}>{s}</th>)}
        </tr>
      </thead>
      <tbody>
        {variants.map(v => (
          <tr key={v}>
            <td>{v}</td>
            {states.map(s => (
              <td key={s} className="p-2 border">
                <Button variant={v} disabled={s === 'disabled'} loading={s === 'loading'}>
                  Text
                </Button>
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  ),
};
```

**Output:** Storybook story generation patterns.

### Step 4: Programmatic Screenshot Capture

Capture screenshots for the full matrix without Storybook.

**Playwright matrix test:**
```typescript
const variants = ['primary', 'secondary', 'outline', 'ghost'] as const;
const states = ['default', 'hover', 'focus', 'disabled'] as const;
const themes = ['light', 'dark'] as const;

for (const variant of variants) {
  for (const state of states) {
    for (const theme of themes) {
      test(`Button ${variant}/${state}/${theme}`, async ({ page }) => {
        await page.goto(`/test/button?variant=${variant}&state=${state}`);
        await page.emulateMedia({
          colorScheme: theme,
          reducedMotion: 'reduce',
        });

        if (state === 'hover') {
          await page.locator('button').hover();
        } else if (state === 'focus') {
          await page.locator('button').focus();
        }

        await expect(page.locator('button')).toHaveScreenshot(
          `button-${variant}-${state}-${theme}.png`
        );
      });
    }
  }
}
```

**Test page (minimal renderer):**
```tsx
// /test/button — lightweight page that renders component in isolation
function ButtonTestPage() {
  const params = useSearchParams();
  const variant = params.get('variant') || 'primary';
  const state = params.get('state') || 'default';

  return (
    <div className="p-8 flex items-center justify-center min-h-screen">
      <Button
        variant={variant}
        disabled={state === 'disabled'}
        loading={state === 'loading'}
      >
        Button Text
      </Button>
    </div>
  );
}
```

**Output:** Programmatic screenshot capture patterns.

### Step 5: Priority-Based Testing Strategy

Define what runs when.

**Testing tiers:**

| Tier | Scope | When | Duration |
|------|-------|------|----------|
| Smoke | 5 critical combos | Every commit (pre-push) | < 30s |
| PR Gate | P0 matrix (30 combos) | Every PR | < 2min |
| Nightly | P1 matrix (90 combos) | Nightly CI | < 5min |
| Release | P2 full matrix (450 combos) | Pre-release | < 15min |

**Smoke selection criteria:**
- Primary/default/light (happy path)
- Primary/disabled/light (disabled state)
- Primary/default/dark (dark mode)
- Destructive/default/light (danger state)
- Primary/loading/light (loading state)

**Output:** Priority-based testing strategy.

### Step 6: Document State Visual Testing

Compile the complete specification.

**Documentation includes:**
- State enumeration methodology (from Step 1)
- Permutation matrix (from Step 2)
- Storybook patterns (from Step 3)
- Programmatic capture (from Step 4)
- Testing tiers (from Step 5)
- Adding new components to the matrix
- Exclusion rules maintenance

**Output:** Component state visual specification document.

---

## Quality Criteria

- P0 matrix covers every variant × state × theme combination
- Exclusion rules eliminate impossible/redundant combinations
- Screenshot tests deterministic (zero flakiness)
- Matrix auto-updates when component props change
- CI runs P0 in < 2 minutes
- New components get matrix within first PR

---

*Squad Apex — Component State Visual Matrix Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-component-state-visual-matrix
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "P0 matrix covers all critical combinations"
    - "Zero flaky tests in matrix"
    - "Exclusion rules documented"
    - "CI runs P0 in < 2 minutes"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Component state visual matrix with Storybook stories and Playwright tests |
| Next action | Fix visual bugs via `@css-eng` or add missing states via `@react-eng` |
