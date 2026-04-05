# YUV Conversion & Encoder Integration

## Memory Layout

### NV12 (8-bit 4:2:0)

```
Width x Height Y plane (luma, one byte per pixel)
followed by
(Width/2) x (Height/2) UV plane (interleaved Cb/Cr pairs)

Total bytes: Width * Height * 1.5

Example 1920x1080:
  Y:  1920 * 1080 = 2,073,600 bytes
  UV:  960 *  540 = 1,036,800 bytes (518,400 Cb + 518,400 Cr interleaved)
  Total: 3,110,400 bytes
```

### P010 (10-bit 4:2:0 in 16-bit containers)

```
Width x Height Y plane (16-bit per sample, 10 MSBs used)
followed by
(Width/2) x (Height/2) UV plane (interleaved, 16-bit per component)

Total bytes: Width * Height * 3

Data is stored in the upper 10 bits of each 16-bit word:
  value_10bit = (raw_16bit >> 6) & 0x3FF
```

### I420 / YV12 (planar 4:2:0)

```
Y plane:  Width x Height
U plane:  Width/2 x Height/2
V plane:  Width/2 x Height/2

I420: Y then U then V
YV12: Y then V then U
```

## Compute Shader: RGB -> NV12

```glsl
#version 450

layout(binding = 0) uniform sampler2D rgb_input;
layout(binding = 1, r8) uniform writeonly image2D y_plane;
layout(binding = 2, rg8) uniform writeonly image2D uv_plane;

layout(push_constant) uniform Params {
    uint width;
    uint height;
    uint color_standard;  // 0 = BT.709, 1 = BT.2020
    uint range;           // 0 = full, 1 = limited
};

// BT.709 full-range coefficients
const vec3 BT709_Y  = vec3( 0.2126,  0.7152,  0.0722);
const vec3 BT709_Cb = vec3(-0.1146, -0.3854,  0.5000);
const vec3 BT709_Cr = vec3( 0.5000, -0.4542, -0.0458);

// BT.2020 full-range coefficients
const vec3 BT2020_Y  = vec3( 0.2627,  0.6780,  0.0593);
const vec3 BT2020_Cb = vec3(-0.1396, -0.3604,  0.5000);
const vec3 BT2020_Cr = vec3( 0.5000, -0.4598, -0.0402);

vec3 rgb_to_ycbcr(vec3 rgb) {
    vec3 coeff_y, coeff_cb, coeff_cr;

    if (color_standard == 0) {
        coeff_y  = BT709_Y;
        coeff_cb = BT709_Cb;
        coeff_cr = BT709_Cr;
    } else {
        coeff_y  = BT2020_Y;
        coeff_cb = BT2020_Cb;
        coeff_cr = BT2020_Cr;
    }

    float Y  = dot(rgb, coeff_y);
    float Cb = dot(rgb, coeff_cb) + 0.5;
    float Cr = dot(rgb, coeff_cr) + 0.5;

    if (range == 1) {
        // Full -> limited range
        Y  = Y  * (235.0 - 16.0) / 255.0 + 16.0 / 255.0;
        Cb = Cb * (240.0 - 16.0) / 255.0 + 16.0 / 255.0;
        Cr = Cr * (240.0 - 16.0) / 255.0 + 16.0 / 255.0;
    }

    return vec3(Y, Cb, Cr);
}

// Y plane: one thread per pixel
layout(local_size_x = 8, local_size_y = 8) in;
void main() {
    ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
    if (coord.x >= int(width) || coord.y >= int(height)) return;

    vec2 uv = (vec2(coord) + 0.5) / vec2(width, height);
    vec3 rgb = texture(rgb_input, uv).rgb;
    vec3 ycbcr = rgb_to_ycbcr(rgb);

    // Write Y
    imageStore(y_plane, coord, vec4(ycbcr.x));

    // Write UV (2x2 block average for chroma subsampling)
    if ((coord.x & 1) == 0 && (coord.y & 1) == 0) {
        // Average 2x2 block for chroma
        vec3 sum = ycbcr;
        sum += rgb_to_ycbcr(texelFetch(rgb_input, coord + ivec2(1, 0), 0).rgb);
        sum += rgb_to_ycbcr(texelFetch(rgb_input, coord + ivec2(0, 1), 0).rgb);
        sum += rgb_to_ycbcr(texelFetch(rgb_input, coord + ivec2(1, 1), 0).rgb);
        sum *= 0.25;

        ivec2 uv_coord = coord / 2;
        imageStore(uv_plane, uv_coord, vec4(sum.y, sum.z, 0.0, 0.0));
    }
}
```

## Compute Shader: RGB -> P010

```glsl
// Same structure as NV12 but with 10-bit output in 16-bit storage
layout(binding = 1, r16) uniform writeonly image2D y_plane;
layout(binding = 2, rg16) uniform writeonly image2D uv_plane;

void main() {
    // ... same as NV12 up to rgb_to_ycbcr()

    // Scale to 10-bit in 16-bit container (upper 10 bits)
    float y_10bit = floor(ycbcr.x * 1023.0 + 0.5) * 64.0 / 65535.0;
    imageStore(y_plane, coord, vec4(y_10bit));

    if ((coord.x & 1) == 0 && (coord.y & 1) == 0) {
        // ... same 2x2 averaging ...
        float cb_10bit = floor(sum.y * 1023.0 + 0.5) * 64.0 / 65535.0;
        float cr_10bit = floor(sum.z * 1023.0 + 0.5) * 64.0 / 65535.0;
        imageStore(uv_plane, coord / 2, vec4(cb_10bit, cr_10bit, 0.0, 0.0));
    }
}
```

