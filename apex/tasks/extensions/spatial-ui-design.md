# Task: spatial-ui-design

```yaml
id: spatial-ui-design
version: "1.0.0"
title: "Spatial UI Design"
description: >
  Designs spatial user interfaces for VisionOS, WebXR, and immersive
  environments. Covers window placement, ornament patterns, volumetric
  UI, gaze/gesture interaction, depth and layering in 3D space,
  glass material language, and comfortable viewing ergonomics.
  Bridges Apple's spatial design principles with web-based 3D.
elicit: false
owner: spatial-eng
executor: spatial-eng
outputs:
  - Spatial UI layout system (windows, volumes, spaces)
  - Gaze and gesture interaction patterns
  - Depth and layering architecture
  - Glass/material language for spatial UI
  - Ergonomic comfort guidelines
  - Spatial UI specification document
```

---

## When This Task Runs

This task runs when:
- Designing UI for VisionOS or WebXR headsets
- Creating floating/volumetric interfaces in 3D
- Need spatial layout system (windows in 3D space)
- Designing gaze-based interaction patterns
- Building immersive dashboard or data visualization
- `*spatial-ui` or `*visionos-design` is invoked

This task does NOT run when:
- WebXR session configuration (use `webxr-session-setup`)
- Standard 3D scene rendering (use `scene-architecture`)
- 2D responsive layout (use CSS tasks via `@css-eng`)

---

## Execution Steps

### Step 1: Define Spatial Layout System

Design window placement and spatial hierarchy.

**Spatial container types (VisionOS model):**

| Container | Description | Example |
|-----------|-------------|---------|
| Window | 2D content floating in space | Settings panel, text editor |
| Volume | 3D content in bounded box | Product viewer, 3D model |
| Full Space | Immersive 3D environment | Virtual room, game world |

**Layout rules:**
- Windows default to 1.5m distance from user (comfortable reading)
- Maximum window width: ~1.2m (comfortable peripheral vision)
- Stacked windows: 0.1m depth offset between layers
- Volumes placed on surfaces (table, floor) or floating
- Full Space replaces entire environment

**Spatial grid system:**
```
Z-axis (depth):
  Near plane:   0.5m (minimum comfortable distance)
  Content zone: 1.0m - 2.0m (primary interaction)
  Context zone: 2.0m - 5.0m (ambient information)
  Far plane:    5.0m+ (environment, skybox)

Y-axis (vertical):
  Eye level:    0° (center of attention)
  Comfortable:  -30° to +20° (primary content)
  Peripheral:   -60° to +40° (secondary content)
  Avoid:        > ±60° (neck strain)
```

**Output:** Spatial layout system.

### Step 2: Design Gaze and Gesture Interaction

Map interaction patterns for spatial input.

**Input modalities:**

| Input | Platform | Precision | Use For |
|-------|----------|-----------|---------|
| Gaze + pinch | VisionOS | High | Primary selection |
| Hand tracking | Quest 3 | Medium | Grab, point, pinch |
| Controllers | Quest, PCVR | Highest | Precise interaction |
| Head ray | All XR | Low | Fallback selection |

**Gaze interaction patterns:**

| Pattern | Behavior |
|---------|----------|
| Hover | Gaze on element → highlight (0.3s dwell) |
| Select | Gaze + pinch gesture (VisionOS) or trigger (Quest) |
| Scroll | Gaze on scrollable + two-finger drag |
| Dismiss | Look away + pinch or flick gesture |
| Drag | Pinch + move hand in space |

**Feedback principles:**
- Gaze hover: subtle scale (1.0 → 1.02) + highlight glow
- Selection: haptic pulse + visual confirmation
- Drag: object follows hand with spring physics
- Error: gentle bounce-back + audio cue

**Affordance indicators:**
```
Interactive element: subtle border glow on gaze
Grabbable element: hand icon on approach
Scrollable area: subtle scroll indicator on edges
Disabled element: reduced opacity, no gaze response
```

**Output:** Gaze and gesture interaction patterns.

### Step 3: Design Depth and Layering

Establish visual hierarchy using spatial depth.

**Depth hierarchy (front to back):**

| Layer | Depth | Content | Example |
|-------|-------|---------|---------|
| Alerts | -0.05m | Urgent notifications | Error, confirmation |
| Overlay | 0m | Modals, popovers | Settings, picker |
| Primary | +0.02m | Main content | App window |
| Secondary | +0.1m | Supporting content | Side panels |
| Background | +0.5m | Environment, ambient | Skybox, room |

