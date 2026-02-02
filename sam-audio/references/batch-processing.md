# Batch Processing Reference

## CSV Manifest Format

```csv
input,prompt,output_format,priority
/data/songs/track01.wav,vocals,flac,high
/data/songs/track02.mp3,drums,wav,normal
/data/songs/track03.flac,bass,mp3,low
```

Required columns: `input`, `prompt`. Optional: `output_format` (default: wav), `priority`.

## Parallel I/O Pattern

Separate GPU inference from disk I/O using a producer-consumer queue:

```python
import torch
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from pathlib import Path

def batch_separate(
    manifest: list[dict],
    predictor,
    output_dir: str,
    io_workers: int = 4,
):
    """Batch separation with parallel I/O and serial GPU inference."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    load_queue: Queue = Queue(maxsize=8)
    save_queue: Queue = Queue(maxsize=8)

    def loader(item):
        waveform, sr = torchaudio.load(item["input"])
        if sr != 16000:
            waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)
        return {"waveform": waveform, **item}

    def saver(result):
        stem = Path(result["input"]).stem
        fmt = result.get("output_format", "wav")
        out_path = out / f"{stem}_{result['prompt']}.{fmt}"
        sf.write(str(out_path), result["audio"].numpy().T, 44100)

    with ThreadPoolExecutor(max_workers=io_workers) as pool:
        # Pre-load files
        load_futures = [pool.submit(loader, item) for item in manifest]

        for future in load_futures:
            loaded = future.result()
            predictor.set_audio(loaded["waveform"], sample_rate=16000)
            masks = predictor.predict(text_prompt=loaded["prompt"], num_candidates=4)
            separated = torchaudio.transforms.Resample(16000, 44100)(masks[0].cpu())
            pool.submit(saver, {**loaded, "audio": separated})
```

## Resume Support

Track progress with a simple done-file:

```python
from pathlib import Path

class ResumeTracker:
    def __init__(self, output_dir: str):
        self.done_path = Path(output_dir) / ".done"
        self.done = set()
        if self.done_path.exists():
            self.done = set(self.done_path.read_text().splitlines())

    def is_done(self, key: str) -> bool:
        return key in self.done

    def mark_done(self, key: str):
        self.done.add(key)
        self.done_path.write_text("\n".join(sorted(self.done)))
```

Usage:

```python
tracker = ResumeTracker("/output/vocals")
for item in manifest:
    if tracker.is_done(item["input"]):
        continue
    # ... process ...
    tracker.mark_done(item["input"])
```

## Multi-GPU Distribution

Split manifest across GPUs:

```python
import torch

def distribute_manifest(manifest: list[dict], num_gpus: int) -> list[list[dict]]:
    """Round-robin distribute items across GPUs."""
    chunks = [[] for _ in range(num_gpus)]
    for i, item in enumerate(manifest):
        chunks[i % num_gpus].append(item)
    return chunks

def process_on_gpu(gpu_id: int, items: list[dict], variant: str = "large"):
    """Process a chunk on a specific GPU."""
    device = f"cuda:{gpu_id}"
    model = SamAudioModel.from_pretrained(f"facebook/sam-audio-{variant}")
    model = model.to(device).half()
    predictor = SamAudioPredictor(model)

    for item in items:
        waveform, sr = torchaudio.load(item["input"])
        waveform = waveform.to(device)
        if sr != 16000:
            waveform = torchaudio.transforms.Resample(sr, 16000).to(device)(waveform)
        predictor.set_audio(waveform, sample_rate=16000)
        masks = predictor.predict(text_prompt=item["prompt"])
        yield masks[0].cpu()
```

Launch with multiprocessing:

```python
import torch.multiprocessing as mp

if __name__ == "__main__":
    num_gpus = torch.cuda.device_count()
    chunks = distribute_manifest(manifest, num_gpus)
    mp.spawn(process_on_gpu, args=(chunks, "large"), nprocs=num_gpus)
```

## Progress Reporting

```python
import time

def process_with_progress(manifest, predictor, output_dir):
    total = len(manifest)
    tracker = ResumeTracker(output_dir)
    skipped = sum(1 for item in manifest if tracker.is_done(item["input"]))
    start = time.monotonic()

    for i, item in enumerate(manifest):
        if tracker.is_done(item["input"]):
            continue

        separate_and_export(item["input"], ..., item["prompt"], predictor)
        tracker.mark_done(item["input"])

        done = i + 1
        elapsed = time.monotonic() - start
        rate = (done - skipped) / elapsed if elapsed > 0 else 0
        remaining = (total - done) / rate if rate > 0 else 0
        print(f"[{done}/{total}] {rate:.1f} files/s, ~{remaining:.0f}s remaining")
```

## Memory Budgeting

| Audio Length | Peak VRAM (large, fp16) | Tip |
|-------------|-------------------------|-----|
| < 1 min | ~4 GB | No special handling |
| 1–5 min | ~6 GB | Default spans (30s) |
| 5–30 min | ~8 GB | Reduce span to 15s |
| > 30 min | ~10 GB+ | Split file first |

Call `torch.cuda.empty_cache()` every 50–100 files in long batches, not per file.
