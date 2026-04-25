---
name: quest-android-vr-client
description: "Native Quest VR with OpenXR: swapchains, timewarp, foveated, NDK, passthrough"
---

# Quest / Android VR Client

<prerequisites>
## Before Writing Code

1. **Identify the graphics API**: OpenGL ES 3.x or Vulkan
2. **Identify the SDK layer**:
   - Raw OpenXR + Meta extensions (most control)
   - OVRFW XrApp framework (convenience, uses OpenGL ES)
3. **Check SDK version**: Meta OpenXR SDK version in project dependencies
4. **Confirm target devices**: Quest 2 / Quest 3 / Quest 3S -- affects available extensions and perf budgets

## Device Specs

| | Quest 2 | Quest 3 | Quest 3S |
|---|---|---|---|
| SoC | XR2 Gen 1 | XR2 Gen 2 | XR2 Gen 2 |
| GPU | Adreno 650 | Adreno 740 | Adreno 740 |
| RAM | 6 GB | 8 GB | 8 GB |
| Display (per eye) | 1832 x 1920 | 2064 x 2208 | 1832 x 1920 |
| Refresh rates | 72 / 90 / 120 Hz | 72 / 90 / 120 Hz | 72 / 90 / 120 Hz |
| Eye tracking | No | No | No |
| Color passthrough | No | Yes | Yes |
| Pancake lenses | No | Yes | Yes |

Shared memory model: CPU and GPU share the same RAM pool. No dedicated VRAM.
</prerequisites>

<core_rules>
## Core Rules

### Frame Loop Contract (OpenXR)

Every VR frame MUST follow this sequence -- never skip steps:

```
xrWaitFrame        -> get predictedDisplayTime
xrBeginFrame       -> signal start of GPU work
  xrAcquireSwapchainImage
  xrWaitSwapchainImage  -> block until compositor releases image
  [render to swapchain]
  xrReleaseSwapchainImage
xrEndFrame         -> submit composition layers
```

**Critical**: `xrWaitFrame` provides the predicted display time. Use it for all pose queries (`xrLocateSpace`, `xrLocateViews`). Rendering with stale poses causes judder.

### Swapchain Setup

```cpp
// Enumerate recommended formats
uint32_t formatCount;
xrEnumerateSwapchainFormats(session, 0, &formatCount, nullptr);
std::vector<int64_t> formats(formatCount);
xrEnumerateSwapchainFormats(session, formatCount, &formatCount, formats.data());

// Create swapchain -- use texture array for multiview
XrSwapchainCreateInfo sci{XR_TYPE_SWAPCHAIN_CREATE_INFO};
sci.usageFlags = XR_SWAPCHAIN_USAGE_COLOR_ATTACHMENT_BIT | XR_SWAPCHAIN_USAGE_SAMPLED_BIT;
sci.format = GL_SRGB8_ALPHA8;  // or VK_FORMAT_R8G8B8A8_SRGB for Vulkan
sci.sampleCount = 1;
sci.width = viewConfig.recommendedImageRectWidth;
sci.height = viewConfig.recommendedImageRectHeight;
sci.faceCount = 1;
sci.arraySize = 2;  // 2 for multiview stereo (texture array)
sci.mipCount = 1;
xrCreateSwapchain(session, &sci, &swapchain);
```

| Format choice | GLES | Vulkan |
|---|---|---|
| Color (sRGB) | `GL_SRGB8_ALPHA8` | `VK_FORMAT_R8G8B8A8_SRGB` |
| Depth | `GL_DEPTH24_STENCIL8` | `VK_FORMAT_D24_UNORM_S8_UINT` |
| Depth (high precision) | `GL_DEPTH_COMPONENT32F` | `VK_FORMAT_D32_SFLOAT` |

**Triple buffering** is handled by the runtime. The swapchain typically contains 3 images. You acquire/wait/render/release -- the compositor manages pacing.

### Multiview Rendering

Multiview (single-pass stereo) renders both eyes in one draw call using `GL_OVR_multiview2`. The swapchain `arraySize = 2` creates a texture array; layer 0 = left eye, layer 1 = right eye.