**Depth cues:**
- Closer objects: sharper, brighter, larger shadow
- Farther objects: slight blur, lower contrast, no shadow
- Focus target: full resolution, highest contrast
- Peripheral: reduced detail (foveated rendering)

**Implementation in R3F:**
```tsx
function SpatialPanel({ depth, children }) {
  return (
    <group position={[0, 0, -depth]}>
      <RoundedBox args={[1.2, 0.8, 0.02]} radius={0.02}>
        <meshPhysicalMaterial
          color="#ffffff"
          transmission={0.9}
          roughness={0.1}
          thickness={0.02}
          envMapIntensity={0.5}
        />
      </RoundedBox>
      <Html transform position={[0, 0, 0.015]}>
        {children}
      </Html>
    </group>
  );
}
```

**Output:** Depth and layering architecture.

### Step 4: Define Material Language

Establish glass/material system for spatial UI elements.

**Material tiers (inspired by VisionOS):**

| Material | Opacity | Blur | Use |
|----------|---------|------|-----|
| Ultra thin | 10% | Heavy | Background panels |
| Thin | 20% | Medium | Secondary content |
| Regular | 40% | Medium | Primary windows |
| Thick | 60% | Light | Focused content |
| Chrome | 80% | None | Toolbar, controls |

**Glass material in Three.js:**
```typescript
const glassMaterial = new THREE.MeshPhysicalMaterial({
  color: '#ffffff',
  transmission: 0.92,
  roughness: 0.05,
  metalness: 0,
  thickness: 0.5,
  ior: 1.5,
  clearcoat: 1,
  clearcoatRoughness: 0.1,
  envMapIntensity: 0.3,
});
```

**Vibrancy (text over glass):**
- Light mode glass: dark text (#1e293b) over light blur
- Dark mode glass: light text (#f1f5f9) over dark blur
- Minimum contrast: 4.5:1 (WCAG AA) even over dynamic backgrounds

**Output:** Glass/material language.

### Step 5: Establish Ergonomic Guidelines

Define comfort boundaries for spatial UI.

**Comfort zones:**

| Parameter | Comfortable | Acceptable | Avoid |
|-----------|------------|------------|-------|
| Viewing distance | 1-2m | 0.5-3m | < 0.5m, > 5m |
| Vertical angle | -15° to +15° | -30° to +20° | > ±40° |
| Horizontal angle | -30° to +30° | -55° to +55° | > ±70° |
| Text size at 1m | 16-24pt | 12-32pt | < 10pt |
| Interaction duration | < 30min | 30-60min | > 60min (without break) |
| Head movement per action | 0° (gaze only) | < 15° | > 30° |

**Anti-patterns:**
- Forcing users to look up for extended periods
- Placing critical UI outside comfortable zone
- Requiring large head movements for frequent actions
- Small text at distance (< 12pt at 2m)
- Rapid depth changes (causes discomfort)
- Moving objects toward user face (triggers flinch)

**Content pacing:**
- Allow 0.5s for eye refocus between depth layers
- Animate transitions between depths (200-400ms)
- Never teleport content to different depth
- Provide resting position at comfortable distance

**Output:** Ergonomic comfort guidelines.

### Step 6: Document Spatial UI Architecture

Compile the complete specification.

**Documentation includes:**
- Spatial layout system (from Step 1)
- Interaction patterns (from Step 2)
- Depth architecture (from Step 3)
- Material language (from Step 4)
- Ergonomic guidelines (from Step 5)
- Platform-specific notes (VisionOS vs Quest vs WebXR)
- Testing on device checklist

**Output:** Spatial UI specification document.

---

## Quality Criteria

- All UI elements within ergonomic comfort zones
- Glass materials maintain text contrast (WCAG AA)
- Gaze interaction provides clear visual feedback
- Depth hierarchy is consistent and intuitive
- No discomfort-inducing patterns (rapid depth, close objects)
- Layout works across VisionOS, Quest 3, and desktop fallback

---

*Squad Apex — Spatial UI Design Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-spatial-ui-design
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "UI within ergonomic comfort zones"
    - "Glass materials maintain WCAG AA contrast"
    - "Gaze interaction has visual feedback"
    - "No discomfort patterns"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@interaction-dsgn` or `@apex-lead` |
| Artifact | Spatial UI specification with layout, interaction, materials, and ergonomics |
| Next action | Implement spatial components via `@spatial-eng` R3F patterns or validate UX via `@interaction-dsgn` |
