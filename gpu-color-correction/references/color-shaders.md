# Color Shader Reference

Complete shader implementations for GPU color correction operations.

## Full Processing Chain (GLSL)

```glsl
#version 450

layout(binding = 0) uniform sampler2D input_texture;
layout(binding = 1) uniform sampler3D color_lut;
layout(binding = 2, rgba16f) uniform writeonly image2D output_image;

layout(push_constant) uniform Params {
    float brightness;     // -1.0 to 1.0
    float contrast;       // 0.0 to 3.0 (1.0 = no change)
    float saturation;     // 0.0 to 3.0 (1.0 = no change)
    float hue_shift;      // radians
    float sharpness;      // 0.0 to 1.0
    float gamma;          // 0.0 = use sRGB curve, >0 = simple pow
    float lut_strength;   // 0.0 to 1.0 (blend with uncorrected)
    uint  flags;          // bit 0: enable LUT, bit 1: HDR mode
};

layout(local_size_x = 8, local_size_y = 8) in;

// --- Transfer functions ---

vec3 srgb_to_linear(vec3 c) {
    vec3 lo = c / 12.92;
    vec3 hi = pow((c + 0.055) / 1.055, vec3(2.4));
    return mix(hi, lo, step(c, vec3(0.04045)));
}

vec3 linear_to_srgb(vec3 c) {
    c = max(c, 0.0);
    vec3 lo = c * 12.92;
    vec3 hi = 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, step(c, vec3(0.0031308)));
}

// --- Color adjustments (linear space) ---

vec3 apply_brightness_contrast(vec3 c, float brightness, float contrast) {
    c += brightness;
    c = (c - 0.18) * contrast + 0.18;
    return max(c, 0.0);
}

vec3 apply_saturation(vec3 c, float saturation) {
    float luma = dot(c, vec3(0.2126, 0.7152, 0.0722));
    return max(mix(vec3(luma), c, saturation), 0.0);
}

vec3 apply_hue_rotation(vec3 c, float angle) {
    if (abs(angle) < 0.001) return c;
    float cosA = cos(angle);
    float sinA = sin(angle);
    // Precomputed BT.709 hue rotation matrix
    mat3 M = mat3(
        0.213 + 0.787*cosA - 0.213*sinA,
        0.213 - 0.213*cosA + 0.143*sinA,
        0.213 - 0.213*cosA - 0.787*sinA,
        0.715 - 0.715*cosA - 0.715*sinA,
        0.715 + 0.285*cosA + 0.140*sinA,
        0.715 - 0.715*cosA + 0.715*sinA,
        0.072 - 0.072*cosA + 0.928*sinA,
        0.072 - 0.072*cosA - 0.283*sinA,
        0.072 + 0.928*cosA + 0.072*sinA
    );
    return M * c;
}

// --- Sharpening (perceptual space) ---

vec3 cas_sharpen(ivec2 coord, vec3 center, float sharpness) {
    vec3 t = texelFetch(input_texture, coord + ivec2( 0, -1), 0).rgb;
    vec3 b = texelFetch(input_texture, coord + ivec2( 0,  1), 0).rgb;
    vec3 l = texelFetch(input_texture, coord + ivec2(-1,  0), 0).rgb;
    vec3 r = texelFetch(input_texture, coord + ivec2( 1,  0), 0).rgb;

    // Convert neighbors to perceptual for sharpening
    t = linear_to_srgb(t); b = linear_to_srgb(b);
    l = linear_to_srgb(l); r = linear_to_srgb(r);
    vec3 c = linear_to_srgb(center);

    vec3 mn = min(min(t, b), min(l, r));
    vec3 mx = max(max(t, b), max(l, r));
    mn = min(mn, c);
    mx = max(mx, c);

    vec3 amp = sqrt(clamp(min(mn, 1.0 - mx) / mx, 0.0, 1.0));
    amp = -1.0 / (8.0 * mix(vec3(0.125), amp, sharpness) + 1.0);

    vec3 result = (t + b + l + r) * amp + c * (1.0 - 4.0 * amp);
    result = clamp(result, mn, mx);

    return srgb_to_linear(result);
}

// --- LUT ---

vec3 apply_3d_lut(vec3 c, float strength) {
    float lut_size = float(textureSize(color_lut, 0).x);
    float scale = (lut_size - 1.0) / lut_size;
    float offset = 0.5 / lut_size;

    vec3 lut_color = texture(color_lut, c * scale + offset).rgb;
    return mix(c, lut_color, strength);
}

// --- Main ---

void main() {
    ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = textureSize(input_texture, 0);
    if (coord.x >= size.x || coord.y >= size.y) return;

    vec3 color = texelFetch(input_texture, coord, 0).rgb;

    // 1. Linearize
    if (gamma == 0.0) {
        color = srgb_to_linear(color);
    } else {
        color = pow(max(color, 0.0), vec3(gamma));
    }

    // 2. Color adjustments in linear space
    color = apply_brightness_contrast(color, brightness, contrast);
    color = apply_saturation(color, saturation);
    color = apply_hue_rotation(color, hue_shift);

    // 3. LUT (applied in linear space, LUT should be authored for linear input)
    if ((flags & 1u) != 0u) {
        color = apply_3d_lut(color, lut_strength);
    }

    // 4. Sharpen (internally converts to perceptual and back)
    if (sharpness > 0.0) {
        color = cas_sharpen(coord, color, sharpness);
    }

    // 5. Re-encode
    if (gamma == 0.0) {
        color = linear_to_srgb(color);
    } else {
        color = pow(max(color, 0.0), vec3(1.0 / gamma));
    }

    imageStore(output_image, coord, vec4(color, 1.0));
}
```

