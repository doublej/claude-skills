# Face Blend Shapes Reference

## XR_FB_face_tracking2 — 70 Blend Shape Weights

### Blend Shapes by Category

#### Brow (6)

| Index | Name | Description |
|-------|------|-------------|
| 0 | `BROW_LOWERER_L` | Left brow pulls down |
| 1 | `BROW_LOWERER_R` | Right brow pulls down |
| 2 | `CHEEK_RAISER_L` | Raises left cheek (affects lower brow) |
| 3 | `CHEEK_RAISER_R` | Raises right cheek |
| 4 | `INNER_BROW_RAISER_L` | Inner left brow up |
| 5 | `INNER_BROW_RAISER_R` | Inner right brow up |

#### Eye (14)

| Index | Name | Description |
|-------|------|-------------|
| 6 | `OUTER_BROW_RAISER_L` | Outer left brow up |
| 7 | `OUTER_BROW_RAISER_R` | Outer right brow up |
| 8 | `EYES_CLOSED_L` | Left eye closes (upper lid down) |
| 9 | `EYES_CLOSED_R` | Right eye closes |
| 10 | `EYES_LOOK_DOWN_L` | Left eye looks down |
| 11 | `EYES_LOOK_DOWN_R` | Right eye looks down |
| 12 | `EYES_LOOK_LEFT_L` | Left eye looks left |
| 13 | `EYES_LOOK_LEFT_R` | Right eye looks left |
| 14 | `EYES_LOOK_RIGHT_L` | Left eye looks right |
| 15 | `EYES_LOOK_RIGHT_R` | Right eye looks right |
| 16 | `EYES_LOOK_UP_L` | Left eye looks up |
| 17 | `EYES_LOOK_UP_R` | Right eye looks up |
| 18 | `LID_TIGHTENER_L` | Squints left eye |
| 19 | `LID_TIGHTENER_R` | Squints right eye |

#### Nose & Cheek (6)

| Index | Name | Description |
|-------|------|-------------|
| 20 | `NOSE_WRINKLER_L` | Left side of nose wrinkles up |
| 21 | `NOSE_WRINKLER_R` | Right side of nose wrinkles up |
| 22 | `CHEEK_PUFF_L` | Left cheek inflates |
| 23 | `CHEEK_PUFF_R` | Right cheek inflates |
| 24 | `CHEEK_SUCK_L` | Left cheek sucks in |
| 25 | `CHEEK_SUCK_R` | Right cheek sucks in |

#### Jaw (4)

| Index | Name | Description |
|-------|------|-------------|
| 26 | `JAW_DROP` | Jaw opens |
| 27 | `JAW_SIDEWAYS_LEFT` | Jaw shifts left |
| 28 | `JAW_SIDEWAYS_RIGHT` | Jaw shifts right |
| 29 | `JAW_THRUST` | Jaw moves forward |

#### Lip Upper (10)

| Index | Name | Description |
|-------|------|-------------|
| 30 | `UPPER_LIP_RAISER_L` | Left upper lip raises (sneer) |
| 31 | `UPPER_LIP_RAISER_R` | Right upper lip raises |
| 32 | `LIP_CORNER_PULLER_L` | Left smile |
| 33 | `LIP_CORNER_PULLER_R` | Right smile |
| 34 | `LIP_CORNER_DEPRESSOR_L` | Left frown |
| 35 | `LIP_CORNER_DEPRESSOR_R` | Right frown |
| 36 | `LIP_STRETCHER_L` | Left lip stretches sideways |
| 37 | `LIP_STRETCHER_R` | Right lip stretches sideways |
| 38 | `LIP_TIGHTENER_L` | Left lip tightens |
| 39 | `LIP_TIGHTENER_R` | Right lip tightens |

#### Lip Lower & Mouth (14)

| Index | Name | Description |
|-------|------|-------------|
| 40 | `LOWER_LIP_DEPRESSOR_L` | Left lower lip drops |
| 41 | `LOWER_LIP_DEPRESSOR_R` | Right lower lip drops |
| 42 | `LIP_PRESSOR_L` | Presses left lips together |
| 43 | `LIP_PRESSOR_R` | Presses right lips together |
| 44 | `LIPS_TOWARD` | Both lips move toward each other |
| 45 | `LIP_FUNNELER_LB` | Left bottom lip funnels |
| 46 | `LIP_FUNNELER_LT` | Left top lip funnels |
| 47 | `LIP_FUNNELER_RB` | Right bottom lip funnels |
| 48 | `LIP_FUNNELER_RT` | Right top lip funnels |
| 49 | `LIP_PUCKER_L` | Left lip pucker |
| 50 | `LIP_PUCKER_R` | Right lip pucker |
| 51 | `LIP_SUCK_LB` | Suck left bottom lip |
| 52 | `LIP_SUCK_LT` | Suck left top lip |
| 53 | `LIP_SUCK_RB` | Suck right bottom lip |

