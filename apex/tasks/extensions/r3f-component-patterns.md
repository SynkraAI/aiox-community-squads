# Task: r3f-component-patterns

```yaml
id: r3f-component-patterns
version: "1.0.0"
title: "R3F Component Patterns"
description: >
  Designs reusable React Three Fiber component patterns for 3D scenes.
  Covers declarative scene composition, Drei helper usage, custom
  hooks for 3D state, instanced rendering for performance, portal
  patterns, and 3D↔2D integration (HTML overlays). Establishes
  conventions for building maintainable 3D component libraries
  that follow React idioms.
elicit: false
owner: spatial-eng
executor: spatial-eng
outputs:
  - R3F component architecture guide
  - Drei helper usage patterns
  - Custom 3D hooks library
  - Instanced rendering patterns
  - HTML overlay / 3D-2D bridge patterns
  - R3F component specification document
```

---

## When This Task Runs

This task runs when:
- Building reusable 3D components in React Three Fiber
- Need Drei helpers for common 3D patterns
- Creating custom hooks for 3D state management
- Rendering large numbers of similar objects (instancing)
- Mixing HTML UI with 3D content
- `*r3f-patterns` or `*r3f-components` is invoked

This task does NOT run when:
- Scene-level architecture decisions (use `scene-architecture`)
- Custom shader development (use `shader-design`)
- WebXR session configuration (use `webxr-session-setup`)

---

## Execution Steps

### Step 1: R3F Component Architecture

Establish conventions for 3D component design.

**Component categories:**

| Category | Examples | Convention |
|----------|---------|------------|
| Primitives | `<Box>`, `<Sphere>`, `<Plane>` | Thin wrappers over Drei |
| Composite | `<Building>`, `<Character>` | Compose primitives + logic |
| Environment | `<Lighting>`, `<Sky>`, `<Ground>` | Scene-level, one per scene |
| Interactive | `<DraggableObject>`, `<Clickable>` | Include event handlers |
| Effect | `<Particles>`, `<Trail>` | Visual effects, no collision |
| UI | `<Billboard>`, `<HtmlOverlay>` | 2D content in 3D space |

**Component template:**
```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { MeshProps } from '@react-three/fiber';

interface InteractiveBoxProps extends MeshProps {
  color?: string;
  speed?: number;
}

export function InteractiveBox({
  color = '#4299e1',
  speed = 1,
  ...meshProps
}: InteractiveBoxProps) {
  const ref = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame((_, delta) => {
    if (ref.current) {
      ref.current.rotation.y += delta * speed;
    }
  });

  return (
    <mesh
      ref={ref}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      {...meshProps}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={hovered ? 'hotpink' : color} />
    </mesh>
  );
}
```

**Rules:**
- Props extend `MeshProps` for standard Three.js mesh properties
- Use `useRef` for direct Three.js object access
- Use `useFrame` for per-frame updates (NOT setInterval)
- Forward `...meshProps` for position/rotation/scale
- Clean up resources in useEffect return

**Output:** R3F component architecture guide.

### Step 2: Drei Helper Patterns

Leverage Drei's 50+ helpers for common 3D patterns.

**Essential Drei helpers:**

| Helper | Use Case | Example |
|--------|----------|---------|
| `<OrbitControls>` | Camera orbit with mouse/touch | Scene exploration |
| `<Environment>` | HDR environment maps | Realistic reflections |
| `<Text3D>` | 3D text with fonts | Headings in 3D |
| `<Html>` | 2D HTML in 3D space | Labels, tooltips |
| `<Float>` | Gentle floating animation | Hero objects |
| `<MeshTransmissionMaterial>` | Glass/liquid material | Glass effects |
| `<useGLTF>` | Load 3D models | GLTF/GLB assets |
| `<ContactShadows>` | Soft ground shadows | Product showcase |
| `<Sparkles>` | Particle sparkle effect | Magic, premium feel |
| `<MeshReflectorMaterial>` | Reflective floor | Gallery, showcase |

**Model loading pattern:**
```tsx
import { useGLTF, Clone } from '@react-three/drei';

function Model({ url, ...props }) {
  const { scene } = useGLTF(url);
  return <Clone object={scene} {...props} />;
}

// Preload for instant display
useGLTF.preload('/models/product.glb');
```

**Text in 3D:**
```tsx
import { Text3D, Center } from '@react-three/drei';

function Title({ children }) {
  return (
    <Center>
      <Text3D
        font="/fonts/inter-bold.json"
        size={0.5}
        height={0.1}
        curveSegments={12}
      >
        {children}
        <meshStandardMaterial color="#1e293b" />
      </Text3D>
    </Center>
  );
}
```

**Output:** Drei helper usage patterns.

### Step 3: Custom 3D Hooks

Build reusable hooks for 3D state management.

**Animation hook:**
```typescript
function useSpringAnimation(target: number, config = { stiffness: 100, damping: 10 }) {
  const value = useRef(0);
  const velocity = useRef(0);

  useFrame((_, delta) => {
    const displacement = target - value.current;
    const springForce = displacement * config.stiffness;
    const dampingForce = velocity.current * config.damping;
    velocity.current += (springForce - dampingForce) * delta;
    value.current += velocity.current * delta;
  });

  return value;
}
```

