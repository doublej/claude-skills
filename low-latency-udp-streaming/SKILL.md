---
name: low-latency-udp-streaming
description: "Video-over-UDP for VR: packet sharding, FEC, adaptive bitrate, ALVR"
---

# Low-Latency UDP Streaming

## Core Constraints

VR streaming has unique requirements that differ from standard video streaming:

| Constraint | Target | Why |
|------------|--------|-----|
| Motion-to-photon latency | <20ms total | >20ms causes motion sickness |
| Frame delivery | Every frame matters | Dropped frames = visual judder |
| Bitrate cannot just drop | Floor ~30 Mbps | Quality below threshold causes nausea too |
| Packet loss tolerance | <0.1% without recovery | Even 1 lost shard = lost frame |
| Jitter budget | <3ms | Decoder needs consistent frame arrival |

**Key difference from regular video streaming**: you cannot simply reduce quality during congestion. Below a visual quality floor, users get sick. The system must maintain framerate even at the cost of resolution.

## Packet Sharding

### Why Shard

Encoded video frames (NALUs) are 10-500 KB. A single UDP datagram >MTU triggers IP fragmentation, which is catastrophic: losing any IP fragment drops the entire datagram, and routers may drop oversized packets entirely.

### MTU Selection

| Network | Safe payload | Notes |
|---------|-------------|-------|
| Ethernet (wired) | 1400 bytes | Leave room for IP(20) + UDP(8) + your header |
| WiFi (typical) | 1400 bytes | Same; WiFi MTU matches Ethernet |
| WiFi (with VPN/tunnel) | 1200-1300 bytes | Tunnel overhead eats into MTU |
| Loopback | 65507 bytes | No fragmentation concern |

**Rule: use 1400 bytes as default payload size.** Never assume 1500. Always leave headroom for headers and potential encapsulation.

### Shard Packet Format

```
Byte layout (per shard):
[0..3]   frame_index: u32     -- which video frame
[4..7]   shard_index: u16     -- which shard within frame (0-based)
         shard_count: u16     -- total shards for this frame
[8..15]  timestamp_ns: u64    -- capture timestamp (for RTT calc)
[16..17] stream_id: u16       -- multiplexed stream identifier
[18..]   payload              -- raw NALU bytes
```

Keep the header small (18-24 bytes). Every byte of header reduces payload capacity across thousands of packets per second.

### Sharding Implementation (Rust)

```rust
const MAX_PAYLOAD: usize = 1400 - HEADER_SIZE;

fn shard_frame(frame: &[u8], frame_idx: u32, ts: u64) -> Vec<Shard> {
    let shard_count = frame.len().div_ceil(MAX_PAYLOAD) as u16;
    frame
        .chunks(MAX_PAYLOAD)
        .enumerate()
        .map(|(i, chunk)| Shard {
            frame_index: frame_idx,
            shard_index: i as u16,
            shard_count,
            timestamp_ns: ts,
            payload: chunk.to_vec(),
        })
        .collect()
}
```

### Reassembly

Track received shards per frame. A frame is complete when `received_count == shard_count`. Set a deadline (e.g., half a frame interval). If incomplete by deadline, discard and request IDR.

```rust
struct FrameAssembler {
    shards: Vec<Option<Vec<u8>>>,
    received: u16,
    expected: u16,
    deadline: Instant,
}

impl FrameAssembler {
    fn insert(&mut self, shard: Shard) -> Option<Vec<u8>> {
        if self.shards[shard.shard_index as usize].is_some() {
            return None; // duplicate
        }
        self.shards[shard.shard_index as usize] = Some(shard.payload);
        self.received += 1;
        (self.received == self.expected).then(|| self.reassemble())
    }
}
```

## IDR Frame Recovery

### Detection

Track frame indices. If `current_frame_index > last_complete + 1`, a frame was lost.

### Recovery Protocol

1. Client detects gap or reassembly timeout
2. Client sends IDR request packet to server (small, over reliable channel or separate UDP)
3. Server signals encoder to insert IDR at next frame
4. Encoder produces IDR frame (keyframe -- full frame, no dependencies)
5. Normal decoding resumes from IDR

### Pitfalls

- **IDR frames are large** (5-10x a P-frame). At 100 Mbps, an IDR can be 500+ KB = 350+ shards. Requesting too many IDRs saturates the link.
- **Rate-limit IDR requests**: max 1 per 100ms. If loss is persistent, the problem is bandwidth, not a single dropped packet.
- **ALVR's `aggressive_keyframe_resend`**: when enabled, resends the last IDR's shards on packet loss instead of requesting a new one. Useful but doubles bandwidth during loss events.
- **AV1 codec note**: some AV1 encoders drop IDR frames or produce non-conformant keyframes. Test IDR insertion explicitly with your encoder.

