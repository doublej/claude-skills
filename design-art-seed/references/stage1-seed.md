# Stage 1 — Seed (philosophical fragments)

Output: a single markdown file titled `<topic-slug>-seed-for-art.md`, saved to `<projectroot>/tmp/`.

## Purpose

Strip the source of argument, chronology, and proper nouns. Leave only the metaphors that *survive being read alone*.

It is **not** the letter, the report, the plan, or the timeline.

## Tone register — required input

Stage 1 is dominated by tone register. The user picks one in the clarify step; everything below switches on it.

| Register | When to use | Default mood | Banned by default |
|----------|-------------|--------------|-------------------|
| `warm` | Default. Most material — including heavy material — lands better here. | Curious, present, attentive, slightly amused. | Lament, ghost vocabulary, funeral imagery. |
| `wry` | Bureaucratic, institutional, absurd source. | Dry, deadpan, light-touch sardonic. | Sentimentality, declarations of feeling. |
| `neutral` | Technical, scientific, infrastructural source. Codebases, schemas, processes. | Observational, precise, no editorial. | Metaphor that imports affect. |
| `playful` | Light source. Hobby, family, celebration, craft. | Buoyant, generous, mischievous. | Critique, complaint, irony at expense of subject. |
| `clinical` | Medical, legal, evidentiary source where neutrality is the point. | Detached, granular, no figuration. | Anything that reads as opinion. |
| `elegiac` | When the work *is* a lament — eulogy, loss, witness. | Mournful, withdrawn, reverential. | Cheer, undermining, deflection. |

**Default to `warm` if the user does not pick.** The condensation grammar is structurally elegiac; choosing `warm` is the active choice that prevents drift.

## The melancholy-default trap

When you strip names/dates/argument from any source, the grammar that survives reads as "object + condition" — *the X that remains, the X that does not arrive*. This noticing-of-absence pattern is the default failure mode of this skill. Counter it actively:

1. **Presence/absence split.** At least **40 % of fragments must inventory what is here**, not what is gone. Even on heavy source. The dandelion in the brick gap is the work; the missing fence is decoration.
2. **Verb register.** Use verbs from the register's whitelist. Avoid the dour-default verbs unless the register is `elegiac`.
3. **No funeral grammar.** Avoid the rhetorical tics of mourning unless register=elegiac: sentences shaped as "the X for the Y that was…", "the absence of…", "what is left of…", repetition triplets, italicised single-line laments.

### Verb whitelist by register

| Register | Use freely | Avoid |
|----------|-----------|-------|
| `warm` | keeps, holds, watches, returns, notices, refuses, names, walks, opens, gathers, learns, repairs, lights, plants, greets | decays, drifts, mourns, ghosts, dissolves, erodes |
| `wry` | files, drafts, signs, stamps, forwards, schedules, minutes, ratifies, footnotes, asterisks, addends | weeps, laments, hollows, vanishes |
| `neutral` | runs, returns, accepts, emits, parses, queues, retries, persists, resolves | (no banned list — but no metaphor that imports mood) |
| `playful` | dances, hums, paints, throws, catches, tries, fails, tries again, wakes, eats | judges, criticises, sighs |
| `clinical` | observed, recorded, measured, present, absent, indicated, noted | (no banned list — every verb is an observation) |
| `elegiac` | (full vocabulary unlocked — including the dour-defaults) | — |

### Forbidden vocabulary by default

Unless register=`elegiac`, **do not use** these without the user explicitly invoking them: *ghost, lament, mourn, void, decay, ruin, rumour-as-pejorative, hollow, withered, fading, slow death, what is left of, all that remains*.

These words feel literary; they do most of the dour-default's lifting. Replace with concrete observation in the chosen register.

## Required structure

```markdown
---
title: <Topic> — Seed for art
author: <user>
date: <YYYY-MM-DD>
status: seed
register: <warm | wry | neutral | playful | clinical | elegiac>
tags: [<topic>, art, philosophy, seed]
purpose: Compressed philosophical fragments drawn from the <topic> material, intended as raw material for art — not a letter, not a complaint, not a plan
---

# Seed

---

<Fragment 1>

---

<Fragment 2>

---

…

---

## Motifs (to grow)

- <motif 1>
- <motif 2>
- …

## Possible forms

- **<Form name>.** <One-paragraph pitch.>
- …

## A note on register

<One sentence: what this seed is NOT.>
```