#### Lip Additional & Chin (6)

| Index | Name | Description |
|-------|------|-------------|
| 54 | `LIP_SUCK_RT` | Suck right top lip |
| 55 | `MOUTH_LEFT` | Mouth shifts left |
| 56 | `MOUTH_RIGHT` | Mouth shifts right |
| 57 | `CHIN_RAISER_B` | Chin boss raises (chin bump) |
| 58 | `CHIN_RAISER_T` | Upper chin raises |
| 59 | `DIMPLER_L` | Left dimple |

#### Supplementary (10)

| Index | Name | Description |
|-------|------|-------------|
| 60 | `DIMPLER_R` | Right dimple |
| 61 | `TONGUE_TIP_INTERDENTAL` | Tongue tip between teeth |
| 62 | `TONGUE_TIP_ALVEOLAR` | Tongue tip at alveolar ridge |
| 63 | `TONGUE_FRONT_DORSAL_PALATE` | Front tongue to palate |
| 64 | `TONGUE_MID_DORSAL_PALATE` | Mid tongue to palate |
| 65 | `TONGUE_BACK_DORSAL_VELAR` | Back tongue to soft palate |
| 66 | `TONGUE_OUT` | Tongue protrusion |
| 67 | `TONGUE_RETREAT` | Tongue pulls back |
| 68 | `UPPER_LIP_RAISER_L_2` | Secondary left upper lip raiser |
| 69 | `UPPER_LIP_RAISER_R_2` | Secondary right upper lip raiser |

## ARKit Mapping (52 Blend Shapes)

For cross-platform compatibility, map FB indices to ARKit blend shape names.

### Direct Mappings

| FB Index | FB Name | ARKit Name |
|----------|---------|-----------|
| 8 | `EYES_CLOSED_L` | `eyeBlinkLeft` |
| 9 | `EYES_CLOSED_R` | `eyeBlinkRight` |
| 10 | `EYES_LOOK_DOWN_L` | `eyeLookDownLeft` |
| 11 | `EYES_LOOK_DOWN_R` | `eyeLookDownRight` |
| 12 | `EYES_LOOK_LEFT_L` | `eyeLookInLeft` |
| 13 | `EYES_LOOK_LEFT_R` | `eyeLookInRight` |
| 14 | `EYES_LOOK_RIGHT_L` | `eyeLookOutLeft` |
| 15 | `EYES_LOOK_RIGHT_R` | `eyeLookOutRight` |
| 16 | `EYES_LOOK_UP_L` | `eyeLookUpLeft` |
| 17 | `EYES_LOOK_UP_R` | `eyeLookUpRight` |
| 18 | `LID_TIGHTENER_L` | `eyeSquintLeft` |
| 19 | `LID_TIGHTENER_R` | `eyeSquintRight` |
| 6 | `OUTER_BROW_RAISER_L` | `browOuterUpLeft` |
| 7 | `OUTER_BROW_RAISER_R` | `browOuterUpRight` |
| 0 | `BROW_LOWERER_L` | `browDownLeft` |
| 1 | `BROW_LOWERER_R` | `browDownRight` |
| 4 | `INNER_BROW_RAISER_L` | `browInnerUp` (combined L+R) |
| 26 | `JAW_DROP` | `jawOpen` |
| 27 | `JAW_SIDEWAYS_LEFT` | `jawLeft` |
| 28 | `JAW_SIDEWAYS_RIGHT` | `jawRight` |
| 29 | `JAW_THRUST` | `jawForward` |
| 32 | `LIP_CORNER_PULLER_L` | `mouthSmileLeft` |
| 33 | `LIP_CORNER_PULLER_R` | `mouthSmileRight` |
| 34 | `LIP_CORNER_DEPRESSOR_L` | `mouthFrownLeft` |
| 35 | `LIP_CORNER_DEPRESSOR_R` | `mouthFrownRight` |
| 55 | `MOUTH_LEFT` | `mouthLeft` |
| 56 | `MOUTH_RIGHT` | `mouthRight` |
| 22 | `CHEEK_PUFF_L` | `cheekPuff` (combined L+R) |
| 20 | `NOSE_WRINKLER_L` | `noseSneerLeft` |
| 21 | `NOSE_WRINKLER_R` | `noseSneerRight` |
| 66 | `TONGUE_OUT` | `tongueOut` |
| 2 | `CHEEK_RAISER_L` | `cheekSquintLeft` |
| 3 | `CHEEK_RAISER_R` | `cheekSquintRight` |

