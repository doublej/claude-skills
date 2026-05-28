---
name: stream-audio
description: "Low-latency audio capture/encoding for VR: WASAPI, PipeWire, Opus, CPAL"
---

<setup_checklist>

Before Writing Code

1. **Identify platform**: Windows (WASAPI) / Linux (PipeWire/PulseAudio) / cross-platform (CPAL)
2. **Determine audio path**: game audio capture (loopback) vs microphone input vs virtual mic forwarding
3. **Check existing setup**: sample rate, channel count, buffer sizes already in use
4. **Identify codec needs**: Opus (networked) vs raw PCM (local/high bandwidth)

</setup_checklist>

<core_architecture>

VR audio pipeline has two directions:

```
Game Audio (PC) ──capture──> encode ──network──> decode ──playback──> Headset speakers
Headset Mic     ──capture──> encode ──network──> decode ──playback──> Virtual mic (PC)
```

### Latency Budget

Total motion-to-photon target: 20ms. Audio gets a slice of that.

| Stage | Target | Notes |
|-------|--------|-------|
| Capture | 1-3ms | WASAPI exclusive: ~1ms, shared: ~3ms, PipeWire: ~2ms |
| Encode | 0.5-2.5ms | Opus 10ms frame = 10ms algorithmic delay; 2.5ms with restricted low delay |
| Network | 1-5ms | WiFi 6/6E on same subnet |
| Jitter buffer | 5-15ms | Trade-off: too small = glitches, too large = desync |
| Decode + playback | 1-3ms | Opus decode is fast; playback buffer adds latency |
| **Total** | **~10-30ms** | Acceptable for VR |

</core_architecture>

<audio_capture>

### CPAL (Cross-Platform, Rust)

Primary crate for device enumeration and stream building. ALVR uses `cpal = "0.15"` (check your version).

```rust
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::{BufferSize, SampleFormat, StreamConfig};

// Device enumeration
let host = cpal::default_host();
let device = host.default_output_device().unwrap(); // for loopback
let config = device.default_output_config()?;

// Build capture stream — use build_input_stream_raw for runtime format
let stream = device.build_input_stream_raw(
    &StreamConfig {
        channels: config.channels(),
        sample_rate: config.sample_rate(),
        buffer_size: BufferSize::Default, // or BufferSize::Fixed(256)
    },
    config.sample_format(),
    move |data: &cpal::Data, _info: &cpal::InputCallbackInfo| {
        // Convert to i16 PCM, send to encoder/network
        let bytes = data.bytes();
        // ... process
    },
    move |err| eprintln!("Stream error: {err}"),
    None,
)?;
stream.play()?;
```

**Key CPAL pitfalls:**
- Loopback devices on Windows report as output devices but need `build_input_stream_raw` -- fall back to `default_output_config()` when `default_input_config()` fails
- `BufferSize::Fixed(n)` is a *request*, not guaranteed -- backend may ignore it
- Sample format varies per device (F32, I16, U16) -- always check `config.sample_format()`
- Stream callback runs on a real-time audio thread -- no allocations, no locks, no I/O

### WASAPI (Windows)

For lowest latency, use WASAPI exclusive mode directly (bypasses Windows audio mixer).

| Mode | Latency | Sharing | Use Case |
|------|---------|---------|----------|
| Shared | 3-10ms | Yes | Loopback capture (game audio) |
| Exclusive | ~1ms | No | Dedicated mic input |
| Shared loopback | 3-10ms | Yes | Capture desktop/game output |

**WASAPI exclusive mode gotcha:** Only one app can use the device. If another app has it, `build_input_stream` fails. Always fall back to shared mode.

### PipeWire / PulseAudio (Linux)

PipeWire is the modern standard; PulseAudio compatibility layer works but adds latency.

