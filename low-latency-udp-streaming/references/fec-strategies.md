# FEC Strategies for Low-Latency Video Streaming

## When to Use FEC vs. Retransmission

| Method | Latency cost | Best when |
|--------|-------------|-----------|
| **FEC only** | 0 extra RTT | RTT > frame_interval; loss is random |
| **ARQ (retransmit)** | +1 RTT per loss | RTT < 5ms; loss is rare |
| **Hybrid FEC + ARQ** | FEC covers most; ARQ catches rest | WiFi VR (typical) |

For VR over WiFi: **FEC is primary, ARQ is fallback.** A retransmission round-trip of 5-10ms on WiFi often exceeds the frame budget.

## XOR Parity FEC

Simplest scheme. XOR all N data packets to produce 1 parity packet. Recovers exactly 1 loss out of N+1 packets.

### Implementation

```rust
fn compute_xor_parity(shards: &[Vec<u8>]) -> Vec<u8> {
    let max_len = shards.iter().map(|s| s.len()).max().unwrap_or(0);
    let mut parity = vec![0u8; max_len];
    for shard in shards {
        for (i, &byte) in shard.iter().enumerate() {
            parity[i] ^= byte;
        }
    }
    parity
}

fn recover_missing(received: &[Option<Vec<u8>>], parity: &[u8]) -> Option<Vec<u8>> {
    let missing_count = received.iter().filter(|s| s.is_none()).count();
    if missing_count != 1 {
        return None; // can only recover exactly 1
    }
    let max_len = parity.len();
    let mut recovered = parity.to_vec();
    for shard in received.iter().flatten() {
        for (i, &byte) in shard.iter().enumerate() {
            recovered[i] ^= byte;
        }
    }
    Some(recovered)
}
```

### Grouping Strategies

**Sequential grouping** (simple):
```
Data:   [0][1][2][3]  [4][5][6][7]  ...
FEC:         [P0]          [P1]
```
Group size N=4: one parity per 4 data packets. 25% overhead. Recovers 1 loss per group.

**Interleaved grouping** (burst-resistant):
```
Data:   [0][1][2][3][4][5][6][7]
FEC P0:  0     2     4     6      (even indices)
FEC P1:    1     3     5     7    (odd indices)
```
Consecutive packet losses (common in WiFi) hit different FEC groups, improving recovery.

**Staircase / sliding window** (lower latency):
```
FEC[i] = XOR(data[i-3], data[i-2], data[i-1], data[i])
```
Each FEC packet covers a sliding window. No need to wait for group boundary. Adds only 1 packet of latency.

### Limitations

- Recovers exactly 1 loss per group
- Recovery probability drops to ~50% for 2 losses (depends on grouping)
- Collapses at 3+ losses per group

## Reed-Solomon FEC

MDS (Maximum Distance Separable) code: from N data + K parity packets, any N of the N+K packets suffice to recover all data.

### When to Choose RS over XOR

- Loss rate >1% sustained
- Large frames with many shards (50+ per frame)
- Need guaranteed recovery up to K losses

### Parameters

```
N = number of data shards
K = number of parity shards (recovery capacity)
Overhead = K / N

Typical for VR WiFi:
  N=200 shards, K=20 parity → 10% overhead, recovers up to 20 lost shards
  N=200 shards, K=40 parity → 20% overhead, recovers up to 40 lost shards
```

### Implementation (Rust)

Use the `reed-solomon-erasure` crate (GF(2^8)):

```rust
use reed_solomon_erasure::galois_8::ReedSolomon;

let rs = ReedSolomon::new(data_shard_count, parity_shard_count)?;

// Encode: shards must all be same length (pad shorter ones)
let mut shards: Vec<Vec<u8>> = data_shards; // N data shards
shards.extend(vec![vec![0u8; shard_size]; parity_shard_count]); // K empty parity
rs.encode(&mut shards)?;
// shards[N..N+K] now contain parity data

// Decode: mark missing shards as None
let mut received: Vec<Option<Vec<u8>>> = shards.into_iter().map(Some).collect();
received[lost_index_1] = None;
received[lost_index_2] = None;
rs.reconstruct(&mut received)?;
// All shards restored
```

### Performance Considerations

| Operation | Cost | Notes |
|-----------|------|-------|
| Encode | O(N*K) GF multiplications | ~1ms for N=200, K=20 on modern CPU |
| Decode (no loss) | 0 | Just drop parity shards |
| Decode (with loss) | O(N*K) + matrix inversion | ~2-5ms for typical VR parameters |

RS decode only runs when packets are actually lost, so the common path (no loss) has zero decode overhead.

### Padding for Variable-Length Shards

RS requires all shards to be the same length. Two approaches:

1. **Zero-pad** shorter shards to max length, include original length in header
2. **Fixed-size shards** with last shard padded, total payload length in frame header

Option 2 is simpler and avoids per-shard length tracking.

## Fountain Codes (RaptorQ)

Rateless erasure codes: generate unlimited parity symbols from data. Receiver needs any N+epsilon symbols (where epsilon is small overhead, ~2-5%).

### Pros
- No need to decide K (parity count) upfront
- Sender keeps generating parity until receiver ACKs
- Near-optimal recovery at any loss rate

### Cons
- Higher computational cost than RS for small K
- More complex implementation
- Slight overhead (~2-5%) over theoretical minimum

### When to Use
- Loss rate is unpredictable or varies widely
- Very large frames (1000+ shards)
- Network path has highly variable characteristics

For typical VR streaming (predictable WiFi, 50-300 shards per frame), RS is simpler and sufficient.

## Adaptive FEC

Adjust FEC overhead based on measured loss rate:

```rust
fn compute_fec_ratio(loss_rate: f32) -> f32 {
    match loss_rate {
        r if r < 0.001 => 0.0,    // <0.1%: no FEC, rely on IDR recovery
        r if r < 0.005 => 0.05,   // <0.5%: minimal XOR parity
        r if r < 0.02  => 0.10,   // <2%: RS with 10% overhead
        r if r < 0.05  => 0.20,   // <5%: RS with 20% overhead
        _              => 0.30,   // >5%: aggressive RS + consider bitrate reduction
    }
}
```

Update FEC parameters every 1-2 seconds based on rolling loss statistics. Do not react to single-packet events.

## FEC + Sharding Integration

```
Frame encode → NALU bytes
    → split into N data shards (each ≤ MAX_PAYLOAD)
    → RS encode to produce K parity shards
    → send N+K shards as UDP packets
    → receiver collects shards, RS decode if needed
    → reassemble NALU → decode frame
```

The parity shards use the same packet format as data shards but with `shard_index >= N` to distinguish them. The receiver tracks both data and parity arrivals.

## Latency Impact

| FEC Type | Added latency | Notes |
|----------|--------------|-------|
| XOR (sliding window) | ~0 | Parity computed on-the-fly |
| XOR (block) | Up to group_size * send_interval | Must wait for full group |
| Reed-Solomon | ~1-2ms encode + 0-5ms decode | Decode only on loss |
| RaptorQ | ~2-5ms encode + 2-5ms decode | Higher fixed cost |

For VR: prefer sliding-window XOR for low-loss scenarios, RS for moderate loss. Switch dynamically based on measured conditions.
