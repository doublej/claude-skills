# Packet Formats for Low-Latency UDP Streaming

## Video Shard Packet

Primary data unit for video transmission. Each UDP datagram carries one shard.

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        frame_index (u32)                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        shard_index (u16)      |        shard_count (u16)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     timestamp_ns (u64)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        stream_id (u16)        |     flags (u8)  | reserved(u8)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         payload ...                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Total header: 20 bytes
Max payload: MTU - IP(20) - UDP(8) - header(20) = 1452 bytes (at 1500 MTU)
Safe payload: 1400 - 20 = 1380 bytes
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `frame_index` | u32 | Monotonically increasing frame counter. Wraps at 2^32 (~13 hours at 90fps). |
| `shard_index` | u16 | 0-based index of this shard within the frame. |
| `shard_count` | u16 | Total shards for this frame (data + FEC). |
| `timestamp_ns` | u64 | Capture timestamp in nanoseconds (monotonic clock). |
| `stream_id` | u16 | Logical stream (video=3, audio=1, tracking=2 in ALVR convention). |
| `flags` | u8 | Bitfield (see below). |
| `reserved` | u8 | Zero. Future use. |

### Flags Bitfield

```
Bit 0: is_idr        -- This frame is an IDR/keyframe
Bit 1: is_fec        -- This shard is FEC parity, not data
Bit 2: is_last_nalu  -- Last NALU in access unit (for multi-NALU frames)
Bit 3-7: reserved
```

### Serialization

Use fixed-size, little-endian encoding. Avoid bincode/serde overhead in the hot path -- the header is small enough to serialize manually.

```rust
impl Shard {
    fn serialize(&self, buf: &mut [u8]) {
        buf[0..4].copy_from_slice(&self.frame_index.to_le_bytes());
        buf[4..6].copy_from_slice(&self.shard_index.to_le_bytes());
        buf[6..8].copy_from_slice(&self.shard_count.to_le_bytes());
        buf[8..16].copy_from_slice(&self.timestamp_ns.to_le_bytes());
        buf[16..18].copy_from_slice(&self.stream_id.to_le_bytes());
        buf[18] = self.flags;
        buf[19] = 0; // reserved
        buf[20..20 + self.payload.len()].copy_from_slice(&self.payload);
    }

    fn deserialize(buf: &[u8]) -> Self {
        Self {
            frame_index: u32::from_le_bytes(buf[0..4].try_into().unwrap()),
            shard_index: u16::from_le_bytes(buf[4..6].try_into().unwrap()),
            shard_count: u16::from_le_bytes(buf[6..8].try_into().unwrap()),
            timestamp_ns: u64::from_le_bytes(buf[8..16].try_into().unwrap()),
            stream_id: u16::from_le_bytes(buf[16..18].try_into().unwrap()),
            flags: buf[18],
            payload: buf[20..].to_vec(),
        }
    }
}
```

## IDR Request Packet

Sent from client to server when frame loss is detected.

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  type (u8)=1  |   reserved    |     last_received_frame (u32) ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ... (cont)    |        timestamp_ns (u64)                     ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ... (cont)                                                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Total: 14 bytes
```

## Statistics Packet

Periodic client-to-server report (every 100-500ms).

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  type (u8)=2  |   reserved    |      frames_received (u32)   ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ...(cont)     |        frames_lost (u32)                     ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ...(cont)     |        shards_received (u32)                 ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ...(cont)     |        shards_lost (u32)                     ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ...(cont)     |        echo_timestamp_ns (u64)               ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ...                           |  decode_queue_len (u16)       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        battery_pct (u8)       |   thermal_state (u8)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Total: 28 bytes
```

The `echo_timestamp_ns` field echoes the most recent `timestamp_ns` received from the server, enabling RTT calculation without clock synchronization.

## Bitrate Adjustment Packet

Server-to-client notification of bitrate/quality change.

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  type (u8)=3  |   reserved    |   target_bitrate_kbps (u32)  ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ...(cont)     |  resolution_scale (u16, fixed 8.8)            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Total: 8 bytes
```

## ALVR Handshake Packets

ALVR uses bincode-serialized Rust structs for handshake. Key fields:

### ClientHandshakePacket (UDP port 9943)

```rust
struct ClientHandshakePacket {
    packet_type: u32,           // always 1
    alvr_name: [u8; 4],         // b"ALVR"
    version: [u8; 32],          // semver string, null-terminated
    device_name: [u8; 32],      // e.g. "Quest 3"
    client_refresh_rate: u16,   // 72, 90, 120
    render_width: u32,
    render_height: u32,
    client_fov: [Fov; 2],       // per-eye field of view
}
```

### ServerHandshakePacket (UDP port 9944)

```rust
struct ServerHandshakePacket {
    packet_type: u32,
    codec: u32,                 // 0=H.264, 1=HEVC
    video_width: u32,
    video_height: u32,
    buffer_size_bytes: u32,
    frame_queue_size: u32,
    refresh_rate: u8,
    stream_mic: bool,
    foveation_mode: u8,
    foveation_strength: f32,
    foveation_shape: f32,
    foveation_vertical_offset: f32,
    web_gui_url: [u8; 32],
}
```

## Packet Type Identification

When multiplexing packet types over a single socket, use the first byte as a type discriminator:

| Type byte | Packet | Direction |
|-----------|--------|-----------|
| 0 | Video shard | Server -> Client |
| 1 | IDR request | Client -> Server |
| 2 | Statistics | Client -> Server |
| 3 | Bitrate adjustment | Server -> Client |
| 4 | Audio shard | Server -> Client |
| 5 | Tracking data | Client -> Server |

## Design Principles

1. **Fixed-size headers**: avoid variable-length encoding in the hot path
2. **Little-endian**: matches x86/ARM (most VR hardware)
3. **Minimal allocations**: deserialize into pre-allocated buffers
4. **No string fields** in data packets: use numeric IDs
5. **Timestamp everything**: enables RTT, jitter, and ordering analysis
