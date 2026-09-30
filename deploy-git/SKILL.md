---
name: deploy-git
description: Git protocol when a commit or push exists only to deploy — temporary worktree, deploy/<target> branch, deploy: commits, no merge back. Use when deploying via git rather than developing.
---

# Deployment git protocol

<presentation>
Open the first response with the banner (once), close the deploy with the report:
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   DEPLOY GIT                                                 ║
║   Deploy-only commits from a temporary worktree              ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

DEPLOY GIT  ──  <target>   ref: <deploy/target|existing sha>   force: <no|asked>

REPO              COMMIT      CHECKS   PUSHED   WORKTREE
────────────────────────────────────────────────────────────
<repo>            <sha|—>     <✓|✗>    <✓|✗>    <removed|kept: why>

github.com/doublej
```
</presentation>

When Git is only required to deploy:

- Prefer pushing an existing commit.
- Use a temporary worktree and `deploy/<target>` branch for generated files, config, or trigger commits.
- Commit only deployment-related changes with `deploy: desc`.
- Run deployment-relevant checks.
- Push only the required deployment ref.
- Do not merge deployment-only commits back.
- Do not disturb unrelated local changes.
- Clean up the temporary branch and worktree afterward.
- Ask before force-pushing or changing a protected/shared branch.
