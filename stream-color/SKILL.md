---
name: stream-color
description: "GPU color correction for VR: shaders, color spaces, LUTs, Vulkan compute"
---

# GPU Color Correction for VR Streaming

<processing_chain>
## Processing Chain Order

Order matters. Wrong order = wrong colors, banding, or clipped highlights.

```
Encoded frame
  |
  1. Linearize (degamma / inverse transfer function)
  2. Color adjustments (brightness, contrast, saturation, hue -- all in linear space)
  3. Sharpen (in perceptual/gamma space for visual accuracy)
  4. Apply transfer function (sRGB gamma, PQ for HDR)
  5. Color space conversion (RGB -> YUV for encoder input)
  |
Encoder
```

**Why this order:**
- Adjustments in linear space are physically correct (additive light)
- Sharpening in perceptual space matches human edge perception
- YUV conversion is always last (encoder expects it, not a visual operation)
</processing_chain>

<transfer_functions>
### sRGB (SDR)

```glsl
// sRGB -> Linear (exact piecewise)
vec3 srgb_to_linear(vec3 c) {
    vec3 lo = c / 12.92;
    vec3 hi = pow((c + 0.055) / 1.055, vec3(2.4));
    return mix(hi, lo, step(c, vec3(0.04045)));
}

// Linear -> sRGB (exact piecewise)
vec3 linear_to_srgb(vec3 c) {
    vec3 lo = c * 12.92;
    vec3 hi = 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, step(c, vec3(0.0031308)));
}

// Fast approximation (when exact not needed)
vec3 srgb_to_linear_fast(vec3 c) { return pow(c, vec3(2.2)); }
vec3 linear_to_srgb_fast(vec3 c) { return pow(c, vec3(1.0 / 2.2)); }
```

**Pitfall**: ALVR uses `step()` with branchless `mix()` in WGSL -- avoid `if/else` per-channel in shaders for the same reason (GPU branch divergence).

### PQ / ST 2084 (HDR10)

```glsl
// PQ constants
const float m1 = 0.1593017578125;    // 2610/16384
const float m2 = 78.84375;           // 2523/32 * 128
const float c1 = 0.8359375;          // 3424/4096
const float c2 = 18.8515625;         // 2413/128
const float c3 = 18.6875;            // 2392/128

// Linear (0-10000 nits normalized to 0-1) -> PQ
vec3 linear_to_pq(vec3 L) {
    vec3 Lm = pow(L, vec3(m1));
    return pow((c1 + c2 * Lm) / (1.0 + c3 * Lm), vec3(m2));
}

// PQ -> Linear
vec3 pq_to_linear(vec3 N) {
    vec3 Np = pow(N, vec3(1.0 / m2));
    return pow(max(Np - c1, 0.0) / (c2 - c3 * Np), vec3(1.0 / m1));
}
```

**Critical**: PQ input is normalized to `[0, 1]` representing `[0, 10000]` nits. SDR content at 100 nits = `0.01` in linear PQ space.

### HLG (Hybrid Log-Gamma)


```glsl
const float hlg_a = 0.17883277;
const float hlg_b = 0.28466892;  // 1 - 4*a
const float hlg_c = 0.55991073;  // 0.5 - a*ln(4*a)

vec3 linear_to_hlg(vec3 L) {
    vec3 lo = sqrt(3.0 * L);
    vec3 hi = hlg_a * log(12.0 * L - hlg_b) + hlg_c;
    return mix(hi, lo, step(L, vec3(1.0 / 12.0)));
}
```
</transfer_functions>

<color_adjustments>
## Color Adjustments (Linear Space)

All operations below assume linear-light RGB input.

### Brightness & Contrast

```glsl
// Brightness: additive offset in linear space
// Contrast: scale around mid-gray (0.18 in linear = perceptual middle gray)
vec3 brightness_contrast(vec3 c, float brightness, float contrast) {
    c += brightness;
    c = (c - 0.18) * contrast + 0.18;
    return max(c, 0.0);
}
```

### Saturation

```glsl
vec3 adjust_saturation(vec3 c, float saturation) {
    // BT.709 luminance coefficients
    float luma = dot(c, vec3(0.2126, 0.7152, 0.0722));
    return max(mix(vec3(luma), c, saturation), 0.0);
}
```

