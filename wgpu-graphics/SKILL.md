---
name: wgpu-graphics
description: "Rust GPU graphics/compute: pipelines, shaders, textures, VR compositors"
---

# wgpu Graphics

## Before Writing Code

1. **Check wgpu version** -- API changed significantly across 0.19/0.20/22/24/25/26:
   ```bash
   grep -E '^wgpu\s*=' Cargo.toml
   ```

2. **Identify backend requirements**:
   - Desktop: Vulkan (Linux/Windows), Metal (macOS), DX12 (Windows)
   - Mobile: Vulkan (Android), Metal (iOS), OpenGL ES (Android fallback)
   - Web: WebGPU or WebGL2 (via wasm)

3. **Detect existing patterns**:
   - HAL interop (`as_hal`, `create_texture_from_hal`) = low-level integration
   - Push constants = OpenGL/Vulkan feature, check `Features::PUSH_CONSTANTS`
   - External textures = platform-specific (EGL images, Vulkan interop)

## Core Architecture

```
Instance -> Adapter -> (Device, Queue)
                            |
              +---------+---+---+---------+
              |         |       |         |
          Buffers   Textures  Shaders  Pipelines
              |         |       |         |
              +----+----+   BindGroups    |
                   |            |         |
              CommandEncoder ---+---------+
                   |
                 Queue.submit()
```

### Initialization

```rust
let instance = wgpu::Instance::new(&wgpu::InstanceDescriptor {
    backends: wgpu::Backends::PRIMARY, // Vulkan + Metal + DX12
    flags: if cfg!(debug_assertions) {
        wgpu::InstanceFlags::DEBUG | wgpu::InstanceFlags::VALIDATION
    } else {
        wgpu::InstanceFlags::empty()
    },
    ..Default::default()
});

let adapter = instance.request_adapter(&wgpu::RequestAdapterOptions {
    power_preference: wgpu::PowerPreference::HighPerformance,
    compatible_surface: surface.as_ref(), // None for headless/compute
    force_fallback_adapter: false,
}).await.expect("no suitable GPU adapter");

let (device, queue) = adapter.request_device(&wgpu::DeviceDescriptor {
    label: Some("Main Device"),
    required_features: wgpu::Features::empty(), // add what you need
    required_limits: wgpu::Limits::default(),    // or adapter.limits()
    memory_hints: wgpu::MemoryHints::Performance,
}, None).await.unwrap();
```

### Backend Selection

| Backend | Platform | When to Use |
|---------|----------|-------------|
| `Backends::VULKAN` | Linux, Windows, Android | Default for these platforms |
| `Backends::METAL` | macOS, iOS | Default for Apple platforms |
| `Backends::DX12` | Windows | Alternative to Vulkan |
| `Backends::GL` | Android, Web (WebGL2) | Fallback when Vulkan unavailable |
| `Backends::BROWSER_WEBGPU` | Web | WebGPU in browser |
| `Backends::PRIMARY` | All | Vulkan + Metal + DX12 (recommended) |

## Pipeline Setup

### Render Pipeline

See `references/pipeline-setup.md` for full vertex buffer layout patterns.

Key decisions:
- **Vertex-less rendering** (fullscreen quad): use `vertex_index` builtin, `TriangleStrip` with 4 vertices, no vertex buffers
- **Vertex buffers**: define `VertexBufferLayout` with stride and attributes
- **Push constants** vs **uniform buffers**: push constants are faster for small (<128 bytes) per-draw data, but require `Features::PUSH_CONSTANTS`

### Compute Pipeline

See `references/compute-patterns.md` for workgroup sizing and image processing patterns.

```rust
let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
    label: Some("Compute"),
    layout: Some(&pipeline_layout),
    module: &shader,
    entry_point: Some("main"),
    compilation_options: Default::default(),
    cache: None,
});
```

## WGSL Shader Patterns

### Push Constants (ALVR pattern)

```wgsl
struct PushConstant {
    transform: mat4x4f,
    view_idx: u32,
}
var<push_constant> pc: PushConstant;

@vertex
fn vertex_main(@builtin(vertex_index) idx: u32) -> VertexOutput {
    var out: VertexOutput;
    out.uv = vec2f(f32(idx & 1), f32(idx >> 1));
    out.position = pc.transform * vec4f(out.uv.x - 0.5, 0.5 - out.uv.y, 0.0, 1.0);
    return out;
}
```