```glsl
#version 320 es
#extension GL_OVR_multiview2 : require
layout(num_views = 2) in;

uniform mat4 viewProj[2];

void main() {
    gl_Position = viewProj[gl_ViewID_OVR] * modelMatrix * vec4(position, 1.0);
}
```

**Pitfall**: Not all shader effects work with multiview. View-dependent effects (reflections, specular) must index `gl_ViewID_OVR`. Post-processing that reads from the color buffer needs separate handling.

### Frame Submission

```cpp
XrCompositionLayerProjection layer{XR_TYPE_COMPOSITION_LAYER_PROJECTION};
layer.space = appSpace;
layer.viewCount = 2;
layer.views = projectionViews;  // array of XrCompositionLayerProjectionView

// Each projection view references a slice of the texture array
projectionViews[eye].subImage.swapchain = swapchain;
projectionViews[eye].subImage.imageArrayIndex = eye;  // 0=left, 1=right
projectionViews[eye].subImage.imageRect = {{0, 0}, {width, height}};

const XrCompositionLayerBaseHeader* layers[] = {
    (XrCompositionLayerBaseHeader*)&layer
};

XrFrameEndInfo endInfo{XR_TYPE_FRAME_END_INFO};
endInfo.displayTime = predictedDisplayTime;
endInfo.environmentBlendMode = XR_ENVIRONMENT_BLEND_MODE_OPAQUE;
endInfo.layerCount = 1;
endInfo.layers = layers;
xrEndFrame(session, &endInfo);
```

## Compositor & Reprojection

### Asynchronous TimeWarp (ATW)

Automatic -- no developer action needed. The compositor reprojects the last submitted frame to match the latest head pose, reducing perceived latency. Works by transforming the rendered image based on orientation delta between render time and display time.

**Limitation**: ATW only corrects rotational movement. Translational movement causes positional artifacts (swimming/wobble at close range).

### Application SpaceWarp (AppSW)

Extension: `XR_FB_space_warp`. Synthesizes intermediate frames from motion vectors + depth, halving required render rate (e.g., render at 45fps, display at 90fps).

**Unlike ATW, AppSW requires developer work**:

1. Enable the extension at instance creation
2. Create motion vector + depth swapchains
3. Render motion vectors each frame (screen-space velocity per pixel)
4. Submit via `XrCompositionLayerSpaceWarpInfoFB` chained to projection views

```cpp
// Query recommended motion vector dimensions
XrSystemSpaceWarpPropertiesFB swProps{XR_TYPE_SYSTEM_SPACE_WARP_PROPERTIES_FB};
// ... chain to system properties query

// Create motion vector swapchain
XrSwapchainCreateInfo mvSci{XR_TYPE_SWAPCHAIN_CREATE_INFO};
mvSci.format = GL_RGBA16F;  // motion vectors need float precision
mvSci.width = swProps.recommendedMotionVectorImageRectWidth;
mvSci.height = swProps.recommendedMotionVectorImageRectHeight;
mvSci.arraySize = 2;
```

**When to use AppSW**: GPU-bound scenes that cannot hit target framerate. Trades visual quality (extrapolation artifacts on fast-moving objects) for framerate.

**When NOT to use**: Scenes with many thin/transparent objects, particle effects, or UI text -- these produce poor motion vectors.

## Foveated Rendering

### Fixed Foveated Rendering (FFR)

Extension: `XR_FB_foveation` + `XR_FB_foveation_configuration`. Renders peripheral vision at lower resolution. Enabled by default on Quest runtime.

```cpp
// Create foveation profile
XrFoveationProfileCreateInfoFB profileInfo{XR_TYPE_FOVEATION_PROFILE_CREATE_INFO_FB};

XrFoveationLevelProfileCreateInfoFB levelInfo{
    XR_TYPE_FOVEATION_LEVEL_PROFILE_CREATE_INFO_FB};
levelInfo.level = XR_FOVEATION_LEVEL_HIGH_FB;  // None, Low, Medium, High, HighTop
levelInfo.verticalOffset = 0.0f;
levelInfo.dynamic = XR_FOVEATION_DYNAMIC_LEVEL_ENABLED_FB;  // auto-adjust based on GPU load

profileInfo.next = &levelInfo;

XrFoveationProfileFB profile;
xrCreateFoveationProfileFB(session, &profileInfo, &profile);

// Apply to swapchain
XrSwapchainStateFoveationFB foveationState{XR_TYPE_SWAPCHAIN_STATE_FOVEATION_FB};
foveationState.profile = profile;
xrUpdateSwapchainFB(swapchain, (XrSwapchainStateBaseHeaderFB*)&foveationState);
```

