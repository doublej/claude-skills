# Safety — strict-mode policy and rationale

The `teams` skill is strict-safe by default. This is deliberate: a team of writers operating on the same repo without isolation is an outstanding way to lose work.

## Dirty working directory policy

**Rule**: if `git status --porcelain` is non-empty at preflight, block the spawn and ask the user via `consult-user-mcp`:

- **commit** — stage + commit with a user-supplied message, then proceed.
- **stash** — `git stash push -u` with a team-named message, proceed. Lead is responsible for popping it after shutdown (or warning the user if popping conflicts).
- **abort** — exit non-zero, no team spawned.

Why: worktrees inherit HEAD, not the working tree. Uncommitted changes stay on the main tree only. If the team edits files there too (e.g. a read-only preset that ended up touching something, or an errant hook), the user's uncommitted work is at risk of being overwritten.

## Branch policy

If the current branch matches `{main, master, production, release/*}`, `preflight.sh` issues a `consult confirm` with default=no. The user can override; the default stance is "don't spawn a team on a protected branch."

This matters most for write-capable presets, but even read-only presets create worktrees on branches like `worktree-<name>`, which can clutter a shared branch's tooling.

## Snapshot gate

Every spawn runs `snapshot.sh <team-name>`, which:

1. `git tag teams/<team-name>-snapshot <HEAD-sha>` — lightweight, not pushed.
2. Echoes the tag name so the user can `git reset --hard teams/<team-name>-snapshot` to roll back everything the team did on the main tree.
3. Tag is **not** auto-deleted by `cleanup.sh` — intentional: rollback target survives team teardown.

Snapshot is a safety floor, not a promise. Worktree changes that got merged by the lead will be undone by the reset, too — which is the point.

## Worktree gate

Presets with `write_access: true` specify `isolation: "worktree"` on every member. This is enforced in `spawn.py`: if the preset says write-capable but a member lacks `isolation`, spawn.py bails with an error.

Read-only presets (plan-committee, pr-review-squad, bug-debug-panel, research-pod, security-audit, creative-think-tank) don't need worktrees because they run in `mode: "plan"` — plan mode forbids writes regardless.

## Worktree merge flow (lead-driven)

When a writer signals task done, the lead:

1. `git -C <worktree> log main..HEAD --oneline` — confirm there are commits.
2. `git -C <worktree> diff main...HEAD --stat` — summarize scope.
3. Decide:
   - **Clean fast-forward possible** → `git merge --ff-only worktree-<name>` on main tree.
   - **Three-way merge needed** → attempt `git merge --no-ff worktree-<name>`. If conflicts, do not resolve. Escalate via consult (resolve-here / leave-for-user / abort).
   - **User wants to resolve** → pause the team, notify user, wait for them to finish before shutting down.

Never force-merge. Never `git merge -X theirs` / `-X ours` without explicit user consent.

## Hook gate

Installed automatically into `~/.claude/settings.json` by `scripts/install.sh`:

- `PreToolUse: Agent` → `~/.claude/hooks/teams/preflight-agent.sh`. Re-checks dirty WD immediately before `Agent()` fires; exit 2 blocks. Catches the window between preflight and actual spawn.
- `TaskCreated` → `task-created.sh`. Enforces every new team task has `owner` and either `blockedBy` set or a deadline in metadata. Exit 2 blocks creation otherwise.
- `TaskCompleted` → `task-completed.sh`. Runs `git status --porcelain` inside the completing member's worktree. Exit 2 if non-empty unless task metadata sets `leave_dirty: true`.
- `TeammateIdle` → `teammate-idle.sh`. Default no-op; preset-aware extensions (enforce_verdict, enforce_severity).

Exit code contract: 0 = allow, 1 = allow with warning to lead, 2 = block and send feedback to lead. Anything else is treated as 0 with a stderr warning.

## Rollback recipe

If a spawn goes sideways and you need to undo:

```bash
# 1. Shut down cleanly
bash ~/.claude/skills/teams/scripts/shutdown.sh <team-name>

# 2. Prune worktrees (doesn't touch main tree)
bash ~/.claude/skills/teams/scripts/cleanup.sh <team-name>

# 3. Roll main tree back to pre-spawn state
git reset --hard teams/<team-name>-snapshot

# 4. (optional) delete the snapshot tag once you're sure
git tag -d teams/<team-name>-snapshot
```

`cleanup.sh` intentionally leaves the snapshot tag; the user decides when to drop it.

## What is NOT protected

- Uncommitted staged changes at the time of a teammate's first `SendMessage` — only preflight catches dirty-WD; after the team starts, the lead is responsible.
- Remote branches — nothing here pushes, but a teammate that opts to push (e.g. via a hook or an ad-hoc `git push`) is not blocked.
- Lockfiles on shared resources (DBs, queue workers) — worktrees don't isolate those.

Callers who push through these edges should add their own hooks, not weaken this skill's defaults.
