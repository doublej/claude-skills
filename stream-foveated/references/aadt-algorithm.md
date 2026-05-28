# AADT Algorithm — Axis-Aligned Distorted Transfer

## Overview

AADT compresses a VR frame by spatially warping it along each axis independently. The center region is preserved at full resolution while edges are compressed by a configurable ratio. This produces a smaller intermediate frame that is cheaper to encode, transmit, and decode.

## Compression Mapping

The mapping function converts coordinates from the full-resolution source to the compressed target. It is piecewise-linear with three segments per axis:

```
Source coordinate (0..1) -> Target coordinate (0..1)

Left edge:    quadratic mapping (0 .. lo_bound) -> (0 .. lo_bound_c)
Center:       linear 1:1       (lo_bound .. hi_bound) -> (lo_bound_c .. hi_bound_c)
Right edge:   quadratic mapping (hi_bound .. 1) -> (hi_bound_c .. 1)
```

The quadratic segments in the edges create a smooth transition from compressed to uncompressed regions.

## Parameter Derivation

Given inputs `center_size`, `center_shift`, `edge_ratio` (all per-axis):

### Step 1: Alignment

Edge sizes must align to `edge_ratio * 2` pixel multiples to prevent seam artifacts at region boundaries:

```rust
let edge_size = view_resolution - center_size * view_resolution;
let center_size_aligned =
    1.0 - (edge_size / (edge_ratio * 2.0)).ceil() * (edge_ratio * 2.0) / view_resolution;
```

The center shift is similarly aligned:

```rust
let edge_size_aligned = view_resolution - center_size_aligned * view_resolution;
let center_shift_aligned =
    (center_shift * edge_size_aligned / (edge_ratio * 2.0)).ceil()
    * (edge_ratio * 2.0) / edge_size_aligned;
```

This alignment is critical. Without it, the compression/decompression cycle introduces sub-pixel misalignment at region boundaries, causing visible seams.

### Step 2: Compute Scale Factor

The foveation scale determines the ratio of compressed to original resolution:

```rust
let foveation_scale = center_size_aligned + (1.0 - center_size_aligned) / edge_ratio;
let optimized_resolution = foveation_scale * view_resolution;
```

The optimized resolution is then aligned to 32-pixel multiples for hardware encoder compatibility:

```rust
let optimized_aligned = (optimized_resolution / 32.0).ceil() * 32.0;
let view_ratio = optimized_resolution / optimized_aligned;
```

`view_ratio` compensates for the padding introduced by 32px alignment.

### Step 3: Shader Constants

The shader uses these derived constants to perform the piecewise mapping:

```rust
let c0 = (1.0 - center_size_aligned) * 0.5;
let c1 = (edge_ratio - 1.0) * c0 * (center_shift_aligned + 1.0) / edge_ratio;
let c2 = (edge_ratio - 1.0) * center_size_aligned + 1.0;

// Region boundaries in source space
let lo_bound = c0 * (center_shift_aligned + 1.0);
let hi_bound = c0 * (center_shift_aligned - 1.0) + 1.0;

// Region boundaries in compressed space
let lo_bound_c = c0 * (center_shift_aligned + 1.0) / c2;
let hi_bound_c = c0 * (center_shift_aligned - 1.0) / c2 + 1.0;

// Left edge quadratic coefficients
let a_left = c2 * (1.0 - edge_ratio) / (edge_ratio * lo_bound_c);
let b_left = (c1 + c2 * lo_bound_c) / lo_bound_c;

// Right edge quadratic coefficients
let a_right = c2 * (edge_ratio - 1.0) / (edge_ratio * (1.0 - hi_bound_c));
let b_right = (c2 - edge_ratio * c1 - 2.0 * edge_ratio * c2
    + c2 * edge_ratio * (1.0 - hi_bound_c) + edge_ratio)
    / (edge_ratio * (1.0 - hi_bound_c));
let c_right = (c2 * edge_ratio - c2) * (c1 - hi_bound_c + c2 * hi_bound_c)
    / (edge_ratio * (1.0 - hi_bound_c) * (1.0 - hi_bound_c));
```

### Step 4: Full Constant Set

These constants are passed as shader uniforms:

| Constant | Purpose |
|----------|---------|
| `ENABLE_FFE` | 1.0 when foveated encoding is active |
| `VIEW_WIDTH_RATIO`, `VIEW_HEIGHT_RATIO` | Compensation for 32px alignment padding |
| `EDGE_X_RATIO`, `EDGE_Y_RATIO` | Compression ratio per axis |
| `C1_X/Y`, `C2_X/Y` | Intermediate mapping coefficients |
| `LO_BOUND_X/Y`, `HI_BOUND_X/Y` | Region boundary coordinates |
| `A_LEFT_X/Y`, `B_LEFT_X/Y` | Left edge quadratic coefficients |
| `A_RIGHT_X/Y`, `B_RIGHT_X/Y`, `C_RIGHT_X/Y` | Right edge quadratic coefficients |

## Shader Logic (Pseudocode)

### Compress (server-side, pre-encode)

```glsl
vec2 compress(vec2 uv) {
    // Per axis:
    if (uv.x < lo_bound) {
        // Left edge: quadratic compression
        compressed.x = a_left * uv.x * uv.x + b_left * uv.x;
    } else if (uv.x > hi_bound) {
        // Right edge: quadratic compression
        compressed.x = a_right * uv.x * uv.x + b_right * uv.x + c_right;
    } else {
        // Center: linear mapping (preserve resolution)
        compressed.x = (uv.x - lo_bound) * center_scale + lo_bound_c;
    }
    // Same for Y axis
    return compressed * view_ratio;
}
```

### Decompress (client-side, post-decode)

The inverse mapping. Same structure but maps from compressed to source coordinates. The client shader uses the same constants.

## Numerical Example

With defaults (`center_size_x=0.45`, `edge_ratio_x=4`, `center_shift_x=0.4`) on a 2048px-wide per-eye view:

```
edge_size = 2048 * (1 - 0.45) = 1126.4
aligned to 4*2=8: ceil(1126.4/8)*8 = 1128
center_size_aligned = 1 - 1128/2048 = 0.449
foveation_scale_x = 0.449 + 0.551/4 = 0.587
optimized_width = 0.587 * 2048 = 1202
aligned to 32: ceil(1202/32)*32 = 1216
```

Total stereo frame: 2432 x 1088 instead of 4096 x 2048 = **~29% of original pixels**.

## Previous ALVR Algorithms

### Warp (deprecated)

Radial tangent-function compression in elliptical pattern. Smooth but causes overall blur because the compression is non-axis-aligned, producing diagonal resampling artifacts.

Demo: https://www.shadertoy.com/view/3l2GRR

### Slices (deprecated)

9-section decomposition (center, 4 edges, 4 corners) with independent resolution per section. Better quality than warp but complex to implement, pack, and unpack. Visible borders at section boundaries.

Demo: https://www.shadertoy.com/view/WddGz8

### Why AADT Won

- Simplest shader (axis-aligned = no diagonal resampling)
- Lowest GPU cost on Quest (critical for decode pipeline)
- Good enough compression for the bandwidth savings
- Alignment to encoder macroblock boundaries is natural (axis-aligned)
