# MediaCodec Configuration Reference

## Format Keys for Decode

### Required

```c
AMediaFormat *format = AMediaFormat_new();
AMediaFormat_setString(format, AMEDIAFORMAT_KEY_MIME, "video/hevc");  // or "video/avc", "video/av01"
AMediaFormat_setInt32(format, AMEDIAFORMAT_KEY_WIDTH, 2064);
AMediaFormat_setInt32(format, AMEDIAFORMAT_KEY_HEIGHT, 2208);
```

### Low-Latency Keys

```c
// Standard (Android 11+ / API 30)
AMediaFormat_setInt32(format, "low-latency", 1);

// Qualcomm vendor extension (pre-Android 11, still works on newer)
AMediaFormat_setInt32(format, "vendor.low-latency.enable", 1);

// Disable frame reordering (for streams without B-frames)
AMediaFormat_setInt32(format, "vendor.qti-ext-dec-low-latency.enable", 1);
```

### Optional Tuning Keys

| Key | Type | Purpose |
|-----|------|---------|
| `max-input-size` | int32 | Max input buffer size. Set to max NALU size to avoid reallocation |
| `priority` | int32 | 0 = realtime, 1 = best-effort. Use 0 for VR |
| `operating-rate` | int32 | Target FPS. Set to 90 or 120 for VR frame rates |
| `max-width` / `max-height` | int32 | Adaptive playback: max resolution without reconfigure |

```c
AMediaFormat_setInt32(format, AMEDIAFORMAT_KEY_PRIORITY, 0);
AMediaFormat_setInt32(format, AMEDIAFORMAT_KEY_OPERATING_RATE, 90);
AMediaFormat_setInt32(format, "max-input-size", 512 * 1024);  // 512KB
```

## Codec Selection

### Finding Decoders

```java
// Java - find all decoders for a MIME type
MediaCodecList list = new MediaCodecList(MediaCodecList.ALL_CODECS);
for (MediaCodecInfo info : list.getCodecInfos()) {
    if (info.isEncoder()) continue;
    for (String type : info.getSupportedTypes()) {
        if (type.equalsIgnoreCase("video/hevc")) {
            // Check capabilities
            MediaCodecInfo.CodecCapabilities caps = info.getCapabilitiesForType(type);
            boolean lowLatency = caps.isFeatureSupported(
                MediaCodecInfo.CodecCapabilities.FEATURE_LowLatency);
            Log.d("Codec", info.getName() + " lowLatency=" + lowLatency);
        }
    }
}
```

### Preferred Decoder Names (Qualcomm XR2)

| Decoder | Codec | Notes |
|---------|-------|-------|
| `c2.qti.avc.decoder` | H.264 | Standard HW decoder |
| `c2.qti.avc.decoder.low_latency` | H.264 | Dedicated low-latency instance |
| `c2.qti.hevc.decoder` | H.265 | Standard HW decoder |
| `c2.qti.hevc.decoder.low_latency` | H.265 | Dedicated low-latency instance |
| `c2.qti.av1.decoder` | AV1 | XR2 Gen 2 only |

Prefer low-latency variants when available. Fall back to standard + `KEY_LOW_LATENCY` flag.

```c
// NDK - create by name
AMediaCodec *codec = AMediaCodec_createCodecByName("c2.qti.hevc.decoder.low_latency");
if (!codec) {
    // Fallback to generic
    codec = AMediaCodec_createDecoderByType("video/hevc");
}
```

## H.264 Profile/Level Negotiation

Common VR streaming profiles:

| Profile | Level | Max Resolution | Max Bitrate | Notes |
|---------|-------|----------------|-------------|-------|
| High | 5.1 | 4096x2304 @ 30 | 50 Mbps | Quest 2 typical |
| High | 5.2 | 4096x2304 @ 60 | 240 Mbps | Quest 3 typical |

For H.265:

| Profile | Level | Max Resolution | Notes |
|---------|-------|----------------|-------|
| Main | 5.1 | 4096x2160 @ 60 | Standard VR streaming |
| Main 10 | 5.1 | 4096x2160 @ 60 | 10-bit HDR content |

## CSD Format Reference

### H.264 CSD Construction

```c
// CSD-0: SPS
// Start code (4 bytes) + NAL header (1 byte, type 0x67) + SPS data
uint8_t csd0[] = {0x00, 0x00, 0x00, 0x01, 0x67, /* SPS bytes... */};

// CSD-1: PPS
// Start code (4 bytes) + NAL header (1 byte, type 0x68) + PPS data
uint8_t csd1[] = {0x00, 0x00, 0x00, 0x01, 0x68, /* PPS bytes... */};
```

