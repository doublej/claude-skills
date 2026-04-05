# ROI Encoding — Region of Interest Quality Control

## Overview

ROI (Region of Interest) encoding tells the video encoder to allocate more bits to important regions and fewer bits to peripheral regions. Unlike image-space compression (AADT), ROI encoding keeps the frame at full resolution but varies quality spatially.

## NVENC ROI Encoding

### Enabling ROI

```c
NV_ENC_CONFIG encConfig = {};
// ... standard config setup ...

// Enable external QP delta map
encConfig.rcParams.enableExtQPDeltaMap = 1;
```

### QP Delta Map Structure

The map specifies per-macroblock QP offsets relative to the base QP:

```c
// For H.264: 16x16 macroblocks
// For HEVC: depends on CTU size (32x32 or 64x64)
uint32_t mb_width  = (frame_width + 15) / 16;   // H.264
uint32_t mb_height = (frame_height + 15) / 16;

// Map is int8_t array, one value per macroblock
int8_t* qp_delta_map = malloc(mb_width * mb_height);

// Negative = higher quality, positive = lower quality
// Range: approximately -51 to +51 (limited by base QP)
```

### Constructing a Foveation QP Map

```c
void build_foveation_qp_map(
    int8_t* map,
    uint32_t mb_width, uint32_t mb_height,
    float center_x, float center_y,     // normalized 0-1
    float fovea_radius,                   // normalized, ~0.15 for 15deg at 100deg FoV
    float mid_radius,                     // normalized, ~0.35
    int8_t fovea_delta,                   // e.g., -10
    int8_t mid_delta,                     // e.g., 0
    int8_t peripheral_delta               // e.g., +15
) {
    for (uint32_t y = 0; y < mb_height; y++) {
        for (uint32_t x = 0; x < mb_width; x++) {
            float nx = (x + 0.5f) / mb_width;
            float ny = (y + 0.5f) / mb_height;
            float dx = nx - center_x;
            float dy = ny - center_y;
            float dist = sqrtf(dx*dx + dy*dy);

            if (dist < fovea_radius) {
                map[y * mb_width + x] = fovea_delta;
            } else if (dist < mid_radius) {
                // Linear interpolation for smooth transition
                float t = (dist - fovea_radius) / (mid_radius - fovea_radius);
                map[y * mb_width + x] = (int8_t)(fovea_delta + t * (mid_delta - fovea_delta));
            } else {
                float t = fminf((dist - mid_radius) / (1.0f - mid_radius), 1.0f);
                map[y * mb_width + x] = (int8_t)(mid_delta + t * (peripheral_delta - mid_delta));
            }
        }
    }
}
```

### Submitting the QP Map

```c
NV_ENC_PIC_PARAMS picParams = {};
// ... standard per-frame setup ...

picParams.qpDeltaMap     = qp_delta_map;
picParams.qpDeltaMapSize = mb_width * mb_height;

nvEncEncodePicture(encoder, &picParams);
```

### QP Delta Guidelines

| Zone | Delta | Visual Effect |
|------|-------|--------------|
| Fovea (0-5 deg) | -10 to -5 | Noticeably sharper center |
| Parafovea (5-15 deg) | -3 to 0 | Baseline quality |
| Near periphery (15-30 deg) | +3 to +8 | Slight softening |
| Far periphery (>30 deg) | +10 to +15 | Visible compression if you look directly |

**Critical**: QP delta is relative to base QP. If base QP is already low (high quality), positive deltas still produce decent quality. If base QP is high (low bitrate), positive deltas may produce visible blocky artifacts.

## HEVC Tile-Based Foveation

HEVC supports independent tiles that can have different QP values. This is coarser than per-CTU ROI but has less overhead.

### Tile Configuration

```c
NV_ENC_CONFIG_HEVC hevcConfig = {};

// Enable tiles
hevcConfig.enableTiles = 1;

// Example: 3x3 grid for center/edge/corner foveation
// Tile column boundaries (in CTU units)
hevcConfig.numTileColumns = 3;
hevcConfig.numTileRows = 3;
```

### Tile QP Assignment

Each tile gets its own slice with independent QP. The encoder assigns quality based on tile position:

```
+--------+--------+--------+
| QP+12  | QP+8   | QP+12  |
| corner  | top    | corner  |
+--------+--------+--------+
| QP+8   | QP-5   | QP+8   |
| left    | CENTER | right   |
+--------+--------+--------+
| QP+12  | QP+8   | QP+12  |
| corner  | bottom | corner  |
+--------+--------+--------+
```

### Tile Tradeoffs

| Approach | Granularity | Overhead | Eye-tracking friendly |
|----------|------------|----------|----------------------|
| Per-MB QP map | 16x16 px (H.264) | Low | Yes (update map each frame) |
| Per-CTU QP map | 32/64 px (HEVC) | Low | Yes |
| Tiles | Configurable regions | Medium (tile headers) | Partial (reconfigure tiles is expensive) |

## AV1 Foveation

AV1 offers the most flexible spatial quality control:

- **Superblock partitioning**: 64x64 or 128x128, with recursive subdivision
- **Segment-based QP**: Up to 8 segments with independent QP
- **Film grain synthesis**: Can mask compression artifacts in peripheral regions

AV1 is ideal for ROI foveation but hardware encoder support (especially on mobile decode) is still maturing.

## ROI vs Image-Space: Decision Matrix

| Factor | ROI Encoding | Image-Space (AADT) |
|--------|-------------|-------------------|
| Output resolution | Full (same as input) | Reduced |
| Decode cost | Full resolution decode | Reduced resolution decode |
| Bandwidth at same bitrate | Same frame size, varied quality | Smaller frame, uniform quality |
| Artifact type | Blockiness in periphery | Resampling blur in periphery |
| Eye tracking integration | Update QP map per frame (cheap) | Recompute shader constants per frame |
| Encoder compatibility | NVENC, AMF, x264/x265, SVT-AV1 | Any (preprocessing step) |
| Mobile decode perf | No benefit (full res decode) | Significant benefit (smaller decode) |
| Can combine with AADT? | Yes — AADT shrinks, ROI varies quality within shrunk frame | N/A |

## Combining ROI + Image-Space

For maximum savings, apply both:

1. AADT compresses the frame spatially (reduces decode cost + bandwidth)
2. ROI encoding within the compressed frame allocates bits to the still-important center

The ROI map for the compressed frame should account for the fact that the center region in the compressed frame is already the high-detail area. A mild fovea_delta of -3 to -5 on the compressed frame's center further sharpens the most critical region.

## NVENC API Gotchas

- `qpDeltaMap` is only respected when `rateControlMode` is `NV_ENC_PARAMS_RC_CBR` or `NV_ENC_PARAMS_RC_VBR`. It is ignored with CQP.
- The map must be updated every frame. NVENC does not cache it.
- Map dimensions must exactly match `ceil(width/mbSize) * ceil(height/mbSize)`. Off-by-one causes silent corruption.
- On some driver versions, ROI with B-frames can cause quality fluctuation. For VR streaming, B-frames are typically disabled anyway (latency).
- `enableExtQPDeltaMap` and `enableMinQP`/`enableMaxQP` can conflict. Test combinations carefully.
- ROI encoding adds ~0.5-1ms to encode time due to the additional per-MB decision.

## Eye Tracking + ROI

ROI encoding is naturally suited for eye-tracked foveation because updating the QP map center position is trivial:

```c
// Each frame: update center based on gaze
float gaze_x = eye_tracker_get_gaze_x();  // normalized 0-1
float gaze_y = eye_tracker_get_gaze_y();

build_foveation_qp_map(
    qp_map, mb_width, mb_height,
    gaze_x, gaze_y,     // dynamic center
    0.08f,               // tighter fovea radius (eye-tracked)
    0.25f,               // tighter mid radius
    -8, 0, +12           // more aggressive deltas (smaller fovea)
);
```

With eye tracking, the fovea radius can be much smaller (0.08 vs 0.15 for fixed) because we know exactly where the user looks. This yields greater peripheral savings.

**Latency concern**: The QP map update must be synchronized with the frame that was rendered using the same gaze data. Stale gaze data means the high-quality region trails the actual gaze point, which is perceptible.
