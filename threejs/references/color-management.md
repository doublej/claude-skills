# Color Management

## Mental Model

- Lighting/PBR shading happens in **linear** space
- Color textures: authored in sRGB → decode to linear for shading
- Output: encode to display color space (usually sRGB)

## Repo Detection

Check for:
- `THREE.ColorManagement.enabled`
- `renderer.outputColorSpace` (newer) or `renderer.outputEncoding` (legacy)
- `texture.colorSpace` (newer) or `texture.encoding` (legacy)

**Do not mix patterns** without understanding repo setup.

## Texture Rules

| Type | Color Space |
|------|-------------|
| baseColor/albedo, emissive | sRGB |
| normal, roughness, metalness, AO, height | linear (no transform) |

If normal map treated as sRGB → shading looks wrong.

## Renderer Setup

```ts
// Three.js r152+
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

// Legacy (pre-r152)
renderer.outputEncoding = THREE.sRGBEncoding;
```

## Texture Color Spaces

```ts
// Color textures (sRGB)
texture.colorSpace = THREE.SRGBColorSpace;

// Data textures (linear)
normalMap.colorSpace = THREE.LinearSRGBColorSpace;
roughnessMap.colorSpace = THREE.LinearSRGBColorSpace;
metalnessMap.colorSpace = THREE.LinearSRGBColorSpace;
aoMap.colorSpace = THREE.LinearSRGBColorSpace;
```

## Tone Mapping Options

```ts
THREE.NoToneMapping           // Raw linear output
THREE.LinearToneMapping       // Simple linear
THREE.ReinhardToneMapping     // Filmic, less contrast
THREE.CineonToneMapping       // Filmic, more contrast
THREE.ACESFilmicToneMapping   // Industry standard (recommended)
THREE.AgXToneMapping          // Newer, better color preservation
THREE.NeutralToneMapping      // Minimal color shift
```

## Postprocessing Color Flow

### Direct Rendering
```
Scene (linear) → Tone Mapping → sRGB Output → Display
```

### With EffectComposer
```
Scene (linear) → RenderPass → [Effects] → OutputPass (tone map + sRGB) → Display
```

**Rule**: Only ONE place does tone mapping + sRGB conversion.

## Symptom → Cause

| Symptom | Likely Cause |
|---------|--------------|
| Too dark | Missing env light for PBR, or double output transform |
| Washed out | Wrong output transform or texture color spaces |
| Neon/saturated | Double tone mapping or wrong exposure |
| Purple/green normal maps | Normal map in sRGB instead of linear |

## Debug Steps

1. Disable postprocessing
2. Render known object with `MeshStandardMaterial` + simple HDRI
3. Compare before/after any color changes
4. Check `renderer.info` for unexpected settings

**Always compare against repo baseline.** Repos may intentionally deviate for stylized rendering.
