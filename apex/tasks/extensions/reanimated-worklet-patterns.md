# Task: reanimated-worklet-patterns

```yaml
id: reanimated-worklet-patterns
version: "1.0.0"
title: "Reanimated Worklet Patterns"
description: >
  Documents and implements advanced Reanimated worklet patterns for
  React Native. Covers shared value architecture, derived values,
  animation composition, gesture-animation coordination, layout
  animations, and worklet threading model. Produces a worklet
  pattern library tailored to the project's animation needs.
elicit: false
owner: mobile-eng
executor: mobile-eng
outputs:
  - Shared value architecture patterns
  - Derived value composition patterns
  - Gesture-to-animation coordination patterns
  - Layout animation patterns (entering/exiting)
  - Worklet threading guidelines
  - Pattern library document
```

---

## When This Task Runs

This task runs when:
- Complex animations require worklet-level control beyond simple `withSpring`
- Multiple animations need coordination (gesture + spring + layout)
- Performance issues caused by JS thread animation calculations
- Team needs standardized animation patterns for consistency
- `*worklet-patterns` or `*reanimated-patterns` is invoked

This task does NOT run when:
- Simple one-off animations that `withSpring`/`withTiming` handle
- Web-only animations (use `@motion-eng` with Framer Motion)
- The task is about gesture handler config (use `gesture-design`)

---

## Execution Steps

### Step 1: Define Shared Value Architecture

Establish patterns for managing `useSharedValue` across components.

**Basic shared value patterns:**

```typescript
// Pattern 1: Single animation driver
const translateX = useSharedValue(0);
const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ translateX: translateX.value }],
}));

// Pattern 2: Derived values (computed from other shared values)
const scale = useDerivedValue(() => {
  return interpolate(translateX.value, [-200, 0, 200], [0.5, 1, 0.5]);
});

// Pattern 3: Multi-property coordination
const progress = useSharedValue(0);
const animatedStyle = useAnimatedStyle(() => ({
  opacity: interpolate(progress.value, [0, 1], [0, 1]),
  transform: [
    { scale: interpolate(progress.value, [0, 0.5, 1], [0.8, 1.1, 1]) },
    { translateY: interpolate(progress.value, [0, 1], [20, 0]) },
  ],
}));
```

**Architecture rules:**
- One shared value per independent animation dimension (x, y, scale, opacity)
- Use `useDerivedValue` for computed properties (never compute in `useAnimatedStyle`)
- Keep shared values close to the component that owns the animation
- Pass shared values as props for cross-component coordination
- NEVER read `.value` in the React render function (only in worklets)

**Anti-patterns to avoid:**
| Anti-pattern | Problem | Correct Pattern |
|-------------|---------|-----------------|
| `useState` for animation values | Triggers re-render per frame | `useSharedValue` |
| Compute in `useAnimatedStyle` | Recalculates every frame | `useDerivedValue` |
| `runOnJS` in hot path | Bridge crossing per frame | Keep computation in worklet |
| Multiple `useAnimatedStyle` on same element | Merging overhead | Single `useAnimatedStyle` |

**Output:** Shared value architecture patterns with naming conventions.

### Step 2: Implement Animation Composition Patterns

Build reusable patterns for combining multiple animations.

**Sequential composition:**
```typescript
// Run animations in sequence
const runSequence = () => {
  'worklet';
  opacity.value = withTiming(1, { duration: 200 }, (finished) => {
    if (finished) {
      translateY.value = withSpring(0, { damping: 15, stiffness: 200 });
    }
  });
};
```

**Parallel composition:**
```typescript
// Run animations simultaneously
const runParallel = () => {
  'worklet';
  opacity.value = withTiming(1, { duration: 300 });
  scale.value = withSpring(1, { damping: 12, stiffness: 180 });
  translateY.value = withSpring(0, { damping: 15, stiffness: 200 });
};
```

**Staggered composition:**
```typescript
// Stagger child animations
const stagger = (items: SharedValue<number>[], delayMs: number) => {
  'worklet';
  items.forEach((item, index) => {
    item.value = withDelay(
      index * delayMs,
      withSpring(1, { damping: 12, stiffness: 180 })
    );
  });
};
```

**Repeat and loop:**
```typescript
// Looping animation (pulse, breathing)
const startPulse = () => {
  'worklet';
  scale.value = withRepeat(
    withSequence(
      withTiming(1.05, { duration: 1000 }),
      withTiming(1.0, { duration: 1000 })
    ),
    -1, // Infinite
    true // Reverse
  );
};
```

**Output:** Animation composition patterns (sequential, parallel, stagger, loop).

### Step 3: Coordinate Gestures with Animations

Design patterns for seamless gesture-to-animation handoff.

**Gesture drives animation, spring finishes:**
```typescript
const panGesture = Gesture.Pan()
  .onUpdate((event) => {
    'worklet';
    // Gesture directly drives position
    translateX.value = event.translationX;
  })
  .onEnd((event) => {
    'worklet';
    // Spring to final position based on velocity
    const shouldDismiss = Math.abs(event.velocityX) > 500 ||
                          Math.abs(event.translationX) > SCREEN_WIDTH * 0.4;
    if (shouldDismiss) {
      translateX.value = withSpring(
        Math.sign(event.translationX) * SCREEN_WIDTH,
        { velocity: event.velocityX, damping: 20 }
      );
    } else {
      translateX.value = withSpring(0, {
        velocity: event.velocityX,
        damping: 20,
        stiffness: 200,
      });
    }
  });
```

