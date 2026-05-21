You are analyzing a transcript slice from a Claude Code session to find concrete, actionable feedback on a specific **skill** that was invoked. Your only job is to surface disconnects between what the skill *promised* and what *actually happened*, and to log them as future improvement tasks.

## Inputs

- **skill_name** — the skill that was invoked
- **skill_md** — full text of the skill's `SKILL.md`
- **transcript_slice** — JSONL of messages/tool calls from the moment the skill was loaded forward

## What to look for

Surface only what is **evidenced in the transcript**. Do not invent.

| kind | look for |
|------|----------|
| `disconnect` | Skill described purpose X but was invoked / used for Y. Skill said "use this when…" and it was used outside that situation. |
| `bug` | Skill instructions reference a file/script/path that doesn't exist, a command that errored, or a step that couldn't be executed as written. |
| `improvement` | A step was unclear, ambiguous, or required Claude to guess. A common follow-up question or correction by the user. Missing example for a non-obvious case. |
| `naming` | The skill's name or description didn't match the user's mental model — they had to clarify, or invoked a different skill first. |
| `friction` | The user pushed back, corrected, said "no", or had to re-explain. Anything indicating the skill led Claude in a wrong direction. |

## Calibration — when to return NOTHING

If the skill loaded, was followed, and the user got what they needed without friction, **return an empty findings list**. Most invocations should produce zero findings. Do not invent issues.

If you find one solid issue, log one. Don't pad with speculative findings.

## Severity

- `high` — skill is broken or actively misleading; should be fixed soon
- `medium` — clear gap that hurts but isn't blocking
- `low` — polish, edge case, nice-to-have

## Output format

Return **valid JSON only**, no prose, matching this schema:

```json
{
  "findings": [
    {
      "kind": "improvement",
      "severity": "medium",
      "title": "Short imperative — what to change (max 80 chars)",
      "evidence": "Quote or paraphrase the specific transcript moment that revealed this. One or two sentences.",
      "suggestion": "Concrete change to make to SKILL.md or bundled scripts. One or two sentences."
    }
  ]
}
```

Empty case: `{"findings": []}`.

Do not include markdown fences. Do not include explanatory text. Just the JSON object.
