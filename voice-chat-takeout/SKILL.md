---
name: voice-chat-takeout
description: Package the current conversation into a voice-ready brief for the voice agent (Claude Voice in practice), which is detached from this system and only ever sees the brief. The project agent picks the slug, kind, and shape from context — user types `/voice-chat-takeout` with no args by default. Two return-channel kinds: CLAUDE_VOICE (TTS-friendly prose, clipboard, one-way) and REMINDERS (brief lands in an Apple Reminders mailbox the project agent reads back via `rbridge mailbox read`). Two brief shapes: decision-walk (converge on a few decisions, 250–500 words) and reference-review (carry a whole corpus of files/items/findings so the voice agent can discuss them all, scales with item count). Triggers on `/voice-chat-takeout`, "voice takeout", "hand off to voice", "walk and talk this", "brief the voice agent on all these".
---

# voice-chat-takeout

You are the **project agent**. Hand the user a voice-friendly brief and
(optionally) open a return channel you can drain afterwards. Pick a
*kind* (return channel) and a *shape* (content structure) — see *Flavors*
and *Shape* below.

## The rule that governs everything: the voice agent is detached

The voice agent has no file access, no shell, no tools, no memory of this
session, and no way to pull more context once the call starts. The brief
you hand it (plus, in REMINDERS mode, the writeback list) is the **entire
universe** it can reason from. If a fact is not in the brief, it does not
exist for the voice agent.

So a brief can never *point at* the system — "see the resolver module",
"the 28 files we discussed", "check the ticket". The voice agent cannot
see, check, or open any of those. Whatever the user will want to talk
about has to be **carried into the brief** as actual content. This is the
single thing that makes a brief work or fail, and it drives both the
context-gathering (step 1) and the choice of shape.

## Vocabulary (must match the bridge)

Canonical table: `~/Documents/development/python/reminders-bridge/README.md`
→ "Voice exchange mailboxes" → "Vocabulary". Use the same terms here.

Three roles:
- **user** — the human. Third-person in the brief; never addressed directly.
- **project agent** — you, the Claude Code session composing the brief.
  Self-refer as "I". Referred to as "the project agent" from outside.
- **voice agent** — the agent on the phone that reads the brief and talks
  to the user. Addressed as "you" inside the brief. Currently Claude Voice
  in practice; do not assume a specific product in the brief.

Surface terms:
- **brief** — the handoff doc you compose. Saved to disk; in REMINDERS
  mode mirrored into the exchange list as a daemon-owned reminder.
- **slug** — `[a-z0-9][a-z0-9-]{0,47}` kebab-case label. Topic-first.
- **voice exchange** / **mailbox** — the open conversation, identified by
  slug. Backed by Reminders list + state file + brief on disk.
- **exchange list** — `Voice: <slug>` (independent of the `Beads: ` namespace).
- **header reminder** / **brief reminder** / **mirror reminder** —
  daemon-owned reminders the bridge manages.
- **response**, **response kind** (`decision` / `note` / `question` /
  `done` / `free`) — what the user adds to the exchange list.
- **writeback contract** — the trailing section of the REMINDERS brief
  that names the list + prefixes.
- **drain** — you read responses via `rbridge mailbox read`.
- **takeout** — the user-facing surface: `/voice-chat-takeout` (mailbox
  flow) or `/voice-deep-takeout` (deep paste-into-voice flow).

## Flavors

- `--kind=CLAUDE_VOICE` (default) — prose brief written for TTS. Saved to
  `~/.claude/voice-takeouts/<ts>-<slug-or-conv>.md` and copied to clipboard
  with `pbcopy`. No return channel; the user speaks freely. (Kind name is
  historical; the brief is for any voice agent.)
- `--kind=REMINDERS` — brief lands in a dedicated Apple Reminders list
  managed by reminders-bridge. The brief includes a writeback contract:
  decisions and follow-ups go into that list as reminders (one per
  item). You drain responses with `rbridge mailbox read --slug X`.

Both flavors are written for the voice agent as the reader. The REMINDERS
flavor adds explicit writeback instructions.

## Shape (orthogonal to kind)

**Kind** is the *return channel*. **Shape** is the *content structure*.
They are independent: any shape can ship as CLAUDE_VOICE or REMINDERS.
Picking the wrong shape is the failure mode this skill is most prone to —
a corpus review crammed into the decision template comes out thin no
matter how long you make it. Pick shape first, then kind.

