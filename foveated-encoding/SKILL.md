---
name: foveated-encoding
description: "VR streaming foveation: AADT, NVENC/AMF params, eye tracking, artifacts"
---

# Foveated Encoding for VR Streaming

## Key Concepts

**Foveated encoding != foveated rendering.** They are complementary:

| Technique | Where | What it reduces | ALVR? |
|-----------|-------|----------------|-------|
| Foveated rendering | GPU render pipeline | Shading cost | No control (game-side) |
| Foveated encoding | Post-render, pre-encode | Encode/decode time + bandwidth | Yes, this is ALVR's domain |
| Clientside foveation | Client GPU (OpenXR) | Client render cost | Yes, via `XR_FB_foveation_vulkan` |

ALVR receives fully-rendered frames and cannot control render-level foveation. It spatially compresses the frame before video encoding, then the client decompresses after decoding.

## ALVR's AADT Algorithm

ALVR uses **Axis-Aligned Distorted Transfer** (reimplementation of Oculus AADT). It compresses lateral edges horizontally and vertical edges vertically, producing a smaller intermediate frame that the encoder processes.

**Pipeline:**
```
Full frame -> AADT compress (GPU shader) -> Encode (NVENC/AMF) -> Network
-> Decode (MediaCodec) -> AADT decompress (GPU shader) -> Display
```

### Configuration Parameters

```rust
FoveatedEncodingConfig {
    center_size_x: f32,    // 0.0-1.0, default 0.45 — center region width ratio
    center_size_y: f32,    // 0.0-1.0, default 0.40 — center region height ratio
    center_shift_x: f32,   // -1.0-1.0, default 0.4 — horizontal offset (nose-ward)
    center_shift_y: f32,   // -1.0-1.0, default 0.1 — vertical offset
    edge_ratio_x: f32,     // 1.0-10.0, default 4.0 — horizontal compression ratio
    edge_ratio_y: f32,     // 1.0-10.0, default 5.0 — vertical compression ratio
}
```

**Defaults rationale:**
- `center_shift_x = 0.4` shifts center toward nose — matches lens sweet spot, not screen center
- `edge_ratio_y > edge_ratio_x` because vertical peripheral vision is less sensitive
- Center region covers roughly the foveal + parafoveal area (~15-20 deg visual angle)

### Resolution Math

The optimized (compressed) resolution is computed per-eye:

```
foveation_scale = center_size + (1 - center_size) / edge_ratio
optimized_resolution = foveation_scale * target_resolution
// Aligned to 32px multiples for encoder compatibility
optimized_aligned = ceil(optimized / 32) * 32
```

With defaults: `scale_x = 0.45 + 0.55/4 = 0.5875`, `scale_y = 0.40 + 0.60/5 = 0.52`.
A 2048x2048 per-eye frame becomes ~1216x1088 -- roughly **37% fewer pixels to encode**.

### Alignment Requirements

All AADT parameters are aligned to `edge_ratio * 2` multiples to prevent seam artifacts at region boundaries. The shader constants (`c0`, `c1`, `c2`, `lo_bound`, `hi_bound`, `a_left`, `b_left`, `a_right`, `b_right`, `c_right`) define the piecewise-linear compression mapping. See `references/aadt-algorithm.md` for the full derivation.

## Foveation Approaches Compared

### Image-Space Compression (ALVR's approach)

Spatially warp the frame to reduce peripheral pixel density before encoding.

**Pros:** Codec-agnostic, works with any encoder, simple decode on mobile.
**Cons:** Introduces resampling artifacts, limited compression curves.

**ALVR history:**
1. **Warp** — radial tangent-function compression. Problem: overall blur.
2. **Slices** — 9-section decomposition with per-section resolution. Problem: complexity, visible borders.
3. **AADT** — axis-aligned edge compression (current). Best balance of simplicity, quality, and mobile GPU cost.

### Encoder-Level ROI (Alternative)

Tell the encoder which regions matter via QP offset maps or ROI rectangles.

**NVENC ROI encoding:**
- Set per-macroblock (16x16 for H.264, CTU for HEVC) QP offsets
- Negative QP delta = higher quality, positive = lower quality
- Typical range: -10 (center) to +15 (far peripheral)
- Requires `NV_ENC_CONFIG::rcParams.enableExtQPDeltaMap = 1`
- Map dimensions: `ceil(width/mbSize) * ceil(height/mbSize)`

