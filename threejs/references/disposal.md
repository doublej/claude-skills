# Disposal and Cleanup

## Why Disposal Matters

Three.js objects hold GPU resources (buffers, textures, shaders) that won't be garbage collected automatically. Failing to dispose causes:
- Memory leaks
- GPU memory exhaustion
- Mobile crashes
- Performance degradation over time

## Full Teardown Pattern

```ts
export function createThreeApp(canvas: HTMLCanvasElement) {
  const renderer = new THREE.WebGLRenderer({ canvas });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera();
  let rafId: number | null = null;

  // ... setup code ...

  function dispose() {
    // 1. Stop render loop
    if (rafId != null) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }

    // 2. Remove event listeners
    window.removeEventListener("resize", onResize);
    canvas.removeEventListener("pointermove", onPointerMove);

    // 3. Dispose scene contents
    disposeObject3D(scene);

    // 4. Dispose render targets
    if (composer) {
      composer.dispose();
      composer.renderTarget1.dispose();
      composer.renderTarget2.dispose();
    }

    // 5. Dispose renderer
    renderer.dispose();
    renderer.forceContextLoss();
  }

  return { dispose };
}
```

## Dispose Helpers

```ts
const TEXTURE_KEYS = [
  "map", "normalMap", "roughnessMap", "metalnessMap", "aoMap", "emissiveMap",
  "alphaMap", "envMap", "lightMap", "bumpMap", "displacementMap",
  "clearcoatMap", "clearcoatNormalMap", "clearcoatRoughnessMap",
  "iridescenceMap", "iridescenceThicknessMap",
  "sheenColorMap", "sheenRoughnessMap",
  "specularMap", "specularIntensityMap", "specularColorMap",
  "transmissionMap", "thicknessMap"
];

export function disposeMaterial(mat: THREE.Material) {
  const anyMat = mat as any;

  // Dispose textures
  for (const k of TEXTURE_KEYS) {
    const tex = anyMat[k];
    if (tex?.isTexture) tex.dispose();
  }

  // Dispose uniforms with textures
  if (anyMat.uniforms) {
    Object.values(anyMat.uniforms).forEach((u: any) => {
      if (u?.value?.isTexture) u.value.dispose();
    });
  }

  mat.dispose();
}

export function disposeObject3D(root: THREE.Object3D) {
  root.traverse((obj) => {
    // Geometry
    const mesh = obj as THREE.Mesh;
    if (mesh.geometry) {
      mesh.geometry.dispose();
    }

    // Material(s)
    const mat = (mesh as any).material;
    if (Array.isArray(mat)) {
      mat.forEach(disposeMaterial);
    } else if (mat) {
      disposeMaterial(mat);
    }

    // Skeleton
    if ((obj as THREE.SkinnedMesh).skeleton) {
      (obj as THREE.SkinnedMesh).skeleton.dispose();
    }
  });
}
```

## Shared Resource Pattern

For resources used by multiple objects, use reference counting:

```ts
class TextureCache {
  private textures = new Map<string, { tex: THREE.Texture; refs: number }>();

  async get(url: string): Promise<THREE.Texture> {
    const existing = this.textures.get(url);
    if (existing) {
      existing.refs++;
      return existing.tex;
    }

    const tex = await loadTexture(url);
    this.textures.set(url, { tex, refs: 1 });
    return tex;
  }

  release(url: string) {
    const entry = this.textures.get(url);
    if (!entry) return;

    entry.refs--;
    if (entry.refs <= 0) {
      entry.tex.dispose();
      this.textures.delete(url);
    }
  }

  disposeAll() {
    this.textures.forEach(({ tex }) => tex.dispose());
    this.textures.clear();
  }
}
```

## React/SPA Considerations

```tsx
useEffect(() => {
  const app = createThreeApp(canvasRef.current!);

  return () => {
    app.dispose();
  };
}, []);
```

**Warning**: In React StrictMode, effects run twice. Ensure dispose is idempotent:

```ts
function dispose() {
  if (disposed) return;
  disposed = true;
  // ... cleanup
}
```

## What Needs Disposal

| Type | Method |
|------|--------|
| Geometry | `geometry.dispose()` |
| Material | `material.dispose()` |
| Texture | `texture.dispose()` |
| Render Target | `renderTarget.dispose()` |
| WebGLRenderer | `renderer.dispose()` |
| EffectComposer | `composer.dispose()` |
| PMREMGenerator | `pmrem.dispose()` |
| Controls | `controls.dispose()` |
| AnimationMixer | `mixer.stopAllAction()` |

## Verifying Cleanup

```ts
// Before dispose
console.log("Before:", renderer.info.memory);

// After dispose
console.log("After:", renderer.info.memory);
// Should show reduced counts

// Check for leaks on route changes
let prevGeo = 0, prevTex = 0;
setInterval(() => {
  const { geometries, textures } = renderer.info.memory;
  if (geometries > prevGeo || textures > prevTex) {
    console.warn("Possible leak:", { geometries, textures });
  }
  prevGeo = geometries;
  prevTex = textures;
}, 5000);
```

## Common Mistakes

1. **Disposing shared textures** — Use reference counting
2. **Not stopping render loop** — Causes orphan RAF callbacks
3. **Forgetting render targets** — EffectComposer has internal targets
4. **Leaving event listeners** — Window/document listeners persist
5. **Not calling forceContextLoss** — Optional but helps release WebGL context
