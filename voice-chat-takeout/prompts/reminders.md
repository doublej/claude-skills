# Brief template — REMINDERS (shape: decision walk)

> This is the **decision-walk** template: the conversation is converging
> on a handful of decisions. If instead the user wants to go over *many
> items* — a fact-check across files, a list of tickets, a batch of
> findings — that is a **reference review**; use
> `prompts/reference_review.md`, which carries the whole corpus, has no
> 500-word cap, and folds in this file's writeback block. Picking the
> wrong shape, not the wrong length, is the usual failure.

> Vocabulary is the bridge's. Canonical, live source: run **`rbridge
> prime`** (its Vocabulary section). Three roles: **user** (the human),
> **project agent** (you, the Claude Code session composing this brief),
> **voice agent** (the agent on the phone that reads the brief). The primer
> wins over anything restated here.

## Audience

The brief is a **handoff from you (the project agent) to the voice
agent**. The voice agent will read it and then talk *with* the user.
You are not addressing the user — you are briefing a peer who is about
to meet the user. The user is a third party in this document.

- Refer to the voice agent as "you" (it is the reader).
- Refer to the user as "the user" or "they". Never "you".
- Refer to yourself (the project agent) as "I".

The voice agent may paraphrase, rephrase, or restructure the brief when
speaking aloud — so prioritize substance over recitable cadence.

## What the brief must do

Carry enough detail that the voice agent can ask sharp follow-ups and
the user can make real decisions while walking. Generic "where we are /
what to think about" prose fails — it sounds like a summary of the
agenda instead of the agenda itself.

## What "good" looks like

A good brief reads like an experienced colleague briefing a peer in two
minutes before a meeting. It names specifics. It states the actual
tradeoff with both sides. It does not pad.

A weak brief looks like this (do NOT do this):

> We're working on the wallgen catalog restructure with the user. There
> are some open questions about how products map. Walk through them.

The voice agent gets no information from that. It can only ask "tell me
more". You burnt its attention.

A strong brief reads like this:

> The user and I locked the wallgen catalog plan in three phases. Phase
> two introduces a resolver function plus a generated catalog file in
> git, with a tiny per-design source of truth — design and eligibility
> files only, no asset moves yet. The first hard call is bosdieren and
> bosdieren collage. The user and I have already decided they collapse
> into one canonical design with three compositions, but Shopify URLs
> still use the legacy slug bosdieren-collage. Migrating means new
> handles and a redirect cliff. Keeping the legacy slug means the
> resolver carries a channel-aware translation layer forever — every
> code path for Shopify has to remember to translate.
>
> Push the user on this: what's the right call, and how much do clean
> public URLs actually matter to them?

That gives the voice agent enough to push back, suggest a third option,
ask specific follow-ups.

## Tone

- Plain words. No markdown formatting — no `**`, no `#`, no bullets.
- Use specific names from the conversation: file names spelled aloud
  ("the resolver dot ts file"), slug names ("bosdieren collage"),
  numbers, percentages. The voice agent needs proper nouns to ground
  the conversation.
- One open question per paragraph. The question the voice agent should
  put to the user is the last sentence of its paragraph.
- POV: address the voice agent as "you"; the user is "the user" / "they";
  self-refer as "I".

## Structure (one paragraph each, in this order; all required unless noted)

Every brief opens with the **Location header** before paragraph 1: my
`cwd` path and a two-level-deep tree, inside a fenced block (see SKILL.md
step 2, "Project orientation"). It is reference scaffolding, not speech —
the no-markdown and spell-out-filenames hard rules below do **not** apply
to it. Then the spoken paragraphs:

1. **State + plan**: where the user and I landed — what's locked, what's
   loose. Longest paragraph (80 – 150 words). The actual technical
   shape, not its category.
2. **Open question 1**: full context for the tradeoff (both sides named),
   then the question the voice agent should put to the user.
3. **Open question 2**: same shape.
4. **Open question 3** (optional, only if it's a real third question —
   do not invent one).
5. **Writeback contract** (verbatim block, see below).
6. **Closing**: one short sentence the voice agent can use to release
   pressure. "No rush — take the walk."

## Hard rules

- **No filenames in shell-command form**. Spell them out: "the resolver
  module" not `resolver.ts`. (Exception: the Location header's `cwd` path
  and tree are raw, fenced reference scaffolding, not spoken prose.)
- **Each open question must name the alternatives** the user is choosing
  between. "Should the user ship now or wait?" is too thin. "Ship now
  and treat staging flakiness as a separate investigation, or block on
  a clean staging run — which is roughly an extra half day" is the bar.
- **No invented detail and no bluffing.** Every proper noun in the
  brief (file name, function name, slug, error string, number, person,
  decision) must trace back to either the conversation transcript or a
  tool call you ran in this session. If you cannot point at where a
  detail came from, do not write it. If the structure demands a detail
  you don't have, **go look it up** (SKILL.md step 1 — Read the file,
  grep the symbol, run `git log`) rather than reach for plausible
  prose. The voice agent will repeat anything you assert with
  confidence; bluffs become bad advice the user has to fact-check
  on a walk.
- **Name the gaps, don't paper over them.** If the user referenced
  something you have no access to (Linear ticket, Slack thread, design
  doc, calendar event), say so explicitly in the brief — one short
  sentence — so the voice agent can ask the user instead of inventing.
- **Length budget**: 250 – 500 words for the brief body, plus the
  writeback block. If you're under 250, you've left out substance —
  go back to context-gathering (SKILL.md step 1) and add specifics.
  Be denser, not longer.
- **Personalize the writeback examples**. Replace the placeholders with
  phrases that actually fit the current topic.

## Writeback contract block

Append this block, with `<slug>` filled in **and** the example prefix
lines rewritten to match the actual conversation topic. Keep the shape
verbatim — only the example phrases change.

```
Decisions and follow-ups that should reach the project agent land in a
Reminders list named "Voice colon <slug>". Each item that should reach
the project agent is one reminder in that list. Title shapes:

  "Decision colon <something concrete from this brief>" — for committed
   calls.
  "Note colon <observation that fits this topic>" — for context worth
   keeping.
  "Question colon <a likely follow-up>" — when the user wants the project
   agent to come back with an answer.
  "Deferred colon <thing you talked about but punted on>" — when the user
   explicitly does not decide on the call and wants to revisit later.
  "Done" — closes the exchange so the project agent can wrap up.

Plain titles without a prefix work too. A single "Done" reminder closes
the list automatically on the next bridge cycle.

If the user does not commit on an open question during the call, do not
fabricate a decision — log it as "deferred colon …" instead and move on.
```

Example, customized for a wallgen-catalog conversation:

```
Decisions and follow-ups land in a Reminders list named "Voice colon
wallgen catalog restructure". Each item that should reach the project
agent is one reminder in that list. Title shapes:

  "Decision colon migrate the Shopify handles" — for committed calls.
  "Note colon the resolver should never know about Shopify" — for
   context worth keeping.
  "Question colon what does the redirect path look like for the legacy
   URLs" — when the user wants the project agent to come back with an
   answer.
  "Deferred colon the bosdieren slug rename" — when the user talked it
   through but wants to sleep on it.
  "Done" — closes the exchange.

Plain titles without a prefix work too.
```
