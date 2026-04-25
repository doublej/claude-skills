# Stage 3 — Editorial illustration brief

Output: a single markdown file titled `<topic-slug>-seed-for-art-editorial.md`, saved to `<projectroot>/tmp/`.

## Purpose

Convert the seed (stage 1) and the variations (stage 2) into a brief that an external illustrator or image-gen tool can execute without re-reading the source. The brief is **hex-code-rigorous, artist-named, NOT-listed, caption-anchored, thumbnail-tested**.

This is the deliverable handed off. The skill ends with this file saved.

## Register inheritance

The register chosen in stage 1 (warm / wry / neutral / playful / clinical / elegiac) governs three concrete decisions in this brief:

| Decision | warm | wry | neutral | playful | clinical | elegiac |
|----------|------|-----|---------|---------|----------|---------|
| Tone hierarchy | warm first, witty second, observant third | witty first, warm second, dry third | observant first, precise second, generous third | warm first, playful second, generous third | precise first, neutral second, complete third | tender first, restrained second, witty third |
| Medicine accent | a cheerful ochre / butter-yellow / honey, used generously | mustard or salmon, used as one wink per image | none required — clarity is the medicine | rose / mint / sherbet, used freely | none — clinical clarity stands alone | a thin warm note (candle-yellow, terracotta) used once per image to prevent dirge |
| House-reference weighting | Gauld before Gorey, Favre before Le Tan | Gauld, Steinberg, Niemann; Sempé in reserve | Tibaud Hérem, Adolf Born, Edward Tufte school | Niemann, Jullien, Zagnoli; cheerful palette | scientific illustrators (Crosby, Howard) | Quint Buchholz, Jon McNaught, Kitty Crowther |

If register is `warm` (default), the brief should be **affirmatively warm** — not a frustrated brief that adds an ochre wash on top. The warmth lives in subject, posture, light, and humour, not just in the color.

## Required sections

The brief MUST contain all seven sections, in this order.

```
1. Deliverable table
2. Context photograph(s)
3. Visual DNA (palette + cues)
4. House references (named artists)
5. Per-image specs (one block per image)
6. Rules for every image
7. Covering note to the illustrator
```

A short article-style preamble before §1 is allowed (and encouraged) — set the register: literary, wry, confident; warm rather than mournful; sharp rather than sad. State the magazine-equivalent register the brief is targeting (e.g. *De Groene*, *NRC Magazine*, *The New Yorker*, *The Gentlewoman*, *Wallpaper\**).

---

## §1 · Deliverable table

A table specifying N illustrations. Default `N = 5`. Columns:

| # | Kind | Aspect | Target px | Role in article |

Default kinds: `Hero` (16:10, 1600×1000) · `Square` (1:1, 1200×1200) · `Wide` (16:10, 1600×1000) · `Tall` (2:3, 1000×1500) · `End-mark` (4:3, 800×600).

Below the table: a one-paragraph **output format** spec — preferred file format (SVG with `role="img"`, `<title>`, `<desc>`, PNG @ 2× fallback), self-hosted typography names (one serif, one mono), and small ornament conventions (plate number, hairline rule, folio).

## §2 · Context photograph(s)

Heading: *context, not reference*.

- Describe the source images (or other reference artefacts) in 2–3 sentences. Atmosphere only.
- Then a bullet list **Take from the photographs** (3–4 atmospheric properties: typology, scale, light quality, vantage).
- Then a bullet list **Leave behind** (3–4 things to actively discard: clutter, photo colour fidelity, identifiable faces / numbers / addresses).
- Close with: "Look at them, note the *<adjective phrase>*, then put them aside. The illustrations should feel *of* this <subject> without being *from* it."

If the source has no photographs, replace this section with `Reference artefacts` (drawings, sound files, screenshots) and apply the same *take from / leave behind* discipline.

## §3 · Visual DNA — palette + cues

Mandatory:

- **Three to four colour cues by hex.** Always include a warm-cream stock, an ink, one institutional/native colour drawn from the source domain, and one *secondary accent* called out as **"the medicine against dourness"** — used once per image, generously. Without the medicine accent the set goes grey.
- **One geometric cue** — a single recognisable visual element drawn from the source's institutional identity (a diagonal, a stamp, a plate-mark, a serial-number rule, a frame ratio). Used once per image.
- **One typographic hint** — name a serif and a mono. Match register: editorial, not poster.

