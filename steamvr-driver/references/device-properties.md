# Device Properties Reference

## Property API

```cpp
auto props = vr::VRProperties();

// Setters by type
props->SetBoolProperty(container, key, value);
props->SetFloatProperty(container, key, value);
props->SetInt32Property(container, key, value);
props->SetUint64Property(container, key, value);
props->SetStringProperty(container, key, value);
props->SetDoubleProperty(container, key, value);
props->SetVec3Property(container, key, vec3);

// Raw property (for matrices, etc.)
vr::HmdMatrix34_t matrix = ...;
props->SetProperty(container, Prop_StatusDisplayTransform_Matrix34,
    &matrix, sizeof(matrix), k_unHmdMatrix34PropertyTag);
```

Always check the return value:
```cpp
auto result = props->SetStringProperty(container, key, value);
if (result != vr::TrackedProp_Success) {
    // Log vr::VRPropertiesRaw()->GetPropErrorNameFromEnum(result)
}
```

## Notifying Property Changes

After setting a property dynamically (outside `Activate`), notify SteamVR:

```cpp
vr::VREvent_Data_t eventData = {};
eventData.property.container = m_propContainer;
eventData.property.prop = key;
vr::VRServerDriverHost()->VendorSpecificEvent(
    m_objectId, vr::VREvent_PropertyChanged, eventData, 0.
);
```

## Essential HMD Properties

| Property | Type | Example | Notes |
|----------|------|---------|-------|
| `Prop_TrackingSystemName_String` | String | `"oculus"` | Groups devices in same tracking space |
| `Prop_ModelNumber_String` | String | `"Miramar"` | Device model |
| `Prop_SerialNumber_String` | String | `"1WMHH000X00000"` | Must be unique |
| `Prop_ManufacturerName_String` | String | `"Oculus"` | |
| `Prop_RenderModelName_String` | String | `"generic_hmd"` | 3D model in SteamVR |
| `Prop_DisplayFrequency_Float` | Float | `90.0` | Hz |
| `Prop_UserIpdMeters_Float` | Float | `0.063` | IPD |
| `Prop_RegisteredDeviceType_String` | String | `"oculus/serial"` | For binding lookup |
| `Prop_CurrentUniverseId_Uint64` | Uint64 | `2` | 0=invalid, 1=reserved |
| `Prop_IsOnDesktop_Bool` | Bool | `false` | Avoid fullscreen warnings (Windows) |
| `Prop_ContainsProximitySensor_Bool` | Bool | `true` | Enable proximity input |
| `Prop_DeviceProvidesBatteryStatus_Bool` | Bool | `true` | Enable battery reporting |
| `Prop_SecondsFromVsyncToPhotons_Float` | Float | `0.011` | Display timing |
| `Prop_UserHeadToEyeDepthMeters_Float` | Float | `0.0` | Eye depth offset |

## Essential Controller Properties

All HMD basics plus:

| Property | Type | Example | Notes |
|----------|------|---------|-------|
| `Prop_ControllerType_String` | String | `"oculus_touch"` | Must match binding profile |
| `Prop_InputProfilePath_String` | String | `"{oculus}/input/touch_profile.json"` | Input binding config |
| `Prop_ControllerRoleHint_Int32` | Int32 | `1` | 0=invalid, 1=left, 2=right |
| `Prop_SupportedButtons_Uint64` | Uint64 | `0xFFFFFFFFFFFFFFFF` | Bitmask of supported buttons |
| `Prop_Axis0Type_Int32` | Int32 | `2` | 2=joystick |
| `Prop_AttachedDeviceId_String` | String | Serial | |

## Tracker Properties

| Property | Type | Example |
|----------|------|---------|
| `Prop_ControllerHandSelectionPriority_Int32` | Int32 | `-1` |
| `Prop_HasDisplayComponent_Bool` | Bool | `false` |
| `Prop_HasCameraComponent_Bool` | Bool | `false` |
| `Prop_HasDriverDirectModeComponent_Bool` | Bool | `false` |
| `Prop_HasVirtualDisplayComponent_Bool` | Bool | `false` |

