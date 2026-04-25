# Stage 2 — Variations (nine formal registers)

Output: a single markdown file titled `<topic-slug>-seed-for-art-variations.md`, saved to `<projectroot>/tmp/`.

## Purpose

Take the seed from stage 1 and re-form it through nine distinct voices. Each variation is the **same source material in a different formal register**. Friction between the nine voices is the work.

The form encodes affect more than the words do. A liturgy *is* funereal-pattern — even if the words try to cheer, the structure hangs black crepe. So the **form cassette** switches with the register chosen in stage 1.

## Cassettes — pick one based on stage 1 register

| Register | Cassette | Affect |
|----------|----------|--------|
| `warm` (default) | **Warm cassette** | Curious, present, attentive, generous |
| `wry` | **Wry cassette** | Deadpan, dry, lightly sardonic, companionable |
| `neutral` / `clinical` | **Neutral cassette** | Observational, precise, no editorial |
| `playful` | **Playful cassette** | Buoyant, mischievous |
| `elegiac` | **Elegiac cassette** | Mournful, withdrawn, reverential |

If the user picked a register stage 1 didn't anticipate, build a cassette by drawing forms whose *structure* matches the affect.

## Required structure

```markdown
---
title: <Topic> — Seeds for art, variations
author: <user>
date: <YYYY-MM-DD>
status: seed
register: <inherited from stage 1>
cassette: <warm | wry | neutral | playful | elegiac>
tags: [<topic>, art, philosophy, seed, variations]
purpose: Formal variations on the <topic> material — each a distinct register. Companion to `<topic-slug>-seed-for-art.md`.
---

# Seeds — variations

*Nine forms, one experience. Each stands alone.*

---

## 1 — <Form name>

<…>

…

---

## A note on use

<one paragraph>
```

---

## Warm cassette — default

### 1 — Inventory of presences
What is here, in this hour. A bullet list of objects, sounds, light, neighbours, daily rhythms — not absences. End with one line that opens forward, e.g. *More arrives tomorrow.*

