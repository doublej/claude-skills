# Compute Patterns

## Full Compute Pipeline Example

```rust
use wgpu::util::DeviceExt;

// 1. Create buffers
let input_buf = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
    label: Some("Input"),
    contents: bytemuck::cast_slice(&input_data),
    usage: wgpu::BufferUsages::STORAGE,
});
let output_buf = device.create_buffer(&wgpu::BufferDescriptor {
    label: Some("Output"),
    size: output_size,
    usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
    mapped_at_creation: false,
});
let staging_buf = device.create_buffer(&wgpu::BufferDescriptor {
    label: Some("Staging"),
    size: output_size,
    usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
    mapped_at_creation: false,
});

// 2. Bind group layout + bind group
let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
    label: None,
    entries: &[
        wgpu::BindGroupLayoutEntry {
            binding: 0, visibility: wgpu::ShaderStages::COMPUTE,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Storage { read_only: true },
                has_dynamic_offset: false, min_binding_size: None,
            },
            count: None,
        },
        wgpu::BindGroupLayoutEntry {
            binding: 1, visibility: wgpu::ShaderStages::COMPUTE,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Storage { read_only: false },
                has_dynamic_offset: false, min_binding_size: None,
            },
            count: None,
        },
    ],
});
let bg = device.create_bind_group(&wgpu::BindGroupDescriptor {
    label: None, layout: &bgl,
    entries: &[
        wgpu::BindGroupEntry { binding: 0, resource: input_buf.as_entire_binding() },
        wgpu::BindGroupEntry { binding: 1, resource: output_buf.as_entire_binding() },
    ],
});

// 3. Pipeline
let pipeline_layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
    label: None, bind_group_layouts: &[&bgl],
    push_constant_ranges: &[], immediate_size: 0,
});
let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
    label: Some("Compute"), layout: Some(&pipeline_layout),
    module: &shader, entry_point: Some("main"),
    compilation_options: Default::default(), cache: None,
});

// 4. Dispatch
let mut encoder = device.create_command_encoder(&Default::default());
{
    let mut pass = encoder.begin_compute_pass(&Default::default());
    pass.set_pipeline(&pipeline);
    pass.set_bind_group(0, &bg, &[]);
    pass.dispatch_workgroups(dispatch_x, 1, 1);
}
encoder.copy_buffer_to_buffer(&output_buf, 0, &staging_buf, 0, output_size);
queue.submit(Some(encoder.finish()));

// 5. Readback
staging_buf.slice(..).map_async(wgpu::MapMode::Read, |_| {});
device.poll(wgpu::PollType::Wait);
let data = staging_buf.slice(..).get_mapped_range();
let result: &[f32] = bytemuck::cast_slice(&data);
```

## Workgroup Sizing

### Guidelines

| Dimension | Typical Size | Notes |
|-----------|-------------|-------|
| 1D data | `@workgroup_size(64)` or `(256)` | Match warp/wavefront size (32 NVIDIA, 64 AMD) |
| 2D image | `@workgroup_size(8, 8)` or `(16, 16)` | 64 or 256 threads total |
| 3D volume | `@workgroup_size(4, 4, 4)` | 64 threads total |

### Dispatch Count Formula

```rust
// Always round up to cover all elements
let dispatch_x = (element_count + workgroup_size - 1) / workgroup_size;

// For 2D:
let dispatch_x = (width + wg_x - 1) / wg_x;
let dispatch_y = (height + wg_y - 1) / wg_y;
```

### Bounds Checking in Shader

```wgsl
@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    if id.x >= arrayLength(&data) { return; }
    // ... process data[id.x]
}
```

### Limits

- Max workgroup size per dimension: 256
- Max total invocations per workgroup: 256 (default) or check `max_compute_invocations_per_workgroup`
- Max dispatch per dimension: 65535

## Image Processing Patterns

### Per-Pixel Compute Shader

```wgsl
@group(0) @binding(0) var input: texture_2d<f32>;
@group(0) @binding(1) var output: texture_storage_2d<rgba8unorm, write>;

@compute @workgroup_size(8, 8)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let dims = textureDimensions(input);
    if id.x >= dims.x || id.y >= dims.y { return; }

    let color = textureLoad(input, vec2<u32>(id.x, id.y), 0);
    let gray = dot(color.rgb, vec3f(0.299, 0.587, 0.114));
    textureStore(output, vec2<u32>(id.x, id.y), vec4f(gray, gray, gray, 1.0));
}
```

Bind group for storage texture:
```rust
wgpu::BindGroupLayoutEntry {
    binding: 1,
    visibility: wgpu::ShaderStages::COMPUTE,
    ty: wgpu::BindingType::StorageTexture {
        access: wgpu::StorageTextureAccess::WriteOnly,
        format: wgpu::TextureFormat::Rgba8Unorm,
        view_dimension: wgpu::TextureViewDimension::D2,
    },
    count: None,
},
```

### Convolution / Blur with Shared Memory