**HEVC tile-based foveation:**
- Divide frame into tiles with independent QP
- Fewer tiles = less overhead but coarser control
- Useful for 2x2 or 3x3 grid with center tile at base QP

See `references/roi-encoding.md` for NVENC API details and QP map construction.

### Why ALVR Uses Image-Space Over ROI

1. **Decode cost**: ROI encoding still sends full-resolution frames — the client must decode at full res. AADT reduces decode resolution.
2. **Mobile constraint**: Quest's MediaCodec has fixed decode throughput. Smaller frames = faster decode = lower latency.
3. **Bandwidth**: AADT physically removes pixels. ROI keeps all pixels but shifts bits. AADT saves more bandwidth at same bitrate.
4. **Simplicity**: QP maps need per-frame encoder configuration. AADT is a static shader pass.

## Quality Regions

Human vision has three relevant zones:

| Zone | Visual Angle | Acuity | Encoding Strategy |
|------|-------------|--------|-------------------|
| Fovea | 0-5 deg | Full | Original resolution |
| Parafovea | 5-10 deg | ~50% | Slight compression acceptable |
| Periphery | >10 deg | <20% | Aggressive compression |

**Mapping to ALVR config:**
- `center_size` controls fovea + parafovea coverage
- `edge_ratio` controls peripheral compression aggressiveness
- At typical HMD FoV (~90 deg per eye), `center_size_x = 0.45` covers ~40 deg -- well beyond fovea

## Eye Tracking Integration

### Fixed vs Tracked Foveation

| Aspect | Fixed | Eye-Tracked |
|--------|-------|-------------|
| Assumes gaze at | Screen center (+ shift) | Actual gaze point |
| Center region size | Large (must cover likely gaze) | Small (follows actual gaze) |
| Bandwidth savings | 30-40% | 50-70% |
| Latency sensitivity | None | Critical (<20ms eye-to-encode) |
| Hardware required | None | Eye tracker (Quest Pro, Pico 4E, etc.) |

### Gaze-to-Foveation Pipeline

```
Eye tracker -> Gaze point (normalized UV) -> Update center_shift_x/y
-> Recompute shader constants -> Apply to next frame
```

**Latency budget breakdown:**
```
Eye tracker sample:    2-5ms
Gaze prediction:       1-2ms
Network to server:     varies (client->server if client-side tracker)
Shader constant update: <1ms
Frame render:          already in pipeline
Encode:                3-8ms
----------------------------------
Total must be:         <20ms eye-to-encode
```

### Saccade Handling

During saccades (rapid eye movements, 200-700 deg/s), the eye moves faster than the foveation center can follow. Two strategies:

1. **Saccade detection + quality boost**: When saccade velocity exceeds threshold (~100 deg/s), temporarily widen center region or reduce edge_ratio. Reset after fixation detected.

2. **Predictive centering**: Use gaze velocity to predict landing point and pre-shift the foveation center. Risky — misprediction wastes bandwidth.

**ALVR status**: Currently fixed foveation only. Eye tracking integration is planned but not implemented. The `center_shift_x/y` parameters would become dynamic per-frame values.

## Parameter Tuning Guide

### Bandwidth vs Quality Tradeoffs

| Goal | Adjust | Direction |
|------|--------|-----------|
| Reduce bandwidth | Decrease `center_size`, increase `edge_ratio` | More aggressive |
| Reduce artifacts | Increase `center_size`, decrease `edge_ratio` | More conservative |
| Shift sweet spot | Adjust `center_shift_x/y` | Match lens center |
| Handle asymmetric FoV | Different `edge_ratio_x` vs `edge_ratio_y` | Vertical usually higher |

### Quality Falloff Curves

AADT uses a piecewise-linear mapping (not gaussian or stepped). The compression function:
- Center region: 1:1 mapping (no distortion)
- Transition: linear ramp from 1:1 to `1:edge_ratio`
- Edge: constant `1:edge_ratio` compression

**Why not gaussian?** Simpler to compute, fewer shader ALU ops on mobile, predictable alignment to encoder macroblocks.