| FFR Level | GPU Savings (approx) | Visual Impact |
|---|---|---|
| None | 0% | Baseline |
| Low | 5-10% | Barely noticeable |
| Medium | 10-20% | Slight peripheral softness |
| High | 20-30% | Noticeable at periphery |
| HighTop | 25-35% | Aggressive, top edge also reduced |

**Dynamic foveation**: Set `dynamic = XR_FOVEATION_DYNAMIC_LEVEL_ENABLED_FB` to let the runtime auto-adjust FFR level based on GPU utilization. The specified level becomes the maximum.

## Passthrough

Extension: `XR_FB_passthrough`. See `references/compositor-pipeline.md` for full setup.

Key points:
- Create `XrPassthroughFB` + `XrPassthroughLayerFB`
- Set `environmentBlendMode = XR_ENVIRONMENT_BLEND_MODE_ALPHA_BLEND` in frame end
- Submit passthrough layer BEFORE projection layers (renders behind app content)
- Style adjustable: brightness/contrast/saturation via `XrPassthroughStyleFB`

## Performance

### CPU/GPU Levels

Quest uses dynamic frequency scaling. Apps can request higher clock levels:

```cpp
// Via XR_EXT_performance_settings
XrPerfSettingsLevelEXT level = XR_PERF_SETTINGS_LEVEL_SUSTAINED_HIGH_EXT;
xrPerfSettingsSetPerformanceLevelEXT(session, XR_PERF_SETTINGS_DOMAIN_CPU_EXT, level);
xrPerfSettingsSetPerformanceLevelEXT(session, XR_PERF_SETTINGS_DOMAIN_GPU_EXT, level);
```

| Level | When |
|---|---|
| `POWER_SAVINGS` | Menu/idle screens |
| `SUSTAINED_LOW` | Simple scenes |
| `SUSTAINED_HIGH` | Complex rendering (default target) |
| `BOOST` | Brief spikes only -- causes thermal throttle |

**Rule**: Use the lowest level that maintains framerate. Higher levels drain battery faster and hit thermal limits sooner.

### Thermal Throttling

When thermal limit is reached, the runtime forces CPU/GPU to power-save levels equivalent to (0,0). Monitor via `XR_EXT_performance_settings` notification events.

Mitigations:
- Dynamic resolution scaling (reduce eye buffer size when hot)
- Increase FFR level
- Reduce draw calls, particle counts, shadow resolution
- Target 90Hz instead of 120Hz

### Performance Budgets

| Metric | Target (90Hz) | Target (120Hz) |
|---|---|---|
| Frame time | < 11.1ms | < 8.3ms |
| Draw calls | < 100-150 | < 80-100 |
| Triangles/frame | < 200K (Q2) / 500K (Q3) | Reduce ~25% |
| Texture memory | < 1 GB | < 1 GB |

### Texture Compression

| Format | BPP | Support | Notes |
|---|---|---|---|
| ASTC 4x4 | 8.0 | All Quest | Best quality, moderate compression |
| ASTC 6x6 | 3.56 | All Quest | Good balance |
| ASTC 8x8 | 2.0 | All Quest | Aggressive, some block artifacts |
| ETC2 | 8.0 | All Quest | Fallback, no alpha quality issues |

**Always use ASTC** on Quest. Uncompressed textures waste shared memory and bandwidth. Use `astcenc` or KTX2 with ASTC for asset pipeline.

## Android Build & Packaging

