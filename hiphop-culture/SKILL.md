---
name: hiphop-culture
description: "Analyze tracks: culture context, BPM, lyrics, visual aesthetic sync"
---

# Hip-Hop Culture

Hip-hop analysis for AI-assisted creative projects. Covers culture context, lyric analysis, BPM math, and visual language.

<culture_context>
**Golden Age Hip-Hop (1987-1997)**: DJ Premier, Pete Rock, RZA — boom bap, heavy samples, jazz/soul breakbeats. Lyricism over hooks.
**East Coast aesthetic**: dark, urban, raw. Graffiti, subway, concrete. Black/grey/gold palette.
**Gang Starr**: Guru (lyricist) + DJ Premier (producer). "Skills" (2003, The Ownerz) feat. KRS-One. 99 BPM, 3:20.
</culture_context>

<bpm_timing_math>
```
beat_interval = 60 / bpm          # seconds per beat
bar_length = beat_interval * 4    # 4 beats per bar
```

For 99 BPM: `beat = 0.606s`, `bar = 2.424s`

Typical verse/hook structure:
- Intro: 0–8 bars (~19s)
- Hook: 8 bars (~19s)
- Verse 1: 16 bars (~39s)
- Hook: 8 bars (~19s)
- Verse 2: 16 bars (~39s)
- Hook: 8 bars (~19s)
- Outro: 4 bars (~10s)
</bpm_timing_math>

<lyric_analysis>
Key thematic elements in "Skills" by Gang Starr:
- "Skills" = craft, mastery, technical excellence
- "Top rank", "vital" = hierarchy, legitimacy
- DJ Premier's signature scratches interpolate KRS-One's voice
- Theme: real MC knowledge vs imposters

Map lyrics to visual triggers: identify **nouns** (skills, mic, beats) and **verbs** (drop, flow, rock) as animation cue words.
</lyric_analysis>

<visual_aesthetic>
## Visual Aesthetic for Hip-Hop Video

```
Background: #0a0a0a (near-black)
Primary text: #f5f5f5
Accent/highlight: #FFD700 (gold) or #FF4444 (red)
Font: monospace or graffiti-adjacent (bold, condensed)
Transitions: hard cuts, glitch, VHS scanlines
Beat markers: flash white on downbeat
```
</visual_aesthetic>

<workflow>
1. Get BPM + duration → calculate beat grid
2. Map lyrics to timestamps (manual or via whisper transcription)
3. Identify key words for visual triggers
4. Define aesthetic palette matching era/artist
5. Hand to `lyric-video-maker` skill with timing data
</workflow>
