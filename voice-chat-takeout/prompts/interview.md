# Brief template — INTERVIEW / INBOUND (shape: interview)

> Vocabulary is the bridge's. Canonical, live source: run **`rbridge
> prime`** (its Vocabulary section). Three roles: **user** (the human),
> **project agent** (you, the Claude Code session composing this brief),
> **voice agent** (the agent on the phone that reads the brief and talks to
> the user). The primer wins over anything restated here.

Use this template when there is **no prior conversation**: the user invoked
the skill *for a subject* (`/voice-chat-takeout for <subject>`) and wants
the voice agent to **interview them** and bring structured answers back.
The brief is a **numbered question script**, not a recap. Always
`--kind=REMINDERS` — an interview is worthless without the answers.

If instead you are packaging a conversation that already happened, use the
decision-walk (`claude_voice.md` / `reminders.md`) or reference-review
(`reference_review.md`) templates.

## The detachment rule (still applies)

The voice agent is detached: no files, no shell, no memory of your
research. It knows only what this brief carries. So the brief must hand it
enough **KNOWN** context to ask intelligent follow-ups — an interviewer who
knows nothing can't probe an answer. But it must not pretend to know the
**GAPS** — those are exactly what the questions exist to fill.

## Research first — build the context you don't have

There is no conversation to back up, so context-gathering (SKILL.md step 1)
is *active research*, and it is the bulk of the work. Fan out cheap
subagents to gather (`Read` the relevant files, `git log`, `grep`, `bd
list`); have one stronger agent synthesize into two piles:

- **KNOWN** — facts you established. These go into the brief so the voice
  agent can follow up ("you said Postgres — the schema already has a
  `jsonb` column, does that change the answer?"). Never ask the user
  something you could look up.
- **GAPS** — what only the user can answer: intent, priorities, taste,
  constraints in their head, decisions not yet made. These *become* the
  numbered questions. Never assume a gap; ask it.

The KNOWN/GAP split *is* the interview design. A good interview asks only
GAPS and arms every question with the relevant KNOWN.

## Audience and POV

A handoff from you (the project agent) to the voice agent.
- Voice agent = "you" (the reader / the interviewer).
- User = "the user" / "they". Never "you".
- Yourself = "I".

## Structure

0. **Location header** — my `cwd` path and a two-level-deep tree in a fenced
   block (see SKILL.md step 2, "Project orientation"). Prefix it with one
   line telling the voice agent it's a silent map, not to be read aloud.
   Reference scaffolding — the spell-out-filenames rule doesn't apply to it.

1. **Framing** — one short paragraph: "You are interviewing the user about
   `<subject>`. Ask the questions below one at a time, let them answer in
   their own words, follow up where useful, and make sure each numbered
   question gets an answer recorded." State the goal of the interview (what
   the user is trying to produce or decide by the end).

2. **What I already know (KNOWN)** — a tight briefing of the established
   facts, in plain speakable prose, so the voice agent can probe answers
   instead of taking them flat. This is the interviewer's homework.

3. **The questions** — a **numbered** list. Each question:
   - is a real GAP (only the user can answer it),
   - carries its relevant KNOWN inline so the voice agent can push,
   - **names its response kind and expected shape**, so the answer drains
     cleanly. Bind each to the existing writeback grammar — **no new
     prefixes** (`mailbox read` only parses
     decision/note/question/deferred/done/free). Example bindings:
     - a call between options → `answer as "Decision: Q3 <redis|sqlite|memory>"`
     - an open-ended fact/opinion → `answer as "Note: Q5 <their answer>"`
     - something they want *you* to chase down → `Question:`
     - something they explicitly punt on → `Deferred:`
   Keep the question itself speakable (no raw identifiers); the `Qn` tag and
   option tokens live in the written answer shape, which the user dictates —
   so keep those tokens short and phonetically clean (`redis`, not a slug).

4. **Writeback contract** — the standard REMINDERS block (see
   `reminders.md`), with one addition: tell the user to **prefix each answer
   with its question number** (`Q3`) so you can map answers back on drain.
   A single "Done" reminder closes the exchange.

5. **Closing** — one short sentence releasing pressure ("No rush — answer
   what you can, skip what you can't, say done when you're finished.").

## Draining (what you do after)

`rbridge mailbox read --slug <slug>` returns the responses. **Map each back
onto its `Qn`.** On a partial return, either proceed on the answered
questions — labeling the assumptions you're forced to make for the rest —
or re-brief just the unanswered gaps as a shorter follow-up script. Never
silently drop a question.

## What "good" looks like

Weak (do NOT do this — a naked question list with no homework, no bindings):

> Interview the user about the caching layer. Ask: What cache should we
> use? How long should things live? Should it be shared? Walk through it.

The voice agent can't push on anything (it knows nothing about the code),
and the answers come back as free text you can't map or drain cleanly.

Strong (framing + KNOWN + bound questions):

> You are interviewing the user about the caching-layer rewrite. Ask these
> one at a time, follow up, and make sure each numbered question gets an
> answer recorded. The goal: by the end I should know enough to write the
> cache module without guessing.
>
> What I already know: the current code caches nothing — every request
> re-reads from the database module and re-renders. The hot path is the
> catalog resolver, called on every product page; I measured it at roughly
> forty milliseconds a call. The app already runs a database the user
> controls, and there is no shared cache service today.
>
> Question one. Where should the cache live — in the app's own memory
> (fast, but lost on restart and not shared across workers), a small
> on-disk store next to the app, or a shared service the user would have to
> run? I know they run a single worker today, which makes in-memory
> tempting, but they mentioned wanting to scale out. Answer as "Decision:
> Q1 memory, sqlite, or shared".
>
> Question two. How stale is acceptable for a catalog entry — seconds,
> minutes, or until the next deploy? The catalog changes when they publish
> a product, which they said is a few times a week. Answer as "Decision: Q2
> seconds, minutes, or deploy".
>
> Question three. Is there anything about the deploy setup I should know
> before I pick — containers, multiple regions, anything that would rule an
> option out? Answer as "Note: Q3 whatever they tell you".

That gives the voice agent a real interview: it knows the code, can push
each answer against what it knows, and every answer comes back tagged and
drainable.

## Hard rules

- **Write for the ear.** The framing, KNOWN briefing, and questions are all
  spoken and heard — short sentences, one idea each, jargon dialed down a
  notch. A question a listener can't hold in one breath is too long; split
  it. Put one plain line in the framing steering the voice agent to *speak*
  plainly too: "Ask these like a sharp colleague talking, not reading a
  spec — plain everyday words, and unpack any technical term the moment you
  use it." See `rbridge prime` → *Brief templates*.
- **Ask GAPS, arm with KNOWN.** Never ask what you could look up; never
  assume what only the user knows. Every question carries its relevant
  known facts.
- **No new response prefixes.** Bind answers to
  decision/note/question/deferred/done/free only — anything else won't
  drain.
- **Number every question and require the `Qn` prefix on answers**, so a
  partial or out-of-order return still maps.
- **No invented detail.** Every KNOWN fact traces to a file you (or a
  subagent) read or a tool call you ran. If you couldn't establish
  something, it's a GAP — ask it, don't assert it.
- **Keep answer tokens phonetically clean.** The user dictates them, and
  speech-to-text destroys slugs, underscores, and paths — offer short plain
  words as the option set (`redis`, `sqlite`, `memory`), never identifiers.
