# OpenXR Extension Authoring & Reference

## Vendor Tags

| Tag | Vendor | Common Extensions |
|-----|--------|-------------------|
| `KHR` | Khronos ratified | Vulkan/GL bindings, visibility mask, composition layer types |
| `EXT` | Multi-vendor | Hand tracking, local floor, eye gaze, HP mixed reality |
| `FB` / `META` | Meta | Passthrough, foveation, face/body/eye tracking, display refresh rate, color space |
| `HTC` | HTC | Vive trackers, facial tracking, passthrough |
| `MSFT` | Microsoft | Spatial anchors, hand mesh, scene understanding, unbounded space |
| `BD` | ByteDance | Pico body tracking, motion tracking |
| `VARJO` | Varjo | Quad views (foveated), environment depth |
| `ULTRALEAP` | Ultraleap | Hand tracking (Leap Motion) |

## Extension Naming Convention

```
XR_{VENDOR}_{feature_name}
```

- Types: `Xr{FeatureName}{VENDOR}` -- e.g. `XrFaceTracker2FB`
- Functions: `xr{VerbNoun}{VENDOR}` -- e.g. `xrCreateFaceTracker2FB`
- Enums: `XR_{FEATURE}_{VALUE}_{VENDOR}` -- e.g. `XR_FACE_EXPRESSION_SET_DEFAULT_FB`
- Struct types: `XR_TYPE_{STRUCT_NAME}_{VENDOR}`

## Struct Chaining (next pointers)

OpenXR uses a singly-linked list via `next` pointers for extensibility. Every struct starts with:

```c
typedef struct XrBaseHeader {
    XrStructureType type;
    void*           next;
};
```

**Input structs** (app -> runtime): `const void* next`
**Output structs** (runtime -> app): `void* next` (runtime writes into pre-allocated chain)

```c
// Chaining example: add foveation to swapchain creation
XrSwapchainCreateInfoFoveationFB foveationInfo = {
    .type = XR_TYPE_SWAPCHAIN_CREATE_INFO_FOVEATION_FB,
    .next = NULL,
    .flags = 0,
};

XrSwapchainCreateInfo swapchainInfo = {
    .type = XR_TYPE_SWAPCHAIN_CREATE_INFO,
    .next = &foveationInfo,  // chain extends the base struct
    // ... other fields
};
```

**Rules:**
- `type` must match the struct -- runtime uses it to walk the chain
- Chain order doesn't matter for input; for output, pre-allocate all structs
- Never chain the same struct type twice in one chain
- Null-terminate with `next = NULL`

## Function Pointer Loading

Extensions not in the core spec must be loaded via `xrGetInstanceProcAddr`:

```c
PFN_xrCreateFaceTracker2FB xrCreateFaceTracker2FB;
xrGetInstanceProcAddr(instance, "xrCreateFaceTracker2FB",
    (PFN_xrVoidFunction*)&xrCreateFaceTracker2FB);
```

**In Rust (openxrs):**

```rust
// If the extension IS in openxrs:
let ext_fns = session.instance().exts().fb_face_tracking2
    .ok_or(sys::Result::ERROR_EXTENSION_NOT_PRESENT)?;

// If NOT in openxrs, load manually:
let pfn: PFN_xrSomeNewFunction = {
    let name = CString::new("xrSomeNewFunction").unwrap();
    let mut f = None;
    (instance.fp().get_instance_proc_addr)(instance.as_raw(), name.as_ptr(), &mut f);
    mem::transmute_copy(&f.unwrap())
};
```

## System Properties Query Pattern

Check if hardware supports an extension feature at the system level:

```c
XrSystemFaceTrackingProperties2FB faceProps = {
    .type = XR_TYPE_SYSTEM_FACE_TRACKING_PROPERTIES2_FB,
    .next = NULL,
};
XrSystemProperties systemProps = {
    .type = XR_TYPE_SYSTEM_PROPERTIES,
    .next = &faceProps,  // chain to get extension properties
};
xrGetSystemProperties(instance, systemId, &systemProps);

if (faceProps.supportsVisualFaceTracking) { /* ... */ }
```

**Rust pattern (from ALVR):**

```rust
fn get_props<G, T>(session: &xr::Session<G>, system: xr::SystemId, default: T) -> xr::Result<T> {
    let instance = session.instance();
    let mut props = default;
    let mut system_properties = sys::SystemProperties::out((&mut props as *mut T).cast());
    unsafe {
        (instance.fp().get_system_properties)(
            instance.as_raw(), system, system_properties.as_mut_ptr(),
        )
    };
    Ok(props)
}
```

## Common Extension Patterns

### FB Passthrough

Enables camera passthrough as a composition layer.

```
xrCreatePassthroughFB -> xrCreatePassthroughLayerFB -> submit as CompositionLayerPassthroughFB
```

- Create with `XR_PASSTHROUGH_IS_RUNNING_AT_CREATION_BIT_FB` to auto-start
- Layer purpose: `RECONSTRUCTION` (full environment) or `PROJECTED` (mesh-mapped)
- Submit BEFORE projection layer (passthrough renders behind content)
- Some runtimes (YVR) ignore `IS_RUNNING_AT_CREATION` -- call `xrPassthroughStartFB` explicitly