```wgsl
const TILE_SIZE: u32 = 16;
const KERNEL_RADIUS: u32 = 2;
const SHARED_SIZE: u32 = TILE_SIZE + KERNEL_RADIUS * 2;

var<workgroup> shared_tile: array<vec4f, SHARED_SIZE * SHARED_SIZE>;

@compute @workgroup_size(TILE_SIZE, TILE_SIZE)
fn blur(
    @builtin(global_invocation_id) gid: vec3<u32>,
    @builtin(local_invocation_id) lid: vec3<u32>,
) {
    let dims = textureDimensions(input);

    // Load tile + halo into shared memory
    let shared_x = lid.x + KERNEL_RADIUS;
    let shared_y = lid.y + KERNEL_RADIUS;
    let sample_pos = vec2<i32>(vec2<u32>(gid.x, gid.y)) - vec2<i32>(i32(KERNEL_RADIUS));

    // Center pixel
    let sx = clamp(i32(gid.x), 0, i32(dims.x) - 1);
    let sy = clamp(i32(gid.y), 0, i32(dims.y) - 1);
    shared_tile[shared_y * SHARED_SIZE + shared_x] = textureLoad(input, vec2<u32>(u32(sx), u32(sy)), 0);

    // Load halo pixels (border threads load extra)
    // ... (elided for brevity, load left/right/top/bottom halo)

    workgroupBarrier();

    if gid.x >= dims.x || gid.y >= dims.y { return; }

    // Apply kernel
    var sum = vec4f(0.0);
    for (var ky: i32 = -i32(KERNEL_RADIUS); ky <= i32(KERNEL_RADIUS); ky++) {
        for (var kx: i32 = -i32(KERNEL_RADIUS); kx <= i32(KERNEL_RADIUS); kx++) {
            let idx = (i32(shared_y) + ky) * i32(SHARED_SIZE) + (i32(shared_x) + kx);
            sum += shared_tile[idx];
        }
    }
    let kernel_size = f32((2 * KERNEL_RADIUS + 1) * (2 * KERNEL_RADIUS + 1));
    textureStore(output, gid.xy, sum / kernel_size);
}
```

### YUV to RGB Decode

Common for video texture decode in VR compositors:

```wgsl
@group(0) @binding(0) var y_plane: texture_2d<f32>;
@group(0) @binding(1) var uv_plane: texture_2d<f32>;  // half resolution
@group(0) @binding(2) var output: texture_storage_2d<rgba8unorm, write>;

@compute @workgroup_size(8, 8)
fn yuv_to_rgb(@builtin(global_invocation_id) id: vec3<u32>) {
    let dims = textureDimensions(y_plane);
    if id.x >= dims.x || id.y >= dims.y { return; }

    let y = textureLoad(y_plane, id.xy, 0).r;
    let uv = textureLoad(uv_plane, id.xy / 2, 0).rg;

    // BT.709 YUV to RGB
    let y_scaled = (y - 16.0 / 255.0) * (255.0 / 219.0);
    let u = uv.x - 0.5;
    let v = uv.y - 0.5;

    let r = y_scaled + 1.5748 * v;
    let g = y_scaled - 0.1873 * u - 0.4681 * v;
    let b = y_scaled + 1.8556 * u;

    textureStore(output, id.xy, vec4f(clamp(r, 0.0, 1.0), clamp(g, 0.0, 1.0), clamp(b, 0.0, 1.0), 1.0));
}
```

## Multiple Compute Passes

Chain compute passes in a single command encoder -- no need to submit between passes (GPU handles dependencies via barriers):

```rust
let mut encoder = device.create_command_encoder(&Default::default());

// Pass 1: Horizontal blur
{
    let mut pass = encoder.begin_compute_pass(&Default::default());
    pass.set_pipeline(&h_blur_pipeline);
    pass.set_bind_group(0, &h_blur_bg, &[]);
    pass.dispatch_workgroups(dispatch_x, dispatch_y, 1);
}

// Pass 2: Vertical blur (reads output of pass 1)
{
    let mut pass = encoder.begin_compute_pass(&Default::default());
    pass.set_pipeline(&v_blur_pipeline);
    pass.set_bind_group(0, &v_blur_bg, &[]);
    pass.dispatch_workgroups(dispatch_x, dispatch_y, 1);
}

queue.submit(Some(encoder.finish()));
```

## Async Buffer Mapping (Non-Blocking)

For real-time applications, avoid `device.poll(PollType::Wait)`:

```rust
// Submit work
staging_buf.slice(..).map_async(wgpu::MapMode::Read, move |result| {
    if result.is_ok() {
        // Process data in callback (runs on poll thread)
    }
});

// Later, in your update loop:
device.poll(wgpu::PollType::Poll); // non-blocking check

// Or with maintain:
match device.poll(wgpu::PollType::Wait) {
    wgpu::PollStatus::QueueEmpty => { /* all work done */ }
    wgpu::PollStatus::SubmissionQueueEmpty => { /* queue empty, device work pending */ }
    _ => {}
}
```

## Indirect Dispatch

For data-driven compute where the GPU determines workgroup counts:

```wgsl
// Indirect dispatch buffer layout: [x: u32, y: u32, z: u32]
@group(0) @binding(0) var<storage, read_write> indirect: array<u32, 3>;

@compute @workgroup_size(1)
fn prepare_dispatch() {
    let count = /* calculate from data */;
    indirect[0] = (count + 63) / 64; // dispatch_x
    indirect[1] = 1;                  // dispatch_y
    indirect[2] = 1;                  // dispatch_z
}
```

```rust
// Buffer for indirect dispatch args
let indirect_buf = device.create_buffer(&wgpu::BufferDescriptor {
    label: Some("Indirect"),
    size: 12, // 3 * u32
    usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::INDIRECT,
    mapped_at_creation: false,
});

// Dispatch indirectly
pass.dispatch_workgroups_indirect(&indirect_buf, 0);
```