## Full Processing Chain (WGSL / wgpu)

```wgsl
@group(0) @binding(0) var input_tex: texture_2d<f32>;
@group(0) @binding(1) var input_sampler: sampler;
@group(0) @binding(2) var output_tex: texture_storage_2d<rgba16float, write>;

struct Params {
    brightness: f32,
    contrast: f32,
    saturation: f32,
    sharpness: f32,
}
@group(0) @binding(3) var<uniform> params: Params;

fn srgb_to_linear(c: vec3f) -> vec3f {
    let lo = c / 12.92;
    let hi = pow((c + 0.055) / 1.055, vec3f(2.4));
    return mix(hi, lo, step(c, vec3f(0.04045)));
}

fn linear_to_srgb(c: vec3f) -> vec3f {
    let cc = max(c, vec3f(0.0));
    let lo = cc * 12.92;
    let hi = 1.055 * pow(cc, vec3f(1.0 / 2.4)) - 0.055;
    return mix(hi, lo, step(cc, vec3f(0.0031308)));
}

fn adjust_brightness_contrast(c: vec3f, brightness: f32, contrast: f32) -> vec3f {
    var result = c + brightness;
    result = (result - 0.18) * contrast + 0.18;
    return max(result, vec3f(0.0));
}

fn adjust_saturation(c: vec3f, saturation: f32) -> vec3f {
    let luma = dot(c, vec3f(0.2126, 0.7152, 0.0722));
    return max(mix(vec3f(luma), c, saturation), vec3f(0.0));
}

@compute @workgroup_size(8, 8)
fn main(@builtin(global_invocation_id) gid: vec3u) {
    let dims = textureDimensions(input_tex);
    if gid.x >= dims.x || gid.y >= dims.y { return; }

    let coord = vec2i(gid.xy);
    var color = textureLoad(input_tex, coord, 0).rgb;

    // Linearize
    color = srgb_to_linear(color);

    // Adjust
    color = adjust_brightness_contrast(color, params.brightness, params.contrast);
    color = adjust_saturation(color, params.saturation);

    // Re-encode
    color = linear_to_srgb(color);

    textureStore(output_tex, coord, vec4f(color, 1.0));
}
```

## HDR Processing Chain (PQ / ST 2084)

