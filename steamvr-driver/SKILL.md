---
name: steamvr-driver
description: "OpenVR driver dev: device providers, HMD emulation, DriverPose_t, ALVR FFI"
---

# SteamVR Driver Development

<architecture_overview>

A SteamVR driver is a shared library loaded by `vrserver`. The entry point exports:

```cpp
// The ONLY export your driver needs
void* HmdDriverFactory(const char* interface_name, int* return_code);
```

vrserver calls this requesting `IServerTrackedDeviceProvider_Version`. Return your provider instance.

```
vrserver -> HmdDriverFactory -> IServerTrackedDeviceProvider
                                    |
                          Init() -> register devices via TrackedDeviceAdded()
                                    |
                          RunFrame() -> poll events, update state
                                    |
                          Cleanup() -> tear down
```

</architecture_overview>

<server_tracked_device_provider>

The driver's main lifecycle interface.

```cpp
class MyDriverProvider : public vr::IServerTrackedDeviceProvider {
    vr::EVRInitError Init(vr::IVRDriverContext* pContext) override {
        VR_INIT_SERVER_DRIVER_CONTEXT(pContext);  // MUST call first
        InitDriverLog(vr::VRDriverLog());

        // Create and register devices
        m_hmd = new MyHmd();
        vr::VRServerDriverHost()->TrackedDeviceAdded(
            "MY-HMD-SERIAL",
            vr::TrackedDeviceClass_HMD,
            m_hmd
        );
        return vr::VRInitError_None;
    }
    void Cleanup() override {
        CleanupDriverLog();
        VR_CLEANUP_SERVER_DRIVER_CONTEXT();  // MUST call last
    }
    void RunFrame() override {
        // Poll events, submit poses -- called every server frame
        vr::VREvent_t event;
        while (vr::VRServerDriverHost()->PollNextEvent(&event, sizeof(event))) {
            handle_event(event);
        }
    }
    const char* const* GetInterfaceVersions() override {
        return vr::k_InterfaceVersions;
    }
    bool ShouldBlockStandbyMode() override { return false; }
    void EnterStandby() override {}
    void LeaveStandby() override {}
};
```

**Critical:** `RunFrame()` runs on the server thread. Never block it. Heavy work goes on separate threads.

</server_tracked_device_provider>

<tracked_device_server_driver>

Every tracked device (HMD, controller, tracker) implements this.

```cpp
class MyDevice : public vr::ITrackedDeviceServerDriver {
    vr::TrackedDeviceIndex_t m_objectId = vr::k_unTrackedDeviceIndexInvalid;
    vr::PropertyContainerHandle_t m_propContainer = vr::k_ulInvalidPropertyContainer;

    vr::EVRInitError Activate(vr::TrackedDeviceIndex_t objectId) override {
        m_objectId = objectId;
        m_propContainer = vr::VRProperties()->TrackedDeviceToPropertyContainer(objectId);
        // Set properties, create input components here
        return vr::VRInitError_None;
    }
    void Deactivate() override {
        m_objectId = vr::k_unTrackedDeviceIndexInvalid;
    }
    void EnterStandby() override {}
    void* GetComponent(const char* componentNameAndVersion) override {
        // Return sub-interfaces (IVRDisplayComponent, IVRDriverDirectModeComponent)
        // MUST static_cast to correct vtable pointer
        if (std::string(componentNameAndVersion) == vr::IVRDisplayComponent_Version)
            return static_cast<vr::IVRDisplayComponent*>(this);
        return nullptr;
    }
    void DebugRequest(const char*, char* buf, uint32_t size) override {
        if (size >= 1) buf[0] = 0;
    }
    vr::DriverPose_t GetPose() override { return m_lastPose; }
};
```

**Pitfall:** `GetComponent` must use `static_cast` to the exact interface type when returning `this`. A plain cast produces wrong vtable pointers with multiple inheritance.

</tracked_device_server_driver>

<device_classes>

| Class | Enum | Use |
|-------|------|-----|
| HMD | `TrackedDeviceClass_HMD` | Head-mounted display |
| Controller | `TrackedDeviceClass_Controller` | Hand controllers |
| Generic Tracker | `TrackedDeviceClass_GenericTracker` | Body/object trackers (Vive Tracker emulation) |
| Tracking Reference | `TrackedDeviceClass_TrackingReference` | Base stations / cameras |

Register with `VRServerDriverHost()->TrackedDeviceAdded(serial, class, driver_ptr)`.
**Serial numbers must be unique** across all devices and persist across sessions.

</device_classes>

<pose_submission>



See `references/pose-and-timing.md` for `DriverPose_t` field reference, coordinate systems, timing, and prediction.

Core pattern:

```cpp
vr::DriverPose_t pose = {};
pose.poseIsValid = true;
pose.result = vr::TrackingResult_Running_OK;
pose.deviceIsConnected = true;
pose.qWorldFromDriverRotation = {1, 0, 0, 0};  // identity
pose.qDriverFromHeadRotation = {1, 0, 0, 0};   // identity
pose.qRotation = {w, x, y, z};
pose.vecPosition[0] = x; pose.vecPosition[1] = y; pose.vecPosition[2] = z;

vr::VRServerDriverHost()->TrackedDevicePoseUpdated(objectId, pose, sizeof(pose));
```

