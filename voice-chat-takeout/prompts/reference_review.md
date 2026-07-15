# Brief template — REFERENCE REVIEW (shape: review)

> Vocabulary is shared with `reminders-bridge`. Canonical table:
> `~/Documents/development/python/reminders-bridge/README.md` → "Voice
> exchange mailboxes" → "Vocabulary". Three roles: **user** (the human),
> **project agent** (you, the Claude Code session composing this brief),
> **voice agent** (the agent on the phone that reads the brief).

Use this template when the conversation is a **corpus review**, not a
decision walk: the user wants to go over many items — a set of files, a
list of tickets, a batch of findings, a fact-check across a directory —
and discuss, verify, or decide on them one at a time. The unit is the
*item*, and there are many. Examples: "go over all 28 CLAUDE.md files and
check the facts", "walk me through every open bug", "review the catalog
entries".

If the conversation is converging on a *handful of decisions*, use the
decision-walk templates (`claude_voice.md` / `reminders.md`) instead.

## The detachment rule (why this template exists)

The voice agent is detached from this system: no files, no shell, no
tools, no way to open the things you are reviewing. It cannot read the 28
files. It only has this brief. So a corpus review cannot be a summary
that *points at* the corpus ("there are some outdated files, walk through
them") — it must **carry the corpus**. The facts the user will probe have
to be physically in the brief, because the voice agent has no other way
to get them. That is why this template has no global length cap: it is
long on purpose, and scales with the number of items.

## Audience and POV (same as the other templates)

A handoff from you (the project agent) to the voice agent.
- Voice agent = "you" (the reader).
- User = "the user" / "they". Never "you".
- Yourself = "I".

## Gather the corpus first — this is most of the work

For a reference review, context-gathering (SKILL.md step 1) is not a
quick pre-flight — it *is* the job. You must actually read every item the
user might raise, because the voice agent can't. Do not compose from
memory of the conversation; the user will name a specific file and ask
"what does it actually say", and a paraphrase collapses.

**Parallelize it.** Fan out subagents — one per item or one per cluster —
to read the files / pull the tickets and return per-item facts (what it
says, what's questionable, the exact claim to verify). Assemble their
findings into the brief. A 28-file audit is 28 reads; do them concurrently,
not in a serial slog, and not by guessing.

## Structure

Light structure is allowed here (an index, per-item headers) — unlike the
decision walk, the voice agent does **not** read this start to finish. It
navigates: the user raises an item, the voice agent jumps to that block.
Keep the *body* of each item speakable plain prose; keep the scaffolding
(index, headers) scannable. No shell-form filenames in the spoken bodies —
spell them out. (The Location header below and the map are scaffolding —
raw paths are fine there.)

0. **Location header** — at the very top, before Orientation: my `cwd`
   path and a two-level-deep tree, inside a fenced block (see SKILL.md
   step 2, "Project orientation"). Reference scaffolding the voice agent
   uses to place any file the user names; it is not read aloud, so the
   spell-out-filenames rule does not apply to it.

1. **Orientation** — one short paragraph. What the corpus is, why the user
   and I are reviewing it, and what outcome the user wants from the call
   (decide which to fix? confirm facts? prioritize?). This frames the
   whole walk.

2. **The map** — a scannable index of every item, grouped logically, each
   with a one-line "what it is". This is the table of contents the voice
   agent uses to find its place when the user says "let's do the wallgen
   one". Include items with nothing wrong (one line each) so the count
   matches the user's mental model — "28 files" should resolve to 28
   entries.

3. **Per-item detail** — one block per item that has something to discuss.
   Each block carries, in plain speakable prose:
   - what the item currently says (the actual content — quote or tight
     summary, not "it has some config"),
   - what's questionable (the specific fact to verify, the conflict with
     another item, the staleness, the bug), and
   - the candidate change, if there is one.
   This is where the substance lives. An item the voice agent can't
   discuss without "tell me more" is a failed block.

4. **Cross-cutting themes** — one paragraph. Patterns across items the
   user should see as a group ("six files reference a CLI called cdy that
   may have been renamed to caddyctl — same question repeats").

5. **What to push on** — the decisions the user needs to make, batched or
   per-item. For a fact-check this is often "for each questionable item,
   confirm or correct".

6. **Writeback contract** (REMINDERS kind only — see reminders.md for the
   block; one reminder per item decision).

7. **Closing** — one short sentence to release pressure.

## Length

No global cap. The floor is coverage: every item the user is likely to
raise must have enough in its block that the voice agent can discuss it
without the file in front of it. Budget per item, not per brief. Be
dense, never padded — a long brief full of "it has some settings" is
worse than a shorter one with real facts. Cut items the user clearly does
not care about down to a single index line.

## What "good" looks like

Weak (do NOT do this — this is the decision-template forced onto a corpus,
the exact failure this template fixes):

> The user and I are reviewing the CLAUDE.md files across the monorepo.
> A few seem outdated and some conflict. The main questions are whether
> to consolidate them and how to handle the conflicts. Walk through it.

The voice agent cannot name a single file, say what any of them contains,
or tell the user which fact is wrong. The user asks "okay, which one
first?" and the voice agent has nothing — it has to ask the user to
recite the corpus it was supposed to be briefed on.

Strong (orientation + map + two real item blocks + a theme):

> The user and I are auditing the 28 CLAUDE.md files across the
> development monorepo for stale or conflicting instructions. The user
> wants to walk the questionable ones and decide, per file, whether to
> fix now, defer, or leave it.
>
> Here is the map. Root level: the dev-root file and the global rules
> file. Web: 11 files, mostly per-app. Python: 9 files. Multi-stack: 5,
> including pimpelmees and remotevr. Audio, go, swift: one each. Of the
> 28, six have something I flagged; the rest looked current and are just
> listed so the count lines up.
>
> First flagged one, the dev-root file. It lists the node folder as "TS
> CLI tools" and names caddyctl with the alias cdy. But the caddyctl
> project's own file calls the binary cdy as well, so that part agrees —
> the stale bit is that dev-root still lists poolsuite-cli under node,
> which moved to the web folder three weeks ago per git. So the question
> is just: drop the poolsuite-cli line from node.
>
> Second, the pimpelmees file. It pins wallgen at port 6500 and the webui
> at 6512, but the wallgen compose file now binds 6501 — the file is one
> port off. That's a real conflict an agent would trip on. Straightforward
> fix, but I want the user to confirm 6501 is the intended new port and
> not a temporary override before I write it.
>
> The recurring theme across four of the six is port and path drift —
> files that were right when written and fell behind a move. None are
> dangerous, all are the kind of thing that sends an agent to the wrong
> place. Push the user to batch-approve the obvious drift fixes and only
> slow down on the two where intent is unclear.

That gives the voice agent a real conversation: it can open with the
count, take the user to any file by name, state what it says and what's
wrong, and know which two need the user's judgment versus which are
rubber-stamps.

## Hard rules

- **Carry, don't point.** Every item the user might raise has its facts in
  the brief. "See the file" is not an option — the voice agent can't.
- **No invented detail and no bluffing.** Every claim about an item traces
  back to a file you (or a subagent) actually read or a tool call you ran.
  If you didn't read it, say so in that item's block ("I didn't get to the
  swift file — flag it for the user") rather than guessing its contents.
- **Name the gaps.** Items behind tools you can't reach (a Linear ticket,
  a private doc) get one honest sentence saying the voice agent should ask
  the user, not a fabricated summary.
- **Match the count.** If the user thinks "28 files", the map has 28
  entries. A silently truncated corpus reads as "covered everything" when
  it wasn't.
