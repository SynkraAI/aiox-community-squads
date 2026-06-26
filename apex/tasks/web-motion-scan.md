# Task: web-motion-scan

```yaml
id: web-motion-scan
version: "1.0.0"
title: "Animation & Transition Extraction"
description: >
  Extract all animations and transitions from an external URL. Identifies
  CSS transitions, CSS animations, JavaScript-driven motion, and spring
  physics configs. Outputs a motion inventory categorized by interaction type.
elicit: false
owner: web-intel
executor: web-intel
inputs:
  - url: "Target URL"
outputs:
  - Motion inventory (transitions, animations, transforms)
  - Spring vs bezier analysis
  - Reduced-motion handling assessment
  - Motion language map (enter, exit, feedback, transform)
veto_conditions:
  - "Motion extraction without checking reduced-motion handling → BLOCK"
```

---

## Command

### `*motion-scan {url}`

Extract animations and transitions from URL.

---

## Execution Steps

### Step 1: Navigate & Capture

Navigate with playwright. Capture:
- All CSS `transition` properties from computed styles
- All CSS `@keyframes` animations
- JavaScript animation libraries detected (Framer Motion, GSAP, Anime.js, etc.)
- `prefers-reduced-motion` media query presence

### Step 2: Extract Motion Properties

```yaml
extraction:
  css_transitions:
    properties: [transition-property, transition-duration, transition-timing-function, transition-delay]
    per_element: "selector → property → duration → easing"

  css_animations:
    properties: [animation-name, animation-duration, animation-timing-function, animation-iteration-count]
    keyframes: "Extract @keyframes definitions"

  transforms:
    properties: [transform, will-change]
    per_element: "What transforms are applied and when"

  js_libraries:
    detect:
      - "framer-motion / motion: data-framer-* attributes, motion.div patterns"
      - "gsap: gsap.to/from/timeline in scripts"
      - "anime.js: anime() calls"
      - "react-spring: useSpring hooks"
      - "Web Animations API: element.animate()"
```

### Step 3: Categorize by Motion Language

```yaml
motion_categories:
  enter: "Elements appearing — opacity 0→1, scale 0.95→1, translateY"
  exit: "Elements disappearing — opacity 1→0, scale 1→0.95"
  feedback: "User interaction response — button press, hover lift"
  transform: "State changes — accordion, tab switch, toggle"
  status: "Status communication — loading, success, error"
  decorative: "Background motion — gradients, particles, ambient"
```

### Step 4: Analyze Spring vs Bezier

```yaml
analysis:
  spring_detection:
    - "spring() in CSS (if supported)"
    - "Framer Motion spring configs"
    - "React Spring configs"
  bezier_detection:
    - "ease, ease-in, ease-out, ease-in-out"
    - "cubic-bezier() functions"
    - "linear"
  reduced_motion:
    - "Check for @media (prefers-reduced-motion: reduce)"
    - "Check for matchMedia in JS"
    - "Report: handled | partially | not handled"
```

### Step 5: Present Motion Report

```
## Motion Analysis: {url}

### Motion Inventory ({N} animations found)
| # | Element | Type | Duration | Easing | Category |
|---|---------|------|----------|--------|----------|
| 1 | .modal | enter | 200ms | spring(300,20) | enter |
| 2 | .btn | feedback | 150ms | ease-out | feedback |
| 3 | .card | hover | 200ms | cubic-bezier(.2,.8,.4,1) | feedback |

### Spring vs Bezier
- Spring physics: {N} animations ({%})
- Bezier curves: {N} animations ({%})
- Linear: {N} ({%})

### Reduced Motion
- Status: {handled | partial | not handled}
- Details: {what is/isn't handled}

### Motion Library: {Framer Motion | GSAP | CSS only | Custom}

Options:
1. Adopt motion patterns (→ @motion-eng for spring conversion)
2. Extract spring configs only
3. Compare with our motion setup
4. Done
```
