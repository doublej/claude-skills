---
name: openxr-dev
description: "Runtime/layer implementation, extension authoring, Vulkan bindings, openxrs"
---

# OpenXR Development

<before_writing>

## Before Writing Code

1. **Identify the role** -- runtime, API layer, application, or extension:
   - Runtime: implements the OpenXR API for specific hardware
   - API layer: intercepts calls between app and runtime (validation, overlay, metrics)
   - Application: consumes the API to render VR/AR content
   - Extension: adds new functionality to any of the above

2. **Check spec version**: OpenXR 1.0 vs 1.1 (1.1 promoted several extensions to core)

3. **Detect graphics API**: Vulkan (`XR_KHR_vulkan_enable2`), OpenGL (`XR_KHR_opengl_enable`), OpenGL ES (`XR_KHR_opengl_es_enable`), D3D11/D3D12

4. **If Rust**: check `openxrs` crate version and available extension bindings

</before_writing>

<object_hierarchy>

## Core Object Hierarchy

```
Entry -> Instance -> System -> Session -> {Swapchain, Space, ActionSet}
                                    |
                              FrameWaiter + FrameStream
```

| Object | Created By | Lifetime | Notes |
|--------|-----------|----------|-------|
| `XrInstance` | `xrCreateInstance` | App lifetime | One per process typically |
| `XrSystemId` | `xrGetSystem` | Transient ID | Re-query after instance loss |
| `XrSession` | `xrCreateSession` | Until loss/exit | Owns GPU binding |
| `XrSwapchain` | `xrCreateSwapchain` | Session | Runtime allocates images |
| `XrSpace` | `xrCreateReferenceSpace` / `xrCreateActionSpace` | Session | Tracking origin |
| `XrActionSet` | `xrCreateActionSet` | Instance | Attach to session once |

</object_hierarchy>

<session_lifecycle>

```
            xrCreateSession
                  |
                  v
    IDLE --> READY --> SYNCHRONIZED --> VISIBLE --> FOCUSED
              |                                       |
              |         xrEndSession                  |
    STOPPING <-------- (any running) <--- LOSS_PENDING
        |
        v
      EXITING
```

**Critical rules:**
- Call `xrBeginSession` only when state becomes `READY`
- Call `xrEndSession` only when state becomes `STOPPING`
- Poll `xrPollEvent` every iteration, not just once
- `SYNCHRONIZED`: submit frames but `shouldRender` is false -- submit empty layers
- `VISIBLE`: render but no input focus
- `FOCUSED`: full rendering + input

```c
// State machine pattern (C)
case XR_SESSION_STATE_READY:
    XrSessionBeginInfo beginInfo = {XR_TYPE_SESSION_BEGIN_INFO};
    beginInfo.primaryViewConfigurationType = XR_VIEW_CONFIGURATION_TYPE_PRIMARY_STEREO;
    xrBeginSession(session, &beginInfo);
    sessionRunning = true;
    break;
case XR_SESSION_STATE_STOPPING:
    sessionRunning = false;
    xrEndSession(session);
    break;
```

</session_lifecycle>

<frame_loop>

```
xrWaitFrame -> xrBeginFrame -> [render] -> xrEndFrame
```

| Function | Blocks? | Purpose |
|----------|---------|---------|
| `xrWaitFrame` | Yes | Paces app to display refresh, returns predicted display time |
| `xrBeginFrame` | No | Marks start of GPU work for this frame |
| `xrEndFrame` | May block | Submits composition layers to runtime |

**Rules:**
- Always call `xrBeginFrame` after `xrWaitFrame`, even if `shouldRender` is false
- If `shouldRender` is false, call `xrEndFrame` with zero layers
- Never skip `xrEndFrame` -- the runtime expects paired begin/end
- Use `predictedDisplayTime` for all pose queries (not wall clock)
- `predictedDisplayPeriod` gives frame interval for motion extrapolation

```c
// Minimal frame loop
XrFrameState frameState = {XR_TYPE_FRAME_STATE};
xrWaitFrame(session, NULL, &frameState);
xrBeginFrame(session, NULL);

if (!frameState.shouldRender) {
    XrFrameEndInfo endInfo = {XR_TYPE_FRAME_END_INFO};
    endInfo.displayTime = frameState.predictedDisplayTime;
    endInfo.environmentBlendMode = XR_ENVIRONMENT_BLEND_MODE_OPAQUE;
    xrEndFrame(session, &endInfo);
    continue;
}

// Locate views, render, submit layers...
```

