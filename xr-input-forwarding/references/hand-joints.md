# Hand Joint Reference

## XR_EXT_hand_tracking — 26 Joints Per Hand

### Joint Index Table

| Index | Name | Parent | Notes |
|-------|------|--------|-------|
| 0 | `PALM` | — | Virtual joint at palm center, not a bone joint |
| 1 | `WRIST` | — | Wrist root, primary attachment point |
| 2 | `THUMB_METACARPAL` | Wrist | Base of thumb |
| 3 | `THUMB_PROXIMAL` | 2 | First thumb bone |
| 4 | `THUMB_DISTAL` | 3 | Second thumb bone |
| 5 | `THUMB_TIP` | 4 | Fingertip point |
| 6 | `INDEX_METACARPAL` | Wrist | Knuckle base |
| 7 | `INDEX_PROXIMAL` | 6 | First bone after knuckle |
| 8 | `INDEX_INTERMEDIATE` | 7 | Middle bone |
| 9 | `INDEX_DISTAL` | 8 | Last bone |
| 10 | `INDEX_TIP` | 9 | Fingertip |
| 11 | `MIDDLE_METACARPAL` | Wrist | |
| 12 | `MIDDLE_PROXIMAL` | 11 | |
| 13 | `MIDDLE_INTERMEDIATE` | 12 | |
| 14 | `MIDDLE_DISTAL` | 13 | |
| 15 | `MIDDLE_TIP` | 14 | |
| 16 | `RING_METACARPAL` | Wrist | |
| 17 | `RING_PROXIMAL` | 16 | |
| 18 | `RING_INTERMEDIATE` | 17 | |
| 19 | `RING_DISTAL` | 18 | |
| 20 | `RING_TIP` | 19 | |
| 21 | `LITTLE_METACARPAL` | Wrist | |
| 22 | `LITTLE_PROXIMAL` | 21 | |
| 23 | `LITTLE_INTERMEDIATE` | 22 | |
| 24 | `LITTLE_DISTAL` | 23 | |
| 25 | `LITTLE_TIP` | 24 | |

### Joint Hierarchy (Tree View)

```
WRIST (1)
├── THUMB_METACARPAL (2)
│   └── THUMB_PROXIMAL (3)
│       └── THUMB_DISTAL (4)
│           └── THUMB_TIP (5)
├── INDEX_METACARPAL (6)
│   └── INDEX_PROXIMAL (7)
│       └── INDEX_INTERMEDIATE (8)
│           └── INDEX_DISTAL (9)
│               └── INDEX_TIP (10)
├── MIDDLE_METACARPAL (11)
│   └── MIDDLE_PROXIMAL (12)
│       └── MIDDLE_INTERMEDIATE (13)
│           └── MIDDLE_DISTAL (14)
│               └── MIDDLE_TIP (15)
├── RING_METACARPAL (16)
│   └── RING_PROXIMAL (17)
│       └── RING_INTERMEDIATE (18)
│           └── RING_DISTAL (19)
│               └── RING_TIP (20)
└── LITTLE_METACARPAL (21)
    └── LITTLE_PROXIMAL (22)
        └── LITTLE_INTERMEDIATE (23)
            └── LITTLE_DISTAL (24)
                └── LITTLE_TIP (25)

PALM (0) — virtual joint, not in bone hierarchy
```

### XrHandJointLocationEXT Structure

```c
typedef struct XrHandJointLocationEXT {
    XrSpaceLocationFlags locationFlags;  // validity + tracked bits
    XrPosef              pose;           // position + orientation
} XrHandJointLocationEXT;
```

### Per-Joint Radius

Retrieved via optional `XrHandJointVelocitiesEXT` and `XrHandTrackingScaleFB`:

```c
// Chain to get radii
XrHandJointRadiusEXT radii[XR_HAND_JOINT_COUNT_EXT];
// ... (not standard — radii come from velocity extension or FB scale)
```

**Typical radii (approximate, in meters):**

| Joint Group | Radius |
|-------------|--------|
| Tips | 0.005 - 0.008 |
| Distal/Intermediate | 0.007 - 0.010 |
| Proximal | 0.010 - 0.013 |
| Metacarpal | 0.012 - 0.015 |
| Wrist | 0.015 - 0.020 |
| Palm | 0.020 - 0.025 |

### Joint Velocities (Optional)

```c
XrHandJointVelocityEXT velocities[XR_HAND_JOINT_COUNT_EXT];
XrHandJointVelocitiesEXT velData = {XR_TYPE_HAND_JOINT_VELOCITIES_EXT};
velData.jointCount = XR_HAND_JOINT_COUNT_EXT;
velData.jointVelocities = velocities;
// Chain into locations.next
locations.next = &velData;
```

Each velocity has:
- `velocityFlags` — which components are valid
- `linearVelocity` — m/s, in base space
- `angularVelocity` — rad/s, in base space

Useful for: gesture recognition velocity thresholds, predictive forwarding.

## XR_FB_hand_tracking_mesh

### Mesh Query (One-Time)

```c
// Get buffer sizes
XrHandTrackingMeshFB mesh = {XR_TYPE_HAND_TRACKING_MESH_FB};
xrGetHandMeshFB(handTracker, &mesh); // fills jointCapacityInput, vertexCapacityInput, indexCapacityInput

// Allocate and query
XrPosef jointBindPoses[XR_HAND_JOINT_COUNT_EXT];
float jointRadii[XR_HAND_JOINT_COUNT_EXT];
XrHandJointEXT jointParents[XR_HAND_JOINT_COUNT_EXT];
XrVector3f vertexPositions[mesh.vertexCapacityInput];
XrVector3f vertexNormals[mesh.vertexCapacityInput];
XrVector2f vertexUVs[mesh.vertexCapacityInput];
XrHandTrackingMeshBlendWeightFB blendWeights[mesh.vertexCapacityInput]; // per-vertex skinning
int16_t indices[mesh.indexCapacityInput];

mesh.jointBindPoses = jointBindPoses;
mesh.jointRadii = jointRadii;
mesh.jointParents = jointParents;
mesh.vertexPositions = vertexPositions;
mesh.vertexNormals = vertexNormals;
mesh.vertexUVs = vertexUVs;
mesh.vertexBlendWeights = blendWeights; // not present in all versions
mesh.indices = indices;

xrGetHandMeshFB(handTracker, &mesh);
```

### Skinning the Mesh

The mesh is skinned to the 26 hand joints using linear blend skinning (LBS):
1. Each vertex has blend weights referencing up to 4 joints
2. Apply joint transforms from `xrLocateHandJointsEXT` to bind poses
3. Transform vertices using weighted sum

**Pitfall:** Mesh topology (index buffer) is static per user but vertex count may differ between users. Never hardcode vertex/index counts.

### Forwarding Mesh Data

For mesh forwarding, only send:
- Joint poses (already forwarded for hand tracking)
- The mesh definition once at connection setup (topology is static)
- Receiver performs skinning locally using forwarded joint poses

Do NOT forward per-frame vertex positions — too expensive. Let the receiver skin locally.

## Coordinate Conventions

All hand joint poses are in the coordinate system of the `baseSpace` passed to `xrLocateHandJointsEXT`.

Joint orientations follow the convention:
- **+X**: points along the bone toward the next joint
- **+Y**: perpendicular, toward the back of the hand (dorsal)
- **-Z**: follows the right-hand rule

For forwarding, prefer sending joints relative to the WRIST joint to decouple from world space.