Use BT.2020 coefficients `(0.2627, 0.6780, 0.0593)` for wide-gamut content.

### Hue Rotation

```glsl
// Rotate hue by angle (radians) using YIQ-like transform
vec3 rotate_hue(vec3 c, float angle) {
    float cosA = cos(angle);
    float sinA = sin(angle);
    mat3 hueRotation = mat3(
        vec3(0.213 + 0.787*cosA - 0.213*sinA,
             0.213 - 0.213*cosA + 0.143*sinA,
             0.213 - 0.213*cosA - 0.787*sinA),
        vec3(0.715 - 0.715*cosA - 0.715*sinA,
             0.715 + 0.285*cosA + 0.140*sinA,
             0.715 - 0.715*cosA + 0.715*sinA),
        vec3(0.072 - 0.072*cosA + 0.928*sinA,
             0.072 - 0.072*cosA - 0.283*sinA,
             0.072 + 0.928*cosA + 0.072*sinA)
    );
    return hueRotation * c;
}
```

### Color Temperature (White Balance)

```glsl
// Shift white balance: temperature (-1 to +1, neg=cool, pos=warm)
vec3 white_balance(vec3 c, float temperature) {
    // Simple channel multiplier approach
    c.r *= 1.0 + temperature * 0.2;
    c.b *= 1.0 - temperature * 0.2;
    return max(c, 0.0);
}
```
</color_adjustments>

<sharpening>
Apply in perceptual (gamma) space, not linear. Linearize -> adjust -> re-gamma -> sharpen -> continue.

### Contrast Adaptive Sharpening (CAS)

```glsl
// AMD FidelityFX CAS (simplified)
vec3 cas_sharpen(sampler2D tex, vec2 uv, vec2 texel_size, float sharpness) {
    vec3 c = texture(tex, uv).rgb;

    vec3 t = texture(tex, uv + vec2( 0, -1) * texel_size).rgb;
    vec3 b = texture(tex, uv + vec2( 0,  1) * texel_size).rgb;
    vec3 l = texture(tex, uv + vec2(-1,  0) * texel_size).rgb;
    vec3 r = texture(tex, uv + vec2( 1,  0) * texel_size).rgb;

    // Min/max of cross neighborhood
    vec3 mn = min(min(t, b), min(l, r));
    vec3 mx = max(max(t, b), max(l, r));
    mn = min(mn, c);
    mx = max(mx, c);

    // Adaptive weight: less sharpening where contrast is already high
    vec3 amp = sqrt(clamp(min(mn, 1.0 - mx) / mx, 0.0, 1.0));
    amp = -1.0 / (8.0 * mix(vec3(0.125), amp, sharpness) + 1.0);

    vec3 result = (t + b + l + r) * amp + c * (1.0 - 4.0 * amp);
    return clamp(result, mn, mx);  // Anti-ringing clamp
}
```

### Unsharp Mask

```glsl
vec3 unsharp_mask(sampler2D tex, vec2 uv, vec2 texel_size, float amount) {
    // Box blur 3x3 approximation
    vec3 blur = vec3(0.0);
    for (int y = -1; y <= 1; y++)
        for (int x = -1; x <= 1; x++)
            blur += texture(tex, uv + vec2(x, y) * texel_size).rgb;
    blur /= 9.0;

    vec3 sharp = texture(tex, uv).rgb;
    return sharp + (sharp - blur) * amount;
}
```

**ALVR note**: ALVR uses Snapdragon GSR (SGSR) which combines edge detection + Lanczos-based upscaling with sharpening in a single pass. See `stream.wgsl` for the implementation.
</sharpening>

<color_space_conversion>
### RGB to YUV (NV12 / P010)

Encoder input is typically NV12 (8-bit 4:2:0) or P010 (10-bit 4:2:0).

| Format | Luma | Chroma | Bit depth | Use |
|--------|------|--------|-----------|-----|
| NV12 | Y plane | Interleaved UV | 8 | SDR encoding |
| P010 | Y plane | Interleaved UV | 10 (in 16-bit) | HDR encoding |

#### BT.709 (SDR, sRGB gamut)