## Fragments — rules

- **8–12 fragments**, separated by `---` rule lines.
- **Presence/absence split:** at least 40 % must be presence-fragments (what is here, what continues, what was found), regardless of register.
- Each fragment **must survive being read alone**. No fragment should require its neighbours.
- **No names. No dates. No quantities** — except where a quantity becomes rhythmic (e.g. "five years", "157 e-mails"). When in doubt, cut the number.
- **Pure metaphor or pure observation.** No argument, no chronology, no list of grievances, no call to action.
- **English only.** Compose every fragment in English regardless of the source's original language. A non-English proper noun or technical term may appear inline as a quotation, but never as a new composed sentence. If a phrase from the source is load-bearing, translate it and note the original term in parentheses on first use only.
- One fragment per logical thesis. If a fragment contains "and also", split.

### Example fragments — same source, three registers

Source: a long-running municipal complaint about a street modification.

**`warm`:**
> The drawing is still in the drawer. The drawer is still in the desk. The desk is still mine. I open it on Sundays and read with the calm of a man who has chosen what he keeps.

**`wry`:**
> The committee is the room you cannot enter. It is also the room *they* cannot leave. We have this in common — neither of us has been to the meeting.

**`elegiac`:**
> Trust is a fence that was removed to make room for a fence that will not be built.

Notice how the same situation — kept drawing, distant committee, removed fence — moves from quiet stewardship (warm) to deadpan-companionable (wry) to mourning (elegiac). Choose the register; the words follow.

### Strong fragment shape

- Concrete subject + reframe in 1–2 short sentences. Stops.
- Names a thing that exists or persists.
- Avoids stating a feeling outright; lets the image carry the feeling.

### Weak fragment shape

> The system has many problems and citizens often feel unheard, which leads to frustration over time.

Generic. No image. Cut.

## Motifs — rules

- **8–10 visual hooks.**
- Each is **a concrete object + an abstract framing**, in noun-and-verb form, *in the chosen register's affect*.
- ✓ warm: "the resident as Sunday archivist of a file the desk holds for him"
- ✓ wry: "the committee as a room that meets without minutes, like a band that rehearses without a setlist"
- ✓ elegiac: "the citizen as archivist of a file the archive refuses to open"
- ✗ "the bureaucratic feeling" (adjective, no object)

The motifs are what stage 3 reaches for when assigning images. Register-mismatched motifs produce register-mismatched images.

## Possible forms — rules

- **6–10 media-form pitches.**
- Each is a one-paragraph specification: *medium · contents · framing*. Three beats. Stops.
- Range across registers' affordances (see stage 2 cassettes for register-appropriate forms).
- Drop forms that fight the chosen register. A `warm` seed should not propose a *funeral procession installation*; an `elegiac` seed should not propose a *birthday card series*.

## A note on register — closing line

One sentence at the foot of the file. State what this seed is **not**.

> This is not the letter. The letter is elsewhere — it argues, it asks, it escalates. This piece does not argue. It condenses.

The function: protect the seed from being read as complaint, plan, or brief.

## Process — what to do with the source

1. Read or skim. Identify 5–8 *recurring concrete objects*.
2. For each object, ask: **what is here, around it, that continues?** — and only secondarily: what is missing? Counter the absence-bias from the start.
3. From the objects, draft fragments. Aim for ≥40 % presence-fragments. Drop weakest until 8–12 remain.
4. Cross-check verb register against the register table. Replace banned verbs.
5. Motifs come from the surviving fragments.
6. Forms come last. Browse the motifs and ask: *which medium would carry this in the chosen register?*

## Verification before stage 2

- [ ] Register declared in frontmatter.
- [ ] ≥8 fragments, each ≤3 sentences, each survives standalone.
- [ ] ≥40 % of fragments are presence-mode (what is here / continues / was found).
- [ ] Verb register matches the chosen register's whitelist.
- [ ] No banned vocabulary present (unless register=`elegiac`).
- [ ] No proper nouns in fragments.
- [ ] All numbers either rhythmic or cut.
- [ ] ≥8 motifs, each concrete object + abstract framing, in chosen register.
- [ ] ≥6 form pitches, each in `medium · contents · framing` shape.
- [ ] Closing note declares what the seed is *not*.

If any check fails, revise before showing the user.
