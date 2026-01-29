# Performance and Memory

Triage first, then optimize the dominant bottleneck.

## Quick Metrics

```ts
// Log periodically (throttled)
console.log({
  drawCalls: renderer.info.render.calls,
  triangles: renderer.info.render.triangles,
  textures: renderer.info.memory.textures,
  geometries: renderer.info.memory.geometries
});
```

## Bottleneck Categories

### 1) Too Many Draw Calls (CPU)

**Signals:** High `calls` + high CPU frame time; lowering resolution doesn't help

**Fixes (by leverage):**
- `InstancedMesh` for repeated objects
- Reduce material count / state changes
- Merge static meshes (build-time)
- Reduce separate skinned meshes

### 2) Too Many Pixels (Fill Rate)

**Signals:** Performance collapses on high DPI; improves when lowering DPR

**Fixes:**
- Cap DPR: `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`
- Lower resolution for expensive passes
- Reduce overdraw (transparent layers)
- Reduce shadow map resolution

### 3) Texture Pressure (VRAM)

**Signals:** Stutters on new content; GPU memory grows; mobile crashes

**Fixes:**
- Reduce texture resolution (2K max for web)
- Reduce unique textures/materials (atlases)
- Use GPU-compressed textures (KTX2)
- Reuse environment maps

### 4) GC Jank

**Signals:** Frequent GC pauses; many temp objects per frame

**Fixes:**
- Reuse `Vector3`, `Matrix4`, arrays
- Avoid per-frame `new` in hot paths
- Typed arrays for particles
- Throttle event handlers

### 5) Shader Compilation Stutter

**Signals:** "First time I look at it" hitch

**Fixes:**
- Compile/warm-up after assets load
- Defer non-critical effects until first paint

## Instancing

```ts
// Instead of 1000 meshes...
const mesh = new THREE.InstancedMesh(geometry, material, 1000);
const dummy = new THREE.Object3D();

for (let i = 0; i < 1000; i++) {
  dummy.position.set(x, y, z);
  dummy.rotation.set(rx, ry, rz);
  dummy.updateMatrix();
  mesh.setMatrixAt(i, dummy.matrix);
}
mesh.instanceMatrix.needsUpdate = true;
```

## Batching (Static Merge)

```ts
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

const geometries = meshes.map(m => {
  const geo = m.geometry.clone();
  geo.applyMatrix4(m.matrixWorld);
  return geo;
});
const merged = mergeGeometries(geometries);
const batchedMesh = new THREE.Mesh(merged, sharedMaterial);
```

## LOD (Level of Detail)

```ts
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);    // Close
lod.addLevel(medDetailMesh, 50);    // Medium
lod.addLevel(lowDetailMesh, 100);   // Far
scene.add(lod);
```

## Shadow Optimization

Shadows scale with:
- Shadow-casting lights count
- Shadow map resolution
- Casters/receivers count
- Update frequency

**Optimizations:**
- Reduce map size: `light.shadow.mapSize.set(1024, 1024)`
- Restrict casting: `mesh.castShadow = false` for unimportant objects
- Freeze for static scenes: `light.shadow.autoUpdate = false`
- Use baked shadows for static lighting

## Memory Leak Checklist

If memory grows on route changes:
- [ ] Render loops not duplicated
- [ ] Event listeners/observers removed
- [ ] Disposed: geometries, materials, textures
- [ ] Disposed: render targets, composers
- [ ] Disposed: PMREM generators

## Profiling

```ts
// GPU timing (requires EXT_disjoint_timer_query)
const query = renderer.extensions.get('EXT_disjoint_timer_query_webgl2');

// Frame timing
let lastTime = performance.now();
function tick() {
  const now = performance.now();
  const frameTime = now - lastTime;
  if (frameTime > 16.67) console.warn(`Frame took ${frameTime.toFixed(1)}ms`);
  lastTime = now;
  requestAnimationFrame(tick);
}
```

## Mobile Considerations

- Cap DPR at 2 (or 1.5 on low-end)
- Reduce shadow map to 512-1024
- Disable expensive postprocessing
- Use compressed textures (KTX2 with ETC/ASTC)
- Fewer lights, bake where possible

## Shipping Advice

- Make improvements measurable and reversible
- Document trade-offs (quality vs FPS)
- Few high-leverage changes > many micro-optimizations
