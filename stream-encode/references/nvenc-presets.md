# NVENC Detailed Reference

## Preset x Tuning Behavior

When you call `CreateDefaultEncoderParams` with a preset+tuning combo, the SDK auto-sets:

| Parameter | Low Latency | Ultra Low Latency |
|-----------|-------------|-------------------|
| `lookaheadDepth` | 0 | 0 |
| `enableLookahead` | 0 | 0 |
| B-frames | 0 | 0 |
| `zeroReorderDelay` | 1 | 1 |
| `lowDelayKeyFrameScale` | 1 | 1 |
| Multi-pass | Preset-dependent | Disabled |
| AQ | Preset-dependent | Disabled |

**Do not re-enable lookahead or B-frames for VR** -- they add frame-level latency.

## Preset Performance Characteristics

Measured on typical VR resolutions (2x 1832x1920 eye buffers):

| Preset | Typical encode time (90Hz budget = 11ms) | Notes |
|--------|-------------------------------------------|-------|
| P1 | 1-3ms | Always safe |
| P2 | 2-4ms | Safe on most GPUs |
| P3 | 3-5ms | May cause drops at 120Hz |
| P4 | 4-7ms | Borderline at 90Hz on slower NVENC |
| P5 | 6-10ms | Only with dedicated NVENC headroom |
| P6-P7 | 10-20ms+ | Not viable for real-time VR |

These are approximate -- actual times depend on GPU generation, resolution, and scene complexity.

## Advanced Rate Control Parameters

### VBV (Video Buffering Verifier)

```cpp
// Tight buffer for minimum latency (1 frame)
uint32_t frameSize = bitrate_bps / framerate;
rcParams.vbvBufferSize = frameSize * 1.1;
rcParams.vbvInitialDelay = frameSize * 1.1;

// Looser buffer for better quality (2-3 frames)
rcParams.vbvBufferSize = frameSize * 2.5;
rcParams.vbvInitialDelay = frameSize * 2.5;
```

**For VR**: use tight (1x-1.5x). Larger buffers allow the encoder to "borrow" bits from future frames, adding latency.

### Low Delay Key Frame Scale

Controls how much larger an IDR can be relative to normal frames:

```cpp
rcParams.lowDelayKeyFrameScale = 1;  // IDR same size as P-frame (tight)
// Higher values allow larger IDRs but cause bitrate spikes
```

### Multi-Pass Modes

```cpp
// No multi-pass (fastest)
rcParams.multiPass = NV_ENC_MULTI_PASS_DISABLED;

// Quarter resolution first pass (recommended for VR quality boost)
rcParams.multiPass = NV_ENC_TWO_PASS_QUARTER_RESOLUTION;

// Full resolution first pass (highest quality, more latency)
rcParams.multiPass = NV_ENC_TWO_PASS_FULL_RESOLUTION;
```

Quarter-resolution multi-pass is the sweet spot for VR: ~5% quality improvement with minimal latency cost.

## Intra Refresh Deep Dive

Intra refresh replaces periodic IDR frames with a rolling wave of intra-coded macroblocks:

```cpp
// H.264
h264Config.enableIntraRefresh = 1;
h264Config.intraRefreshPeriod = 60;  // start new wave every 60 frames
h264Config.intraRefreshCnt = 5;      // wave spans 5 frames

// Same API for HEVC and AV1
hevcConfig.enableIntraRefresh = 1;
// ...
```

**How it works**: over `intraRefreshCnt` frames, a vertical band of intra-coded macroblocks sweeps across the frame. After `intraRefreshPeriod` frames, a new wave starts.

**VR trade-offs**:
- Pro: No bitrate spikes (IDRs can be 5-10x larger than P-frames)
- Pro: Smoother frame delivery timing
- Con: Error recovery takes `intraRefreshCnt` frames instead of 1 IDR
- Con: May not work with all decoders (Android MediaCodec generally supports it)