```glsl
// PQ constants
const float PQ_m1 = 0.1593017578125;
const float PQ_m2 = 78.84375;
const float PQ_c1 = 0.8359375;
const float PQ_c2 = 18.8515625;
const float PQ_c3 = 18.6875;

vec3 pq_to_linear(vec3 N) {
    vec3 Np = pow(max(N, 0.0), vec3(1.0 / PQ_m2));
    return pow(max(Np - PQ_c1, 0.0) / (PQ_c2 - PQ_c3 * Np), vec3(1.0 / PQ_m1));
}

vec3 linear_to_pq(vec3 L) {
    vec3 Lm = pow(max(L, 0.0), vec3(PQ_m1));
    return pow((PQ_c1 + PQ_c2 * Lm) / (1.0 + PQ_c3 * Lm), vec3(PQ_m2));
}

// HDR color correction chain
vec3 hdr_color_correct(vec3 pq_color) {
    // 1. PQ -> linear nits (0-10000 range normalized to 0-1)
    vec3 linear = pq_to_linear(pq_color);

    // 2. Scale to working range: 100 nits SDR reference = 0.5 working value
    linear *= 50.0;  // 1.0 in PQ linear = 10000 nits, so *50 -> 100 nits = 0.5

    // 3. Adjustments in linear (same ops as SDR but on HDR range)
    linear = apply_brightness_contrast(linear, brightness * 0.5, contrast);
    linear = apply_saturation(linear, saturation);

    // 4. Scale back
    linear /= 50.0;

    // 5. Linear -> PQ (no clamping to 1.0!)
    return linear_to_pq(max(linear, 0.0));
}
```

## Tonemapping (HDR -> SDR fallback)

```glsl
// Reinhard extended
vec3 tonemap_reinhard(vec3 c, float max_white) {
    vec3 numerator = c * (1.0 + c / (max_white * max_white));
    return numerator / (1.0 + c);
}

// ACES filmic (Narkowicz approximation)
vec3 tonemap_aces(vec3 c) {
    const float a = 2.51;
    const float b = 0.03;
    const float cc = 2.43;
    const float d = 0.59;
    const float e = 0.14;
    return clamp((c * (a * c + b)) / (c * (cc * c + d) + e), 0.0, 1.0);
}

// AgX (neutral, good for VR -- less hue shift than ACES)
vec3 agx_default_contrast(vec3 x) {
    vec3 x2 = x * x;
    vec3 x4 = x2 * x2;
    return 15.5 * x4 * x2 - 40.14 * x4 * x + 31.96 * x4
         - 6.868 * x2 * x + 0.4298 * x2 + 0.1191 * x - 0.00232;
}
```

## Color Space Conversion Matrices

```glsl
// All matrices operate on linear-light RGB values

// sRGB/BT.709 primaries -> XYZ (D65)
const mat3 BT709_TO_XYZ = mat3(
    0.4124, 0.3576, 0.1805,
    0.2126, 0.7152, 0.0722,
    0.0193, 0.1192, 0.9505
);

// XYZ (D65) -> sRGB/BT.709
const mat3 XYZ_TO_BT709 = mat3(
     3.2406, -1.5372, -0.4986,
    -0.9689,  1.8758,  0.0415,
     0.0557, -0.2040,  1.0570
);

// BT.2020 -> XYZ (D65)
const mat3 BT2020_TO_XYZ = mat3(
    0.6370, 0.1446, 0.1689,
    0.2627, 0.6780, 0.0593,
    0.0000, 0.0281, 1.0610
);

// XYZ (D65) -> BT.2020
const mat3 XYZ_TO_BT2020 = mat3(
     1.7167, -0.3557, -0.2534,
    -0.6667,  1.6165,  0.0158,
     0.0176, -0.0428,  0.9421
);

// DCI-P3 (D65) -> XYZ
const mat3 P3_TO_XYZ = mat3(
    0.4866, 0.2657, 0.1982,
    0.2290, 0.6917, 0.0793,
    0.0000, 0.0451, 1.0439
);
```

## Dithering Patterns

### Ordered Dither (Bayer 4x4)

```glsl
const float bayer4x4[16] = float[16](
     0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
    12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
     3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
    15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0
);

vec3 ordered_dither(vec3 c, ivec2 coord, float bit_depth) {
    int idx = (coord.x % 4) + (coord.y % 4) * 4;
    float threshold = bayer4x4[idx] - 0.5;
    float step_size = 1.0 / (pow(2.0, bit_depth) - 1.0);
    return c + threshold * step_size;
}
```

### Temporal Blue Noise Dither

```glsl
// Better for VR: distributes error over frames, less visible pattern
vec3 temporal_dither(vec3 c, vec2 pixel_coord, uint frame_index) {
    // Blue noise approximation via interleaved gradient noise
    vec2 p = pixel_coord + float(frame_index) * vec2(5.588238, 5.123456);
    float noise = fract(52.9829189 * fract(dot(p, vec2(0.06711056, 0.00583715))));
    return c + (noise - 0.5) / 255.0;
}
```
