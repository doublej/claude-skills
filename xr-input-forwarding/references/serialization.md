# Serialization & Network Transport Reference

## Wire Format Specification

### Packet Header (16 bytes)

```
Offset  Size  Field
0       4     Magic: 0x58524654 ("XRFT")
4       4     Sequence number (uint32, wrapping)
8       8     Timestamp (int64, XrTime nanoseconds)
```

### Source Mask (1 byte after header)

```
Bit 0: Left hand data present
Bit 1: Right hand data present
Bit 2: Face data present
Bit 3: Body data present
Bit 4: Eye gaze data present
Bit 5: Keyframe flag (full state, not delta)
Bit 6-7: Reserved
```

### Per-Source Block

```
Offset  Size  Field
0       1     Source type enum (0=left hand, 1=right, 2=face, 3=body, 4=eye)
1       2     Payload length (uint16, max 65535 bytes)
3       N     Payload data (format depends on source type)
```

## Compact Encoding Algorithms

### Smallest-Three Quaternion (6 bytes)

Exploits unit quaternion constraint: `x² + y² + z² + w² = 1`

```
Encoding:
1. Find index of component with largest absolute value
2. If that component is negative, negate entire quaternion (sign flip is valid for quats)
3. Encode remaining 3 components as signed 14-bit fixed-point [-1/√2, 1/√2]
4. Pack: [2-bit index][14-bit a][14-bit b][14-bit c] = 44 bits → 6 bytes (pad 4 bits)

Decoding:
1. Extract index and 3 components
2. Compute missing: w = sqrt(1 - a² - b² - c²)
3. Place components in correct positions based on index
```

**Range justification:** If one component is the largest, the others are each bounded by [-1/√2, 1/√2] ≈ [-0.707, 0.707]. 14 bits gives precision of ~0.0001 radians.

```c
// Encoding example
void encode_quat_smallest3(XrQuaternionf q, uint8_t out[6]) {
    float abs_vals[4] = {fabsf(q.x), fabsf(q.y), fabsf(q.z), fabsf(q.w)};
    int largest = 0;
    for (int i = 1; i < 4; i++)
        if (abs_vals[i] > abs_vals[largest]) largest = i;

    // Ensure largest component is positive
    float components[4] = {q.x, q.y, q.z, q.w};
    if (components[largest] < 0)
        for (int i = 0; i < 4; i++) components[i] = -components[i];

    // Pack 3 remaining as 14-bit signed fixed-point
    float scale = 8191.0f / 0.70710678f; // 14-bit range mapped to [-1/√2, 1/√2]
    int idx = 0;
    int16_t packed[3];
    for (int i = 0; i < 4; i++) {
        if (i == largest) continue;
        packed[idx++] = (int16_t)(components[i] * scale);
    }

    // Bit-pack: 2-bit index + 3x14-bit = 44 bits
    uint64_t bits = ((uint64_t)largest << 42)
                  | ((uint64_t)(packed[0] & 0x3FFF) << 28)
                  | ((uint64_t)(packed[1] & 0x3FFF) << 14)
                  | ((uint64_t)(packed[2] & 0x3FFF));
    for (int i = 5; i >= 0; i--) { out[i] = bits & 0xFF; bits >>= 8; }
}
```

### Fixed-Point Position (6 bytes)

For typical XR tracking ranges (±4 meters from origin):

```
Each axis: int16_t, scale = 32767 / 4.0 (0.122mm precision)
Total: 3 × 2 bytes = 6 bytes

Encoding: int16_t encoded = (int16_t)(position * (32767.0f / 4.0f));
Decoding: float position = encoded * (4.0f / 32767.0f);
```

**Range trade-off:**
- ±4m: 0.12mm precision (good for hand/body tracking)
- ±2m: 0.06mm precision (better for fingers)
- ±8m: 0.24mm precision (room-scale body)

For body tracking where the user moves around a large space, consider ±8m or send root position as float32 and child joints as relative int16.

### Face Weight Quantization (1 byte per weight)

```
Encoding: uint8_t encoded = (uint8_t)(weight * 255.0f + 0.5f);
Decoding: float weight = encoded / 255.0f;

Precision: 0.39% — imperceptible for facial animation
```

## Delta Compression

### Per-Joint Delta Detection

```c
bool joint_changed(XrPosef prev, XrPosef curr) {
    // Position threshold: 0.1mm
    float dx = curr.position.x - prev.position.x;
    float dy = curr.position.y - prev.position.y;
    float dz = curr.position.z - prev.position.z;
    if (dx*dx + dy*dy + dz*dz > 1e-8f) return true;

    // Orientation threshold: ~0.5 degrees (dot product > 0.99996)
    float dot = fabsf(
        curr.orientation.x * prev.orientation.x +
        curr.orientation.y * prev.orientation.y +
        curr.orientation.z * prev.orientation.z +
        curr.orientation.w * prev.orientation.w
    );
    return dot < 0.99996f;
}
```

### Delta Frame Format

```
[1 byte]  Joint change bitmask length (N = ceil(jointCount / 8))
[N bytes] Bitmask: 1 = joint changed, 0 = unchanged
[M × 12]  Only changed joints (compact pose encoding)
```

### Keyframe Strategy

- Send full state (keyframe) every 30-60 frames (~0.5-1s at 72Hz)
- Also send keyframe when: new client connects, tracking regained after loss, large discontinuity detected
- Mark keyframes with bit 5 in source mask