### Peripheral Quality Floor

Too-aggressive edge ratios cause visible artifacts:
- **>6x**: Visible pixelation during saccades
- **>8x**: Noticeable even with fixed gaze (peripheral shimmer)
- **4-5x**: Safe default, barely perceptible

Saccades temporarily move high-acuity vision into the compressed zone. Users see the low-quality peripheral content for 50-100ms before fixating on the new center. This is why the peripheral quality floor matters more than static analysis suggests.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Visible foveation boundaries | Increase `center_size` or decrease `edge_ratio` — the transition is too sharp |
| Quality swimming on head turns | The compressed zone moves with head motion. Ensure edge_ratio is conservative enough that peripheral compression isn't visible during rotation |
| Disabling foveated encoding | ALVR warns: "may result in significantly higher encode/decode times and stuttering, or even crashing" — the full-res encode can exceed the latency budget |
| Encoder alignment mismatch | Optimized resolution must be aligned to 32px multiples for hardware encoders. ALVR handles this, but custom implementations must too |
| Center shift vs lens offset | `center_shift_x` accounts for the fact that lens optical center is nasal-shifted. Don't zero it unless testing |
| Asymmetric eye rendering | ALVR computes per-eye, applying same config to both. For stereo, the center_shift is mirrored |
| Clientside foveation stacking | `clientside_foveation` (OpenXR `XR_FB_foveation_vulkan`) is separate from encode foveation. Both can be active — render foveation reduces Quest GPU load, encode foveation reduces bandwidth |
| Codec choice interaction | HEVC handles foveation better than H.264 at low bitrates due to larger CTU sizes. AV1 even better with its flexible tile/SB structure |

## Encoder Configuration Context

ALVR's encoder settings interact with foveation:

**NVENC tuning for foveated frames:**
- `quality_preset: P1` (default) — fastest, fine for already-compressed frames
- `adaptive_quantization_mode: Spatial` — helps allocate bits to remaining detail
- `multi_pass: QuarterResolution` — reduces banding in compressed regions
- `rate_control_mode: CBR` — predictable bandwidth with foveated frames

**AMF:**
- `enable_vbaq: true` — Variance Based Adaptive Quantization helps with foveated content
- `enable_hmqb: true` — High Motion Quality Boost helps during fast head rotations

## Clientside Foveation (OpenXR)

Separate from encode foveation. Reduces render resolution on the Quest GPU:

```rust
ClientsideFoveationConfig {
    mode: Static { level: Low/Medium/High } | Dynamic { max_level: ... },
    vertical_offset_deg: f32,  // -45 to +45 deg
}
```

- **Static**: Fixed foveation level, predictable performance
- **Dynamic**: Runtime adjusts level based on GPU load — can cause quality fluctuation
- **vertical_offset_deg**: Shifts foveation center vertically for games with non-centered UI

This is **render-level** foveation (via `XR_FB_foveation_vulkan`), orthogonal to ALVR's encode foveation.

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `aadt-algorithm.md` | Understanding AADT shader math, compression mapping derivation, alignment calculations |
| `roi-encoding.md` | Implementing NVENC ROI encoding, QP offset maps, HEVC tile foveation, comparing with image-space approach |

## ALVR Codebase Pointers

| Component | Path (relative to alvr repo root) |
|-----------|------|
| Foveated encoding config | `alvr/session/src/settings.rs` — `FoveatedEncodingConfig` struct |
| AADT shader constants | `alvr/graphics/src/stream.rs` — `foveated_encoding_shader_constants()` |
| D3D11 FFR pipeline (Windows) | `alvr/server_openvr/cpp/platform/win32/FFR.cpp` |
| Client decompression | `alvr/client_core/src/connection.rs` — decoder pipeline |
| Clientside foveation config | `alvr/session/src/settings.rs` — `ClientsideFoveationConfig` |
| NVENC encoder config | `alvr/session/src/settings.rs` — `NvencConfig` |
| Server connection setup | `alvr/server_core/src/connection.rs` — passes foveation params to OpenVR config |
| Wiki: FFR explanation | `wiki/Fixed-Foveated-Rendering-(FFR).md` |
| Wiki: How ALVR works | `wiki/How-ALVR-works.md` — foveated encoding section |
