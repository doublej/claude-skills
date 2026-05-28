# Format Conversion Reference

## Format Matrix

| Format | Extension | Lossless | Typical Use | ffmpeg Codec |
|--------|-----------|----------|-------------|--------------|
| WAV | `.wav` | Yes | Working format, model I/O | `pcm_s16le` / `pcm_f32le` |
| FLAC | `.flac` | Yes | Archival, distribution | `flac` |
| AIFF | `.aiff` | Yes | macOS/Logic Pro | `pcm_s16be` |
| MP3 | `.mp3` | No | Distribution, streaming | `libmp3lame` |
| AAC | `.m4a` | No | Apple ecosystem, streaming | `aac` / `libfdk_aac` |
| OGG | `.ogg` | No | Open-source, games | `libvorbis` |
| Opus | `.opus` | No | Low-latency streaming | `libopus` |

## Python ffmpeg Wrapper

```python
import subprocess
from pathlib import Path

def ffmpeg_convert(
    input_path: str,
    output_path: str,
    sample_rate: int | None = None,
    channels: int | None = None,
    codec: str | None = None,
    bitrate: str | None = None,
    sample_fmt: str | None = None,
):
    """Convert audio via ffmpeg subprocess."""
    cmd = ["ffmpeg", "-y", "-i", input_path]

    if sample_rate:
        cmd += ["-ar", str(sample_rate)]
    if channels:
        cmd += ["-ac", str(channels)]
    if codec:
        cmd += ["-c:a", codec]
    if bitrate:
        cmd += ["-b:a", bitrate]
    if sample_fmt:
        cmd += ["-sample_fmt", sample_fmt]

    cmd.append(output_path)
    subprocess.run(cmd, check=True, capture_output=True)
```

## Pre-Processing: Prepare for Model

The model expects 16kHz mono WAV. Convert input before separation:

```python
def prepare_for_model(input_path: str, work_dir: str) -> str:
    """Convert any audio to 16kHz mono WAV for model input."""
    out = Path(work_dir) / f"{Path(input_path).stem}_16k.wav"
    ffmpeg_convert(
        input_path, str(out),
        sample_rate=16000,
        channels=1,
        codec="pcm_s16le",
    )
    return str(out)
```

## Post-Processing: Export Formats

Common export presets:

```python
EXPORT_PRESETS = {
    "wav_44k": {"sample_rate": 44100, "codec": "pcm_s16le"},
    "wav_48k": {"sample_rate": 48000, "codec": "pcm_s16le"},
    "wav_96k": {"sample_rate": 96000, "codec": "pcm_s24le"},
    "flac_44k": {"sample_rate": 44100, "codec": "flac", "sample_fmt": "s24"},
    "flac_48k": {"sample_rate": 48000, "codec": "flac", "sample_fmt": "s24"},
    "mp3_320": {"sample_rate": 44100, "codec": "libmp3lame", "bitrate": "320k"},
    "mp3_192": {"sample_rate": 44100, "codec": "libmp3lame", "bitrate": "192k"},
    "aac_256": {"sample_rate": 44100, "codec": "aac", "bitrate": "256k"},
    "opus_128": {"sample_rate": 48000, "codec": "libopus", "bitrate": "128k"},
}

def export_with_preset(input_path: str, output_path: str, preset: str):
    """Export audio using a named preset."""
    params = EXPORT_PRESETS[preset]
    ffmpeg_convert(input_path, output_path, **params)
```

## Sample Rate Handling

### Resampling Quality

```bash
# High-quality resampling with SoX resampler (best quality)
ffmpeg -i input.wav -af "aresample=resampler=soxr:precision=33" -ar 44100 output.wav

# Standard resampling (good for most cases)
ffmpeg -i input.wav -ar 44100 output.wav
```

### In Python with torchaudio

```python
import torchaudio

def resample(waveform, orig_sr: int, target_sr: int):
    """Resample with torchaudio (high quality)."""
    if orig_sr == target_sr:
        return waveform
    return torchaudio.transforms.Resample(
        orig_freq=orig_sr,
        new_freq=target_sr,
        resampling_method="sinc_interp_kaiser",
    )(waveform)
```

### Sample Rate Decision Guide

| Scenario | Target SR | Reason |
|----------|-----------|--------|
| Model input | 16000 Hz | Model requirement |
| Music production | 44100 Hz | CD standard |
| Video production | 48000 Hz | Film/broadcast standard |
| Archival / mastering | 96000 Hz | Maximum quality preservation |
| Speech / podcasts | 22050 Hz | Adequate for voice |

## Batch Format Conversion

Convert an entire directory:

```python
from pathlib import Path

def batch_convert(input_dir: str, output_dir: str, preset: str, ext: str):
    """Convert all audio files in a directory."""
    inp = Path(input_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    audio_exts = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".aiff"}
    for f in inp.iterdir():
        if f.suffix.lower() in audio_exts:
            export_with_preset(str(f), str(out / f"{f.stem}.{ext}"), preset)
```

## Checking Audio Properties

```python
def get_audio_info(path: str) -> dict:
    """Get audio file properties via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    import json
    return json.loads(result.stdout)
```
