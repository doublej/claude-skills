---
name: prompt-midjourney
description: Write, debug, and iterate Midjourney prompts against the current V8 family (V8.2 default). Use when constructing an MJ prompt, choosing between --sref / --oref / moodboards, setting parameters and weights, scoring returned images and deciding the next action, diagnosing why output misses intent, or porting V6/V7-era prompts to V8. Triggers on "midjourney", "MJ prompt", "--sref", "--oref", "sref random", "style reference", "omni reference", "why does midjourney keep", "make an image prompt for midjourney". For upstream concept work (data → philosophy → motif → brief) use design-art-seed, which hands off to this skill.
---

# Midjourney prompting

<intro>

Craft and iterate Midjourney prompts for the V8 family. Two halves: construct a prompt that earns its
first generation, then read what came back and decide the one thing to change next.

Output is prompt text by default — the user pastes it. Only read `references/execution.md` if they
want generation driven from the session.

</intro>

<version_check>

**V8.2 is the default model (since 2026-07-24). Midjourney shipped three minor versions in four months.**

Training data on this product is stale by construction. `references/parameters.md` is a cache with a
verification date, not truth. Two consequences:

- Never state a parameter's behaviour from memory. Read `references/parameters.md`.
- If the job is high-stakes, or the user reports a flag behaving differently than documented, check
  <https://updates.midjourney.com> before insisting. `docs.midjourney.com` blocks automated fetching —
  use the changelog host, or ask the user to paste the doc page.

The most common source of wrong advice is confidently repeating V6/V7 syntax. `--cref` is dead,
`--q` does not exist on V8, `::` weighting is gone, and `--style raw` is now `--raw`.

</version_check>

<workflow>

## 1. Establish the target

Get to a concrete visual target before writing any prompt words.

- **Reference image given** → break it down across the seven dimensions in `references/diagnostics.md`
  (subject, lighting, colour, mood, composition, material, spatial). With several references, separate
  what is *shared* across them (the aesthetic being asked for) from what *varies* (subject, incidental).
- **Description only** → identify which dimensions the user specified and which they left open. Do not
  silently invent the unspecified ones; either pick deliberately and say so, or ask about the one that
  most changes the result.
- **Neither** ("something cool for the homepage") → this is a style-discovery job, not a prompt job.
  Go to `--draft` + `--sref random` (see step 3) rather than guessing.

## 2. Choose the approach

| Situation | Approach |
|---|---|
| The look is describable in words | Prompt-only. Most transferable — the knowledge works again next time |
| A quality resists description (grain character, specific colour grade, rendering style) | `--sref` on an image or style code |
| A specific face, body, garment, or product must persist | `--oref` + `--ow` |
| Both: hard-to-describe aesthetic *and* explicit subject requirements | Hybrid — `--sref` for the aesthetic, prompt words for the subject. Track which half owns which dimension so you know what to adjust later |
| The user cannot name the look at all | `--draft --sref random` for 24 styles in one job, then pin the winner |

State the approach and why, in one line, before writing the prompt. If it's hybrid, say which
dimensions are coming from the reference.

## 3. Construct

Read `references/parameters.md` for syntax and ranges, `references/translation.md` for turning visual
qualities into words.

```
[subject] [subject details] [environment] [style/mood] [technical] [--flags]
```

- Front-load the subject — word position is weight.
- Stay under ~40 words. Start short; add back only what the output is actually missing.
- Build realism from named components (light setup, film stock, lens, one physical detail), never from
  quality adjectives. "8k, photorealistic, masterpiece" actively degrades V7+ output.
- Abstract mood compounds work directly on V8 — use them.
- Quote text to be rendered, 1–4 words: `a sign reading "OPEN"`.
- Parameters at the very end, two ASCII hyphens.
- Explore in SD or `--draft`; rerun keepers as `--hd`.

## 4. Lint before handing over

```bash
python3 ~/.claude/skills/prompt-midjourney/scripts/lint_prompt.py '<prompt>'
python3 ~/.claude/skills/prompt-midjourney/scripts/lint_prompt.py --json '<prompt>'   # machine-readable
```

Catches dead parameters, out-of-range values, mid-prompt flags, em dashes, HD/aspect-ratio conflicts,
`--no` contradictions, over-long rendered text, and quality-spam words. Exit 1 on any error.

Fix every error. Warnings are judgement calls — resolve or explain them, don't ignore them silently.

## 5. Score and iterate

When the user shares output, work through `references/diagnostics.md`:

1. Score all seven dimensions, 0–1. Say which are readings vs. guesses.
2. Act on the **lowest** dimension, not the mean.
3. Pick the action from the gap→action table — Vary Subtle, targeted prompt edit, `--no`, add `--sref`,
   adjust a weight, Edit/Vary Region, and so on. Changing the prompt is one option among many, and
   often the wrong one.
4. Change **one aspect per iteration**, or the result is uninterpretable.
5. Above ~0.85, prefer Vary Subtle to rewriting — high-scoring prompts are fragile equilibria.
6. When two iterations in opposite directions both lose ground, name the tradeoff and stop optimising.
   Accepting a balanced result is a legitimate outcome, not a failure.

## 6. Hand off

Give the final prompt as a single copy-pasteable line, plus: which approach was used, what each
parameter is doing, and — if iterating — what changed since the last version and what it cost.

</workflow>

<references>

| File | Read when |
|---|---|
| `references/parameters.md` | Any parameter question. Every time — do not answer from memory |
| `references/translation.md` | Turning a reference image or intent into prompt language; choosing `--sw` / `--ow` |
| `references/diagnostics.md` | Output came back; scoring, gap→action, symptom→fix |
| `references/execution.md` | User asks about APIs, MCP servers, or driving generation from the session |

</references>

<rules>

- Read `references/parameters.md` before stating any parameter's behaviour. Stale confidence is the main failure mode of this skill.
- Never emit `--cref`, `--cw`, `--q`, `--turbo`, `--style raw`, or `::` weighting. Run the linter.
- Never pad a prompt with quality adjectives to sound thorough.
- Distinguish what is verified from what is inferred. If a parameter's current behaviour is uncertain, say so and point at the changelog rather than guessing confidently.
- Every generation costs the user real GPU minutes. Don't propose a ten-iteration plan when three targeted changes will do, and don't recommend `--hd` for exploration.
- Scores are preliminary until the user validates them. Present them as readings.

</rules>
