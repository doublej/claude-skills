# Runbook template (heavy tier)

Use when a run goes many iterations without a human present — overnight runs, multi-hour migrations, autonomous optimization. The runbook is a file in the repo: the loop's single source of truth, re-read at the start of every iteration, updated and committed at the end. Pattern proven on a 15-iteration, ~13-hour autonomous performance loop.

Adapted from edwluo/designing-loops (MIT).

## Why a file, not a prompt

- **Wake-ups start with thin context.** A scheduled loop may resume with no conversation history — durable state must live outside the conversation.
- **Prompts can't be audited; files can.** The ledger records what the loop did and why, reconcilable against reality afterwards.
- **Commits make it resumable.** A crashed loop restarts from the last committed ledger entry, not from zero.
- **Written goals resist redefinition.** A goals table with numbers, committed before the run, is the fixed point the audit checks against.

## Template

```markdown
# {{NAME}} Loop Runbook

> Status: ACTIVE | PAUSED | DONE ({{DATE}})
> This file is the loop's single source of truth: every iteration starts by
> reading §5 Ledger and ends by updating §5 and committing this file.
> Background: {{LINKS to motivating docs/issues}}

## 0. Goals (stop when ALL achieved or ALL blocked)

| # | Goal | Success metric (a number, measured how) |
|---|---|---|
| G1 | {{headline goal}} | {{e.g. peak memory ≤ 500MB on fixed benchmark corpus, measured by X}} |
| G2 | {{secondary}} | {{quantified}} |
| G3 | Safety | main stays releasable; every change verified, zero regressions |

## 1. Hard guardrails (re-read every iteration; violating any = stop that item)

Tier the rules — blanket bans force the loop to disobey or stall:

- 🟢 Allowed: {{powerful-but-scary things it MAY do, with discipline attached —
  e.g. "may rebuild and restart the app for verification; record timestamp,
  branch, commit hash in the ledger each time"}}
- 🔴 Red lines: {{never touch — security-sensitive code, secrets/credentials,
  user data, releases, files outside the project. Spell them out.}}
- 🟡 Conditional: {{allowed only after a stated precondition — e.g. "risky
  refactor X only after measurement proves ROI; any regression = revert"}}
- Isolated branch/worktree; commit everything (uncommitted worktree work dies
  with it). Main stays untouched.
- Self-merge gate (all three or don't merge): zero observable behavior change,
  tests green, independent review with no blocker.
- New facts contradicting this plan → stop the item, record in ledger. When
  measurements contradict expectations, record both sides; never erase the
  inconvenient number.

## 2. Work queue (ordered; every item pre-verified to be real)

Only queue items whose diagnosis is independently confirmed — in the original
run, adversarial review rejected 25 of 40 candidates BEFORE the loop started.
Queuing unverified work wastes the whole night.

- Format: `id · description · risk[low/med/high] · verify-how`
- Mark which items need live verification (rebuild/measure) vs. tests alone.

### 2.X Vetoed approaches (do not re-attempt)
- {{approach}} — {{who/what rejected it and why}}

## 3. Iteration protocol (every wake-up, in order)

1. Read §5 Ledger latest state (not the whole history).
2. Run the standing measurement pass; append data to §5.
3. Take the highest-priority available item; advance it to a natural
   breakpoint — bounded work per iteration.
4. Code items: tests → independent review for >~50 LoC or anything touching
   concurrency/data integrity → live verification against a baseline captured
   BEFORE the change → merge gate (§1) → merge or revert, never half-landed.
5. Update §5 (one line: what moved, data, next) → commit + push.
6. Pacing: more work queued → short sleep. Only waiting on something slow →
   long sleep (30–60m). Done or all blocked → final report, stop scheduling.
7. Same failure 3× → item BLOCKED with reason, move on. ALL blocked → final
   report + slow heartbeat until the human returns.

## 4. Final report (fill into §5 top when the loop ends)

- ✅ Landed: commits + verification evidence each (before/after numbers)
- 🖥️ Current state the human needs (what's running, which branch, how to
  get back)
- 🧭 Decisions deferred to the human, with the data needed to decide
- 📈 Goal-by-goal: ORIGINAL metric wording vs. measured result — if a goal
  was re-scoped mid-run, say so explicitly
- ⚠️ Blocked/abandoned items and why

## 5. Ledger (newest first; append every iteration)
```

## Post-run audit (the human's half of the contract)

1. Re-measure headline metrics independently — trust self-reported numbers in
   neither direction.
2. Compare each ✅ against §0's original wording. Re-scoped goals are sometimes
   legitimate; silent re-scoping never is.
3. Spot-check landed changes against the merge gate.
4. Carry §2.X (vetoed approaches) into the next run's runbook.
