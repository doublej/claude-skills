# AMF Detailed Reference

## Property Naming Convention

AMF uses different property name prefixes per codec:

| Codec | Component ID | Property Prefix |
|-------|-------------|-----------------|
| H.264 | `AMFVideoEncoderVCE_AVC` | `AMF_VIDEO_ENCODER_*` |
| HEVC | `AMFVideoEncoder_HEVC` | `AMF_VIDEO_ENCODER_HEVC_*` |
| AV1 | `AMFVideoEncoder_AV1` | `AMF_VIDEO_ENCODER_AV1_*` |

**Pitfall**: Using H.264 property names on an HEVC encoder silently fails. Always match prefix to codec.

## HEVC Configuration

```cpp
auto encoder = /* CreateComponent with AMFVideoEncoder_HEVC */;

encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_USAGE,
                     AMF_VIDEO_ENCODER_HEVC_USAGE_ULTRA_LOW_LATENCY);
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_QUALITY_PRESET,
                     AMF_VIDEO_ENCODER_HEVC_QUALITY_PRESET_SPEED);
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_PROFILE, AMF_VIDEO_ENCODER_HEVC_PROFILE_MAIN);

// 10-bit
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_PROFILE, AMF_VIDEO_ENCODER_HEVC_PROFILE_MAIN_10);
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_COLOR_BIT_DEPTH,
                     AMF_COLOR_BIT_DEPTH_10);

// Rate control
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_RATE_CONTROL_METHOD,
                     AMF_VIDEO_ENCODER_HEVC_RATE_CONTROL_METHOD_CBR);
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_TARGET_BITRATE, bitrate);
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_PEAK_BITRATE, bitrate);
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_FRAMESIZE, AMFConstructSize(w, h));
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_FRAMERATE, AMFConstructRate(fps, 1));

// No B-frames
encoder->SetProperty(AMF_VIDEO_ENCODER_HEVC_MAX_NUM_REFRAMES, 1);
```

## AV1 Configuration

```cpp
auto encoder = /* CreateComponent with AMFVideoEncoder_AV1 */;

encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_USAGE,
                     AMF_VIDEO_ENCODER_AV1_USAGE_ULTRA_LOW_LATENCY);
encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_QUALITY_PRESET,
                     AMF_VIDEO_ENCODER_AV1_QUALITY_PRESET_SPEED);
encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_RATE_CONTROL_METHOD,
                     AMF_VIDEO_ENCODER_AV1_RATE_CONTROL_METHOD_CBR);
encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_TARGET_BITRATE, bitrate);
encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_PEAK_BITRATE, bitrate);
encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_FRAMESIZE, AMFConstructSize(w, h));
encoder->SetProperty(AMF_VIDEO_ENCODER_AV1_FRAMERATE, AMFConstructRate(fps, 1));
```

AV1 on AMF requires RDNA3 (RX 7000 series) or newer.

## Rate Control Methods

| Method | H.264 Constant | When |
|--------|----------------|------|
| CBR | `AMF_VIDEO_ENCODER_RATE_CONTROL_METHOD_CBR` | VR default |
| Peak-constrained VBR | `AMF_VIDEO_ENCODER_RATE_CONTROL_METHOD_PEAK_CONSTRAINED_VBR` | Pre-analysis required |
| Latency-constrained VBR | `AMF_VIDEO_ENCODER_RATE_CONTROL_METHOD_LATENCY_CONSTRAINED_VBR` | VR alternative to CBR |
| CQP | `AMF_VIDEO_ENCODER_RATE_CONTROL_METHOD_CONSTANT_QP` | Testing only |

**Latency-constrained VBR**: AMF-specific mode. Aims to hit target bitrate while prioritizing latency -- frames that would exceed budget get lower quality rather than stalling. Good alternative to CBR for VR.

**Filler data**: Required for CBR to work correctly on some AMD hardware. Without it, the actual bitrate may fluctuate:

```cpp
encoder->SetProperty(AMF_VIDEO_ENCODER_FILLER_DATA_ENABLE, true);
```

