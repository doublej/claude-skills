# Safety harness (heavy tier)

Why unattended runs die: permission-skipping alone breaks down after ~20 minutes — context gets compacted, the agent forgets the plan, repeats steps, or drifts; and a hallucinated destructive command has full permission to execute. Four layers fix this. Offer them for any overnight/unattended run; install only with the user's go-ahead (they're project-level hooks).

Architecture adapted from GodModeAI2025/NightShift (Apache-2.0).

## Layer 1 — Runbook as external memory

The runbook/mission file (see other references) is the loop's memory. Every step concrete: a file path, a shell command, or a named function — "implement the auth module" makes a headless agent guess; guessing unattended means wasted budget or broken code.

## Layer 2 — Hooks (guardrails)

Project `.claude/settings.json` hooks (adapt the paths/patterns per project):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "loop/hooks/block-destructive.sh" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "date +%s > loop/heartbeat" }]
      }
    ],
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [{ "type": "command", "command": "echo 'Context was compacted. Re-read loop/MISSION.md (or the runbook) and PROGRESS.md, then continue at the next unchecked item.'" }]
      }
    ]
  }
}
```

`block-destructive.sh` — read the tool input JSON from stdin, exit 2 (block) on
matches like: `rm -rf /`, `rm -rf ~`, `sudo `, `chmod 777`, `curl … | bash`,
`git push --force`, `git reset --hard origin`, writes outside the project dir,
anything touching `.env`/secrets paths. Keep the list short and project-tuned —
an over-broad blocker stalls the run.

The `SessionStart` compact hook is the critical one: context compaction, not
permissions, is what kills long runs. Re-injecting "re-read the runbook" makes
the run survive any number of compactions.

## Layer 3 — Autonomy zones (in the runbook/mission)

Prevents both failure modes: hesitating on trivial ops, and overreaching on critical files. Adapt per project — a devops task needs config freedom; a docs task can be write-restricted to `docs/`:

```markdown
🟢 Free (no logging): read files; create/edit in src/, tests/, docs/;
   install deps; run tests; git add + commit on the run branch
🟡 Log first (one line in PROGRESS.md why): delete files; change config
   files; touch >3 files in one step; major dependency upgrades
🔴 Forbidden (even with permissions skipped): files outside the project;
   secrets/credentials/API keys; production data; force-push; deploy,
   publish, send, spend, delete
```

## Layer 4 — Error budget + watchdog

- **Error budget** in the mission: e.g. "≤2 known-flaky test failures tolerated; any NEW failing test = fix before proceeding; 3 consecutive iterations with rising failure count = stop and report." Without it the loop either stops at the first flaky test or ignores real regressions.
- **Watchdog** (optional, outside the session): a cron/launchd job that checks `loop/heartbeat` age; stale >N minutes → notify the user. Keep it dumb — liveness only, no restarts.

## Boundaries

- Sandbox/permission mode is the user's call — never enable permission-skipping yourself; state that the harness assumes it and let the user launch.
- Hooks live in the project and outlive the run — remind the user to remove them (or gate them on the run branch) when the loop is done.
