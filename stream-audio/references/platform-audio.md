# Platform Audio Configuration

## Windows (WASAPI)

### Shared Mode

Default mode. Audio goes through Windows Audio Session API mixer. Multiple apps can use the device simultaneously.

```rust
// CPAL shared mode (default)
let stream_config = StreamConfig {
    channels: config.channels(),
    sample_rate: config.sample_rate(),
    buffer_size: BufferSize::Default, // Windows chooses ~10ms
};
```

**Shared mode latency:** Minimum ~3ms with `AUDCLNT_STREAMFLAGS_EVENTCALLBACK`. Default is ~10ms.

### Exclusive Mode

Bypasses the audio mixer entirely. Lowest latency (~1ms) but locks the device.

```rust
// Request exclusive-like behavior via CPAL
let stream_config = StreamConfig {
    channels: config.channels(),
    sample_rate: config.sample_rate(),
    buffer_size: BufferSize::Fixed(128), // ~2.7ms at 48kHz
};
// Note: CPAL doesn't expose true WASAPI exclusive mode directly.
// For true exclusive, use the windows crate with IAudioClient::Initialize
// and AUDCLNT_SHAREMODE_EXCLUSIVE.
```

**Exclusive mode via windows crate (raw WASAPI):**

```rust
use windows::Win32::Media::Audio::*;

unsafe {
    let audio_client: IAudioClient = device.Activate(CLSCTX_ALL, None)?;

    // Get mix format for the device
    let format = audio_client.GetMixFormat()?;

    // Initialize in exclusive mode with event-driven buffering
    audio_client.Initialize(
        AUDCLNT_SHAREMODE_EXCLUSIVE,
        AUDCLNT_STREAMFLAGS_EVENTCALLBACK | AUDCLNT_STREAMFLAGS_NOPERSIST,
        buffer_duration,    // REFERENCE_TIME in 100ns units
        buffer_duration,    // periodicity = buffer_duration for exclusive
        format.as_ref().unwrap(),
        None,
    )?;

    let event = CreateEventW(None, false, false, None)?;
    audio_client.SetEventHandle(event)?;
    // WaitForSingleObject(event, INFINITE) in audio thread
}
```

### Loopback Capture

Capture what's playing on an output device (game audio).

```rust
// WASAPI loopback via windows crate
unsafe {
    audio_client.Initialize(
        AUDCLNT_SHAREMODE_SHARED,
        AUDCLNT_STREAMFLAGS_LOOPBACK | AUDCLNT_STREAMFLAGS_EVENTCALLBACK,
        buffer_duration,
        0, // periodicity must be 0 for shared mode
        format.as_ref().unwrap(),
        None,
    )?;

    let capture_client: IAudioCaptureClient = audio_client.GetService()?;
    audio_client.Start()?;

    // In capture loop:
    let mut buffer_ptr = std::ptr::null_mut();
    let mut frames_available = 0u32;
    let mut flags = 0u32;
    capture_client.GetBuffer(
        &mut buffer_ptr,
        &mut frames_available,
        &mut flags,
        None, None,
    )?;
    // flags & AUDCLNT_BUFFERFLAGS_SILENT != 0 means silence
    // Process buffer_ptr as PCM data
    capture_client.ReleaseBuffer(frames_available)?;
}
```

**CPAL loopback approach (ALVR pattern):**
CPAL doesn't have a dedicated loopback API. ALVR works around this by:
1. Getting the output device
2. Calling `default_output_config()` (since `default_input_config()` fails for output devices)
3. Building an input stream on the output device (uses WASAPI loopback internally on Windows CPAL backends)

### Device Muting

When capturing loopback audio and playing it on the VR headset, you may want to mute the PC speakers to avoid echo:

```rust
// ALVR pattern: mute via IAudioEndpointVolume
use windows::Win32::Media::Audio::Endpoints::IAudioEndpointVolume;

let endpoint_volume: IAudioEndpointVolume =
    imm_device.Activate(CLSCTX_ALL, None)?;
endpoint_volume.SetMute(true, &GUID::zeroed())?;  // mute
// Restore on shutdown:
endpoint_volume.SetMute(false, &GUID::zeroed())?;
```

## Linux (PipeWire)

### Key Concepts

- **Node**: audio source or sink (like a device or app stream)
- **Quantum**: PipeWire's processing block size (like WASAPI buffer period)
- **Driver**: the node that paces the processing graph

### Low-Latency Quantum Tuning

```bash
# Check current quantum
pw-metadata -n settings 0 clock.quantum

# Set minimum quantum for low latency (requires restart of affected streams)
# In pipewire.conf or a .conf.d drop-in:
context.properties = {
    default.clock.quantum     = 256    # ~5.3ms at 48kHz
    default.clock.min-quantum = 64     # ~1.3ms at 48kHz (minimum allowed)
    default.clock.max-quantum = 1024   # ~21.3ms at 48kHz
    default.clock.rate        = 48000
}
```

