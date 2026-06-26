> **DEPRECATED** — Scope absorbed into `accessibility-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: touch-target-audit

```yaml
id: touch-target-audit
version: "1.0.0"
title: "Touch Target Audit"
description: >
  Audits and fixes touch/click target sizes across the application.
  Validates against WCAG 2.2 SC 2.5.8 (Target Size Minimum: 24x24px)
  and SC 2.5.5 (Target Size Enhanced: 44x44px). Covers buttons, links,
  form controls, icon buttons, close buttons, and mobile-specific
  interactions. Ensures adequate spacing between adjacent targets.
elicit: false
owner: a11y-eng
executor: a11y-eng
outputs:
  - Touch target inventory (all interactive elements)
  - Size compliance report (24px minimum / 44px enhanced)
  - Spacing analysis (adjacent target overlap)
  - Mobile-specific target audit
  - Fix recommendations per component
  - Touch target specification document
```

---

## When This Task Runs

This task runs when:
- Mobile UI development or responsive design
- Accessibility audit flags small touch targets
- New interactive components are added
- Icon-only buttons are created
- Dense UI patterns need target validation (tables, lists, toolbars)
- `*touch-target` or `*target-audit` is invoked

This task does NOT run when:
- Keyboard navigation (use `keyboard-navigation-patterns`)
- Focus indicator styling (use `focus-management-design`)
- Color contrast (use `color-contrast-automation`)

---

## Execution Steps

### Step 1: Inventory All Interactive Elements

Scan the codebase for every clickable/tappable element.

**Elements to inventory:**

| Element Type | Examples |
|-------------|---------|
| Buttons | `<button>`, `<input type="submit">` |
| Links | `<a href>`, `<Link>` |
| Icon buttons | Close (×), menu (☰), actions |
| Form controls | Checkboxes, radio buttons, switches |
| Select/dropdown | Trigger elements |
| Tabs | Tab buttons in tab lists |
| List items | Clickable rows/cards |
| Nav items | Mobile navigation links |
| Custom interactive | `onClick` on `<div>`, `<span>` |

**For each element, record:**
- Component and file path
- Rendered size (width × height)
- Padding contributing to target area
- Adjacent targets and spacing
- Mobile vs desktop behavior

**Output:** Touch target inventory.

### Step 2: Validate Against WCAG 2.2 Thresholds

Test every target against the two WCAG levels.

**WCAG 2.2 thresholds:**

| Level | Minimum Size | Exceptions |
|-------|-------------|------------|
| SC 2.5.8 (AA) | 24×24 CSS px | Inline links, sentence text, browser-native controls |
| SC 2.5.5 (AAA) | 44×44 CSS px | Same exceptions |

**Measurement rules:**
- Size = visual size + padding (the entire clickable area)
- If element is 20×20 but has 12px padding → actual target = 44×44 → PASS
- Measure the RENDERED size, not the CSS declaration
- For circular targets: diameter must meet threshold

**Spacing rule (WCAG 2.5.8):**
- Adjacent targets < 24px apart need offset circles of 24px that don't overlap
- OR each target individually meets 24×24px minimum

**Output:** Size compliance report.

### Step 3: Analyze Adjacent Target Spacing

Check for overlapping or too-close targets.

**Problem patterns:**

| Pattern | Issue | Fix |
|---------|-------|-----|
| Icon buttons in toolbar | 6px gap, 24px targets | Add gap or increase padding |
| Table action buttons | 3 buttons in last column | Space or use dropdown menu |
| Mobile nav items | 32px height, 0px gap | Increase height to 44px, add 8px gap |
| Breadcrumb links | Text links touching | Add padding between items |
| Tag/chip dismiss × | 16×16 close button | Increase to 24×24 minimum |

**Rules:**
- Minimum 8px spacing between adjacent targets (recommended)
- No overlapping clickable areas
- Dense patterns (tables, toolbars): consider grouping into dropdown/menu

**Output:** Spacing analysis.

### Step 4: Mobile-Specific Audit

Validate targets for touch interaction (not just click).

**Mobile considerations:**
- Touch targets should be 44×44px minimum (Apple HIG, Material Design)
- Thumb zone: bottom 1/3 of screen is easiest to reach
- One-handed operation: primary actions within thumb reach
- Fat finger tolerance: 8px minimum spacing
- Swipe targets: at least 44px in swipe direction

**Platform guidelines:**

| Platform | Minimum | Recommended |
|----------|---------|-------------|
| WCAG 2.2 AA | 24×24px | — |
| WCAG 2.2 AAA | 44×44px | — |
| Apple HIG | 44×44pt | 44×44pt |
| Material Design | 48×48dp | 48×48dp |
| Android | 48×48dp | 48×48dp |

**Output:** Mobile-specific target audit.

### Step 5: Generate Fix Recommendations

For each failing target, provide specific fixes.

**Fix strategies:**

| Issue | Fix |
|-------|-----|
| Small icon button (16×16) | Add `min-w-11 min-h-11 p-2.5` (44px) |
| Small text link | Add `py-2 px-3` padding |
| Close button (×) | Increase to 44×44 with larger hit area |
| Checkbox/radio | Wrap in label with padding |
| Dense table actions | Replace with overflow menu |
| Mobile nav items | `min-h-[44px]` with `py-3` |

**CSS pattern for invisible target expansion:**
```css
.icon-button {
  position: relative;
}
.icon-button::after {
  content: '';
  position: absolute;
  inset: -8px; /* Expands clickable area by 8px in all directions */
}
```

**Output:** Fix recommendations per component.

### Step 6: Document Touch Target Architecture

Compile the complete specification.

**Documentation includes:**
- Target inventory (from Step 1)
- Compliance report (from Step 2)
- Spacing analysis (from Step 3)
- Mobile audit (from Step 4)
- Fix recommendations (from Step 5)
- Design tokens for target sizes
- Testing procedure (browser DevTools overlay)

**Output:** Touch target specification document.

---

## Quality Criteria

- All targets meet WCAG 2.2 SC 2.5.8 minimum (24×24px)
- Primary actions meet enhanced target size (44×44px)
- Adjacent targets have minimum 8px spacing
- Icon-only buttons have visible or expanded hit areas
- Mobile-specific targets validated on actual devices
- No overlapping clickable regions

---

*Squad Apex — Touch Target Audit Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-touch-target-audit
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Zero targets below WCAG 2.2 AA minimum (24x24px)"
    - "Primary actions at 44x44px enhanced level"
    - "Adjacent targets have 8px minimum spacing"
    - "Mobile validation completed"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@css-eng` or `@react-eng` |
| Artifact | Touch target audit report with fix recommendations |
| Next action | Apply CSS fixes via `@css-eng` or component changes via `@react-eng` |
