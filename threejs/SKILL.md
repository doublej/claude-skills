---
name: threejs
description: "Unified Three.js/WebGL/WebGPU development skill. Use when: (1) building Three.js applications \u2014 rendering, glTF assets, color management, postprocessing, shaders, interaction, performance; (2) animating 3D/DOM with Theatre.js \u2014 timelines, keyframes, Studio editor, @theatre/r3f; (3) choosing animation easing and timing; (4) working with 3D space, positioning, transforms, or camera setup. Covers vanilla, React Three Fiber, and production deployment."
---

# Three.js Development

## Before Writing Code

1. **Detect repo setup** (do not guess):
   - Framework: vanilla / React (R3F) / Vue / Svelte / Next.js
   - Bundler: Vite / Webpack / Next / custom
   - Three.js revision: check `node_modules/three/package.json`
   - Import style: `three/addons/...` or `three/examples/jsm/...`

2. **Run repo audit** (if scripts available):
   ```bash
   node scripts/three-doctor.mjs
   ```

3. **Identify lifecycle ownership**:
   - Where is the render loop?
   - What triggers mount/unmount?
   - Are there route transitions or XR loops?

## Core Rules

### Lifecycle Contract

Every Three.js integration MUST have:
- **Init**: renderer, scene, camera -> attach to canvas
- **Resize**: renderer + camera + composer + DPR cap
- **Loop**: `requestAnimationFrame` or `setAnimationLoop` (XR)
- **Teardown**: stop loop, remove listeners, dispose ALL GPU resources

Target API: `createThreeApp(canvas) -> { resize(), update(dt), render(), dispose() }`

### Color and Postprocessing

- Direct rendering -> renderer output settings apply
- EffectComposer (WebGL) -> OutputPass handles tone mapping; passes needing sRGB (e.g., FXAA) go AFTER OutputPass
- WebGL and WebGPU postprocessing stacks differ -- do not mix
- Color textures -> sRGB; data textures (normal, roughness) -> linear

### Assets

- Prefer glTF/GLB
- Enable DRACO/KTX2/meshopt only if already used or required
- Always dispose loaded resources on unmount

### Safety

- No network commands without explicit request
- No dependency changes without verification plan
- Match existing repo patterns

## What NOT to Do

- Rewrite architecture or switch frameworks unless requested
- Add dependencies when Three.js built-ins suffice
- Global style/formatting changes -- keep diffs minimal

## 3D Space & Positioning

### Coordinate System

Three.js uses a **right-handed** coordinate system:
- **X**: right
- **Y**: up
- **Z**: toward viewer (out of screen)

### Transform Properties

Every `Object3D` has:

| Property | Type | Notes |
|----------|------|-------|
| `position` | `Vector3` | World units from parent origin |
| `rotation` | `Euler` | Radians, default order `'XYZ'` |
| `quaternion` | `Quaternion` | No gimbal lock, synced with `rotation` |
| `scale` | `Vector3` | Multiplier per axis |

Setting `rotation` updates `quaternion` and vice versa.

### Local vs World Space

```ts
// position is local (relative to parent)
child.position.set(2, 0, 0);

// Get world coordinates
const worldPos = new THREE.Vector3();
child.getWorldPosition(worldPos);

// Convert between spaces
object.localToWorld(vec);
object.worldToLocal(vec);
```

### Parent-Child Hierarchy

Children inherit parent transforms. Use `Group` for logical grouping:

```ts
const group = new THREE.Group();
group.position.set(5, 0, 0);

const child = new THREE.Mesh(geo, mat);
child.position.set(0, 2, 0); // world position = (5, 2, 0)
group.add(child);
scene.add(group);
```

### Cameras

```ts
// Perspective (most 3D scenes)
const cam = new THREE.PerspectiveCamera(50, w / h, 0.1, 200);
cam.position.set(0, 1.5, 4);
cam.lookAt(0, 0, 0);

// Orthographic (2D-like, UI overlays, isometric)
const size = 10;
const cam = new THREE.OrthographicCamera(-size * aspect, size * aspect, size, -size, 0.1, 1000);
```

`PerspectiveCamera(fov, aspect, near, far)` -- fov is vertical in degrees. Keep `near` as large and `far` as small as possible to avoid z-fighting.

### Common Positioning Patterns

