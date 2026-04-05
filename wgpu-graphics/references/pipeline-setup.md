# Render Pipeline Setup

## Vertex Buffer Layouts

### Interleaved (position + UV + normal)

```rust
const VERTEX_LAYOUT: wgpu::VertexBufferLayout = wgpu::VertexBufferLayout {
    array_stride: 32, // 3 + 2 + 3 floats = 8 * 4 bytes
    step_mode: wgpu::VertexStepMode::Vertex,
    attributes: &[
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x3, offset: 0, shader_location: 0 },  // position
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x2, offset: 12, shader_location: 1 }, // uv
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x3, offset: 20, shader_location: 2 }, // normal
    ],
};
```

### Vertex-Less Fullscreen Quad

No vertex buffer needed. Generate UVs from `vertex_index`:

```wgsl
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> VertexOutput {
    var out: VertexOutput;
    // TriangleStrip with 4 vertices covers the screen
    out.uv = vec2f(f32(idx & 1), f32(idx >> 1));
    out.position = vec4f(out.uv * 2.0 - 1.0, 0.0, 1.0);
    return out;
}
```

```rust
// Pipeline: topology = TriangleStrip, buffers = &[]
// Draw: render_pass.draw(0..4, 0..1);
```

### Instance Data

```rust
const INSTANCE_LAYOUT: wgpu::VertexBufferLayout = wgpu::VertexBufferLayout {
    array_stride: 64, // mat4x4f
    step_mode: wgpu::VertexStepMode::Instance,
    attributes: &[
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x4, offset: 0, shader_location: 3 },
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x4, offset: 16, shader_location: 4 },
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x4, offset: 32, shader_location: 5 },
        wgpu::VertexAttribute { format: wgpu::VertexFormat::Float32x4, offset: 48, shader_location: 6 },
    ],
};
// Pipeline buffers: &[VERTEX_LAYOUT, INSTANCE_LAYOUT]
// Draw: render_pass.draw(0..vertex_count, 0..instance_count);
```

## Full Render Pipeline

```rust
let render_pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
    label: Some("Main Render Pipeline"),
    layout: Some(&pipeline_layout), // or None for auto-layout (no push constants)
    vertex: wgpu::VertexState {
        module: &shader,
        entry_point: Some("vs_main"),
        compilation_options: Default::default(),
        buffers: &[VERTEX_LAYOUT],
    },
    fragment: Some(wgpu::FragmentState {
        module: &shader,
        entry_point: Some("fs_main"),
        compilation_options: Default::default(),
        targets: &[Some(wgpu::ColorTargetState {
            format: surface_format,
            blend: Some(wgpu::BlendState::REPLACE),
            write_mask: wgpu::ColorWrites::ALL,
        })],
    }),
    primitive: wgpu::PrimitiveState {
        topology: wgpu::PrimitiveTopology::TriangleList,
        strip_index_format: None,
        front_face: wgpu::FrontFace::Ccw,
        cull_mode: Some(wgpu::Face::Back),
        polygon_mode: wgpu::PolygonMode::Fill,
        unclipped_depth: false,
        conservative: false,
    },
    depth_stencil: Some(wgpu::DepthStencilState {
        format: wgpu::TextureFormat::Depth32Float,
        depth_write_enabled: true,
        depth_compare: wgpu::CompareFunction::Less,
        stencil: wgpu::StencilState::default(),
        bias: wgpu::DepthBiasState::default(),
    }),
    multisample: wgpu::MultisampleState {
        count: 1,       // or 4 for MSAA
        mask: !0,
        alpha_to_coverage_enabled: false,
    },
    multiview: None,    // Some(NonZeroU32::new(2).unwrap()) for stereo
    cache: None,
});
```

## Blend States

| Preset | Constant | Use Case |
|--------|----------|----------|
| Replace | `BlendState::REPLACE` | Opaque geometry |
| Alpha blend | `BlendState::ALPHA_BLENDING` | Standard transparency |
| Premultiplied alpha | `BlendState::PREMULTIPLIED_ALPHA_BLENDING` | Compositing, VR layers |
| Additive | custom (src=One, dst=One) | Particles, glow |

### Custom Blend (ALVR lobby pattern)

```rust
blend: Some(wgpu::BlendState {
    color: wgpu::BlendComponent {
        src_factor: wgpu::BlendFactor::SrcAlpha,
        dst_factor: wgpu::BlendFactor::OneMinusSrcAlpha,
        operation: wgpu::BlendOperation::Add,
    },
    alpha: wgpu::BlendComponent {
        src_factor: wgpu::BlendFactor::One,
        dst_factor: wgpu::BlendFactor::OneMinusSrcAlpha,
        operation: wgpu::BlendOperation::Add,
    },
}),
```