```glsl
// Full-range BT.709
vec3 rgb_to_yuv_709(vec3 rgb) {
    float Y  =  0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b;
    float Cb = -0.1146 * rgb.r - 0.3854 * rgb.g + 0.5000 * rgb.b + 0.5;
    float Cr =  0.5000 * rgb.r - 0.4542 * rgb.g - 0.0458 * rgb.b + 0.5;
    return vec3(Y, Cb, Cr);
}
```

#### BT.2020 (HDR, wide gamut)

```glsl
// Full-range BT.2020
vec3 rgb_to_yuv_2020(vec3 rgb) {
    float Y  =  0.2627 * rgb.r + 0.6780 * rgb.g + 0.0593 * rgb.b;
    float Cb = -0.1396 * rgb.r - 0.3604 * rgb.g + 0.5000 * rgb.b + 0.5;
    float Cr =  0.5000 * rgb.r - 0.4598 * rgb.g - 0.0402 * rgb.b + 0.5;
    return vec3(Y, Cb, Cr);
}
```

#### Limited vs Full Range

```glsl
// Scale from full [0,1] to limited [16/255, 235/255] (luma), [16/255, 240/255] (chroma)
vec3 full_to_limited_8bit(vec3 yuv) {
    yuv.x = yuv.x * (235.0 - 16.0) / 255.0 + 16.0 / 255.0;
    yuv.yz = yuv.yz * (240.0 - 16.0) / 255.0 + 16.0 / 255.0;
    return yuv;
}
```

**ALVR note**: ALVR's `staging_fragment.glsl` handles limited-range correction from Android hardware decoder output. The `FIX_LIMITED_RANGE` define expands limited `[16, 235]` back to full `[0, 255]`.

### Gamut Mapping (BT.709 <-> BT.2020)


```glsl
// BT.709 -> BT.2020 (3x3 matrix)
const mat3 BT709_TO_BT2020 = mat3(
    0.6274,  0.3293,  0.0433,
    0.0691,  0.9195,  0.0114,
    0.0164,  0.0880,  0.8956
);

// BT.2020 -> BT.709 (inverse)
const mat3 BT2020_TO_BT709 = mat3(
    1.6605, -0.5877, -0.0728,
   -0.1246,  1.1330, -0.0084,
   -0.0182, -0.1006,  1.1187
);
```

**Pitfall**: BT.2020 -> BT.709 can produce negative values (out-of-gamut). Clamp or use soft-clip tonemapping before conversion.
</color_space_conversion>

<compute_vs_fragment>
## Compute vs Fragment Shaders

| Aspect | Fragment Shader | Compute Shader |
|--------|----------------|----------------|
| Invocation | Per-pixel, driven by rasterizer | Explicit dispatch |
| Memory access | Texture sampling (filtered) | Image load/store (unfiltered) or SSBO |
| Output | Framebuffer attachment | Storage image / buffer |
| Shared memory | No | Yes (workgroup-local) |
| Synchronization | Implicit (rasterization order) | Explicit barriers |
| Best for | Simple per-pixel ops, leveraging texture filtering | Multi-pass, histogram, LUT generation, reductions |

**VR streaming rule of thumb**: Fragment shaders suffice for the common color correction chain. Use compute when you need shared memory (histogram equalization, auto-exposure) or structured buffer output (encoder-ready NV12 plane layout).

### Vulkan Compute Pipeline Setup (Rust/wgpu)

```rust
// Minimal compute pipeline for color correction
let shader = device.create_shader_module(wgpu::include_wgsl!("color_correct.wgsl"));

let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
    label: Some("color_correction"),
    layout: None,  // Auto-infer from shader
    module: &shader,
    entry_point: Some("main"),
    compilation_options: Default::default(),
    cache: None,
});

// Dispatch: one thread per pixel, workgroup 8x8
let workgroups_x = (width + 7) / 8;
let workgroups_y = (height + 7) / 8;
compute_pass.dispatch_workgroups(workgroups_x, workgroups_y, 1);
```

### Workgroup Size Guidelines

| Resolution | Workgroup | Threads/group | Notes |
|-----------|-----------|---------------|-------|
| Any | 8x8 | 64 | Safe default, good occupancy |
| Any | 16x16 | 256 | Better for simple ops, may hit register pressure |
| Any | 32x1 | 32 | Matches warp/wave size on most GPUs |
| Mobile (Quest) | 8x8 | 64 | Adreno GPUs prefer 64 threads |

