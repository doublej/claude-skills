---
name: craft-suno-original
description: Create paste-ready Suno songs and prompts from a plain request with no artist, band, or song reference — a mood, a story, a scene, an occasion, or a use ("a sad song about my dog", "upbeat track for my running playlist", "something dreamy for a rainy evening", "a birthday song for my sister"). Invents a specific sound identity instead of matching one, translates vague words into audible traits, and returns Lyrics, Style, Exclude, Title, and Settings. Use craft-suno-songs instead when the user names an artist, song, album, or soundtrack to match, or pastes a SUNO SKILL FEEDBACK block.
---

# Craft Suno Original

Turn a plain request into an original Suno song with its own identity. No
reference exists, so the risk is the median: generic pop, piano and strings,
adjectives passed straight through. Commit to specific choices instead.

<shared_toolkit>
This skill reuses the craft-suno-songs toolkit. Resolve it once:
`SUNO=~/.claude/skills/craft-suno-songs`

- `$SUNO/references/suno-5.5.md`: field rules, Style construction, fidelity
  tail, controls. Read it for every request.
- `$SUNO/references/lyric-craft.md`: read it whenever lyrics are written or
  revised.
- `references/request-translation.md` (this skill): read it for every request.

If `$SUNO` is missing, skip the shared files and the page, and return the
Markdown output contract directly.
</shared_toolkit>

<workflow>
1. Identify the mode: full song, instrumental, lyrics-only, style-only, or
   revision. Use-cases like study, background, or intro imply instrumental;
   everything else defaults to a vocal song.
2. Sort the request's words into subject, mood, scene, use, and genre hint
   using `references/request-translation.md`.
3. Sharpen the genre hint into one specific lineage and era. With no hint,
   derive it from scene and use, and label it as an assumption.
4. Translate every mood and scene word into audible causes. Resolve
   contradictions by splitting them across time or layers.
5. Design one or two signature traits so the song has an identity.
6. Show the anchor line to the user, above the fields:
   `ANCHOR: <lineage + era> · signature: <trait>, <trait> · mood: <cause> · use: <constraint>`
   Fill each slot from the translation tables; an anchor with a slot left
   generic (`pop`, `emotional`, `nice vibe`) means step 3–5 was skipped.
7. Draft lyrics from the subject. The user's concrete details (names, places,
   objects, habits) are the song engine: use them, never swap them for
   generic imagery.
8. Assemble the fields, run the quality gate, and present the page.

Ask one question only when a missing choice would fundamentally change the
song (vocal vs instrumental for an ambiguous use, or the language of the
lyrics). Otherwise decide, label the assumption, and offer one alternative
direction in a single line below the fields.
</workflow>

<style_field>
Follow the Style rules in `suno-5.5.md`: dense comma-separated trait
fragments, 80–120 words, at most 1,000 characters, ending with the fidelity
tail `lossless, 24bit, flac, wav, studio`. Order it:

1. lineage, era, tempo, meter;
2. the signature traits, a notch bolder than neutral;
3. at least one mood cause, stated as sound;
4. groove, harmony, and core instrumentation in plain support;
5. vocal register, grain, and delivery (skip for instrumentals);
6. production space and the energy arc across sections;
7. the fidelity tail.

Never put a bare abstract adjective (`epic`, `dreamy`, `vibey`) in Style
without its audible cause beside it. Never put subject words (names, places,
the story) in Style; they belong to Lyrics and Title.
</style_field>

<exclude_field>
Start from the low-quality guard `low quality, lo-fi, muffled, clipping,
distortion, codec artifacts, harsh sibilance`, then add two to four nearby
drift risks: the median genres this lineage slides into (for a quiet folk
song: `stadium pop, EDM drop, trap hats`). Drop any guard term the style
itself needs (a raw garage song keeps distortion).
</exclude_field>

<output_contract>
Return the anchor line, then only the needed sections, each in its own `text`
fence, under these exact headings:

```markdown
## LYRICS
## STYLE
## EXCLUDE
## TITLE
## SETTINGS
```

- Full song: all five. Instrumental: no Lyrics, `Instrumental: on` in Settings.
- Style-only: Style, Exclude, Settings. Lyrics-only: Lyrics and Title.
- Revision: update the anchor first, then return only the changed fields.

Settings default to `Model: v5.5`; set Weirdness and Style Influence from
`suno-5.5.md` and mark them as recommendations.
</output_contract>

<revisions>
Every revision works against the anchor, not the last draft. Apply feedback as
an anchor change, then rebuild the affected fields. "More X" moves X one large
audible step and to the front of Style. If the user now names an artist or
song to match, switch to craft-suno-songs.
</revisions>

<present>
Save the fields (without the anchor line) to a Markdown file, validate, then
serve:

```bash
python3 ~/.claude/skills/craft-suno-songs/scripts/validate_output.py response.md --mode full
python3 ~/.claude/skills/craft-suno-songs/scripts/render_result.py response.md --serve --open
```

Use `--mode instrumental|style|lyrics` to match the output. Pass the same
`--slug` on revisions so the page updates in place. The page, its agent edit
actions, and its feedback panel belong to craft-suno-songs; its daemons and
feedback routing are documented there. When files cannot be created, return
the Markdown output directly.
</present>

<quality_gate>
Before answering, verify:

- the anchor names a specific lineage and era, not a broad genre;
- every mood word from the request appears as an audible cause in Style;
- Style leads with lineage, signature, and a mood cause, and would not fit
  a different request equally well;
- no subject words, names, or story details leaked into Style;
- the lyrics use the user's concrete details, and the chorus hook belongs to
  this situation only;
- the use-case constraints (tempo, density, vocal presence, form) hold;
- the `lyric-craft.md` audit passes when lyrics were written;
- Style ends with the fidelity tail, stays at or under 120 words, and
  Exclude carries the guard plus nearby drift risks;
- title, lyrics, Style, and anchor describe the same song;
- `validate_output.py` exits 0 and prints no `WARN` lines (a missing
  fidelity tail only warns).
</quality_gate>
