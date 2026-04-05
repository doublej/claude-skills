---
name: nvenc-amf-encoding
description: "NVENC/AMF hardware encoder tuning for low-latency H.264/HEVC/AV1 streaming"
---

# NVENC / AMF Hardware Encoding

## Before Configuring

1. **Identify the GPU vendor** -- NVENC (NVIDIA) and AMF (AMD) have different APIs, presets, and property names
2. **Identify the codec** -- H.264, HEVC, or AV1. Each has different config structs and capability levels
3. **Identify the use case** -- VR streaming, game streaming, recording, or transcoding dictate very different parameter choices
4. **Check driver version** -- encoder capabilities depend on driver, not just hardware generation

## VR Streaming Encoder Pipeline

Typical flow for ALVR and similar VR streamers:

```
GPU render -> texture copy -> HW encode -> NAL parse -> network send
                                |
                        NVENC or AMF session
```

Key constraints:
- Encode must complete within frame budget (e.g., <8ms at 120Hz)
- Single-frame latency: no B-frames, no lookahead, no reordering
- Bitrate adapts dynamically based on network conditions
- IDR insertion is manual (on packet loss), not periodic

## NVENC Configuration (NVIDIA)

### Preset x Tuning Matrix

NVENC uses a two-axis system: **quality preset** (P1-P7) and **tuning info**.

| Preset | Speed | Quality | VR Streaming Use |
|--------|-------|---------|------------------|
| P1 | Fastest | Lowest | Default for VR -- meets frame budget |
| P2-P3 | Fast | Low-Med | Good tradeoff if GPU has headroom |
| P4 | Medium | Medium | Balanced -- test with your target framerate |
| P5 | Slow | High | Only if GPU is significantly overpowered |
| P6-P7 | Slowest | Highest | Too slow for real-time VR |

| Tuning | Purpose |
|--------|---------|
| `NV_ENC_TUNING_INFO_LOW_LATENCY` | VR/game streaming default |
| `NV_ENC_TUNING_INFO_ULTRA_LOW_LATENCY` | Aggressive -- may reduce quality |
| `NV_ENC_TUNING_INFO_HIGH_QUALITY` | Recording, not for VR |
| `NV_ENC_TUNING_INFO_LOSSLESS` | Lossless mode, very high bitrate |

Setting tuning info auto-configures most latency-related params. Override individual settings only when needed.

### Initialization Pattern (C++)

```cpp
NV_ENC_INITIALIZE_PARAMS initParams = { NV_ENC_INITIALIZE_PARAMS_VER };
NV_ENC_CONFIG encodeConfig = { NV_ENC_CONFIG_VER };
initParams.encodeConfig = &encodeConfig;

// Let SDK set defaults for preset+tuning combo
encoder->CreateDefaultEncoderParams(
    &initParams,
    NV_ENC_CODEC_H264_GUID,      // or HEVC/AV1
    NV_ENC_PRESET_P1_GUID,        // P1 for VR
    NV_ENC_TUNING_INFO_LOW_LATENCY
);

// Override specifics
initParams.encodeWidth = width;
initParams.encodeHeight = height;
initParams.frameRateNum = 90;  // match HMD refresh
initParams.frameRateDen = 1;

// VR-critical overrides
encodeConfig.gopLength = NVENC_INFINITE_GOPLENGTH;  // no auto-IDR
encodeConfig.frameIntervalP = 1;                     // no B-frames

// Rate control
encodeConfig.rcParams.rateControlMode = NV_ENC_PARAMS_RC_CBR;
uint32_t maxFrameSize = bitrate_bps / refreshRate;
encodeConfig.rcParams.vbvBufferSize = maxFrameSize * 1.1;
encodeConfig.rcParams.vbvInitialDelay = maxFrameSize * 1.1;
encodeConfig.rcParams.maxBitRate = bitrate_bps;
encodeConfig.rcParams.averageBitRate = bitrate_bps;
```

### Codec-Specific Config