**ALVR context**: ALVR uses fragment shaders via wgpu's render pipeline for stream color correction. The shader constants are set via `PipelineCompilationOptions` (specialization constants equivalent), not push constants, for static configuration like `ENABLE_SRGB_CORRECTION`.
</compute_vs_fragment>

<lut_correction>
## LUT-Based Correction

### 1D LUT

Per-channel transfer function. Store as 1D texture, 256+ entries.

```glsl
// 1D LUT application (per-channel)
uniform sampler1D lut_r, lut_g, lut_b;

vec3 apply_1d_lut(vec3 c) {
    return vec3(
        texture(lut_r, c.r).r,
        texture(lut_g, c.g).r,
        texture(lut_b, c.b).r
    );
}
```

### 3D LUT

Cross-channel color grading. Typically 17x17x17 or 33x33x33 with trilinear interpolation.

```glsl
// 3D LUT application
uniform sampler3D color_lut;
uniform float lut_size;  // e.g., 33.0

vec3 apply_3d_lut(vec3 c) {
    // Half-texel offset for correct interpolation at boundaries
    float scale = (lut_size - 1.0) / lut_size;
    float offset = 0.5 / lut_size;
    return texture(color_lut, c * scale + offset).rgb;
}
```

**Key**: Always use `LINEAR` (trilinear) filtering on 3D LUT textures. Nearest-neighbor causes visible color banding.

### Loading .cube LUT Files


```rust
// Parse Adobe .cube format (common LUT interchange)
fn parse_cube_lut(data: &str) -> (usize, Vec<[f32; 3]>) {
    let mut size = 0usize;
    let mut entries = Vec::new();
    for line in data.lines() {
        let line = line.trim();
        if line.starts_with("LUT_3D_SIZE") {
            size = line.split_whitespace().nth(1).unwrap().parse().unwrap();
        } else if !line.is_empty() && !line.starts_with('#') && !line.starts_with("TITLE")
                   && !line.starts_with("DOMAIN") {
            let vals: Vec<f32> = line.split_whitespace()
                .filter_map(|s| s.parse().ok()).collect();
            if vals.len() == 3 { entries.push([vals[0], vals[1], vals[2]]); }
        }
    }
    (size, entries)
}
```
</lut_correction>

<headset_calibration>
## Per-Headset Calibration

Different VR headsets have different display characteristics:

| Headset | Panel | Color Space | Transfer | Notes |
|---------|-------|-------------|----------|-------|
| Quest 2/3 | LCD | sRGB (approx) | sRGB gamma | Slight blue shift, limited contrast |
| Quest Pro | Mini-LED LCD | sRGB | sRGB gamma | Better contrast, local dimming |
| Pico 4 | LCD | sRGB (approx) | sRGB gamma | Warm tint on some units |
| Valve Index | LCD | sRGB | sRGB gamma | Good color accuracy |
| Bigscreen Beyond | Micro-OLED | DCI-P3 (approx) | sRGB gamma | Wide gamut, perfect blacks |
| Pimax Crystal | Mini-LED | Wide gamut | sRGB gamma | Oversaturated without correction |

### Calibration Profile Structure

```rust
struct HeadsetColorProfile {
    name: String,
    // White point correction (D65 reference)
    white_point_offset: [f32; 2],  // delta-xy from D65
    // Per-channel gamma curves
    gamma: [f32; 3],  // [R, G, B]
    // Gamut mapping matrix (identity = no correction)
    gamut_matrix: [[f32; 3]; 3],
    // Black level offset (OLED vs LCD)
    black_level: f32,
    // Max brightness in nits
    max_nits: f32,
}
```
</headset_calibration>

<pitfalls>
## Common Pitfalls

### Banding from Low Precision

| Bit depth | Levels | Visible banding? |
|-----------|--------|-----------------|
| 8-bit | 256 | Yes, especially in dark gradients |
| 10-bit | 1024 | Rarely visible |
| 16-bit float | 65536 | No |

**Fix**: Do all intermediate computation in at least 16-bit float (`rgba16f`). Only quantize at the final output stage. Use dithering if targeting 8-bit output:

