> **DEPRECATED** — Scope absorbed into `animation-architecture.md`. See `data/task-consolidation-map.yaml`.

# Task: gesture-animation-system

```yaml
id: gesture-animation-system
version: "1.0.0"
title: "Gesture-Animation System Design"
description: >
  Designs the unified system connecting gesture input to animation
  output. Maps gesture events to animation responses, implements
  the Hybrid Engine pattern (WAAPI for simple, rAF for complex),
  designs velocity-to-spring handoff, and creates reusable
  gesture-animation primitives. The bridge between user touch/mouse
  and visual motion response.
elicit: false
owner: motion-eng
executor: motion-eng
outputs:
  - Gesture-to-animation mapping
  - Hybrid Engine implementation (WAAPI + rAF)
  - Velocity-to-spring handoff patterns
  - Gesture-animation primitives library
  - Interaction feel specifications
  - Gesture-animation system specification document
```

---

## When This Task Runs

This task runs when:
- Drag interactions need smooth animation responses
- Swipe gestures need natural spring physics at release
- Pull-to-refresh or swipe-to-dismiss needs implementation
- Animations feel disconnected from the gesture that triggers them
- Need to design the "feel" of an interaction (spring tension, damping)
- `*gesture-animation` or `*interaction-feel` is invoked

This task does NOT run when:
- Gesture handler configuration only (use `gesture-design` for mobile)
- Animation without gesture input (use `animation-design` or `choreography-design`)
- Scroll-driven animations (use `scroll-driven-animation`)

---

## Execution Steps

### Step 1: Map Gestures to Animations

Define the gesture-to-animation response for every interaction.

**Mapping table:**
| Gesture | Phase | Animation Response | Physics |
|---------|-------|-------------------|---------|
| Drag | During | Element follows pointer (1:1) | Direct mapping |
| Drag | Release | Spring to target or origin | Spring (damping, stiffness) |
| Swipe | Release fast | Fling with deceleration | Velocity-based decay |
| Swipe | Release slow | Spring back to origin | Spring |
| Pinch | During | Scale follows finger distance | Direct mapping |
| Pinch | Release | Spring to nearest snap | Spring with snap points |
| Long press | Start | Scale down 0.95 + haptic | Timing (150ms) |
| Long press | Release | Spring back to 1.0 | Spring |
| Tap | Down | Scale 0.97, opacity 0.8 | Timing (100ms) |
| Tap | Up | Spring back to 1.0, 1.0 | Spring (fast) |

**Gesture phase model:**
```
IDLE → START → UPDATE → END → ANIMATE → IDLE
         ↓        ↓       ↓        ↓
      (capture) (track) (release) (physics)
```

**Output:** Complete gesture-to-animation mapping.

### Step 2: Implement Hybrid Engine

Design the animation engine that selects the optimal rendering path.

