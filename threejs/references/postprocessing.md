# Postprocessing

## EffectComposer (WebGL)

```ts
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
// ... effect passes ...
composer.addPass(new OutputPass()); // ALWAYS last
```

## Pass Ordering Rules

1. **RenderPass** — first (renders scene to buffer)
2. **Effect passes** — bloom, DOF, SSAO, etc.
3. **OutputPass** — last (tone mapping + sRGB)
4. **FXAA/SMAA** — after OutputPass if needed (they expect sRGB input)

## Common Passes

```ts
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { BokehPass } from "three/addons/postprocessing/BokehPass.js";
import { SSAOPass } from "three/addons/postprocessing/SSAOPass.js";
import { SMAAPass } from "three/addons/postprocessing/SMAAPass.js";

// Bloom
const bloom = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,   // strength
  0.4,   // radius
  0.85   // threshold
);

// Depth of Field
const bokeh = new BokehPass(scene, camera, {
  focus: 1.0,
  aperture: 0.025,
  maxblur: 0.01
});

// SSAO
const ssao = new SSAOPass(scene, camera, width, height);
ssao.kernelRadius = 16;
ssao.minDistance = 0.005;
ssao.maxDistance = 0.1;

// Anti-aliasing (after OutputPass)
const smaa = new SMAAPass(width, height);
```

## Resize Handling

```ts
function onResize() {
  const w = window.innerWidth;
  const h = window.innerHeight;

  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();

  composer.setSize(w, h);

  // Some passes need explicit resize
  bloom.resolution.set(w, h);
}
```

## Custom Passes

### ShaderPass

```ts
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const customShader = {
  uniforms: {
    tDiffuse: { value: null },
    amount: { value: 1.0 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float amount;
    varying vec2 vUv;
    void main() {
      vec4 color = texture2D(tDiffuse, vUv);
      gl_FragColor = color * amount;
    }
  `
};

const pass = new ShaderPass(customShader);
composer.addPass(pass);
```

## WebGPU Postprocessing

WebGPU uses a different API — do NOT mix with WebGL passes.

```ts
import { PostProcessing } from "three/addons/tsl/display/PostProcessing.js";
import { bloom, dof, toneMapping } from "three/addons/tsl/display/PostProcessing.js";

const postProcessing = new PostProcessing(renderer);
postProcessing.outputNode = bloom(toneMapping(scene.colorNode));
```

## Selective Bloom

Render bloom-only objects to separate layer:

```ts
const BLOOM_LAYER = 1;
const bloomLayer = new THREE.Layers();
bloomLayer.set(BLOOM_LAYER);

glowingMesh.layers.enable(BLOOM_LAYER);

// Custom bloom pass that only affects layer
const bloomComposer = new EffectComposer(renderer);
bloomComposer.renderToScreen = false;
bloomComposer.addPass(new RenderPass(scene, camera));
bloomComposer.addPass(bloomPass);

// Final composer combines
const finalPass = new ShaderPass(
  new THREE.ShaderMaterial({
    uniforms: {
      baseTexture: { value: null },
      bloomTexture: { value: bloomComposer.renderTarget2.texture }
    },
    // ... combine shader
  })
);
```

## Performance Tips

1. **Lower resolution** for expensive passes (bloom, DOF)
2. **Skip passes** when not needed (toggle `pass.enabled`)
3. **Reduce samples** for SSAO, SSR
4. **Single render target** when possible

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Double bright | Tone mapping twice | Remove renderer tone mapping when using OutputPass |
| Washed out | Missing OutputPass | Add OutputPass as last pass |
| Aliased after bloom | FXAA before OutputPass | Move FXAA after OutputPass |
| Bloom not visible | Wrong threshold | Lower bloom threshold |
