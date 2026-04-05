# Quest Performance Targets & Optimization

## Memory Budgets

Quest uses unified memory (shared CPU/GPU). All texture, mesh, and buffer data lives in the same pool as app code and runtime overhead.

| Device | Total RAM | Available to App (approx) | Texture Budget |
|---|---|---|---|
| Quest 2 | 6 GB | ~3.5 GB | 1.0-1.5 GB |
| Quest 3 / 3S | 8 GB | ~4.5 GB | 1.5-2.0 GB |

**Texture memory dominates**. A single uncompressed 4096x4096 RGBA8 texture = 64 MB. With ASTC 6x6 = ~9.5 MB.

### Memory Monitoring

```cpp
// Use Android APIs to monitor memory pressure
#include <sys/sysinfo.h>

struct sysinfo si;
sysinfo(&si);
uint64_t availableRAM = si.freeram * si.mem_unit;
```

Or use `adb shell dumpsys meminfo <pid>` during development.

## GPU Performance

### Draw Call Budgets

| Complexity | Draw Calls | Triangles | Notes |
|---|---|---|---|
| Simple (menu/UI) | < 50 | < 50K | Easy 120Hz |
| Medium (game) | 50-150 | 100-300K | Target 90Hz |
| Complex (detailed world) | 150-300 | 300-500K | 72Hz, FFR High |
| Too much | > 300 | > 500K | Will drop frames |

### Rendering Optimization Checklist

- [ ] Multiview enabled (halves draw calls)
- [ ] FFR at Medium or higher
- [ ] ASTC textures everywhere
- [ ] Texture atlas for small textures
- [ ] LOD system for distant objects
- [ ] Occlusion culling (frustum at minimum)
- [ ] Dynamic resolution scaling when thermal
- [ ] No real-time shadows (or very low-res shadow maps, 512x512 max)
- [ ] Baked lighting where possible

### Shader Complexity

Quest GPUs (Adreno) are **bandwidth-limited**, not ALU-limited. Optimize for:
- Fewer texture samples per fragment
- Lower precision (`mediump` default, `highp` only where needed)
- Avoid dependent texture reads
- Minimize overdraw (alpha blending is expensive)

```glsl
// Prefer mediump everywhere possible
precision mediump float;
precision mediump sampler2D;

// Only use highp for positions and depth
highp vec4 position;
```

### Fill Rate

Quest panels are high-resolution. At 2064x2208 per eye (Quest 3), that is ~9.1M pixels per eye, ~18.2M total. Every pixel of overdraw multiplies this cost.

Reduce overdraw:
- Sort opaque objects front-to-back
- Use early-Z / depth pre-pass for complex scenes
- Minimize transparent/alpha-blended surfaces
- Discard fragments in shader rather than blending with alpha=0

## CPU Performance

### Thread Model

Quest apps typically use:
- **Main thread**: OpenXR frame loop, pose queries, layer submission
- **Render thread**: GL/Vulkan command recording (can be same as main)
- **Game thread**: physics, AI, game logic
- **Audio thread**: spatial audio processing

Keep the main/render thread as lean as possible. Offload work to game thread. The OpenXR frame loop must never block on game logic.

### Java/JNI Overhead

Native apps still run in an Android Activity. JNI calls have overhead:
- Batch JNI calls (don't cross boundary per-frame for trivial data)
- Cache `jclass` and `jmethodID` lookups
- Use `AttachCurrentThread` / `DetachCurrentThread` carefully on worker threads

## Profiling Tools

| Tool | What It Shows | How to Use |
|---|---|---|
| OVR Metrics Tool | FPS, CPU/GPU time, thermals, tears | Sideload APK, runs as overlay |
| Snapdragon Profiler | GPU counters, shader analysis, memory | USB connection, capture traces |
| Android GPU Inspector | Vulkan frame captures | `adb` + AGI desktop app |
| RenderDoc | Frame debugging (Vulkan) | RenderDoc Android build |
| `adb shell dumpsys` | Memory, process info | `adb shell dumpsys meminfo <pid>` |
| Systrace / Perfetto | CPU thread timelines | `adb` trace capture |

### OVR Metrics Tool Key Metrics

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| App GPU Time | < 8ms (90Hz) | 8-10ms | > 10ms |
| App CPU Time | < 8ms (90Hz) | 8-10ms | > 10ms |
| Stale frames/sec | 0 | 1-3 | > 5 |
| Tears/sec | 0 | Any | - |
| Temperature | < 35C | 35-40C | > 40C |
| Battery level | > 20% | 10-20% | < 10% |

## Dynamic Resolution Scaling

Reduce eye buffer resolution when GPU-bound or thermal-throttling:

```cpp
// Start at recommended resolution
uint32_t renderWidth = viewConfig.recommendedImageRectWidth;
uint32_t renderHeight = viewConfig.recommendedImageRectHeight;

// Scale factor: 1.0 = full, 0.7 = 70% (good fallback)
float scaleFactor = 1.0f;

// Adjust based on frame timing
if (lastGpuTimeMs > 10.0f) {
    scaleFactor = std::max(0.6f, scaleFactor - 0.05f);
} else if (lastGpuTimeMs < 7.0f && scaleFactor < 1.0f) {
    scaleFactor = std::min(1.0f, scaleFactor + 0.02f);
}

// Use imageRect in layer submission to render smaller viewport
projectionViews[eye].subImage.imageRect = {
    {0, 0},
    {(int32_t)(renderWidth * scaleFactor), (int32_t)(renderHeight * scaleFactor)}
};
```

**Note**: You cannot resize the swapchain at runtime. Create it at full recommended size and use `imageRect` to control the rendered viewport. The compositor upscales.

## Vulkan-Specific Considerations

### Validation Layers on Quest

Vulkan validation layers work on Quest but are very slow (~10x overhead). Use only during development:

```cpp
const char* validationLayers[] = {"VK_LAYER_KHRONOS_validation"};
// Enable only in debug builds
#ifdef NDEBUG
    createInfo.enabledLayerCount = 0;
#else
    createInfo.enabledLayerCount = 1;
    createInfo.ppEnabledLayerNames = validationLayers;
#endif
```

### Vulkan vs OpenGL ES on Quest

| Aspect | OpenGL ES | Vulkan |
|---|---|---|
| Ease of use | Simpler, more samples | Complex, explicit |
| Multiview | `GL_OVR_multiview2` | `VK_KHR_multiview` |
| CPU overhead | Higher (driver thread) | Lower (explicit) |
| GPU perf | Same hardware | Same hardware |
| Debugging | RenderDoc limited | Full RenderDoc + AGI |
| Meta samples | More available | Growing |

For most projects, OpenGL ES is simpler with no GPU performance penalty. Choose Vulkan for CPU-bound apps that need explicit threading control or advanced features.

## Common Performance Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Uncompressed textures | Convert all to ASTC |
| Per-frame allocations | Pre-allocate, use pools |
| Unnecessary state changes | Sort by material/shader |
| Full-res shadow maps | Bake shadows or use 256-512px cascades |
| Reading back from GPU | Never `glReadPixels` in frame loop |
| Unbatched small meshes | Merge static geometry |
| Complex fragment shaders | Use `mediump`, simplify PBR |
| No frustum culling | Cull against view frustum per eye |
| Debug logging in release | Strip all `ALOG*` in release builds |
| Synchronous asset loads | Load on background thread |
