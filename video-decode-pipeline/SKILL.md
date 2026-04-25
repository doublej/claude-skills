---
name: video-decode-pipeline
description: "VR headset decode: MediaCodec H.264/H.265/AV1, decode-to-texture, XR2"
---

# Video Decode Pipeline (VR/XR)

<before_writing>

## Before Writing Code

1. **Identify the target**:
   - Headset: Quest 2 (XR2 Gen 1) / Quest 3 (XR2 Gen 2) / Quest 3S / Quest Pro
   - API layer: NDK (`AMediaCodec`) or Java (`MediaCodec`)
   - Rendering API: OpenGL ES 3.x or Vulkan
   - Codec: H.264 / H.265 / AV1

2. **Check existing decoder setup**:
   - How are NALUs received? (network stream, file, shared memory)
   - Surface output or ByteBuffer output?
   - Sync or async dequeue mode?

3. **Read chipset quirks**: `references/chipset-quirks.md`

</before_writing>

<core_rules>

## Core Rules

### API Choice: NDK vs Java

| Factor | NDK (`AMediaCodec`) | Java (`MediaCodec`) |
|--------|---------------------|---------------------|
| Latency | Lower (no JNI overhead per call) | Slightly higher |
| Thread control | Full native thread management | Callback on Looper thread |
| Surface interop | `ANativeWindow` from `ASurfaceTexture` | `Surface` from `SurfaceTexture` |
| Vulkan path | Direct `AHardwareBuffer` access | Requires JNI to get `HardwareBuffer` |
| API surface | Smaller, stable C API | Richer (more format keys, better docs) |
| Error info | Less descriptive error codes | Richer exceptions |

**Rule**: Use NDK for C/C++ VR engines. Use Java only if the app is primarily Java/Kotlin or needs format keys unavailable in NDK.

### Decoder Lifecycle

```
create -> configure(format, surface, flags=0) -> start -> [feed/drain loop] -> stop -> delete
```

Every decoder MUST follow this sequence. Skipping `stop` before `delete` leaks hardware resources and may prevent future decoder creation (only 1-2 HW decoder instances available).

### Surface Output is Mandatory

Never use ByteBuffer output for VR decode. Surface output:
- Enables zero-copy GPU texture path
- Avoids CPU-side YUV-to-RGB conversion
- Is the only path that meets VR frame timing

### Low-Latency Configuration

```c
// NDK
AMediaFormat_setInt32(format, "low-latency", 1);          // Android 11+
AMediaFormat_setInt32(format, "vendor.low-latency.enable", 1); // Qualcomm pre-11

// Java
format.setInteger(MediaFormat.KEY_LOW_LATENCY, 1);         // Android 11+
format.setFeature(MediaCodecInfo.CodecCapabilities.FEATURE_LowLatency, true);
```

On XR2 devices, also look for dedicated low-latency decoder names:
- `c2.qti.hevc.decoder.low_latency`
- `c2.qti.avc.decoder.low_latency`

These are separate codec instances that always operate in low-latency mode.

</core_rules>

<csd>

## Codec-Specific Data (CSD)

CSD buffers contain parameter sets the decoder needs before it can decode frames.

| Codec | CSD-0 | CSD-1 |
|-------|-------|-------|
| H.264 | SPS (with start code `00 00 00 01 67`) | PPS (with start code `00 00 00 01 68`) |
| H.265 | VPS+SPS+PPS concatenated (each with start code) | -- |
| AV1 | OBU sequence header | -- |

### CSD Submission Methods

**Method 1: In MediaFormat (preferred)**
```c
AMediaFormat_setBuffer(format, "csd-0", sps_data, sps_size);
AMediaFormat_setBuffer(format, "csd-1", pps_data, pps_size);
// configure() will submit CSD automatically on start()
```

**Method 2: As flagged input buffers**
```c
// After start(), submit CSD as first buffer(s)
AMediaCodec_queueInputBuffer(codec, idx, 0, csd_size,
    timestamp, AMEDIACODEC_BUFFER_FLAG_CODEC_CONFIG);
```