ALVR defaults filler data to disabled because it wastes bandwidth; the bitrate fluctuation is acceptable for adaptive streaming.

## Quality Enhancement Properties

### VBAQ (Variance Based Adaptive Quantization)

```cpp
encoder->SetProperty(AMF_VIDEO_ENCODER_ENABLE_VBAQ, true);
```

Allocates more bits to smooth/flat areas (where artifacts are most visible) and fewer to highly textured areas. Safe for VR with negligible performance cost.

### High Motion Quality Boost (HMQB)

```cpp
encoder->SetProperty(AMF_VIDEO_ENCODER_HIGH_MOTION_QUALITY_BOOST_ENABLE, true);
```

Pre-analyzes motion vectors and allocates more bits to high-motion regions. Small performance cost but noticeable quality improvement in fast-moving VR scenes.

### Pre-Analysis Pipeline

```cpp
// Requires: use_preproc=true AND NOT 10-bit
encoder->SetProperty(AMF_VIDEO_ENCODER_PRE_ANALYSIS_ENABLE, true);
```

**Constraints**:
- Only works with `PEAK_CONSTRAINED_VBR` rate control
- Requires preprocessor (`use_preproc`) to be enabled
- Incompatible with 10-bit encoding
- Not all GPUs support it (query `AMF_VIDEO_ENCODER_CAP_PRE_ANALYSIS`)
- **Adds significant latency** -- not recommended for VR

### Preprocessor

```cpp
encoder->SetProperty(AMF_VIDEO_ENCODER_PRE_ANALYSIS_ENABLE, true);
// Noise reduction parameters
// preproc_sigma: strength (0-10, default 4)
// preproc_tor: tolerance (0-10, default 7)
```

Applies noise reduction before encoding. Can improve compression efficiency for noisy sources, but VR renders are typically clean -- limited benefit.

## AMF Surface Management

### Surface Allocation

```cpp
amf::AMFSurfacePtr surface;
// From system memory
context->AllocSurface(amf::AMF_MEMORY_HOST, format, w, h, &surface);

// From D3D11 texture (zero-copy)
context->CreateSurfaceFromDX11Native(texture, &surface, nullptr);
```

### Surface Formats

| Format | Use |
|--------|-----|
| `AMF_SURFACE_RGBA` | Standard SDR input |
| `AMF_SURFACE_NV12` | SDR with HDR bypass (pre-converted) |
| `AMF_SURFACE_P010` | HDR 10-bit |
| `AMF_SURFACE_BGRA` | Alternative SDR |

### Input/Output Flow

```
SubmitInput(surface) -> encoder processes -> QueryOutput(&data)
```

`SubmitInput` can return:
- `AMF_OK` -- accepted
- `AMF_INPUT_FULL` -- encoder busy, try again after QueryOutput
- `AMF_EOF` -- after Drain(), no more input accepted

`QueryOutput` can return:
- `AMF_OK` -- data available
- `AMF_REPEAT` -- not ready yet, poll again
- `AMF_EOF` -- no more output

### Polling Pattern for VR

```cpp
void AMFPipe::doPassthrough(uint32_t timerResolution) {
    amf::AMFDataPtr data;
    uint16_t timeout = 1000;  // max 1 second

    AMF_RESULT res = encoder->QueryOutput(&data);
    timeBeginPeriod(timerResolution);  // Windows timer resolution
    while (!data && --timeout != 0) {
        amf_sleep(1);
        res = encoder->QueryOutput(&data);
    }
    timeEndPeriod(timerResolution);

    if (data) {
        processOutput(data);
    }
}
```

**Critical**: Always set `timeBeginPeriod(1)` around tight polling loops on Windows, or the 1ms sleep becomes 15ms.

## Color Management

### SDR Color

