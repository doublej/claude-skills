#!/usr/bin/env python3
"""Generate a self-contained HTML5 lyric video from timestamped data."""

import json
import sys
import argparse
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: {bg};
    color: {text_color};
    font-family: 'Courier New', Courier, monospace;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }}

  #scanlines {{
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.15) 2px,
      rgba(0,0,0,0.15) 4px
    );
    pointer-events: none;
    z-index: 100;
  }}

  #beat-flash {{
    position: fixed;
    inset: 0;
    background: white;
    opacity: 0;
    pointer-events: none;
    z-index: 50;
    transition: opacity 0.05s;
  }}

  #main-lyric {{
    font-size: clamp(1.5rem, 4vw, 3.5rem);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: center;
    padding: 2rem;
    max-width: 90vw;
    line-height: 1.2;
    color: {text_color};
    transition: opacity 0.15s, transform 0.15s;
    text-shadow: 0 0 30px {accent}44;
  }}

  #main-lyric.highlight {{
    color: {accent};
    text-shadow: 0 0 40px {accent}88, 0 0 80px {accent}44;
  }}

  #main-lyric.label {{
    font-size: clamp(0.8rem, 2vw, 1.2rem);
    color: {accent}88;
    letter-spacing: 0.3em;
  }}

  #overlay {{
    position: fixed;
    bottom: 2rem;
    left: 2rem;
    right: 2rem;
    font-size: 0.75rem;
    color: {terminal};
    font-family: 'Courier New', monospace;
    opacity: 0;
    transition: opacity 0.3s;
    max-width: 600px;
    white-space: pre-wrap;
    border-left: 2px solid {terminal};
    padding-left: 1rem;
  }}

  #progress {{
    position: fixed;
    top: 0;
    left: 0;
    height: 2px;
    background: {accent};
    width: 0%;
    transition: width 0.1s linear;
    box-shadow: 0 0 8px {accent};
  }}

  #meta {{
    position: fixed;
    top: 1rem;
    right: 1rem;
    font-size: 0.65rem;
    color: {text_color}44;
    text-transform: uppercase;
    letter-spacing: 0.15em;
  }}

  #controls {{
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    font-size: 0.65rem;
    color: {text_color}44;
    cursor: pointer;
  }}

  #status {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.8rem;
    color: {accent};
    letter-spacing: 0.2em;
    text-align: center;
    display: none;
  }}

  .hidden {{ opacity: 0 !important; }}
</style>
</head>
<body>
<div id="scanlines"></div>
<div id="beat-flash"></div>
<div id="progress"></div>
<div id="meta">{artist} — {track_title} // {bpm} BPM</div>
<div id="main-lyric"></div>
<div id="overlay"></div>
<div id="controls" onclick="togglePlay()">[ SPACE ] play/pause</div>
<div id="status">LOAD AUDIO<br>Drop .mp3 onto page or press P to play</div>

<audio id="audio" preload="auto">
  <source src="{audio_src}" type="audio/mpeg">
</audio>

<script>
const LYRICS = {lyrics_json};
const OVERLAYS = {overlays_json};
const BPM = {bpm};
const DURATION = {duration};

const audio = document.getElementById('audio');
const lyricEl = document.getElementById('main-lyric');
const overlayEl = document.getElementById('overlay');
const progressEl = document.getElementById('progress');
const beatFlash = document.getElementById('beat-flash');

let lastLyricIdx = -1;
let lastOverlayIdx = -1;
let beatInterval = 60 / BPM;
let nextBeat = 0;
let raf;

function flashBeat() {{
  beatFlash.style.opacity = '0.06';
  setTimeout(() => beatFlash.style.opacity = '0', 50);
}}

function updateLyric(t) {{
  // Find current lyric
  let idx = -1;
  for (let i = 0; i < LYRICS.length; i++) {{
    if (LYRICS[i].t <= t) idx = i;
    else break;
  }}
  if (idx !== lastLyricIdx && idx >= 0) {{
    lastLyricIdx = idx;
    const entry = LYRICS[idx];
    lyricEl.style.opacity = '0';
    lyricEl.style.transform = 'translateY(8px)';
    setTimeout(() => {{
      lyricEl.textContent = entry.text;
      lyricEl.className = entry.type || 'lyric';
      if (entry.highlight) lyricEl.classList.add('highlight');
      lyricEl.style.opacity = '1';
      lyricEl.style.transform = 'translateY(0)';
    }}, 80);
  }}
}}

function updateOverlay(t) {{
  let idx = -1;
  for (let i = 0; i < OVERLAYS.length; i++) {{
    if (OVERLAYS[i].t <= t) idx = i;
    else break;
  }}
  if (idx !== lastOverlayIdx) {{
    lastOverlayIdx = idx;
    if (idx >= 0) {{
      overlayEl.textContent = OVERLAYS[idx].text;
      overlayEl.style.opacity = '1';
    }} else {{
      overlayEl.style.opacity = '0';
    }}
  }}
}}

function tick() {{
  const t = audio.currentTime;
  updateLyric(t);
  updateOverlay(t);
  progressEl.style.width = (t / (DURATION || audio.duration || 200)) * 100 + '%';

  // Beat flash
  if (t >= nextBeat) {{
    flashBeat();
    nextBeat = Math.floor(t / beatInterval + 1) * beatInterval;
  }}

  raf = requestAnimationFrame(tick);
}}

function togglePlay() {{
  if (audio.paused) {{
    audio.play().catch(() => {{
      document.getElementById('status').style.display = 'block';
    }});
    requestAnimationFrame(tick);
  }} else {{
    audio.pause();
    cancelAnimationFrame(raf);
  }}
}}

document.addEventListener('keydown', e => {{
  if (e.code === 'Space') {{ e.preventDefault(); togglePlay(); }}
}});

// Drag and drop audio file
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => {{
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('audio/')) {{
    audio.src = URL.createObjectURL(file);
    audio.play();
    requestAnimationFrame(tick);
    document.getElementById('status').style.display = 'none';
  }}
}});

// Auto-play attempt
audio.addEventListener('canplaythrough', () => {{
  togglePlay();
}});

// Show first lyric immediately
if (LYRICS.length > 0) {{
  lyricEl.textContent = LYRICS[0].text;
  lyricEl.className = LYRICS[0].type || 'lyric';
}}
</script>
</body>
</html>
"""


def generate(data: dict, out_path: Path) -> None:
    bpm = data.get("bpm", 99)
    lyrics = data.get("lyrics", [])
    overlays = data.get("overlays", [])
    palette = data.get("palette", {})
    audio_src = data.get("audio", "")
    title = data.get("title", "Lyric Video")
    artist = data.get("artist", "")
    track_title = data.get("track_title", "")
    duration = data.get("duration", 200)

    html = HTML_TEMPLATE.format(
        title=title,
        artist=artist,
        track_title=track_title,
        bpm=bpm,
        duration=duration,
        audio_src=audio_src,
        lyrics_json=json.dumps(lyrics),
        overlays_json=json.dumps(overlays),
        bg=palette.get("bg", "#0a0a0a"),
        text_color=palette.get("text", "#f5f5f5"),
        accent=palette.get("accent", "#FFD700"),
        terminal=palette.get("terminal", "#00FF41"),
    )

    out_path.write_text(html)
    print(f"Generated: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="Input JSON file")
    parser.add_argument("--out", default="lyric_video.html")
    args = parser.parse_args()

    if args.input:
        data = json.loads(Path(args.input).read_text())
    else:
        data = json.loads(sys.stdin.read())

    generate(data, Path(args.out))


if __name__ == "__main__":
    main()