### AndroidManifest.xml

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.vrapp">

    <!-- VR app markers -->
    <uses-feature android:name="android.hardware.vr.headtracking" android:required="true" />

    <application android:allowBackup="false" android:hasCode="false">
        <activity android:name="android.app.NativeActivity"
            android:theme="@android:style/Theme.Black.NoTitleBar.Fullscreen"
            android:launchMode="singleTask"
            android:screenOrientation="landscape"
            android:configChanges="density|keyboard|keyboardHidden|navigation|orientation|screenLayout|screenSize|uiMode"
            android:excludeFromRecents="false">

            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="com.oculus.intent.category.VR" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Target Quest devices -->
        <meta-data android:name="com.oculus.supportedDevices"
            android:value="quest2|quest3|quest3s" />
    </application>
</manifest>
```

### build.gradle (NDK)

```groovy
android {
    compileSdkVersion 33
    ndkVersion "25.2.9519653"

    defaultConfig {
        minSdkVersion 26        // Quest minimum
        targetSdkVersion 32
        ndk { abiFilters 'arm64-v8a' }  // Quest is arm64 only
        externalNativeBuild {
            cmake {
                arguments '-DANDROID_STL=c++_shared',
                          '-DANDROID_PLATFORM=android-26'
            }
        }
    }

    externalNativeBuild {
        cmake {
            path 'src/main/cpp/CMakeLists.txt'
        }
    }
}
```

### OpenXR Loader

Use the Khronos OpenXR Loader **v1.0.34+** (older versions crash on Quest). No proprietary loader required.

```cmake
# CMakeLists.txt
find_package(OpenXR REQUIRED)
target_link_libraries(${PROJECT_NAME} OpenXR::openxr_loader)
```

## What NOT to Do

- **Skip `xrWaitFrame`** -- causes frame pacing issues and compositor desync
- **Render at display resolution** -- use `recommendedImageRectWidth/Height`, not display pixel count
- **Allocate per-frame** -- shared memory means GC/malloc pressure hits both CPU and GPU
- **Use `BOOST` level sustained** -- guaranteed thermal throttle within minutes
- **Ignore `XR_SESSION_STATE_STOPPING`** -- must release swapchains and end session cleanly
- **Use multi-pass stereo** when multiview is available -- doubles draw calls for no benefit
- **Submit layers with stale poses** -- always query poses at `predictedDisplayTime`

## Troubleshooting

| Symptom | Likely Cause |
|---|---|
| Black screen on launch | Missing VR intent category in manifest, wrong loader version |
| Judder/swimmy feel | Rendering with stale pose, missing `xrWaitFrame` |
| One eye black | Wrong `imageArrayIndex` in projection view, multiview not enabled |
| Thermal throttle in <5min | CPU/GPU level too high, no dynamic resolution |
| Crash on swapchain create | Unsupported format, `arraySize` wrong for multiview |
| Passthrough not visible | Layer order wrong (must be behind projection), blend mode not set |
| FFR not applying | Profile not attached to swapchain, or dynamic disabled |
| APK rejected by Store | Missing `com.oculus.supportedDevices`, wrong `minSdkVersion` |
| Distorted periphery | Asymmetric projection not handled in shader |

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|---|---|
| `compositor-pipeline.md` | Frame timing details, layer ordering, passthrough setup, depth composition |
| `quest-perf-targets.md` | Hardware limits, profiling tools, optimization strategies, memory budgets |

## Key Extensions Reference

| Extension | Purpose |
|---|---|
| `XR_KHR_opengl_es_enable` | OpenGL ES graphics binding |
| `XR_KHR_vulkan_enable2` | Vulkan graphics binding |
| `XR_FB_foveation` | Foveated rendering base |
| `XR_FB_foveation_configuration` | FFR level control |
| `XR_FB_space_warp` | Application SpaceWarp |
| `XR_FB_passthrough` | Camera passthrough |
| `XR_FB_hand_tracking_mesh` | Hand mesh rendering |
| `XR_EXT_hand_tracking` | Hand skeleton tracking |
| `XR_FB_scene` | Scene understanding / room layout |
| `XR_FB_spatial_entity` | Spatial anchors |
| `XR_EXT_performance_settings` | CPU/GPU level control |
| `XR_KHR_composition_layer_depth` | Depth-based reprojection |
| `XR_FB_display_refresh_rate` | Query/set refresh rate |