```rust
// PipeWire stream setup (ALVR pattern)
let stream = pw::stream::Stream::new(
    &core,
    "alvr-audio",
    pw::properties::properties! {
        *pw::keys::MEDIA_CLASS => "Audio/Sink",    // Capture game audio
        // or "Audio/Source" for virtual mic output
        *pw::keys::MEDIA_ROLE => "Game",
    },
)?;
```

**PipeWire node types:**
- `Audio/Sink` -- receives audio (use for capturing game output)
- `Audio/Source` -- produces audio (use for virtual microphone)
- Monitor sources -- capture what a sink is playing (like PulseAudio monitor)

See `references/platform-audio.md` for PipeWire quantum tuning and PulseAudio `tsched` config.

</audio_capture>

<opus_encoding>

Opus is the standard codec for VR audio streaming. See `references/opus-config.md` for full parameter reference.

### Recommended VR Settings

```rust
use audio_codec::opus::OpusEncoder;

let mut encoder = OpusEncoder::new(48000, 2); // 48kHz stereo

// Configure for low-latency VR
// Application: VOIP for mic, Audio for game sound
// Bitrate: 128kbps stereo, 64kbps mono
// Frame size: 10ms (480 samples at 48kHz) — best latency/quality trade-off
```

| Parameter | Game Audio | Microphone |
|-----------|-----------|------------|
| Sample rate | 48000 Hz | 48000 Hz |
| Channels | 2 (stereo) | 1 (mono) |
| Application | OPUS_APPLICATION_AUDIO | OPUS_APPLICATION_VOIP |
| Bitrate | 128 kbps | 32-64 kbps |
| Frame size | 10ms (480 samples) | 10ms (480 samples) |
| Complexity | 5-7 (balance CPU/quality) | 3-5 |
| Inband FEC | Off | On |
| DTX | Off | On (saves bandwidth on silence) |

**Frame size trade-offs:**
- 2.5ms -- lowest latency, poor quality, high bitrate overhead
- 5ms -- good for VR, marginal quality loss
- 10ms -- **sweet spot** for VR: good quality, acceptable latency
- 20ms -- standard VoIP, too much latency for VR
- 60ms -- music streaming, not for VR

### Raw PCM Streaming

When bandwidth allows (local network, USB), skip encoding:

```rust
// 48kHz stereo i16 = 192 KB/s = 1.5 Mbps — trivial on WiFi
let bytes: Vec<u8> = samples.iter()
    .flat_map(|s| s.to_ne_bytes())
    .collect();
```

Use raw PCM when: latency budget is extremely tight (<5ms total), bandwidth is abundant, or CPU is constrained.

</opus_encoding>

<packet_loss_jitter>

### Jitter Buffer

Ring buffer that absorbs network timing jitter. ALVR uses a sample-based VecDeque approach.

```rust
// ALVR pattern: batch-based jitter buffer
let batch_frames_count = sample_rate * batch_ms / 1000;      // fade unit
let average_buffer_frames = sample_rate * buffering_ms / 1000; // target fill

// Playback callback pulls batches
fn get_next_frame_batch(
    buffer: &mut VecDeque<f32>,
    channels: usize,
    batch_frames: usize,
) -> Vec<f32> {
    if buffer.len() / channels >= batch_frames {
        let mut batch: Vec<f32> = buffer.drain(..batch_frames * channels).collect();
        // Auto fade-out when buffer running low (prevents hard cut)
        if buffer.len() / channels < batch_frames {
            for f in 0..batch_frames {
                let vol = 1.0 - f as f32 / batch_frames as f32;
                for c in 0..channels {
                    batch[f * channels + c] *= vol;
                }
            }
        }
        batch
    } else {
        vec![0.0; batch_frames * channels] // silence on underrun
    }
}
```

### Jitter Buffer Sizing

| Buffer size | Effect |
|-------------|--------|
| < 5ms | Frequent underruns, glitches |
| 5-10ms | Aggressive, good for wired/WiFi 6E |
| 10-20ms | **Recommended for VR WiFi** |
| 20-50ms | Safe but noticeable audio lag |
| > 50ms | Lip-sync issues, not suitable for VR |