### FB Display Refresh Rate

```c
uint32_t count;
xrEnumerateDisplayRefreshRatesFB(session, 0, &count, NULL);
float *rates = malloc(count * sizeof(float));
xrEnumerateDisplayRefreshRatesFB(session, count, &count, rates);
xrRequestDisplayRefreshRateFB(session, 90.0f);
```

### EXT Hand Tracking

```c
XrHandTrackerEXT tracker;
XrHandTrackerCreateInfoEXT createInfo = {XR_TYPE_HAND_TRACKER_CREATE_INFO_EXT};
createInfo.hand = XR_HAND_LEFT_EXT;
createInfo.handJointSet = XR_HAND_JOINT_SET_DEFAULT_EXT;
xrCreateHandTrackerEXT(session, &createInfo, &tracker);

// Per frame:
XrHandJointLocationEXT joints[XR_HAND_JOINT_COUNT_EXT];
XrHandJointLocationsEXT locations = {XR_TYPE_HAND_JOINT_LOCATIONS_EXT};
locations.jointCount = XR_HAND_JOINT_COUNT_EXT;
locations.jointLocations = joints;

XrHandJointsLocateInfoEXT locateInfo = {XR_TYPE_HAND_JOINTS_LOCATE_INFO_EXT};
locateInfo.baseSpace = referenceSpace;
locateInfo.time = predictedDisplayTime;
xrLocateHandJointsEXT(tracker, &locateInfo, &locations);
```

26 joints per hand, arranged in a skeleton hierarchy. Always check `isActive` and per-joint `locationFlags`.

### FB Face Tracking 2

```rust
// ALVR pattern -- create tracker
let tracker = FaceTracker2FB::new(session.clone(), visual: true, audio: true)?;

// Per frame -- get 70 blend shape weights
let weights: Option<Vec<f32>> = tracker.get_face_expression_weights(predicted_time)?;
```

63 expression weights mapping to ARKit-compatible blend shapes plus extras.

### FB Body Tracking / Meta Full Body

- `XR_FB_body_tracking`: upper body (hip to head + arms), 70 joints
- `XR_META_body_tracking_full_body`: adds legs, 84 joints
- `XR_BD_body_tracking`: ByteDance/Pico variant with different joint set

### FB Foveation

Fixed foveation rendering -- reduces resolution at periphery:

```c
XrFoveationProfileCreateInfoFB profileInfo = {XR_TYPE_FOVEATION_PROFILE_CREATE_INFO_FB};
XrFoveationLevelProfileCreateInfoFB levelInfo = {XR_TYPE_FOVEATION_LEVEL_PROFILE_CREATE_INFO_FB};
levelInfo.level = XR_FOVEATION_LEVEL_HIGH_FB;
levelInfo.verticalOffset = 0.0f;
levelInfo.dynamic = XR_FOVEATION_DYNAMIC_LEVEL_ENABLED_FB;
profileInfo.next = &levelInfo;

XrFoveationProfileFB profile;
xrCreateFoveationProfileFB(session, &profileInfo, &profile);

// Apply to swapchain via XR_FB_swapchain_update_state
```

### HTC Passthrough / Facial Tracking

- `XR_HTC_passthrough`: alternative to FB, different API surface
- `XR_HTC_facial_tracking`: lip and eye expressions, different blend shape set than FB

## Extension Object Lifecycle

Every `xrCreate*` must have a matching `xrDestroy*`. In Rust, implement `Drop`:

```rust
impl Drop for MyExtensionObject {
    fn drop(&mut self) {
        unsafe { (self.ext_fns.destroy_my_object)(self.handle); }
    }
}
```

**Keep a reference to the session** in your wrapper to prevent use-after-free:

```rust
pub struct MyTracker {
    _session: xr::Session<xr::AnyGraphics>,  // prevent drop
    handle: sys::MyTrackerEXT,
    ext_fns: raw::MyExtensionEXT,
}
```

## Writing a New Extension Wrapper (Rust/openxrs)

1. Define the raw sys types if not in openxrs (or use `openxr::sys` if available)
2. Load function pointers via `get_instance_proc`
3. Create a safe wrapper struct holding handle + fn pointers + session ref
4. Implement `new()` that checks extension availability and creates the object
5. Add query methods that call the extension functions
6. Implement `Drop` for cleanup
7. Handle `ERROR_FEATURE_UNSUPPORTED` and `ERROR_EXTENSION_NOT_PRESENT` gracefully

```rust
fn create_ext_object<T>(
    name: &str,
    enabled: Option<bool>,
    create_cb: impl FnOnce() -> xr::Result<T>,
) -> Option<T> {
    enabled.unwrap_or(false).then(|| match create_cb() {
        Ok(obj) => Some(obj),
        Err(sys::Result::ERROR_FEATURE_UNSUPPORTED) => None,
        Err(sys::Result::ERROR_EXTENSION_NOT_PRESENT) => None,
        Err(e) => { warn!("Failed to create {name}: {e}"); None }
    }).flatten()
}
```