</frame_loop>

<swapchain>

**Format negotiation** -- the runtime lists supported formats, app picks one:

```c
uint32_t count;
xrEnumerateSwapchainFormats(session, 0, &count, NULL);
int64_t *formats = malloc(count * sizeof(int64_t));
xrEnumerateSwapchainFormats(session, count, &count, formats);
// Pick preferred format from the list -- DON'T assume any format exists
```

</swapchain>

<format_preference>

| Preference | Vulkan | OpenGL | Use |
|-----------|--------|--------|-----|
| SDR | `VK_FORMAT_R8G8B8A8_SRGB` | `GL_SRGB8_ALPHA8` | Default, widest support |
| HDR | `VK_FORMAT_R16G16B16A16_SFLOAT` | `GL_RGBA16F` | HDR passthrough/content |
| Linear | `VK_FORMAT_R8G8B8A8_UNORM` | `GL_RGBA8` | When doing own gamma |

</format_preference>

<acquire_wait_release>

**Acquire/wait/release cycle:**

```c
uint32_t index;
xrAcquireSwapchainImage(swapchain, NULL, &index);

XrSwapchainImageWaitInfo waitInfo = {XR_TYPE_SWAPCHAIN_IMAGE_WAIT_INFO};
waitInfo.timeout = XR_INFINITE_DURATION;
xrWaitSwapchainImage(swapchain, &waitInfo);

// Render to images[index]

xrReleaseSwapchainImage(swapchain, NULL);
```

**Pitfall:** You MUST release before calling `xrEndFrame`. Unreleased swapchain images cause runtime errors or hangs.

</acquire_wait_release>

<stereo>

**Stereo rendering options:**
- Two swapchains (one per eye) -- simpler, ALVR pattern
- One swapchain with `arraySize=2` -- single framebuffer, multi-view rendering
- One wide swapchain, two viewports -- sideby-side

</stereo>

<reference_spaces>

| Type | Origin | Use |
|------|--------|-----|
| `VIEW` | Head-locked | HUDs, reticles |
| `LOCAL` | Seated, arbitrary initial | Seated experiences |
| `LOCAL_FLOOR` | Floor-level, arbitrary initial | Standing without boundaries (1.1 core, was `EXT_local_floor`) |
| `STAGE` | Room center, floor level | Room-scale with boundaries |
| `UNBOUNDED_MSFT` | Large-scale tracking | Arena, outdoor |

**Pitfall:** `STAGE` may not be available on all runtimes. Fall back to `LOCAL_FLOOR` or `LOCAL` + height offset.

Handle `XrEventDataReferenceSpaceChangePending` -- recenter your tracking origin.

</reference_spaces>

<action_system>

```
ActionSet -> Action -> SuggestedBinding -> InteractionProfile
                |
          ActionSpace (for pose actions)
```

**Setup order:**
1. Create action sets and actions at instance level
2. Suggest bindings for each interaction profile
3. Attach action sets to session (`xrAttachSessionActionSets`) -- **one-time, irreversible**
4. Each frame: `xrSyncActions` then query states

```c
// Suggest bindings
XrPath profilePath;
xrStringToPath(instance, "/interaction_profiles/oculus/touch_controller", &profilePath);

XrActionSuggestedBinding bindings[] = {
    {gripAction, triggerPath},      // /user/hand/left/input/trigger/value
    {poseAction, gripPosePath},     // /user/hand/left/input/grip/pose
};

XrInteractionProfileSuggestedBinding suggestion = {XR_TYPE_INTERACTION_PROFILE_SUGGESTED_BINDING};
suggestion.interactionProfile = profilePath;
suggestion.suggestedBindings = bindings;
suggestion.countSuggestedBindings = 2;
xrSuggestInteractionProfileBindings(instance, &suggestion);
```

</action_system>

<interaction_profiles>

**Common interaction profiles:**

| Profile Path | Controllers |
|-------------|-------------|
| `/interaction_profiles/khr/simple_controller` | Minimum viable (select + pose) |
| `/interaction_profiles/oculus/touch_controller` | Quest/Rift |
| `/interaction_profiles/valve/index_controller` | Index |
| `/interaction_profiles/htc/vive_controller` | Vive |
| `/interaction_profiles/bytedance/pico_neo3_controller` | Pico Neo 3 |
| `/interaction_profiles/bytedance/pico4_controller` | Pico 4 |