### Derived/Combined Mappings

Some ARKit shapes need combining multiple FB weights:

| ARKit Name | Derivation |
|-----------|-----------|
| `browInnerUp` | `max(INNER_BROW_RAISER_L, INNER_BROW_RAISER_R)` |
| `cheekPuff` | `max(CHEEK_PUFF_L, CHEEK_PUFF_R)` |
| `mouthPucker` | `max(LIP_PUCKER_L, LIP_PUCKER_R)` |
| `mouthFunnel` | `mean(LIP_FUNNELER_LB, LIP_FUNNELER_LT, LIP_FUNNELER_RB, LIP_FUNNELER_RT)` |
| `mouthClose` | `LIPS_TOWARD` |
| `mouthShrugUpper` | `mean(UPPER_LIP_RAISER_L, UPPER_LIP_RAISER_R)` |
| `mouthShrugLower` | `mean(LOWER_LIP_DEPRESSOR_L, LOWER_LIP_DEPRESSOR_R)` |
| `mouthRollUpper` | `mean(LIP_SUCK_LT, LIP_SUCK_RT)` |
| `mouthRollLower` | `mean(LIP_SUCK_LB, LIP_SUCK_RB)` |
| `mouthUpperUpLeft` | `UPPER_LIP_RAISER_L` |
| `mouthUpperUpRight` | `UPPER_LIP_RAISER_R` |
| `mouthLowerDownLeft` | `LOWER_LIP_DEPRESSOR_L` |
| `mouthLowerDownRight` | `LOWER_LIP_DEPRESSOR_R` |
| `mouthStretchLeft` | `LIP_STRETCHER_L` |
| `mouthStretchRight` | `LIP_STRETCHER_R` |
| `mouthPressLeft` | `LIP_PRESSOR_L` |
| `mouthPressRight` | `LIP_PRESSOR_R` |
| `mouthDimpleLeft` | `DIMPLER_L` |
| `mouthDimpleRight` | `DIMPLER_R` |
| `eyeWideLeft` | `1.0 - EYES_CLOSED_L` (inverse, approximate) |
| `eyeWideRight` | `1.0 - EYES_CLOSED_R` (inverse, approximate) |

### FB-Only Blend Shapes (No ARKit Equivalent)

These 18 shapes exist only in FB tracking — useful for high-fidelity forwarding:
- Tongue articulation (indices 61-65, 67): precise tongue placement
- Secondary lip raisers (68-69): subtle upper lip motion
- Chin details (57-58): chin boss movement
- Cheek suck (24-25): concave cheek motion
- Lip tighteners (38-39): compression

## Confidence Values

```c
float confidences[XR_FACE_CONFIDENCE2_COUNT_FB]; // 2 values
// [0] = XR_FACE_CONFIDENCE2_LOWER_FACE_FB — jaw, lips, chin, cheeks
// [1] = XR_FACE_CONFIDENCE2_UPPER_FACE_FB — brow, eyes, nose
```

- Range: [0.0, 1.0]
- Below ~0.2: unreliable (face partially occluded, poor lighting)
- Below ~0.5: caution — blend toward neutral
- Above ~0.7: reliable tracking

**Recommendation:** When forwarding, include confidence values. Let the receiver decide the threshold for application (animation, lip sync, etc.).

## Calibration & Per-User Normalization

FB face tracking does NOT auto-calibrate to "neutral face." A user's resting expression may produce non-zero weights. Solutions:

1. **Capture neutral baseline:** Record 1-2 seconds of "relaxed face," average the weights
2. **Subtract baseline:** `normalized = clamp(raw - baseline, 0, 1)`
3. **Scale to range:** Some users have smaller expression range — normalize based on observed min/max per weight
4. **Recalibrate on request:** Provide a "recalibrate" action in the UI

**Pitfall:** Baseline drift occurs as the headset shifts on the face. Consider periodic recalibration or a running average.
