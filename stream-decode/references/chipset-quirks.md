# Chipset Quirks & Per-Headset Decoder Details

## Headset / Chipset Matrix

| Headset | Chipset | GPU | Android | Max HW Decoders |
|---------|---------|-----|---------|-----------------|
| Quest 2 | XR2 Gen 1 (SM8250) | Adreno 650 | 10 (API 29) -> 12 | 2 |
| Quest Pro | XR2 Gen 1 (SM8250) | Adreno 650 | 12 | 2 |
| Quest 3 | XR2 Gen 2 (SM8550-AB) | Adreno 740 | 12 (API 32) | 2 |
| Quest 3S | XR2 Gen 2 (SM8550-AB) | Adreno 740 | 12 | 2 |
| Pico 4 | XR2 Gen 1 (SM8250) | Adreno 650 | 10 | 2 |

## Codec Support Per Chipset

### XR2 Gen 1 (Quest 2, Pico 4)

| Codec | Max Resolution | Max Bitrate | Profiles |
|-------|---------------|-------------|----------|
| H.264 | 4096x2304 | 240 Mbps | Baseline, Main, High (up to 5.2) |
| H.265 | 4096x2160 | 240 Mbps | Main, Main 10 (up to 5.1) |
| AV1 | Not supported | -- | -- |

### XR2 Gen 2 (Quest 3, Quest 3S)

| Codec | Max Resolution | Max Bitrate | Profiles |
|-------|---------------|-------------|----------|
| H.264 | 4096x2304 | 240 Mbps | Baseline, Main, High (up to 5.2) |
| H.265 | 8192x4320 | 500 Mbps | Main, Main 10 (up to 6.1) |
| AV1 | 4096x2176 | 500 Mbps | Main (level 5.1) |

## Known Bugs & Workarounds

### XR2 Gen 1 (Quest 2)

**1. flush() silently kills output callbacks**
- After `AMediaCodec_flush()`, async output callbacks may stop firing entirely
- Workaround: if no output within 100ms after flush + CSD resubmit + IDR, do full `stop()/configure()/start()` cycle
- Frequency: intermittent, ~5% of flush operations

**2. Decoder stall on rapid resolution changes**
- Switching resolution (e.g., 2064x2208 -> 1832x1920) during streaming without full reconfigure causes indefinite stall
- Workaround: always do `stop()/configure()/start()` for resolution changes, never rely on adaptive playback

**3. First frame delay after configure**
- First decoded frame takes 30-80ms longer than steady-state
- Workaround: pre-warm decoder by submitting CSD + one IDR during initialization, before the user sees output

**4. SurfaceTexture.updateTexImage() race**
- Calling `updateTexImage()` from a thread different than the GL context owner causes silent corruption
- Workaround: always call from the GL thread, or use `attachToGLContext()`/`detachFromGLContext()` for thread migration

### XR2 Gen 2 (Quest 3)

**1. AV1 decoder limited instance count**
- Only 1 AV1 HW decoder instance available (vs 2 for H.264/H.265)
- Creating a second AV1 decoder returns `AMEDIA_ERROR_INSUFFICIENT_RESOURCE`
- Workaround: use H.265 if dual-decoder is needed (e.g., left+right eye separate streams)

**2. H.265 Main 10 HDR metadata handling**
- HDR static metadata in SEI NALUs is sometimes ignored
- Workaround: pass HDR metadata explicitly via `MediaFormat` keys:
  ```c
  AMediaFormat_setInt32(format, "color-transfer", 7);  // HLG
  AMediaFormat_setInt32(format, "color-standard", 9);   // BT.2020
  ```

**3. Operating rate hint threshold**
- Setting `AMEDIAFORMAT_KEY_OPERATING_RATE` above 120 causes the decoder to silently cap at 90 FPS output
- Workaround: set to exactly 90 or 120, matching actual target refresh rate