**Gesture with rubber banding (overscroll):**
```typescript
const clampedTranslate = useDerivedValue(() => {
  const clamped = Math.max(-MAX_TRANSLATE, Math.min(MAX_TRANSLATE, rawTranslate.value));
  const overflow = rawTranslate.value - clamped;
  // Rubber band: diminishing returns beyond bounds
  return clamped + overflow * 0.3;
});
```

**Gesture with snap points:**
```typescript
const snapTo = (value: number, snapPoints: number[], velocity: number) => {
  'worklet';
  // Find nearest snap point, biased by velocity
  const projected = value + velocity * 0.1;
  const nearest = snapPoints.reduce((prev, curr) =>
    Math.abs(curr - projected) < Math.abs(prev - projected) ? curr : prev
  );
  return withSpring(nearest, { velocity, damping: 20, stiffness: 200 });
};
```

**Output:** Gesture-animation coordination patterns.

### Step 4: Implement Layout Animation Patterns

Define entering, exiting, and layout change animations.

**Entering animations (component mount):**
```typescript
import { FadeInDown, SlideInRight, ZoomIn } from 'react-native-reanimated';

// Predefined
<Animated.View entering={FadeInDown.duration(300).springify()}>

// Custom entering
const customEntering = (values) => {
  'worklet';
  const animations = {
    opacity: withTiming(1, { duration: 300 }),
    transform: [{ translateY: withSpring(0, { damping: 15 }) }],
  };
  const initialValues = {
    opacity: 0,
    transform: [{ translateY: 50 }],
  };
  return { initialValues, animations };
};
```

**Exiting animations (component unmount):**
```typescript
<Animated.View exiting={FadeOutUp.duration(200)}>

// Custom exiting
const customExiting = (values) => {
  'worklet';
  const animations = {
    opacity: withTiming(0, { duration: 200 }),
    transform: [{ scale: withTiming(0.9) }],
  };
  const initialValues = {
    opacity: 1,
    transform: [{ scale: 1 }],
  };
  return { initialValues, animations };
};
```

**Layout transitions (reordering, resizing):**
```typescript
import { Layout, LinearTransition } from 'react-native-reanimated';

// Smooth layout changes when items reorder
<Animated.View layout={LinearTransition.springify()}>

// Custom layout transition
<Animated.View layout={Layout.duration(300).springify()}>
```

**Staggered list pattern:**
```typescript
{items.map((item, index) => (
  <Animated.View
    key={item.id}
    entering={FadeInDown.delay(index * 50).springify()}
    exiting={FadeOutUp}
    layout={LinearTransition.springify()}
  >
    <ItemCard item={item} />
  </Animated.View>
))}
```

**Output:** Layout animation patterns for mount, unmount, and reorder.

### Step 5: Document Threading Model

Explain the worklet threading model and its constraints.

**Thread architecture:**
| Thread | Purpose | Access |
|--------|---------|--------|
| JS Thread | React rendering, business logic | Full JS runtime |
| UI Thread | Animations, gesture handling | Worklet runtime only |
| Background | Heavy computation | `runOnUI`/`runOnJS` bridge |

**Worklet rules:**
- `'worklet'` functions run on UI thread — no React state, no async, no most APIs
- `runOnUI(() => { ... })()` — schedule work on UI thread from JS
- `runOnJS(callback)(args)` — schedule work on JS thread from worklet
- Shared values are the ONLY way to pass data between threads
- `runOnJS` is async — don't expect immediate result

**What you CAN do in worklets:**
- Math operations, interpolation
- Read/write shared values
- Call other worklet functions
- Use Reanimated utility functions

**What you CANNOT do in worklets:**
- Call React hooks
- Access React state/props (use shared values instead)
- Make API calls or use async/await
- Use console.log (use `runOnJS(console.log)` for debugging)
- Access most JS standard library (Date, RegExp, etc.)

**Output:** Threading model documentation with do/don't reference.

### Step 6: Create Pattern Library Document

Compile all patterns into a searchable reference.

**Document structure:**
- Shared value patterns (from Step 1)
- Animation composition (from Step 2)
- Gesture coordination (from Step 3)
- Layout animations (from Step 4)
- Threading model (from Step 5)
- Quick reference table: pattern name → use case → code snippet
- Common mistakes and how to fix them

**Output:** Complete worklet pattern library document.

---

## Quality Criteria

- All animation patterns must run on UI thread (`'worklet'` verified)
- No `runOnJS` calls in hot animation paths
- Gesture-to-animation handoff must be seamless (no frame drops)
- Layout animations must handle rapid add/remove without glitches
- Every pattern must include reduced-motion consideration

---

*Squad Apex — Reanimated Worklet Patterns Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-reanimated-worklet-patterns
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All patterns must run on UI thread (worklet verified)"
    - "No runOnJS calls in hot animation paths"
    - "Gesture-to-animation handoff is seamless"
    - "Layout animations handle rapid operations without glitches"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@motion-eng` or `@apex-lead` |
| Artifact | Worklet pattern library with shared values, composition, gestures, layout animations, and threading guide |
| Next action | Apply patterns in feature implementation or validate with `gesture-test-suite` |
