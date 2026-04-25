# Canonical run — ORAC Volkerakstraat

The skill's reference implementation. Use this when a user asks "what does a finished version look like?" or when sanity-checking the shape and tone of your own output.

## Files

- **Stage 1 source:** `~/Documents/development/_life/Personal/orac-volkerakstraat-seed-for-art.md`
- **Stage 2 source:** `~/Documents/development/_life/Personal/orac-volkerakstraat-seed-for-art-variations.md`
- **Stage 3 source:** `~/Documents/development/_life/Personal/orac-volkerakstraat-seed-for-art-editorial.md`
- **Resulting illustrations:** `~/Documents/development/_life/Personal/orac-editorial-illustrations/`
  - `01-red-line.png`
  - `02-faceless-committee.png`
  - `03-nervous-system.png`
  - `04-absent-fence.png`
  - `05-one-breath.png`

## Notes on the run

This was the canonical run. Source: a 5-year municipal complaint dossier on the Volkerakstraat 7 case in Utrecht — 157 e-mails, multiple stakeholders, a removed hedge, an unbuilt fence, two underground waste containers, one resident relocated to 10,000 km. Stage 1 was produced from the prompt *"now highly philosophical, as a seed for art"* run on the assembled dossier. Stages 2 and 3 followed directly. Stage 3 was handed to an image-gen tool and produced 5 finished editorial PNGs the user describes as "amazing".

## The lesson is not "always be elegiac"

The canonical run is **elegiac source rendered into a warm brief**. Stages 1 and 2 lean dour because the dossier itself was a complaint; stage 3 actively pushes back ("warm first, witty second, critical third — Gauld before Gorey — the medicine against dourness"). The published illustrations are warm and wry, not mournful, *despite* the source.

The skill now does that lift earlier. Picking `warm` (default) at the clarify step makes stages 1 and 2 affirmatively warm rather than salvaged-from-elegiac at stage 3. If you want the canonical run's output shape on heavy material, pick `wry` for stage 1 and let the brief's warmth land on already-non-mournful seed material.

Read the three files in order. Notice:

- **Stage 1's discipline.** No names, no dates. The municipality is "a rumour"; the citizen is "the nervous system". Eleven fragments, ten motifs, eight forms.
- **Stage 2's range.** Inventory is dry; liturgy is liturgical; the container monologue speaks first-person from a hole in the ground. None of the nine sounds like another.
- **Stage 3's rigour.** Hex-coded palette (`#E30613` Utrecht red, `#E3B43B` daylight ochre, `#F4EFE4` cream stock, `#1A1A1A` ink, `#A67B5B` brick). Eight named artists with weighting (*Gauld before Gorey*). Seven domain-specific NOTs ("no Dom tower, no heraldic shield, no anthropomorphised containers"). Thumbnail test on every image. A closing note granting permission to refuse.

> **Note on the captions.** The canonical run shipped Dutch captions because the article was a Dutch-language web essay. **The skill in its current form produces English captions only.** If you re-run on the same source today, the brief will deliver English captions and the per-image specs will match.

The PNGs are visible evidence the brief worked. When in doubt about the shape of your own output, open both the brief and the illustrations side-by-side and check: *did I match the discipline?*
