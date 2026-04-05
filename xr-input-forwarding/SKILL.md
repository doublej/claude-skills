---
name: xr-input-forwarding
description: "Stream XR tracking over network: hand/face/body/eye poses, compression"
---

# XR Input Forwarding

## Before Writing Code

1. **Identify tracking sources** — which extensions are available on the runtime:
   - Hand: `XR_EXT_hand_tracking` (standard), `XR_FB_hand_tracking_mesh` (Meta mesh)
   - Face: `XR_FB_face_tracking2` (Meta, 70 blend shapes)
   - Body: `XR_META_body_tracking` (full body), `XR_FB_body_tracking` (upper body)
   - Eye: `XR_EXT_eye_gaze_interaction` (standard gaze)

2. **Determine forwarding topology**:
   - Headset -> PC (ALVR/SteamVR streaming)
   - Headset -> Headset (social VR)
   - Headset -> Application server (motion capture, analytics)

3. **Check privacy requirements** — eye tracking and face tracking require explicit user consent on Meta and other platforms. The runtime gates these behind permission dialogs.

## Hand Tracking

### Extension Setup

Request `XR_EXT_hand_tracking` and create trackers for each hand:

```c
XrHandTrackerCreateInfoEXT createInfo = {XR_TYPE_HAND_TRACKER_CREATE_INFO_EXT};
createInfo.hand = XR_HAND_LEFT_EXT;
createInfo.handJointSet = XR_HAND_JOINT_SET_DEFAULT_EXT;
xrCreateHandTrackerEXT(session, &createInfo, &leftTracker);
```

### Joint Data Retrieval

```c
XrHandJointLocationEXT joints[XR_HAND_JOINT_COUNT_EXT]; // 26 joints
XrHandJointLocationsEXT locations = {XR_TYPE_HAND_JOINT_LOCATIONS_EXT};
locations.jointCount = XR_HAND_JOINT_COUNT_EXT;
locations.jointLocations = joints;

XrHandJointsLocateInfoEXT locateInfo = {XR_TYPE_HAND_JOINTS_LOCATE_INFO_EXT};
locateInfo.baseSpace = referenceSpace;
locateInfo.time = predictedDisplayTime;
xrLocateHandJointsEXT(tracker, &locateInfo, &locations);
```

**Critical:** Check `locations.isActive` before reading joints. When `false`, hand is not tracked (occluded, out of range).

Per-joint flags in `XrHandJointLocationEXT`:
- `locationFlags & XR_SPACE_LOCATION_POSITION_VALID_BIT` — position usable
- `locationFlags & XR_SPACE_LOCATION_POSITION_TRACKED_BIT` — actively tracked vs estimated

Joint hierarchy and indices: see `references/hand-joints.md`.

### Hand Tracking Mesh (Meta)

`XR_FB_hand_tracking_mesh` provides a deformable mesh skinned to the 26 joints. Query vertex/index buffers once (topology is static), then update vertex positions each frame.

**Pitfall:** The mesh vertex count can vary between users. Query buffer sizes first, allocate, then fill.

### Forwarding Hand Data

For each hand per frame, forward:
- `isActive` flag (1 bit)
- 26 x `XrPosef` (position `XrVector3f` + orientation `XrQuaternionf`) = 26 x 28 bytes = 728 bytes
- 26 x `locationFlags` (only need 4 bits each, pack into 13 bytes)
- 26 x `radius` (float, for collision/visualization) = 104 bytes

**Total raw:** ~846 bytes per hand, ~1692 for both hands at full precision.

## Face Tracking

### Extension Setup (Meta)

```c
XrFaceTrackerCreateInfo2FB createInfo = {XR_TYPE_FACE_TRACKER_CREATE_INFO2_FB};
createInfo.faceExpressionSet = XR_FACE_EXPRESSION_SET2_DEFAULT_FB;
xrCreateFaceTracker2FB(session, &createInfo, &faceTracker);
```

### Retrieving Blend Shapes

```c
float weights[XR_FACE_EXPRESSION2_COUNT_FB]; // 70 weights
float confidences[XR_FACE_CONFIDENCE2_COUNT_FB]; // 2 confidences
XrFaceExpressionWeights2FB expressionWeights = {XR_TYPE_FACE_EXPRESSION_WEIGHTS2_FB};
expressionWeights.weightCount = XR_FACE_EXPRESSION2_COUNT_FB;
expressionWeights.weights = weights;
expressionWeights.confidenceCount = XR_FACE_CONFIDENCE2_COUNT_FB;
expressionWeights.confidences = confidences;

XrFaceExpressionInfo2FB info = {XR_TYPE_FACE_EXPRESSION_INFO2_FB};
info.time = predictedDisplayTime;
xrGetFaceExpressionWeights2FB(faceTracker, &info, &expressionWeights);
```

**Check:** `expressionWeights.isValid` and `expressionWeights.isEyeFollowingBlendshapesValid`.

Blend shape list by category: see `references/face-blendshapes.md`.

### ARKit Compatibility