### 2 — Postcard
Second person, addressed to a friend who has not seen the place/situation. 6–10 short sentences. Casual, attentive, the writer noticing something good. End with a small generous gesture (*come visit; the light at six is the kind you'd like*).

### 3 — Field note (naturalist)
The source observed as if by a careful naturalist. Date and location at top. 4–6 short paragraphs noting *what thrives* in the situation: which species of attention, which behaviours, which patience. Latin-style binomials are welcome (*archivus paterfamilias*). Tone: respectful curiosity.

### 4 — Glossary (warm)
A small dictionary of the domain's vocabulary. 6–8 terms. For each: the formal definition, and a second definition written from inside, *generous and observed*. Not sardonic — appreciative. The second definition reveals what the term means to someone who lives it.

### 5 — Walking tour
First-person plural, present tense. *We start at the corner. We turn here. Look at this.* 6–8 stops. The voice is a friendly local. Stops point to small specific things — a brick, a window, a habit.

### 6 — Letter to the next [resident / maintainer / steward]
Written to whoever inherits the situation after you. Tone: warm handover, not warning. What the next person will love. What is worth keeping. One small thing they should know on day one.

### 7 — Catalogue of small wins
A numbered list of small daily/weekly wins inside the situation. 8–12 entries. Each one specific, modest, real. Not self-help — observation. *3. The Sunday rhythm of opening the drawer.*

### 8 — Object monologue (companionable)
Speak as a non-human object central to the source. First person, present tense. 6–10 short lines. Tone: matter-of-fact, slightly amused, *not lonely*. The object likes its job. End with one line addressed to a regular companion.

### 9 — Almanac entry
Format as a dated almanac page. Weather, sunrise/sunset, the day's small observances, a seasonal note. The source's situation appears as one of several attentive observations of the day. The form is calendrical, not narrative.

---

## Wry cassette

### 1 — Inventory (deadpan)
A bullet list of what is on site, presences and absences both, written with no editorial. The deadpan IS the joke. End with one flat line that lands the absurdity, *e.g. All elements have been ratified except the elements.*

### 2 — Glossary (sardonic)
A small dictionary. For each term: 1. formal definition. 2. sardonic-but-not-bitter definition that lands the lived experience. *appointment — n. 1. an agreement between two parties. 2. a state of mind held exclusively by one of them.* The second definitions are short and sharp.

### 3 — Memo (parody)
A pitch-perfect parody memo, header and all. *To: <department>. From: <sender>. Re: <subject>. Date: [unspecified].* Drained of content; the form is the joke. 4–6 numbered paragraphs each ending in `[deferred]`, `[noted]`, `[under consideration]`.

### 4 — Patch notes / changelog
Format as a software changelog or release notes for the situation. *v5.2.0 — added third committee. v5.2.1 — committee removed for compliance reasons.* Funny because true.

### 5 — FAQ
Numbered Q&A. 6–8 pairs. The questions are sincere; the answers are dry. Last Q gets a one-word answer that lands the whole piece.

### 6 — Object monologue (deadpan)
Object speaks first person about its job. Tone: a worker explaining the role to a stagiair. *I'm a hole in the ground. The work is steady.* Not lonely; bored-professional.

### 7 — Instructions
Numbered list — 10 to 14 steps — for performing the role the source forces on the user. Imperative second person. Steps build from naïve to seasoned. End with two or three lines that name the role plainly.

### 8 — Brochure
Marketing copy for the situation as if it were a product. *Underground Containers — Now With Forty-Plus Daily Impacts!* Headline, three feature bullets, a fine-print disclaimer. Don't break the deadpan.

### 9 — Postscript
A one-paragraph postscript appended to a longer (unseen) document. Begins *P.S. —* and contains the one observation the document forgot. The forgotten observation is the load-bearing line of the entire piece.

---

## Neutral / clinical cassette

### 1 — Inventory
Bulleted list of items present at the site/in the source. No editorial. Counts where applicable. Sorted by category.

### 2 — Schema / spec
The situation rendered as a technical spec. Headings: *Inputs · Outputs · State · Failure modes · Dependencies*. 1–3 lines under each. Reads like documentation.

### 3 — Glossary (definitional)
Domain vocabulary. One precise definition per term. No second definition. The definitions themselves carry the case if written closely.

### 4 — Procedure
Numbered procedure, 8–12 steps. Imperative. The procedure documents the actual chain of events as if it were a runbook.

### 5 — Datasheet
A datasheet-style table. Rows: *Property · Value · Tolerance · Notes*. Each row a small fact about the source.

### 6 — Classification key
A dichotomous key, biology-textbook style. *1a. If <condition>, go to 2. 1b. If <other>, go to 5.* Leads the reader through the situation by branching.

### 7 — Provenance record
A museum-style provenance record. Tracks the central artifact through hands, dates, conditions. Plain, archival.

### 8 — Field note (observational)
Date, location, conditions. Plain prose. What was observed. Three or four short paragraphs.

### 9 — Citation list
Numbered citations. Each citation references a real (or pseudo-real) document, conversation, photograph from the source. Format: *[1] <author>, "<title>", <date>.* 8–12 entries.

---

## Playful cassette

### 1 — Inventory of curiosities
A mock museum-vitrine list. Each item gets a short whimsical label.
### 2 — Recipe
Ingredients and method for becoming/making something inside the source. Cooking-show prose; specific quantities, generous timing.
### 3 — Anthem
Verse-and-chorus. Three short verses, one repeating chorus. Cheerful, in the source's vocabulary.
### 4 — Birthday card
Front: greeting. Inside: the punchline-as-message.
### 5 — Glossary (delighted)
Each term gets a definition that sounds like a child's enthusiasm explained back.
### 6 — Treasure map key
Numbered legend for an unseen map. 1=the start, 2=the obstacle, … N=the prize. The legend tells the story.
### 7 — Jingle
Short lyric in the rhythm of an advertising jingle. 8–12 lines.
### 8 — Object monologue (excited)
The object speaks first person, slightly hyper, about its job. Tone: enthusiast.
### 9 — Greeting card range
Five greeting-card front-fronts: *Sympathy · Congratulations · Get Well · Thank You · Just Because*, each repurposed for a moment in the source.

---

## Elegiac cassette

*Use only when the work is meant to be a lament, an elegy, a witness. Not the default.*

### 1 — Inventory (of what remains)
What is left on site, as of `<date>`. Bullets. End with the line *All else has been removed, pending the arrival of nothing.*

### 2 — Minutes (never sent)
Bureaucratic form drained of content; closes with three flat institutional finalities.

### 3 — Object monologue (confessional)
Object speaks first person; lonely, tired, addressed to the one person who has left.

### 4 — Liturgy
Call-and-response prayer form. Six pairs. Closes with one italic English line: *Amen, on behalf of the directly affected.* Always written in English regardless of source language.

### 5 — Glossary (wounded)
Stacked definitions, second definition cuts.

### 6 — One breath
Single recursive sentence ending with `…`.

### 7 — Diary of the [object]
The artifact narrates its history in dated entries, ending in present loneliness.

### 8 — Missing persons report
Police-template format for an absent thing. Status: *missing*.

### 9 — Instructions (for becoming the role)
Numbered. Closes *Accept that the organization has no nervous system. / Accept that you are it. / Report what it cannot feel.*

---

## A note on use — how to close

One paragraph. State that these are not drafts of a single work; they are nine entry points into one experience. Any can be developed, combined, abandoned, or pressed against its neighbour. End with one sentence of *what is fixed* across all nine — the single load-bearing observation the source rests on, written in the chosen register.

## Verification before stage 3

- [ ] Cassette declared in frontmatter, matches stage 1 register.
- [ ] All nine sections present, in the cassette's listed order.
- [ ] Each section is in a distinctly different voice. If two read alike, rewrite the weaker.
- [ ] No section drifts into the dour-default unless cassette is `elegiac`.
- [ ] Each section can be quoted in isolation as a printable artwork.
- [ ] Closing "note on use" declares the fixed observation in the register's affect.
