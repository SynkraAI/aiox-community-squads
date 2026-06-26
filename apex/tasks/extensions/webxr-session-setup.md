# Task: webxr-session-setup

```yaml
id: webxr-session-setup
version: "1.0.0"
title: "WebXR Session Setup"
description: >
  Configures WebXR Device API sessions for immersive VR and AR
  experiences. Covers session modes (inline, immersive-vr, immersive-ar),
  reference spaces, input sources, feature detection, R3F XR integration
  via @react-three/xr, and progressive enhancement for non-XR devices.
  Handles headset-specific quirks (Quest, Vision Pro, PCVR).
elicit: false
owner: spatial-eng
executor: spatial-eng
outputs:
  - WebXR feature detection and capability matrix
  - Session initialization patterns (VR/AR/inline)
  - Reference space configuration
  - Input source handling (controllers, hands, gaze)
  - R3F XR integration patterns (@react-three/xr)
  - WebXR session specification document
```

---

## When This Task Runs

This task runs when:
- Project needs VR/AR capabilities via WebXR
- Integrating @react-three/xr with R3F scenes
- Supporting multiple XR devices (Quest, Vision Pro, PCVR)
- Need progressive enhancement for XR features
- `*webxr-setup` or `*xr-session` is invoked

This task does NOT run when:
- Standard 3D rendering without XR (use `scene-architecture`)
- Shader development (use `shader-design`)
- 3D performance issues (use `3d-performance-audit`)

---

## Execution Steps

### Step 1: Feature Detection and Capability Matrix

Detect WebXR support and available features.

**Feature detection:**
```typescript
async function detectXRCapabilities() {
  if (!navigator.xr) {
    return { supported: false, reason: 'WebXR API not available' };
  }

  const capabilities = {
    'immersive-vr': await navigator.xr.isSessionSupported('immersive-vr'),
    'immersive-ar': await navigator.xr.isSessionSupported('immersive-ar'),
    'inline': true, // Always supported if WebXR exists
  };

  return { supported: true, capabilities };
}
```

**Device capability matrix:**

| Device | VR | AR | Hand tracking | Controllers | Passthrough |
|--------|----|----|--------------|-------------|-------------|
| Quest 3 | Yes | Yes | Yes | Yes | Yes (color) |
| Quest Pro | Yes | Yes | Yes | Yes | Yes (color) |
| Vision Pro | Yes | Yes | Yes | No (gestures) | Yes |
| Pico 4 | Yes | No | Yes | Yes | No |
| PCVR (SteamVR) | Yes | No | Varies | Yes | No |
| Mobile AR | No | Yes | No | No | N/A |

**Output:** WebXR capability matrix.

### Step 2: Session Initialization Patterns

Configure XR session creation for each mode.

**Session modes:**

| Mode | Use Case | Reference Space |
|------|----------|----------------|
| `inline` | 3D content in page (no headset) | `viewer` |
| `immersive-vr` | Full VR experience | `local-floor` or `bounded-floor` |
| `immersive-ar` | AR overlay on real world | `local-floor` |

**R3F XR integration (@react-three/xr):**
```tsx
import { XR, createXRStore } from '@react-three/xr';

const xrStore = createXRStore({
  depthSensing: true,
  handTracking: true,
});

function App() {
  return (
    <>
      <button onClick={() => xrStore.enterVR()}>Enter VR</button>
      <button onClick={() => xrStore.enterAR()}>Enter AR</button>
      <Canvas>
        <XR store={xrStore}>
          <Scene />
        </XR>
      </Canvas>
    </>
  );
}
```

**Session lifecycle:**
1. Check support → 2. Request session → 3. Create reference space → 4. Start render loop → 5. Handle end

**Output:** Session initialization patterns.

### Step 3: Reference Space Configuration

Configure spatial tracking for different experiences.

**Reference space types:**