```cpp
// H.264
auto& h264 = encodeConfig.encodeCodecConfig.h264Config;
h264.repeatSPSPPS = 1;           // SPS/PPS with every IDR
h264.idrPeriod = NVENC_INFINITE_GOPLENGTH;
h264.maxNumRefFrames = 0;        // SDK default (usually 1-2)
h264.entropyCodingMode = NV_ENC_H264_ENTROPY_CODING_MODE_CAVLC; // faster decode

// HEVC
auto& hevc = encodeConfig.encodeCodecConfig.hevcConfig;
hevc.repeatSPSPPS = 1;
hevc.idrPeriod = NVENC_INFINITE_GOPLENGTH;
hevc.maxNumRefFramesInDPB = 0;

// AV1
auto& av1 = encodeConfig.encodeCodecConfig.av1Config;
av1.repeatSeqHdr = 1;
av1.idrPeriod = NVENC_INFINITE_GOPLENGTH;
```

### Dynamic Reconfiguration

NVENC supports mid-stream bitrate/framerate changes without reinitializing:

```cpp
NV_ENC_RECONFIGURE_PARAMS reconfig = { NV_ENC_RECONFIGURE_PARAMS_VER };
reconfig.reInitEncodeParams = initParams;  // updated params
encoder->Reconfigure(&reconfig);
```

### IDR Insertion

For VR, disable automatic IDR and insert manually on packet loss:

```cpp
NV_ENC_PIC_PARAMS picParams = {};
if (need_idr) {
    picParams.encodePicFlags = NV_ENC_PIC_FLAG_FORCEIDR;
}
encoder->EncodeFrame(packets, &picParams);
```

### Multi-Pass and Adaptive Quantization

| Feature | Setting | Effect on VR |
|---------|---------|--------------|
| Multi-pass (1/4 res) | `NV_ENC_TWO_PASS_QUARTER_RESOLUTION` | Small quality gain, minimal perf cost |
| Multi-pass (full res) | `NV_ENC_TWO_PASS_FULL_RESOLUTION` | Better quality, higher latency |
| Spatial AQ | `enableAQ = 1` | Reduces banding, good default |
| Temporal AQ | `enableTemporalAQ = 1` | Better overall quality, tiny perf cost |

### Intra Refresh (Alternative to IDR)

Spreads intra-coded macroblocks across frames instead of one large IDR spike:

```cpp
config.enableIntraRefresh = 1;
config.intraRefreshPeriod = 60;  // frames between full refresh cycles
config.intraRefreshCnt = 5;      // how many frames the refresh wave spans
```

**Tradeoff**: smoother bitrate but slower error recovery than instant IDR.

## AMF Configuration (AMD)

### Quality Presets

| Preset | Constant | VR Use |
|--------|----------|--------|
| Speed | `AMF_VIDEO_ENCODER_QUALITY_PRESET_SPEED` | Default for VR |
| Balanced | `AMF_VIDEO_ENCODER_QUALITY_PRESET_BALANCED` | If GPU has headroom |
| Quality | `AMF_VIDEO_ENCODER_QUALITY_PRESET_QUALITY` | Not for real-time VR |

### Usage Modes

| Mode | Constant | Purpose |
|------|----------|---------|
| Ultra Low Latency | `AMF_VIDEO_ENCODER_USAGE_ULTRA_LOW_LATENCY` | VR streaming (recommended) |
| Low Latency | `AMF_VIDEO_ENCODER_USAGE_LOW_LATENCY` | Game streaming |
| Webcam | `AMF_VIDEO_ENCODER_USAGE_WEBCAM` | Video chat |
| Transcoding | `AMF_VIDEO_ENCODER_USAGE_TRANSCODING` | Offline processing |

### Initialization Pattern (C++)

