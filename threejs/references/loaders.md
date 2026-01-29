# Asset Loading

## LoadingManager

```ts
const manager = new THREE.LoadingManager();

manager.onStart = (url, loaded, total) => console.log(`Loading: ${url}`);
manager.onLoad = () => console.log("All assets loaded");
manager.onProgress = (url, loaded, total) => {
  updateProgressBar((loaded / total) * 100);
};
manager.onError = (url) => console.error(`Failed: ${url}`);

const textureLoader = new THREE.TextureLoader(manager);
const gltfLoader = new GLTFLoader(manager);
```

## glTF/GLB

```ts
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const loader = new GLTFLoader();
loader.load("model.glb", (gltf) => {
  scene.add(gltf.scene);

  // Animations
  if (gltf.animations.length > 0) {
    const mixer = new THREE.AnimationMixer(gltf.scene);
    gltf.animations.forEach(clip => mixer.clipAction(clip).play());
  }
});
```

### With DRACO Compression

```ts
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath("https://www.gstatic.com/draco/versioned/decoders/1.5.6/");
dracoLoader.preload();

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);
```

### With KTX2 Textures

```ts
import { KTX2Loader } from "three/addons/loaders/KTX2Loader.js";

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath("https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/basis/");
ktx2Loader.detectSupport(renderer);

const gltfLoader = new GLTFLoader();
gltfLoader.setKTX2Loader(ktx2Loader);
```

### With Meshopt

```ts
import { MeshoptDecoder } from "three/addons/libs/meshopt_decoder.module.js";

const gltfLoader = new GLTFLoader();
gltfLoader.setMeshoptDecoder(MeshoptDecoder);
```

## HDR Environment

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

## Textures

```ts
const loader = new THREE.TextureLoader();

// Color texture (sRGB)
const colorMap = loader.load("color.jpg", (tex) => {
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
});

// Data texture (linear)
const normalMap = loader.load("normal.jpg", (tex) => {
  tex.colorSpace = THREE.LinearSRGBColorSpace;
});
```

## Async/Promise Pattern

```ts
function loadGLTF(url: string): Promise<GLTF> {
  return new Promise((resolve, reject) => {
    new GLTFLoader().load(url, resolve, undefined, reject);
  });
}

// Usage
async function init() {
  const [model, env] = await Promise.all([
    loadGLTF("model.glb"),
    loadHDR("environment.hdr")
  ]);
  scene.add(model.scene);
  scene.environment = env;
}
```

## Process Loaded Models

```ts
loader.load("model.glb", (gltf) => {
  const model = gltf.scene;

  // Enable shadows
  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  // Find specific mesh
  const head = model.getObjectByName("Head");

  // Center and scale
  const box = new THREE.Box3().setFromObject(model);
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  model.position.sub(center);
  model.scale.setScalar(1 / Math.max(size.x, size.y, size.z));

  scene.add(model);
});
```

## Caching

```ts
THREE.Cache.enabled = true;

// Custom cache
class AssetCache {
  private textures = new Map<string, THREE.Texture>();
  private models = new Map<string, THREE.Object3D>();

  async getTexture(key: string, url: string) {
    if (this.textures.has(key)) return this.textures.get(key)!;
    const tex = await loadTexture(url);
    this.textures.set(key, tex);
    return tex;
  }

  async getModel(key: string, url: string) {
    if (this.models.has(key)) return this.models.get(key)!.clone();
    const gltf = await loadGLTF(url);
    this.models.set(key, gltf.scene);
    return gltf.scene.clone();
  }

  dispose() {
    this.textures.forEach(t => t.dispose());
    this.textures.clear();
    this.models.clear();
  }
}
```

## Error Handling

```ts
async function loadWithRetry(url: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await loadGLTF(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```
