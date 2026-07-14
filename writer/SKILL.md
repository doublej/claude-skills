---
name: writer
description: "Draft/rewrite text: blog posts, Slack/Email/WhatsApp messages, Dutch rewrites. Includes a mandatory watermark-strip filter for messages. Triggers on \"write an email\", \"draft an email\", \"reply to this email\", \"write a blog post\", \"rewrite this\", \"in het Nederlands\", or pasted text the user wants rewritten."
---

# Writer

Write text that says something real, says it clearly, and respects the reader's time.

<mode_routing>

Detect the mode from the user's request:

| Mode | Trigger | What it does |
|------|---------|--------------|
| **blog** | "write a blog post", "article", "tutorial", "opinion piece", "case study" | Full blog workflow |
| **message** | "Slack message", "email", "WhatsApp", "Telegram", platform name mentioned | Platform-native message |
| **rewrite** | "rewrite this", "clean this up", "make this better", pasted text without platform/language target | Clean up existing English text |
| **dutch** | "in het Nederlands", "vertaal", "naar Nederlands", "maak dit natuurlijker", Dutch text input | Natural Dutch rewrite |

Modes combine: "write a Dutch blog post" = blog + dutch. "Slack bericht in het Nederlands" = message + dutch.

Each mode has a quick and guided path. Default to quick — rewrite immediately when you have enough context.

**Guided** triggers: input is very rough/ambiguous, user explicitly asks for help, or critical info is missing. Ask at most 2 questions.

</mode_routing>

<blog_mode>

### Workflow

```
1. BRIEF    → Gather topic, audience, voice, constraints
2. RESEARCH → Verify claims, gather examples and data
3. OUTLINE  → Structure by reader value, get approval
4. DRAFT    → Write with anti-slop enforcement
5. REVIEW   → Quality checklist
6. DELIVER  → Markdown with frontmatter
```

### Step 1: Brief

Gather before writing:
- **Topic**: What specifically are we writing about?
- **Type**: Technical post, opinion piece, tutorial, case study, or update? (see `references/blog-types.md`)
- **Audience**: Who reads this? What do they already know?
- **Thesis**: One sentence — what's the point?
- **Voice sample**: Link to an existing post by the author (triggers Voice Calibration)
- **Target length**: Default 800–1200 words unless specified

### Step 2: Research

Before writing a single word:
- Verify every factual claim. If you can't verify it, flag it.
- Gather concrete examples: code snippets, data points, real tool names
- Find counterarguments to the thesis — address them or adjust
- No claim without evidence. No example without specifics.

### Step 3: Outline

1. **Lead with the point.** The reader should know the thesis within the first two paragraphs.
2. **Order by reader value.** Most useful content first. Background later (or never).
3. **Each section earns its place.** If removing a section doesn't hurt the post, remove it.

Use the structural template from `references/blog-types.md` for the chosen type.

Present the outline for approval before drafting:

```
## Outline: [Title]

**Thesis:** [one sentence]
**Type:** [post type]
**Est. length:** [word count]

1. [Section] — [what it covers and why]
2. [Section] — [what it covers and why]
3. ...
```

### Step 4: Draft

Apply Writing Rules and Anti-Slop Rules (see below).

**Paragraph flow:**
- First sentence of each paragraph: states the point
- Remaining sentences: support with evidence or example
- Last paragraph of each section: bridges to the next or delivers a conclusion

### Step 5: Review

Check the draft:

**Content:** Thesis clear in first two paragraphs · Every claim supported · No unsupported superlatives · Counterarguments addressed

**Voice:** Zero banned words/phrases · Reads like a human · Matches author voice (if sample provided)

**Structure:** Every section earns its place · Paragraphs 1–4 sentences · Code examples complete and runnable

**Anti-Clickbait:** Title is honest · No "You Won't Believe" patterns · Title matches content

### Step 6: Deliver

Output as markdown with frontmatter:

```markdown
---
title: "Exact Post Title"
description: "One-sentence summary for SEO/social"
tags: [tag1, tag2, tag3]
date: YYYY-MM-DD
draft: true
---

[Post body in markdown]
```