```ts
// Look at target
camera.lookAt(target.position);

// Orbit around point
const angle = time * speed;
obj.position.set(Math.cos(angle) * radius, 0, Math.sin(angle) * radius);

// Smooth interpolation (call each frame)
object.position.lerp(targetPos, 0.05);
object.quaternion.slerp(targetQuat, 0.05);

// Get camera forward direction
const dir = new THREE.Vector3();
camera.getWorldDirection(dir);

// Center model at origin
const box = new THREE.Box3().setFromObject(model);
const center = box.getCenter(new THREE.Vector3());
model.position.sub(center);
```

### Units & Scale

No fixed unit system. Common conventions:
- **Architectural / games**: 1 unit = 1 metre (physics engines assume this)
- **Small objects**: 1 unit = 1 centimetre

Keep scale consistent across all models in a scene.

## Quick Reference

### Lifecycle (Vanilla)

```ts
import * as THREE from "three";

export function createThreeApp(canvas: HTMLCanvasElement) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, canvas.clientWidth / canvas.clientHeight, 0.1, 200);
  camera.position.set(0, 1.5, 4);

  let rafId: number | null = null;

  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  function update(dt: number) { /* animate */ }
  function render() { renderer.render(scene, camera); }

  function tick(prev = performance.now()) {
    rafId = requestAnimationFrame(() => tick(prev));
    const now = performance.now();
    update(Math.min((now - prev) / 1000, 0.05));
    render();
  }

  function dispose() {
    if (rafId != null) cancelAnimationFrame(rafId);
    renderer.dispose();
  }

  return { resize, update, render, dispose, scene, camera };
}
```

### Disposal Helper

```ts
const TEXTURE_KEYS = [
  "map", "normalMap", "roughnessMap", "metalnessMap", "aoMap", "emissiveMap",
  "alphaMap", "envMap", "lightMap", "bumpMap", "displacementMap",
];

export function disposeMaterial(mat: THREE.Material) {
  for (const k of TEXTURE_KEYS) {
    const tex = (mat as any)[k];
    if (tex?.isTexture) tex.dispose();
  }
  mat.dispose();
}

export function disposeObject3D(root: THREE.Object3D) {
  root.traverse((obj) => {
    const mesh = obj as THREE.Mesh;
    if (mesh.geometry) mesh.geometry.dispose();
    const mat = mesh.material;
    if (Array.isArray(mat)) mat.forEach(disposeMaterial);
    else if (mat) disposeMaterial(mat);
  });
}
```

### glTF Loading (DRACO/KTX2)

```ts
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";
import { KTX2Loader } from "three/addons/loaders/KTX2Loader.js";

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath("https://www.gstatic.com/draco/versioned/decoders/1.5.6/");

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath("https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/basis/");
ktx2Loader.detectSupport(renderer);

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);
gltfLoader.setKTX2Loader(ktx2Loader);

gltfLoader.load("model.glb", (gltf) => {
  gltf.scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });
  scene.add(gltf.scene);
});
```

### Environment Map (PMREM)

```ts
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";

const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

new RGBELoader().load("environment.hdr", (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;
  scene.environment = envMap;
  scene.background = envMap;
  texture.dispose();
  pmremGenerator.dispose();
});
```

### InstancedMesh

```ts
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial();
const mesh = new THREE.InstancedMesh(geometry, material, 1000);

const dummy = new THREE.Object3D();
const color = new THREE.Color();

for (let i = 0; i < 1000; i++) {
  dummy.position.set(Math.random() * 100, 0, Math.random() * 100);
  dummy.updateMatrix();
  mesh.setMatrixAt(i, dummy.matrix);
  mesh.setColorAt(i, color.setHSL(Math.random(), 0.8, 0.5));
}
mesh.instanceMatrix.needsUpdate = true;
mesh.instanceColor!.needsUpdate = true;
scene.add(mesh);
```

### Raycasting

```ts
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

canvas.addEventListener("pointermove", (e) => {
  pointer.x = (e.offsetX / canvas.clientWidth) * 2 - 1;
  pointer.y = -(e.offsetY / canvas.clientHeight) * 2 + 1;
});

function checkIntersections() {
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(scene.children, true);
  if (hits.length > 0) {
    console.log("Hit:", hits[0].object.name);
  }
}
```

### Postprocessing (WebGL)

```ts
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(w, h), 1.5, 0.4, 0.85));
composer.addPass(new OutputPass()); // Tone mapping + sRGB -- ALWAYS last

function render() { composer.render(); }
function resize() { composer.setSize(w, h); }
```

## Animation & Motion

### Theatre.js Integration

Visual timeline animation editor for web. Provides Studio UI (dev) + programmatic playback (prod).