**4. Low-latency decoder name changed in firmware v62+**
- Pre-v62: `c2.qti.hevc.decoder.low_latency`
- v62+: same name but different internal behavior (uses Codec2 instead of OMX)
- Impact: timing characteristics changed slightly (1-2ms faster decode, but 3-5ms longer configure)
- No code change needed, just be aware of benchmark differences across firmware versions

### Both Chipsets

**1. Max input buffer size underestimation**
- Default `max-input-size` may be too small for high-bitrate 4K streams
- Symptom: `queueInputBuffer` silently truncates data, producing artifacts
- Workaround: explicitly set `max-input-size` to at least 512KB for VR streams:
  ```c
  AMediaFormat_setInt32(format, "max-input-size", 512 * 1024);
  ```

**2. Timestamp discontinuity crash**
- Submitting a timestamp that jumps backward by more than ~2 seconds (on some firmware) causes a decoder crash
- Workaround: maintain a monotonic timestamp counter; if source timestamps jump, remap to monotonic sequence

**3. configure() after reset() fails without format**
- `AMediaCodec_reset()` clears internal format. Must pass a complete format to `configure()` again
- Common mistake: caching the old format pointer but forgetting to re-set CSD buffers

**4. Surface released before decoder stop**
- If the `ANativeWindow`/`Surface` is destroyed before `AMediaCodec_stop()`, the decoder may hang or crash in `stop()`
- Workaround: always stop decoder first, then release surface

## Decode Latency Benchmarks (Typical)

Measured from `queueInputBuffer` to `onOutputBufferAvailable` callback, 1080p H.265, 30 Mbps, IDR interval 1s.

| Device | Steady-State P-frame | IDR Frame | First Frame |
|--------|---------------------|-----------|-------------|
| Quest 2 | 3-5ms | 8-12ms | 40-80ms |
| Quest 3 | 2-4ms | 6-10ms | 30-60ms |
| Quest 3 (AV1) | 4-7ms | 10-15ms | 50-90ms |

For eye-buffer resolution (per-eye ~1832x1920):

| Device | Steady-State P-frame | IDR Frame |
|--------|---------------------|-----------|
| Quest 2 | 5-8ms | 12-18ms |
| Quest 3 | 3-5ms | 8-14ms |

These are decode-only times. Total motion-to-photon latency includes network, encode, compositor, and display.

## Debugging Tips

### Dumping Decoder Capabilities

```java
// Run on device to enumerate all decoder details
MediaCodecList list = new MediaCodecList(MediaCodecList.ALL_CODECS);
for (MediaCodecInfo info : list.getCodecInfos()) {
    if (info.isEncoder()) continue;
    Log.d("CODEC", "Name: " + info.getName());
    for (String type : info.getSupportedTypes()) {
        CodecCapabilities caps = info.getCapabilitiesForType(type);
        VideoCapabilities vc = caps.getVideoCapabilities();
        Log.d("CODEC", "  Type: " + type);
        Log.d("CODEC", "  MaxWidth: " + vc.getSupportedWidths());
        Log.d("CODEC", "  MaxHeight: " + vc.getSupportedHeights());
        Log.d("CODEC", "  MaxBitrate: " + vc.getBitrateRange());
        Log.d("CODEC", "  LowLatency: " +
            caps.isFeatureSupported(CodecCapabilities.FEATURE_LowLatency));
    }
}
```

### Logcat Filters for Decoder Debug

```bash
# Codec lifecycle and errors
adb logcat -s MediaCodec:V OMXClient:V CCodec:V

# Qualcomm-specific decoder logs
adb logcat -s C2QtiComp:V QC2Comp:V vendor.qti.video:V

# Surface/texture issues
adb logcat -s SurfaceTexture:V BufferQueue:V GraphicBuffer:V
```

### Checking Active Decoder Instances

```bash
# See how many codec instances are active
adb shell dumpsys media.codec | grep -A5 "active"
```
