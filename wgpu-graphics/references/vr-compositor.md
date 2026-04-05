# VR Compositor Patterns

Patterns from ALVR's wgpu-based VR compositor for OpenXR headsets.

## Architecture Overview

```
Hardware Buffer (decoded video) -> Staging Renderer (GL) -> Staging Texture (wgpu)
    -> Stream Renderer (wgpu render pipeline) -> OpenXR Swapchain (per-eye)
```

ALVR uses a hybrid GL + wgpu approach on Android:
- **GL (glow)**: Imports Android hardware buffers via EGL, renders to staging textures
- **wgpu**: Compositing, reprojection, foveated encoding decode, all render passes

## GraphicsContext Pattern

Centralized GPU context holding wgpu core objects + platform-specific handles:

```rust
pub struct GraphicsContext {
    _instance: wgpu::Instance,
    adapter: wgpu::Adapter,
    pub device: wgpu::Device,
    pub queue: wgpu::Queue,
    // Platform-specific (Android/GL)
    pub egl_display: egl::Display,
    pub egl_config: egl::Config,
    pub egl_context: egl::Context,
    pub gl_context: gl::Context,
}
```

Key design decisions:
- Uses `Rc<GraphicsContext>` -- shared ownership without thread-safety overhead (VR compositor is single-threaded render loop)
- Stores raw EGL/GL handles for Android hardware buffer interop
- `make_current()` method for EGL context binding before GL calls

## OpenXR Swapchain Integration

Import OpenXR GL textures into wgpu via HAL:

```rust
pub fn create_gl_swapchain(
    device: &wgpu::Device,
    gl_textures: &[u32],  // OpenXR swapchain texture IDs
    resolution: UVec2,
    format: wgpu::TextureFormat,
) -> Vec<wgpu::TextureView> {
    gl_textures.iter().map(|gl_tex| {
        create_texture_from_gles(device, *gl_tex, resolution, format)
            .create_view(&Default::default())
    }).collect()
}

fn create_texture_from_gles(
    device: &wgpu::Device,
    texture: u32,
    resolution: UVec2,
    format: wgpu::TextureFormat,
) -> wgpu::Texture {
    let size = wgpu::Extent3d {
        width: resolution.x, height: resolution.y, depth_or_array_layers: 1,
    };

    unsafe {
        let hal_texture = device.as_hal::<wgpu::hal::api::Gles, _, _>(|device| {
            device.unwrap().texture_from_raw(
                NonZeroU32::new(texture).unwrap(),
                &wgpu::hal::TextureDescriptor {
                    label: None, size, mip_level_count: 1, sample_count: 1,
                    dimension: wgpu::TextureDimension::D2, format,
                    usage: wgpu::hal::TextureUses::COLOR_TARGET,
                    memory_flags: wgpu::hal::MemoryFlags::empty(),
                    view_formats: vec![],
                },
                Some(Box::new(|| ())), // drop callback
            )
        });

        device.create_texture_from_hal::<wgpu::hal::api::Gles>(
            hal_texture,
            &wgpu::TextureDescriptor {
                label: None, size, mip_level_count: 1, sample_count: 1,
                dimension: wgpu::TextureDimension::D2, format,
                usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
                view_formats: &[],
            },
        )
    }
}
```

## Stereo Rendering with Push Constants

Per-eye rendering using push constants for transform data:

```rust
// Push constant layout
const TRANSFORM_SIZE: u32 = std::mem::size_of::<Mat4>() as u32;  // 64 bytes
const VIEW_INDEX_SIZE: u32 = std::mem::size_of::<u32>() as u32;  // 4 bytes
// Total: 68+ bytes, well within 128B limit

for (view_idx, view_params) in view_params.iter().enumerate() {
    let mut pass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
        color_attachments: &[Some(wgpu::RenderPassColorAttachment {
            view: &render_targets[view_idx][swapchain_index],
            resolve_target: None,
            ops: wgpu::Operations {
                load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
                store: wgpu::StoreOp::Store,
            },
        })],
        ..Default::default()
    });

    // Compute reprojection transform
    let model = Mat4::from_translation(/* quad position */);
    let view = Mat4::from_quat(view_params.reprojection_rotation).inverse();
    let proj = projection_from_fov(view_params.fov);
    let transform = proj * view * model;

    pass.set_pipeline(&pipeline);
    pass.set_push_constants(
        wgpu::ShaderStages::VERTEX_FRAGMENT, 0,
        bytemuck::cast_slice(&transform.to_cols_array()),
    );
    pass.set_push_constants(
        wgpu::ShaderStages::VERTEX_FRAGMENT, TRANSFORM_SIZE,
        &(view_idx as u32).to_le_bytes(),
    );
    pass.set_bind_group(0, &bind_groups[view_idx], &[]);
    pass.draw(0..4, 0..1); // fullscreen quad
}
queue.submit(Some(encoder.finish()));
```

## Projection Matrix for VR

Asymmetric frustum from OpenXR FoV (tangent angles):