Always set `draft: true`.

### Vault Integration

When writing a blog post for a project, check for a promotion vault folder:

**Path:** `_management/promotion-vault/projects/{project-name}/`

If it exists:
- Read `index.md` frontmatter for project context
- Write blog post body to `blog-post.md` in the vault folder
- Add an `article` entry to `posts.yaml`

If not, suggest: `bun run _management/promotion-vault/scripts/promote.ts {project} init`

</blog_mode>

<message_mode>

### Quick Mode

1. Detect target platform
2. Read `references/voice-samples.md` for voice profile
3. Apply platform rules (see `references/platform-{name}.md`)
4. Check against `references/banned-words.md`
5. Run the draft through the post-write filter (see Post-Write Filter below)
6. Output in code block, ready to copy

### Guided Mode

Gather what's missing (max 2 questions):
- **To whom?** — Recipient/audience
- **About what?** — Core point in one sentence
- **Desired outcome?** — What should the reader do/feel/know?
- **Platform** — Slack, Email, WhatsApp, Telegram, or Reddit/forum

### Platform Rules

| Platform | Register | Key trait | Reference |
|----------|----------|-----------|-----------|
| Slack | Professional-casual | Point on line 1, thread-aware | `references/platform-slack.md` |
| Email | Formal spectrum | Subject line matters, paragraph discipline | `references/platform-email.md` |
| WhatsApp | Very casual | Speech-like bursts, can split messages | `references/platform-whatsapp.md` |
| Telegram | Medium-casual | Rich formatting ok, longer messages fine | `references/platform-telegram.md` |
| Discord | Casual-informative | Community-aware, server context matters, no corporate polish | `references/platform-discord.md` |
| Reddit/forum | Casual-informative | Disclose ownership, no sales pitch, lead with the solution | `references/platform-reddit.md` |

### Length Discipline

- Slack: 1-4 lines for updates, up to a short paragraph for context
- Email: as short as possible while being complete
- WhatsApp: 1-3 short bursts, never a wall of text
- Telegram: can be longer but stay focused
- Discord: short and conversational; a few lines, split into messages if it runs long
- Reddit/forum: enough to be genuinely useful, never a wall of text or a pitch

### Tone Modifiers

| Modifier | Effect |
|----------|--------|
| softer | Add courtesy, soften directives, more "would you mind" |
| firmer | Remove hedging, stronger language, clear expectations |
| urgent | Front-load the ask, add time pressure, trim context |
| formal | Full sentences, proper structure, no contractions |
| casual | Contractions, shorter sentences, conversational |

### Post-Write Filter (mandatory)

Every email/message draft goes through the clean script before output. Always run it — even on drafts you wrote yourself, since em-dashes sneak in:

```bash
echo "$DRAFT" | python3 ~/.claude/skills/writer/scripts/clean.py
```