The 70 FB blend shapes are a superset of Apple's 52 ARKit blend shapes. For cross-platform forwarding, map the FB indices to ARKit names. The mapping is mostly 1:1 for matching expressions — see `references/face-blendshapes.md` for the full mapping table.

### Forwarding Face Data

- 70 x `float` weights = 280 bytes raw
- 2 x `float` confidences (upper face, lower face) = 8 bytes
- `isValid` + `isEyeFollowingBlendshapesValid` flags = 1 byte

**Total raw:** ~289 bytes per frame. Weights are [0.0, 1.0] range — quantize to uint8 for 70 bytes (0.4% precision loss, imperceptible for animation).

## Body Tracking

### Full Body (XR_META_body_tracking)

70 joints covering root through fingertips and toes. Requires headset + controllers; no external sensors.

```c
XrBodyTrackerCreateInfoMETA createInfo = {XR_TYPE_BODY_TRACKER_CREATE_INFO_META};
createInfo.bodyJointSet = XR_BODY_JOINT_SET_FULL_BODY_META;
xrCreateBodyTrackerMETA(session, &createInfo, &bodyTracker);
```

### Upper Body (XR_FB_body_tracking)

Subset: 70 joints but only upper body is reliably tracked. Leg joints are estimated/procedural.

### Joint Hierarchy

```
Root (0)
└── Hips (1)
    ├── SpineLower (2) -> SpineMiddle -> SpineUpper -> Chest -> Neck -> Head
    ├── LeftUpperLeg (8) -> LeftLowerLeg -> LeftFoot -> LeftToe
    ├── RightUpperLeg (12) -> RightLowerLeg -> RightFoot -> RightToe
    ├── LeftShoulder (16) -> LeftUpperArm -> LeftLowerArm -> LeftHand -> [fingers]
    └── RightShoulder (38) -> RightUpperArm -> RightLowerArm -> RightHand -> [fingers]
```

Full joint index table: see `references/body-joints.md`.

### Forwarding Body Data

- 70 x `XrPosef` = 70 x 28 bytes = 1960 bytes raw
- 70 x `locationFlags` = ~35 bytes packed
- Skeleton confidence metadata

**Optimization:** Upper body only (first ~36 joints) cuts payload in half when legs aren't needed.

## Eye Tracking

### Gaze Interaction (XR_EXT_eye_gaze_interaction)

Creates a **single gaze pose** (combined eye direction) via the action system:

```c
// Create action with pose type
XrActionCreateInfo actionInfo = {XR_TYPE_ACTION_CREATE_INFO};
actionInfo.actionType = XR_ACTION_TYPE_POSE_INPUT;
strcpy(actionInfo.actionName, "gaze");
xrCreateAction(actionSet, &actionInfo, &gazeAction);

// Bind to gaze interaction profile
xrStringToPath(instance, "/interaction_profiles/ext/eye_gaze_interaction", &profilePath);
xrStringToPath(instance, "/user/eyes_ext/input/gaze_ext/pose", &gazePosePath);
```

**Key difference from other tracking:** Eye gaze uses the standard action system, not a dedicated tracker object. The pose represents a ray (position = eye midpoint, orientation = gaze direction).

### Forwarding Eye Data

- 1 x `XrPosef` = 28 bytes (gaze ray origin + direction)
- `locationFlags` = 1 byte
- `isActive` from action state = 1 byte

**Total:** ~30 bytes per frame. Tiny payload, but **privacy-sensitive** — see privacy section below.

### Privacy Considerations

- Eye tracking reveals cognitive load, attention, reading patterns, emotional state
- Always gate behind explicit user consent flow
- Consider downsampling gaze data (e.g., 10 Hz instead of frame rate)
- Strip raw gaze before logging; prefer derived metrics (fixation zones, not raw coordinates)
- Some platforms (Meta) enforce system-level permission dialogs

## Data Serialization

### Binary Format Design

Layout for a complete tracking frame packet:

```
Header (16 bytes):
  [4] magic: 0x58524654 ("XRFT")
  [4] sequence number (uint32, wrapping)
  [8] timestamp (XrTime, int64 nanoseconds)

Source mask (1 byte):
  bit 0: left hand
  bit 1: right hand
  bit 2: face
  bit 3: body
  bit 4: eye gaze

Per-source data (variable):
  [2] source type + data length (uint16)
  [N] source-specific payload
```

### Compact Representations

| Data | Raw | Compact | Method |
|------|-----|---------|--------|
| Quaternion | 16 bytes (4 floats) | 6 bytes | Smallest-three encoding |
| Position | 12 bytes (3 floats) | 6 bytes | Fixed-point 16-bit (±4m range, 0.12mm precision) |
| Full pose | 28 bytes | 12 bytes | Combined above |
| Face weight | 4 bytes (float) | 1 byte | Quantize [0,1] to uint8 |
| Joint flags | 4 bytes (uint64) | 1 nibble | Only 4 meaningful bits |

**Smallest-three quaternion encoding:**
1. Find the component with largest absolute value
2. Store which component (2 bits) + signs
3. Encode remaining 3 as 14-bit fixed-point each
4. Reconstruct fourth via `w = sqrt(1 - x² - y² - z²)`