| Type | Origin | Use Case |
|------|--------|----------|
| `viewer` | Head position | Inline content, 360 photos |
| `local` | Device position at start | Seated experiences |
| `local-floor` | Floor level at start | Standing, room-scale |
| `bounded-floor` | Floor + boundary | Guardian-aware experiences |
| `unbounded` | Large-scale tracking | AR outdoor, large spaces |

**Floor detection:**
```typescript
async function setupReferenceSpace(session: XRSession) {
  try {
    // Prefer floor-level reference
    return await session.requestReferenceSpace('local-floor');
  } catch {
    // Fallback: manual floor offset
    const space = await session.requestReferenceSpace('local');
    const floorOffset = new XRRigidTransform(
      { x: 0, y: -1.6, z: 0 } // Average standing height
    );
    return space.getOffsetReferenceSpace(floorOffset);
  }
}
```

**Output:** Reference space configuration.

### Step 4: Input Source Handling

Handle controllers, hand tracking, and gaze input.

**Input sources in R3F:**
```tsx
import { useXRInputSourceState, XROrigin } from '@react-three/xr';

function Hands() {
  const leftHand = useXRInputSourceState('hand', 'left');
  const rightHand = useXRInputSourceState('hand', 'right');

  return (
    <XROrigin>
      {leftHand && <HandModel hand={leftHand} />}
      {rightHand && <HandModel hand={rightHand} />}
    </XROrigin>
  );
}
```

**Input priority:**
1. Hand tracking (most natural, Quest 3, Vision Pro)
2. Controllers (most precise, Quest, PCVR)
3. Gaze + pinch (Vision Pro primary)
4. Screen touch (mobile AR, inline)

**Interaction patterns:**

| Action | Controller | Hand | Gaze |
|--------|-----------|------|------|
| Select | Trigger press | Pinch | Dwell/tap |
| Grab | Grip press | Grab gesture | N/A |
| Point | Ray from controller | Index finger ray | Head ray |
| Scroll | Thumbstick | Pinch + move | Head nod |

**Output:** Input source handling patterns.

### Step 5: Progressive Enhancement

Design fallback experiences for non-XR devices.

**Enhancement tiers:**

| Tier | Device | Experience |
|------|--------|-----------|
| Full XR | Quest 3, Vision Pro | Immersive 3D environment |
| Desktop 3D | PC/Mac with mouse | Orbit camera, click interaction |
| Mobile 3D | Phone/tablet | Touch orbit, gyroscope |
| 2D fallback | No WebGL | Static images, 2D interface |

**Implementation:**
```tsx
function ExperienceRouter() {
  const { capabilities } = useXRCapabilities();

  if (capabilities['immersive-vr']) {
    return <ImmersiveExperience />;
  }
  if (hasWebGL()) {
    return <Desktop3DExperience />;
  }
  return <FallbackExperience />;
}
```

**Output:** Progressive enhancement patterns.

### Step 6: Document WebXR Architecture

Compile the complete specification.

**Documentation includes:**
- Capability matrix (from Step 1)
- Session patterns (from Step 2)
- Reference spaces (from Step 3)
- Input handling (from Step 4)
- Progressive enhancement (from Step 5)
- Device-specific quirks and workarounds
- Performance budget for XR (90fps VR, 72fps Quest)

**Output:** WebXR session specification document.

---

## Quality Criteria

- XR session works on Quest 3 and Vision Pro
- Graceful fallback on non-XR devices (no crashes)
- Input handling supports controllers AND hand tracking
- Reference space correctly detects floor level
- Performance maintains 72fps+ on Quest, 90fps on PCVR
- All XR features behind capability checks

---

*Squad Apex — WebXR Session Setup Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-webxr-session-setup
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "XR sessions initialize on supported devices"
    - "Graceful fallback on non-XR devices"
    - "Input handling covers controllers + hands"
    - "72fps+ on Quest, 90fps on PCVR"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | WebXR session architecture with R3F integration |
| Next action | Implement XR scene via `@spatial-eng` scene-architecture or integrate with app via `@react-eng` |
