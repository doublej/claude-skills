# Brief template — CLAUDE_VOICE (shape: decision walk)

> This is the **decision-walk** template: the conversation is converging
> on a handful of decisions. If instead the user wants to go over *many
> items* — a fact-check across files, a list of tickets, a batch of
> findings — that is a **reference review**; use
> `prompts/reference_review.md`, which carries the whole corpus and has no
> 500-word cap. Picking the wrong shape, not the wrong length, is the
> usual failure.

> Vocabulary is shared with `reminders-bridge`. Canonical table:
> `~/Documents/development/python/reminders-bridge/README.md` → "Voice
> exchange mailboxes" → "Vocabulary". Three roles: **user** (the human),
> **project agent** (you, the Claude Code session composing this brief),
> **voice agent** (the agent on the phone that reads the brief).

## Audience

The brief is a **handoff from you (the project agent) to the voice
agent**. The voice agent will read it and then talk *with* the user.
You are not addressing the user — you are briefing a peer who is about
to meet the user. The user is a third party in this document.

- Refer to the voice agent as "you" (it is the reader).
- Refer to the user as "the user" or "they". Never "you".
- Refer to yourself (the project agent) as "I".

The voice agent may paraphrase, rephrase, or restructure the brief when
speaking aloud — so prioritize substance over recitable cadence. Dense
context beats smooth prose.

## What the brief must do

Carry enough specific detail that the voice agent can ask sharp
follow-ups and the user can make real decisions while walking. Generic
"where we are, what to think about" prose fails. The user already knows
the topic; the voice agent needs the *substance* of it to push on.

## What "good" looks like

A good brief reads like an experienced colleague catching a peer up
before a meeting. Specifics. Tradeoffs with both sides named. No padding.

Weak (do NOT do this):

> We've been working through the wallgen catalog restructure. There are
> some open questions about how to map products. Walk through them with
> the user.

That tells the voice agent nothing concrete. Every follow-up will be
"tell me more about X".

Strong:

> The user and I locked the wallgen catalog plan in three phases. Phase
> two introduces a resolver function plus a generated catalog file in
> git, with
> a tiny per-design source of truth — design and eligibility files only,
> no asset moves yet. The thing chewing at the user is that bosdieren
> and bosdieren collage are collapsing into one canonical design with
> three compositions, but Shopify URLs still use the legacy slug
> bosdieren collage. Migrating means new handles and a redirect cliff.
> Keeping the legacy slug means the resolver carries a channel-aware
> translation layer forever.
>
> Push the user on this: what is their gut, and how much do clean public
> URLs actually matter here?

The voice agent now has enough to open with a sharp opener, push back,
suggest a third option, ask specific follow-ups.

## Tone

- Plain words. No markdown — no `**`, no `#`, no bullets. The voice
  agent may read passages aloud verbatim.
- Use specific names from the conversation: spelled-out file names,
  slugs, numbers. Proper nouns ground the conversation.
- POV: address the voice agent as "you"; the user is "the user" / "they";
  self-refer as "I".

## Structure (all four sections required)

Every brief opens with the **Location header** before section 1: my `cwd`
path and a two-level-deep tree, inside a fenced block (see SKILL.md step 2,
"Project orientation"). It is reference scaffolding, not speech — the
no-markdown and spell-out-filenames hard rules below do **not** apply to
it. Then the four spoken sections:

1. **State + plan**: where the user and I landed — what's locked, what's
   loose. Longest paragraph (80 – 150 words). The actual technical
   shape, not its category.
2. **What the user should chew on**: one to three paragraphs, one per
   open question. Each names the alternatives the user is weighing. The
   question the voice agent should put to the user is the last sentence
   of its paragraph.
3. **What I will do with the user's answers**: one paragraph. High level
   — no implementation details. "Whatever the user decides on the slug
   question, I'll write the migration or the translation layer once
   they're back."
4. **Closing**: a single short sentence the voice agent can use to
   release pressure. "No rush — take the walk."

## Hard rules

- No filenames in shell form. Spell them out. (Exception: the Location
  header's `cwd` path and tree are raw, fenced reference scaffolding.)
- No URLs, no command snippets, no markdown. (Same exception for the
  Location header block.)
- Each open question must name the alternatives concretely. "Should the
  user ship now?" fails; "Ship now and treat staging flakiness as a
  separate investigation, or block on a clean staging run which is
  roughly an extra half day?" passes.
- **No invented detail and no bluffing.** Every proper noun in the
  brief (file name, function name, slug, error string, number, person,
  decision) must trace back to either the conversation transcript or a
  tool call you ran in this session. If you cannot point at where a
  detail came from, do not write it. If the structure demands a detail
  you don't have, **go look it up** (SKILL.md step 1 — Read the file,
  grep the symbol, run `git log`) rather than reach for plausible
  prose.
- **Name the gaps, don't paper over them.** If the user referenced
  something you have no access to (Linear ticket, Slack thread, design
  doc, calendar event), say so explicitly in the brief — one short
  sentence — so the voice agent can ask the user instead of inventing.
- No writeback channel — CLAUDE_VOICE is one-way. Do not instruct the
  voice agent or the user to record anything. If you need writeback,
  use `--kind=REMINDERS`.
- Length: 250 – 500 words. Dense, not long. If you're under 250, you've
  almost certainly left out the substance — go back and (a) look up
  what you skipped, then (b) add it.