### Delta Compression

Between consecutive frames, most joints move minimally:

```
Delta frame:
  [1] change bitmask per joint group
  [N] only changed joints' data

Threshold: skip joint if:
  - position delta < 0.1mm
  - orientation delta < 0.5 degrees
```

**Typical compression ratios:**
- Hands stationary: ~20:1 (only wrist/forearm change)
- Talking (face only): ~4:1 (lips active, forehead stable)
- Walking (full body): ~2:1

**Keyframe interval:** Send full state every 0.5-1s to allow late-joiners and error recovery.

### Interpolation at Receiver

```
Received frames: F(t0), F(t1), F(t2), ...
Render time: t_render = t_latest - jitter_buffer

For each joint:
  pose = slerp(F(t_prev).quat, F(t_next).quat, alpha)  // orientation
  pos  = lerp(F(t_prev).pos,  F(t_next).pos,  alpha)   // position
  alpha = (t_render - t_prev) / (t_next - t_prev)
```

**Rules:**
- Use SLERP for quaternions, never LERP (produces non-unit quaternions)
- Buffer 2-3 frames for jitter absorption (adds 20-40ms latency at 72Hz)
- Extrapolate cautiously — max 1 frame beyond last received, then hold
- For face blend shapes, linear interpolation of weights is fine

## Timestamp Synchronization

### The Problem

Each tracking source runs on its own clock or sample rate:
- Hand tracking: per-frame (72/90/120 Hz)
- Face tracking: up to 72 Hz (may skip frames)
- Body tracking: per-frame
- Eye tracking: up to 90 Hz (action system cadence)

### Synchronization Strategy

All sources use `predictedDisplayTime` from `xrWaitFrame` as the query time:

```c
// Single time source for all queries in one frame
XrTime t = frameState.predictedDisplayTime;
xrLocateHandJointsEXT(handTracker, &locateInfo_with_t, &handLocations);
xrGetFaceExpressionWeights2FB(faceTracker, &info_with_t, &faceWeights);
xrLocateBodyJointsMETA(bodyTracker, &locateInfo_with_t, &bodyLocations);
xrLocateSpace(gazeSpace, refSpace, t, &gazeLocation);
```

**For network forwarding**, attach the `XrTime` (int64 nanoseconds) to each packet. The receiver should:
1. Establish clock offset via NTP-style ping/pong at connection start
2. Convert sender `XrTime` to local timeline
3. Use local `predictedDisplayTime` for interpolation target

**Pitfall:** `XrTime` epoch varies by runtime — it's relative, not absolute. Never compare `XrTime` values across different devices without synchronization.

## Coordinate System Transforms

### Common Mismatches

| Source | Coordinate System | Up | Forward |
|--------|------------------|----|---------|
| OpenXR | Right-handed | +Y | -Z |
| Unity | Left-handed | +Y | +Z |
| Unreal | Left-handed | +Z | +X |
| glTF/Blender | Right-handed | +Y | -Z (same as OpenXR) |

**Transform OpenXR -> Unity:**
```c
// Negate Z for position, negate X and Y for quaternion
unity_pos = { ox_pos.x, ox_pos.y, -ox_pos.z };
unity_quat = { -ox_quat.x, -ox_quat.y, ox_quat.z, ox_quat.w };
```

**Rule:** Apply coordinate transforms at the boundary (sender or receiver, not both). Document which convention the wire format uses.

### Reference Space Alignment

When forwarding between devices, the sender's `LOCAL` or `STAGE` space origin won't match the receiver's. Options:
- **Root-relative:** Send all joints relative to a root joint (hips for body, wrist for hands). Receiver places root in their own space.
- **Head-relative:** Send poses relative to head/VIEW space. Useful for face and eye data.
- **Calibrated absolute:** Run a calibration step to align coordinate systems (complex, needed for shared physical spaces).

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Reading joints when `isActive` is false | Check before accessing joint array |
| Not handling tracking loss mid-stream | Hold last valid pose, fade out after timeout |
| Comparing `XrTime` across devices | Synchronize clocks first, use relative deltas |
| LERP on quaternions | Use SLERP (or NLERP if you normalize after) |
| Sending full state every frame | Use delta compression with periodic keyframes |
| Ignoring face confidence values | Gate blend shape application on confidence > 0.5 |
| Body leg data when upper-body only | Check joint validity flags; legs may be procedural |
| Coordinate system mismatch | Transform at boundary, document wire format convention |
| Eye gaze without consent check | Gate on permission; provide fallback when denied |
| Quantization artifacts on fast motion | Increase precision for velocity-critical joints (wrist, fingers) |
| Blocking on tracking data send | Use async/non-blocking sends; drop frames rather than queue |
| Missing keyframes after packet loss | Periodic full-state refresh (every 0.5-1s) |

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `hand-joints.md` | Joint indices, hierarchy, radius values, mesh details |
| `face-blendshapes.md` | All 70 FB blend shapes, categories, ARKit mapping |
| `body-joints.md` | Full/upper body joint indices, hierarchy, confidence |
| `serialization.md` | Wire format specs, compression algorithms, bandwidth calculations |
