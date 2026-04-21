---
description: Verify the repo + env are ready to spawn a teams skill agent team (env flag, git clean, branch OK, no orphans).
allowed-tools: Bash
---

Run the teams preflight check:

```bash
bash ~/.claude/skills/teams/scripts/preflight.sh
```

Report the exit code back to the user. Non-zero means the user needs to resolve something before spawning a team.