| Quantum | Latency (48kHz) | Use Case |
|---------|-----------------|----------|
| 64 | 1.3ms | Extreme low-latency, high CPU |
| 128 | 2.7ms | Pro audio, VR |
| 256 | 5.3ms | Good balance |
| 512 | 10.7ms | Default, general use |
| 1024 | 21.3ms | Low CPU, high latency |

**Per-stream quantum override:**

```rust
// Request specific quantum in PipeWire properties
pw::properties::properties! {
    *pw::keys::NODE_LATENCY => "128/48000",  // quantum/rate
    *pw::keys::NODE_RATE => "1/48000",
}
```

### PipeWire Virtual Devices

**Virtual sink (capture game audio):**

```bash
# Create a virtual sink that captures audio
pw-cli create-node adapter {
    factory.name=support.null-audio-sink
    node.name="vr-capture"
    media.class="Audio/Sink"
    audio.rate=48000
    audio.channels=2
    object.linger=true
}
# Then route game audio to this sink via pavucontrol or pw-link
```

**Virtual source (mic forwarding):**

The PipeWire stream with `MEDIA_CLASS => "Audio/Source"` and `Direction::Output` creates a virtual mic automatically. No external tools needed.

### PipeWire Monitor Sources

Alternative to creating a custom sink -- monitor what an existing sink plays:

```bash
# List monitor sources
pw-cli ls Node | grep -A2 "monitor"

# Link a monitor to your capture stream
pw-link "alsa_output.pci-0000_00_1f.3.analog-stereo:monitor_FL" "alvr-audio:input_FL"
pw-link "alsa_output.pci-0000_00_1f.3.analog-stereo:monitor_FR" "alvr-audio:input_FR"
```

### PipeWire Stream Flags

```rust
StreamFlags::AUTOCONNECT   // auto-connect to default sink/source
StreamFlags::MAP_BUFFERS   // map buffer memory (required for data access)
StreamFlags::RT_PROCESS    // run process callback in real-time thread
StreamFlags::INACTIVE      // don't start immediately
```

**Always use `RT_PROCESS`** for low-latency audio -- otherwise the callback runs in the main loop thread with unpredictable scheduling.

## Linux (PulseAudio Legacy)

If stuck with PulseAudio (no PipeWire):

### Low-Latency Configuration

```bash
# /etc/pulse/daemon.conf
default-fragment-size-msec = 5    # buffer fragment size
default-fragments = 2              # number of fragments
high-priority = yes
realtime-scheduling = yes
realtime-priority = 5
```

**tsched (timer-based scheduling):**

```bash
# In /etc/pulse/default.pa — disable tsched for lower latency
load-module module-udev-detect tsched=0
# tsched=0 uses interrupt-based scheduling (lower latency, higher CPU)
```

### PulseAudio Virtual Devices

```bash
# Create a null sink (virtual output)
pactl load-module module-null-sink sink_name=vr_capture sink_properties=device.description="VR_Audio_Capture"

# The monitor source is auto-created: vr_capture.monitor
# Route game audio to vr_capture, read from vr_capture.monitor

# Create a virtual source (virtual microphone)
pactl load-module module-virtual-source source_name=vr_mic master=vr_capture.monitor
```

## macOS (CoreAudio)

CoreAudio uses an `AudioUnit` / `AVAudioEngine` model. CPAL wraps this on macOS.

**Key differences from Windows/Linux:**
- No native loopback capture -- requires a virtual audio driver (BlackHole, Loopback by Rogue Amoeba)
- CoreAudio buffer sizes are in frames, set via `kAudioDevicePropertyBufferFrameSize`
- Default buffer: 512 frames (~10.7ms at 48kHz), minimum ~128 frames on most hardware

```bash
# Install BlackHole for loopback capture on macOS
brew install blackhole-2ch
# Then create a Multi-Output device in Audio MIDI Setup combining
# your speakers + BlackHole. Capture from BlackHole.
```

## Real-Time Thread Priority

Audio callbacks must run at high priority to avoid glitches.

### Linux

```rust
// Set real-time priority for audio thread
use libc::{sched_param, sched_setscheduler, SCHED_FIFO};

unsafe {
    let param = sched_param { sched_priority: 50 };
    sched_setscheduler(0, SCHED_FIFO, &param);
}
// Requires CAP_SYS_NICE or rtkit (PipeWire handles this automatically for its threads)
```

### Windows

```rust
// Use MMCSS (Multimedia Class Scheduler Service)
use windows::Win32::Media::Multimedia::AvSetMmThreadCharacteristicsW;

let mut task_index = 0u32;
let handle = unsafe {
    AvSetMmThreadCharacteristicsW(w!("Pro Audio"), &mut task_index)?
};
// Revert on thread exit:
// AvRevertMmThreadCharacteristics(handle)?;
```

WASAPI event-driven mode + MMCSS "Pro Audio" class gives the most consistent audio timing on Windows.