Use the cleaned stdout as the output. What it removes:
- Em-dashes: ` —` → `,` and bare `—` → `, ` (matches the user's raycast clean-watermark exactly)
- Zero-width chars, NBSP, all U+2000–U+200A spaces, line/paragraph separators, BiDi controls
- Non-printable control bytes
- RTF residue (`\rtf1`, `\fonttbl`, `\par`, etc.) and HTML font/style/class/span/div/p/meta tags with inline `font-family:`, `color:`, `background:` declarations
- GUIDs (8-4-4-4-12 hex)
- Trailing whitespace, runs of 3+ blank lines, double spaces
- NFKC-normalizes the whole thing first

What it does NOT remove (use the writing pass, not the filter): slop phrases, slop words, bad rhythm. The filter strips mechanical tells; the writing pass strips lexical tells. Both required.

After output, mention what the filter removed if it removed anything. The script prints a one-line summary to **stderr** in the form `clean.py: <total> chars, <n> spaced em-dash, <n> bare em-dash, <n> zero-width, <n> control, …` (only the categories that fired appear; when a run strips just whitespace it may read `clean.py: 1 chars`). Relay that summary. If nothing was removed it prints `clean.py: nothing removed` — in that case say nothing.

### Difficult Messages

For rejections, bad news, complaints, escalations — apply the Difficult Messages rules in rewrite mode (lead with the decision, one sentence of context, one "sorry" max, concrete next step).

### Input Handling

**Rough notes / bullet points:** Construct a coherent message. Fill gaps with reasonable assumptions.

**Existing text:** Reshape to match target platform. Preserve core message.

**Platform conversion:** Restructure for how people read on that platform — don't just shorten.

### Output Format

Present in a code block, ready to copy. For email, include subject line above:

**Subject:** [subject line]
~~~
[Email body here]
~~~

For WhatsApp, show splits when natural:

~~~
Message 1:
[first part]

Message 2:
[second part]
~~~

No commentary after output unless asked.

### Message Self-Check

Before outputting, verify:
- Ran the draft through `~/.claude/skills/writer/scripts/clean.py` (no em-dashes survived — spot-check)
- Zero banned words/phrases from `references/banned-words.md`
- Length matches platform norms
- Tone matches the relationship (don't write "Hi Sarah," to someone the user calls "S")
- The ask or point is on line 1, not buried
- No AI rhythm (see Sentence Variety in Shared Rules)

</message_mode>

<rewrite_mode>

For text that isn't a blog post, platform message, or Dutch translation. The user just wants cleaner English.

1. Read the input and identify what's wrong (slop, filler, weak structure, passive voice, hedging)
2. Check `references/voice-samples.md` for voice profile
3. Rewrite applying Writing Rules + Anti-Slop Rules
4. Preserve the author's meaning and intent exactly
5. Output in code block, ready to copy

**Rules:**
- Don't change the format (if it's a list, keep it a list)
- Don't add content. Only remove or rephrase.
- Don't make it longer. Default direction is shorter.
- If you removed more than ~30% of the words, note what you cut and why (one line)

### Codebase-Wide Sweep

When the task is stripping a banned pattern (em-dashes, semicolons, a slop phrase) across many files rather than rewriting one text:

1. **Grep** for the pattern to map every hit and which files it touches.
2. **Categorise** hits: rendered/user-facing copy (rewrite these) vs. code, comments, or data the pattern is legitimate in (leave these — an em-dash in a regex or a URL is not slop).
3. **Replace in batch** — a script or scoped edits, not file-by-file freehand. Substitute the pattern's intent, don't just delete (an em-dash usually becomes a period, comma, or "to").
4. **Run the project's checks** (build, typecheck, lint) to confirm nothing broke.
5. **Commit** the sweep as one atomic change.

### Difficult Messages

When the content involves bad news, rejections, complaints, or sensitive topics:
- Lead with the decision, not the reasoning. Don't bury the "no."
- Be direct but not cold. One sentence of context is enough.
- Don't over-apologise. One "sorry" max.
- Don't soften so much that the message becomes ambiguous.
- End with a clear next step, not a vague "let me know."

</rewrite_mode>

<dutch_mode>

### Quick Mode

1. Detect source language (English or Dutch)
2. Detect or ask register (see Register System)
3. Check `references/voice-samples.md` for Dutch voice profile
4. Rewrite applying Dutch Writing Rules + Anti-Slop
5. Check against `references/banned-dutch.md`
6. Output in code block, ready to copy

### Guided Mode

Gather what's missing (max 2 questions):
- **Who reads this?** — Friend, colleague, client, public audience
- **What's the point?** — Core message in one sentence
- **Register** — Casual, friendly, or professional

### Register System

| Register | When | Characteristics |
|----------|------|-----------------|
| casual | Friends, social media | Contractions (da's, 't, 'n), short sentences, spoken rhythm, "je/jij" |
| friendly | Team messages, community posts | Warm but clear, "je" default, light humour ok |
| professional | Client emails, formal docs | "U" when appropriate, full sentences, precise but not bureaucratic |

Default to **friendly** when register is unclear. Register affects word choice, not honesty.

### Dutch Writing Rules

1. **Zeg wat je bedoelt.** No hedging, no filler, no weasel words.
2. **Kort als het kan.** Fewer words when possible.
3. **Schrijf zoals je praat.** If it sounds like a government letter, rewrite.
4. **Concreet boven vaag.** Specifics over generalisations.
5. **Geen vals enthousiasme.** Don't inject excitement the original doesn't have.

**Natural Dutch patterns:**
- Contractions where spoken Dutch would: "dat is" → "da's", "het" → "'t" (casual/friendly only)
- Use particles: "even", "gewoon", "toch", "wel", "maar"
- Correct Dutch word order — not English word order
- Use "er" constructions naturally
- Prefer Dutch words over anglicisms (see `references/banned-dutch.md`)

### Anglicism Quick Reference

| Don't write | Write instead |
|-------------|---------------|
| checken | controleren, nakijken |
| basically | eigenlijk, in feite |
| issue | probleem, kwestie |
| cancellen | annuleren, afzeggen |
| managen | beheren, regelen |
| updaten | bijwerken |

Exception: tech terms without a natural Dutch equivalent stay English (API, frontend, deployment, commit).

### Output Format

~~~
[Rewritten Dutch text]
~~~

If input was long (>3 paragraphs), show the register used:

**Register:** friendly
~~~
[Rewritten Dutch text]
~~~

### Before/After

**English input:**
> I wanted to reach out to let you know that we've been making great progress on the project and I'm excited to share that we'll be launching next week.

**Dutch output (friendly):**
> We liggen goed op schema. Volgende week gaan we live.

</dutch_mode>

<shared_rules>

### Writing Rules (All Modes)

1. **Lead with the point.** Don't build up to it.
2. **One idea per paragraph.** Two ideas = two paragraphs.
3. **Show, don't tell.** Code > description. Example > explanation.
4. **Short paragraphs.** 1–4 sentences.
5. **Active voice.** "We removed the cache" not "The cache was removed."
6. **Specific > vague.** "800ms to 120ms" not "significantly improved."
7. **Cut filler.** Every word earns its place.

### Dutch Directness (All Modes)

1. Say what you mean. No hedging.
2. Respect the reader's time. Fewer words when possible.
3. Substance over style. Plain with insight beats polished with nothing.
4. Opinions are fine. State clearly, support, acknowledge the other side.
5. No false modesty. Don't undersell good work. Don't oversell mediocre work.

### Sentence Variety (All Modes)

AI text has a rhythmic tell: it alternates short-long-short-long like a metronome. Human writing is irregular.

**Rules:**
- Vary sentence length unpredictably. Three short in a row is fine. Two long ones back-to-back is fine. A pattern is not.
- Don't start consecutive sentences the same way. If two paragraphs both open with "The...", rewrite one.
- Mix sentence types: statements, fragments, questions (real ones, not rhetorical). Not every sentence needs a subject-verb-object.
- Read it aloud. If it sounds like a speech, it's too smooth. Real writing has edges.

### Anti-Slop Rules (All Modes)

Check every sentence against `references/banned-words.md` (English) or `references/banned-dutch.md` (Dutch).

The banned-words reference is the source of truth. Below are the categories — see the reference file for full lists.

**AI giveaway punctuation:** em-dashes, semicolons in casual text, dramatic ellipsis.

**AI giveaway structures:** mirrored contrasts, parallel pairs, triple-adjective lists, "Not only X but also Y", "Whether it's X or Y", balanced spectrum lists ("from X to Y").

**AI giveaway transitions:** "This is where X comes in", "At its core,", "In essence,", "Simply put,", "Here's the thing:", rhetorical questions used as transitions ("So what does this mean?", "But why does this matter?").

**AI giveaway tone:** added enthusiasm, "Great question!" energy, summarising back, overly smooth transitions, the recap paragraph that restates what was already said.

**AI giveaway rhythm:** predictable short-long alternation, every paragraph opening the same way, exactly 3 or 5 bullet points.

### Voice Calibration

When the user provides a writing sample or `references/voice-samples.md` has content:

1. **Extract:** sentence length, paragraph patterns, greeting/sign-off habits, formality level, emoji use, humour style, contractions, how they open
2. **Summarize** as 3–4 bullet voice profile before drafting
3. **Match** throughout. When unsure, lean shorter and more direct.

No samples? Default to direct and natural.

</shared_rules>
