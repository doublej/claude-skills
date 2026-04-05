# DriverPose_t & Timing

## DriverPose_t Fields

```cpp
struct DriverPose_t {
    // Timing
    double poseTimeOffset;              // seconds offset from "now" for prediction

    // Coordinate transforms (identity for most drivers)
    HmdQuaternion_t qWorldFromDriverRotation;   // driver space -> world space rotation
    double vecWorldFromDriverTranslation[3];     // driver space -> world space translation
    HmdQuaternion_t qDriverFromHeadRotation;     // head space -> driver space rotation
    double vecDriverFromHeadTranslation[3];      // head space -> driver space translation

    // Device position and orientation in driver space
    double vecPosition[3];
    double vecVelocity[3];              // m/s
    double vecAcceleration[3];          // m/s^2
    HmdQuaternion_t qRotation;
    double vecAngularVelocity[3];       // rad/s
    double vecAngularAcceleration[3];   // rad/s^2

    // Status
    ETrackingResult result;             // TrackingResult_Running_OK etc.
    bool poseIsValid;
    bool willDriftInYaw;
    bool shouldApplyHeadModel;
    bool deviceIsConnected;
};
```

## Coordinate System

SteamVR uses a right-handed coordinate system:
- **+X** = right
- **+Y** = up
- **+Z** = backward (toward user)

This is the same as OpenGL convention.

## Quaternion Convention

`HmdQuaternion_t` is `{w, x, y, z}` -- scalar-first.

```cpp
// Identity quaternion
vr::HmdQuaternion_t identity = {1.0, 0.0, 0.0, 0.0};
```

## Transform Chain

Final world pose = `WorldFromDriver * DriverPose * DriverFromHead`

For most drivers, set both transforms to identity:
```cpp
pose.qWorldFromDriverRotation = {1, 0, 0, 0};
pose.vecWorldFromDriverTranslation[0] = 0;
pose.vecWorldFromDriverTranslation[1] = 0;
pose.vecWorldFromDriverTranslation[2] = 0;
pose.qDriverFromHeadRotation = {1, 0, 0, 0};
pose.vecDriverFromHeadTranslation[0] = 0;
pose.vecDriverFromHeadTranslation[1] = 0;
pose.vecDriverFromHeadTranslation[2] = 0;
```

Use `WorldFromDriver` when your tracking system has a different origin than SteamVR's world (e.g., calibration offset). Use `DriverFromHead` when the tracking point is not the head center (e.g., tracker mounted on top of HMD).

## Pose Prediction

`poseTimeOffset` tells SteamVR how far into the future (positive) or past (negative) this pose represents relative to "now":

- **0.0**: Pose is for the current moment
- **Positive**: Pose is already predicted for the future (SteamVR applies less correction)
- **Negative**: Pose is from the past (SteamVR applies more correction)

When you provide velocity and acceleration, SteamVR uses them for additional prediction. If you can predict poses yourself, set `poseTimeOffset` to match your prediction target and provide velocity for SteamVR's interpolation.

```cpp
// Pose is for 5ms in the future
pose.poseTimeOffset = 0.005;

// Provide velocity for SteamVR's prediction
pose.vecVelocity[0] = vx;
pose.vecVelocity[1] = vy;
pose.vecVelocity[2] = vz;
pose.vecAngularVelocity[0] = wx;
pose.vecAngularVelocity[1] = wy;
pose.vecAngularVelocity[2] = wz;
```

## Tracking Results

```cpp
enum ETrackingResult {
    TrackingResult_Uninitialized          = 1,  // not yet tracked
    TrackingResult_Calibrating_InProgress = 100,
    TrackingResult_Calibrating_OutOfRange = 101,
    TrackingResult_Running_OK             = 200, // fully tracking
    TrackingResult_Running_OutOfRange     = 201, // tracking but degraded
    TrackingResult_Fallback_RotationOnly  = 300, // orientation only, no position
};
```

## VSync and Frame Pacing

**Compositor-mode** (Linux, or Windows without direct mode):
```cpp
// Signal vsync to SteamVR
vr::VRServerDriverHost()->VsyncEvent(0.0);
```

**Direct-mode** (Windows with `IVRDriverDirectModeComponent`):
- `PostPresent()` is called after frame presentation
- Use this to wait for vsync or pace frames
- Set `Prop_DriverDirectModeSendsVsyncEvents_Bool` to control whether the driver or SteamVR drives vsync

ALVR pattern for frame pacing:
```cpp
// In PostPresent() or equivalent
void wait_for_vsync() {
    auto duration = calculate_time_until_next_vsync();
    if (duration.has_value()) {
        std::this_thread::sleep_for(*duration);
    } else {
        std::this_thread::sleep_for(std::chrono::milliseconds(8)); // fallback ~120Hz
    }
}
```

## Submitting Poses

```cpp
void submit_pose(vr::DriverPose_t pose) {
    m_lastPose = pose;  // cache for GetPose()
    vr::VRServerDriverHost()->TrackedDevicePoseUpdated(
        m_objectId, pose, sizeof(vr::DriverPose_t)
    );
}
```

Call `TrackedDevicePoseUpdated` whenever you have new tracking data. Can be called from any thread.

**Timing:** Submit poses as fast as your tracking system provides them. SteamVR handles interpolation/prediction to display time. Submitting at higher rates than display refresh is fine and improves prediction quality.

## Display Timing Properties

```cpp
// How long from vsync to photons reaching the user's eyes
props->SetFloatProperty(container, Prop_SecondsFromVsyncToPhotons_Float, 0.011f);

// Display refresh rate in Hz
props->SetFloatProperty(container, Prop_DisplayFrequency_Float, 90.0f);

// Seconds between vsyncs
props->SetFloatProperty(container, Prop_SecondsFromPhotonsToVblank_Float, 0.0f);
```

**Pitfall (Linux):** vrcompositor may overwrite `DisplayFrequency` to 90Hz during initialization. ALVR works around this by re-setting the property after the encoder connects.