**Hybrid Engine pattern (Matt Perry's approach):**
```typescript
type AnimationEngine = 'waapi' | 'raf' | 'css';

function selectEngine(animation: AnimationConfig): AnimationEngine {
  // CSS transitions: simple state changes, no interruption needed
  if (animation.simple && !animation.interruptible) return 'css';

  // WAAPI: keyframe animations, multi-property, interruptible
  if (animation.keyframes && !animation.physicsBased) return 'waapi';

  // rAF: spring physics, gesture-driven, complex interpolation
  return 'raf';
}
```

**Engine capabilities:**
| Feature | CSS Transition | WAAPI | rAF (Spring) |
|---------|---------------|-------|-------------|
| Simple A→B | Yes | Yes | Overkill |
| Multi-keyframe | No | Yes | Yes |
| Spring physics | No | No | Yes |
| Gesture-driven | No | Partial | Yes |
| Interruptible | Difficult | Yes | Yes |
| 60fps guaranteed | Yes (compositor) | Yes (compositor) | Requires care |
| Velocity handoff | No | No | Yes |

**Implementation:**

**CSS path (simple):**
```css
.button {
  transition: transform 150ms ease, opacity 150ms ease;
}
.button:active {
  transform: scale(0.97);
  opacity: 0.8;
}
```

**WAAPI path (keyframes):**
```typescript
element.animate([
  { transform: 'translateX(0)', opacity: 1 },
  { transform: 'translateX(-100px)', opacity: 0 },
], {
  duration: 300,
  easing: 'ease-out',
  fill: 'forwards',
});
```

**rAF path (spring physics):**
```typescript
function springAnimation(
  from: number,
  to: number,
  velocity: number,
  config: { damping: number; stiffness: number; mass: number },
  onUpdate: (value: number) => void,
  onComplete: () => void
) {
  let position = from;
  let currentVelocity = velocity;

  function tick() {
    const force = -config.stiffness * (position - to);
    const dampingForce = -config.damping * currentVelocity;
    const acceleration = (force + dampingForce) / config.mass;

    currentVelocity += acceleration * (1 / 60);
    position += currentVelocity * (1 / 60);

    onUpdate(position);

    if (Math.abs(currentVelocity) < 0.01 && Math.abs(position - to) < 0.01) {
      onUpdate(to);
      onComplete();
      return;
    }

    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);
}
```

**Output:** Hybrid Engine implementation with engine selection logic.

### Step 3: Design Velocity-to-Spring Handoff

Seamlessly transition from gesture-driven motion to physics-based animation.

**The handoff moment:** When the user releases their finger/mouse, the element has a position AND velocity. The spring animation must START from that exact state.

```typescript
interface GestureEndState {
  position: number;      // Where the element is
  velocity: number;      // How fast it was moving
  direction: 1 | -1;    // Which direction
}

interface SpringConfig {
  target: number;        // Where to animate to
  damping: number;       // How quickly oscillation dies
  stiffness: number;     // How snappy the spring is
  mass: number;          // How heavy (affects momentum)
}

function gestureToSpring(
  endState: GestureEndState,
  snapPoints: number[]
): { target: number; config: SpringConfig } {
  // Project where the element would end up given current velocity
  const projectedEnd = endState.position + endState.velocity * 0.3;

  // Find nearest snap point to projected end
  const target = snapPoints.reduce((nearest, point) =>
    Math.abs(point - projectedEnd) < Math.abs(nearest - projectedEnd)
      ? point
      : nearest
  );

  // Spring config: faster velocity = more damping needed
  const config = {
    damping: 20 + Math.abs(endState.velocity) * 0.01,
    stiffness: 200,
    mass: 1,
  };

  return { target, config };
}
```

**Velocity thresholds:**
| Velocity | Interpretation | Action |
|----------|---------------|--------|
| <100px/s | Slow release | Spring to nearest snap point |
| 100-500px/s | Normal swipe | Spring to next snap point |
| >500px/s | Fast fling | Animate past next snap, spring to further |
| >1000px/s | Very fast fling | Dismiss / complete action |

**Output:** Velocity-to-spring handoff patterns.

### Step 4: Create Gesture-Animation Primitives

Build reusable primitives for common gesture-animation patterns.

**Draggable primitive:**
```typescript
function useDraggable(config: {
  axis: 'x' | 'y' | 'both';
  bounds?: { min: number; max: number };
  snapPoints?: number[];
  rubberBand?: boolean;
  onDragEnd?: (state: GestureEndState) => void;
}) {
  // Returns: { style, handlers, isDragging }
}
```

**Swipeable primitive:**
```typescript
function useSwipeable(config: {
  direction: 'left' | 'right' | 'up' | 'down';
  threshold: number; // Distance to trigger
  velocityThreshold: number; // Speed to trigger
  onSwipe: () => void;
  onCancel: () => void;
}) {
  // Returns: { style, handlers }
}
```

**Dismissible primitive:**
```typescript
function useDismissible(config: {
  direction: 'down' | 'right';
  threshold: 0.4; // 40% of dimension
  onDismiss: () => void;
  rubberBand: true;
}) {
  // Returns: { style, handlers, progress }
}
```

**Pressable primitive (tap feedback):**
```typescript
function usePressable(config?: {
  scale?: number;       // Default: 0.97
  opacity?: number;     // Default: 0.8
  duration?: number;    // Default: 100ms
  springBack?: boolean; // Default: true
}) {
  // Returns: { style, handlers, isPressed }
}
```

**Output:** Gesture-animation primitive library.

### Step 5: Specify Interaction Feel

Document the exact physics that define the app's interaction personality.

**Spring presets:**
| Name | Damping | Stiffness | Mass | Feel |
|------|---------|-----------|------|------|
| `snappy` | 20 | 300 | 0.8 | Quick, no overshoot |
| `gentle` | 15 | 150 | 1.0 | Soft, slight overshoot |
| `bouncy` | 10 | 200 | 0.8 | Playful, visible bounce |
| `heavy` | 25 | 200 | 1.5 | Weighty, slow settle |
| `instant` | 30 | 500 | 0.5 | Near-instant, no bounce |

**Interaction feel rules:**
- Primary actions (buttons, nav): `snappy` — responsive, no bounce
- Content transitions (page, modal): `gentle` — smooth, inviting
- Fun interactions (likes, reactions): `bouncy` — playful feedback
- Dismissals (close, swipe away): `instant` — get out of the way
- Data-heavy (charts, tables): `heavy` — deliberate, stable

**Output:** Interaction feel specifications with spring presets.

### Step 6: Document Gesture-Animation System

Compile the complete specification.

**Documentation includes:**
- Gesture-to-animation mapping (from Step 1)
- Hybrid Engine design (from Step 2)
- Velocity handoff patterns (from Step 3)
- Primitive library API (from Step 4)
- Interaction feel guide (from Step 5)
- Reduced-motion alternatives for all animations
- Performance constraints (60fps budget per animation)

**Output:** Complete gesture-animation system specification.

---

## Quality Criteria

- Gesture-to-animation handoff must be seamless (no pause between release and spring)
- Hybrid Engine must select optimal path for each animation type
- Spring physics must incorporate gesture velocity (not start from zero)
- All primitives must respect prefers-reduced-motion
- Interactions must maintain 60fps

---

*Squad Apex — Gesture-Animation System Design Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-gesture-animation-system
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Gesture-to-spring handoff is seamless"
    - "Hybrid Engine selects optimal path per animation"
    - "Velocity incorporated into spring start state"
    - "All animations respect prefers-reduced-motion"
    - "60fps maintained during all interactions"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Gesture-animation system with Hybrid Engine, velocity handoff, primitives, and feel specifications |
| Next action | Implement primitives via `@react-eng` or validate a11y via `@a11y-eng` |
