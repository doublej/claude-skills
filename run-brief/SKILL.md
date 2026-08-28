---
name: run-brief
description: >-
  Compile a one-line intent into a complete hands-off run that finishes in one
  pass — scope pin, execution shape, provable done-when, independent verifier,
  budget, and the exact launch line — without the user explaining the process.
  Use for autonomous work that does NOT repeat: "do this while I'm out", "just
  do it, don't ask me", "fix this whole thing and report back", "delegate this",
  "run it end to end", "one-shot it", "/run-brief". Sibling of loop-brief —
  route to loop-brief instead when the work is a repeating cycle (watch a PR,
  poll CI, run every N minutes, iterate until a bar is beaten).
---

# Run Brief

One messy sentence in, one launchable run out. The user never explains the process — the process lives here. This is the **one-shot** half of the pair; `loop-brief` owns anything that cycles.

<non_negotiables>
A hands-off run is only as safe as its weakest of four parts. Never ship one missing any:

1. **The Spec (the pin)** — what to build, what is explicitly OUT of scope, acceptance criteria. Stops invented scope.
2. **The Verifier (not the writer)** — tests, lint, typecheck, a fresh-context skeptic subagent, a screenshot read. Whoever wrote it never grades it.
3. **Done-when (provable, dual)** — a finish line the transcript can prove, PLUS an abandon-when. "Make it good" is unprovable; the run will either sprawl or lie.
4. **Budget** — agent count / wall-clock / turn cap, stated once and repeated identically wherever it appears.

If the request has no provable done-when yet, the FIRST job is to write one.
</non_negotiables>

<step_0_ladder>
Take the lowest rung that solves the problem:

```
do it now < one prompt + a verification step < subagent fan-out < /orchestrate < /orchestrate-sessions or teams (worktrees)
```

- The task is small and you can just do it → **do it**, and say that instead of producing a brief. A brief for 10 minutes of work is the over-engineered answer.
- The agent keeps failing because it can't tell if its own work is right → add a **verification step** (run it, click it, read the console), not more agents.
- Work genuinely repeats or must iterate against a bar → **stop and hand off to `loop-brief`** (or `gauntlet-loop` for build-vs-critic iteration). Don't build a loop here.
- Escalate to worktrees/sessions only when writers would collide on the same files or the run outlives one session.
</step_0_ladder>

<step_1_recon>
**Silent recon first — never ask what you can see.** Scan: folder layout, stack (package.json / pyproject / Cargo.toml), CLAUDE.md / AGENTS.md, the real test + lint + typecheck commands, git state (dirty? branch?), existing CI. "vitest is already wired, that's the verifier" beats "what's your stack?".
</step_1_recon>

<step_2_shape>
Pick the execution shape from how the work decomposes, not from how big it feels.

| Shape | When | Launch with |
|---|---|---|
| Single pass | One coherent change, one verifier at the end | Plain prompt block + verification step |
| Fan-out | N independent items, no shared files | `/orchestrate` (or `agent-orchestrator` skill for a hand-built DAG) |
| Pipeline | Stages feed each other (research → plan → build → verify) | `/orchestrate` with ordered stages |
| Parallel writers | Several agents editing overlapping code | `teams` skill — worktree per writer, merge at the end |
| Long / outlives a session | Hours of work, resumable, needs its own context | `/orchestrate-sessions` |

Two failure smells: fan-out where items share files (they will clobber each other → pipeline or worktrees), and a pipeline where stages are actually independent (wasted wall-clock → fan out).
</step_2_shape>

<step_3_done_when>
Write done-when BEFORE the work description.

- **A number beats an adjective.** "0 strict errors", "all 23 routes return 200", "bundle < 250KB". "Cleaner" forces the run to judge itself, and under pressure it judges generously.
- **Always dual.** Done-when OR abandon-when: `Done when tsc --strict reports 0 errors and the suite passes, OR after 3 approaches the count has not moved.`
- **Per-item policy** for multi-item runs: same failure 3× → mark the item BLOCKED with a reason, move on. ALL blocked → stop and report. One poisoned item must not eat the whole budget.
- **Pin the original wording.** Long runs quietly re-scope "done". Keep the acceptance criteria in a place the run can't reword, and audit every claimed ✅ against the original line.
- Honesty buckets in the final report: **done / blocked / cut**. Blocked is never dressed up as done.
</step_3_done_when>

<step_4_draft_and_score>
Draft first — never interview.

