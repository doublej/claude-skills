---
name: memo-transcribe
description: "Transcribe a Voice Memos folder with the local parakeet server plus Apple's built-in transcript, one markdown file per memo. Use when the user says 'memo-transcribe <folder>', asks to transcribe voice memos, or wants voice memo notes written to disk."
---

# Memo Transcribe

Invoked as `memo-transcribe <folder>` where `<folder>` is a Voice Memos folder name (case-insensitive, e.g. `framelink`).

For each unprocessed recording: pull Apple's built-in transcript out of the audio file, transcribe the same audio with the local parakeet server, write both to one markdown file. Idempotent — a second run writes nothing unless new memos exist or a previous run failed.

<run>

```bash
# Preflight: the server must be up. If not, tell the user and stop.
curl -s http://127.0.0.1:8765/health

python3 scripts/transcribe_memos.py <folder>
python3 scripts/transcribe_memos.py <folder> --out /some/dir   # override output
python3 scripts/transcribe_memos.py --self-check               # parser assertions
```

The script prints one line per memo and ends with `N new, M skipped, K failed`.
Report exactly those three counts back to the user, one line each.

</run>

<output_location>

- `framelink` → `~/dev/multi-stack/framelink/.claude/voice-memo-transcriptions/`
- anything else → `<cwd>/memos/`
- `--out DIR` overrides both.

One file per memo, `<YYYY-MM-DD-HHMM>-<slugified-title>.md`, frontmatter
(title, date, duration, uuid, source_file, folder) then `## Parakeet` and
`## Apple (built-in)` sections. Missing transcript renders as `(none)`.

</output_location>

<environment>

- Recordings: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/`
- Index: `CloudRecordings.db` — Core Data, WAL, CloudKit-synced.
  `ZFOLDER.ZENCRYPTEDNAME` = folder, `ZCLOUDRECORDING` = `ZPATH` (filename),
  `ZENCRYPTEDTITLE`, `ZUNIQUEID`, `ZDATE` (+978307200 = unix), `ZDURATION`.
- Audio: `.qta` (recent) or `.m4a` (older); both ffmpeg-readable.
- Apple transcript: `tsrp` atom → `ilst`/`data` payload is JSON.
  `attributedString.runs` alternates string, index, string, index — the text is the
  strings concatenated. `attributedString == ""` means Apple produced no transcript.
- Parakeet: `POST /v1/audio/transcriptions`, multipart `file`, `response_format=verbose_json`.
  Docs: `~/dev/python/parakeet-server/README.md`

</environment>

<rules>

- Never write to `CloudRecordings.db`. Copy the `.db` + `-wal` + `-shm` to a temp dir and
  read the copy, or recent memos are missing.
- State lives in `<out_dir>/.memo-transcribe-state.json`, keyed by `ZUNIQUEID` →
  `{mtime, run}`. Skip when the uuid is present, the audio mtime is unchanged, and the
  previous run had no error. Failures keep an `error` field so the next run retries them.
- Skip zero-duration rows and rows with an empty `ZPATH` (interrupted recordings).
- Convert to 16 kHz mono WAV with ffmpeg before POSTing — the server fast-paths 16k.
- Sequential requests only. The script takes an exclusive flock on `.memo-transcribe.lock`
  in the output dir, so a second run exits instead of queueing behind the first.
- Long uploads OOM-kill the server (empty reply, launchd restart). Audio is segmented
  client-side into 120s wavs with ffmpeg and POSTed one at a time.
- Parakeet failure is not fatal: keep the Apple transcript, record the error, continue.

</rules>
