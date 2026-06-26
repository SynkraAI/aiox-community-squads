# 3D Scene Quality & Performance Checklist

> **Agent:** spatial-eng (Paul) | **Gate:** QG-AX-3D

## Scene Structure

- [ ] Scene graph hierarchy is flat (max 3 levels deep)
- [ ] All meshes use descriptive names (not "Mesh001")
- [ ] Lights are minimal (max 3 dynamic lights per scene)
- [ ] Camera has defined near/far clipping planes

## Performance

- [ ] InstancedMesh used for repeated objects (>10 instances)
- [ ] LOD (Level of Detail) configured for complex geometries
- [ ] Textures are power-of-2 dimensions (512, 1024, 2048)
- [ ] Textures compressed (KTX2/Basis for web, ASTC for mobile)
- [ ] Draw calls < 100 per frame
- [ ] Triangle count within budget (mobile: <100K, desktop: <500K)
- [ ] No memory leaks (dispose geometries, materials, textures on unmount)

## Models & Assets

- [ ] Format is glTF/GLB (never OBJ or FBX in production)
- [ ] Models are draco-compressed for web delivery
- [ ] No unused vertices or degenerate triangles
- [ ] Materials use PBR (physically-based rendering) pipeline

## Shaders

- [ ] Custom shaders have uniform type validation
- [ ] No shader compilation stalls (precompile or warm-up)
- [ ] Fragment shader complexity is bounded (no nested loops)

## Accessibility

- [ ] Non-spatial fallback available for screen readers
- [ ] Keyboard navigation for interactive 3D elements
- [ ] Reduced-motion users get static alternative
- [ ] Color is not the only differentiator in 3D UI

## WebXR / Spatial

- [ ] Session type matches use case (immersive-vr or immersive-ar)
- [ ] Exit button accessible at all times during XR session
- [ ] Frame rate targets met (72fps VR, 60fps AR)
- [ ] Raycasting configured for pointer/hand interaction