```rust
fn projection_from_fov(fov: Fov) -> Mat4 {
    const NEAR: f32 = 0.1;
    let tanl = f32::tan(fov.left);
    let tanr = f32::tan(fov.right);
    let tanu = f32::tan(fov.up);
    let tand = f32::tan(fov.down);

    let a = 2.0 / (tanr - tanl);
    let b = 2.0 / (tanu - tand);
    let c = (tanr + tanl) / (tanr - tanl);
    let d = (tanu + tand) / (tanu - tand);

    // Infinite reverse-Z with flipped Y for wgpu NDC
    Mat4::from_cols(
        Vec4::new(a,    0.0,  c,     0.0),
        Vec4::new(0.0, -b,   -d,     0.0),
        Vec4::new(0.0,  0.0, -1.0,  -NEAR),
        Vec4::new(0.0,  0.0, -1.0,   0.0),
    ).transpose()
}
```

Notes:
- Y is negated for wgpu's clip space (Y-down in NDC)
- Uses infinite far plane with reverse-Z for better depth precision
- FoV angles are in radians, typically asymmetric per-eye

## Foveated Encoding

ALVR implements Fixed Foveated Encoding (FFE) -- compresses peripheral regions at lower resolution, decoded in the fragment shader via override constants.

### Rust side: compute shader constants

```rust
// Calculate optimized resolution and FFE parameters
let foveation_scale = center_size + (1.0 - center_size) / edge_ratio;
let optimized_resolution = foveation_scale * view_resolution;

let mut constants = HashMap::new();
constants.insert("ENABLE_FFE".into(), 1.0);
constants.insert("VIEW_WIDTH_RATIO".into(), ratio.x as f64);
constants.insert("EDGE_X_RATIO".into(), edge_ratio.x as f64);
// ... many more parameters for piecewise UV remapping
```

### WGSL side: UV correction

```wgsl
override ENABLE_FFE: bool = false;
override VIEW_WIDTH_RATIO: f32 = 0.0;
override EDGE_X_RATIO: f32 = 0.0;
// ... more overrides

@fragment
fn fragment_main(@location(0) uv: vec2f) -> @location(0) vec4f {
    var corrected_uv = uv;
    if ENABLE_FFE {
        // Piecewise linear/quadratic UV remapping
        // Center region: linear mapping
        // Edge regions: quadratic expansion (undo compression)
        corrected_uv = decompress_foveated_uv(uv);
    }
    return textureSample(texture, tex_sampler, corrected_uv);
}
```

## Chroma Key / Passthrough

For mixed reality passthrough with chroma keying:

```wgsl
struct PushConstant {
    // ...
    passthrough_mode: u32,  // 0=blend, 1=RGB chroma, 2=HSV chroma
    blend_alpha: f32,
    ck_channel0: vec4f,     // per-channel [start_max, start_min, end_min, end_max]
    ck_channel1: vec4f,
    ck_channel2: vec4f,
}

fn chroma_key_mask(color: vec3f) -> f32 {
    // Smoothstep-based feathered masking
    let start_mask = smoothstep(start_min, start_max, color);
    let end_mask = smoothstep(end_min, end_max, color);
    return max(start_mask.x, max(start_mask.y, /* ... */));
}
```

## Staging Renderer (Hardware Buffer Import)

Android-specific pattern for importing decoded video frames:

1. Get `ANativeWindowBuffer` from MediaCodec
2. Create EGL image from hardware buffer via `eglCreateImageKHR`
3. Bind to `GL_TEXTURE_EXTERNAL_OES`
4. Render fullscreen quad to wgpu staging texture via GL
5. wgpu pipeline reads staging texture for final compositing

This hybrid approach is needed because wgpu doesn't directly support Android hardware buffer import. The GL staging step bridges the gap.

## wgpu vs Raw Vulkan for VR

| Aspect | wgpu | Raw Vulkan |
|--------|------|-----------|
| Swapchain management | Abstracted (Surface) | Manual (VkSwapchainKHR) |
| Synchronization | Automatic | Manual (fences, semaphores) |
| Memory allocation | Automatic | Manual or via VMA |
| OpenXR texture import | HAL interop (verbose) | Direct VkImage import |
| Multiview rendering | `multiview` field | VK_KHR_multiview extension |
| Push constants | Cross-backend abstraction | Direct Vulkan push constants |
| External memory | Not directly supported | VK_KHR_external_memory |
| Timeline semaphores | Not exposed | VK_KHR_timeline_semaphore |
| Debug markers | Limited | VK_EXT_debug_utils |

### When to drop to raw Vulkan

- External memory import/export (DMA-buf, hardware buffers)
- Timeline semaphore synchronization with external APIs
- Fine-grained queue family management
- Direct Vulkan extension access not exposed by wgpu

### When wgpu is sufficient

- All compositing and shader work
- Texture rendering and postprocessing
- Cross-platform compute pipelines
- Most VR compositor logic (with GL staging for Android)

## Multiview Rendering

For stereo rendering without per-eye loops (requires `Features::MULTIVIEW`):

```rust
// Pipeline with multiview
multiview: Some(NonZeroU32::new(2).unwrap()),

// Texture array for both eyes
let stereo_texture = device.create_texture(&wgpu::TextureDescriptor {
    size: wgpu::Extent3d {
        width, height,
        depth_or_array_layers: 2, // one layer per eye
    },
    // ...
});
```

```wgsl
@vertex
fn vs_main(@builtin(view_index) view_idx: u32) -> VertexOutput {
    // Use view_idx to select per-eye transform
    let transform = transforms[view_idx];
    // ...
}
```

Note: ALVR currently uses a per-eye render loop rather than multiview, allowing different bind groups per eye. Multiview is more efficient but less flexible.