```cpp
amf::AMFComponentPtr encoder;
factory->CreateComponent(context, AMFVideoEncoderVCE_AVC, &encoder);
// HEVC: AMFVideoEncoder_HEVC, AV1: AMFVideoEncoder_AV1

// H.264 VR config
encoder->SetProperty(AMF_VIDEO_ENCODER_USAGE, AMF_VIDEO_ENCODER_USAGE_ULTRA_LOW_LATENCY);
encoder->SetProperty(AMF_VIDEO_ENCODER_PROFILE, AMF_VIDEO_ENCODER_PROFILE_HIGH);
encoder->SetProperty(AMF_VIDEO_ENCODER_PROFILE_LEVEL, 42);
encoder->SetProperty(AMF_VIDEO_ENCODER_B_PIC_PATTERN, 0);           // no B-frames
encoder->SetProperty(AMF_VIDEO_ENCODER_QUALITY_PRESET,
                     AMF_VIDEO_ENCODER_QUALITY_PRESET_SPEED);
encoder->SetProperty(AMF_VIDEO_ENCODER_TARGET_BITRATE, bitrate_bps);
encoder->SetProperty(AMF_VIDEO_ENCODER_PEAK_BITRATE, bitrate_bps);
encoder->SetProperty(AMF_VIDEO_ENCODER_FRAMESIZE, AMFConstructSize(w, h));
encoder->SetProperty(AMF_VIDEO_ENCODER_FRAMERATE, AMFConstructRate(fps, 1));

// Rate control
encoder->SetProperty(AMF_VIDEO_ENCODER_RATE_CONTROL_METHOD,
                     AMF_VIDEO_ENCODER_RATE_CONTROL_METHOD_CBR);
encoder->SetProperty(AMF_VIDEO_ENCODER_FILLER_DATA_ENABLE, false);
```

### AMF Quality Enhancements

| Feature | Property | Effect |
|---------|----------|--------|
| VBAQ | `AMF_VIDEO_ENCODER_ENABLE_VBAQ` | Allocates more bits to smooth areas, reduces banding |
| HMQB | `AMF_VIDEO_ENCODER_HIGH_MOTION_QUALITY_BOOST_ENABLE` | Motion-aware encoding, slight perf cost |
| Pre-analysis | `AMF_VIDEO_ENCODER_PRE_ANALYSIS_ENABLE` | Higher quality, significant latency increase |
| Preprocessor | `AMF_VIDEO_ENCODER_PRE_ANALYSIS_ENABLE` + preproc | Noise reduction before encode |

**VBAQ**: safe to enable for VR, negligible perf impact.
**HMQB**: safe for VR, small benefit in fast-motion scenes.
**Pre-analysis**: avoid for VR -- adds latency. Only useful for recording.

### AMF Submit/Query Pattern

AMF uses an async submit/query model unlike NVENC's synchronous EncodeFrame:

```cpp
// Submit
amf::AMFSurfacePtr surface;
context->AllocSurface(amf::AMF_MEMORY_DX11, format, w, h, &surface);
// ... copy texture to surface ...
encoder->SubmitInput(surface);

// Query (may need polling)
amf::AMFDataPtr data;
AMF_RESULT res = encoder->QueryOutput(&data);
if (res == AMF_OK && data) {
    amf::AMFBufferPtr buffer(data);
    // buffer->GetNative() -> bitstream pointer
    // buffer->GetSize() -> bitstream size
}
// res == AMF_REPEAT means try again
```

**Pitfall**: `QueryOutput` may return `AMF_REPEAT` -- you must poll. For VR, use `QueryOutput` with a tight timeout loop (1ms sleep between polls, max ~16ms total).

## Rate Control for VR

| Mode | When to Use | Notes |
|------|-------------|-------|
| **CBR** | Default for VR | Predictable bitrate, works with adaptive algorithms |
| **VBR** | If network has headroom | May confuse adaptive bitrate controllers |
| **CQP** | Debugging/testing only | Fixed quality, unpredictable bitrate |

CBR + adaptive bitrate (measuring network throughput and adjusting target) is the standard approach for VR streaming.

### VBV Buffer Sizing

For minimum latency, set VBV buffer to ~1 frame worth of bits:

```
vbvBufferSize = bitrate_bps / framerate * 1.1
```

Larger buffers allow better quality but add latency. For VR, keep it tight.

## Entropy Coding: CAVLC vs CABAC

| | CAVLC | CABAC |
|--|-------|-------|
| Decode speed | Faster | Slower |
| Compression | ~10-15% worse | Better |
| VR recommendation | Default | Only if decoder handles it well |

ALVR defaults to CAVLC because mobile VR decoders (Quest) handle it faster. If your target decoder is powerful (PC-to-PC streaming), CABAC is fine.

## Color Configuration

### Standard Dynamic Range

