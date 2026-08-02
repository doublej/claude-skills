# Run contract templates (standard tier)

Fill every `{{PLACEHOLDER}}` with a real value or delete its line. No `{{...}}` survives into the user's files. The turn/time cap must be IDENTICAL in the launcher and the mission's hard stop.

Adapted from jbrazy480/loop-maker (MIT).

## loop/MISSION.md

```markdown
# Mission: {{CODENAME}}

{{ONE_SENTENCE_GOAL}}

## Scope
- Building: {{WHAT}}
- Lives in: {{FOLDER_OR_BRANCH}}
- OUT of scope (do not touch): {{EXCLUSIONS}}

## Definition of done (provable — the transcript must be able to prove each line)
- [ ] {{CHECKABLE_CRITERION_1}}  — verify: `{{SHELL_COMMAND}}` → {{EXPECTED_OUTPUT}}
- [ ] {{CHECKABLE_CRITERION_2}}  — verify: {{HOW}}
- All features in feature_list.json have "passes": true

## Hard stop (identical to the launcher)
Stop when the definition of done is met, OR after {{N_TURNS_OR_HOURS}} — whichever
comes first. Also stop if {{FAILURE_CONDITION, e.g. "5 consecutive iterations
produce no progress on any feature"}}.

## Verifier (never the writer)
{{e.g. "npm test && npm run typecheck && npm run lint after every feature; a
fresh-context review pass over the diff before marking any feature passed.
Evidence goes in PROGRESS.md: paste the command output, never just claim it."}}

## Never ask, always log
Do not stop to ask questions. Decide with research, log the question + chosen
answer + why in PROGRESS.md, keep moving. Blocked after 3 distinct approaches →
mark it blocked in PROGRESS.md, ship the strong 80%, record what was cut.
Blocked is never reported as done.

## Rules
- One item per iteration; search the codebase before building anything new.
- No placeholder implementations. Never edit or remove a test to make it pass.
- Verify from the source of truth: the DB row, the raw response, the file on
  disk — never a UI badge or your own claim.
- Commit every green step on {{BRANCH}}. Nothing outward-facing: no deploy,
  publish, send, spend, or delete. Never touch secrets or files outside
  {{FOLDER_OR_BRANCH}}.
- Long command output → redirect to a file and tail it.
- After any context compaction: re-read this file and PROGRESS.md, continue at
  the next unchecked item.
```

## loop/feature_list.json (feature builds only)

JSON on purpose — agents corrupt JSON less than Markdown. The agent may only
flip `"passes"` to `true` with evidence logged in PROGRESS.md.

```json
{
  "features": [
    {
      "id": "F1",
      "description": "{{FEATURE}}",
      "verify": ["{{STEP: command or manual check with expected result}}"],
      "passes": false
    }
  ]
}
```

## loop/PROGRESS.md

```markdown
# Progress — {{CODENAME}}

## Honesty buckets
- DONE (with evidence):
- BLOCKED (reason + 3 approaches tried):
- CUT (what + why):

## Decision log (question → chosen answer → why)
| # | Question | Decision | Why |
|---|---|---|---|

## Iteration log (newest first — one line per iteration: what moved, evidence, next)
```

## Launcher (paste in reply AND write to loop/LAUNCH.md)

Pointing at the file beats a long inline prompt — no character ceiling, state
survives compaction:

```
Read loop/MISSION.md and execute it as the {{CODENAME}} run. Work until the
definition of done is met or the {{N_TURNS_OR_HOURS}} cap is hit. Track state
in loop/PROGRESS.md and loop/feature_list.json.
```

Self-paced multi-hour run → prefix with `/loop `. Recurring watch → `/loop 15m …` with the watch instruction inline. Cloud cron → `/schedule`.

## AGENTS.md note

If the repo has no rules file, offer a ≤60-line `AGENTS.md` at repo root
(commands, conventions, Always/Never lists). Never overwrite an existing
CLAUDE.md — append `@AGENTS.md` on its own line instead.