- `--shape=decision` (default) — **decision walk**. The conversation is
  converging on a handful of decisions. The brief is a tight 250–500 word
  narrative: state + plan, then 2–3 open questions, each naming a concrete
  tradeoff. Templates: `prompts/claude_voice.md` / `prompts/reminders.md`.
- `--shape=reference` — **reference review**. The conversation is a sweep
  over *many items* — files, tickets, findings, a fact-check across a
  directory — that the user wants to go over and decide on one at a time.
  The brief carries the whole corpus: an index plus per-item facts, so the
  detached voice agent can discuss any item without opening it. No global
  length cap; it scales with item count. Template:
  `prompts/reference_review.md`.

**You pick the shape from the conversation.** The tell: is the user trying
to *decide a few things* (decision) or *go through a list* (reference)? If
the user says "walk me through all of them", "go over each", "check the
facts across these", "review every X" — that's reference. If neither fits
cleanly, lean toward carrying *more* context, structured to match how the
user will move through it — the detachment rule means under-carrying hurts
far more than over-carrying.

Reference reviews almost always want `--kind=REMINDERS`: a per-item walk
generates many small decisions, and one reminder per item is how they get
back to you.

## Invocation

```
/voice-chat-takeout                       # you pick kind + shape + slug from context
/voice-chat-takeout --kind=CLAUDE_VOICE   # force the TTS-only flavor
/voice-chat-takeout --kind=REMINDERS      # force the writeback flavor
/voice-chat-takeout --shape=decision      # force the decision-walk shape
/voice-chat-takeout --shape=reference     # force the corpus / reference-review shape
/voice-chat-takeout --mailbox=<slug>      # user-supplied slug (rare)
```

**You pick the slug.** Default behavior: read the conversation, distill
the topic into a kebab-case label, use it. The user almost never types
`--mailbox=` themselves — that flag exists only for the case where they
want a specific name (e.g. matching an existing Linear ticket).

**You also pick the kind.** Default to `REMINDERS` if the conversation has
open questions where you need the user's answers back. Default to
`CLAUDE_VOICE` if the user just wants to think out loud — no return
channel needed. Heuristic: if you would normally ask follow-up questions,
you need REMINDERS; if you are handing over context for them to chew on,
CLAUDE_VOICE is enough.

**You also pick the shape** (see *Shape* above) — decision walk by
default, reference review when the conversation is a sweep over many
items.

If the user passed an explicit `--kind=`, `--shape=`, or `--mailbox=`,
that wins over your default.

### Slug grammar

`[a-z0-9][a-z0-9-]{0,47}`. Rules you follow when generating one:

- Kebab-case, lowercase, digits OK after first char.
- Topic-first, not action-first: `wallgen-shipping-decision` not
  `decide-wallgen-shipping`.
- Skip filler verbs (`figure-out-`, `talk-about-`, `discuss-`).
- 2–5 words. Hard cap 48 chars.
- Include the date only if the same topic recurs (`q3-roadmap-walk` is
  fine; `wallgen-2026-05-16` is fine if it's a daily standup; otherwise
  omit).
- If the conversation has a project / repo name, lead with it
  (`pimpelmees-shopify-cutover`, `remotevr-quest-decode`).

Examples of slugs you generate:
- Conversation about whether to ship a wallgen change → `wallgen-shipping-decision`
- Late-night debug followup on the rbridge fixer path → `rbridge-fixer-followup`
- User asked to walk through Q3 roadmap → `q3-roadmap-walk`