</pose_submission>

<device_properties>

Set in `Activate()` via `vr::VRProperties()`:

```cpp
auto props = vr::VRProperties();
props->SetStringProperty(container, vr::Prop_SerialNumber_String, "MY-SERIAL");
props->SetStringProperty(container, vr::Prop_ModelNumber_String, "My HMD");
props->SetStringProperty(container, vr::Prop_TrackingSystemName_String, "mydriver");
props->SetStringProperty(container, vr::Prop_ManufacturerName_String, "MyCompany");
props->SetStringProperty(container, vr::Prop_RenderModelName_String, "generic_hmd");
props->SetFloatProperty(container, vr::Prop_DisplayFrequency_Float, 90.0f);
props->SetFloatProperty(container, vr::Prop_UserIpdMeters_Float, 0.063f);
```

**Essential HMD properties:** `TrackingSystemName`, `ModelNumber`, `SerialNumber`, `ManufacturerName`, `RenderModelName`, `DisplayFrequency`, `UserIpdMeters`.

**Essential controller properties:** All HMD basics plus `ControllerType`, `InputProfilePath`, `ControllerRoleHint` (1=left, 2=right), `RegisteredDeviceType`.

See `references/device-properties.md` for full property reference and emulation profiles.

</device_properties>

<input_system>

See `references/input-system.md` for:
- Input component creation (boolean, scalar, haptic, skeleton)
- Controller profile JSON format
- SteamVR Input 2.0 (hand tracking)
- Button mapping patterns from ALVR
- Legacy vs new input API

</input_system>

<display_component>

Required for HMD devices. Describes display characteristics:

```cpp
class MyHmd : public ITrackedDeviceServerDriver, public vr::IVRDisplayComponent {
    void GetWindowBounds(int32_t* x, int32_t* y, uint32_t* w, uint32_t* h) override;
    bool IsDisplayOnDesktop() override { return false; }  // virtual display
    bool IsDisplayRealDisplay() override;  // true on Linux, false on Windows (direct mode)
    void GetRecommendedRenderTargetSize(uint32_t* w, uint32_t* h) override;
    void GetEyeOutputViewport(EVREye eye, uint32_t* x, uint32_t* y, uint32_t* w, uint32_t* h) override;
    void GetProjectionRaw(EVREye eye, float* left, float* right, float* top, float* bottom) override;
    DistortionCoordinates_t ComputeDistortion(EVREye eye, float u, float v) override {
        return {{u, v}, {u, v}, {u, v}};  // no distortion (handled elsewhere)
    }
};
```

**Projection values** are tangent-space: `tan(fov_angle)` for each edge. Left/bottom are negative.

**Render target size** is per-eye. Total framebuffer is typically `width*2 x height`.

</display_component>

<direct_mode_component>

Bypasses the SteamVR compositor -- the driver controls frame presentation directly. Windows-only in practice. See `references/direct-mode.md` for the full interface and ALVR's implementation pattern.

Key methods: `CreateSwapTextureSet`, `SubmitLayer`, `Present`, `PostPresent`.

</direct_mode_component>

<driver_manifest>

`driver.vrdrivermanifest` in driver root:

```json
{
    "alwaysActivate": false,
    "name": "mydriver",
    "directory": "",
    "resourceOnly": false,
    "hmd_presence": ["*.*"]
}
```

| Field | Purpose |
|-------|---------|
| `alwaysActivate` | Load even without HMD detection |
| `name` | Driver identifier (matches folder name) |
| `resourceOnly` | If true, only provides resources (models, icons), no devices |
| `hmd_presence` | USB VID.PID pairs that trigger activation |

Register driver: `vrpathreg adddriver /path/to/driver`

</driver_manifest>

<vrsettings_api>

Persistent key-value store in `steamvr.vrsettings`:

```cpp
// Read
float rate = vr::VRSettings()->GetFloat("mydriver", "refreshRate");
bool enabled = vr::VRSettings()->GetBool(vr::k_pch_SteamVR_Section, "enableLinuxVulkanAsync");

// Write
vr::VRSettings()->SetFloat("mydriver", "refreshRate", 90.0f);
vr::VRSettings()->SetBool(vr::k_pch_SteamVR_Section, "disableAsyncReprojection", true);
```

**Pitfall:** Writing SteamVR-section settings (like async reprojection) can conflict with user preferences. Only do this when necessary and document it.

</vrsettings_api>

<event_handling>

Poll in `RunFrame()`:

```cpp
vr::VREvent_t event;
while (vr::VRServerDriverHost()->PollNextEvent(&event, sizeof(event))) {
    switch (event.eventType) {
        case vr::VREvent_Input_HapticVibration: {
            auto& h = event.data.hapticVibration;
            // h.containerHandle, h.fDurationSeconds, h.fFrequency, h.fAmplitude
            break;
        }
        case vr::VREvent_DriverRequestedQuit:
            // Shutdown requested
            break;
        case vr::VREvent_ChaperoneUniverseHasChanged:
            // Playspace changed -- update tracking origin
            break;
    }
}
```