1. **Draft v1 immediately** from the one-liner + recon. Fill every gap with a researched default, never a blank. Include the things the change breaks without (empty/error states, input validation, auth on new routes) as decisions already made — easy to veto. List what was deliberately left out.
2. **Score it out loud** — `Brief Strength: x/10`, five checks, one line each (✓ or what's missing):
   - Scope pinned (incl. ≥1 thing OUT)
   - Done-when provable (numbers, dual)
   - Verifier isn't the writer
   - Stuck-plan set (per-item policy + decision log)
   - Budget bounded (agents/time cap + shape justified)
3. **Questions: at most ONE batched form, ≤3 questions**, only for decisions that materially change the run and that recon + safe defaults can't settle. Use the consult-user form dialog with one line of *why* per question. On AFK/cancel: proceed with defaults, log the open questions.
4. "Just send it" in any phrasing → ship the current draft immediately, assumptions logged.
</step_4_draft_and_score>

<step_5_tiers>
| Tier | When | Artifacts |
|---|---|---|
| **Light** | ≤ ~1h, low risk, single goal | One copy-paste prompt block. No files. |
| **Standard** | Multi-hour, multi-agent, or must survive compaction | `run/BRIEF.md` + `run/PROGRESS.md` in the repo |
| **Heavy** | Unattended or risky changes | Standard + worktree isolation + safety hooks |

Standard/heavy rules:

- **State lives in the project repo** — `run/BRIEF.md`, `run/PROGRESS.md`. Never a scratchpad, `/tmp`, or any session-scoped path: it is wiped before the next session can read it, and a brief the run can't re-read is the same as no brief.
- The launcher stays short and points at the brief file. A 100-word kickoff beats a 1,500-word prompt; length is earned by specifics (paths, commands, criteria), never prose.
- The budget number is IDENTICAL in launcher and brief file.
- **Never-ask with an escape hatch:** decide with research, log question + answer + why in PROGRESS.md, keep moving. Blocked after 3 distinct approaches → ship the strong 80%, record what was cut.
- Evidence, not claims: every "it works" carries the command output, test result, or screenshot, checked at the source of truth (DB row, raw response, file on disk) — never a UI badge or a worker's own say-so.
- Commit every green step; work on an isolated branch or worktree.

For standard/heavy, adapt the templates in `~/.claude/skills/loop-brief/references/` (`run-contract-templates.md` for BRIEF/PROGRESS, `safety-harness.md` for hooks and autonomy zones) — read the file and rename `loop/MISSION.md` → `run/BRIEF.md`, dropping the iteration/wake-up sections. **Name the section headings you kept and the ones you dropped** when you report the files written, so it is visible the template was actually opened.
</step_5_tiers>

<step_6_deliver>
Deliver a **Run Card**:

1. **Shape + one-line justification** (or "no run needed — I just did it", or "this repeats → loop-brief")
2. **Brief Strength: x/10** with remaining assumptions
3. **The contract** — light: one copy-paste block; standard/heavy: files written, with paths
4. **Launch line, verbatim** — the exact `/orchestrate …`, `/orchestrate-sessions …`, or prompt to paste. One thing, then walk away.
5. **Done-when / abandon-when / per-item policy / budget**
6. **Three plain lines** — what it will do, how it checks itself, what the user sees on return

Safety briefing (standard/heavy, ~4 lines):
- Nothing outward-facing inside the run: no deploy, publish, send, spend, delete.
- Scoped to one branch or worktree; secrets untouched (red line).
- Budget is set and the run has explicit permission to stop.
- **The review on return is not optional** — delegation amplifies judgment, it doesn't replace it.
</step_6_deliver>

<step_7_audit>
The final report is a claim, not a fact. After any substantial run:

- Re-measure the headline numbers independently. Self-reported metrics drift optimistic.
- Check each ✅ against the ORIGINAL acceptance wording, not the report's paraphrase.
- Adversarially verify fixes with a fresh-context skeptic before trusting them.
- Keep the vetoed list — rejections are results, and they stop the next run re-walking dead ends.
</step_7_audit>

<worked_examples>
**"Add dark mode across the app while I'm out"** → Fan-out, standard tier. Recon finds 14 components + a token file. `run/BRIEF.md` pins tokens-first, one agent per component group, done-when = every component renders in both themes with no hardcoded hex left (`grep -rE '#[0-9a-fA-F]{6}' src/` empty) and the suite passes. Launch: `/orchestrate` pointed at the brief.

**"Fix all 47 TypeScript strict errors"** → Single pass, light tier: `tsc --strict → 0 errors and tests pass. Batches of ~10, tests after each. Abandon if two consecutive batches reduce the count by zero.`

**"Port these 6 services to the new client"** → Parallel writers, heavy tier: worktree per service via `teams`, per-service BLOCKED policy, merge and run integration tests at the end.

**"Keep fixing CI on PR #142 until it merges"** → Not this skill. It recurs → `loop-brief`.

**"Translate the README to Dutch"** → No brief. Just do it; verification is reading it.
</worked_examples>
