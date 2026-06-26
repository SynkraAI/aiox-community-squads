# Task: keyboard-navigation-patterns

```yaml
id: keyboard-navigation-patterns
version: "1.0.0"
title: "Keyboard Navigation Patterns"
description: >
  Designs and implements comprehensive keyboard navigation for complex
  UI patterns. Covers roving tabindex, arrow key navigation, focus
  trapping (modals/drawers), skip links, keyboard shortcuts, and
  composite widget navigation (tabs, menus, grids, trees). Ensures
  every interactive element is reachable and operable via keyboard
  alone — "if you can click it, you can Tab to it."
elicit: false
owner: a11y-eng
executor: a11y-eng
outputs:
  - Keyboard navigation pattern catalog
  - Roving tabindex implementations
  - Focus trap patterns (modal/drawer/popover)
  - Skip link architecture
  - Keyboard shortcut registry
  - Keyboard navigation specification document
```

---

## When This Task Runs

This task runs when:
- Complex widget needs keyboard support (tabs, menus, trees, grids)
- Modal/drawer/popover needs focus trapping
- Page navigation needs skip links
- App needs keyboard shortcut system
- `*keyboard-nav` or `*keyboard-patterns` is invoked

This task does NOT run when:
- ARIA attribute implementation (use `aria-pattern-implementation`)
- Screen reader announcement testing (use `screen-reader-testing`)
- Color contrast issues (use `color-contrast-automation`)

---

## Execution Steps

### Step 1: Audit Current Keyboard Navigation

Map every interactive element and its keyboard reachability.

**Audit checklist per component:**

| Check | Method |
|-------|--------|
| Tab reachable? | Tab through entire page |
| Visible focus indicator? | Check `:focus-visible` styles |
| Logical tab order? | Verify DOM order matches visual order |
| Escape closes overlays? | Press Escape on modals/popovers |
| Arrow keys in composites? | Test tabs, menus, listboxes |
| No keyboard traps? | Can Tab out of every region |
| Skip link present? | Tab from page load — first element? |

**Output:** Keyboard navigation audit results.

### Step 2: Implement Roving Tabindex

Design arrow-key navigation for composite widgets.

**Roving tabindex pattern:**
```tsx
function useRovingTabIndex(items: HTMLElement[]) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e: KeyboardEvent) => {
    let next = activeIndex;
    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        next = (activeIndex + 1) % items.length;
        break;
      case 'ArrowUp':
      case 'ArrowLeft':
        next = (activeIndex - 1 + items.length) % items.length;
        break;
      case 'Home':
        next = 0;
        break;
      case 'End':
        next = items.length - 1;
        break;
    }
    setActiveIndex(next);
    items[next]?.focus();
    e.preventDefault();
  };

  return { activeIndex, handleKeyDown };
}
```

**Widget patterns:**

| Widget | Keys | Orientation |
|--------|------|-------------|
| Tabs | Left/Right | Horizontal |
| Menu | Up/Down, Enter, Escape | Vertical |
| Listbox | Up/Down, Home, End | Vertical |
| Grid | All arrows | 2D |
| Tree | Up/Down, Left/Right (expand/collapse) | Vertical |
| Toolbar | Left/Right | Horizontal |

**Rules:**
- Only ONE item in composite has `tabindex="0"` (active)
- All others have `tabindex="-1"` (focusable via JS only)
- Arrow keys move focus, Tab moves OUT of composite
- Home/End jump to first/last item
- Type-ahead: typing a letter jumps to matching item

**Output:** Roving tabindex implementations.

### Step 3: Design Focus Trap Patterns

Implement focus containment for overlay components.

**Focus trap requirements:**
1. Focus moves to first focusable element on open
2. Tab at last element wraps to first element
3. Shift+Tab at first element wraps to last element
4. Escape closes the overlay and returns focus to trigger
5. Background content is inert (`inert` attribute or `aria-hidden`)

**Implementation:**
```tsx
function useFocusTrap(ref: RefObject<HTMLElement>) {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const focusable = element.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), ' +
      'select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    const first = focusable[0] as HTMLElement;
    const last = focusable[focusable.length - 1] as HTMLElement;

    first?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last?.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first?.focus();
      }
    };

    element.addEventListener('keydown', handleKeyDown);
    return () => element.removeEventListener('keydown', handleKeyDown);
  }, [ref]);
}
```

**Overlay types and behavior:**

| Overlay | Focus on open | Escape | Return focus |
|---------|--------------|--------|--------------|
| Modal | First focusable | Closes | Trigger element |
| Drawer | Close button | Closes | Trigger element |
| Popover | First focusable | Closes | Trigger element |
| Combobox list | Stays on input | Closes list | Input (already there) |
| Toast | Don't steal focus | Dismiss | N/A |

**Output:** Focus trap patterns.

### Step 4: Implement Skip Links

Design skip navigation for efficient page traversal.

**Skip link architecture:**
```html
<!-- First focusable element on page -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#navigation" class="skip-link">Skip to navigation</a>

<!-- Targets -->
<nav id="navigation">...</nav>
<main id="main-content" tabindex="-1">...</main>
```

**CSS (visible on focus only):**
```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  z-index: 9999;
  padding: 1rem;
  background: var(--color-primary);
  color: white;
}
.skip-link:focus {
  top: 0;
}
```

**Rules:**
- Skip link is the FIRST focusable element on page
- Target element needs `tabindex="-1"` for programmatic focus
- Minimum skip links: "Skip to main content"
- SPA: reset skip link behavior on route change

**Output:** Skip link architecture.

### Step 5: Design Keyboard Shortcut System

Create a centralized keyboard shortcut registry.

**Shortcut registry:**
```typescript
const shortcuts: ShortcutMap = {
  'mod+k': { action: 'openCommandPalette', description: 'Open command palette' },
  'mod+/': { action: 'openSearch', description: 'Focus search' },
  'Escape': { action: 'closeOverlay', description: 'Close current overlay' },
  '?': { action: 'showShortcuts', description: 'Show keyboard shortcuts' },
};
```

**Rules:**
- `mod` = Cmd on Mac, Ctrl on Windows/Linux
- Never override browser defaults (Ctrl+C, Ctrl+V, Ctrl+T)
- Never override screen reader keys (VoiceOver, NVDA)
- Shortcuts must be discoverable (? to show list)
- Shortcuts disabled when focus is in text input
- All shortcuts must have accessible labels

**Output:** Keyboard shortcut registry.

### Step 6: Document Keyboard Navigation Architecture

Compile the complete specification.

**Documentation includes:**
- Navigation audit results (from Step 1)
- Roving tabindex patterns (from Step 2)
- Focus trap implementations (from Step 3)
- Skip link architecture (from Step 4)
- Shortcut registry (from Step 5)
- Decision tree: which pattern for which widget
- Testing procedures (manual keyboard testing checklist)

**Output:** Keyboard navigation specification document.

---

## Quality Criteria

- Every interactive element reachable via Tab or arrow keys
- No keyboard traps in any component
- Focus indicators visible and meeting 3:1 contrast ratio
- All overlays properly trap and restore focus
- Skip links functional on every page
- Keyboard shortcuts never conflict with AT keys

---

*Squad Apex — Keyboard Navigation Patterns Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-keyboard-navigation-patterns
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Zero keyboard traps across all components"
    - "Every interactive element Tab-reachable"
    - "Focus indicators meet 3:1 contrast"
    - "Skip links present and functional"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Keyboard navigation patterns with roving tabindex, focus traps, skip links |
| Next action | Implement in components via `@react-eng` or validate with AT via `@a11y-eng` screen reader testing |
