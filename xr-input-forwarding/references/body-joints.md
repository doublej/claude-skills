# Body Joint Reference

## XR_META_body_tracking — Full Body (70 Joints)

### Joint Index Table

#### Core Spine & Head (8)

| Index | Name | Parent |
|-------|------|--------|
| 0 | `ROOT` | — |
| 1 | `HIPS` | Root |
| 2 | `SPINE_LOWER` | Hips |
| 3 | `SPINE_MIDDLE` | SpineLower |
| 4 | `SPINE_UPPER` | SpineMiddle |
| 5 | `CHEST` | SpineUpper |
| 6 | `NECK` | Chest |
| 7 | `HEAD` | Neck |

#### Left Leg (8)

| Index | Name | Parent |
|-------|------|--------|
| 8 | `LEFT_UPPER_LEG` | Hips |
| 9 | `LEFT_LOWER_LEG` | LeftUpperLeg |
| 10 | `LEFT_FOOT_ANKLE_TWIST` | LeftLowerLeg |
| 11 | `LEFT_FOOT_ANKLE` | LeftFootAnkleTwist |
| 12 | `LEFT_FOOT_SUBTALAR` | LeftFootAnkle |
| 13 | `LEFT_FOOT_TRANSVERSE` | LeftFootSubtalar |
| 14 | `LEFT_FOOT_BALL` | LeftFootTransverse |
| 15 | `LEFT_FOOT_TOES` | LeftFootBall |

#### Right Leg (8)

| Index | Name | Parent |
|-------|------|--------|
| 16 | `RIGHT_UPPER_LEG` | Hips |
| 17 | `RIGHT_LOWER_LEG` | RightUpperLeg |
| 18 | `RIGHT_FOOT_ANKLE_TWIST` | RightLowerLeg |
| 19 | `RIGHT_FOOT_ANKLE` | RightFootAnkleTwist |
| 20 | `RIGHT_FOOT_SUBTALAR` | RightFootAnkle |
| 21 | `RIGHT_FOOT_TRANSVERSE` | RightFootSubtalar |
| 22 | `RIGHT_FOOT_BALL` | RightFootTransverse |
| 23 | `RIGHT_FOOT_TOES` | RightFootBall |

#### Left Arm (4)

| Index | Name | Parent |
|-------|------|--------|
| 24 | `LEFT_SHOULDER` | Chest |
| 25 | `LEFT_SCAPULA` | LeftShoulder |
| 26 | `LEFT_ARM_UPPER` | LeftScapula |
| 27 | `LEFT_ARM_LOWER` | LeftArmUpper |

#### Left Hand (14)

| Index | Name | Parent |
|-------|------|--------|
| 28 | `LEFT_HAND_WRIST_TWIST` | LeftArmLower |
| 29 | `LEFT_HAND_PALM` | LeftHandWristTwist |
| 30 | `LEFT_HAND_THUMB_METACARPAL` | LeftHandPalm |
| 31 | `LEFT_HAND_THUMB_PROXIMAL` | 30 |
| 32 | `LEFT_HAND_THUMB_DISTAL` | 31 |
| 33 | `LEFT_HAND_THUMB_TIP` | 32 |
| 34 | `LEFT_HAND_INDEX_METACARPAL` | LeftHandPalm |
| 35-37 | `LEFT_HAND_INDEX_PROXIMAL..TIP` | Chain |
| 38-41 | `LEFT_HAND_MIDDLE_*` | Chain |
| 42-45 | `LEFT_HAND_RING_*` | Chain |
| 46-49 | `LEFT_HAND_LITTLE_*` | Chain (METACARPAL..TIP) |

#### Right Arm (4)

| Index | Name | Parent |
|-------|------|--------|
| 50 | `RIGHT_SHOULDER` | Chest |
| 51 | `RIGHT_SCAPULA` | RightShoulder |
| 52 | `RIGHT_ARM_UPPER` | RightScapula |
| 53 | `RIGHT_ARM_LOWER` | RightArmUpper |

#### Right Hand (14)

| Index | Name | Parent |
|-------|------|--------|
| 54 | `RIGHT_HAND_WRIST_TWIST` | RightArmLower |
| 55 | `RIGHT_HAND_PALM` | RightHandWristTwist |
| 56-69 | `RIGHT_HAND_THUMB..LITTLE_TIP` | Same pattern as left |

### Hierarchy (Tree View)

