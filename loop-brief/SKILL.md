---
name: loop-brief
description: >-
  Compile a quick one-line intent into a complete autonomous run — loop type,
  provable stop conditions, independent verifier, budget, and the exact launch
  line — without the user having to explain the process. Use when the user wants
  hands-off agent work from a short prompt, e.g. "run this overnight", "keep
  going until X", "babysit this PR", "fix all N errors", "don't ask me, just do
  it", "make a loop for this", "autonomous run", "ship while I sleep",
  "/loop-brief". Also use before writing any /loop or /schedule prompt, and when
  auditing why a previous autonomous run overran, stalled, or lied about being
  done.
---

# Loop Brief

Write loops, not prompts. The user gives one messy sentence; this skill returns a run they can launch and walk away from. Never make them explain the process — the process lives here.

<non_negotiables>
A run is only as safe as its weakest of three parts. Never ship a run missing any one:

1. **The Spec (the pin)** — what to build, what is explicitly OUT of scope, acceptance criteria. Stops invented scope.
2. **The Verifier (not the writer)** — work checked by something other than the agent that wrote it: tests, lint, typecheck, screenshot review, a fresh-context skeptic. The writer never grades its own homework.
3. **The Stop Condition (provable, dual)** — a finish line the transcript can literally prove, plus a turn/time cap. "Make it good" is unprovable; the loop will either never end or lie that it's done.

If the request can't be given a provable stop condition yet, the FIRST job is to define one.
</non_negotiables>

<step_0_ladder>
Take the lowest rung that solves the problem:

```
better prompt < verification step < criteria+cap prompt < /loop < /schedule
```

Each rung up adds token cost and new failure modes.

- One turn keeps failing because the agent can't tell if its work is correct → the fix is a **verification step** (how to check: run the app, click the thing, read the console), not a loop. A loop around blindness repeats the blindness N times.
- Task is one-shot and merely large → subagents, not a loop. Loops are for repeated cycles, not big batches.
- Reach for a loop only when iteration is essential or the work genuinely recurs.

"No loop needed — here's the simpler fix" is a valid, complete outcome. Say it and stop.
</step_0_ladder>

<step_1_recon>
**Silent recon before anything else — never ask what you can see.** Scan: folder structure, stack (package.json / pyproject / Cargo.toml), CLAUDE.md / AGENTS.md, test + lint + typecheck commands, current git state, existing CI. "I see you're on SvelteKit with vitest — I'll use that as the verifier" beats "what's your stack?".
</step_1_recon>

<step_2_classify>
Two questions decide the type: **what triggers a cycle** and **what stops the whole thing**.

| Type | Trigger | Stop | Primitive here |
|---|---|---|---|
| Turn-based | User's next prompt | User judgment | Plain prompt + verification step |
| Goal-based | One prompt, now | Criteria met OR attempt cap | Criteria+cap prompt; self-paced `/loop` for multi-hour |
| Time-based | Clock | User cancels or work dries up (PR merged, queue empty) | `/loop Nm` (local) |
| Proactive | Schedule, no human present | Each task exits on its own goal | `/schedule` (cloud cron) |

Mixed cases resolve by the *stop* question: "fix CI on this PR" sounds goal-based, but CI re-triggers as reviewers push — it stops when the PR merges. That's time-based.

For time-based: the interval is a property of the watched thing, not a preference. Reviews arrive over hours → 15–30m. A ~8-min CI run → one ~4-min check ×2, not every 60s. Prefer the longest interval that still catches the change in useful time.
</step_2_classify>

<step_3_stop_conditions>
Write the stop condition BEFORE the work description.

- **A number beats an adjective.** "0 strict errors", "Lighthouse ≥ 90", "RSS < 80MB" — mechanically checkable. "Faster", "cleaner" force the loop to judge "good enough", and under pressure it judges generously.
- **Always dual-stop.** Success OR bounded failure: `Stop when all 47 errors are fixed and tests pass, OR 5 consecutive attempts produce no reduction in error count.` Success-only runs forever on an unreachable goal; cap-only quits sloppy with the goal in reach.
- **Per-item failure policy** for multi-item runs: same failure 3× → mark item BLOCKED with reason, move to next. ALL blocked → report and stop. Without this, one poisoned item eats the night's budget.
- **Guard against goal redefinition.** Long runs under pressure quietly re-scope "done" (documented case: "peak memory ≤ 500MB" silently became "long-term memory health" ✅). Pin the original metrics in a place the loop can't edit their meaning (goals table in the contract/runbook) and audit claimed ✅ against the original wording.
</step_3_stop_conditions>

<step_4_draft_and_score>
Draft first — never interview.

