> **DEPRECATED** — Scope absorbed into `animation-architecture.md`. See `data/task-consolidation-map.yaml`.

# Task: layout-animation-patterns

```yaml
id: layout-animation-patterns
version: "1.0.0"
title: "Layout Animation Patterns"
description: >
  Designs layout animations that smoothly handle DOM changes: element
  reordering, adding/removing items, size changes, and shared layout
  transitions. Uses FLIP technique, Framer Motion layoutId, CSS
  View Transitions API, and auto-animate patterns. Eliminates visual
  jumps when the DOM changes — "everything moves, nothing teleports."
elicit: false
owner: motion-eng
executor: motion-eng
outputs:
  - Layout animation pattern catalog
  - FLIP technique implementations
  - Framer Motion layout patterns
  - CSS View Transitions patterns
  - List reorder animations
  - Layout animation specification document
```

---

## When This Task Runs

This task runs when:
- List items need smooth reorder animation (drag-and-drop, sort change)
- Items being added/removed from lists need enter/exit animations
- Element size changes need smooth transitions (accordion, expand/collapse)
- Shared layout transitions needed (list item → detail view)
- Page transitions need smooth morphing (SPA navigation)
- `*layout-animation` or `*layout-patterns` is invoked

This task does NOT run when:
- Simple opacity/transform animations (use `animation-design`)
- Scroll-driven animations (use `scroll-driven-animation`)
- Gesture input design (use `gesture-animation-system`)

---

## Execution Steps

### Step 1: Catalog Layout Animation Needs

Identify all DOM change scenarios that need animation.

| Scenario | Type | Example |
|----------|------|---------|
| List item added | Enter | New message appears in chat |
| List item removed | Exit | Todo item deleted |
| List reorder | Move | Drag-and-drop, sort change |
| Accordion open | Size change | FAQ expands |
| Tab switch | Shared layout | Active tab indicator slides |
| Card → Detail | Shared layout | List item expands to full page |
| Filter applied | Multi-item | Grid items rearrange |
| Page navigation | View transition | Page morphs to next page |

**Output:** Layout animation needs catalog.

### Step 2: Implement FLIP Technique

Use First-Last-Invert-Play for smooth layout transitions.

**FLIP explained:**
1. **First:** Record element's initial position/size
2. **Last:** Apply the DOM change (element moves to new position)
3. **Invert:** Calculate the delta and apply inverse transform
4. **Play:** Animate the inverse transform to zero (element moves smoothly)

**Manual FLIP implementation:**
```typescript
function flip(element: HTMLElement, callback: () => void) {
  // FIRST: Record current position
  const first = element.getBoundingClientRect();

  // Apply DOM change
  callback();

  // LAST: Record new position
  const last = element.getBoundingClientRect();

  // INVERT: Calculate delta and apply inverse transform
  const deltaX = first.left - last.left;
  const deltaY = first.top - last.top;
  const deltaW = first.width / last.width;
  const deltaH = first.height / last.height;

  element.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(${deltaW}, ${deltaH})`;
  element.style.transformOrigin = 'top left';

  // PLAY: Animate to identity (removal of inverse)
  requestAnimationFrame(() => {
    element.style.transition = 'transform 300ms ease';
    element.style.transform = '';

    element.addEventListener('transitionend', () => {
      element.style.transition = '';
      element.style.transformOrigin = '';
    }, { once: true });
  });
}
```

**When to use FLIP:**
- Simple position/size changes
- When Framer Motion is not available
- Performance-critical scenarios (FLIP is very lightweight)

**Output:** FLIP technique implementations.

### Step 3: Implement Framer Motion Layout Patterns

Use Framer Motion's layout animation system for complex scenarios.

**Basic layout animation:**
```tsx
import { motion } from 'framer-motion';

function ExpandableCard({ isExpanded }) {
  return (
    <motion.div layout className="card">
      <motion.h2 layout="position">{title}</motion.h2>
      {isExpanded && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {description}
        </motion.p>
      )}
    </motion.div>
  );
}
```

**Shared layout (list → detail):**
```tsx
function ProductList({ products }) {
  const [selected, setSelected] = useState(null);

  return (
    <LayoutGroup>
      {products.map(product => (
        <motion.div
          key={product.id}
          layoutId={`product-${product.id}`}
          onClick={() => setSelected(product)}
          className="product-card"
        >
          <motion.img layoutId={`img-${product.id}`} src={product.image} />
          <motion.h3 layoutId={`title-${product.id}`}>{product.name}</motion.h3>
        </motion.div>
      ))}

      <AnimatePresence>
        {selected && (
          <motion.div
            layoutId={`product-${selected.id}`}
            className="product-detail"
          >
            <motion.img layoutId={`img-${selected.id}`} src={selected.image} />
            <motion.h3 layoutId={`title-${selected.id}`}>{selected.name}</motion.h3>
            <p>{selected.description}</p>
            <button onClick={() => setSelected(null)}>Close</button>
          </motion.div>
        )}
      </AnimatePresence>
    </LayoutGroup>
  );
}
```

**List reorder animation:**
```tsx
import { Reorder, AnimatePresence } from 'framer-motion';