```
ROOT (0)
└── HIPS (1)
    ├── SPINE_LOWER (2)
    │   └── SPINE_MIDDLE (3)
    │       └── SPINE_UPPER (4)
    │           └── CHEST (5)
    │               ├── NECK (6)
    │               │   └── HEAD (7)
    │               ├── LEFT_SHOULDER (24)
    │               │   └── LEFT_SCAPULA (25)
    │               │       └── LEFT_ARM_UPPER (26)
    │               │           └── LEFT_ARM_LOWER (27)
    │               │               └── LEFT_HAND_WRIST_TWIST (28)
    │               │                   └── LEFT_HAND_PALM (29)
    │               │                       └── [5 finger chains]
    │               └── RIGHT_SHOULDER (50)
    │                   └── [mirror of left arm]
    ├── LEFT_UPPER_LEG (8)
    │   └── LEFT_LOWER_LEG (9)
    │       └── LEFT_FOOT_ANKLE_TWIST (10)
    │           └── LEFT_FOOT_ANKLE (11)
    │               └── LEFT_FOOT_SUBTALAR (12)
    │                   └── LEFT_FOOT_TRANSVERSE (13)
    │                       └── LEFT_FOOT_BALL (14)
    │                           └── LEFT_FOOT_TOES (15)
    └── RIGHT_UPPER_LEG (16)
        └── [mirror of left leg]
```

## XR_FB_body_tracking — Upper Body Subset

Uses the same joint indices but only reliably tracks indices 0-7 (spine/head) and 24-55 (arms/hands). Leg joints (8-23) are present but procedurally estimated — they maintain plausible poses but don't reflect actual leg motion.

### Detecting Upper vs Full Body

```c
// Check which extension is available
if (available.meta_body_tracking) {
    // Full body — legs are real tracking data
    createInfo.bodyJointSet = XR_BODY_JOINT_SET_FULL_BODY_META;
} else if (available.fb_body_tracking) {
    // Upper body only — legs are estimated
    createInfo.bodyJointSet = XR_BODY_JOINT_SET_DEFAULT_FB;
}
```

### Retrieving Body Joints

```c
XrBodyJointLocationMETA joints[XR_BODY_JOINT_COUNT_META]; // 70
XrBodyJointLocationsMETA locations = {XR_TYPE_BODY_JOINT_LOCATIONS_META};
locations.jointCount = XR_BODY_JOINT_COUNT_META;
locations.jointLocations = joints;

XrBodyJointsLocateInfoMETA locateInfo = {XR_TYPE_BODY_JOINTS_LOCATE_INFO_META};
locateInfo.baseSpace = referenceSpace;
locateInfo.time = predictedDisplayTime;

xrLocateBodyJointsMETA(bodyTracker, &locateInfo, &locations);
```

**Check:** `locations.isActive` before accessing joints. `locations.confidence` gives overall tracking quality (0.0-1.0).

### Per-Joint Validity

Each `XrBodyJointLocationMETA` has `locationFlags`:
- `POSITION_VALID_BIT | ORIENTATION_VALID_BIT`: data is usable
- `POSITION_TRACKED_BIT | ORIENTATION_TRACKED_BIT`: actively tracked

For upper-body-only tracking, leg joints will have VALID but NOT TRACKED flags — meaning they're estimated/procedural.

## Forwarding Strategies

### Full Body (All 70 Joints)

- Raw: 70 x 28 bytes = 1960 bytes per frame
- Compact (smallest-three + fixed-point): 70 x 12 bytes = 840 bytes
- With delta compression: ~400-800 bytes typical

### Upper Body Only (First 36 Joints)

Send indices 0-7 (spine/head) + 24-55 (arms/hands):
- Raw: 36 x 28 bytes = 1008 bytes
- Compact: 36 x 12 bytes = 432 bytes

### Skeleton-Relative Encoding

Instead of absolute poses, send each joint relative to its parent:
- Reduces delta compression threshold sensitivity
- More compact: child joints have smaller ranges
- Required for retargeting to different skeleton proportions

### Retargeting Considerations

When forwarding to a receiver with different avatar proportions:
1. Send joint rotations (not positions) for chain joints
2. Receiver applies rotations to their own bone lengths
3. Only root/hips position needs absolute coordinates
4. Finger joints: use normalized curl/splay angles instead of poses

## Skeleton Definition

Query once at tracker creation:

```c
XrBodySkeletonMETA skeleton = {XR_TYPE_BODY_SKELETON_META};
skeleton.jointCount = XR_BODY_JOINT_COUNT_META;
XrBodySkeletonJointMETA skeletonJoints[XR_BODY_JOINT_COUNT_META];
skeleton.joints = skeletonJoints;
xrGetBodySkeletonMETA(bodyTracker, &skeleton);
```

Each `XrBodySkeletonJointMETA` provides:
- `joint`: parent joint index (-1 for root)
- `pose`: T-pose bind position
- Use bind poses for skinning and retargeting reference