### H.265 CSD Construction

```c
// CSD-0: VPS + SPS + PPS concatenated, each with start code
uint8_t csd0[] = {
    0x00, 0x00, 0x00, 0x01, 0x40, 0x01, /* VPS bytes... */
    0x00, 0x00, 0x00, 0x01, 0x42, 0x01, /* SPS bytes... */
    0x00, 0x00, 0x00, 0x01, 0x44, 0x01, /* PPS bytes... */
};
// No CSD-1 for H.265
```

### NAL Unit Type Quick Reference

| Codec | NAL Type | Byte (after start code) | Purpose |
|-------|----------|------------------------|---------|
| H.264 | SPS | `0x67` | Sequence parameters |
| H.264 | PPS | `0x68` | Picture parameters |
| H.264 | IDR | `0x65` | Keyframe |
| H.264 | Non-IDR | `0x61` | P-frame |
| H.265 | VPS | `0x40` (type 32) | Video parameters |
| H.265 | SPS | `0x42` (type 33) | Sequence parameters |
| H.265 | PPS | `0x44` (type 34) | Picture parameters |
| H.265 | IDR_W_RADL | `0x26` (type 19) | Keyframe |
| H.265 | TRAIL_R | `0x02` (type 1) | P-frame |

H.265 NAL type is in bits 1-6 of the first byte after start code: `(byte >> 1) & 0x3F`.

## Vulkan Import Sequence (AHardwareBuffer)

Full zero-copy pipeline for decoded frames:

```c
// 1. Create ImageReader with HARDWARE format
AImageReader *reader;
AImageReader_newWithUsage(width, height,
    AIMAGE_FORMAT_PRIVATE,           // decoder chooses internal format
    AHARDWAREBUFFER_USAGE_GPU_SAMPLED_IMAGE,
    max_images,                       // typically 3-5
    &reader);

// 2. Get ANativeWindow from ImageReader, use as decode surface
ANativeWindow *window;
AImageReader_getWindow(reader, &window);
AMediaCodec_configure(codec, format, window, NULL, 0);

// 3. On frame available, acquire AImage -> AHardwareBuffer
AImage *image;
AImageReader_acquireLatestImage(reader, &image);

AHardwareBuffer *hwbuf;
AImage_getHardwareBuffer(image, &hwbuf);

// 4. Import into Vulkan
AHardwareBuffer_Desc desc;
AHardwareBuffer_describe(hwbuf, &desc);

VkAndroidHardwareBufferFormatPropertiesANDROID fmtProps = {
    .sType = VK_STRUCTURE_TYPE_ANDROID_HARDWARE_BUFFER_FORMAT_PROPERTIES_ANDROID
};
VkAndroidHardwareBufferPropertiesANDROID hwbufProps = {
    .sType = VK_STRUCTURE_TYPE_ANDROID_HARDWARE_BUFFER_PROPERTIES_ANDROID,
    .pNext = &fmtProps
};
vkGetAndroidHardwareBufferPropertiesANDROID(device, hwbuf, &hwbufProps);

// 5. Create VkImage with external memory
VkExternalMemoryImageCreateInfo extMemInfo = {
    .sType = VK_STRUCTURE_TYPE_EXTERNAL_MEMORY_IMAGE_CREATE_INFO,
    .handleTypes = VK_EXTERNAL_MEMORY_HANDLE_TYPE_ANDROID_HARDWARE_BUFFER_BIT_ANDROID
};

VkImageCreateInfo imageInfo = {
    .sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO,
    .pNext = &extMemInfo,
    .imageType = VK_IMAGE_TYPE_2D,
    .format = fmtProps.format,  // may be VK_FORMAT_UNDEFINED for vendor YUV
    .extent = {desc.width, desc.height, 1},
    .mipLevels = 1,
    .arrayLayers = 1,
    .samples = VK_SAMPLE_COUNT_1_BIT,
    .tiling = VK_IMAGE_TILING_OPTIMAL,
    .usage = VK_IMAGE_USAGE_SAMPLED_BIT,
};
vkCreateImage(device, &imageInfo, NULL, &vkImage);

// 6. Import memory
VkImportAndroidHardwareBufferInfoANDROID importInfo = {
    .sType = VK_STRUCTURE_TYPE_IMPORT_ANDROID_HARDWARE_BUFFER_INFO_ANDROID,
    .buffer = hwbuf
};
VkMemoryAllocateInfo allocInfo = {
    .sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,
    .pNext = &importInfo,
    .allocationSize = hwbufProps.allocationSize,
    .memoryTypeIndex = /* find compatible type from hwbufProps.memoryTypeBits */
};
vkAllocateMemory(device, &allocInfo, NULL, &memory);
vkBindImageMemory(device, vkImage, memory, 0);

// 7. Create YCbCr conversion sampler (for NV12 decoded output)
VkSamplerYcbcrConversionCreateInfo ycbcrInfo = {
    .sType = VK_STRUCTURE_TYPE_SAMPLER_YCBCR_CONVERSION_CREATE_INFO,
    .pNext = &fmtProps.externalFormat ? &extFormatInfo : NULL,
    .format = fmtProps.format,
    .ycbcrModel = VK_SAMPLER_YCBCR_MODEL_CONVERSION_YCBCR_709,  // BT.709
    .ycbcrRange = VK_SAMPLER_YCBCR_RANGE_ITU_NARROW,
    .chromaFilter = VK_FILTER_LINEAR,
};
```