```cpp
// H.264
encoder->SetProperty(AMF_VIDEO_ENCODER_FULL_RANGE_COLOR, true);
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_COLOR_PROFILE,
                     AMF_VIDEO_CONVERTER_COLOR_PROFILE_FULL_709);
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_TRANSFER_CHARACTERISTIC,
                     AMF_COLOR_TRANSFER_CHARACTERISTIC_GAMMA22);
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_COLOR_PRIMARIES,
                     AMF_COLOR_PRIMARIES_BT709);
```

### HDR Color

```cpp
// Input signaling (tells encoder what you're feeding)
encoder->SetProperty(AMF_VIDEO_ENCODER_INPUT_COLOR_PROFILE,
                     AMF_VIDEO_CONVERTER_COLOR_PROFILE_FULL_2020);
encoder->SetProperty(AMF_VIDEO_ENCODER_INPUT_TRANSFER_CHARACTERISTIC,
                     AMF_COLOR_TRANSFER_CHARACTERISTIC_GAMMA22);
encoder->SetProperty(AMF_VIDEO_ENCODER_INPUT_COLOR_PRIMARIES,
                     AMF_COLOR_PRIMARIES_BT2020);

// Output signaling (metadata in bitstream)
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_COLOR_PROFILE,
                     AMF_VIDEO_CONVERTER_COLOR_PROFILE_FULL_2020);
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_TRANSFER_CHARACTERISTIC,
                     AMF_COLOR_TRANSFER_CHARACTERISTIC_GAMMA22);
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_COLOR_PRIMARIES,
                     AMF_COLOR_PRIMARIES_BT2020);
```

**Pitfall**: If input and output color profiles don't match, AMF will attempt a color space conversion internally, adding latency and potentially mangling colors. For VR, set both identically.

## IDR Insertion (AMF)

```cpp
// H.264: set per-frame property on the surface
surface->SetProperty(AMF_VIDEO_ENCODER_FORCE_PICTURE_TYPE,
                     AMF_VIDEO_ENCODER_PICTURE_TYPE_IDR);

// HEVC
surface->SetProperty(AMF_VIDEO_ENCODER_HEVC_FORCE_PICTURE_TYPE,
                     AMF_VIDEO_ENCODER_HEVC_PICTURE_TYPE_IDR);
```

Unlike NVENC where you pass flags to EncodeFrame, AMF sets the IDR flag as a property on the input surface before submitting.

## Capability Queries

```cpp
amf::AMFCapsPtr caps;
if (encoder->GetCaps(&caps) == AMF_OK) {
    bool hasPreAnalysis = false;
    caps->GetProperty(AMF_VIDEO_ENCODER_CAP_PRE_ANALYSIS, &hasPreAnalysis);

    bool hasQueryTimeout = false;
    caps->GetProperty(AMF_VIDEO_ENCODER_CAPS_QUERY_TIMEOUT_SUPPORT, &hasQueryTimeout);
}
```

Always query caps before enabling advanced features -- not all GPUs support all features. Failing to check caps and setting unsupported properties is silently ignored by AMF (no error returned).

## AMD Hardware Generations

| Generation | Architecture | HW Encode | AV1 Encode |
|------------|-------------|-----------|------------|
| Polaris | GCN4 | VCN 1.0 | No |
| Vega | GCN5 | VCN 1.0 | No |
| Navi 1x | RDNA1 | VCN 2.0 | No |
| Navi 2x | RDNA2 | VCN 3.0 | No |
| Navi 3x | RDNA3 | VCN 4.0 | Yes |
| Navi 4x | RDNA4 | VCN 5.0 | Yes |

## Common AMF Error Codes

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| `AMF_OK` | Success | -- |
| `AMF_INPUT_FULL` | Encoder queue full | Query output before submitting more |
| `AMF_REPEAT` | Output not ready | Keep polling |
| `AMF_EOF` | End of stream | After Drain() |
| `AMF_NOT_SUPPORTED` | Feature unavailable | GPU doesn't support this codec/feature |
| `AMF_FAIL` | Generic failure | Check driver version, re-init context |
| `AMF_NEED_MORE_INPUT` | Encoder needs more frames | Submit another frame (rare in low-latency mode) |
