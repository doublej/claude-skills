#!/usr/bin/env python3
"""Batch audio separation CLI with resume and format export.

Usage:
    python batch_separate.py manifest.csv --output-dir ./output
    python batch_separate.py manifest.csv --output-dir ./output --preset balanced --format flac
    python batch_separate.py manifest.csv --output-dir ./output --variant huge --workers 8

CSV manifest format:
    input,prompt[,output_format]
    /path/to/song.wav,vocals,flac
    /path/to/track.mp3,drums,wav
"""

import argparse
import csv
import subprocess
import sys
import time
from pathlib import Path

QUALITY_PRESETS = {
    "fast": {"num_candidates": 1, "predict_spans": False},
    "balanced": {"num_candidates": 4, "predict_spans": True, "span_duration": 30.0},
    "best": {"num_candidates": 16, "predict_spans": True, "span_duration": 15.0},
}

EXPORT_FORMATS = {
    "wav": {"codec": "pcm_s16le", "ext": "wav"},
    "flac": {"codec": "flac", "ext": "flac", "sample_fmt": "s24"},
    "mp3_320": {"codec": "libmp3lame", "ext": "mp3", "bitrate": "320k"},
    "mp3_192": {"codec": "libmp3lame", "ext": "mp3", "bitrate": "192k"},
}


class ResumeTracker:
    def __init__(self, output_dir: Path):
        self.done_path = output_dir / ".done"
        self.done: set[str] = set()
        if self.done_path.exists():
            self.done = set(self.done_path.read_text().splitlines())

    def is_done(self, key: str) -> bool:
        return key in self.done

    def mark_done(self, key: str):
        self.done.add(key)
        self.done_path.write_text("\n".join(sorted(self.done)))


def load_manifest(csv_path: str) -> list[dict]:
    with open(csv_path) as f:
        return list(csv.DictReader(f))


def ffmpeg_convert(input_path: str, output_path: str, **kwargs):
    cmd = ["ffmpeg", "-y", "-i", input_path]
    if "sample_rate" in kwargs:
        cmd += ["-ar", str(kwargs["sample_rate"])]
    if "codec" in kwargs:
        cmd += ["-c:a", kwargs["codec"]]
    if "bitrate" in kwargs:
        cmd += ["-b:a", kwargs["bitrate"]]
    if "sample_fmt" in kwargs:
        cmd += ["-sample_fmt", kwargs["sample_fmt"]]
    cmd.append(output_path)
    subprocess.run(cmd, check=True, capture_output=True)


def separate_file(input_path, prompt, predictor, preset_params):
    import torchaudio

    waveform, sr = torchaudio.load(input_path)
    if sr != 16000:
        waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)

    predictor.set_audio(waveform, sample_rate=16000)
    masks = predictor.predict(text_prompt=prompt, **preset_params)
    separated = masks[0]

    # Resample to 44.1kHz for output
    separated = torchaudio.transforms.Resample(16000, 44100)(separated)
    return separated.cpu()


def main():
    parser = argparse.ArgumentParser(description="Batch audio separation with SAM Audio")
    parser.add_argument("manifest", help="CSV manifest file")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument(
        "--variant",
        choices=["base", "large", "huge"],
        default="large",
        help="Model variant (default: large)",
    )
    parser.add_argument(
        "--preset",
        choices=list(QUALITY_PRESETS),
        default="balanced",
        help="Quality preset (default: balanced)",
    )
    parser.add_argument(
        "--format",
        choices=list(EXPORT_FORMATS),
        default="wav",
        help="Output format (default: wav)",
    )
    parser.add_argument("--workers", type=int, default=4, help="I/O worker threads")
    parser.add_argument("--device", default="cuda", help="Device (default: cuda)")
    parser.add_argument("--dry-run", action="store_true", help="List files without processing")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tracker = ResumeTracker(output_dir)

    pending = [item for item in manifest if not tracker.is_done(item["input"])]
    total = len(manifest)
    skipped = total - len(pending)

    print(f"Manifest: {total} files, {skipped} already done, {len(pending)} pending")

    if args.dry_run:
        for item in pending:
            fmt = item.get("output_format", args.format)
            print(f"  {item['input']} → {item['prompt']} ({fmt})")
        return

    if not pending:
        print("Nothing to do.")
        return

    # Import heavy deps only when needed
    import torch
    import soundfile as sf
    from segment_anything_audio import SamAudioModel, SamAudioPredictor

    print(f"Loading model: sam-audio-{args.variant} on {args.device}...")
    model = SamAudioModel.from_pretrained(f"facebook/sam-audio-{args.variant}")
    model = model.to(args.device).half()
    predictor = SamAudioPredictor(model)
    preset_params = QUALITY_PRESETS[args.preset]

    start = time.monotonic()

    for i, item in enumerate(pending):
        input_path = item["input"]
        prompt = item["prompt"]
        fmt_key = item.get("output_format", args.format)
        fmt = EXPORT_FORMATS.get(fmt_key, EXPORT_FORMATS["wav"])
        stem = Path(input_path).stem
        out_path = output_dir / f"{stem}_{prompt}.{fmt['ext']}"

        try:
            separated = separate_file(input_path, prompt, predictor, preset_params)
            tmp_wav = output_dir / f".tmp_{stem}.wav"
            sf.write(str(tmp_wav), separated.numpy().T, 44100)

            if fmt_key != "wav":
                ffmpeg_convert(str(tmp_wav), str(out_path), **fmt)
                tmp_wav.unlink()
            else:
                tmp_wav.rename(out_path)

            tracker.mark_done(input_path)
            elapsed = time.monotonic() - start
            rate = (i + 1) / elapsed
            remaining = (len(pending) - i - 1) / rate if rate > 0 else 0
            print(f"[{skipped + i + 1}/{total}] {out_path.name} ({rate:.1f} files/s, ~{remaining:.0f}s left)")

        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            print(f"[SKIP] {input_path}: CUDA OOM — try smaller variant", file=sys.stderr)
        except Exception as e:
            print(f"[FAIL] {input_path}: {e}", file=sys.stderr)

        # Periodic VRAM cleanup
        if (i + 1) % 50 == 0:
            torch.cuda.empty_cache()

    elapsed = time.monotonic() - start
    done_count = len(pending) - len([
        item for item in pending if not tracker.is_done(item["input"])
    ])
    print(f"\nDone: {done_count}/{len(pending)} files in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
