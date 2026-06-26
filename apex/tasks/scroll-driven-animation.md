> **DEPRECATED** — Scope absorbed into `animation-architecture.md`. See `data/task-consolidation-map.yaml`.

# Task: scroll-driven-animation

```yaml
id: scroll-driven-animation
version: "1.0.0"
title: "Scroll-Driven Animation Design"
description: >
  Designs and implements scroll-driven animations using the CSS Scroll
  Timeline API and JavaScript scroll-linked patterns. Covers scroll
  progress indicators, parallax effects, reveal-on-scroll, sticky
  header transitions, and scroll-snapped animations. Ensures 60fps
  by avoiding main thread scroll handlers where possible.
elicit: false
owner: motion-eng
executor: motion-eng
outputs:
  - Scroll animation inventory
  - CSS Scroll Timeline implementations
  - JavaScript scroll-linked patterns (fallback)
  - Parallax effect specifications
  - Scroll performance audit
  - Scroll animation specification document
```

---

## When This Task Runs

This task runs when:
- Landing pages need scroll-driven visual effects
- Progress indicators need to track scroll position
- Parallax effects are requested
- Sticky headers need to transform on scroll
- Elements need to animate as they enter the viewport
- `*scroll-animation` or `*scroll-driven` is invoked

This task does NOT run when:
- Animations are triggered by user actions, not scroll (use `animation-design`)
- The task is about scroll containment/behavior (use `defensive-css-patterns`)
- Infinite scroll loading (use `@react-eng`)

---

## Execution Steps

### Step 1: Design Scroll Animation Inventory

Map all scroll-driven animations needed in the project.

| Animation | Trigger | Progress | Priority |
|-----------|---------|----------|----------|
| Reading progress bar | Page scroll | 0% → 100% of document | High |
| Header shrink | Scroll past hero | 0-200px scroll distance | High |
| Section fade-in | Element enters viewport | Intersection-based | Medium |
| Parallax background | Continuous scroll | Relative to scroll position | Low |
| Number counter | Section enters viewport | Animate number 0 → target | Medium |
| Horizontal scroll section | Vertical scroll → horizontal | Section progress | Low |

**Output:** Complete scroll animation inventory with priority.

### Step 2: Implement CSS Scroll Timeline Animations

Use the native CSS Scroll Timeline API for declarative, off-main-thread animations.

**Reading progress indicator:**
```css
@keyframes progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--color-accent);
  transform-origin: left;
  animation: progress auto linear;
  animation-timeline: scroll();
}
```

**Element reveal on scroll (view timeline):**
```css
@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal-on-scroll {
  animation: reveal auto ease-out both;
  animation-timeline: view();
  animation-range: entry 0% entry 40%;
}
```

**Header transform on scroll:**
```css
@keyframes header-shrink {
  from {
    padding-block: 1.5rem;
    background: transparent;
  }
  to {
    padding-block: 0.5rem;
    background: var(--color-surface);
    box-shadow: var(--shadow-sm);
  }
}

.header {
  position: sticky;
  top: 0;
  animation: header-shrink auto linear both;
  animation-timeline: scroll();
  animation-range: 0px 200px;
}
```

**Browser support:** Chrome 115+, Edge 115+. Firefox and Safari still behind.

**Output:** CSS Scroll Timeline implementations for each animation.

### Step 3: Implement JavaScript Fallback Patterns

Provide scroll-linked animations for browsers without Scroll Timeline API.

**Intersection Observer (reveal on scroll):**
```typescript
function useRevealOnScroll(options = {}) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.2, rootMargin: '0px 0px -50px 0px', ...options }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return ref;
}

// CSS
.reveal-target {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal-target.revealed {
  opacity: 1;
  transform: translateY(0);
}
```

**Framer Motion scroll-linked:**
```tsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxHero() {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, -150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);

  return (
    <motion.div style={{ y, opacity }}>
      <h1>Hero Content</h1>
    </motion.div>
  );
}

function ReadingProgress() {
  const { scrollYProgress } = useScroll();

  return (
    <motion.div
      className="reading-progress"
      style={{ scaleX: scrollYProgress }}
    />
  );
}
```

**Progressive enhancement strategy:**
```typescript
const supportsScrollTimeline = CSS.supports('animation-timeline', 'scroll()');

if (supportsScrollTimeline) {
  // CSS handles it — no JS needed
  element.classList.add('scroll-timeline-supported');
} else {
  // Fallback to Framer Motion / Intersection Observer
  initJSScrollAnimations();
}
```

**Output:** JavaScript scroll animation fallbacks.

### Step 4: Design Parallax Effects

Implement performant parallax that doesn't cause jank.

**Parallax rules:**
- Use `transform: translateY()` only (GPU-accelerated, no layout recalc)
- Never parallax text (readability and a11y issue)
- Maximum parallax ratio: 0.5x (subtle > dramatic)
- Disable parallax on `prefers-reduced-motion`
- Test on mobile (parallax often disabled on mobile for performance)

**CSS-only parallax (perspective trick):**
```css
.parallax-container {
  height: 100vh;
  overflow-y: auto;
  perspective: 1px;
}

.parallax-bg {
  position: absolute;
  inset: 0;
  transform: translateZ(-1px) scale(2);
  /* Element moves slower than scroll */
}

.parallax-content {
  position: relative;
  transform: translateZ(0);
  /* Normal scroll speed */
}
```

**Output:** Parallax effect specifications with performance constraints.

### Step 5: Audit Scroll Performance

Verify all scroll animations maintain 60fps.

**Performance checklist:**
- No `scroll` event listeners in hot path (use Intersection Observer)
- No `getBoundingClientRect()` on scroll (triggers layout recalc)
- All animated properties are GPU-composited (transform, opacity)
- No forced synchronous layouts (read then write pattern)
- `will-change: transform` applied sparingly (only when needed)
- `contain: paint` on scroll containers

**Chrome DevTools scroll performance audit:**
1. Open Performance tab
2. Enable "Scrolling Performance Issues" in Rendering tab
3. Scroll through the page
4. Check for "Forced reflow" and "Long task" markers
5. Verify FPS counter stays at 60

**Output:** Scroll performance audit with specific fixes.

### Step 6: Document Scroll Animation Architecture

Compile the complete specification.

**Documentation includes:**
- Animation inventory (from Step 1)
- CSS Scroll Timeline implementations (from Step 2)
- JavaScript fallbacks (from Step 3)
- Parallax specifications (from Step 4)
- Performance audit results (from Step 5)
- Reduced-motion strategy for all scroll animations
- Browser support table

**Output:** Complete scroll animation specification document.

---

## Quality Criteria

- All scroll animations must maintain 60fps
- No scroll event listeners (use Intersection Observer or Scroll Timeline)
- Parallax must be disabled on prefers-reduced-motion
- CSS Scroll Timeline used where supported, JS fallback where not
- No layout thrashing during scroll

---

*Squad Apex — Scroll-Driven Animation Design Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-scroll-driven-animation
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All scroll animations maintain 60fps"
    - "No scroll event listeners in hot path"
    - "Parallax disabled on prefers-reduced-motion"
    - "Progressive enhancement for Scroll Timeline API"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@perf-eng` or `@apex-lead` |
| Artifact | Scroll animation architecture with CSS Scroll Timeline, JS fallbacks, parallax specs, and performance audit |
| Next action | Validate performance via `@perf-eng` or test a11y via `@a11y-eng` |
