---
name: design-art-seeddescription: "Distill any source into a 3-stage art seed: philosophical fragments, formal variations, editorial illustration brief. Triggers on philosophical seed, art seed, editorial illustration brief, image prompt from dossier, turn this project into images."
---

<intro>

Convert dense source material into prompts an external image-gen tool (Midjourney, Imagen, Nano-Banana) or human illustrator can act on. **No image generation inside this skill** — only markdown deliverables.

</intro>

<rationale>

Going `data → image` produces AI slop. Going `data → philosophy → motif → brief` strips literalism at every step. The canonical run (see `references/example-orac.md`) turned a 5-year, 157-email municipal complaint into 5 published editorial illustrations the user describes as "amazing".

</rationale>

<stages>

| # | Stage | Output | Purpose |
|---|-------|--------|---------|
| 1 | Seed | `<topic>-seed-for-art.md` | Philosophical fragments + motifs + possible forms |
| 2 | Variations | `<topic>-seed-for-art-variations.md` | Nine formal registers (inventory, liturgy, glossary…) |
| 3 | Brief | `<topic>-seed-for-art-editorial.md` | Editorial illustration brief, hex-coded, artist-named |

Stage N depends on stage N-1's output as raw material — but each stage's deliverable also stands alone.

</stages>

<workflow>

### 1. Clarify the source — and explain why each question matters

Do **not** dump a bare question list. Open with one short paragraph that frames what's about to happen, then ask only what you can't infer. Each question gets a one-line *why*.

Template:

> This skill turns a source — a dossier, project, life event, codebase, essay — into prompts for an external image tool. Three stages: philosophical fragments → nine register-shifted variations → an editorial illustration brief. Before I start, I need a few things:
>
> **Source.** What material am I working from? *— I need something to read; a file path, folder, pasted text, or a conversation we've had.*
>
> **Tone register.** Pick one — *warm* (default), *wry*, *neutral*, *playful*, *clinical*, *elegiac*. *— Condensation defaults to melancholy if I let it. Picking a register early stops the seed from drifting dour. Even heavy source material usually lands better as wry-warm than as lament; choose elegiac only if you want the work to be a dirge.*
>
> **Medium ambition.** What is the eventual artwork? *— A print series wants different motifs than a sound piece or a single magazine illustration. Shapes what stage 1 reaches for.*
>
> **Stages.** Run all three, or just one? *— Default is all three with confirmation between each. Pick one stage if the earlier output already exists.*

**Output language: English only.** All fragments, variations, captions, and brief sections are written in English regardless of the source's original language. Quote a non-English term inline only when it is a *proper noun or unique technical term* with no English equivalent (and even then, gloss it in English). Never compose new sentences in another language.

Skip a question if you can already infer the answer. If the user has provided no source at all, the source question is the only one that matters until they answer it.

**Tone register is load-bearing.** Once chosen, it propagates to every stage:
- Stage 1 fragment rules + verb whitelist switch by register.
- Stage 2 form cassette switches by register (different nine slots).
- Stage 3 tone hierarchy + medicine-accent + artist weighting inherits the register.

Default: `warm`. The canonical ORAC run was elegiac source rendered into a *warm* brief — that's the lesson, not "always be elegiac".

### 2. Stage 1
Load `references/stage1-seed.md`. Produce fragments file. Show the user; ask if they want to proceed to stage 2.

### 3. Stage 2
Load `references/stage2-variations.md`. Produce nine-registers file. Show the user; confirm before stage 3.

### 4. Stage 3
Load `references/stage3-brief.md`. Produce editorial brief. Hand off — do not generate images.

### 5. Hand-off
State explicitly: "Brief saved at `<path>`. Paste into Midjourney / Imagen / Nano-Banana, or hand to an illustrator. Skill ends here."

### Argument resolution
- `$ARGUMENTS = 1|2|3` → run only that stage. Source for stage 2/3 must already exist or be supplied.
- `$ARGUMENTS = all` (default) → run all three with confirmation between each.

</workflow>

<anti_patterns_check>

Always read `references/anti-patterns.md` once per session. The failure modes there ("moody and atmospheric", "a figure stands in shadow", generic NOT-lists) are what a skilled brief actively closes off.

</anti_patterns_check>

<output_conventions>

- **Save location: always `<projectroot>/tmp/`**. Create the directory if it does not exist. Never write inside any `.claude/` directory or other config/state path. If `<projectroot>` is ambiguous (no git root, no obvious project), use the current working directory's `tmp/`.
- File naming: `<topic-slug>-seed-for-art.md`, `-variations.md`, `-editorial.md`. Slug uses kebab-case.
- Frontmatter on each: `title`, `author`, `date` (today, `YYYY-MM-DD`), `status: seed`, `tags`, `purpose`.

</output_conventions>

<what_not>

- Not a image generator. Stop at the brief.
- Not a project-management or planning tool. Output is artistic raw material.
- Not domain-specific. Works on any source where you can identify a thesis.

</what_not>

<references>

| File | Load when |
|------|-----------|
| `references/stage1-seed.md` | Producing fragments + motifs + forms |
| `references/stage2-variations.md` | Producing nine formal registers |
| `references/stage3-brief.md` | Producing editorial illustration brief |
| `references/anti-patterns.md` | Always — once per session |
| `references/example-orac.md` | Reading the canonical run for shape and tone |

</references>
