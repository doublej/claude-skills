---
name: git
description: Git workflow management — branching strategies, hooks, repo organization, CI/CD integration, semantic versioning. Use when asked to set up or improve git workflows, configure hooks, organize repos, plan releases, or establish team conventions.
---

# Git Workflow Manager

Provide simple, effective version control and repository organization. Prefer the simplest strategy that fits the team size and project complexity. Always offer a rollback path for workflow changes.

## Branching Strategies

Choose based on team size and release cadence:

| Strategy | Best for | Key rule |
|----------|----------|----------|
| Trunk-based | Small teams, CI/CD | Short-lived branches, merge daily |
| GitHub Flow | Web apps, frequent deploy | `main` always deployable, feature branches |
| GitFlow | Versioned releases | `main` + `develop` + `feature/` + `release/` + `hotfix/` |

Branch naming: `type/short-description` — e.g. `feat/user-auth`, `fix/null-pointer`, `chore/update-deps`.

## Git Hooks

Prefer `pre-commit` framework or simple shell scripts. Committed hooks live in `scripts/hooks/`, activated via `git config core.hooksPath scripts/hooks`.

Common hooks:

```bash
# pre-commit: lint + typecheck
#!/bin/sh
npm run lint && npm run typecheck

# commit-msg: enforce format
#!/bin/sh
grep -qE '^(feat|fix|chore|docs|refactor|test|ci): .+' "$1" || {
  echo "Bad commit message. Use: type: description"
  exit 1
}

# pre-push: run tests
#!/bin/sh
npm test
```

## Repository Organization

```
project/
├── src/
├── scripts/
│   └── hooks/        # shared git hooks
├── .gitignore
├── .github/
│   ├── workflows/    # CI/CD
│   └── pull_request_template.md
└── CHANGELOG.md
```

`.gitignore` essentials: `node_modules/`, `dist/`, `.env`, `*.log`, `.DS_Store`, `Thumbs.db`.

## Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

- `PATCH`: backwards-compatible bug fix
- `MINOR`: new backwards-compatible feature
- `MAJOR`: breaking change

Tag: `git tag -a v1.4.2 -m "release: v1.4.2" && git push --tags`

Automate with `standard-version` or `semantic-release` when using conventional commits.

## Conventional Commits

Format: `type(scope): description`

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`, `perf`

Breaking change: add `!` — `feat!: redesign API` or footer `BREAKING CHANGE: ...`

## CI/CD Integration

- Run lint + tests on every PR, block merge on failure
- Deploy only from tags or `main`
- Keep secrets in CI environment variables, never in repo

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run lint && npm test
```

## Monorepo Patterns

- JS/TS: `pnpm workspaces` or `turborepo`
- One `.gitignore` at root, supplemented per package
- Tag releases per package: `pkg-name@1.2.0`
- Use path filters in CI to avoid unnecessary job runs

## Rollback Reference

| Scenario | Command |
|----------|---------|
| Undo last commit, keep changes | `git reset --soft HEAD~1` |
| Undo last commit, discard | `git reset --hard HEAD~1` |
| Revert pushed commit safely | `git revert <sha>` |
| Recover deleted branch | `git reflog` then `git checkout -b name <sha>` |
| Undo a merge | `git revert -m 1 <merge-sha>` |
