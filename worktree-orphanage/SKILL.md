---
name: worktree-orphanage
description: "Scan all git worktrees for orphaned (unmerged) work against main/develop or given target branches; summarize, estimate progress and importance, and recommend merge/finish/archive per worktree. Read-only: it reports and prints removal commands, never removes, prunes or merges anything itself. Use when the user runs /worktree-orphanage, asks 'what's in my worktrees', 'unmerged worktree work', 'stale worktrees', or 'which worktrees can I delete'."
---

<arguments>
`/worktree-orphanage [target-branch...] [--branches] [--yes]`

- `target-branch...` — merge targets to check against. Default: auto-detect
  main, master, develop (every one that exists locally or on origin) plus
  the branch the main worktree has checked out (the line the project
  actually integrates on, e.g. `feature/cloudflare`).
- `--branches` / `-b` — also scan local branches that aren't checked out in
  any worktree folder (shown as `(no worktree)` rows). Pass it through to
  the script.
- `--yes` / `-y` — skip the phase-2 confirmation gate, go straight to the
  detailed report.
</arguments>

<presentation>
Print once, first thing in the response:
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   WORKTREE ORPHANAGE                                         ║
║   Unmerged worktree work finder                              ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
The phase-2 summary table and the phase-3 summary table take this shape (ranked most-important-first in phase 3; per-worktree detail and full paths follow as prose):

```
WORKTREE ORPHANAGE  ──  <repo>   targets: <main,develop>   orphaned: <n>/<total>

WORKTREE    BRANCH     AHEAD      CHERRY   ABSORBED   UNMERGED   DIRTY   STASH   LAST_ACTIVITY   CLASS     ACTION
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
<~/path>    <branch>   <t:n,…>    <n|—>    <n|—>      <n|—>      <n|—>   <n|—>   <date>          <class>   <merge|finish|archive|delete|—>

github.com/doublej
```
</presentation>

<phase_1_scan>
Cheap and deterministic — one script, git plumbing only, no file reads, no
agents, no session-search.

Run from the repo (pass any target-branch args through):

```bash
<skill-dir>/scripts/scan.sh [--branches] [target-branch...]
```

The script is the whole of phase 1: no `find`, `git worktree list` or `du`
of your own before or instead of it. Script missing or erroring → report
the error and stop; never improvise a replacement.

Scope is the repo at cwd, even when it contains nested repos. Sweep
several repos only when cwd is not a repo (`NOT_A_REPO`) or the user
explicitly asks for a folder / all repos — then run the script once per
repo root and tell the user you did so:

```bash
find <dir> -maxdepth 3 -type d -name .git -not -path '*/node_modules/*' | while read -r g; do
  d=${g%/.git}; [ "$(git -C "$d" worktree list | wc -l)" -gt 1 ] && (cd "$d" && <skill-dir>/scripts/scan.sh [args])
done
```

The script buckets each worktree's ahead-of-target commits with three
defenses against false "unmerged" verdicts — plain `target..HEAD` overcounts
because cherry-picked and squash-merged work has different shas:

1. **cherry** — patch-id identical commit exists in target (`git cherry`)
2. **absorbed** — the diff is already present in target's tree
   (reverse-apply check; catches squash merges, edited cherry-picks, and
   whole-branch squashes via the cumulative branch diff)
3. **unmerged** — genuinely absent from target

Classes (work that landed in ANY one target counts as landed — in
branch-flow repos main may trail develop, and that alone is not orphaned):
- **clean** — not ahead of at least one target, nothing dirty
- **likely-merged** — ahead by shas, but every commit is cherry/absorbed in
  some target and the tree is clean; an educated guess, present it as such
- **orphaned** — unmerged commits vs every target, and/or dirty tree
- **detached / broken** — detached HEAD, prunable, or missing directory

Columns with `,`-separated values follow the target order printed in AHEAD.
</phase_1_scan>

<phase_2_gate>
Mandatory stop. Phase 3 never starts without a "yes" from this gate or an
explicit `--yes`; running autonomously is not a yes.

Render the script's TSV as the one-screen `<presentation>` report table (shorten paths to
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
- Declined, cancelled, AFK, or no consult-user-mcp → the summary table IS
  the deliverable; stop.
</phase_2_gate>

<phase_3_report>
Orphaned worktrees only. Per worktree:

1. `git log --stat <target>..HEAD` (never full diffs) + the dirty-file list
   → infer what the work is.
2. Invoke the `session-search` skill (Skill tool) before writing any
   estimate: `search "<branch>"` with `-p <worktree path>`, widening to
   `--folder <repo parent>` if empty → original intent and where the last
   session left off. Nothing found → say
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
  Recommended deletions end the report as a copy-paste block
  (`git worktree remove <path>` / `git branch -d <branch>`) for the user to
  run. A later "clean them up" is a new task outside this skill: run only
  the exact list the user confirms, never `--force` and never on an
  orphaned or dirty worktree.
- Phase 1 = the script, nothing else.
- "likely-merged" and all phase-3 numbers are educated guesses — label them.
- No caching, config files, or report persistence.
</constraints>