**Pitfall**: Do NOT submit CSD both ways. If CSD is in the format, do not also queue it as a flagged buffer -- the decoder will see it twice and may produce garbage frames or stall.

**Pitfall**: Every NAL unit in CSD must start with the 4-byte start code `\x00\x00\x00\x01`. Missing start codes cause silent decoder misconfiguration.

</csd>

<feed_drain>

## Feed/Drain Loop

### Async Mode (Recommended for VR)

```c
AMediaCodecOnAsyncNotifyCallback cb = {
    .onAsyncInputAvailable  = on_input_available,
    .onAsyncOutputAvailable = on_output_available,
    .onAsyncFormatChanged   = on_format_changed,
    .onAsyncError           = on_error,
};
AMediaCodec_setAsyncNotifyCallback(codec, cb, userdata);
```

Async mode avoids blocking `dequeueInputBuffer`/`dequeueOutputBuffer` polls. Callbacks fire on a dedicated codec thread.

**Critical**: Once async callbacks are set, do NOT call `dequeueInputBuffer` or `dequeueOutputBuffer`. Mixing sync and async is undefined behavior.

### Sync Mode (Simpler, Higher Latency)

```c
// Feed
ssize_t idx = AMediaCodec_dequeueInputBuffer(codec, timeout_us);
if (idx >= 0) {
    uint8_t *buf;
    size_t buf_size;
    buf = AMediaCodec_getInputBuffer(codec, idx, &buf_size);
    memcpy(buf, nalu_data, nalu_size);
    AMediaCodec_queueInputBuffer(codec, idx, 0, nalu_size, pts_us, 0);
}

// Drain
AMediaCodecBufferInfo info;
ssize_t out = AMediaCodec_dequeueOutputBuffer(codec, &info, timeout_us);
if (out >= 0) {
    // For surface output, render=true releases buffer to surface
    AMediaCodec_releaseOutputBuffer(codec, out, true);
}
```

**Timeout**: Use `0` for non-blocking poll in render loops. Use `10000` (10ms) if you can afford to block.

</feed_drain>

<decode_texture>

## Decode-to-Texture Pipeline

### OpenGL ES Path (Standard)

```
MediaCodec -> Surface(SurfaceTexture) -> GL_TEXTURE_EXTERNAL_OES -> shader sample
```

1. Create GL external texture and `SurfaceTexture`
2. Create `Surface` from `SurfaceTexture`, pass to `configure()`
3. On output available: `releaseOutputBuffer(idx, render=true)`
4. `SurfaceTexture.updateTexImage()` latches the frame
5. `SurfaceTexture.getTransformMatrix()` -- apply in shader (handles Y-flip, crop)

```glsl
#extension GL_OES_EGL_image_external : require
uniform samplerExternalOES uTexture;
uniform mat4 uTexTransform;

void main() {
    vec2 tc = (uTexTransform * vec4(vTexCoord, 0.0, 1.0)).xy;
    gl_FragColor = texture2D(uTexture, tc);
}
```

**Pitfall**: You MUST use `samplerExternalOES`, not `sampler2D`. External textures have different sampling rules. Forgetting this produces black frames with no error.

**Pitfall**: Always apply the transform matrix. It changes per-frame on some devices (rotation, Y-flip, non-trivial crop).

### Vulkan Path (Zero-Copy)

```
MediaCodec -> ImageReader(HARDWARE) -> AImage -> AHardwareBuffer -> VkImage (external memory import)
```

See `references/mediacodec-config.md` for the full Vulkan import sequence.

Key requirements:
- `VK_ANDROID_external_memory_android_hardware_buffer` extension
- `VK_KHR_sampler_ycbcr_conversion` for NV12/NV21 formats
- YCbCr conversion sampler must match the source format (typically BT.709 + 4:2:0)

**XR2 quirk**: Decoded frames use `OMX_QCOM_COLOR_FormatYUV420PackedSemiPlanar32m` internally, which maps to NV12 with vendor-specific stride alignment. The Vulkan driver handles this transparently when importing via `AHardwareBuffer`, but manual stride calculations will be wrong.