**Recommendation**: Keep disabled by default. Enable only if IDR-induced bitrate spikes cause network congestion. If enabled, set `intraRefreshPeriod` to ~60 and `intraRefreshCnt` to ~5.

## Reference Frame Configuration

```cpp
// Default: let SDK decide (usually 1-2 for low latency)
config.maxNumRefFrames = 0;

// Single reference frame (minimum latency, minimum quality)
config.maxNumRefFrames = 1;

// For reference frame invalidation (RFI)
config.maxNumRefFrames = 16;  // SDK recommended for RFI
// WARNING: RFI with maxNumRefFrames=16 can degrade visual quality
```

**Reference Frame Invalidation (RFI)**: Alternative to IDR for error recovery. Instead of sending a full IDR, invalidate the corrupted reference and let the encoder avoid referencing it. Requires client-side feedback (which frames were lost). ALVR does not currently use RFI; it uses IDR-on-loss.

## Weighted Prediction

```cpp
initParams.enableWeightedPrediction = true;
```

Can improve quality for scenes with fading/dissolves. Minimal impact on typical VR content. ALVR exposes this but defaults to disabled.

## 10-Bit Encoding

```cpp
// Buffer format
NV_ENC_BUFFER_FORMAT_YUV420_10BIT  // for NV12 input
NV_ENC_BUFFER_FORMAT_ABGR10        // for RGB input

// HEVC: signal 10-bit
hevcConfig.pixelBitDepthMinus8 = 2;

// AV1: signal 10-bit
av1Config.pixelBitDepthMinus8 = 2;
// H.264 does NOT support 10-bit in NVENC
```

**Limitation**: NVENC on Linux does not reliably support 10-bit in all driver versions.

## AV1-Specific Notes

NVENC's AV1 output includes IVF container headers that must be stripped for raw OBU streaming:

```cpp
// Strip IVF file header (32 bytes, appears once at start)
const uint8_t ivf_magic[4] = { 0x44, 0x4B, 0x49, 0x46 }; // "DKIF"
if (len >= 4 && !memcmp(buf, ivf_magic, 4)) {
    buf += 32;
    len -= 32;
}
// Strip IVF frame header (12 bytes per frame)
buf += 12;
len -= 12;
```

AV1 requires Ada Lovelace (RTX 40 series) or newer.

## Error Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| `NV_ENC_ERR_OUT_OF_MEMORY` | Session limit or VRAM | Too many sessions or huge resolution |
| `NV_ENC_ERR_INVALID_PARAM` | Bad config combination | Codec not supported on this GPU (e.g., HEVC on old GPU) |
| `NV_ENC_ERR_ENCODER_BUSY` | Encode not finished | Submitting faster than encoder can process |
| `NV_ENC_ERR_NEED_MORE_INPUT` | Async mode, keep feeding | Normal in async -- not an error |
| `NV_ENC_ERR_UNSUPPORTED_DEVICE` | GPU too old | Check `NvEncGetEncodeGUIDs` for supported codecs |

## Hardware Generations

| Generation | Chip | NVENC Engines | AV1 Encode | Notable |
|------------|------|---------------|------------|---------|
| Turing | TU1xx | 1 | No | First to support B-frame on NVENC |
| Ampere | GA1xx | 1 | No | Improved quality at same preset |
| Ada Lovelace | AD1xx | 2-3 | Yes | Split-frame encoding, AV1 support |
| Blackwell | GB2xx | 2-3 | Yes | Further quality improvements |

## Async Encoding Pattern

For maximum throughput, separate encode submission from output collection:

```cpp
// Thread 1: Submit frames
const NvEncInputFrame* frame = encoder->GetNextInputFrame();
// copy texture to frame
encoder->EncodeFrame(packets, &picParams);

// Thread 2: Collect output (async mode only)
// Wait on event object associated with output buffer
// Copy bitstream when signaled
```

For VR, synchronous single-threaded encode is simpler and sufficient -- NVENC latency is predictable. Only use async if you need to overlap encode with other GPU work.
