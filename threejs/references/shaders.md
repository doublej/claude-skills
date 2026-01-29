# Shaders

## ShaderMaterial Basics

```ts
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0xff0000) },
    uTexture: { value: texture }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec3 uColor;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(uColor * (0.5 + 0.5 * sin(uTime)), 1.0);
    }
  `
});

// Update in render loop
material.uniforms.uTime.value = clock.getElapsedTime();
```

## Built-in Uniforms

```glsl
// Matrices (auto-provided)
uniform mat4 modelMatrix;         // Object to world
uniform mat4 modelViewMatrix;     // Object to camera
uniform mat4 projectionMatrix;    // Camera projection
uniform mat4 viewMatrix;          // World to camera
uniform mat3 normalMatrix;        // Normal transform

// Camera (auto-provided)
uniform vec3 cameraPosition;

// Attributes (auto-provided)
attribute vec3 position;
attribute vec3 normal;
attribute vec2 uv;
```

## onBeforeCompile

Modify built-in materials without full rewrite:

```ts
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });

material.onBeforeCompile = (shader) => {
  // Add uniform
  shader.uniforms.uTime = { value: 0 };

  // Modify vertex shader
  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    `
    #include <begin_vertex>
    transformed.y += sin(position.x * 2.0 + uTime) * 0.5;
    `
  );

  // Store reference for updates
  material.userData.shader = shader;
};

// Update in loop
if (material.userData.shader) {
  material.userData.shader.uniforms.uTime.value = time;
}
```

## Common Injection Points

```glsl
// Vertex
#include <begin_vertex>      // After position is read
#include <project_vertex>    // After projection

// Fragment
#include <color_fragment>    // After color is determined
#include <output_fragment>   // Final output
```

## RawShaderMaterial

Full control, no auto-includes:

```ts
const material = new THREE.RawShaderMaterial({
  uniforms: { ... },
  vertexShader: `
    precision highp float;
    attribute vec3 position;
    uniform mat4 modelViewMatrix;
    uniform mat4 projectionMatrix;
    void main() {
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    precision highp float;
    void main() {
      gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
  `
});
```

## Node Materials (TSL)

Three.js Shading Language for WebGPU (and WebGL fallback):

```ts
import { MeshStandardNodeMaterial } from "three/nodes";
import { uv, sin, time, vec4 } from "three/tsl";

const material = new MeshStandardNodeMaterial();
material.colorNode = sin(uv().x.mul(10).add(time)).mul(0.5).add(0.5);
```

## GLSL Snippets

### Fresnel Effect
```glsl
float fresnel = pow(1.0 - dot(viewDirection, normal), 3.0);
```

### Noise
```glsl
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
}
```

### Smooth Minimum
```glsl
float smin(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}
```

### UV Distortion
```glsl
vec2 distortedUv = vUv + sin(vUv.y * 10.0 + uTime) * 0.1;
```

## Performance Tips

1. **Avoid conditionals** in fragment shaders
2. **Precompute** values in vertex shader when possible
3. **Use lowp/mediump** precision when acceptable
4. **Batch uniform updates** to avoid state changes