1. **Draft v1 immediately** from the one-liner + recon. Fill every gap with a researched default, never a blank. Add the pieces the feature breaks without (empty/error states, input validation, auth on new routes) as decisions already made — easy to veto. List what was left out on purpose.
2. **Score it out loud** — `Brief Strength: x/10` against five checks, one line each (✓ or what's missing):
   - Scope pinned (incl. ≥1 thing OUT of scope)
   - Done is provable (numbers, not adjectives; dual stop)
   - Verifier isn't the writer
   - Stuck-plan set (per-item policy + decision log)
   - Budget bounded (turn/time cap + model routing)
3. **Questions: at most ONE batched form, ≤3 questions** — only for decisions that materially change the run and that recon + safe defaults can't resolve. Use the consult-user form dialog, one line of why per question. Never ask one-at-a-time; never ask what a default covers. On AFK/cancel: proceed with defaults, write the open questions into the contract's decision log.
4. "Just send it" (in any phrasing) → ship the current draft immediately with remaining assumptions logged in the contract.
</step_4_draft_and_score>

<step_5_tiers>
| Tier | When | Artifacts |
|---|---|---|
| **Light** | ≤ ~1h, low risk, single goal | One copy-paste prompt block. No files. |
| **Standard** | Multi-hour or multi-feature, resumable | `loop/MISSION.md` + `loop/PROGRESS.md` (+ `feature_list.json` for feature builds) → `references/run-contract-templates.md` |
| **Heavy** | Overnight / unattended / risky changes | Standard + runbook (`references/runbook-template.md`) + safety hooks (`references/safety-harness.md`) |

Standard/heavy rules:
- Launcher points at the mission file (short kickoff line, state on disk) — the prompt itself stays small. Short beats long: a 103-word master prompt has outperformed a 1,500-word one. Length is earned only by specifics (paths, commands, criteria), never prose.
- State lives in markdown/JSON files that survive compaction and session death. Feature lists are JSON on purpose — agents corrupt JSON less than Markdown.
- The turn/time cap is IDENTICAL in launcher and mission file. One number, two places.
- **Never-ask with escape hatch**, baked into every mission: decide with research, log question + chosen answer + why in PROGRESS.md, keep moving. Blocked after 3 distinct approaches → ship the strong 80%, record what was cut. Blocked is never dressed up as done (honesty buckets: done / blocked / cut).
- Evidence, not claims: every "it works" carries the test output, command result, or screenshot, verified from the source of truth (DB row, raw response, file on disk) — never a UI badge or the worker's own claim.
- Commit every green step; work on an isolated branch or worktree.
</step_5_tiers>

<step_6_deliver>
Deliver a **Run Card**:

1. **Type + one-line justification** (or "no loop — simpler fix: …")
2. **Brief Strength: x/10** (with remaining assumptions if shipped before 10)
3. **The contract** — light: one copy-paste block; standard/heavy: files written, with paths
4. **Launch line, verbatim** — the exact `/loop …`, `/schedule …`, or prompt to paste. One thing, then walk away.
5. **Stop conditions + budget** — success, failure cap, per-item policy, turn/time cap
6. **Three plain lines on what happens next** — what it will do, how it checks itself, what the user sees on return

Safety briefing (every standard/heavy run, compressed to ~4 lines):
- Nothing outward-facing inside the run: no deploy, publish, send, spend, delete. Ever.
- Scoped to one branch/worktree so a bad run can't damage the rest. Secrets stay untouched (red line).
- Caps are set; the run has explicit permission to stop.
- **The morning review is not optional** — the loop amplifies judgment, it doesn't replace it.
</step_6_deliver>

<step_7_audit>
The run's final report is a claim, not a fact. After any substantial run:

- Re-measure headline metrics independently (a real run self-reported 122MB; independent measurement said 79MB — only the audit made either number trustworthy).
- Check each ✅ against the goal's ORIGINAL wording, not the report's wording.
- Adversarially verify before trusting fixes (same run: 40 candidate fixes, 15 survived skeptic review).
- Keep the vetoed list — rejections are results; they stop the next run from re-attempting dead ends.
</step_7_audit>

<worked_examples>
**"Babysit PR #142 until it merges"** → Time-based, light tier:

```
/loop 15m check PR #142: address new review comments, fix failing CI.
Stop when the PR is merged. If the same CI failure persists after 3
consecutive fixes, stop and summarize what's blocked.
```

**"Fix all 47 TypeScript strict errors"** → Goal-based, light tier: criteria+cap prompt — `tsc --strict reports 0 errors and tests pass. Batches of ~10, tests after each batch. Stop after 6 attempts or when two consecutive batches reduce the count by zero.`

**"Run this refactor overnight"** → Heavy tier: mission + runbook + hooks, self-paced `/loop` pointed at the runbook, audit planned for the morning.

**"Translate the README to Dutch"** → No loop. One turn, verifiable by reading. Recommending against the loop is the correct output.
</worked_examples>

<credits>
Vendored under license: loop taxonomy, stop-condition rules, runbook pattern from edwluo/designing-loops (MIT); mission scoring, never-ask protocol, honesty buckets from jbrazy480/loop-maker (MIT); hook safety layers and autonomy zones from GodModeAI2025/NightShift (Apache-2.0).
</credits>