### Packet Loss Recovery

ALVR's approach (implemented in `receive_samples_loop`):

1. **Detect loss** via sequence numbers (`data.had_packet_loss()`)
2. **Flush stale audio** -- keep only one batch for cross-fade
3. **Accumulate recovery buffer** until it exceeds target fill + one batch
4. **Fade-in** the recovery buffer (linear ramp over one batch)
5. **Cross-fade** with remaining old audio if available

**Opus PLC (Packet Loss Concealment):** Pass `None`/null data to `opus_decode` -- it generates interpolated audio from its internal state. Only works for 1-2 consecutive lost packets.

### Buffer Overflow Handling

When packets arrive faster than playback (clock drift, network burst):

```rust
// ALVR pattern: drain excess, cross-fade at boundary
if buffer_frames > 2 * target + batch {
    let excess = buffer.drain(0..(buffer_frames - target) * channels).collect();
    // Cross-fade: ramp new start in, ramp old end out
    for f in 0..batch {
        let t = f as f32 / batch as f32;
        for c in 0..channels {
            buffer[f * channels + c] =
                buffer[f * channels + c] * t + excess[f * channels + c] * (1.0 - t);
        }
    }
}
```

</packet_loss_jitter>

<virtual_microphone>

For forwarding VR headset microphone audio back to the PC as a standard input device.

### Windows

Requires a virtual audio cable driver. ALVR auto-detects these pairs:

| Sink (output to) | Source (apps read from) | Software |
|-------------------|------------------------|----------|
| CABLE Input | CABLE Output | VB-CABLE |
| VoiceMeeter Input | VoiceMeeter Output | VoiceMeeter |
| Virtual Cable 1 | Virtual Cable 2 | VAC |

**Setup:** Install VB-CABLE or VoiceMeeter. ALVR writes decoded mic audio to the sink; Discord/games read from the source.

### Linux (PipeWire)

PipeWire creates virtual sources natively -- no extra software needed.

```rust
// Create a virtual microphone source via PipeWire
pw::properties::properties! {
    *pw::keys::NODE_NAME => "ALVR Microphone",
    *pw::keys::MEDIA_CLASS => "Audio/Source",     // appears as mic input
    *pw::keys::MEDIA_ROLE => "Communication",
}
// Connect stream as Output direction (we produce audio)
stream.connect(spa::utils::Direction::Output, None,
    StreamFlags::AUTOCONNECT | StreamFlags::MAP_BUFFERS | StreamFlags::RT_PROCESS,
    &mut params,
)?;
```

Apps see "ALVR Microphone" as a regular input device.

</virtual_microphone>

<channel_downmixing>

VR headsets typically play stereo. Games may output 5.1/7.1 surround.

| Input | Supported | Mix coefficients (L/R) |
|-------|-----------|----------------------|
| Mono (1ch) | Yes | Duplicate to both |
| Stereo (2ch) | Yes | Pass through |
| Quad (4ch) | Yes | FL=1/0, FR=0/1, BL=0.707/0, BR=0/0.707 |
| 5.1 (6ch) | Yes | Center at 0.707/0.707, LFE ignored |
| 7.1 (8ch) | Yes | Full surround fold-down |
| 5ch, 7ch | No | Not standard layouts |
| > 8ch | No | Bail with error |

**Sample format conversion** -- always normalize to target format early in the pipeline:

```rust
// F32 -> i16 (common for network transmission)
let i16_sample: i16 = (f32_sample.clamp(-1.0, 1.0) * i16::MAX as f32) as i16;

// i16 -> f32 (common for playback/processing)
let f32_sample: f32 = i16_sample as f32 / i16::MAX as f32;
```

</channel_downmixing>

<spatial_audio>

### HRTF (Head-Related Transfer Function)

Simulates 3D positioning using stereo headphones. Each sound source gets a pair of FIR filters (left/right ear) based on its angle relative to the listener's head.