### Pipeline Override Constants

Compile-time specialization -- avoids branching in hot shaders:

```rust
let mut constants = HashMap::new();
constants.insert("ENABLE_FEATURE".into(), true.into());
constants.insert("GAMMA_VALUE".into(), 2.2_f64);

// In pipeline descriptor:
compilation_options: PipelineCompilationOptions {
    constants: &constants,
    zero_initialize_workgroup_memory: false,
},
```

```wgsl
override ENABLE_FEATURE: bool = false;
override GAMMA_VALUE: f32 = 1.0;
```

## Resource Management

### Textures

```rust
let texture = device.create_texture(&wgpu::TextureDescriptor {
    label: Some("My Texture"),
    size: wgpu::Extent3d { width, height, depth_or_array_layers: 1 },
    mip_level_count: 1,
    sample_count: 1,
    dimension: wgpu::TextureDimension::D2,
    format: wgpu::TextureFormat::Rgba8UnormSrgb,
    usage: wgpu::TextureUsages::TEXTURE_BINDING | wgpu::TextureUsages::COPY_DST,
    view_formats: &[],
});

// Upload data
queue.write_texture(
    wgpu::TexelCopyTextureInfo {
        texture: &texture, mip_level: 0,
        origin: wgpu::Origin3d::ZERO, aspect: wgpu::TextureAspect::All,
    },
    &rgba_data,
    wgpu::TexelCopyBufferLayout {
        offset: 0,
        bytes_per_row: Some(width * 4),
        rows_per_image: Some(height),
    },
    wgpu::Extent3d { width, height, depth_or_array_layers: 1 },
);
```

### Common Texture Formats

| Format | Use Case | Notes |
|--------|----------|-------|
| `Rgba8UnormSrgb` | Color textures (sRGB) | Auto gamma correction |
| `Rgba8Unorm` | Linear color, data textures | No gamma, use for compositing |
| `Bgra8UnormSrgb` | Swapchain (common default) | Desktop surface format |
| `Rgba16Float` | HDR rendering | 16-bit float per channel |
| `Depth32Float` | Depth buffer | Standard depth format |
| `R8Unorm` | Single channel (alpha masks) | Grayscale data |

### Buffer Mapping (GPU readback)

```rust
// 1. Copy GPU buffer -> staging buffer (MAP_READ | COPY_DST)
encoder.copy_buffer_to_buffer(&gpu_buf, 0, &staging_buf, 0, size);
queue.submit(Some(encoder.finish()));

// 2. Map the staging buffer
staging_buf.slice(..).map_async(wgpu::MapMode::Read, |_| {});
device.poll(wgpu::PollType::Wait); // blocks until mapped

// 3. Read data
let data = staging_buf.slice(..).get_mapped_range();
let result: &[f32] = bytemuck::cast_slice(&data);
// ... use result ...
drop(data);
staging_buf.unmap();
```

### Drop-Based Cleanup

wgpu resources are reference-counted and cleaned up on drop. No explicit `dispose()` needed in most cases. However:
- **Textures/buffers from HAL** may need custom drop callbacks
- **Mapped buffers** must be unmapped before drop
- **Surface** must outlive its window

## What NOT to Do

- Mix `queue.write_buffer()` and `encoder.copy_buffer_to_buffer()` for the same destination in the same submission
- Call `device.poll()` in a tight loop without submitting work
- Use `mapped_at_creation: true` for large buffers you'll immediately unmap -- prefer `queue.write_buffer()`
- Assume texture format support -- check `adapter.get_texture_format_features()`
- Use `Backends::all()` when you only need native -- `Backends::PRIMARY` excludes GL/WebGL overhead

## Cross-Platform Differences

| Issue | Metal | Vulkan | DX12 | OpenGL |
|-------|-------|--------|------|--------|
| Push constant max size | 4KB | 128-256B typical | 256B | Not supported natively |
| Texture format naming | reversed byte order | standard | standard | varies |
| Validation layers | Metal validation | `VK_LAYER_KHRONOS_validation` | D3D12 debug layer | GL debug output |
| Surface format | `Bgra8UnormSrgb` | varies | `Bgra8UnormSrgb` | varies |
| Timestamp queries | Limited support | Full support | Full support | Not supported |