```glsl
// Temporal dithering to reduce banding (8-bit output)
vec3 dither(vec3 c, vec2 pixel_coord, float frame) {
    float noise = fract(sin(dot(pixel_coord + frame, vec2(12.9898, 78.233))) * 43758.5453);
    return c + (noise - 0.5) / 255.0;
}
```

### Clamping HDR Values

```glsl
// WRONG: clamps highlights before they reach the transfer function
color = clamp(color, 0.0, 1.0);  // kills HDR
color = linear_to_pq(color);

// RIGHT: only clamp negatives, let PQ handle the range
color = max(color, 0.0);
color = linear_to_pq(color);     // PQ maps [0, 10000 nits] to [0, 1]
```

### Shader Precision

```glsl
// WRONG: mediump loses precision in dark regions
mediump vec3 color = srgb_to_linear(texel.rgb);  // 10-bit mantissa

// RIGHT: use highp for color math
highp vec3 color = srgb_to_linear(texel.rgb);    // 23-bit mantissa
```

On mobile GPUs (Adreno/Mali), `mediump` is real 16-bit float. Always use `highp` for:
- Transfer function calculations (pow, log)
- YUV conversion coefficients
- Accumulated color values

### Double Gamma

```
// WRONG: applying gamma twice
gpu_output (already sRGB) -> sRGB encode again -> too bright/washed out

// Signs of double gamma:
// - Midtones too bright
// - Dark areas look "lifted"
// - Colors appear desaturated
```

Check: render a 50% gray patch. If it measures ~73% (`0.5^(1/2.2) = 0.73`), gamma was applied twice.

### Processing Order Mistakes

```
// WRONG: sharpening in linear space amplifies highlights disproportionately
linear_color = srgb_to_linear(input);
sharpened = cas_sharpen(linear_color);  // highlight ringing
output = linear_to_srgb(sharpened);

// RIGHT: sharpen in perceptual space
linear_color = srgb_to_linear(input);
adjusted = brightness_contrast(linear_color, ...);
perceptual = linear_to_srgb(adjusted);
sharpened = cas_sharpen(perceptual);    // uniform edge response
output = sharpened;
```

## WGSL-Specific Notes

WGSL (used by ALVR via wgpu) differs from GLSL:

| GLSL | WGSL |
|------|------|
| `vec3` | `vec3f` / `vec3<f32>` |
| `mix(a, b, t)` | `mix(a, b, t)` (same) |
| `step(edge, x)` | `step(edge, x)` (same) |
| `pow(x, y)` | `pow(x, y)` (same, but no negative base) |
| `#define` / `#ifdef` | `override` constants + `if` |
| `uniform` | `var<uniform>` or `override` for compile-time |
| `layout(push_constant)` | `var<push_constant>` |
| `gl_FragCoord` | `@builtin(position)` |
| `imageStore` | `textureStore` |
| No equivalent | `@compute @workgroup_size(8, 8)` |

**WGSL `pow()` pitfall**: `pow(x, y)` is undefined for negative `x`. Always guard with `max(x, 0.0)` before `pow()` calls in transfer functions.

## ALVR Integration Notes

ALVR's color pipeline (in `alvr/graphics/`):

1. **Hardware buffer** -> `StagingRenderer` (GLES external texture -> wgpu texture)
2. **Stream shader** (`stream.wgsl`):
   - Optional foveated encoding decode (FFE)
   - Optional SGSR upscaling with edge-aware sharpening
   - Optional sRGB linearization (`ENABLE_SRGB_CORRECTION`)
   - Optional encoding gamma (`ENCODING_GAMMA`)
   - Chroma keying for passthrough (RGB or HSV)
3. **Output** -> OpenXR swapchain

Key integration points:
- Shader constants via `PipelineCompilationOptions` (compile-time, not runtime)
- Push constants for per-frame data (transforms, chroma key params)
- Limited range fix in staging fragment shader (`FIX_LIMITED_RANGE`)
- Two-view stereo rendering (left/right eye in single pass)

To add new color corrections to ALVR: add `override` constants to `stream.wgsl`, pass them through `StreamRenderer::new()`, and expose in session settings.

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `color-shaders.md` | Complete shader implementations for all color ops |
| `yuv-conversion.md` | NV12/P010 layout, chroma subsampling, encoder integration |

</pitfalls>
