---
name: threejs
description: Build, debug, and optimize Three.js applications. Covers WebGL/WebGPU rendering, glTF assets, color management, postprocessing, shaders, interaction, and performance. Use when writing Three.js code, fixing rendering issues, or optimizing 3D web apps.
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
- **Init**: renderer, scene, camera → attach to canvas
- **Resize**: renderer + camera + composer + DPR cap
- **Loop**: `requestAnimationFrame` or `setAnimationLoop` (XR)
- **Teardown**: stop loop, remove listeners, dispose ALL GPU resources

Target API: `createThreeApp(canvas) → { resize(), update(dt), render(), dispose() }`

### Color and Postprocessing

- Direct rendering → renderer output settings apply
- EffectComposer (WebGL) → OutputPass handles tone mapping; passes needing sRGB (e.g., FXAA) go AFTER OutputPass
- WebGL and WebGPU postprocessing stacks differ — do not mix
- Color textures → sRGB; data textures (normal, roughness) → linear

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
- Global style/formatting changes — keep diffs minimal

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
composer.addPass(new OutputPass()); // Tone mapping + sRGB — ALWAYS last

function render() { composer.render(); }
function resize() { composer.setSize(w, h); }
```

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
| First-frame stutter | Shader compilation — add warmup pass |
| Memory growth | Resources not disposed on unmount |
| Stretched on resize | Camera aspect not updated, composer not resized |

## Deep Reference

Load on demand from `references/`:
- `color-management.md` — Linear workflow, texture color spaces
- `postprocessing.md` — EffectComposer, pass ordering, WebGPU differences
- `performance.md` — Draw calls, fill rate, VRAM, GC, profiling
- `loaders.md` — glTF, DRACO, KTX2, async patterns, caching
- `shaders.md` — GLSL, onBeforeCompile, node materials
- `interaction.md` — Raycasting, GPU picking, controls
- `disposal.md` — Full teardown patterns, reference counting

## Scripts

Run without loading source:
- `scripts/three-doctor.mjs` — Repo pattern audit
- `scripts/asset-audit.mjs` — Asset size report
