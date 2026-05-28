# Vive Tracker Emulation

## Overview

Many VR applications expect Vive Trackers for body/object tracking. Emulating them requires setting specific properties so SteamVR and applications recognize the device correctly.

## Minimal Registration

```cpp
vr::VRServerDriverHost()->TrackedDeviceAdded(
    "MyTracker_Waist",                         // unique serial
    vr::TrackedDeviceClass_GenericTracker,      // device class
    m_tracker                                   // ITrackedDeviceServerDriver*
);
```

## Required Properties

Set these in `Activate()`:

```cpp
auto props = vr::VRProperties();

// Core identity
props->SetStringProperty(container, Prop_TrackingSystemName_String, "lighthouse");
props->SetStringProperty(container, Prop_ModelNumber_String, "Vive Tracker Pro MV");
props->SetStringProperty(container, Prop_SerialNumber_String, "UNIQUE_SERIAL");
props->SetStringProperty(container, Prop_RenderModelName_String, "{htc}vr_tracker_vive_1_0");
props->SetStringProperty(container, Prop_ManufacturerName_String, "HTC");
props->SetStringProperty(container, Prop_ResourceRoot_String, "htc");

// Device type registration (determines role)
props->SetStringProperty(container, Prop_RegisteredDeviceType_String,
    "ALVR/tracker/waist");  // see role table below
props->SetStringProperty(container, Prop_InputProfilePath_String,
    "{htc}/input/vive_tracker_profile.json");
props->SetStringProperty(container, Prop_ControllerType_String,
    "vive_tracker_waist");  // see role table below
props->SetInt32Property(container, Prop_DeviceClass_Int32,
    vr::TrackedDeviceClass_GenericTracker);

// Not a controller -- don't interfere with hand assignment
props->SetInt32Property(container, Prop_ControllerRoleHint_Int32,
    vr::TrackedControllerRole_Invalid);
props->SetInt32Property(container, Prop_ControllerHandSelectionPriority_Int32, -1);

// Disable unused components
props->SetBoolProperty(container, Prop_HasDisplayComponent_Bool, false);
props->SetBoolProperty(container, Prop_HasCameraComponent_Bool, false);
props->SetBoolProperty(container, Prop_HasDriverDirectModeComponent_Bool, false);
props->SetBoolProperty(container, Prop_HasVirtualDisplayComponent_Bool, false);
```

## Tracker Roles

| Body Part | RegisteredDeviceType | ControllerType |
|-----------|---------------------|----------------|
| Waist/Hips | `ALVR/tracker/waist` | `vive_tracker_waist` |
| Chest | `ALVR/tracker/chest` | `vive_tracker_waist` |
| Left foot | `ALVR/tracker/left_foot` | `vive_tracker_left_foot` |
| Right foot | `ALVR/tracker/right_foot` | `vive_tracker_right_foot` |
| Left knee | `ALVR/tracker/left_knee` | `vive_tracker_left_knee` |
| Right knee | `ALVR/tracker/right_knee` | `vive_tracker_right_knee` |
| Left elbow | `ALVR/tracker/left_elbow` | `vive_tracker_left_elbow` |
| Right elbow | `ALVR/tracker/right_elbow` | `vive_tracker_right_elbow` |
| Left shoulder | `ALVR/tracker/left_shoulder` | `vive_tracker_left_shoulder` |
| Right shoulder | `ALVR/tracker/right_shoulder` | `vive_tracker_right_shoulder` |
| Camera | `ALVR/tracker/camera` | `vive_tracker_camera` |
| Keyboard | `ALVR/tracker/keyboard` | `vive_tracker_keyboard` |

The `RegisteredDeviceType` prefix (`ALVR/tracker/`) can be anything, but the suffix determines the role. The `ControllerType` must match the pattern `vive_tracker_{role}`.

## Vive Hardware Emulation Properties

For maximum compatibility, set these firmware/hardware strings:

```cpp
props->SetBoolProperty(container, Prop_WillDriftInYaw_Bool, false);
props->SetBoolProperty(container, Prop_DeviceIsWireless_Bool, true);
props->SetBoolProperty(container, Prop_DeviceIsCharging_Bool, false);
props->SetFloatProperty(container, Prop_DeviceBatteryPercentage_Float, 1.0f);
props->SetBoolProperty(container, Prop_DeviceProvidesBatteryStatus_Bool, true);
props->SetBoolProperty(container, Prop_DeviceCanPowerOff_Bool, true);

props->SetStringProperty(container, Prop_ConnectedWirelessDongle_String, "D0000BE000");
props->SetStringProperty(container, Prop_TrackingFirmwareVersion_String,
    "1541800000 RUNNER-WATCHMAN$runner-watchman@runner-watchman 2018-01-01 "
    "FPGA 512(2.56/0/0) BL 0 VRC 1541800000 Radio 1518800000");
props->SetStringProperty(container, Prop_HardwareRevision_String,
    "product 128 rev 2.5.6 lot 2000/0/0 0");

props->SetUint64Property(container, Prop_HardwareRevision_Uint64, 2214720000);
props->SetUint64Property(container, Prop_FirmwareVersion_Uint64, 1541800000);
props->SetUint64Property(container, Prop_FPGAVersion_Uint64, 512);
props->SetUint64Property(container, Prop_VRCVersion_Uint64, 1514800000);
props->SetUint64Property(container, Prop_RadioVersion_Uint64, 1518800000);
props->SetUint64Property(container, Prop_DongleVersion_Uint64, 8933539758);

props->SetBoolProperty(container, Prop_Firmware_UpdateAvailable_Bool, false);
props->SetBoolProperty(container, Prop_Firmware_ManualUpdate_Bool, false);
props->SetBoolProperty(container, Prop_Firmware_ForceUpdateRequired_Bool, false);
props->SetBoolProperty(container, Prop_Firmware_RemindUpdate_Bool, false);
props->SetBoolProperty(container, Prop_Identifiable_Bool, false);
```

## Status Icons

```cpp
props->SetStringProperty(container, Prop_NamedIconPathDeviceOff_String,
    "{htc}/icons/tracker_status_off.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceSearching_String,
    "{htc}/icons/tracker_status_searching.gif");
props->SetStringProperty(container, Prop_NamedIconPathDeviceSearchingAlert_String,
    "{htc}/icons/tracker_status_searching_alert.gif");
props->SetStringProperty(container, Prop_NamedIconPathDeviceReady_String,
    "{htc}/icons/tracker_status_ready.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceReadyAlert_String,
    "{htc}/icons/tracker_status_ready_alert.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceNotReady_String,
    "{htc}/icons/tracker_status_error.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceStandby_String,
    "{htc}/icons/tracker_status_standby.png");
props->SetStringProperty(container, Prop_NamedIconPathDeviceAlertLow_String,
    "{htc}/icons/tracker_status_ready_low.png");
```

## Pose Updates

Tracker poses follow the same pattern as any device:

```cpp
void UpdateTrackerPose(const DeviceMotion* motion) {
    if (m_objectId == vr::k_unTrackedDeviceIndexInvalid) return;

    bool tracked = (motion != nullptr);
    vr::DriverPose_t pose = {};
    pose.poseIsValid = tracked;
    pose.deviceIsConnected = tracked;
    pose.result = tracked ? vr::TrackingResult_Running_OK
                          : vr::TrackingResult_Uninitialized;
    pose.qWorldFromDriverRotation = {1, 0, 0, 0};
    pose.qDriverFromHeadRotation = {1, 0, 0, 0};

    if (motion) {
        pose.qRotation = {motion->w, motion->x, motion->y, motion->z};
        pose.vecPosition[0] = motion->px;
        pose.vecPosition[1] = motion->py;
        pose.vecPosition[2] = motion->pz;
    }

    vr::VRServerDriverHost()->TrackedDevicePoseUpdated(
        m_objectId, pose, sizeof(pose));
}
```

Set `deviceIsConnected = false` when the tracker is not available. SteamVR will show it as disconnected rather than removing it.

## Tracking System Isolation

If you want your trackers in a **different tracking space** than the HMD (e.g., for space calibration tools like OpenVR Space Calibrator), use a different `TrackingSystemName`:

```cpp
// HMD uses "lighthouse", trackers use custom name
props->SetStringProperty(container, Prop_TrackingSystemName_String, "MyTrackerCustom");
```

This allows tools to calibrate between tracking systems by treating them as separate coordinate spaces.

## Proxy Tracker Pattern

ALVR uses a "ViveTrackerProxy" -- a tracker that mirrors the HMD pose but in a different tracking system. This enables space calibration between ALVR's tracking and native SteamVR tracking. The proxy is registered alongside the HMD and updated on every HMD pose update.