```ts
import { getProject, types } from '@theatre/core'
import studio from '@theatre/studio'

if (import.meta.env.DEV) studio.initialize()

const project = getProject('My Project')
const sheet = project.sheet('Main')
const obj = sheet.object('Box', {
  position: types.compound({
    x: types.number(0), y: types.number(0), z: types.number(0)
  }),
  opacity: types.number(1, { range: [0, 1] })
})

obj.onValuesChange((v) => {
  mesh.position.set(v.position.x, v.position.y, v.position.z)
})

project.ready.then(() => sheet.sequence.play({ iterationCount: Infinity }))
```

#### R3F Pattern

```tsx
import { editable as e, SheetProvider, PerspectiveCamera } from '@theatre/r3f'
import extension from '@theatre/r3f/dist/extension'

if (import.meta.env.DEV) { studio.initialize(); studio.extend(extension) }

<Canvas>
  <SheetProvider sheet={sheet}>
    <PerspectiveCamera theatreKey="Camera" makeDefault position={[5, 5, -5]} fov={75} />
    <e.mesh theatreKey="Cube">
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </e.mesh>
  </SheetProvider>
</Canvas>
```

#### Critical Rules

- **Studio is AGPL** -- dev only, wrap in `import.meta.env.DEV`
- **Production**: export state JSON from Studio, load via `getProject('Name', { state })`
- Every `e.*` needs a unique `theatreKey`
- Wait for `project.ready` before playback
- R3F: must call `studio.extend(extension)` for 3D controls

| Shortcut | Action |
|----------|--------|
| `Alt + \` | Toggle Studio |
| `Space` | Play/pause |
| `Shift + drag` | Focus range |
| Right-click prop | Sequence/keyframe |

### Easing Quick Reference

| Easing | Duration | Use Case |
|--------|----------|----------|
| **Ease-out** | 200-500ms | UI appearing (default, 80% of cases) |
| **Ease-in-out** | 300-500ms | Position changes |
| **Ease-in** | 150-300ms | UI disappearing |
| **Linear** | Variable | Spinners, loaders |
| **Back** | 400-600ms | Playful overshoot |
| **Bounce** | 800-1200ms | Landing, dropping |
| **Elastic** | 800-1200ms | Spring, attention |
| **Spring** | Variable | Gesture response |

**Key rules:**
- Under 100ms = glitch; over 700ms = sluggish
- Bounce/elastic need 800ms+ to settle
- Animate only `transform` and `opacity` (GPU-accelerated)
- Always support `prefers-reduced-motion`
- Mobile 300ms baseline, desktop 200ms baseline

## Quality Gates

### Build & Runtime
- [ ] `npm run build` succeeds
- [ ] `npm run dev` renders without console errors

### Visual
- [ ] No blank screen on load
- [ ] Resize works (no stretched output)
- [ ] DPR intentional (no accidental 3x-4x on mobile)

### Color & Postprocessing
- [ ] No double tone mapping
- [ ] Texture color spaces correct (color=sRGB, data=linear)
- [ ] Composer resized correctly

### Performance
- [ ] Draw calls within expected range
- [ ] Repeated meshes use instancing/batching
- [ ] Shadow maps sized appropriately

### Memory & Teardown
- [ ] Unmount stops render loop
- [ ] Event listeners removed
- [ ] GPU resources disposed

## Troubleshooting

| Symptom | Likely Cause |
|---------|--------------|
| Blank screen | Missing camera position, wrong near/far, no lights for PBR |
| Too dark | Missing env light, double output transform |
| Washed out | Wrong texture color spaces, tone mapping issues |
| Neon/saturated | Double tone mapping |
| First-frame stutter | Shader compilation -- add warmup pass |
| Memory growth | Resources not disposed on unmount |
| Stretched on resize | Camera aspect not updated, composer not resized |

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `color-management.md` | Linear workflow, texture color spaces, tone mapping |
| `postprocessing.md` | EffectComposer, pass ordering, WebGPU differences |
| `performance.md` | Draw calls, fill rate, VRAM, GC, profiling |
| `loaders.md` | glTF, DRACO, KTX2, async patterns, caching |
| `shaders.md` | GLSL, onBeforeCompile, node materials (TSL) |
| `interaction.md` | Raycasting, GPU picking, controls (orbit, fly, drag) |
| `disposal.md` | Full teardown patterns, reference counting |
| `theatre-js.md` | Core API, prop types, Studio, React/R3F integration, production, audio sync |
| `animation-easing.md` | Easing families, timing guidelines, platform standards, real-world examples |

## Scripts

Run without loading source:
- `scripts/three-doctor.mjs` -- Repo pattern audit
- `scripts/asset-audit.mjs` -- Asset size report
