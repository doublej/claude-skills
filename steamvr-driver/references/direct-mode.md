# IVRDriverDirectModeComponent

Direct mode bypasses the SteamVR compositor. The driver manages texture creation, layer compositing, and frame presentation. Windows-only in practice (requires D3D11 shared textures).

## When to Use

- Streaming drivers (like ALVR) that encode and transmit frames
- Drivers that do their own compositing/distortion
- Drivers where compositor overhead is unacceptable

## Interface

Return from `GetComponent()` when asked for `IVRDriverDirectModeComponent_Version`:

```cpp
void* GetComponent(const char* name) override {
    if (std::string(name) == vr::IVRDriverDirectModeComponent_Version)
        return m_directModeComponent.get();
    return nullptr;
}
```

## Key Methods

### CreateSwapTextureSet

SteamVR calls this to allocate textures for rendering. You create D3D11 textures and return shared handles.

```cpp
void CreateSwapTextureSet(
    uint32_t pid,
    const SwapTextureSetDesc_t* desc,
    SwapTextureSet_t* outSet
) {
    D3D11_TEXTURE2D_DESC texDesc = {};
    texDesc.Width = desc->nWidth;
    texDesc.Height = desc->nHeight;
    texDesc.Format = (DXGI_FORMAT)desc->nFormat;
    texDesc.MipLevels = 1;
    texDesc.ArraySize = 1;
    texDesc.SampleDesc.Count = std::max(1u, (uint32_t)desc->nSampleCount);
    texDesc.Usage = D3D11_USAGE_DEFAULT;
    texDesc.BindFlags = D3D11_BIND_SHADER_RESOURCE | D3D11_BIND_RENDER_TARGET;
    texDesc.MiscFlags = D3D11_RESOURCE_MISC_SHARED;

    // Handle depth formats
    if (format == DXGI_FORMAT_R32G8X24_TYPELESS || format == DXGI_FORMAT_R32_TYPELESS)
        texDesc.BindFlags = D3D11_BIND_DEPTH_STENCIL;

    // Create 3 textures for triple buffering
    for (int i = 0; i < 3; i++) {
        device->CreateTexture2D(&texDesc, nullptr, &textures[i]);
        // Get shared handle via IDXGIResource::GetSharedHandle
        outSet->rSharedTextureHandles[i] = (SharedTextureHandle_t)sharedHandle;
    }
}
```

**Pitfall:** Applications may request textures larger than `GetRecommendedRenderTargetSize`. Always use the requested size to avoid cropped output.

### DestroySwapTextureSet / DestroyAllSwapTextureSets

Clean up textures. Track by shared handle and PID.

### GetNextSwapTextureSetIndex

Returns which texture index to render to next:

```cpp
void GetNextSwapTextureSetIndex(
    SharedTextureHandle_t handles[2],
    uint32_t (*indices)[2]
) {
    (*indices)[0] = next_index_for(handles[0]);
    (*indices)[1] = next_index_for(handles[1]);
}
```

### SubmitLayer

Called once per composition layer per frame. Store layers for compositing in `Present`:

```cpp
void SubmitLayer(const SubmitLayerPerEye_t (&perEye)[2]) {
    if (m_submitLayer < MAX_LAYERS) {
        m_submitLayers[m_submitLayer][0] = perEye[0];
        m_submitLayers[m_submitLayer][1] = perEye[1];
        m_submitLayer++;
    }
}
```

`SubmitLayerPerEye_t` contains:
- `hTexture` -- shared texture handle
- `bounds` -- UV bounds within texture
- `mHmdPose` -- pose at render time (for reprojection)

### Present

Called after all layers are submitted. Copy/composite textures and kick off encoding:

```cpp
void Present(SharedTextureHandle_t syncTexture) {
    std::lock_guard lock(m_presentMutex);
    CopyTexture(m_submitLayer);  // composite layers -> encoder input
    m_submitLayer = 0;           // reset for next frame
}
```

### PostPresent

Called after `Present`. Use for frame pacing / vsync wait:

```cpp
void PostPresent() {
    WaitForVSync();
}
```

## ALVR Direct Mode Flow

```
SteamVR app renders -> SubmitLayer (per eye, per layer)
                    -> Present
                       |-> Copy shared textures to encoder input
                       |-> Encode frame (NVENC/AMF/VAAPI)
                       |-> Transmit to client
                    -> PostPresent
                       |-> Wait for next vsync
```

## Properties for Direct Mode

```cpp
// Set on HMD device
props->SetBoolProperty(container, Prop_HasDriverDirectModeComponent_Bool, true);

// Whether the driver generates vsync events (vs SteamVR)
props->SetBoolProperty(container, Prop_DriverDirectModeSendsVsyncEvents_Bool, false);
```

## Pose History

ALVR keeps a `PoseHistory` to match submitted frames with the pose used for rendering:

```cpp
class PoseHistory {
    // Store pose at submission time
    void OnPoseUpdated(uint64_t timestampNs, DeviceMotion motion);

    // Look up pose for a given frame timestamp
    DeviceMotion GetPoseAt(uint64_t timestampNs);
};
```

This enables accurate reprojection on the client side by correlating each encoded frame with its tracking data.

## Linux Alternative

On Linux, direct mode is not used. Instead:
- `IsDisplayRealDisplay()` returns `true`
- SteamVR compositor handles frame presentation
- Encoding happens via separate encoder thread that captures from compositor output
- Async reprojection can be controlled via VRSettings:

```cpp
vr::VRSettings()->SetBool(k_pch_SteamVR_Section,
    k_pch_SteamVR_DisableAsyncReprojection_Bool, true);
vr::VRSettings()->SetBool(k_pch_SteamVR_Section,
    k_pch_SteamVR_EnableLinuxVulkanAsync_Bool, false);
```
