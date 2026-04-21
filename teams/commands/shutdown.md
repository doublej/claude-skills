---
description: Graceful shutdown of a team. Sends shutdown_request to every member, waits for ACK, then TeamDelete. Args - <team-name>.
allowed-tools: Bash, SendMessage, TeamDelete
---

Shut down a team.

Argument: `<team-name>`. If empty, first run `/teams:status` and ask the user which team to shut down.

Execute the script to print the sequence:

```bash
bash ~/.claude/skills/teams/scripts/shutdown.sh $ARGUMENTS
```

The script lists the exact `SendMessage` + `TeamDelete` calls. Execute them in order. Wait for each `shutdown_response` before proceeding. After `TeamDelete`, also run:

```bash
bash ~/.claude/skills/teams/scripts/cleanup.sh $ARGUMENTS
```

to prune worktrees.