## Socket Configuration

### Send/Receive Buffers

```rust
use std::net::UdpSocket;

let socket = UdpSocket::bind("0.0.0.0:0")?;

// Sender: buffer >= 2x largest frame to avoid drops during send bursts
socket.set_send_buffer_size(2 * 1024 * 1024)?; // 2 MB

// Receiver: buffer >= 1 frame interval worth of data
// At 200 Mbps, 90fps: ~278 KB per frame, so 1-2 MB is safe
socket.set_recv_buffer_size(2 * 1024 * 1024)?; // 2 MB

// Non-blocking for poll/epoll integration
socket.set_nonblocking(true)?;
```

### Platform-Specific

| Option | Linux | macOS | Effect |
|--------|-------|-------|--------|
| `SO_SNDBUF` | Kernel doubles the value | Exact value | Set 2x on macOS to match Linux behavior |
| `SO_RCVBUF` | Capped by `net.core.rmem_max` | Capped by `kern.ipc.maxsockbuf` | Raise sysctl if needed |
| `UDP_CORK` | Available | Not available | Coalesce small writes; marginal benefit |
| `SO_TXTIME` | Linux 4.19+ | Not available | Schedule packet transmission time |
| `IP_TOS` | Both | Both | Set DSCP for QoS (0xB8 = EF for real-time) |

### Packet Pacing

Do not send all shards of a frame in a tight loop. Burst transmission overwhelms WiFi TX queues and causes tail drops.

```rust
// Pace shards across the frame interval
let pace_interval = frame_interval / shard_count as u32;
for shard in &shards {
    socket.send_to(&shard.serialize(), target)?;
    std::thread::sleep(pace_interval);
    // Or better: use a timer wheel / tokio::time::interval
}
```

At 90fps with 200 shards per frame, that's ~55us between shards -- achievable with busy-wait or high-resolution timers, not `thread::sleep` (which has ~1ms granularity on most OS).

## Network Statistics

### RTT Measurement

Embed timestamps in video packets. Client echoes timestamp back in a lightweight stats packet:

```
RTT = current_time - echoed_timestamp
one_way_latency ~= RTT / 2  (approximation; asymmetric paths exist)
```

### Packet Loss Rate

```rust
struct LossTracker {
    expected_next: u32,
    received: u32,
    lost: u32,
}

impl LossTracker {
    fn record(&mut self, seq: u32) {
        if seq > self.expected_next {
            self.lost += seq - self.expected_next;
        }
        self.expected_next = seq + 1;
        self.received += 1;
    }

    fn loss_rate(&self) -> f32 {
        self.lost as f32 / (self.received + self.lost) as f32
    }
}
```

### Bandwidth Estimation

Measure bytes received over a sliding window (e.g., 500ms). Smooth with EWMA:

```
bw_estimate = alpha * measured_bw + (1 - alpha) * bw_estimate
// alpha = 0.1-0.3 for stability
```

## Adaptive Bitrate for VR

### Strategy: Step-Wise with Floor

Unlike ABR for regular video, VR ABR must respect a quality floor:

```
if loss_rate > 2% OR rtt > 30ms:
    bitrate = max(bitrate * 0.8, BITRATE_FLOOR)
    request_idr()
elif loss_rate < 0.5% AND rtt < 15ms AND bandwidth_headroom > 20%:
    bitrate = min(bitrate * 1.05, BITRATE_CAP)
// else: hold steady
```

| Parameter | Typical Value | Notes |
|-----------|--------------|-------|
| `BITRATE_FLOOR` | 30 Mbps | Below this, visual quality causes discomfort |
| `BITRATE_CAP` | 200 Mbps | Encoder/network limit |
| Ramp-up rate | 5% per interval | Conservative to avoid oscillation |
| Ramp-down rate | 20% per step | Aggressive to recover quickly |
| Measurement interval | 500ms | Balance responsiveness vs. noise |

### What to Adjust (Priority Order)

1. **Encode bitrate** -- primary lever
2. **Resolution scale** -- foveated rendering can reduce peripheral resolution
3. **Refresh rate** -- drop from 90Hz to 72Hz as last resort (noticeable)

**Never** adjust by dropping frames. Every frame must be delivered.