## Depth/Stencil Configurations

### Depth-Only (most common)

```rust
depth_stencil: Some(wgpu::DepthStencilState {
    format: wgpu::TextureFormat::Depth32Float,
    depth_write_enabled: true,
    depth_compare: wgpu::CompareFunction::Less,
    stencil: wgpu::StencilState::default(),
    bias: wgpu::DepthBiasState::default(),
}),
```

### No Depth (2D/overlay rendering)

```rust
depth_stencil: None,
```

### Depth Read-Only (transparent pass)

```rust
depth_stencil: Some(wgpu::DepthStencilState {
    format: wgpu::TextureFormat::Depth32Float,
    depth_write_enabled: false, // read but don't write
    depth_compare: wgpu::CompareFunction::Less,
    stencil: wgpu::StencilState::default(),
    bias: wgpu::DepthBiasState::default(),
}),
```

## Render Pass Recording

```rust
let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor::default());
{
    let mut pass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
        label: Some("Main Pass"),
        color_attachments: &[Some(wgpu::RenderPassColorAttachment {
            view: &target_view,
            resolve_target: None, // Some(&resolve_view) for MSAA
            ops: wgpu::Operations {
                load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
                store: wgpu::StoreOp::Store,
            },
        })],
        depth_stencil_attachment: Some(wgpu::RenderPassDepthStencilAttachment {
            view: &depth_view,
            depth_ops: Some(wgpu::Operations {
                load: wgpu::LoadOp::Clear(1.0),
                store: wgpu::StoreOp::Store,
            }),
            stencil_ops: None,
        }),
        ..Default::default()
    });

    pass.set_pipeline(&render_pipeline);
    pass.set_bind_group(0, &bind_group, &[]);
    pass.set_vertex_buffer(0, vertex_buf.slice(..));
    pass.set_index_buffer(index_buf.slice(..), wgpu::IndexFormat::Uint16);
    pass.draw_indexed(0..index_count, 0, 0..1);
}
queue.submit(std::iter::once(encoder.finish()));
```

## Push Constants Layout

Push constants require explicit pipeline layout (auto-layout does not infer them).

```rust
let pipeline_layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
    label: None,
    bind_group_layouts: &[&bind_group_layout],
    push_constant_ranges: &[wgpu::PushConstantRange {
        stages: wgpu::ShaderStages::VERTEX_FRAGMENT,
        range: 0..128, // max typically 128 bytes
    }],
});
```

Alignment rules for push constant data:
- Each `set_push_constants` call offset must be 4-byte aligned
- Total range per stage limited by `max_push_constant_size` (check adapter limits)
- On Metal, push constants are emulated via argument buffers (no hard 128B limit)
- On Vulkan, 128 bytes guaranteed, some GPUs support 256+

## Bind Group Layout Patterns

### Texture + Sampler (most common)

```rust
let layout = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
    label: None,
    entries: &[
        wgpu::BindGroupLayoutEntry {
            binding: 0,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Texture {
                sample_type: wgpu::TextureSampleType::Float { filterable: true },
                view_dimension: wgpu::TextureViewDimension::D2,
                multisampled: false,
            },
            count: None,
        },
        wgpu::BindGroupLayoutEntry {
            binding: 1,
            visibility: wgpu::ShaderStages::FRAGMENT,
            ty: wgpu::BindingType::Sampler(wgpu::SamplerBindingType::Filtering),
            count: None,
        },
    ],
});
```

### Uniform Buffer

```rust
wgpu::BindGroupLayoutEntry {
    binding: 0,
    visibility: wgpu::ShaderStages::VERTEX | wgpu::ShaderStages::FRAGMENT,
    ty: wgpu::BindingType::Buffer {
        ty: wgpu::BufferBindingType::Uniform,
        has_dynamic_offset: false,
        min_binding_size: NonZeroU64::new(64), // None for no validation
    },
    count: None,
},
```

### Storage Buffer (read-write)

```rust
wgpu::BindGroupLayoutEntry {
    binding: 0,
    visibility: wgpu::ShaderStages::COMPUTE,
    ty: wgpu::BindingType::Buffer {
        ty: wgpu::BufferBindingType::Storage { read_only: false },
        has_dynamic_offset: false,
        min_binding_size: None,
    },
    count: None,
},
```

### Storage Texture (write-only in compute)

```rust
wgpu::BindGroupLayoutEntry {
    binding: 0,
    visibility: wgpu::ShaderStages::COMPUTE,
    ty: wgpu::BindingType::StorageTexture {
        access: wgpu::StorageTextureAccess::WriteOnly,
        format: wgpu::TextureFormat::Rgba8Unorm,
        view_dimension: wgpu::TextureViewDimension::D2,
    },
    count: None,
},
```
