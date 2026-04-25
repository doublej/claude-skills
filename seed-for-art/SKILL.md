---
name: seed-for-art
description: "Distill any source — dossier, project, life event, codebase, essay — into a 3-stage art seed: philosophical fragments, formal variations, editorial illustration brief. Triggers on 'philosophical seed', 'image prompt from dossier', 'editorial illustration brief', 'art seed', 'turn this project into images', 'seed for art'."
arguments: "stage: Literal['1', '2', '3', 'all'] = 'all'"
---

# Seed for Art

Convert dense source material into prompts an external image-gen tool (Midjourney, Imagen, Nano-Banana) or human illustrator can act on. **No image generation inside this skill** — only markdown deliverables.

## Why this exists

Going `data → image` produces AI slop. Going `data → philosophy → motif → brief` strips literalism at every step. The canonical run (see `references/example-orac.md`) turned a 5-year, 157-email municipal complaint into 5 published editorial illustrations the user describes as "amazing".

## The 3 stages

| # | Stage | Output | Purpose |
|---|-------|--------|---------|
| 1 | Seed | `<topic>-seed-for-art.md` | Philosophical fragments + motifs + possible forms |
| 2 | Variations | `<topic>-seed-for-art-variations.md` | Nine formal registers (inventory, liturgy, glossary…) |
| 3 | Brief | `<topic>-seed-for-art-editorial.md` | Editorial illustration brief, hex-coded, artist-named |

Stage N depends on stage N-1's output as raw material — but each stage's deliverable also stands alone.

## Workflow

1. **Clarify source.** Ask: what is the topic? Is it a file/folder/conversation? What is the medium ambition (print, sound, sculpture, film, web essay, single image)? What native language(s) carry case-specific weight?
2. **Stage 1.** Load `references/stage1-seed.md`. Produce fragments file. Confirm with user before stage 2.
3. **Stage 2.** Load `references/stage2-variations.md`. Produce nine-registers file. Confirm before stage 3.
4. **Stage 3.** Load `references/stage3-brief.md`. Produce editorial brief. Hand off — do not generate images.
5. **Hand-off.** State explicitly: "Brief saved at `<path>`. Paste into Midjourney / Imagen / Nano-Banana, or hand to an illustrator. Skill ends here."

Argument resolution:
- `$ARGUMENTS = 1|2|3` → run only that stage. Source for stage 2/3 must already exist or be supplied.
- `$ARGUMENTS = all` (default) → run all three with confirmation between each.

## Before each stage

Always read `references/anti-patterns.md` once per session. The failure modes there ("moody and atmospheric", "a figure stands in shadow", generic NOT-lists) are what a skilled brief actively closes off.

## Stage outputs — file conventions

- File naming: `<topic-slug>-seed-for-art.md`, `-variations.md`, `-editorial.md`. Slug uses kebab-case.
- Default save location: same dir as source material if the source is a file; otherwise ask.
- Frontmatter on each: `title`, `author`, `date` (today, `YYYY-MM-DD`), `status: seed`, `tags`, `purpose`.

## What this skill is NOT

- Not a image generator. Stop at the brief.
- Not a project-management or planning tool. Output is artistic raw material.
- Not domain-specific. Works on any source where you can identify a thesis.

## Reference files

| File | Load when |
|------|-----------|
| `references/stage1-seed.md` | Producing fragments + motifs + forms |
| `references/stage2-variations.md` | Producing nine formal registers |
| `references/stage3-brief.md` | Producing editorial illustration brief |
| `references/anti-patterns.md` | Always — once per session |
| `references/example-orac.md` | Reading the canonical run for shape and tone |