End with a hierarchy line — the image reads **A first, B second, C third**, drawn from the register inheritance table above.

Hex codes are non-negotiable. Replace every colour name with a hex. `ochre` drifts; `#E3B43B` reproduces.

## §4 · House references

A named-artist list of 6–10 illustrators. Each line: `**<Artist Name>** — <one-clause why>`.

Below the list, a **weighting line** that disambiguates:
> *Gauld before Gorey, Favre before Le Tan, Zagnoli before Mattotti. When in doubt between witty and mournful, choose witty.*

Adapt the names to the brief's tone. The weighting line is the discrimination — adjectives like "minimalist editorial" do not discriminate; "Gauld before Gorey" does.

If the user has not stated which references to weight, **ask before drafting**.

## §5 · Per-image specs

One block per image. Heading: `### NN · <KIND> · *<title in the source domain's language>*`.

Each block contains:

1. **Concept paragraph** (3–6 sentences) — describe the composition: subject, framing, palette deployment, geometric cue placement, *what makes the image land*. Concrete nouns, never adjectives. State the joke or the thesis the image carries — *one thesis per image*.
2. **Caption** in serif italic, set in the article underneath the image. The caption is in the *source's native language* (or bilingual if that is the seed's register). It anchors the image to a literary point.
3. **Thumbnail-readability note** — one sentence: "The image should work at thumbnail (<silhouette description>) and at full size (<the joke or detail that rewards close reading>)."

Each image carries **one thesis**. If a spec says "this image shows X *and also* Y", split into two images or cut Y.

## §6 · Rules for every image

A bullet list, 6–10 items. MUST include:

- A *positive* warmth rule (e.g. "Warm first. Ochre wash, brick tone, sunlit surface.").
- A *tone* rule (e.g. "Wry, not angry.").
- A *no-cartoon* rule that still permits wit.
- A *no-anonymous-figure* rule (silhouettes OK, faceless portraits not).
- A *no-real-names/dates* rule.
- **At least one specific anti-cliché, drawn from the source domain.** ✓ "No Utrecht skyline, Dom tower, or heraldic shield." ✗ "No clichés." Generic NOT-lists do nothing — domain-specific ones close lazy paths.
- A *medicine-accent* rule reminding the illustrator to use the secondary accent generously.
- A *white-space* rule. (e.g. "White space is breath, not silence. A quarter of every image is paper — for air, not for absence.")

## §7 · Covering note to the illustrator

Two short paragraphs.

Paragraph 1 — **Permission to refuse.** "Treat this brief as grammar, not instruction. The <cue> and the <cue> are cues; drop them if the image is stronger without. Any of these N may be refused and replaced — a strong illustrator will propose a <N+1>th image that makes two of these redundant."

Paragraph 2 — **Closing tone declaration.** State the tone hierarchy one more time, in plain prose. End on what the article wins by, and what the images win by — they are different. Example: *the article wins by being read; the images win by being lingered over*.

---

## Optional appendix — Seed library

If you produced more concept candidates than the deliverable count, list them here as a numbered library with `★` marking the chosen ones and `∙` marking the held substitutes. Each line is one half-sentence. Useful for the illustrator to draw from if a chosen image is rejected.

## Verification before saving

- [ ] §1 deliverable table present, with px and aspect ratios.
- [ ] §2 context section uses *take from / leave behind* lists.
- [ ] §3 palette is fully hex-coded; secondary accent named as "medicine".
- [ ] §3 includes one geometric cue and one typographic hint.
- [ ] §4 lists ≥6 named artists and includes a weighting line.
- [ ] §5 — N image blocks, each with concept + caption + thumbnail test.
- [ ] §5 — each image carries exactly one thesis.
- [ ] §6 rules list contains ≥1 *domain-specific* anti-cliché.
- [ ] §7 covering note grants permission to refuse.

If any fails, revise before showing the user.

## Hand-off

After saving, tell the user:
1. The exact path of the saved file.
2. That the brief is paste-ready for Midjourney / Imagen / Nano-Banana, or hand-off to a human illustrator.
3. That the skill ends here — image generation is out of scope.
