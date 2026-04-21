---
description: Prune a team's worktrees, branches, and leftover team dir. Keeps the snapshot tag. Args - <team-name>.
allowed-tools: Bash
---

Clean up a team's filesystem footprint.

Argument: `<team-name>`.

```bash
bash ~/.claude/skills/teams/scripts/cleanup.sh $ARGUMENTS
```

The script:

- Removes `.claude/worktrees/<name>/` for each member (asks via consult if any is dirty).
- Deletes merged worktree branches.
- Removes `~/.claude/teams/<team-name>/` if still present.
- Preserves the `teams/<team-name>-snapshot` tag so rollback remains possible.

Surface the snapshot tag name in the response so the user knows rollback is available.