Tell the user the slug you picked in your reply ("opened mailbox
`wallgen-shipping-decision`") so they can rename via `rbridge mailbox
close` + re-open if they hate it.

## What you do

1. **Gather missing context first.** The conversation is the *starting
   point* of the brief — not the source of truth. Before composing,
   run a pre-flight pass: for everything mentioned in the conversation
   but not yet *seen* in this session via a tool call, go look. Each
   gap left unfilled becomes hand-wavy prose the voice agent cannot
   push on, and the user gets a thinner walk because of it.

   This is non-optional. Treat it as part of the cost of the
   `/voice-chat-takeout` invocation. A brief composed purely from
   conversation memory will paraphrase, generalize, and inevitably
   bluff a detail the user notices on the call.

   Categories to check (skip those that don't apply — but skip
   *deliberately*, not by forgetting):

   - **Files mentioned by path** — Read them. Capture the relevant
     function signatures, config values, or sections so you can name
     specifics in the brief instead of "the resolver thing".
   - **Symbols mentioned without definition** — function names, class
     names, config keys, CLI flags, env vars: grep + read the
     definition. The brief should never use a symbol you haven't seen
     defined in this session.
   - **Errors / stack traces / log lines** — grep the source for the
     message, read the line that produces it. Quote the real error
     text, not a paraphrase.
   - **Git references** — branches, commits, PRs, "the change you
     made", "the work this morning": run `git log --oneline -20`,
     `git status`, `git diff HEAD~1..HEAD --stat`. For a specific
     file: `git log --oneline -10 -- <path>`.
   - **Related files** — if you're discussing one module, peek one
     layer out: sibling files, test file, the primary consumer. One
     layer is usually enough — do not boil the ocean.
   - **Package / dependency versions** — if a version matters for the
     discussion, check `package.json` / `pyproject.toml` /
     `Cargo.toml` / lockfile / `uv tree`.
   - **External references you can't reach** — Linear tickets, Slack
     threads, Calendar events, design docs in tools without a CLI:
     **name the gap explicitly in the brief** ("the user mentioned a
     Linear ticket I couldn't read — they'll have the context") so the
     voice agent knows that knowledge is closed to it.

   **Stop rule**: when every proper noun the brief would name has
   backing evidence in your tool history (a signature, a file you
   actually Read, a git SHA you actually inspected), context-gathering
   is done. If you'd need to bluff a single sentence to fit a
   structure slot, you are not done.

   **Anti-pattern (decision shape)**: do not fish. The point is to back
   up what is already on the table, not to re-investigate the repo. If
   the conversation never raised a topic, do not seed the brief with one
   to "fill space".

   **Reference shape changes this step's weight.** When the conversation
   is a corpus review (`--shape=reference`), the corpus *is* the subject,
   so reading all of it is the job, not fishing — the user will ask "what
   does file N actually say" and the detached voice agent can't open it.
   This is the bulk of the work. **Parallelize it**: fan out subagents,
   one per item or per cluster, to read the files / pull the tickets and
   return per-item facts (what it says, what's questionable, the exact
   claim to verify), then assemble. A 28-file audit is 28 concurrent
   reads, not a serial slog and not guesswork. See `reference_review.md`.

2. **Pick the shape, then compose the brief** from the conversation +
   your gathered context. Shape (decision vs reference) is chosen as
   described under *Shape* above. Use the matching prompt template:
   - decision shape, CLAUDE_VOICE → `prompts/claude_voice.md`
   - decision shape, REMINDERS → `prompts/reminders.md`
   - reference shape (either kind) → `prompts/reference_review.md`
     (it tells you where the REMINDERS writeback block goes)

   Each template defines audience, tone, structure, and the writeback
   contract. Read it once, then write the brief in your own words — do
   not paste the template back as the brief, and do not skip the
   structure sections.

   **POV (non-negotiable)**: the brief is a handoff *from you (the
   project agent) to the voice agent*. The voice agent is "you"; the
   user is third-person ("the user", "they"); self-refer as "I".
   Never address the user directly — you are briefing a peer who is
   about to meet them.

   **Project orientation (always include)**: the voice agent has no
   shell — it cannot run `pwd` or `ls` to find its bearings. So carry
   the layout into the brief: include the absolute working-directory
   path and a 2-level-deep tree of it, near the top, so the agent has a
   spatial model of the project and can place any file or directory the
   user names. Generate it during step 1 with `pwd` and `tree -L 2`
   (fall back to `find . -maxdepth 2 -not -path './.git/*' | sort` if
   `tree` is absent), and prune obvious noise dirs (`.git`,
   `node_modules`, `.venv`, build/output dirs) so it stays scannable.
   Drop it into the brief verbatim inside a fenced block — this is
   reference scaffolding, like an index, not spoken prose, so raw
   shell-form paths are fine here (the one exception to "spell paths
   out").

   **Quality bar**: the brief is the only context the voice agent gets
   (the detachment rule). If it reads like an agenda summary ("we are
   working on X, there are some open questions, walk through them") you
   failed — the voice agent has no substance to push on. Each open
   question / item must name the concrete alternatives or facts in play,
   with proper nouns from the conversation **or from step 1's
   context-gathering**. Hit the section structure for your shape.

   **Length is shape-dependent — do not apply one cap to both:**
   - decision shape: 250 – 500 words. Under-budget almost always means
     missing substance; be denser, not longer.
   - reference shape: **no global cap.** It scales with the number of
     items — budget per item, not per brief. The floor is coverage:
     every item the user is likely to raise must carry enough fact that
     the voice agent can discuss it without the file. A reference brief
     squeezed to 500 words is the original failure — it cannot ground a
     fact-check across many items.

   See the worked good-vs-bad example inside each template.

   **Self-check before saving**: re-read your brief and ask, for each
   proper noun (file, function, error string, slug, number, person):
   "Did I see this in this session, or am I paraphrasing memory of the
   conversation?" If the answer is the latter for anything
   load-bearing, go back to step 1 and look it up. Two minutes of
   re-reading beats a brief that collapses on the user's first probe.

3. **Save the brief** under `~/.claude/voice-takeouts/<YYYYMMDD-HHMM>-<slug-or-conv>.md`
   (create dir if missing). Always save, regardless of kind.

4. **Activate the channel**:

   - CLAUDE_VOICE: `pbcopy < <brief-path>`. Report the file path.
   - REMINDERS: pipe the brief into the bridge CLI:
     ```bash
     rbridge mailbox open --slug <slug> --kind REMINDERS --brief - <<< "$(cat <brief-path>)"
     ```
     Capture stdout — it gives you the exact `rbridge mailbox read …`
     command for later. Include that block verbatim in your reply.

5. **Tell the user** what you produced. Keep it terse:
   - File path of the saved brief.
   - For REMINDERS: list name + `read` command (from `rbridge` stdout).
   - For CLAUDE_VOICE: confirmation that the brief is on the clipboard.

## After the voice exchange

When the user comes back from voice and signals they are done (or you want
to check in mid-conversation), run:

```bash
rbridge mailbox read --slug <slug>
```

You'll get JSON with the user's responses. Each entry has:
- `kind`: `decision` | `note` | `question` | `deferred` | `done` | `free`
- `title`: cleaned response text
- `body`: any extended text in the reminder body

`deferred` is for things the user explicitly punted on during the call
("talked about it, no decision yet, revisit later"). Treat them as
open questions you should re-raise next session, not as resolved
items.

Process them, then close:

```bash
rbridge mailbox close --slug <slug>
```

(Or instruct the user to add a `done` reminder — the daemon auto-closes on
the next cycle, around 5 seconds.)

## Discoverability and silent breadcrumbs

The bridge drops a high-priority reminder titled `Voice exchange open: <slug>`
into the user's default Reminders list (the one iOS opens by default).
**No notification fires.** The user discovers the exchange the next time
they glance at Reminders, which is the point — agents can open exchanges
overnight, during meetings, while the user is AFK, without pushing alerts.

To disable the default-list mirror set `RBRIDGE_MAILBOX_MIRROR=false`.

## Failure modes

- **`rbridge: command not found`**: the bridge CLI is not on PATH.
  Install it from the reminders-bridge repo:
  ```bash
  uv tool install --force --reinstall \
    /Users/jurrejan/Documents/development/python/reminders-bridge
  ```
  Then retry `rbridge mailbox open`. The brief is already saved to disk
  so nothing is lost.
- **Reminders permission missing**: `rbridge mailbox open` exits with code
  2 and a clear error. The brief is saved to disk regardless. Tell the
  user to grant permission in System Settings → Privacy & Security →
  Reminders, then re-run.
- **Empty brief**: `rbridge mailbox open` refuses with exit 1. Always
  produce at least a one-paragraph brief.
- **Slug collision**: re-using a slug refreshes the header + brief
  reminders but keeps prior user responses intact. Idempotent.

## Examples

CLAUDE_VOICE (default, no return channel):

```
/voice-chat-takeout
```

Result: brief in `~/.claude/voice-takeouts/20260515-2130-current-thread.md`,
clipboard primed for paste into the voice agent (typically the Claude
Voice mobile app).

REMINDERS (writeback):

```
/voice-chat-takeout --mailbox=wallgen-shipping-decision
```

Result: brief saved to disk, list `Voice: wallgen-shipping-decision`
created in Reminders with two reminders (header + brief), mirror reminder
dropped in the default list, and the read command echoed for later.

REFERENCE REVIEW (corpus walk, auto-detected from the conversation):

```
/voice-chat-takeout            # conversation was "go over all 28 CLAUDE.md files and check the facts"
```

Result: I fan out subagents to read all 28 files, assemble a
`reference_review.md`-shaped brief (orientation + 28-entry map + per-item
facts for the flagged ones), default to `--kind=REMINDERS` so each
per-file decision lands as its own reminder, and echo the `read` command.
The brief is long on purpose — it carries every file the user might raise
because the voice agent cannot open any of them.