</interaction_profiles>

<composition_layers>

Submitted via `xrEndFrame`. Order matters -- first layer is rendered bottommost.

| Layer Type | Use |
|-----------|-----|
| `XrCompositionLayerProjection` | Primary stereo rendered content |
| `XrCompositionLayerQuad` | Floating panels, UI overlays |
| `XrCompositionLayerCylinder` | Curved displays, panoramic UI |
| `XrCompositionLayerEquirect` | 360 photo/video |
| `XrCompositionLayerPassthroughFB` | Camera passthrough (FB extension) |

**Projection layer** requires per-eye `XrCompositionLayerProjectionView` with:
- `pose` and `fov` from `xrLocateViews`
- `subImage` pointing to swapchain + rect

**Layer flags:**
- `XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT` -- enable alpha blending
- `XR_COMPOSITION_LAYER_UNPREMULTIPLIED_ALPHA_BIT` -- if alpha is not premultiplied

</composition_layers>

<pose_timing>

## Pose Prediction & Timing

```c
XrSpaceLocation location = {XR_TYPE_SPACE_LOCATION};
xrLocateSpace(handSpace, referenceSpace, predictedDisplayTime, &location);

if (location.locationFlags & XR_SPACE_LOCATION_POSITION_VALID_BIT) {
    // Use location.pose
}
```

**Always check flags** before using pose data:
- `POSITION_VALID_BIT` / `ORIENTATION_VALID_BIT` -- data is usable
- `POSITION_TRACKED_BIT` / `ORIENTATION_TRACKED_BIT` -- actively tracked (vs estimated)

**Motion-to-photon latency** = time from physical motion to photons hitting display. Lower is better. The runtime handles reprojection/timewarp, but the app must:
1. Use `predictedDisplayTime` for all `xrLocateSpace` / `xrLocateViews` calls
2. Minimize GPU work between pose query and frame submission
3. Consider late-latching for critical poses (query as late as possible)

</pose_timing>

<graphics_binding>

## Graphics Binding Setup

### Vulkan

```c
// Before creating session, call these (mandatory even if you ignore results):
xrGetVulkanGraphicsRequirements2KHR(instance, systemId, &requirements);
xrGetVulkanInstanceExtensionsKHR(...);  // required VK instance extensions
xrGetVulkanDeviceExtensionsKHR(...);    // required VK device extensions
xrGetVulkanGraphicsDevice2KHR(...);     // which VkPhysicalDevice to use

XrGraphicsBindingVulkan2KHR binding = {XR_TYPE_GRAPHICS_BINDING_VULKAN2_KHR};
binding.instance = vkInstance;
binding.physicalDevice = physicalDevice;  // MUST match what runtime returned
binding.device = device;
binding.queueFamilyIndex = graphicsQueueFamily;
binding.queueIndex = 0;

XrSessionCreateInfo sessionInfo = {XR_TYPE_SESSION_CREATE_INFO};
sessionInfo.next = &binding;
sessionInfo.systemId = systemId;
```

</graphics_binding>

<opengles>

### OpenGL ES (Android pattern from ALVR)

```rust
// openxrs crate
let (session, frame_waiter, frame_stream) = unsafe {
    instance.create_session(system, &xr::opengles::SessionCreateInfo::Android {
        display: egl_display.as_ptr(),
        config: egl_config.as_ptr(),
        context: egl_context.as_ptr(),
    })?
};
```

</opengles>

<extensions>

## Extension Authoring

See `references/extensions.md` for:
- Extension naming conventions (vendor tags: EXT, KHR, FB, HTC, BD, MSFT)
- Struct chaining with `next` pointers
- Function pointer loading via `xrGetInstanceProcAddr`
- ALVR's `extra_extensions` patterns for wrapping raw FFI

</extensions>

<openxrs_crate>

## openxrs Crate (Rust)

The `openxrs` crate by Ralith wraps the OpenXR C API with safe Rust types.

**Key type mappings:**

