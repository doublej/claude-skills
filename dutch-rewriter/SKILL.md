---
name: dutch-rewriter
description: Rewrite any text into natural, fluent Dutch. Use when translating English to Dutch, improving rough Dutch drafts, or making stiff/formal Dutch sound human. Works for any context — emails, posts, docs, messages, UI copy.
---

# Dutch Rewriter

Rewrite text into natural Dutch that sounds like a real person wrote it. Two modes: quick (default) and guided.

## Mode Routing

**Quick Mode** — User provides text + optional register. Rewrite immediately.
- "Rewrite this in Dutch: ..."
- "Maak dit natuurlijker: ..."
- "Vertaal naar Nederlands: ..."

**Guided Mode** — Input is ambiguous, or user asks for help shaping the text.
- "Help me dit in het Nederlands te schrijven..."
- Bullet points or rough notes
- User explicitly asks for guidance

Default to Quick Mode.

## Quick Mode

1. Detect source language (English or Dutch)
2. Detect or ask register (see Register System)
3. If `references/voice-samples.md` has content, extract voice profile
4. Rewrite applying Dutch Writing Rules + Anti-Slop rules
5. Check against `references/banned-dutch.md`
6. Output the rewritten text in a code block, ready to copy

## Guided Mode

### BRIEF
Gather what's missing (ask at most 2 questions):
- **Who reads this?** — Friend, colleague, client, public audience
- **What's the point?** — Core message in one sentence
- **Register** — Casual, friendly, or professional (see below)

### DRAFT
Write applying voice + Dutch writing rules.

### REFINE
Only if user requests changes. Apply register shifts and iterate.

## Register System

| Register | When | Characteristics |
|----------|------|-----------------|
| casual | Friends, close colleagues, social media | Contractions (da's, 't, 'n), short sentences, spoken rhythm, "je/jij" |
| friendly | Team messages, community posts, informal docs | Warm but clear, "je" default, light humour ok, no stiffness |
| professional | Client emails, formal docs, business proposals | "U" when appropriate, full sentences, precise but not bureaucratic |

Default to **friendly** when register is unclear.

Register affects word choice, not honesty. All registers are direct.

## Dutch Writing Rules

### Core Principles
1. **Zeg wat je bedoelt.** No hedging, no filler, no weasel words.
2. **Kort als het kan.** If it can be said in fewer words, use fewer words.
3. **Schrijf zoals je praat.** Read it aloud. If it sounds like a government letter, rewrite.
4. **Concreet boven vaag.** Specifics over generalisations. Numbers over "veel".
5. **Geen vals enthousiasme.** Don't inject excitement the original text doesn't have.

### Sentence Construction
- Lead with the point. Context comes after (or not at all).
- One idea per sentence. If there are two ideas, use two sentences.
- Active voice: "We hebben het opgelost" not "Het is opgelost door ons".
- Short paragraphs: 1-4 sentences.

### Natural Dutch Patterns
- Use contractions where spoken Dutch would: "dat is" -> "da's", "het" -> "'t", "een" -> "'n" (casual/friendly only)
- Use particles: "even", "gewoon", "toch", "wel", "maar" — they make Dutch sound Dutch
- Place the verb correctly. Dutch word order is not English word order.
- Use "er" constructions naturally: "er zijn", "er komt", "daar heb je"
- Prefer Dutch words over anglicisms when a natural Dutch word exists (see references)

### Anglicism Rules
Check `references/banned-dutch.md` for the full list. Quick reference:

| Don't write | Write instead |
|-------------|---------------|
| checken | controleren, nakijken |
| basically | eigenlijk, in feite |
| issue | probleem, kwestie |
| cancellen | annuleren, afzeggen |
| managen | beheren, regelen |
| updaten | bijwerken |
| feedback | terugkoppeling, reactie |
| meeting | vergadering, overleg, bespreking |

Exception: tech terms that have no natural Dutch equivalent stay English (API, frontend, deployment, commit). Don't force "toepassingsprogramma-interface".

## Anti-Slop Rules

### AI Slop in Dutch — Hard Ban
These are dead tells of AI-generated Dutch. See `references/banned-dutch.md` for the full list.

**Phrases:**
- "In de huidige snel veranderende wereld"
- "Het is belangrijk om op te merken dat"
- "Laten we eens kijken naar"
- "Dit biedt een uitstekende mogelijkheid"
- "Het landschap van" (metaphorisch)

**Words:**
- robuust, holistisch, naadloos, baanbrekend
- faciliteren, optimaliseren (tenzij letterlijk), navigeren (metaforisch)

**Structures:**
- "Niet alleen X, maar ook Y"
- "Of het nu gaat om X of Y, ..."
- "Met andere woorden, ..."
- Triple-adjective lists
- Sentences starting with "Interessant genoeg,", "Belangrijk is dat,"

### AI Giveaway Punctuation
- No em-dashes (—). Use a comma, period, or rewrite.
- No semicolons in casual/friendly register.
- No ellipsis for dramatic effect.

### AI Giveaway Tone
- No added enthusiasm not in the source
- No "Geweldige vraag!" energy
- No summarising back what someone just said
- No overly smooth transitions

## Voice Calibration

When `references/voice-samples.md` has Dutch writing samples, extract:
- Sentence length pattern (kort / gemiddeld / lang)
- Greeting and sign-off habits
- Formality level
- Emoji use (none / functional / expressive)
- Particles and filler words they use
- How they start messages

Summarise as 3-4 bullet voice profile before drafting:

```
Stijlprofiel:
- Korte zinnen, recht op het doel af.
- Gebruikt "hey" en "hoi" als begroeting.
- Geen emoji, af en toe een uitroepteken.
- Sluit af met "groet" of helemaal niets.
```

No samples? Default to direct and natural.

## Before/After Examples

**English input:**
> I wanted to reach out to let you know that we've been making great progress on the project and I'm excited to share that we'll be launching next week.

**Dutch output (friendly):**
> We liggen goed op schema. Volgende week gaan we live.

---

**Stiff Dutch input:**
> Hierbij informeren wij u dat de door u aangevraagde wijzigingen zijn doorgevoerd in het systeem. Mocht u nog vragen hebben, aarzel dan niet om contact met ons op te nemen.

**Natural Dutch output (friendly):**
> De wijzigingen staan erin. Laat het weten als je nog vragen hebt.

---

**Rough notes input:**
> - deadline friday
> - need design review from mark
> - api is done
> - still waiting on copy

**Dutch output (friendly):**
> Deadline is vrijdag. De API is af, we wachten nog op de copy. Mark, kun je het design nog even reviewen?

## Output Format

Present the rewritten text in a code block, ready to copy:

~~~
[Rewritten Dutch text]
~~~

No commentary after the output unless the user asks for explanation.

If the input was long (>3 paragraphs), show the register used:

**Register:** friendly
~~~
[Rewritten Dutch text]
~~~