## FEC Strategies

See `references/fec-strategies.md` for detailed comparison and implementation patterns.

**Quick decision guide:**

| Scenario | FEC Type | Overhead |
|----------|----------|----------|
| WiFi, <1% loss | XOR parity (1 FEC per N data) | ~10-15% |
| WiFi, 1-3% loss | Reed-Solomon GF(2^8) | ~20-30% |
| Wired, <0.1% loss | None (rely on IDR recovery) | 0% |
| High loss, can't retransmit | Fountain codes (RaptorQ) | Variable |

## QUIC as Alternative Transport

### Pros
- Built-in stream multiplexing (no head-of-line blocking between streams)
- 0-RTT connection establishment
- Congestion control built-in
- Encryption included (important for wireless)

### Cons
- Encryption overhead adds ~1-2ms latency per packet
- Congestion control may conflict with VR's "must deliver" requirement
- Library maturity still limited (as of 2026)
- Cannot disable reliability per-stream in most implementations

**Verdict**: promising for control channels and audio. For video data, raw UDP with application-layer FEC still wins on latency. ALVR uses a hybrid approach: TCP/QUIC for control, UDP for video shards.

## WiFi vs. Wired Latency

| Factor | Wired | WiFi 5 (802.11ac) | WiFi 6/6E (802.11ax) |
|--------|-------|-------|---------|
| Base latency | <1ms | 2-5ms | 1-3ms |
| Jitter | <0.5ms | 2-10ms | 1-3ms |
| Packet loss | ~0% | 0.1-2% | 0.05-0.5% |
| Bandwidth | 1 Gbps+ | 200-400 Mbps real | 400-800 Mbps real |
| Interference | None | High | Medium (6 GHz less) |

### WiFi Optimization Checklist

- [ ] Use 5 GHz or 6 GHz band (never 2.4 GHz)
- [ ] 160 MHz channel width if supported
- [ ] Router within 5m line-of-sight to headset
- [ ] Disable power saving on WiFi adapter
- [ ] Dedicated SSID for VR (no other traffic)
- [ ] Set DSCP/QoS priority for VR traffic
- [ ] Monitor channel utilization; switch if >50% busy

## ALVR Integration Patterns

### Crate Structure

- `alvr_sockets` -- StreamSocket with multiplexed streams over single UDP/TCP socket
- `alvr_packets` -- Packet type definitions, serialized with bincode
- `alvr_common` -- Shared types (settings, handshake packets)

### StreamSocket Design

ALVR's StreamSocket multiplexes multiple logical streams (video=3, audio, tracking, statistics) over a single UDP socket. Each stream has independent sharding and reassembly -- no head-of-line blocking between streams.

### Connection Flow

```
1. Client broadcasts ClientHandshakePacket on UDP port 9943
2. Server responds with ServerHandshakePacket to port 9944
3. StreamSocket established on negotiated port
4. Video stream begins on stream_id=3
```

### Key Settings (from ConnectionDesc)

```rust
ConnectionDesc {
    throttling_bitrate_bits: encode_bitrate * 3/2 + audio_bitrate,
    sending_timeslot_us: 500,       // microseconds between send bursts
    limit_timeslot_packets: 0,      // 0 = unlimited
    client_recv_buffer_size: encode_bitrate_mbs * 2 + offset,
    frame_queue_size: 1,            // 1 = drop stale frames; 5 = buffer
    aggressive_keyframe_resend: false,
}
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Periodic frame drops every ~1s | WiFi power saving | Disable adapter power management |
| Gradual latency increase | Receive buffer overflow | Increase `SO_RCVBUF`; pace sends |
| Burst packet loss | TX queue overflow from send bursts | Implement packet pacing |
| IDR storm (constant keyframes) | IDR request not rate-limited | Add 100ms cooldown between requests |
| High loss on 5 GHz WiFi | DFS channel radar event | Use non-DFS channels (36-48, 149-165) |
| Works wired, fails WiFi | MTU/fragmentation | Reduce payload to 1200 bytes |
| One-way latency asymmetric | WiFi uplink slower than downlink | Normal; adjust jitter buffer accordingly |
| Decoder stalls after loss | Missing IDR recovery | Implement gap detection + IDR request |

## Deep Reference

| Reference | Use When |
|-----------|----------|
| `fec-strategies.md` | Choosing and implementing FEC; XOR vs Reed-Solomon vs fountain codes |
| `packet-format.md` | Detailed packet layouts, header fields, serialization patterns |
