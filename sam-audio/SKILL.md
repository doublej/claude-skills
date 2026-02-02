---
name: sam-audio
description: Integrate Meta's SAM (Segment Anything Model) for audio separation. Covers model loading, prompt types, quality tuning, batch processing, format conversion, post-processing, and memory management. Use when separating audio sources, building separation pipelines, or processing audio collections.
---

# SAM Audio Integration

Separate audio sources using Meta's Segment Anything Audio model. Focus on integration patterns — pipelines, batch processing, format handling, and production memory management.

## When to Use This Skill

- Separating vocals, instruments, or sound effects from audio files
- Building audio separation pipelines with pre/post-processing
- Batch processing audio collections with resume capability
- Converting between audio formats around separation workflows
- Managing GPU memory for large-scale audio separation

## Setup

### Environment

```bash
# Create venv with uv
uv venv .venv --python 3.11
source .venv/bin/activate

# Install SAM audio + dependencies
uv pip install segment-anything-audio torch torchaudio
uv pip install huggingface_hub soundfile pydub

# HuggingFace auth (model is gated)
huggingface-cli login
```

### Model Variants

| Variant | VRAM | Speed | Quality | Use Case |
|---------|------|-------|---------|----------|
| `sam-audio-base` | ~4 GB | Fast | Good | Prototyping, previews |
| `sam-audio-large` | ~8 GB | Medium | Better | Production single-file |
| `sam-audio-huge` | ~16 GB | Slow | Best | Final masters, critical work |

### Load Model

```python
from segment_anything_audio import SamAudioModel, SamAudioPredictor

model = SamAudioModel.from_pretrained("facebook/sam-audio-large")
model = model.to("cuda").half()  # float16 saves ~50% VRAM
predictor = SamAudioPredictor(model)
```

## Core API

### Single-File Separation

```python
import torchaudio

def separate_source(audio_path: str, prompt: str, model, predictor) -> torch.Tensor:
    """Separate a single source from an audio file."""
    waveform, sr = torchaudio.load(audio_path)
    if sr != 16000:
        waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)

    predictor.set_audio(waveform, sample_rate=16000)
    masks = predictor.predict(text_prompt=prompt)
    return masks[0]  # Best prediction
```

### Prompt Types

| Type | Parameter | Example | Best For |
|------|-----------|---------|----------|
| Text | `text_prompt` | `"vocals"`, `"piano"` | General source identification |
| Visual | `spectrogram_point` | `(time_s, freq_hz)` | Precise frequency targeting |
| Span | `time_span` | `(start_s, end_s)` | Isolating time regions |

```python
# Text prompt
masks = predictor.predict(text_prompt="drums")

# Visual prompt — point on spectrogram
masks = predictor.predict(spectrogram_point=(2.5, 440.0))

# Time span
masks = predictor.predict(time_span=(10.0, 15.0))
```

## Quality Tuning

### Prediction Spans

Split long audio into overlapping spans for consistent quality:

```python
masks = predictor.predict(
    text_prompt="vocals",
    predict_spans=True,
    span_duration=30.0,    # seconds per span
    span_overlap=2.0,      # overlap for crossfade
)
```

### Reranking Candidates

Generate multiple candidates, pick best:

```python
masks = predictor.predict(
    text_prompt="vocals",
    num_candidates=8,
    rerank=True,
)
```

### Quality Presets

| Preset | `num_candidates` | `predict_spans` | `span_duration` | Notes |
|--------|-------------------|-----------------|-----------------|-------|
| Fast | 1 | False | — | Preview, testing |
| Balanced | 4 | True | 30.0 | Default production |
| Best | 16 | True | 15.0 | Final masters |

## Integration Patterns

### Pipeline Function