**Key rules:**
- HRTF must update with head tracking pose data (quaternion from IMU)
- Use per-source convolution, not a single global HRTF
- Standard HRIR datasets: MIT KEMAR, LISTEN, SADIE II
- Typical HRIR length: 128-512 taps at 48kHz

### Ambisonics

Encode spatial audio as a spherical harmonic field, decode to headphones with head tracking.

| Order | Channels | Angular resolution | Use case |
|-------|----------|-------------------|----------|
| 1st (FOA) | 4 (W,X,Y,Z) | ~60 degrees | VR video, ambient |
| 2nd | 9 | ~30 degrees | Games, moderate precision |
| 3rd (HOA) | 16 | ~15 degrees | High-end VR |

**Rotation:** Apply head tracking rotation matrix to ambisonics channels *before* decoding to binaural. This is a simple matrix multiply on the B-format channels.

### Audio-Pose Synchronization

Audio frames must be rendered for the head pose at their *playback* time, not capture time.

```
Capture game audio (t=0) → encode → network (t=5ms) → jitter buffer →
  At playback (t=15ms): apply HRTF using predicted head pose at t=15ms
```

Timestamp each audio packet with the video frame it corresponds to. On the headset, match audio playback to the pose used for that video frame.

</spatial_audio>

<clock_drift>

PC and headset have independent clocks. Over minutes, audio drifts relative to video.

**Detection:** Track buffer fill level over time. Consistent growth = headset clock faster. Consistent drain = headset clock slower.

**Correction approaches:**
1. **Sample dropping/insertion** -- crude, can cause clicks
2. **Resampling** -- adjust playback rate by 0.01-0.1% (e.g., 48000 -> 48005 Hz)
3. **Buffer level PID controller** -- target a fixed buffer fill, adjust playback rate continuously
4. **ALVR approach** -- overflow detection with cross-fade drain (see buffer overflow section)

**Never resample by large ratios** -- introduces audible artifacts. Drift correction should be < 0.5% rate adjustment.

</clock_drift>

<troubleshooting>

| Symptom | Likely Cause |
|---------|-------------|
| No audio captured | Wrong device (loopback needs output device config) |
| Crackling/clicks | Buffer underrun, try larger buffer or jitter buffer |
| Audio cuts out periodically | Packet loss without PLC, or exclusive mode contention |
| Audio drifts from video | Clock drift, no compensation |
| High CPU from audio | Opus complexity too high, or per-sample allocations in callback |
| Distorted after format convert | Wrong endianness (use `to_ne_bytes`), or clipping on F32->I16 |
| PipeWire: "no matching format" | AudioInfo format/rate/channels mismatch with negotiated params |
| Virtual mic not seen by apps | Wrong MEDIA_CLASS (need "Audio/Source", not "Audio/Sink") |
| One-sided stereo | Channel mapping wrong in downmix, check L/R coefficients |
| Exclusive mode fails | Another app holds the device, fall back to shared mode |

</troubleshooting>

<anti_patterns>

- **Allocating in audio callback** -- causes GC/allocation jitter. Pre-allocate all buffers.
- **Locking a mutex in audio callback** -- use `try_lock()` or lock-free ring buffers.
- **Resampling every packet** -- resample once at capture or playback, not in the network path.
- **Ignoring sample format** -- F32 vs I16 mismatch causes noise/silence. Always check device format.
- **Hardcoding device names** -- devices vary per system. Use substring matching or index fallback.
- **Mixing blocking I/O with audio thread** -- network sends in audio callback cause underruns. Use a channel/queue.

</anti_patterns>

<deep_reference>

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `opus-config.md` | Opus encoder/decoder parameters, CTL values, frame sizes, FEC/DTX/PLC details |
| `platform-audio.md` | WASAPI exclusive/shared mode setup, PipeWire quantum tuning, PulseAudio low-latency config |

</deep_reference>
