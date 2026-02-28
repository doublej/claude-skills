---
name: justfile
description: Create and manage Justfiles for project task automation. Use when setting up a new project's task runner, adding recipes to an existing Justfile, or creating tmux-based dev environments with Just.
---

# Justfile

Create Justfiles that match the user's established conventions. Detect project stack and generate appropriate recipes.

## Workflow

1. Check if `Justfile` or `justfile` already exists in the project
2. Detect stack from package.json, pyproject.toml, Cargo.toml, etc.
3. Generate recipes matching detected stack + user conventions below
4. Run `just --list` to verify

## Conventions (from user's projects)

### File naming
- Use `Justfile` (capital J) for new files

### Shell setting
- SvelteKit/bun projects: `set shell := ["zsh", "-euo", "pipefail"]`
- Python/uv projects: `set dotenv-load` when .env is used
- Simpler projects: omit shell setting (use default)

### Default recipe
Always include as first recipe:
```just
default:
    @just --list
    @echo ''
    @echo "branch: $(git branch --show-current 2>/dev/null || echo 'n/a')"
```

### Groups
Use `[group('name')]` to organise recipes. Standard groups:
- `setup` — install, init
- `develop` — dev, preview, sync
- `quality` — lint, typecheck, test, check, loc-check
- `build` — build
- `deploy` — deploy, cf-deploy
- `cleanup` — clean

### Variable naming
- Private/internal variables: `_prefix := "value"`
- Public variables: `name := "value"`

### Recipe style
- Comments above every recipe: `# Description of what this does`
- Suppress echo with `@` for info-only lines
- Use `{{variable}}` interpolation
- Variadic args: `*ARGS` (zero-or-more), `+ARGS` (one-or-more)
- Default params: `serve port="8765":`
- Dependencies: `build-run *ARGS: build-frontend`
- Shebang for multi-line logic: `#!/usr/bin/env bash` or `#!/usr/bin/env zsh`

## Stack-Specific Recipes

### Bun / SvelteKit
```just
[group('setup')]
install:
    bun install

[group('develop')]
dev:
    bun run dev

[group('develop')]
preview:
    bun run preview

[group('quality')]
lint:
    bun run lint

[group('quality')]
lint-fix:
    bun run lint:fix

[group('quality')]
typecheck:
    bun run check

[group('quality')]
test:
    bun run test

[group('quality')]
check:
    @echo '→ Running lint...'
    just lint
    @echo '→ Running typecheck...'
    just typecheck
    @echo '→ Running tests...'
    just test

[group('build')]
build:
    bun run build

[group('cleanup')]
clean:
    rm -rf .svelte-kit/ build/ node_modules/.cache/
```

### Python / uv
```just
install:
    uv sync

dev:
    uv run python main.py --dev

test *ARGS:
    uv run pytest {{ARGS}}

lint:
    uv run ruff check --fix .
    uv run ruff format .

check: lint test

clean:
    rm -rf build/ dist/ *.egg-info .coverage htmlcov/ .pytest_cache/
    find . -type d -name __pycache__ -exec rm -rf {} +
```

### Node / npm
```just
install:
    npm install

dev:
    npm run dev

build:
    npm run build

test:
    npm run test

lint:
    npm run lint
```

## tmux Dev Session Recipes

For projects needing multiple processes (worker + client, frontend + backend), use tmux recipes. See `references/tmux-recipes.md` for the full pattern.

Key structure:
- `_session := "name"` — short session name (3-5 chars)
- `tmux-dev` — create session with panes, open iTerm
- `tmux-attach` — attach to existing session
- `tmux-kill` — kill session
- `tmux-restart` — kill + dev
- `tmux-logs-<pane>` — capture last 50 lines from pane
- `tmux-status` — show session and pane info

## loc-check Recipe

For projects with line-length conventions (from CLAUDE.md `code_caps`):
```just
[group('quality')]
loc-check:
    #!/usr/bin/env zsh
    setopt null_glob
    err=0
    for f in src/**/*.ts src/**/*.svelte; do
        lines=$(wc -l < "$f")
        if (( lines > 400 )); then echo "error: $f ($lines lines, max 400)"; err=1
        elif (( lines > 300 )); then echo "warn: $f ($lines lines, target ≤300)"; fi
    done
    exit $err
```
Adjust glob patterns and thresholds per project.

## Syntax Quick Reference

| Feature | Syntax |
|---------|--------|
| Variable | `name := "value"` |
| Private var | `_name := "value"` |
| Interpolation | `{{name}}` |
| Param with default | `recipe param="default":` |
| Variadic (0+) | `recipe *ARGS:` |
| Variadic (1+) | `recipe +ARGS:` |
| Env export param | `recipe $param:` |
| Dependency | `recipe: dep1 dep2` |
| Dep with args | `recipe: (dep1 "arg")` |
| Attribute | `[group('name')]` |
| Multiple attrs | `[no-cd, private]` |
| Silent line | `@echo "quiet"` |
| Shebang recipe | `#!/usr/bin/env bash` |
| Shell setting | `set shell := ["zsh", "-euo", "pipefail"]` |
| Dotenv | `set dotenv-load` |
| Quiet global | `set quiet` |
| Built-in dir | `{{justfile_directory()}}` |
| OS conditional | `[macos]` / `[linux]` / `[unix]` / `[windows]` |
| Confirm before run | `[confirm]` or `[confirm("Are you sure?")]` |
| Script recipe | `[script]` |
| Doc override | `[doc("Custom help text")]` |