| C API | openxrs | Notes |
|-------|---------|-------|
| `XrInstance` | `xr::Instance` | Ref-counted |
| `XrSession` | `xr::Session<G>` | Generic over graphics API (`Vulkan`, `OpenGlEs`) |
| `XrSwapchain` | `xr::Swapchain<G>` | |
| `XrSpace` | `xr::Space` | |
| `XrAction<T>` | `xr::Action<T>` | `T`: `bool`, `f32`, `xr::Posef`, `xr::Haptic` |
| `XrPath` | `xr::Path` | Interned string, `xr::Path::NULL` for empty |
| `XrTime` | `xr::Time` | Nanoseconds via `.as_nanos()` / `from_nanos()` |
| `XrDuration` | `xr::Duration` | `XR_INFINITE_DURATION` = `xr::Duration::INFINITE` |

**Extension function loading** (for extensions not in openxrs):

```rust
// Load a function pointer not yet wrapped by openxrs
fn get_instance_proc<FnTy>(session: &xr::Session<G>, name: &str) -> xr::Result<FnTy> {
    unsafe {
        let name = CString::new(name).unwrap();
        let mut pfn = None;
        xr_res((session.instance().fp().get_instance_proc_addr)(
            session.instance().as_raw(),
            name.as_ptr(),
            &mut pfn,
        ))?;
        pfn.map(|f| mem::transmute_copy(&f))
           .ok_or(sys::Result::ERROR_EXTENSION_NOT_PRESENT)
    }
}
```

**Extension object wrapper pattern** (from ALVR):

```rust
pub struct FaceTracker2FB {
    _session: xr::Session<xr::AnyGraphics>,  // prevent session drop
    handle: sys::FaceTracker2FB,
    ext_fns: raw::FaceTracking2FB,            // loaded function pointers
}

impl Drop for FaceTracker2FB {
    fn drop(&mut self) {
        unsafe { (self.ext_fns.destroy_face_tracker2)(self.handle); }
    }
}
```

**Checking extension availability:**

```rust
let available = entry.enumerate_extensions()?;
let mut exts = xr::ExtensionSet::default();
exts.fb_passthrough = available.fb_passthrough;
exts.ext_hand_tracking = available.ext_hand_tracking;
// Extensions NOT in ExtensionSet go in exts.other: Vec<String>
exts.other = available.other.into_iter()
    .filter(|e| WANTED_EXTENSIONS.contains(&e.as_str()))
    .collect();
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Assuming swapchain format exists | Always enumerate and pick from available list |
| Using wall clock for poses | Use `predictedDisplayTime` from `xrWaitFrame` |
| Forgetting `xrBeginFrame`/`xrEndFrame` pairing | Always pair, even when not rendering |
| Not checking `shouldRender` | Submit empty layers when false |
| Not polling events | Poll every frame iteration, handle all events |
| Calling `xrBeginSession` at wrong state | Only on `READY` state transition |
| Not handling `InstanceLossPending` | Break session loop, may need full re-init |
| Unreleased swapchain image | Always release before `xrEndFrame` |
| Attaching action sets twice | `xrAttachSessionActionSets` is one-shot per session |
| `STAGE` space unavailable | Fall back to `LOCAL_FLOOR` or `LOCAL` + offset |
| Not calling `graphics_requirements` | Mandatory before `xrCreateSession`, even if unused |
| Submitting stale display time | Runtime may reject frames with wrong timestamps |

</pitfalls>

<loader_architecture>

```
Application -> OpenXR Loader -> [API Layers] -> Runtime
```

- **Loader**: discovers runtime and layers, dispatches calls
- **API layers**: intercept calls (validation, overlay, recording)
- **Runtime**: hardware-specific implementation
- Android: loader is a shared library (`libopenxr_loader.so`), may have vendor variants
- Desktop: loader reads `XR_RUNTIME_JSON` env var or system registry

</loader_architecture>

<deep_reference>

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `extensions.md` | Authoring extensions, struct chaining, FB/HTC/BD extensions, passthrough |
| `session-lifecycle.md` | Session state machine details, error recovery, multi-session patterns |

</deep_reference>

<alvr_context>

## ALVR Integration Context

ALVR's `client_openxr` crate at `rust/alvr/repo/alvr/client_openxr/` demonstrates:
- Full session lifecycle with lobby/stream dual-mode rendering
- OpenGL ES graphics binding on Android
- Extension wrapping in `extra_extensions/` (face tracking, body tracking, passthrough)
- Platform-specific loader selection (Quest, Pico, YVR, Lynx)
- Swapchain format negotiation via `alvr_graphics::choose_swapchain_format`
- Projection layer building with alpha config
- Haptic feedback via action system
- Reference space change handling

</alvr_context>