**Hover/click interaction hook:**
```typescript
function useInteraction() {
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);

  const bind = {
    onPointerOver: (e: ThreeEvent) => { e.stopPropagation(); setHovered(true); },
    onPointerOut: () => setHovered(false),
    onClick: (e: ThreeEvent) => { e.stopPropagation(); setClicked(prev => !prev); },
  };

  useEffect(() => {
    document.body.style.cursor = hovered ? 'pointer' : 'auto';
    return () => { document.body.style.cursor = 'auto'; };
  }, [hovered]);

  return { hovered, clicked, bind };
}
```

**Viewport-aware visibility:**
```typescript
function useVisibility(ref: RefObject<THREE.Object3D>) {
  const [visible, setVisible] = useState(true);

  useFrame(({ camera }) => {
    if (!ref.current) return;
    const frustum = new THREE.Frustum();
    frustum.setFromProjectionMatrix(
      new THREE.Matrix4().multiplyMatrices(
        camera.projectionMatrix,
        camera.matrixWorldInverse
      )
    );
    setVisible(frustum.containsPoint(ref.current.position));
  });

  return visible;
}
```

**Output:** Custom 3D hooks library.

### Step 4: Instanced Rendering

Render thousands of similar objects efficiently.

**InstancedMesh pattern:**
```tsx
import { useRef, useMemo } from 'react';
import { InstancedMesh, Object3D, Color } from 'three';

function Particles({ count = 1000 }) {
  const ref = useRef<InstancedMesh>(null);
  const dummy = useMemo(() => new Object3D(), []);

  useEffect(() => {
    if (!ref.current) return;
    for (let i = 0; i < count; i++) {
      dummy.position.set(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      );
      dummy.updateMatrix();
      ref.current.setMatrixAt(i, dummy.matrix);
    }
    ref.current.instanceMatrix.needsUpdate = true;
  }, [count]);

  return (
    <instancedMesh ref={ref} args={[undefined, undefined, count]}>
      <sphereGeometry args={[0.05, 8, 8]} />
      <meshStandardMaterial color="#4299e1" />
    </instancedMesh>
  );
}
```

**When to use instancing:**

| Objects | Technique | Draw Calls |
|---------|-----------|-----------|
| < 100 | Regular meshes | 100 |
| 100-10K | InstancedMesh | 1 |
| 10K-1M | InstancedMesh + LOD | 1 + LOD switches |
| > 1M | GPU particles (compute shader) | 1 |

**Drei Instances helper:**
```tsx
import { Instances, Instance } from '@react-three/drei';

function Trees({ positions }) {
  return (
    <Instances limit={1000}>
      <cylinderGeometry args={[0.1, 0.2, 1]} />
      <meshStandardMaterial color="brown" />
      {positions.map((pos, i) => (
        <Instance key={i} position={pos} />
      ))}
    </Instances>
  );
}
```

**Output:** Instanced rendering patterns.

### Step 5: HTML Overlay / 3D-2D Bridge

Integrate HTML content with 3D scenes.

**Drei Html component:**
```tsx
import { Html } from '@react-three/drei';

function ProductCard({ product, position }) {
  return (
    <group position={position}>
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#e2e8f0" />
      </mesh>
      <Html
        position={[0, 1.2, 0]}
        center
        distanceFactor={8}
        occlude
        transform
      >
        <div className="bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
          <h3 className="font-semibold">{product.name}</h3>
          <p className="text-sm text-slate-600">{product.price}</p>
        </div>
      </Html>
    </group>
  );
}
```

**Portal pattern (render 3D inside 2D layout):**
```tsx
import { Canvas } from '@react-three/fiber';

function Page() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="prose">
        <h1>Product</h1>
        <p>Description here...</p>
      </div>
      <div className="aspect-square rounded-xl overflow-hidden">
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ProductScene />
        </Canvas>
      </div>
    </div>
  );
}
```

**Rules:**
- Use `distanceFactor` to scale HTML with distance
- Use `occlude` to hide HTML behind 3D objects
- Minimize HTML elements in 3D (expensive DOM operations)
- Use `transform` for CSS3D (better perf than DOM overlay)
- Canvas needs explicit dimensions (not auto-sizing)

**Output:** HTML overlay / 3D-2D bridge patterns.

### Step 6: Document R3F Component Architecture

Compile the complete specification.

**Documentation includes:**
- Component architecture guide (from Step 1)
- Drei patterns (from Step 2)
- Custom hooks library (from Step 3)
- Instancing patterns (from Step 4)
- HTML overlay patterns (from Step 5)
- Performance guidelines (draw calls, geometry reuse, texture atlasing)
- File organization conventions

**Output:** R3F component specification document.

---

## Quality Criteria

- Components follow React idioms (props, hooks, composition)
- Drei helpers used for standard patterns (no reinventing)
- Instanced rendering for > 100 similar objects
- Custom hooks are reusable across scenes
- HTML overlays don't degrade 3D performance
- All components clean up resources on unmount

---

*Squad Apex — R3F Component Patterns Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-r3f-component-patterns
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Components follow React idioms"
    - "Drei used for standard patterns"
    - "Instancing for 100+ similar objects"
    - "Resources cleaned up on unmount"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | R3F component patterns with Drei, hooks, instancing, and HTML overlays |
| Next action | Implement in project via `@react-eng` or optimize via `@perf-eng` |