**Vendor events:** `VREvent_VendorSpecific_Reserved_Start + offset` for custom events.

```cpp
// Fire custom event
vr::VRServerDriverHost()->VendorSpecificEvent(objectId, myCustomEvent, {}, 0);
```

</event_handling>

<tracker_emulation>

See `references/tracker-emulation.md` for the complete property set needed to emulate Vive Trackers, including role assignment and icon paths.

</tracker_emulation>

<pitfalls>

| Pitfall | Fix |
|---------|-----|
| Blocking `RunFrame()` | Offload heavy work to threads; RunFrame is the server tick |
| Missing `VR_INIT_SERVER_DRIVER_CONTEXT` | First call in `Init()`, or all VR API calls fail |
| Wrong vtable from `GetComponent` | Use `static_cast<IVRDisplayComponent*>(this)` |
| Non-unique serial numbers | Serials must be globally unique and stable across sessions |
| Setting properties before `Activate` | `prop_container` is only valid after `Activate` |
| Linux refresh rate overwrite | vrcompositor may reset `DisplayFrequency` -- re-set after encoder connects |
| Calling `SetChaperoneArea` on main thread | Crashes SteamVR on Linux -- call from a spawned thread |
| Not cleaning up on `Cleanup()` | Release all resources, stop threads, call `VR_CLEANUP_SERVER_DRIVER_CONTEXT` last |
| `TrackedDeviceAdded` after `Init` returns | Can add devices later, but they won't be activated until next frame |

</pitfalls>

<debugging>

| Log | Location | Content |
|-----|----------|---------|
| `vrserver.txt` | `~/.local/share/Steam/logs/` (Linux) or `%LOCALAPPDATA%\openvr\` (Win) | Server-side messages |
| `driver_log.txt` | Driver directory or SteamVR logs | Your `VRDriverLog()` output |
| `vrclient_*.txt` | Same logs directory | Client application messages |

Use `InitDriverLog(vr::VRDriverLog())` in `Init()` and `DriverLog()` to write.

SteamVR monitor: `~/.steam/steam/steamapps/common/SteamVR/bin/linux64/vrmonitor` shows connected devices and status.

</debugging>

<alvr_integration>

ALVR's `server_openvr` crate at `rust/alvr/repo/alvr/server_openvr/` demonstrates a production Rust FFI to C++ OpenVR driver:

- **Entry point:** `HmdDriverFactory` in `src/lib.rs` -- Rust `#[no_mangle] extern "C"` calling C++ `CppOpenvrEntryPoint`
- **FFI bridge:** C++ `bindings.h` defines function pointers set from Rust, C++ calls back into Rust
- **Device hierarchy:** `TrackedDevice` base -> `Hmd`, `Controller`, `FakeViveTracker`
- **Pose flow:** Rust `ServerCoreEvent::Tracking` -> C++ `SetTracking()` -> per-device `OnPoseUpdated()` -> `TrackedDevicePoseUpdated()`
- **Property setting:** Rust `props.rs` maps `OpenvrProperty` enums to FFI `SetOpenvrProperty` calls
- **Emulation modes:** `HeadsetEmulationMode` (RiftS, Quest2, QuestPro, Vive, Custom) and `ControllersEmulationMode` (Touch, Index, Vive Wand, Vive Tracker, Pico4, Custom)
- **Direct mode (Windows):** `OvrDirectModeComponent` manages D3D11 shared textures
- **Threading:** `driver_ready_idle` spawns event loop thread; main thread stays free for `RunFrame`

Key files:
- `cpp/alvr_server/alvr_server.cpp` -- `DriverProvider`, entry points, event loop
- `cpp/alvr_server/TrackedDevice.{h,cpp}` -- base class with `Activate`/`Deactivate`/`GetPose`
- `cpp/alvr_server/HMD.{h,cpp}` -- HMD with `IVRDisplayComponent`
- `cpp/alvr_server/Controller.{h,cpp}` -- input components, skeleton, button mapping
- `cpp/alvr_server/FakeViveTracker.{h,cpp}` -- body tracker emulation
- `src/lib.rs` -- Rust entry, FFI setup, event dispatch
- `src/props.rs` -- property setting, serial number generation, emulation profiles

</alvr_integration>

<deep_reference>

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `pose-and-timing.md` | DriverPose_t fields, coordinate systems, prediction, vsync |
| `device-properties.md` | Full property reference, emulation profiles (Oculus, Vive, Index, Pico) |
| `input-system.md` | Input components, controller profiles, SteamVR Input 2.0, skeleton |
| `direct-mode.md` | IVRDriverDirectModeComponent, D3D11 shared textures, frame presentation |
| `tracker-emulation.md` | Vive Tracker property sets, role assignment, body tracking |

</deep_reference>
