# Task: moti-animation-architecture

```yaml
id: moti-animation-architecture
version: "1.0.0"
title: "Moti Animation Architecture"
description: >
  Designs cross-platform animation architecture using Moti (by Fernando
  Rojo). Implements universal animations that work on both web and
  React Native with the same API. Covers MotiView/MotiText patterns,
  animation variants, presence transitions, staggered animations,
  and Moti + NativeWind integration. Produces animation patterns
  that eliminate platform-specific animation code.
elicit: false
owner: cross-plat-eng
executor: cross-plat-eng
outputs:
  - Moti installation and configuration
  - Animation variant system design
  - Presence transition patterns (mount/unmount)
  - Staggered animation patterns
  - Moti + NativeWind integration
  - Animation architecture specification document
```

---

## When This Task Runs

This task runs when:
- Cross-platform animations needed (same API for web and native)
- Migrating from platform-specific animation libraries to universal
- Building a shared animation system for a monorepo
- Presence animations needed (enter/exit for conditional rendering)
- `*moti-animations` or `*moti-arch` is invoked

This task does NOT run when:
- Native-only animations needing worklet control (use `reanimated-worklet-patterns`)
- Web-only animations (use `@motion-eng` with Framer Motion)
- Gesture-driven animations (use `gesture-design` first, then animate)

---

## Execution Steps

### Step 1: Install and Configure Moti

Set up Moti in the cross-platform monorepo.

**Installation:**
```bash
# In the shared UI package
cd packages/ui
npm install moti

# Moti depends on Reanimated (native) and framer-motion (web)
npm install react-native-reanimated  # Native
npm install framer-motion            # Web (auto-detected)
```

**How Moti works:**
| Platform | Animation Engine | Detection |
|----------|-----------------|-----------|
| React Native | Reanimated 3 | Automatic via Metro |
| Web | Framer Motion | Automatic via Webpack |

**Babel configuration (for Reanimated):**
```javascript
// babel.config.js
module.exports = {
  plugins: ['react-native-reanimated/plugin'],
};
```

**Key principle:** Write animations once with Moti → runs on Reanimated (native) or Framer Motion (web) automatically. No platform branching needed.

**Output:** Moti configured in monorepo with both animation engines.

### Step 2: Design Animation Variant System

Create reusable animation variants for consistent motion across the app.

**Variant definition pattern:**
```typescript
// packages/ui/src/animations/variants.ts
export const fadeIn = {
  from: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
  transition: { type: 'timing', duration: 300 },
};

export const slideUp = {
  from: { opacity: 0, translateY: 20 },
  animate: { opacity: 1, translateY: 0 },
  exit: { opacity: 0, translateY: -10 },
  transition: { type: 'spring', damping: 15, stiffness: 150 },
};

export const scaleIn = {
  from: { opacity: 0, scale: 0.9 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 },
  transition: { type: 'spring', damping: 20, stiffness: 200 },
};

export const slideFromRight = {
  from: { opacity: 0, translateX: 50 },
  animate: { opacity: 1, translateX: 0 },
  exit: { opacity: 0, translateX: -20 },
  transition: { type: 'spring', damping: 18, stiffness: 200 },
};
```

**Using variants in components:**
```tsx
import { MotiView } from 'moti';
import { slideUp } from '@ui/animations/variants';

function Card({ children }) {
  return (
    <MotiView {...slideUp}>
      {children}
    </MotiView>
  );
}
```

**Dynamic variants (state-driven):**
```tsx
import { MotiView } from 'moti';

function ExpandableCard({ isExpanded }) {
  return (
    <MotiView
      animate={{
        height: isExpanded ? 200 : 80,
        opacity: 1,
      }}
      transition={{ type: 'spring', damping: 15 }}
    >
      {children}
    </MotiView>
  );
}
```

**Variant naming convention:**
| Category | Variants | Purpose |
|----------|----------|---------|
| Enter | `fadeIn`, `slideUp`, `slideFromRight`, `scaleIn` | Component mount |
| Exit | `fadeOut`, `slideDown`, `slideToLeft`, `scaleOut` | Component unmount |
| State | `expanded`, `collapsed`, `selected`, `highlighted` | State changes |
| Feedback | `pulse`, `shake`, `bounce` | User action feedback |

**Output:** Animation variant system with reusable presets.

### Step 3: Implement Presence Transitions

Design enter/exit animations for conditionally rendered components.

**AnimatePresence pattern:**
```tsx
import { AnimatePresence, MotiView } from 'moti';

function NotificationBanner({ visible, message }) {
  return (
    <AnimatePresence>
      {visible && (
        <MotiView
          key="notification"
          from={{ opacity: 0, translateY: -50 }}
          animate={{ opacity: 1, translateY: 0 }}
          exit={{ opacity: 0, translateY: -50 }}
          transition={{ type: 'spring', damping: 15 }}
        >
          <Text>{message}</Text>
        </MotiView>
      )}
    </AnimatePresence>
  );
}
```