```cpp
// NVENC
config.h264VUIParameters.videoFullRangeFlag = 1;  // full range (0-255)
config.h264VUIParameters.colourPrimaries = NV_ENC_VUI_COLOR_PRIMARIES_BT709;
config.h264VUIParameters.transferCharacteristics = NV_ENC_VUI_TRANSFER_CHARACTERISTIC_SRGB;

// AMF
encoder->SetProperty(AMF_VIDEO_ENCODER_FULL_RANGE_COLOR, true);
encoder->SetProperty(AMF_VIDEO_ENCODER_OUTPUT_COLOR_PROFILE,
                     AMF_VIDEO_CONVERTER_COLOR_PROFILE_FULL_709);
```

### HDR

Use BT.2020 primaries with 10-bit encoding:

```cpp
// NVENC: NV_ENC_BUFFER_FORMAT_YUV420_10BIT or ABGR10
// AMF: AMF_SURFACE_P010

// Color signaling
colourPrimaries = BT2020;
transferCharacteristics = SRGB;  // sRGB EOTF, not PQ
matrixCoefficients = BT2020_NCL;
```

## Split-Frame Encoding (Ada Lovelace+)

GPUs with multiple NVENC engines (RTX 4090, etc.) can split a frame horizontally across engines:
- Each slice encodes independently and in parallel
- ~4% quality penalty at slice boundaries
- Doubles throughput for high-resolution encoding
- Automatic when using SDK -- driver handles load balancing

Not user-configurable via the encode API directly; the driver decides based on resolution and available engines.

## Session Limits

| GPU Class | Max Concurrent Sessions |
|-----------|------------------------|
| GeForce (pre-2024) | 3 |
| GeForce (2024+) | 8 |
| GeForce (2025+) | 12 |
| Quadro/RTX Pro (high-end) | Unlimited |

Exceeding the limit returns `NV_ENC_ERR_OUT_OF_MEMORY` on session creation.

## ALVR Integration Notes

ALVR's encoder lives in C++ (`alvr/server_openvr/cpp/platform/`) with Rust FFI:

- **Windows**: `VideoEncoderNVENC.cpp` (direct NVENC SDK), `VideoEncoderAMF.cpp` (AMF SDK)
- **Linux**: `EncodePipelineNvEnc.cpp`, `EncodePipelineVAAPI.cpp` (FFmpeg-based)
- **FFI boundary**: C++ calls `ParseFrameNals()` which calls Rust `send_video()` via callback
- **Dynamic params**: Rust `BitrateManager` computes bitrate/framerate, C++ reads via `GetDynamicEncoderParams()`
- **Settings flow**: Rust `settings.rs` defines `NvencConfig`/`AmfConfig` structs -> C++ `Settings` reads them
- **Codec selection**: H.264 default, HEVC for better quality at cost of encoder latency
- **AV1**: Supported on NVENC (Ada+) and AMF (RDNA3+), requires IVF header stripping on NVENC

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Encoder stall / timeout | Frame too complex for preset+bitrate | Lower preset (P1), increase bitrate, or reduce resolution |
| `NV_ENC_ERR_OUT_OF_MEMORY` | Session limit hit or VRAM exhaustion | Close other encoder sessions; check session count |
| Bitrate spikes on IDR | IDR frame much larger than P-frames | Enable intra refresh, or increase VBV buffer slightly |
| Washed-out colors | Wrong color range (limited vs full) | Set `videoFullRangeFlag=1` / `FULL_RANGE_COLOR=true` |
| Green/purple artifacts | Surface format mismatch | Verify NV12/P010/ABGR matches input texture format |
| AMF `QueryOutput` hangs | No timeout on query loop | Add max iteration count with 1ms sleep |
| Runaway latency (CABAC) | Decoder can't keep up with CABAC | Switch to CAVLC |
| Quality degrades over time | No IDR sent after packet loss | Implement IDR-on-loss with `NV_ENC_PIC_FLAG_FORCEIDR` |
| Encoder returns empty output | Input surface not properly filled | Verify texture copy completed before encode call |
| 10-bit not working (Linux+NVIDIA) | Driver limitation | 10-bit NVENC on Linux requires specific driver versions |

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `nvenc-presets.md` | Detailed NVENC preset/tuning combinations, per-codec settings, advanced rate control |
| `amf-config.md` | AMF property reference, HEVC/AV1 differences, preprocessing pipeline, color management |
