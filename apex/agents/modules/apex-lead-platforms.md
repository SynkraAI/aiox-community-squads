# apex-lead — Platform Standards & Motion Language (Lazy-Loaded)

> **Load condition:** Only when cross-platform work, `*platform-check`, or motion audit.
> **Parent:** `agents/apex-lead.md`

```yaml
platform_standards:
  web:
    framework: "Next.js 15+ (App Router)"
    rendering: "React 19+ (Server Components default)"
    styling: "CSS Modules + Design Tokens"
    animation: "Framer Motion (spring physics)"
    testing: "Vitest + Playwright + Storybook"
    breakpoints: ["320px (mobile-s)", "375px (mobile)", "768px (tablet)", "1024px (desktop)", "1440px (desktop-l)", "2560px (4k)"]

  mobile:
    framework: "React Native (New Architecture)"
    tooling: "Expo SDK 52+"
    animation: "Reanimated 3 (spring physics)"
    navigation: "Expo Router"
    testing: "Jest + Detox"
    targets: ["iOS 16+", "Android 13+"]

  spatial:
    frameworks: ["Three.js", "React Three Fiber", "WebXR"]
    platforms: ["VisionOS", "Meta Quest", "WebXR browsers"]
    rendering: "WebGPU (with WebGL fallback)"
    interaction: "Gaze + Hand tracking + Controllers"

motion_language:
  philosophy: >
    Motion is a language, not decoration. Every animation communicates
    something to the user — entry, exit, relationship, feedback, status.

  spring_defaults:
    gentle:
      stiffness: 120
      damping: 14
      mass: 1
      use_for: "Modals, overlays, page transitions"
    responsive:
      stiffness: 300
      damping: 20
      mass: 1
      use_for: "Buttons, toggles, interactive elements"
    snappy:
      stiffness: 500
      damping: 25
      mass: 0.8
      use_for: "Micro-interactions, feedback, quick responses"
    bouncy:
      stiffness: 200
      damping: 10
      mass: 1
      use_for: "Celebratory moments, success states, delight"

  interaction_types:
    enter: "Element appears — scale from 0.95, fade from 0, spring gentle"
    exit: "Element disappears — scale to 0.95, fade to 0, duration 150ms"
    transform: "Element changes — spring responsive, no opacity change"
    feedback: "User action acknowledged — spring snappy, scale 0.97 → 1"
    status: "State change communicated — color transition 200ms, no motion if reduced"

  rules:
    - "NEVER use linear easing for UI animations"
    - "NEVER exceed 300ms for feedback animations"
    - "ALWAYS provide prefers-reduced-motion fallback"
    - "ALWAYS test animations at 0.25x speed"
    - "PREFER spring physics over duration+easing"
    - "MATCH animation energy to interaction energy"
```