### Metal-Specific

- Metal Validation: set `MTL_DEBUG_LAYER=1` environment variable
- Push constants mapped to Metal argument buffers -- larger size limit but different perf profile
- `TextureFormat::Bgra8Unorm` is the standard swapchain format

### Vulkan-Specific

- Enable validation: `VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation`
- Push constant size varies by GPU -- query `adapter.limits().max_push_constant_size`
- Vulkan interop for external textures: use `wgpu::hal` API

## VR Compositor Patterns

See `references/vr-compositor.md` for ALVR-specific patterns including:
- OpenXR swapchain integration via HAL texture import
- Stereo rendering with per-view push constants
- Reprojection/timewarp with matrix-based UV correction
- Foveated encoding with shader override constants
- Staging renderers for Android hardware buffer decode

## Performance

### Pipeline Caching

```rust
// wgpu 24+: PipelineCacheDescriptor
let cache = device.create_pipeline_cache(&wgpu::PipelineCacheDescriptor {
    label: Some("Pipeline Cache"),
    data: None, // or load from disk
    fallback: true,
});
// Pass `cache: Some(&cache)` to pipeline descriptors
```

### Avoiding GPU Stalls

- **Never** call `device.poll(PollType::Wait)` on the render thread -- use async or poll with timeout
- **Double/triple buffer** uniform data -- don't write to a buffer the GPU is still reading
- **Batch submissions** -- one `queue.submit()` per frame with all command buffers
- **Minimize bind group switches** -- sort draws by pipeline/bind group

### Timestamp Queries

```rust
// Requires Features::TIMESTAMP_QUERY
let query_set = device.create_query_set(&wgpu::QuerySetDescriptor {
    label: Some("Timestamps"),
    ty: wgpu::QueryType::Timestamp,
    count: 2,
});

// In render/compute pass descriptor:
timestamp_writes: Some(wgpu::RenderPassTimestampWrites {
    query_set: &query_set,
    beginning_of_pass_write_index: Some(0),
    end_of_pass_write_index: Some(1),
}),

// Resolve to buffer
encoder.resolve_query_set(&query_set, 0..2, &timestamp_buf, 0);
// Read back and multiply by queue.get_timestamp_period() for nanoseconds
```

## Buffer Alignment

| Rule | Value | Notes |
|------|-------|-------|
| `COPY_BUFFER_ALIGNMENT` | 4 bytes | `copy_buffer_to_buffer` offset/size |
| `COPY_BYTES_PER_ROW_ALIGNMENT` | 256 bytes | `bytes_per_row` in texture copies |
| Uniform buffer offset | 256 bytes | Dynamic offset alignment |
| Storage buffer offset | 32 bytes minimum | Check `min_storage_buffer_offset_alignment` |
| Min uniform buffer size | varies | Check `min_uniform_buffer_binding_size` |

### Texture Copy Row Alignment

```rust
// bytes_per_row must be multiple of 256
let unpadded_row = width * bytes_per_pixel;
let padded_row = (unpadded_row + 255) & !255; // align to 256
```

## Troubleshooting

| Symptom | Likely Cause |
|---------|--------------|
| `RequestDeviceError` | Required features/limits not supported by adapter |
| Black screen | Missing bind group, wrong attachment format, no `queue.submit()` |
| Validation error: "buffer is not large enough" | Buffer size < bind group layout's `min_binding_size` |
| Texture copy fails | `bytes_per_row` not aligned to 256, or texture usage missing `COPY_DST`/`COPY_SRC` |
| `SurfaceError::Outdated` | Window resized -- reconfigure surface |
| `SurfaceError::Lost` | GPU reset or driver crash -- recreate surface |
| Push constants ignored | Layout not set (auto-layout doesn't infer push constants) |
| Shader compilation error | WGSL syntax, or using features not in `required_features` |
| Performance regression on Metal | Overuse of storage textures (Metal prefers render attachments) |

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `pipeline-setup.md` | Vertex buffer layouts, render pipeline variations, depth/stencil |
| `compute-patterns.md` | Compute shaders, workgroup sizing, image processing, GPU readback |
| `vr-compositor.md` | ALVR patterns, OpenXR integration, HAL interop, stereo rendering |
