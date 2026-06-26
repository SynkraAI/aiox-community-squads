# Task: screen-transition-architecture

```yaml
id: screen-transition-architecture
version: "1.0.0"
title: "Screen Transition Architecture"
description: >
  Designs custom screen transitions for React Native navigation.
  Implements shared element transitions, custom stack animations,
  modal presentations, and tab switch effects using Reanimated.
  Ensures 60fps on UI thread, respects reduced-motion preferences,
  and handles gesture-driven transitions (swipe-back).
elicit: false
owner: mobile-eng
executor: mobile-eng
outputs:
  - Transition inventory (per navigation type)
  - Shared element transition specifications
  - Custom animation implementations (Reanimated)
  - Gesture-driven transition handlers
  - Reduced-motion fallback plan
  - Transition specification document
```

---

## When This Task Runs

This task runs when:
- Default React Navigation transitions need customization
- Shared element transitions are needed (list-to-detail, profile avatars)
- Custom modal presentations are required (bottom sheet, full-screen cover)
- Gesture-driven navigation (swipe-back) needs custom behavior
- Transitions are janky or running on JS thread
- `*screen-transition` or `*transition-arch` is invoked

This task does NOT run when:
- The animation is within a single screen (use `animation-architecture`)
- The task is about gesture design without navigation (use `gesture-design`)
- The issue is web-only transitions (delegate to `@motion-eng`)

---

## Execution Steps

### Step 1: Inventory Current Transitions

Map all navigation transitions in the app by type.

| Navigation Type | Current Transition | Target Transition | Priority |
|----------------|-------------------|-------------------|----------|
| Stack push | Default slide | Custom spring slide | Medium |
| Stack pop | Default slide | Gesture-driven + spring | High |
| Modal present | Default slide-up | Bottom sheet + backdrop | High |
| Modal dismiss | Default slide-down | Gesture-driven dismiss | High |
| Tab switch | None (instant) | Cross-fade | Low |
| Shared element | None | Hero animation | High |

For each transition, note:
- Current FPS (is it janky?)
- Thread (JS or UI?)
- Duration and easing
- Gesture support (can user drive it?)

**Output:** Complete transition inventory with improvement targets.

### Step 2: Design Shared Element Transitions

Implement hero animations that create visual continuity between screens.

**Architecture:**
```typescript
// Using react-native-shared-element or React Navigation 7 shared transitions
import { SharedElement } from 'react-navigation-shared-element';

// Source screen (list item)
<SharedElement id={`item.${item.id}.photo`}>
  <Image source={item.photo} style={styles.thumbnail} />
</SharedElement>

// Destination screen (detail)
<SharedElement id={`item.${item.id}.photo`}>
  <Image source={item.photo} style={styles.hero} />
</SharedElement>
```

**Shared element design rules:**
- Tag shared elements with unique, stable IDs
- Only share elements that provide visual continuity (images, titles, avatars)
- Limit to 3 shared elements per transition (performance)
- Provide a fade fallback if shared element transition fails
- Handle aspect ratio changes between source and destination

**Transition configuration:**
```typescript
const transitionSpec = {
  animation: 'spring',
  config: {
    damping: 20,
    stiffness: 300,
    mass: 0.8,
    overshootClamping: false,
    restDisplacementThreshold: 0.01,
    restSpeedThreshold: 0.01,
  },
};
```

**Output:** Shared element transition specifications for each list→detail pair.

### Step 3: Implement Custom Stack Transitions

Build custom push/pop animations using Reanimated.

**Custom transition animation:**
```typescript
import { CardStyleInterpolators } from '@react-navigation/stack';
import Animated, {
  interpolate,
  useAnimatedStyle,
} from 'react-native-reanimated';

const customTransition = {
  cardStyleInterpolator: ({ current, next, layouts }) => {
    'worklet';
    const translateX = interpolate(
      current.progress,
      [0, 1],
      [layouts.screen.width, 0]
    );
    const opacity = interpolate(
      current.progress,
      [0, 0.5, 1],
      [0, 0.5, 1]
    );

    return {
      cardStyle: {
        transform: [{ translateX }],
        opacity,
      },
    };
  },
  transitionSpec: {
    open: { animation: 'spring', config: { damping: 20, stiffness: 300 } },
    close: { animation: 'spring', config: { damping: 20, stiffness: 300 } },
  },
};
```

