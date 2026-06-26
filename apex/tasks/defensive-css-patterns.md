> **DEPRECATED** — Scope absorbed into `css-architecture-audit.md`. See `data/task-consolidation-map.yaml`.

# Task: defensive-css-patterns

```yaml
id: defensive-css-patterns
version: "1.0.0"
title: "Defensive CSS Patterns"
description: >
  Implements defensive CSS patterns that prevent layout breakage from
  unexpected content. Handles text overflow, image aspect ratios,
  flexbox/grid wrapping, scroll containment, long words, missing
  images, dynamic content length, and RTL support. Produces CSS that
  doesn't break regardless of content — "CSS that anticipates the worst."
elicit: false
owner: css-eng
executor: css-eng
outputs:
  - Defensive pattern catalog (20+ patterns)
  - Content-resilient component templates
  - Text overflow strategy
  - Image fallback patterns
  - Scroll containment rules
  - Defensive CSS specification document
```

---

## When This Task Runs

This task runs when:
- Components break with unexpected content (long text, missing images, empty states)
- User-generated content causes layout shifts or overflow
- Internationalization reveals layout fragility (German text is 30% longer)
- QA finds visual bugs from edge case content
- `*defensive-css` or `*css-defense` is invoked

This task does NOT run when:
- The issue is a specific CSS bug (use `stacking-context-debug`)
- Architecture-level CSS decisions (use `css-architecture-audit`)
- Performance optimization (use `@perf-eng`)

---

## Execution Steps

### Step 1: Text Overflow Protection

Prevent text from breaking layouts.

**Pattern catalog:**

```css
/* 1. Truncate single line */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 2. Clamp multi-line (2 lines) */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 3. Break long words (URLs, German compound words) */
.break-word {
  overflow-wrap: break-word;
  word-break: break-word;
  hyphens: auto;
}

/* 4. Minimum width protection in flex */
.flex-child-safe {
  min-width: 0; /* Allows flex child to shrink below content size */
}

/* 5. Table cell text protection */
.table-cell-safe {
  max-width: 0; /* Forces truncation in table layout */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

**Tailwind equivalents:**
```html
<p class="truncate">...</p>
<p class="line-clamp-2">...</p>
<p class="break-words">...</p>
<div class="flex"><span class="min-w-0 truncate">...</span></div>
```

**Output:** Text overflow patterns for all common scenarios.

### Step 2: Image Resilience

Handle images that fail to load, have wrong aspect ratios, or are missing.

```css
/* 1. Aspect ratio protection (prevents layout shift) */
.img-container {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}
.img-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 2. Broken image fallback */
img {
  min-height: 50px;
  background-color: var(--color-surface-elevated);
}
img::after {
  content: attr(alt);
  display: grid;
  place-items: center;
  height: 100%;
  font-size: 0.875rem;
  color: var(--color-content-secondary);
}

/* 3. Avatar with initials fallback */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--color-primary);
  display: grid;
  place-items: center;
  color: white;
  font-weight: 600;
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

**Output:** Image resilience patterns with fallbacks.

### Step 3: Flexbox/Grid Safety

Prevent flex and grid layouts from breaking.

```css
/* 1. Flex wrapping protection */
.flex-safe {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

/* 2. Flex child minimum width (prevents overflow) */
.flex-safe > * {
  min-width: 0;   /* Allow shrinking */
  flex-shrink: 1;
}

/* 3. Grid auto-fit (adapts columns to available space) */
.grid-responsive {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  gap: 1rem;
}

/* 4. Grid with maximum columns */
.grid-max-4 {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(250px, 100%), 1fr));
  gap: 1rem;
}

/* 5. Prevent grid blowout from long content */
.grid-safe > * {
  min-width: 0;
  overflow: hidden;
}

/* 6. Sticky positioning safety */
.sticky-safe {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  /* Prevent content pushing sticky element */
  align-self: start;
}
```

**Output:** Flex/grid safety patterns.

### Step 4: Scroll Containment

Prevent scroll chaining and contain scroll regions.

```css
/* 1. Modal scroll containment (prevent body scroll) */
.modal-open body {
  overflow: hidden;
}
.modal-content {
  overscroll-behavior: contain;
  overflow-y: auto;
  max-height: 80vh;
}

/* 2. Sidebar independent scroll */
.sidebar {
  overflow-y: auto;
  overscroll-behavior: contain; /* Don't scroll parent */
  height: 100vh;
  position: sticky;
  top: 0;
}

/* 3. Horizontal scroll with snap */
.carousel {
  display: flex;
  overflow-x: auto;
  overscroll-behavior-x: contain;
  scroll-snap-type: x mandatory;
  scrollbar-width: none; /* Hide scrollbar */
}
.carousel::-webkit-scrollbar { display: none; }
.carousel > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}

/* 4. Scrollbar gutter (prevent layout shift) */
.scrollable {
  overflow-y: auto;
  scrollbar-gutter: stable; /* Reserve space for scrollbar */
}
```

**Output:** Scroll containment patterns.

### Step 5: Dynamic Content Safety

Handle empty states, single items, and variable content lengths.

```css
/* 1. Empty state with :empty */
.list:empty::before {
  content: "No items found";
  display: block;
  text-align: center;
  padding: 2rem;
  color: var(--color-content-secondary);
}

/* 2. Single-child special case */
.card-grid > :only-child {
  max-width: 400px; /* Don't stretch single card full-width */
}

/* 3. Last child margin removal */
.stack > :last-child {
  margin-bottom: 0;
}

/* 4. Quantity queries (adapt layout based on item count) */
/* 1-3 items: single row */
.tag-list:has(:nth-child(n + 4)) {
  flex-wrap: wrap;
}

/* 5. Content-dependent minimum height */
.hero {
  min-height: max(50vh, 400px);
}

/* 6. Safe area insets (mobile notch) */
.bottom-bar {
  padding-bottom: env(safe-area-inset-bottom);
}
```

**Output:** Dynamic content safety patterns.

### Step 6: Document Defensive CSS Specification

Compile all patterns into a searchable reference.

**Documentation includes:**
- Text overflow patterns (from Step 1)
- Image resilience (from Step 2)
- Flex/grid safety (from Step 3)
- Scroll containment (from Step 4)
- Dynamic content safety (from Step 5)
- Quick reference cheat sheet
- Integration with Tailwind utility classes
- Testing checklist (content edge cases to verify)

**Output:** Complete defensive CSS specification document.

---

## Quality Criteria

- All patterns must handle content 3x longer than expected
- Images must display gracefully when broken or missing
- Flex/grid layouts must not overflow their containers
- Scroll containers must not chain to parent
- Patterns must work in latest Chrome, Firefox, Safari

---

*Squad Apex — Defensive CSS Patterns Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-defensive-css-patterns
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All patterns handle 3x content length without breaking"
    - "Broken images display fallback gracefully"
    - "No flex/grid overflow in any component"
    - "Scroll containment prevents chaining"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@qa-visual` or `@apex-lead` |
| Artifact | Defensive CSS pattern catalog with templates and testing checklist |
| Next action | Apply patterns to components or run visual regression via `@qa-visual` |