```python
import torch
import torchaudio
import soundfile as sf
from pathlib import Path

def separate_and_export(
    input_path: str,
    output_path: str,
    prompt: str,
    predictor,
    sr_out: int = 44100,
):
    """Full pipeline: load → separate → export."""
    waveform, sr = torchaudio.load(input_path)
    if sr != 16000:
        waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)

    predictor.set_audio(waveform, sample_rate=16000)
    masks = predictor.predict(
        text_prompt=prompt,
        num_candidates=4,
        predict_spans=True,
    )

    separated = masks[0]
    if sr_out != 16000:
        separated = torchaudio.transforms.Resample(16000, sr_out)(separated)

    sf.write(output_path, separated.cpu().numpy().T, sr_out)
```

### Memory Management

```python
# Singleton model — load once, reuse
_model_cache = {}

def get_predictor(variant: str = "large", device: str = "cuda"):
    if variant not in _model_cache:
        model = SamAudioModel.from_pretrained(f"facebook/sam-audio-{variant}")
        model = model.to(device).half()
        _model_cache[variant] = SamAudioPredictor(model)
    return _model_cache[variant]

# Free VRAM between large batches
def clear_gpu():
    torch.cuda.empty_cache()
    import gc
    gc.collect()
```

Key memory rules:
- **float16**: Always use `.half()` — halves VRAM with negligible quality loss
- **Singleton**: Load model once, never per-file
- **empty_cache**: Call between batch chunks, not between individual files
- **CPU offload**: Move tensors to CPU with `.cpu()` before saving

### Error Handling

Handle errors at system boundaries only:

```python
from pathlib import Path

def safe_separate(input_path: str, prompt: str, predictor) -> tuple[bool, str]:
    """Returns (success, message)."""
    path = Path(input_path)

    if not path.exists():
        return False, f"File not found: {input_path}"

    suffix = path.suffix.lower()
    supported = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"}
    if suffix not in supported:
        return False, f"Unsupported format: {suffix}"

    try:
        waveform, sr = torchaudio.load(str(path))
    except Exception as e:
        return False, f"Failed to load audio: {e}"

    try:
        predictor.set_audio(waveform, sample_rate=sr)
        masks = predictor.predict(text_prompt=prompt)
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return False, "CUDA out of memory — try a smaller model variant"
    except Exception as e:
        return False, f"Separation failed: {e}"

    return True, "OK"
```

## Batch Processing

Process file collections with CSV manifests and resume:

```python
import csv
from pathlib import Path

def process_manifest(csv_path: str, predictor, output_dir: str):
    """Process files listed in a CSV manifest."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    done_file = out / ".done"
    done = set(done_file.read_text().splitlines()) if done_file.exists() else set()

    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if row["input"] in done:
                continue
            separate_and_export(
                row["input"],
                str(out / f"{Path(row['input']).stem}_{row['prompt']}.wav"),
                row["prompt"],
                predictor,
            )
            done.add(row["input"])
            done_file.write_text("\n".join(done))
```

CSV manifest format:
```csv
input,prompt,output_format
/data/song1.wav,vocals,wav
/data/song2.mp3,drums,flac
```

See **[BATCH PROCESSING](references/batch-processing.md)** for parallel I/O, multi-GPU, and the `batch_separate.py` CLI script.

## Format Conversion

Use ffmpeg for format conversion before/after separation:

```bash
# Pre-process: convert to WAV 16kHz mono (model input)
ffmpeg -i input.mp3 -ar 16000 -ac 1 input_16k.wav

# Post-process: export as high-quality FLAC
ffmpeg -i separated.wav -c:a flac -sample_fmt s24 output.flac

# Post-process: export as MP3 320kbps
ffmpeg -i separated.wav -c:a libmp3lame -b:a 320k output.mp3
```

See **[FORMAT CONVERSION](references/format-conversion.md)** for the full format matrix, Python ffmpeg wrappers, and sample rate handling.

## Post-Processing

Apply normalization and cleanup after separation:

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

See **[POST-PROCESSING](references/post-processing.md)** for LUFS normalization, silence trimming, noise gate, and export chains.
