---
name: junie-delegate
description: Plan and manage a coding task while JetBrains Junie (gemini-3.8-flash, "flash 3.8") writes every line of code headless. Use when the user says "let Junie code it", "delegate to Junie", "you plan, Junie builds", "junie-delegate", or wants Claude to stay on architecture, review and verification while a cheap fast model does the typing. NOT for tasks Claude should implement itself.
---

# Junie Delegate

Claude plans, scopes, reviews and verifies. Junie writes the code. The split is the point:
Claude never edits implementation files in this mode, and Junie never decides scope.

<roles>
Claude (planner/manager) — owns and never delegates:
- Reading the codebase, deciding the approach, splitting work into orders.
- Writing the work order: exact files, exact done-when.
- Reviewing the diff and running the quality gates. Junie's self-report is a claim, not evidence.
- Accepting, correcting, or reverting.

Junie (implementer) — owns only:
- Editing source files inside one accepted work order.

Claude may still write: the work order, throwaway verification scripts, and commit messages.
Claude may NOT write: the implementation, its tests, or its fixes. A correction goes back to
Junie as a follow-up order, not into Claude's own Edit call.
</roles>

<preflight>
Run once per task, before the first order:

```bash
cd <project> && git status --short && git rev-parse --short HEAD
```

- Working tree must be clean. Junie commits its own work (JJ's `~/.junie/AGENTS.md`
  mandates commit-when-done), so a dirty tree makes its commits unreviewable. Commit or
  stash first.
- Record the short SHA as `BASELINE`. This is the only handle on what Junie changed.
- Project-specific rules for Junie go in `<project>/.junie/guidelines.md` — Junie reads that
  file itself, so put standing constraints there instead of repeating them in every order.
</preflight>

<work_order>
One order = one atomic change Claude can verify in a single review pass. Too big is the
failure mode: a flash model handed "refactor the auth layer" returns plausible sprawl.

Write the order in this shape, as one string:

```
Goal: <one sentence, the outcome not the steps>
Files: <exact paths Junie may touch; say "no other files">
Constraints: <existing helper to reuse, pattern to match, what not to change>
Done when: <a command that exits 0, or an observable Claude can check>
```

Rules:
- Name the files. Unscoped orders are where a cheap model invents structure.
- State the done-when as something Claude can run. "Works correctly" is not a done-when.
- No more than ~3 files per order. Split instead of widening.
- Do not paste large code into the order — Junie reads the repo.
</work_order>

<dispatch>
```bash
python3 ~/.claude/skills/junie-delegate/scripts/dispatch.py \
  --project <project> "<work order>"
```

Long orders: write to a file and pass `--task-file <path>`.

Before announcing a dispatch, state the `BASELINE` SHA and quote the order's `Done when:`
line verbatim. If either is missing, the preflight was skipped — go back and run it.

The script pins `modelForLaunch` to `gemini-3.8-flash` in `~/.junie/settings.json` (Junie has
no `--model` flag) and prints a digest: session id, changed files, cost, elapsed, summary.
Override with `--model <id>` only when the user names another model.

Never run raw `junie --output-format json` and read its stdout. That payload embeds the full
before/after text of every changed file and will flood the planning context. The digest plus
`git diff` is the whole interface.
</dispatch>

<review>
```bash
cd <project> && git log --oneline <BASELINE>..HEAD && git diff <BASELINE>..HEAD
```

Then run the gates yourself — tests, typecheck, lint, format — per the repo's own commands.
Junie reports having verified; verify anyway.

Judge only three things:
1. Does the done-when actually hold?
2. Did it touch files outside the order?
3. Is anything in the diff unrequested (speculative abstraction, stray refactor, new dep)?

Out-of-scope edits are the common defect. Revert them rather than arguing them into shape.
</review>

<iterate>
Correction goes back to the same session, which keeps Junie's context:

```bash
python3 ~/.claude/skills/junie-delegate/scripts/dispatch.py \
  --project <project> --session-id <id> "Correction: <what is wrong>. <what to do instead>. Keep everything else."
```

Two correction rounds maximum per order. Still wrong after two means the order was wrong, not
the model: `git reset --hard <BASELINE>`, re-split into smaller orders, dispatch fresh.
</iterate>

<parallel>
Junie edits the real working tree, so two runs in one checkout collide. For independent
orders in parallel, give each its own `git worktree` and pass its path as `--project`.
Sequential is the default; only parallelize when the orders touch disjoint files.
</parallel>

<costs>
Roughly $0.04–0.08 and 60–110s for a single-file order (measured). The digest's `cost` is
cumulative for the session, so a follow-up shows the running total, not the delta. Report the
total to the user at the end of a multi-order task.
</costs>