function SortableList({ items, onReorder }) {
  return (
    <Reorder.Group values={items} onReorder={onReorder}>
      <AnimatePresence>
        {items.map(item => (
          <Reorder.Item
            key={item.id}
            value={item}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ type: 'spring', damping: 20, stiffness: 200 }}
          >
            {item.content}
          </Reorder.Item>
        ))}
      </AnimatePresence>
    </Reorder.Group>
  );
}
```

**Output:** Framer Motion layout animation patterns.

### Step 4: Implement CSS View Transitions

Use the View Transitions API for page-level transitions.

**Same-document view transition (SPA):**
```typescript
async function navigateTo(url: string) {
  if (!document.startViewTransition) {
    // Fallback: instant navigation
    router.push(url);
    return;
  }

  const transition = document.startViewTransition(() => {
    router.push(url);
  });

  await transition.finished;
}
```

**CSS for view transitions:**
```css
/* Default crossfade (automatic) */
::view-transition-old(root) {
  animation: fade-out 200ms ease;
}
::view-transition-new(root) {
  animation: fade-in 200ms ease;
}

/* Named transitions for specific elements */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero) {
  animation: scale-down 300ms ease;
}
::view-transition-new(hero) {
  animation: scale-up 300ms ease;
}
```

**Next.js integration (experimental):**
```tsx
// With next/navigation
'use client';
import { useRouter } from 'next/navigation';

function NavigationLink({ href, children }) {
  const router = useRouter();

  const handleClick = (e) => {
    e.preventDefault();
    if (document.startViewTransition) {
      document.startViewTransition(() => router.push(href));
    } else {
      router.push(href);
    }
  };

  return <a href={href} onClick={handleClick}>{children}</a>;
}
```

**Output:** CSS View Transitions patterns with fallback.

### Step 5: Design Enter/Exit Animations for Lists

Create smooth add/remove animations for dynamic lists.

**Enter animation (new item):**
```tsx
<AnimatePresence>
  {items.map(item => (
    <motion.div
      key={item.id}
      initial={{ opacity: 0, height: 0, marginBottom: 0 }}
      animate={{ opacity: 1, height: 'auto', marginBottom: 8 }}
      exit={{ opacity: 0, height: 0, marginBottom: 0 }}
      transition={{
        opacity: { duration: 0.2 },
        height: { type: 'spring', damping: 20, stiffness: 200 },
      }}
    >
      <ListItem item={item} />
    </motion.div>
  ))}
</AnimatePresence>
```

**Staggered enter:**
```tsx
const container = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.05 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i.id} variants={item}>
      {i.content}
    </motion.li>
  ))}
</motion.ul>
```

**Rules:**
- Animate `height` with spring (not timing) for natural feel
- Exit should be faster than enter (200ms vs 300ms)
- Stagger max 50ms between items, cap total at 500ms
- Use `AnimatePresence mode="popLayout"` to avoid layout jump during exit

**Output:** List enter/exit animation patterns.

### Step 6: Document Layout Animation Architecture

Compile the complete specification.

**Documentation includes:**
- Layout animation catalog (from Step 1)
- FLIP technique guide (from Step 2)
- Framer Motion patterns (from Step 3)
- View Transitions API guide (from Step 4)
- List animation patterns (from Step 5)
- Decision tree: which technique for which scenario
- Reduced-motion alternatives
- Performance notes (avoid animating `height`/`width` directly when possible)

**Output:** Complete layout animation specification document.

---

## Quality Criteria

- No layout jumps or teleporting elements when DOM changes
- List reorder animations must maintain 60fps with 100+ items
- Shared layout transitions must handle interrupted animations
- View Transitions must have progressive enhancement fallback
- All layout animations must respect prefers-reduced-motion

---

*Squad Apex — Layout Animation Patterns Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-layout-animation-patterns
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "No layout jumps or teleporting elements"
    - "List reorder at 60fps with 100+ items"
    - "Shared layout handles interrupted animations"
    - "Reduced-motion respected for all patterns"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Layout animation patterns with FLIP, Framer Motion, View Transitions, and list animations |
| Next action | Implement in components via `@react-eng` or validate performance via `@perf-eng` |
