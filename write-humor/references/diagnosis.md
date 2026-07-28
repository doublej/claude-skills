# Diagnosis

Start here when something exists but is not working. Match the symptom, apply the
fix, then re-run the rewrite ladder in `mechanics.md`.

<symptom_table>

| Symptom | Cause | Fix |
|---|---|---|
| "I have a topic but no jokes" | No premise | Run the attitude rotation in `premise.md` |
| "It's a funny story but it dies on the page" | Story has no public premise | Extract the observation; reorder the events as evidence for it |
| "The punch feels random" | No connector | Name the target assumption and the connector before touching the wording |
| "They understand it but don't laugh" | No turn, too much explanation, or weak attitude | Sharpen the violation, cut words, raise the emotional pressure |
| "It lands too early" | Reveal placed before the end | Move the decisive word or image to final position |
| "It reads as written, not spoken" | Prose rhythm is leading | Convert paragraphs into scenes and act-outs; read aloud |
| "It's a pile of separate jokes" | No spine | Build theme → conflict → escalation → turn → ending |
| "It's clever but cold" | All mechanics, no attitude | Find what actually irritates you about the topic |
| "It's mean" | Violation without a safety net | Add self-implication, impossible exaggeration, or redirect upward |
| "It's fine, just not funny" | Premise generates exactly one joke | Go back to the premise; this one is exhausted |

</symptom_table>

<joke_level_anti_patterns>

| Anti-pattern | What it looks like | Repair |
|---|---|---|
| **Single-story joke** | The punch restates the setup's complaint with more heat | You have an attitude, not a joke. Run the joke mine. |
| **Random twist** | Surprising but does not fit backwards | Story 2 must be retroactively inevitable. Find a real connector. |
| **Multiple connectors** | Several possible jokes tangled in one line | Pick one. The others become tags. |
| **Buried reveal** | The decisive word appears mid-sentence, then the line trails off | Everything after the reveal is drag. Cut it. |
| **Explained punch** | "…which is funny because…" | If it needs explaining, the connector was wrong. |
| **Hedged punch** | "kind of", "I guess", "maybe" inside the punch | Commit. A hedge tells the reader you don't believe it. |
| **Flagged joke** | "lol", "just kidding", "/s", "😂" | You are asking for the laugh instead of earning it. |
| **Diluted list** | Five parallel items where three would do | Two to establish, one to break. Items four and five are decay. |
| **Punching down** | The target has less power than the audience | Redirect upward, or make yourself the specimen. |
| **Reference as punchline** | The "joke" is naming a thing the reader recognizes | Recognition is not a laugh. Add a turn on top of it. |

</joke_level_anti_patterns>

<automated_check>

`scripts/joke_lint.py` catches the mechanical subset deterministically — buried
reveals, explained punches, hedges, crutch phrases, setup bloat, diluted lists. It
has no opinion about whether anything is funny.

```bash
python3 ~/.claude/skills/write-humor/scripts/joke_lint.py draft.md
python3 ~/.claude/skills/write-humor/scripts/joke_lint.py draft.md --premise --strict
python3 ~/.claude/skills/write-humor/scripts/joke_lint.py draft.md --json
```

Run it before delivering. Errors should be fixed; warnings should be justified.
Everything it *cannot* see — premise quality, whether the connector is real,
whether the attitude is genuine — is your job.

</automated_check>

<testing_the_draft>

Real reactions outrank analysis. Where a live test is possible, read the results
this way:

| Signal | Meaning |
|---|---|
| Laughter before the end | The turn was visible too early |
| Silence after a long setup | Premise was unclear, or the payoff did not justify the wait |
| Understanding but no laugh | Too much explanation, or the violation is too mild |
| One cold room | Weak evidence — do not rewrite yet |
| Three failures | Strong evidence — cut or rebuild |
| Laugh in an unplanned spot | Follow it. That is the real premise. |

That last row is the most valuable and the most ignored. An unplanned laugh is the
material telling you where its actual pressure is.

</testing_the_draft>
