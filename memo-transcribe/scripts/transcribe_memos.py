#!/usr/bin/env python3
"""Transcribe a Voice Memos folder: Apple built-in transcript + local parakeet ASR.

Usage:  transcribe_memos.py <folder> [--out DIR]
        transcribe_memos.py --self-check
"""

import fcntl
import json
import re
import shutil
import sqlite3
import struct
import subprocess
import sys
import tempfile
from datetime import datetime, date
from pathlib import Path

RECORDINGS = Path.home() / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
PARAKEET = "http://127.0.0.1:8765"
CORE_DATA_EPOCH = 978307200  # 2001-01-01 → unix
CHUNK_SECONDS = 120  # longer uploads OOM-kill the server; see parakeet_text()
FRAMELINK_OUT = Path.home() / "dev/multi-stack/framelink/.claude/voice-memo-transcriptions"


# --- Apple built-in transcript (tsrp atom) ---------------------------------

def runs_to_text(runs):
    """attributedString.runs alternates [str, index, str, index, ...]; keep the strings."""
    return "".join(x for x in runs if isinstance(x, str))


def apple_transcript(audio: Path) -> str:
    """Read the `tsrp` metadata atom. Returns '' when Apple produced no transcript."""
    blob = audio.read_bytes()
    i = blob.find(b"tsrp")
    if i < 0:
        return ""
    j = blob.find(b"data", i)
    if j < 0:
        return ""
    size = struct.unpack(">I", blob[j - 4:j])[0]
    payload = blob[j + 12:j - 4 + size]  # skip size/type/version+flags/reserved
    try:
        attributed = json.loads(payload)["attributedString"]
    except (ValueError, KeyError):
        return ""
    if not attributed:
        return ""
    return runs_to_text(attributed["runs"]).strip()


# --- parakeet --------------------------------------------------------------

def parakeet_text(audio: Path, tmp: Path) -> str:
    """Split to <=CHUNK_SECONDS wavs and POST each.

    Whole-file uploads are not safe: a 6-minute memo grows the encoder's activations
    until the server is OOM-killed mid-request (empty reply, launchd restarts it).
    Segmenting client-side keeps every request inside a size the server survives, and
    sidesteps the quadratic cost that made long memos crawl.
    """
    for stale in tmp.glob("part*.wav"):
        stale.unlink()
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(audio),
         "-ac", "1", "-ar", "16000",
         "-f", "segment", "-segment_time", str(CHUNK_SECONDS),
         str(tmp / "part%03d.wav")],
        check=True,
    )
    parts = []
    for wav in sorted(tmp.glob("part*.wav")):
        out = subprocess.run(
            ["curl", "-sS", "-f", "-m", "600", f"{PARAKEET}/v1/audio/transcriptions",
             "-F", f"file=@{wav}", "-F", "response_format=json"],
            check=True, capture_output=True, text=True,
        ).stdout
        parts.append(json.loads(out)["text"].strip())
        wav.unlink()
    return " ".join(p for p in parts if p).strip()


# --- index -----------------------------------------------------------------

def read_index(folder: str):
    """Copy the CloudKit-synced DB (+ WAL) out and read the folder's rows."""
    with tempfile.TemporaryDirectory() as td:
        for suffix in ("", "-wal", "-shm"):
            src = RECORDINGS / f"CloudRecordings.db{suffix}"
            if src.exists():
                shutil.copy2(src, Path(td) / src.name)
        db = sqlite3.connect(Path(td) / "CloudRecordings.db")
        rows = db.execute(
            "SELECT r.ZPATH, r.ZENCRYPTEDTITLE, r.ZUNIQUEID, r.ZDATE, r.ZDURATION "
            "FROM ZCLOUDRECORDING r JOIN ZFOLDER f ON r.ZFOLDER = f.Z_PK "
            "WHERE lower(f.ZENCRYPTEDNAME) = lower(?) ORDER BY r.ZDATE",
            (folder,),
        ).fetchall()
        db.close()
    return [r for r in rows if r[0] and r[4]]  # drop empty ZPATH / zero duration


# --- output ----------------------------------------------------------------

def slug(title: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (title or "untitled").lower())).strip("-")


def write_note(out_dir: Path, folder: str, row, parakeet: str, apple: str) -> Path:
    path, title, uuid, zdate, duration = row
    when = datetime.fromtimestamp(zdate + CORE_DATA_EPOCH)
    dest = out_dir / f"{when:%Y-%m-%d-%H%M}-{slug(title)}.md"
    dest.write_text(
        "---\n"
        f"title: {title}\n"
        f"date: {when:%Y-%m-%d %H:%M}\n"
        f"duration: {int(duration) // 60}:{int(duration) % 60:02d}\n"
        f"uuid: {uuid}\n"
        f"source_file: {path}\n"
        f"folder: {folder}\n"
        "---\n\n"
        f"## Parakeet\n{parakeet or '(none)'}\n\n"
        f"## Apple (built-in)\n{apple or '(none)'}\n"
    )
    return dest


# --- main ------------------------------------------------------------------

def main(folder: str, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # The server holds a single MLX model. Two runs queue behind each other, look hung,
    # and race on the state file — so only one run may exist at a time.
    lock = open(out_dir / ".memo-transcribe.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit("another memo-transcribe run is already active — not starting a second")

    state_file = out_dir / ".memo-transcribe-state.json"
    state = json.loads(state_file.read_text()) if state_file.exists() else {}

    new = skipped = failed = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for row in read_index(folder):
            path, title, uuid, _, _ = row
            audio = RECORDINGS / path
            if not audio.exists():
                print(f"missing  {path}", flush=True)
                failed += 1
                continue
            mtime = audio.stat().st_mtime
            done = state.get(uuid)
            if done and done["mtime"] == mtime and not done.get("error"):
                skipped += 1
                continue

            apple = apple_transcript(audio)
            try:
                parakeet, error = parakeet_text(audio, tmp), None
            except (subprocess.CalledProcessError, ValueError, KeyError) as exc:
                parakeet, error = "", str(exc)

            dest = write_note(out_dir, folder, row, parakeet, apple)
            state[uuid] = {"mtime": mtime, "run": date.today().isoformat()}
            if error:
                state[uuid]["error"] = error
                failed += 1
                print(f"failed   {dest.name}: {error}", flush=True)
            else:
                new += 1
                print(f"wrote    {dest.name}", flush=True)
            state_file.write_text(json.dumps(state, indent=2))

    print(f"\n{new} new, {skipped} skipped, {failed} failed", flush=True)
    print(f"output: {out_dir}", flush=True)


def self_check():
    runs = ["Okay,", 0, " when", 1, " I", 2, " open", 3]
    assert runs_to_text(runs) == "Okay, when I open", runs_to_text(runs)
    assert slug("Volkerakstraat 7 56") == "volkerakstraat-7-56"
    print("self-check ok", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--self-check":
        self_check()
        sys.exit(0)
    if not args:
        sys.exit(__doc__)
    name = args[0]
    if "--out" in args:
        out = Path(args[args.index("--out") + 1]).expanduser()
    elif name.lower() == "framelink":
        out = FRAMELINK_OUT
    else:
        out = Path.cwd() / "memos"
    main(name, out)
