# Opus Codec Configuration

## Encoder Settings (CTL)

### Application Modes

| Constant | Value | Use Case |
|----------|-------|----------|
| `OPUS_APPLICATION_VOIP` | 2048 | Speech, mic forwarding. Enables FEC, DTX, voice detection. |
| `OPUS_APPLICATION_AUDIO` | 2049 | Music/game audio. Best quality for non-speech. |
| `OPUS_APPLICATION_RESTRICTED_LOWDELAY` | 2051 | Minimum algorithmic delay (2.5ms). Quality trade-off. |

### Key CTL Parameters

```c
// Bitrate (bps) — OPUS_SET_BITRATE
opus_encoder_ctl(enc, OPUS_SET_BITRATE(128000));  // 128kbps stereo game audio
opus_encoder_ctl(enc, OPUS_SET_BITRATE(64000));   // 64kbps mono mic

// Complexity (0-10) — OPUS_SET_COMPLEXITY
opus_encoder_ctl(enc, OPUS_SET_COMPLEXITY(5));  // balanced for VR

// Signal type hint — OPUS_SET_SIGNAL
opus_encoder_ctl(enc, OPUS_SET_SIGNAL(OPUS_SIGNAL_MUSIC));  // game audio
opus_encoder_ctl(enc, OPUS_SET_SIGNAL(OPUS_SIGNAL_VOICE));  // mic

// Inband FEC — OPUS_SET_INBAND_FEC (VOIP mode only)
opus_encoder_ctl(enc, OPUS_SET_INBAND_FEC(1));          // enable
opus_encoder_ctl(enc, OPUS_SET_PACKET_LOSS_PERC(10));   // expected loss %

// DTX (Discontinuous Transmission) — silence suppression
opus_encoder_ctl(enc, OPUS_SET_DTX(1));  // mic only, saves bandwidth

// Force mono/stereo
opus_encoder_ctl(enc, OPUS_SET_FORCE_CHANNELS(2));  // force stereo
```

### Rust (audio-codec crate)

```rust
use audio_codec::opus::{OpusEncoder, OpusDecoder};
use audio_codec::{Encoder, Decoder};

// Encoder
let mut enc = OpusEncoder::new(48000, 2); // 48kHz stereo
let pcm: &[i16] = &[/* 480 samples per channel = 10ms at 48kHz */];
let encoded: Vec<u8> = enc.encode(pcm);

// Decoder
let mut dec = OpusDecoder::new(48000, 2);
let decoded: PcmBuf = dec.decode(&encoded);
```

### Rust (opus/audiopus crate — direct bindings)

```rust
use audiopus::{coder::Encoder, Application, Channels, SampleRate};

let mut enc = Encoder::new(
    SampleRate::Hz48000,
    Channels::Stereo,
    Application::Audio, // or Voip, LowDelay
)?;
enc.set_bitrate(audiopus::Bitrate::Bits(128000))?;
enc.set_complexity(5)?;

let mut output = vec![0u8; 4000];
let len = enc.encode(&pcm_i16, &mut output)?;
output.truncate(len);
```

## Frame Sizes

Opus supports specific frame durations. Frame size in samples = `sample_rate * duration_ms / 1000`.

| Duration | Samples (48kHz) | Algorithmic delay | VR suitability |
|----------|----------------|-------------------|----------------|
| 2.5ms | 120 | 2.5ms | Extreme low-latency, poor quality |
| 5ms | 240 | 5ms | Good for VR, slight quality loss |
| 10ms | 480 | 10ms | **Recommended** |
| 20ms | 960 | 20ms | Standard VoIP, too slow for VR |
| 40ms | 1920 | 40ms | Music streaming |
| 60ms | 2880 | 60ms | Maximum efficiency |

With `RESTRICTED_LOWDELAY`: algorithmic delay = frame size (no lookahead).
With `AUDIO`/`VOIP`: algorithmic delay = frame size + 2.5ms lookahead (Opus SilkVOIP) or 6.5ms (CELT).

## Packet Loss Concealment (PLC)

### Decoder-side PLC

Pass null/empty data to the decoder to generate concealment audio:

```c
// C API — opus_decode with NULL input triggers PLC
int samples = opus_decode(decoder, NULL, 0, pcm_out, frame_size, 0);
// last arg: 0 = normal PLC, 1 = FEC decode (if available in next packet)
```

```rust
// Rust — check if your binding supports decode_plc or decode with None
// audiopus: decoder.decode(None, &mut output, false)?;
```

**PLC quality degrades rapidly:**
- 1 lost packet: nearly transparent
- 2 lost packets: audible but acceptable
- 3+ lost packets: noticeable artifacts, fade to silence

### Forward Error Correction (FEC)

When FEC is enabled, Opus embeds a lower-bitrate copy of the *previous* frame in the current packet.

```
Packet N:   [Current frame N] [FEC of frame N-1]
Packet N+1: [Current frame N+1] [FEC of frame N]
```

If packet N is lost but N+1 arrives, decode FEC from N+1 to recover frame N:

```c
// Decode FEC from packet N+1 to recover lost packet N
opus_decode(decoder, packet_n_plus_1, len, pcm_out, frame_size, 1);  // fec=1
// Then decode packet N+1 normally
opus_decode(decoder, packet_n_plus_1, len, pcm_out, frame_size, 0);
```

**FEC costs ~20-30% extra bitrate.** Only worth it for mic audio where packet loss is expected.

## Bitrate Guidelines

| Scenario | Mono | Stereo |
|----------|------|--------|
| Minimum intelligible speech | 8-12 kbps | - |
| Good speech (mic forwarding) | 24-32 kbps | - |
| High quality speech | 48-64 kbps | - |
| Game audio (acceptable) | - | 64-96 kbps |
| Game audio (good) | - | 128 kbps |
| Game audio (transparent) | - | 160-256 kbps |
| Overkill (diminishing returns) | > 64 kbps | > 256 kbps |

VBR (variable bitrate) is default and recommended. CBR only if network needs predictable bandwidth.

## Sample Rate Support

Opus natively supports: 8000, 12000, 16000, 24000, 48000 Hz.

**Always use 48000 Hz for VR.** Internal bandwidth modes:

| Bandwidth | Frequency range | Auto-selected when |
|-----------|----------------|-------------------|
| Narrowband | 0-4 kHz | Very low bitrate voice |
| Mediumband | 0-6 kHz | Low bitrate voice |
| Wideband | 0-8 kHz | Normal voice |
| Super-wideband | 0-12 kHz | High quality voice |
| Fullband | 0-20 kHz | Music / game audio |

Opus auto-selects bandwidth based on bitrate and signal type. For game audio at 128kbps+, it will use fullband.