## Color Format Notes

| Device | Internal Format | Equivalent |
|--------|----------------|------------|
| Quest 2 (XR2 Gen 1) | `OMX_QCOM_COLOR_FormatYUV420PackedSemiPlanar32m` | NV12 + 32-byte aligned stride |
| Quest 3 (XR2 Gen 2) | `OMX_QCOM_COLOR_FormatYUV420PackedSemiPlanar32m` | NV12 + 32-byte aligned stride |

When using Surface/SurfaceTexture output, the color format is handled transparently. Only relevant when using ByteBuffer output (not recommended) or manual `AHardwareBuffer` inspection.

## Complete NDK Decoder Setup (Minimal)

```c
#include <media/NdkMediaCodec.h>
#include <media/NdkMediaFormat.h>
#include <android/native_window.h>

typedef struct {
    AMediaCodec *codec;
    AMediaFormat *format;
    ANativeWindow *surface;
    bool started;
} VrDecoder;

bool vr_decoder_init(VrDecoder *dec, const char *mime,
                     int width, int height,
                     ANativeWindow *surface,
                     const uint8_t *csd0, size_t csd0_size,
                     const uint8_t *csd1, size_t csd1_size) {
    // Try low-latency decoder first
    const char *ll_name = strcmp(mime, "video/hevc") == 0
        ? "c2.qti.hevc.decoder.low_latency"
        : "c2.qti.avc.decoder.low_latency";

    dec->codec = AMediaCodec_createCodecByName(ll_name);
    if (!dec->codec) {
        dec->codec = AMediaCodec_createDecoderByType(mime);
    }
    if (!dec->codec) return false;

    dec->format = AMediaFormat_new();
    AMediaFormat_setString(dec->format, AMEDIAFORMAT_KEY_MIME, mime);
    AMediaFormat_setInt32(dec->format, AMEDIAFORMAT_KEY_WIDTH, width);
    AMediaFormat_setInt32(dec->format, AMEDIAFORMAT_KEY_HEIGHT, height);
    AMediaFormat_setInt32(dec->format, AMEDIAFORMAT_KEY_PRIORITY, 0);
    AMediaFormat_setInt32(dec->format, AMEDIAFORMAT_KEY_OPERATING_RATE, 90);
    AMediaFormat_setInt32(dec->format, "low-latency", 1);

    if (csd0 && csd0_size > 0)
        AMediaFormat_setBuffer(dec->format, "csd-0", csd0, csd0_size);
    if (csd1 && csd1_size > 0)
        AMediaFormat_setBuffer(dec->format, "csd-1", csd1, csd1_size);

    dec->surface = surface;
    ANativeWindow_acquire(surface);

    media_status_t status = AMediaCodec_configure(
        dec->codec, dec->format, surface, NULL, 0);
    if (status != AMEDIA_OK) return false;

    status = AMediaCodec_start(dec->codec);
    if (status != AMEDIA_OK) return false;

    dec->started = true;
    return true;
}

void vr_decoder_destroy(VrDecoder *dec) {
    if (dec->started) AMediaCodec_stop(dec->codec);
    if (dec->codec) AMediaCodec_delete(dec->codec);
    if (dec->format) AMediaFormat_delete(dec->format);
    if (dec->surface) ANativeWindow_release(dec->surface);
}
```