**Transition patterns by screen type:**
| Screen Type | Push Animation | Pop Animation |
|-------------|---------------|---------------|
| Standard detail | Slide from right + fade | Slide to right + fade |
| Sub-page | Slide from right (full) | Swipe-back gesture |
| Modal | Slide from bottom | Swipe-down gesture |
| Alert/dialog | Scale up + backdrop | Scale down + backdrop |
| Full-screen media | Cross-fade | Pinch-to-dismiss |

**Output:** Custom transition implementations per screen type.

### Step 4: Implement Gesture-Driven Transitions

Make transitions interactive — user drags to control progress.

**Swipe-back gesture (iOS-style):**
```typescript
const gestureConfig = {
  gestureEnabled: true,
  gestureDirection: 'horizontal',
  gestureResponseDistance: {
    horizontal: 50,  // Activate within 50px from edge
  },
  cardOverlayEnabled: true,
};
```

**Bottom sheet modal with gesture dismiss:**
- Pan gesture controls modal position
- Velocity threshold: if velocity > 500, dismiss
- Distance threshold: if dragged > 50% of height, dismiss
- Spring back if thresholds not met
- Backdrop opacity interpolates with drag progress

**Key implementation rules:**
- All gesture calculations must use `'worklet'` directive
- Use `useSharedValue` for progress tracking
- Interpolate visual properties from gesture progress (0 to 1)
- Handle edge cases: quick flick, slow drag, mid-gesture cancel
- Snap points for bottom sheet: expanded, half, collapsed, dismissed

**Output:** Gesture-driven transition handlers with threshold configuration.

### Step 5: Plan Reduced-Motion Fallbacks

Respect `prefers-reduced-motion` for users who need it.

**Detection:**
```typescript
import { AccessibilityInfo } from 'react-native';

const [reduceMotion, setReduceMotion] = useState(false);

useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
  const sub = AccessibilityInfo.addEventListener(
    'reduceMotionChanged',
    setReduceMotion
  );
  return () => sub.remove();
}, []);
```

**Fallback strategy:**
| Normal Transition | Reduced-Motion Fallback |
|-------------------|------------------------|
| Spring slide (300ms) | Instant (0ms) or fade (150ms) |
| Shared element hero | Cross-fade (150ms) |
| Bottom sheet spring | Instant snap to position |
| Gesture-driven | Still gesture-driven but instant snap |
| Tab cross-fade | Instant switch |

**Output:** Reduced-motion fallback plan per transition type.

### Step 6: Document Transition Architecture

Compile the complete transition specification.

**Documentation includes:**
- Transition inventory table (from Step 1)
- Shared element specifications (from Step 2)
- Custom animation code (from Step 3)
- Gesture handler configurations (from Step 4)
- Reduced-motion fallbacks (from Step 5)
- Spring physics parameters used
- Platform-specific notes (iOS vs Android differences)

**Output:** Complete transition specification document.

---

## Quality Criteria

- All transitions must run at 60fps on UI thread (no JS thread animations)
- Shared element transitions must handle interrupted gestures gracefully
- Gesture-driven transitions must have velocity and distance thresholds
- Reduced-motion fallbacks must be provided for every transition
- Spring parameters must produce natural-feeling motion

---

*Squad Apex — Screen Transition Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-screen-transition-architecture
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All transitions must run at 60fps on UI thread"
    - "Shared elements handle interrupted gestures gracefully"
    - "Gesture thresholds defined for velocity and distance"
    - "Reduced-motion fallbacks provided for every transition"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@motion-eng` or `@apex-lead` |
| Artifact | Transition architecture with shared elements, custom animations, gesture handlers, and reduced-motion plan |
| Next action | Validate with `gesture-test-suite` via `@qa-xplatform` or integrate motion design via `@motion-eng` |