## Icon Properties

Set status icons for the SteamVR dashboard:

```cpp
props->SetStringProperty(container, Prop_NamedIconPathDeviceOff_String,
    "{mydriver}/icons/headset_off.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceSearching_String,
    "{mydriver}/icons/headset_searching.gif");
props->SetStringProperty(container, Prop_NamedIconPathDeviceReady_String,
    "{mydriver}/icons/headset_ready.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceStandby_String,
    "{mydriver}/icons/headset_standby.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceAlertLow_String,
    "{mydriver}/icons/headset_ready_low.png");
```

`{mydriver}` resolves to your driver's `resources/` directory.

## HMD Emulation Profiles (from ALVR)

### Quest 2
```
TrackingSystemName = "oculus"
ModelNumber = "Miramar"
Manufacturer = "Oculus"
Serial = "1WMHH000X00000"
RenderModel = "generic_hmd"
RegisteredDeviceType = "oculus/{serial}"
Icons = "{oculus}/icons/quest_headset_*"
```

### Quest Pro
```
TrackingSystemName = "oculus"
ModelNumber = "Meta Quest Pro"
Manufacturer = "Oculus"
Serial = "230YC0XXXX00XX"
```

### Vive
```
TrackingSystemName = "Vive Tracker"
ModelNumber = "ALVR driver server"
Manufacturer = "HTC"
RegisteredDeviceType = "vive"
Icons = "{htc}/icons/vive_headset_*"
```

## Controller Emulation Profiles

### Oculus Touch (Quest 2/3/Pro)
```
TrackingSystemName = "oculus"
ControllerType = "oculus_touch"
InputProfilePath = "{oculus}/input/touch_profile.json"
RegisteredDeviceType = "oculus/{serial}_Controller_{Left|Right}"
```

### Valve Index (Knuckles)
```
TrackingSystemName = "indexcontroller"
Manufacturer = "Valve"
ControllerType = "knuckles"
InputProfilePath = "{indexcontroller}/input/index_controller_profile.json"
RenderModel = "{indexcontroller}valve_controller_knu_1_0_{left|right}"
```

### Vive Wand
```
TrackingSystemName = "htc"
Manufacturer = "HTC"
ControllerType = "vive_controller"
RenderModel = "vr_controller_vive_1_5"
```

### Pico 4
```
TrackingSystemName = "vrlink"
Manufacturer = "ByteDance"
ControllerType = "pico_controller"
InputProfilePath = "{vrlink}/input/pico_controller_profile.json"
```

## Battery Reporting

```cpp
vr::VRProperties()->SetFloatProperty(container,
    vr::Prop_DeviceBatteryPercentage_Float, 0.85f);  // 0.0-1.0
vr::VRProperties()->SetBoolProperty(container,
    vr::Prop_DeviceIsCharging_Bool, false);
```

Requires `Prop_DeviceProvidesBatteryStatus_Bool = true`.

## Dynamic Eye Configuration (from ALVR)

Update IPD and FOV at runtime without recreating the device:

```cpp
// Update eye-to-head transforms
vr::HmdMatrix34_t leftTransform = identity;
leftTransform.m[0][3] = -ipd / 2.0f;
vr::HmdMatrix34_t rightTransform = identity;
rightTransform.m[0][3] = ipd / 2.0f;
vr::VRServerDriverHost()->SetDisplayEyeToHead(objectId, leftTransform, rightTransform);

// Update projection (tangent-space bounds)
vr::VRServerDriverHost()->SetDisplayProjectionRaw(objectId, leftProj, rightProj);

// Notify lens config changed
vr::VRServerDriverHost()->VendorSpecificEvent(
    objectId, vr::VREvent_LensDistortionChanged, {}, 0);
```