## Chroma Subsampling Pitfalls

### Incorrect Averaging

```glsl
// WRONG: averaging RGB then converting
vec3 avg_rgb = (rgb00 + rgb10 + rgb01 + rgb11) * 0.25;
vec3 ycbcr = rgb_to_ycbcr(avg_rgb);  // Y is wrong (nonlinear mixing)

// RIGHT: convert each pixel, then average chroma
vec3 ycbcr00 = rgb_to_ycbcr(rgb00);
vec3 ycbcr10 = rgb_to_ycbcr(rgb10);
vec3 ycbcr01 = rgb_to_ycbcr(rgb01);
vec3 ycbcr11 = rgb_to_ycbcr(rgb11);
float Cb = (ycbcr00.y + ycbcr10.y + ycbcr01.y + ycbcr11.y) * 0.25;
float Cr = (ycbcr00.z + ycbcr10.z + ycbcr01.z + ycbcr11.z) * 0.25;
```

### Linear vs Gamma Domain Subsampling

For highest quality, subsample chroma in linear light:

```glsl
// Convert to linear before chroma averaging
vec3 linear00 = srgb_to_linear(rgb00);
// ... convert all 4 pixels
// Average chroma in linear space
// Convert back to gamma before YUV conversion
```

In practice, the visual difference is negligible for SDR content. For HDR (PQ), it matters more.

## Encoder Integration Patterns

### Vulkan/wgpu -> Hardware Encoder

```
GPU texture (RGBA)
    |
    v
Compute shader: RGB -> NV12/P010
    |
    v
GPU buffer (NV12 layout)
    |
    v
Copy to encoder input surface:
  - NVENC: map CUarray, copy Y/UV planes
  - VAAPI: map VAImage, copy planes
  - MediaCodec: ANativeWindow queue
  - AMF: map AMFSurface, copy planes
```

### ALVR's Approach

ALVR doesn't do explicit RGB->YUV on the GPU side. The flow is:
1. GPU renders to swapchain texture (RGBA)
2. Encoder (NVENC/VAAPI/MediaCodec) handles the color space conversion internally
3. The `encoding_gamma` parameter pre-compensates for encoder gamma assumptions

This is simpler but less flexible than explicit GPU-side conversion.

### Stride / Alignment

Encoders often require aligned row strides:

| Encoder | Y stride alignment | UV stride alignment |
|---------|-------------------|-------------------|
| NVENC | 256 bytes | 256 bytes |
| VAAPI | Varies (usually 64) | Same as Y |
| MediaCodec | Device-specific | Device-specific |
| x264 | 32 bytes | 32 bytes |

```glsl
// Account for stride in buffer writes
uint y_stride = (width + alignment - 1) & ~(alignment - 1);
uint y_offset = coord.y * y_stride + coord.x;

uint uv_stride = ((width / 2 * 2) + alignment - 1) & ~(alignment - 1);
uint uv_offset = height * y_stride + (coord.y / 2) * uv_stride + (coord.x & ~1);
```

## YUV -> RGB (Decoder Output)

For the reverse path (decoder output -> display):

```glsl
// BT.709 full-range YCbCr -> RGB
vec3 ycbcr_to_rgb_709(float Y, float Cb, float Cr) {
    Cb -= 0.5;
    Cr -= 0.5;
    float R = Y + 1.5748 * Cr;
    float G = Y - 0.1873 * Cb - 0.4681 * Cr;
    float B = Y + 1.8556 * Cb;
    return vec3(R, G, B);
}

// BT.709 limited-range YCbCr -> RGB
vec3 ycbcr_limited_to_rgb_709(float Y, float Cb, float Cr) {
    Y  = (Y  - 16.0/255.0) / ((235.0 - 16.0) / 255.0);
    Cb = (Cb - 16.0/255.0) / ((240.0 - 16.0) / 255.0);
    Cr = (Cr - 16.0/255.0) / ((240.0 - 16.0) / 255.0);
    return ycbcr_to_rgb_709(Y, Cb, Cr);
}
```

## Color Standard Selection

| Content | Gamut | Transfer | YUV Matrix |
|---------|-------|----------|------------|
| SDR streaming | BT.709 | sRGB | BT.709 |
| HDR10 streaming | BT.2020 | PQ (ST 2084) | BT.2020 |
| HLG streaming | BT.2020 | HLG | BT.2020 |
| Quest native | sRGB (709) | sRGB | BT.709 |
| PC VR (SDR) | sRGB (709) | sRGB | BT.709 |
| PC VR (HDR) | scRGB or BT.2020 | Linear or PQ | BT.2020 |

## Signaling Color Info to Decoder

The decoder needs to know what color format was used. For H.264/H.265, this is carried in VUI parameters:

```
colour_primaries:       1 = BT.709, 9 = BT.2020
transfer_characteristics: 1 = BT.709, 16 = PQ, 18 = HLG
matrix_coefficients:    1 = BT.709, 9 = BT.2020
video_full_range_flag:  0 = limited, 1 = full
```

If these are wrong, the decoder will interpret colors incorrectly even if the GPU shader did everything right.
