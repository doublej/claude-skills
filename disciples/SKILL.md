---
name: disciples
description: Run any number of improvement subagents ("disciples") on the current repo, one at a time in a rotating loop, each owning one lens (design, performance, simplify, bugs, tests, a11y, security, docs, or any custom lens). Each disciple makes one or two small verified commits per turn and reads its own past results from a ledger, so later turns build on earlier ones. The loop keeps going until every lens reports nothing left worth changing. Use for "/disciples", "keep improving this", "run N agents in a loop", "improvement loop", "let agents polish this repo", "rotate agents over design/perf/bugs".
---

# Disciples

The main session is the master. It never edits code itself: it dispatches one disciple, checks what came back, writes the ledger, and dispatches the next. Disciples run one at a time because they share one working tree and one git index. Two disciples at once would edit and stage over each other's work.

<presentation>
Run tier. Print the banner once when the loop starts, then print the report when the loop ends or JJ stops it.
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   DISCIPLES                                                  ║
║   Rotating subagents that keep improving a repo              ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
```
DISCIPLES  ──  <repo>   disciples: <n>   turns: <n>   stop: <converged|cap|blocked|stopped>

#    LENS           RESULT   COMMIT    EVIDENCE
──────────────────────────────────────────────────────────────
1    design         ✓        a1b2c3d   before/after shots, 2 sizes
2    performance    —        —         no change beyond spread (3x3)
3    bugs           ✗        reverted  new test failure, fix failed

github.com/doublej
```
Marks: `✓` committed and verified, `—` nothing worth changing, `✗` reverted or blocked. Under the block, list the beads or issues the disciples filed and the ledger path.
</presentation>

<arguments>
Parse the arguments as data:
- empty → 4 disciples: `design performance simplify bugs`
- a number N → the first N lenses in the order in `references/lenses.md`. If N is larger than the catalogue, derive the extra lenses from the repo's backlog or its CLAUDE.md, and name each one in the setup line.
- words or quoted phrases → one disciple per lens, in the order given. A name that isn't in the catalogue becomes a custom lens.
- `rounds=M` → stop after M full rotations. With no cap, the loop runs until it converges.
- `resume` → continue from the newest ledger instead of starting a new one.
</arguments>

<setup>
Do this once, then print the banner and one setup line: `lenses: … · check: <cmd> · baseline: <n failing> · ledger: <path>`.
1. Confirm the directory is a git repo. If it isn't, report `Blocked: not a git repo` and stop.
2. Find the check command in this order: the repo CLAUDE.md's verification section, then a `check` recipe in the justfile or Makefile, then the package.json scripts (lint + typecheck + test), then the pyproject tool config. If none of these exists, use the test command alone and say so in the setup line.
3. Run the check once. Record which gates fail now as the **baseline**. A disciple may not add a failure to it.
4. Create the ledger at `$(git rev-parse --git-common-dir)/disciples/<YYYY-MM-DD-HHMM>.md`. It lives in the git dir, so it never dirties the tree and every worktree shares it. Write the lenses, check command, and baseline into it.
</setup>

<loop>
Each turn:
1. **Pick** the next active lens in rotation.
2. **Fill** `references/preamble.md` with these values:
   - `{{LENS}}`: the lens name
   - `{{MISSION}}`: the lens's block from `references/lenses.md`, or the custom-lens block with its name filled in
   - `{{CHECK}}` and `{{BASELINE}}`: from setup
   - `{{DIRTY}}`: run `git status --porcelain` now, minus the files disciples committed. These files belong to other sessions.
   - `{{HISTORY}}`: this lens's previous ledger entries
3. **Dispatch** the filled brief as one `Agent` call with `subagent_type: "general-purpose"` and `model: "opus"`. Dispatch nothing else while it runs.
4. **Verify** what the disciple reports before accepting it:
   - `git show --stat <sha>` touches only the files it named, and none from `{{DIRTY}}`.
   - Rerun the check command. It shows no failure beyond the baseline.
   - The evidence it names (screenshots, numbers, test names) exists.
   - If something fails, send the same disciple one `SendMessage` asking it to fix it. If it fails again, run `git revert --no-edit <sha>` and mark the turn `✗`.
5. **Record** one ledger entry for the turn: turn number, lens, result mark, shas, the evidence, what was tried and rejected, beads or issues filed, and the disciple's "Next for this lens" line.
6. **Retire** a lens after it returns `Nothing worth changing` on two of its turns in a row, or after two `✗` turns in a row.

When a step doesn't need my input, keep going. Put status notes in the same message as your next action, one line per turn: `#<n> <lens> <mark> <sha> <one-line result>`. Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, changing anything outside this repository.

The loop ends when every lens is retired (`converged`), the `rounds=` cap is reached (`cap`), the check fails at the start of a turn for a reason no disciple caused (`blocked`, with the failure shown), or JJ interrupts (`stopped`). When it ends, print the report and write the repo's handoff note if its CLAUDE.md asks for one.

After a context compaction, reread the ledger before dispatching again. The ledger, not the conversation, is the record of what happened.
</loop>

<boundaries>
- The master never pushes, deploys, or rewrites history. Disciples only commit.
- The repo's own CLAUDE.md wins over this skill on commit format, journals, task trackers, and forbidden paths. The preamble tells disciples to read it first.
- Keep each dispatch self-contained. A disciple sees only its brief, never this conversation.
</boundaries>
