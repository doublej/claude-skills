# Post-Processing Reference

## Peak Normalization

```python
import numpy as np

def normalize_peak(audio: np.ndarray, target_db: float = -1.0) -> np.ndarray:
    """Peak-normalize audio to target dB."""
    peak = np.abs(audio).max()
    if peak == 0:
        return audio
    target = 10 ** (target_db / 20.0)
    return audio * (target / peak)
```

## LUFS Normalization

Loudness normalization per EBU R128 standard:

```bash
# Measure loudness
ffmpeg -i input.wav -af loudnorm=print_format=json -f null -

# Normalize to -14 LUFS (streaming standard)
ffmpeg -i input.wav -af loudnorm=I=-14:TP=-1:LRA=11 output.wav

# Two-pass for higher accuracy
ffmpeg -i input.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1
# Then use measured values in second pass:
ffmpeg -i input.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=-18:measured_TP=-2:measured_LRA=9:measured_thresh=-28" output.wav
```

### LUFS Targets

| Platform | Target LUFS | True Peak |
|----------|-------------|-----------|
| Spotify | -14 | -1 dBTP |
| Apple Music | -16 | -1 dBTP |
| YouTube | -14 | -1 dBTP |
| Podcast | -16 to -18 | -1 dBTP |
| Broadcast (EBU) | -23 | -1 dBTP |

### Python LUFS (with pyloudnorm)

```python
import pyloudnorm as pyln

def normalize_lufs(audio: np.ndarray, sr: int, target: float = -14.0) -> np.ndarray:
    """LUFS-normalize audio."""
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    return pyln.normalize.loudness(audio, loudness, target)
```

## Silence Trimming

Remove leading/trailing silence:

```python
def trim_silence(
    audio: np.ndarray,
    threshold_db: float = -40.0,
    min_silence_ms: int = 100,
    sr: int = 44100,
) -> np.ndarray:
    """Trim silence from start and end of audio."""
    threshold = 10 ** (threshold_db / 20.0)
    min_samples = int(min_silence_ms * sr / 1000)

    # Find first non-silent sample
    abs_audio = np.abs(audio) if audio.ndim == 1 else np.abs(audio).max(axis=1)
    above = abs_audio > threshold

    if not above.any():
        return audio

    start = np.argmax(above)
    end = len(above) - np.argmax(above[::-1])

    # Keep a small pad
    start = max(0, start - min_samples)
    end = min(len(audio), end + min_samples)

    return audio[start:end] if audio.ndim == 1 else audio[start:end, :]
```

### ffmpeg Trim

```bash
# Remove silence from start/end (threshold -40dB, min 0.5s silence)
ffmpeg -i input.wav -af "silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.5,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.5,areverse" output.wav
```

## Noise Gate

Suppress low-level noise in separated audio:

```python
def noise_gate(
    audio: np.ndarray,
    threshold_db: float = -50.0,
    attack_ms: float = 1.0,
    release_ms: float = 50.0,
    sr: int = 44100,
) -> np.ndarray:
    """Apply noise gate to suppress low-level noise."""
    threshold = 10 ** (threshold_db / 20.0)
    attack_coeff = np.exp(-1.0 / (attack_ms * sr / 1000))
    release_coeff = np.exp(-1.0 / (release_ms * sr / 1000))

    envelope = np.zeros(len(audio))
    env = 0.0
    mono = audio if audio.ndim == 1 else audio.mean(axis=1)

    for i in range(len(mono)):
        level = abs(mono[i])
        coeff = attack_coeff if level > env else release_coeff
        env = coeff * env + (1 - coeff) * level
        envelope[i] = env

    gain = np.where(envelope > threshold, 1.0, envelope / (threshold + 1e-10))
    gain = np.clip(gain, 0.0, 1.0)

    if audio.ndim == 1:
        return audio * gain
    return audio * gain[:, np.newaxis]
```

## Export Chain

Combine post-processing steps into a reusable chain:

```python
from dataclasses import dataclass

@dataclass
class ExportConfig:
    normalize_lufs: float | None = -14.0
    normalize_peak_db: float | None = None
    trim_silence: bool = True
    trim_threshold_db: float = -40.0
    noise_gate: bool = False
    noise_gate_threshold_db: float = -50.0

def apply_export_chain(
    audio: np.ndarray,
    sr: int,
    config: ExportConfig,
) -> np.ndarray:
    """Apply post-processing chain to separated audio."""
    result = audio.copy()

    if config.noise_gate:
        result = noise_gate(result, config.noise_gate_threshold_db, sr=sr)

    if config.trim_silence:
        result = trim_silence(result, config.trim_threshold_db, sr=sr)

    if config.normalize_lufs is not None:
        result = normalize_lufs(result, sr, config.normalize_lufs)
    elif config.normalize_peak_db is not None:
        result = normalize_peak(result, config.normalize_peak_db)

    return result
```

### Preset Chains

```python
CHAIN_PRESETS = {
    "music_streaming": ExportConfig(
        normalize_lufs=-14.0,
        trim_silence=True,
    ),
    "podcast": ExportConfig(
        normalize_lufs=-16.0,
        trim_silence=True,
        noise_gate=True,
        noise_gate_threshold_db=-45.0,
    ),
    "mastering": ExportConfig(
        normalize_peak_db=-1.0,
        trim_silence=False,
    ),
    "preview": ExportConfig(
        normalize_peak_db=-3.0,
        trim_silence=True,
    ),
}

# Usage
result = apply_export_chain(audio, 44100, CHAIN_PRESETS["music_streaming"])
```