**Modal with presence animation:**
```tsx
function Modal({ visible, onClose, children }) {
  return (
    <AnimatePresence>
      {visible && (
        <>
          {/* Backdrop */}
          <MotiView
            key="backdrop"
            from={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            exit={{ opacity: 0 }}
            transition={{ type: 'timing', duration: 200 }}
            style={StyleSheet.absoluteFill}
          />
          {/* Content */}
          <MotiView
            key="modal"
            from={{ opacity: 0, scale: 0.9, translateY: 20 }}
            animate={{ opacity: 1, scale: 1, translateY: 0 }}
            exit={{ opacity: 0, scale: 0.95, translateY: 10 }}
            transition={{ type: 'spring', damping: 20 }}
          >
            {children}
          </MotiView>
        </>
      )}
    </AnimatePresence>
  );
}
```

**Presence animation rules:**
- Always provide `exit` animation (otherwise component disappears instantly)
- Use `key` prop on animated elements inside `AnimatePresence`
- `exit` should be quicker than `enter` (200ms vs 300ms)
- Modal backdrop should animate separately from content
- Handle interrupted animations (open/close in rapid succession)

**Output:** Presence transition patterns for modals, notifications, and conditional content.

### Step 4: Design Staggered Animations

Implement staggered animations for lists and groups.

**Stagger children pattern:**
```tsx
import { MotiView } from 'moti';

function StaggeredList({ items }) {
  return (
    <View>
      {items.map((item, index) => (
        <MotiView
          key={item.id}
          from={{ opacity: 0, translateY: 20 }}
          animate={{ opacity: 1, translateY: 0 }}
          transition={{
            type: 'spring',
            damping: 15,
            delay: index * 50, // 50ms stagger between items
          }}
        >
          <ListItem item={item} />
        </MotiView>
      ))}
    </View>
  );
}
```

**Skeleton loading pattern:**
```tsx
import { MotiView } from 'moti';

function Skeleton({ width, height }) {
  return (
    <MotiView
      from={{ opacity: 0.3 }}
      animate={{ opacity: 0.7 }}
      transition={{
        type: 'timing',
        duration: 1000,
        loop: true,
      }}
      style={{
        width,
        height,
        borderRadius: 4,
        backgroundColor: '#e0e0e0',
      }}
    />
  );
}
```

**Stagger configuration rules:**
- Max stagger delay: `items.length * 50ms` but cap at 500ms total
- First 5 items visible immediately, stagger the rest
- For large lists (>20 items), only stagger visible items
- Reverse stagger for exit animations (last in, first out)

**Output:** Staggered animation patterns for lists and loading states.

### Step 5: Integrate Moti with NativeWind

Combine Moti animations with NativeWind (Tailwind) styling.

**MotiView with className:**
```tsx
import { MotiView, MotiText } from 'moti';

function AnimatedCard({ children }) {
  return (
    <MotiView
      className="bg-white rounded-xl p-4 shadow-md"
      from={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: 'spring', damping: 15 }}
    >
      <MotiText className="text-lg font-bold text-gray-900">
        {children}
      </MotiText>
    </MotiView>
  );
}
```

**Animated + styled pattern:**
```tsx
// Static styles via NativeWind (className)
// Dynamic styles via Moti (animate prop)
<MotiView
  className="rounded-lg overflow-hidden"     // Static: NativeWind
  animate={{ height: expanded ? 300 : 100 }}  // Dynamic: Moti
  transition={{ type: 'spring', damping: 20 }}
>
```

**Integration rules:**
- Use NativeWind (`className`) for static styles (layout, colors, borders)
- Use Moti (`animate`) for dynamic/animated styles (opacity, transform, dimensions)
- NEVER animate via className changes (causes full re-render, no interpolation)
- Moti handles the transition; NativeWind handles the look

**Output:** Moti + NativeWind integration patterns.

### Step 6: Document Animation Architecture

Compile the complete animation architecture specification.

**Documentation includes:**
- Installation and configuration (from Step 1)
- Variant system reference (from Step 2)
- Presence transition patterns (from Step 3)
- Stagger patterns (from Step 4)
- NativeWind integration guide (from Step 5)
- Reduced-motion handling with Moti
- Performance notes (Reanimated worklet vs Framer Motion)

**Reduced-motion with Moti:**
```tsx
import { useReducedMotion } from 'moti';

function AnimatedComponent() {
  const reducedMotion = useReducedMotion();

  return (
    <MotiView
      animate={{ opacity: 1, translateY: 0 }}
      transition={
        reducedMotion
          ? { type: 'timing', duration: 0 }
          : { type: 'spring', damping: 15 }
      }
    />
  );
}
```

**Output:** Complete animation architecture specification document.

---

## Quality Criteria

- All animations must work identically on web and native
- Presence transitions must handle rapid show/hide without glitches
- Staggered animations must cap total delay at 500ms
- NativeWind classes must not conflict with Moti animate values
- Reduced-motion must be respected on all platforms

---

*Squad Apex — Moti Animation Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-moti-animation-architecture
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Animations work identically on web and native"
    - "Presence transitions handle rapid toggle without glitches"
    - "Staggered animations respect max delay cap"
    - "Reduced-motion respected on all platforms"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@motion-eng` or `@apex-lead` |
| Artifact | Moti animation architecture with variants, presence, stagger, and NativeWind integration |
| Next action | Apply in feature implementation or validate with visual regression via `@qa-visual` |
