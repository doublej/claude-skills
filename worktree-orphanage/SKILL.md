---
name: worktree-orphanage
description: "Scan all git worktrees for orphaned (unmerged) work against main/develop or given target branches; summarize, estimate progress and importance, and recommend merge/finish/archive per worktree. Use when the user runs /worktree-orphanage, asks 'what's in my worktrees', 'unmerged worktree work', 'stale worktrees', or 'which worktrees can I delete'."
---

<arguments>
`/worktree-orphanage [target-branch...] [--yes]`

- `target-branch...` — merge targets to check against. Default: auto-detect
  main, master, develop (every one that exists locally or on origin).
- `--yes` / `-y` — skip the phase-2 confirmation gate, go straight to the
  detailed report.
</arguments>

<phase_1_scan>
Cheap and deterministic — one script, git plumbing only, no file reads, no
agents, no session-search.

Run from the repo (pass any target-branch args through):

```bash
<skill-dir>/scripts/scan.sh [target-branch...]
```

If cwd is not a repo (script exits 2 with `NOT_A_REPO`): scan immediate
subdirectories for git repos, run the script in each that has extra
worktrees, and tell the user you did so.

The script buckets each worktree's ahead-of-target commits with three
defenses against false "unmerged" verdicts — plain `target..HEAD` overcounts
because cherry-picked and squash-merged work has different shas:

1. **cherry** — patch-id identical commit exists in target (`git cherry`)
2. **absorbed** — the diff is already present in target's tree
   (reverse-apply check; catches squash merges, edited cherry-picks, and
   whole-branch squashes via the cumulative branch diff)
3. **unmerged** — genuinely absent from target

Classes (a worktree is judged against ALL targets):
- **clean** — nothing ahead, nothing dirty
- **likely-merged** — ahead by shas, but every commit is cherry/absorbed and
  the tree is clean; an educated guess, present it as such
- **orphaned** — genuinely unmerged commits vs any target, and/or dirty tree
- **detached / broken** — detached HEAD, prunable, or missing directory

Columns with `,`-separated values follow the target order printed in AHEAD.
</phase_1_scan>

<phase_2_gate>
Render the script's TSV as a one-screen markdown table (shorten paths to
`~`-relative). Then:

- All worktrees clean or likely-merged with zero unmerged/dirty → report
  that, note likely-merged ones can probably be deleted after a quick eyeball
  (`git log <target>..<branch>`), and stop. Never ask.
- `--yes` passed → go straight to phase 3.
- Otherwise ask ONE confirm question via consult-user-mcp `ask`:
  "N worktrees have unmerged work. Spend tokens on a detailed report
  (session history + progress estimate)?" — body: phase 3 reads git logs and
  searches past Claude sessions per worktree to reconstruct intent and
  estimate progress/importance.
- Declined or cancelled → the summary table IS the deliverable; stop.
</phase_2_gate>

<phase_3_report>
Orphaned worktrees only. Per worktree:

1. `git log --stat <target>..HEAD` (never full diffs) + the dirty-file list
   → infer what the work is.
2. Run the `session-search` skill scoped to the worktree's path/branch →
   original intent and where the last session left off. Nothing found → say
   "no session history found" and estimate from git evidence alone; never
   fabricate intent.
3. Estimate, explicitly labeled as estimates:
   - **What it is** — one sentence
   - **Progress** — rough % complete + what remains (intent vs. diff state)
   - **Importance** — high/medium/low + one line of justification (commit
     substance, session intent, recency)
   - **Recommended action** — merge / finish (include the resume command) /
     archive / delete

3+ orphaned worktrees → parallelize per-worktree analysis via subagents;
conclusions come back, not raw logs.

Final output: ranked most-important-first — summary table on top,
per-worktree detail below, full worktree paths bundled at the bottom.
</phase_3_report>

<constraints>
- Read-only: never merge, rebase, prune, delete, or stash — only recommend.
- Phase 1 = the script, nothing else.
- "likely-merged" and all phase-3 numbers are educated guesses — label them.
- No caching, config files, or report persistence.
</constraints>
