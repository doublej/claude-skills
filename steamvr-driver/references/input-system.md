# Input System

## Input Components

Create in `Activate()` via `vr::VRDriverInput()`:

### Boolean (buttons, touches)

```cpp
vr::VRInputComponentHandle_t handle;
vr::VRDriverInput()->CreateBooleanComponent(container, "/input/a/click", &handle);

// Update
vr::VRDriverInput()->UpdateBooleanComponent(handle, true, 0.0);
```

### Scalar (triggers, axes)

```cpp
vr::VRInputComponentHandle_t handle;
vr::VRDriverInput()->CreateScalarComponent(
    container,
    "/input/trigger/value",
    &handle,
    vr::VRScalarType_Absolute,      // or VRScalarType_Relative
    vr::VRScalarUnits_NormalizedOneSided  // 0..1
);

// Update
vr::VRDriverInput()->UpdateScalarComponent(handle, 0.75f, 0.0);
```

Scalar units:
- `VRScalarUnits_NormalizedOneSided` -- 0.0 to 1.0 (triggers, grip)
- `VRScalarUnits_NormalizedTwoSided` -- -1.0 to 1.0 (joystick axes)

### Haptic

```cpp
vr::VRInputComponentHandle_t haptic;
vr::VRDriverInput()->CreateHapticComponent(container, "/output/haptic", &haptic);
```

Haptic events come through `VREvent_Input_HapticVibration` in `RunFrame()`:
```cpp
case vr::VREvent_Input_HapticVibration: {
    auto& h = event.data.hapticVibration;
    if (h.containerHandle == m_controller->prop_container) {
        play_haptic(h.fDurationSeconds, h.fFrequency, h.fAmplitude);
    }
    break;
}
```

### Skeleton (hand tracking)

```cpp
vr::VRInputComponentHandle_t skeleton;
vr::VRDriverInput()->CreateSkeletonComponent(
    container,
    "/input/skeleton/left",       // component path
    "/skeleton/hand/left",        // skeleton path
    "/pose/raw",                  // base pose path
    vr::VRSkeletalTracking_Partial,  // tracking level
    nullptr,                      // grip limit transforms (null = none)
    0,                            // grip limit count
    &skeleton
);
```

Tracking levels:
- `VRSkeletalTracking_Estimated` -- inferred from controller inputs
- `VRSkeletalTracking_Partial` -- some finger tracking
- `VRSkeletalTracking_Full` -- full hand tracking (optical)

Update with 31 bone transforms per frame:

```cpp
vr::VRBoneTransform_t bones[31];
// Fill bone transforms...

vr::VRDriverInput()->UpdateSkeletonComponent(
    skeleton,
    vr::VRSkeletalMotionRange_WithController,
    bones, 31
);
vr::VRDriverInput()->UpdateSkeletonComponent(
    skeleton,
    vr::VRSkeletalMotionRange_WithoutController,
    bones, 31
);
```

**Pitfall:** Must update both motion ranges even if they're identical, or hand models freeze.

**Pitfall:** Must set initial bone transforms in `Activate()` or hands appear frozen until the first tracking update.

### Proximity Sensor

```cpp
vr::VRInputComponentHandle_t proximity;
vr::VRDriverInput()->CreateBooleanComponent(container, "/proximity", &proximity);

// When user puts on HMD
vr::VRDriverInput()->UpdateBooleanComponent(proximity, true, 0.0);
// When user takes off HMD
vr::VRDriverInput()->UpdateBooleanComponent(proximity, false, 0.0);
```

## Standard Input Paths

### Oculus Touch / Meta Controllers
```
/input/a/click, /input/a/touch
/input/b/click, /input/b/touch
/input/x/click, /input/x/touch          (left only)
/input/y/click, /input/y/touch          (left only)
/input/trigger/value, /input/trigger/touch
/input/grip/value, /input/grip/touch
/input/thumbstick/x, /input/thumbstick/y
/input/thumbstick/click, /input/thumbstick/touch
/input/thumbrest/touch
/input/system/click                      (may be reserved by SteamVR)
/output/haptic
```

### Valve Index
All Touch paths plus:
```
/input/finger/index, /input/finger/middle
/input/finger/ring, /input/finger/pinky
/input/trackpad/x, /input/trackpad/y
/input/trackpad/force, /input/trackpad/touch
```

### Vive Wand
```
/input/system/click
/input/grip/click
/input/menu/click
/input/trigger/value, /input/trigger/click
/input/trackpad/x, /input/trackpad/y
/input/trackpad/click, /input/trackpad/touch
/output/haptic
```

## Controller Profile JSON

Located at `{driver}/resources/input/{profile_name}.json`. Tells SteamVR what inputs exist.

```json
{
    "jsonid": "input_profile",
    "controller_type": "mycontroller",
    "device_class": "TrackedDeviceClass_Controller",
    "resource_root": "mydriver",
    "driver_name": "mydriver",
    "input_bindingui_mode": "controller_binding_ui",
    "should_show_binding_errors": true,
    "input_bindingui_left": {
        "image": "{mydriver}/icons/controller_left.png"
    },
    "input_bindingui_right": {
        "image": "{mydriver}/icons/controller_right.png"
    },
    "input_source": {
        "/input/a": {
            "type": "button",
            "binding_image_point": [50, 50],
            "order": 1
        },
        "/input/trigger": {
            "type": "trigger",
            "binding_image_point": [30, 70],
            "order": 2
        },
        "/input/thumbstick": {
            "type": "joystick",
            "binding_image_point": [40, 30],
            "order": 3
        },
        "/output/haptic": {
            "type": "haptic",
            "order": 10
        }
    }
}
```

**Critical:** `controller_type` must match `Prop_ControllerType_String` exactly.

## SteamVR Input 2.0 (Hand Tracking)

For dedicated hand tracking devices separate from controllers:

```cpp
// Register as a hand tracker device
vr::VRServerDriverHost()->TrackedDeviceAdded(
    "HandTracker_Left",
    vr::TrackedDeviceClass_Controller,  // still use Controller class
    m_handTracker
);

// Set special properties
props->SetStringProperty(container, Prop_ControllerType_String,
    "svl_hand_interaction_augmented");
props->SetStringProperty(container, Prop_InputProfilePath_String,
    "{vrlink}/input/svl_hand_interaction_augmented_input_profile.json");
props->SetInt32Property(container, Prop_ControllerRoleHint_Int32, 1); // left
```

ALVR registers two pairs of devices per hand: controllers + hand trackers. Selection happens at runtime by toggling `deviceIsConnected` in the pose.

## Button Mapping (ALVR Pattern)

ALVR maps abstract button IDs to SteamVR input paths using lookup tables:

```cpp
// Per-button registration
std::map<uint64_t, ButtonInfo> LEFT_CONTROLLER_BUTTON_MAPPING;

struct ButtonInfo {
    std::vector<const char*> steamvr_paths;  // can map to multiple paths
    ButtonType type;  // Binary, ScalarOneSided, ScalarTwoSided
};
```

This allows runtime remapping and supports emulating different controller profiles with the same physical input data.