### Face Delta Compression

Face blend shapes benefit from a different strategy — threshold on weight change:

```c
// Only send weight if delta > 1/255 (below quantization noise)
bool face_weight_changed(float prev, float curr) {
    return fabsf(curr - prev) > (1.0f / 255.0f);
}
```

Face deltas are more effective than joint deltas because many blend shapes stay near zero (tongue, cheek suck, etc.).

## Bandwidth Calculations

### Per-Source Raw vs Compact vs Delta (at 72 Hz)

| Source | Raw (bytes/frame) | Compact | Delta (typical) | Raw BW | Compact BW | Delta BW |
|--------|-------------------|---------|-----------------|--------|-----------|----------|
| Hand (×2) | 1692 | 720 | ~200 | 945 kbps | 403 kbps | 112 kbps |
| Face | 289 | 79 | ~30 | 162 kbps | 44 kbps | 17 kbps |
| Body (full) | 1960 | 840 | ~400 | 1094 kbps | 470 kbps | 224 kbps |
| Eye | 30 | 14 | ~10 | 17 kbps | 8 kbps | 6 kbps |
| **All sources** | **3971** | **1653** | **~640** | **2218 kbps** | **925 kbps** | **359 kbps** |

Delta BW assumes moderate movement. Vigorous activity approaches compact BW.

### Bandwidth Budget Guidelines

- WiFi 6 (local streaming): 5+ Mbps available — use compact, skip delta
- WiFi 5 / congested: 1-2 Mbps — use delta compression
- Mobile data (5G): 0.5-1 Mbps — delta + reduced update rate
- WebRTC data channel: ~256 kbps typical — delta + face/hands only, reduce Hz

## Interpolation

### Quaternion SLERP

```c
XrQuaternionf quat_slerp(XrQuaternionf a, XrQuaternionf b, float t) {
    float dot = a.x*b.x + a.y*b.y + a.z*b.z + a.w*b.w;

    // Take shortest path
    if (dot < 0.0f) { b.x=-b.x; b.y=-b.y; b.z=-b.z; b.w=-b.w; dot=-dot; }

    // Fall back to LERP for nearly identical quaternions (avoid div by zero)
    if (dot > 0.9995f) {
        XrQuaternionf r = {
            a.x + t*(b.x-a.x), a.y + t*(b.y-a.y),
            a.z + t*(b.z-a.z), a.w + t*(b.w-a.w)
        };
        float len = sqrtf(r.x*r.x + r.y*r.y + r.z*r.z + r.w*r.w);
        r.x/=len; r.y/=len; r.z/=len; r.w/=len;
        return r;
    }

    float theta = acosf(dot);
    float sin_theta = sinf(theta);
    float wa = sinf((1.0f-t)*theta) / sin_theta;
    float wb = sinf(t*theta) / sin_theta;
    return (XrQuaternionf){
        wa*a.x + wb*b.x, wa*a.y + wb*b.y,
        wa*a.z + wb*b.z, wa*a.w + wb*b.w
    };
}
```

### Jitter Buffer

```
Target latency = 2-3 frames (28-42ms at 72Hz)

Buffer state:
  frames[]: ring buffer of received tracking frames
  play_cursor: interpolation position (behind latest by buffer depth)

Each render tick:
  t_render = current_time - buffer_latency
  Find F_prev, F_next bracketing t_render
  alpha = (t_render - F_prev.time) / (F_next.time - F_prev.time)
  Interpolate all joints with alpha
```

### Extrapolation (Use Sparingly)

When the jitter buffer runs dry (packet loss, network spike):

```c
// Linear extrapolation — max 1 frame duration
if (t_render > F_latest.time) {
    float extrap_dt = t_render - F_latest.time;
    float max_extrap = frame_interval; // e.g., 1/72 sec

    if (extrap_dt > max_extrap) {
        // Hold last pose — don't extrapolate further
        return F_latest;
    }

    // Extrapolate using velocity if available
    for (int j = 0; j < joint_count; j++) {
        pos[j] = F_latest.pos[j] + F_latest.vel[j] * extrap_dt;
        // For orientation, use angular velocity
    }
}
```

**Pitfall:** Extrapolating finger joints looks terrible — they overshoot into impossible poses. Only extrapolate wrist/root; hold finger poses.

## Transport Protocols

### UDP (Preferred for Real-Time)

- No head-of-line blocking
- Packet loss is acceptable (next frame replaces anyway)
- Add sequence numbers for ordering; discard out-of-order packets
- No need for retransmission — stale data is useless

### WebRTC DataChannel (Browser)

- Supports unreliable/unordered mode (set `ordered: false, maxRetransmits: 0`)
- Built-in NAT traversal
- ~256 kbps practical limit on congested connections — use delta compression

### TCP (Avoid for Tracking Data)

- Head-of-line blocking causes latency spikes
- Only acceptable for initial handshake, skeleton definition transfer, or non-real-time recording

### Protocol Handshake

```
Client -> Server: HELLO + supported sources + capabilities
Server -> Client: ACCEPT + negotiated sources + skeleton definitions
Client -> Server: READY
Server -> Client: [tracking frames begin]
```

Include in HELLO: protocol version, supported compact encodings, max update rate, coordinate convention.
