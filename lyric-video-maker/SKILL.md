---
name: lyric-video-maker
description: "Lyric-synced HTML5 video pages with CSS animations from timed text"
---

# Lyric Video Maker

<description>
Generates a self-contained HTML5 lyric video. Audio plays in browser; lyrics animate on beat using CSS keyframes + JavaScript timing.
</description>

<input_format>

## Input Format

```json
{
  "audio": "path/to/track.mp3",
  "bpm": 99,
  "lyrics": [
    { "t": 0.0,   "text": "[Intro]",           "type": "label" },
    { "t": 4.85,  "text": "Skills...",          "type": "lyric" },
    { "t": 9.7,   "text": "Top rank point blank", "type": "lyric", "highlight": true }
  ],
  "overlays": [
    { "t": 30.0, "text": ">>> Building skills...", "type": "terminal" }
  ],
  "palette": {
    "bg": "#0a0a0a",
    "text": "#f5f5f5",
    "accent": "#FFD700",
    "terminal": "#00FF41"
  }
}
```

</input_format>

<workflow>

## Generate Script

```bash
python3 scripts/generate_video.py input.json --out lyric_video.html
```

Opens `lyric_video.html` in browser. Audio must be local or CORS-accessible.

## Aesthetic Options

- `style: "boom-bap"` — dark bg, gold accent, hard cuts on beats
- `style: "terminal"` — green on black, monospace, scanlines
- `style: "graffiti"` — colorful, bold, spray-paint reveal animations

## Workflow

1. Get lyrics + timestamps (manual, Whisper, or BPM estimation)
2. Prepare `input.json` with timing data
3. Add overlay content from `transcript-capture` output
4. Run `generate_video.py` → open in browser
5. Record screen + mix with audio for final MP4 (use QuickTime or OBS)

</workflow>