</decode_texture>

<timestamp>

## Timestamp Management

- Timestamps are in microseconds (`int64_t`)
- Use monotonically increasing values -- decoders use them for frame reordering
- For streaming: use sender timestamps, not local wall clock
- For low-latency: PTS order = decode order (no B-frames), so reordering is a no-op

**Frame pacing**: Release output buffers at the intended display time using `AMediaCodec_releaseOutputBufferAtTime(codec, idx, display_time_ns)` for smooth playback. For VR, you typically want immediate release + compositor-side pacing.

</timestamp>

<error_recovery>

## Error Recovery

### Decoder Stall (No Output)

Common causes:
1. **Missing reference frames** -- decoder waits for frames it will never get. Fix: send an IDR/keyframe.
2. **CSD never sent** -- decoder accepted input but cannot produce output. Fix: reconfigure with CSD.
3. **Input buffer exhaustion** -- all input buffers queued, none returned. Fix: drain output buffers first.
4. **Corrupt NALU broke internal state** -- decoder is confused. Fix: flush or reset.

### Recovery Strategies

| Strategy | When | Cost |
|----------|------|------|
| `flush()` | Recoverable errors, seek | ~5-20ms, preserves codec instance |
| `stop()` + `configure()` + `start()` | Format change (resolution, codec) | ~50-100ms |
| `reset()` | Unrecoverable error | ~100-200ms, re-creates internal state |
| Delete + create new | Codec completely broken | ~200-500ms, last resort |

```c
// Flush: fast recovery, resubmit CSD after flush
AMediaCodec_flush(codec);
// Must resubmit CSD (SPS/PPS) as first buffers after flush

// Reset: heavier, but recovers from more error states
AMediaCodec_stop(codec);
// Reconfigure with format + surface
AMediaCodec_configure(codec, format, window, NULL, 0);
AMediaCodec_start(codec);
```

**Pitfall**: After `flush()`, you MUST resubmit CSD before sending regular frames. The decoder discards its parameter set state on flush. Failing to do this produces green/corrupt frames.

**Pitfall**: On XR2 Gen 1, `flush()` occasionally fails silently -- output callbacks stop firing. If no output arrives within 100ms after flush + CSD + IDR, escalate to `stop()/configure()/start()`.

</error_recovery>

<don_ts>

## What NOT to Do

- Use ByteBuffer output mode (CPU copy kills frame timing)
- Mix sync and async dequeue APIs on the same codec
- Submit CSD both in format AND as flagged buffers
- Call `dequeueOutputBuffer` with long timeouts in the render thread
- Assume decoder state survives `flush()` -- always resubmit CSD
- Create more than 2 HW decoder instances (will fail silently or crash)
- Use `BUFFER_FLAG_END_OF_STREAM` for streaming (it's for finite playback only)

</don_ts>

<troubleshooting>

## Troubleshooting

| Symptom | Likely Cause |
|---------|--------------|
| Black frames | Wrong texture type (`sampler2D` instead of `samplerExternalOES`) |
| Green/corrupt first frames | CSD not submitted or submitted incorrectly |
| Decoder stall (no output) | Missing IDR, reference frame gap, or input exhaustion |
| High decode latency (>15ms) | Low-latency flag not set, B-frames in stream |
| Crash on second decoder create | Previous decoder not properly stopped/deleted |
| Color shift / wrong colors | YCbCr conversion mismatch (BT.601 vs BT.709) |
| Stretched/cropped output | Not applying SurfaceTexture transform matrix |
| Output callbacks stop firing | XR2 Gen 1 flush bug -- escalate to stop/configure/start |
| `configure()` returns error | Unsupported resolution/profile, or CSD malformed |
| Intermittent frame drops | Async output not released fast enough, back-pressure |

</troubleshooting>

<deep_reference>

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `mediacodec-config.md` | Full configure() parameters, format keys, Vulkan import sequence |
| `chipset-quirks.md` | Per-headset decoder limits, known bugs, workarounds |

</deep_reference>
