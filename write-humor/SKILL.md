---
name: write-humor
description: >
  Write, sharpen, and diagnose humor in any medium — jokes, bits, social posts,
  talks, newsletters, marketing copy, product microcopy. Builds from premise
  mechanics (topic + attitude → premise → connector → turn) rather than guessing
  at funny, and ships a deterministic linter for buried reveals, explained
  punches, hedges, and crutch phrases. Use when asked to "write a joke", "make
  this funnier", "add humor", "punch this up", "why isn't this funny", "roast
  this", "write a bit about X", or when reviewing comedy/light copy before it
  ships. For chaotic persona-driven ideation use drunk-claude; for stripping AI
  tells use write-deslop.
---

# Write Humor

Craft skill for constructing humor deliberately. The premise is the engine, the
connector is the hinge, and final position is load-bearing — most "this isn't
landing" problems are mechanical, not mysterious.

<mode_detection>

Pick one. If genuinely ambiguous, ask once, then commit.

| Signal | Mode |
|---|---|
| "write a joke/bit about X", "roast this", topic with no draft | **CONSTRUCT** |
| "make this funnier", "add humor", "punch this up", draft supplied | **INJECT** |
| "why isn't this funny", "this isn't landing", draft that already tried | **DIAGNOSE** |

</mode_detection>

<construct>

## Mode: CONSTRUCT — build from nothing

1. **Establish the premise.** Do not skip this even when the user hands you a
   topic. Topic ≠ premise. Read `references/premise.md`, run the attitude
   rotation, generate six candidates, filter after.

   Climb the specificity ladder until you reach a scene, person, object, or
   behavior you can picture. Broad topics cannot be joked about.

2. **Mine the joke.** Read `references/mechanics.md`. Run the six-step drill
   literally — write the assumptions and connector down. Guessing at punchlines
   without naming the connector is the single most common failure.

3. **Select devices.** Read `references/devices.md`. Choose by the pressure
   already in the material, not by working down the list. Two or three devices
   composed beats one device applied hard.

4. **Escalate.** Tags off the same connector are the cheapest laughs available —
   the setup is already paid for. For anything longer than a one-liner, build a
   spine: theme → conflict → escalation → turn → ending.

5. **Rewrite.** Ladder in `references/mechanics.md`, in order. Steps 1–3 resolve
   most problems.

6. **Lint, then deliver.** See `<delivery>`.

</construct>

<inject>

## Mode: INJECT — add humor to existing prose

1. **Read for the argument first.** Identify the core information and the tone.
   The humor serves the text; if it competes with the information, the
   information wins.

2. **Set the density.** Read `references/calibration.md` — the dose is
   context-dependent and getting it wrong is worse than no humor. Match the
   register to the channel while you are there.

3. **Find the injection points.** Humor attaches where the reader's attention
   already changes gear:
   - the turn in an argument
   - the last item of a list
   - a summary or conclusion
   - headings, opening, closing
   - the concrete example inside an abstract passage

   Do not spread humor evenly. Even distribution reads as nervous.

4. **Convert, don't decorate.** Prefer replacing a dead phrase with a live one
   over inserting a joke. A dead metaphor swapped for a specific image does more
   than a bolted-on gag.

5. **Preserve meaning.** Every claim must survive intact. Report what changed and
   where.

6. **Lint, then deliver.**

</inject>

<diagnose>

## Mode: DIAGNOSE — fix what exists

1. **Run the linter first.** Mechanical faults are cheap to find and cheap to
   fix; do not spend judgment on what a script can catch.

   ```bash
   python3 ~/.claude/skills/write-humor/scripts/joke_lint.py draft.md --premise --strict
   ```

2. **Match the symptom.** `references/diagnosis.md` has the symptom → cause → fix
   table and the anti-pattern catalog.

3. **Test the two-story model.** Name Story 1 and Story 2 explicitly. If you
   cannot, there is no joke — there is a statement with an attitude, and the
   repair is at the premise, not the wording.

4. **Check the premise last-but-decisive.** A premise that generates exactly one
   joke is exhausted. No amount of rewriting recovers it; go back to
   `references/premise.md`.

5. **Report the mechanism, not just the verdict.** "The punch restates the setup
   instead of reinterpreting it" is actionable. "This isn't funny" is not.

</diagnose>

<delivery>

Always, before returning humor to the user:

```bash
python3 ~/.claude/skills/write-humor/scripts/joke_lint.py <file>
```

Fix every `error`. Justify any `warn` you keep. The linter has no opinion about
whether something is funny — premise quality, connector validity, and genuine
attitude remain your job.

**Deliver options, not a verdict.** Give 2–3 versions and name the device each
one uses. Voice is the user's decision; mechanics are yours. Recommend one and
say why in a single line.

**Show the joint when it helps.** For CONSTRUCT and DIAGNOSE, surfacing the
premise and connector lets the user redirect at the level that matters instead of
relitigating word choice.

</delivery>

<rules>

- Premise before punchline. Always. A blurry premise makes rewriting worthless.
- Never recycle known jokes, meme formats, or another comic's angle. If a line
  feels familiar, it is — say so and push for the personal observation.
- Recognition is not a laugh. Naming a thing the reader knows is not a punchline
  until something turns on top of it.
- Specific beats general, every time. Reach for the concrete noun.
- Cut everything after the reveal.
- If it needs a laugh-sign (`lol`, `/s`, an emoji), it needs a rewrite.
- Red lines in `references/calibration.md` are non-negotiable — no punching down,
  no trait-as-punchline, no humor during genuine distress, never trade
  correctness for a laugh.
- "Be serious" takes effect in the current reply, not the next one. See the
  escape hatch in `references/calibration.md`.

</rules>

<resources>

| File | Contents |
|---|---|
| `references/mechanics.md` | Four theories, two-story model, joke mine drill, escalation, rewrite ladder |
| `references/premise.md` | Topic + attitude formula, attitude vocabulary, quality filter, specificity ladder |
| `references/devices.md` | Twelve named devices — when to use, how each fails |
| `references/diagnosis.md` | Symptom → cause → fix table, anti-patterns, reading live reactions |
| `references/calibration.md` | Density per context, register per channel, red lines, escape hatch, house style |
| `scripts/joke_lint.py` | Deterministic checks — `--json`, `--premise`, `--strict`, `--unit line\|paragraph` |

</resources>
