---
name: justfile
description: "Create and manage Justfiles for project task automation and dev environments"
---

# Justfile

Create Justfiles that match the user's established conventions. Detect project stack and generate appropriate recipes.

## Workflow

1. **Check filename:** MUST be `Justfile` (capital J), not `justfile`
2. Check if `Justfile` already exists in the project
3. Detect stack from package.json, pyproject.toml, Cargo.toml, etc.
4. Generate recipes matching detected stack + user conventions below
5. **Verify output:** Run `just --list` to check grouping, git branch, and formatting

## Conventions (from user's projects)

### ⚠️ File naming (CRITICAL — mistakes here are persistent)
- **MUST be `Justfile` (capital J)** — NOT `justfile`
- This is case-sensitive and Unix convention
- Check: `ls -la Justfile` must exist (not `justfile`)

### Shell setting
**Rule:** Set shell **IF** any of these apply:
- Project uses bun/SvelteKit → `set shell := ["zsh", "-euo", "pipefail"]`
- Project uses .env file → `set dotenv-load` (alone, no `:=`)
- Multi-line bash recipes exist → `set shell := ["bash", "-euo", "pipefail"]`
- Otherwise → omit (use default)

**Common mistake:** Declaring `set dotenv-load := false` or `set dotenv-load := true` — use bare `set dotenv-load` only.

### ⚠️ Default recipe (CRITICAL — must be first recipe)
**Always include exactly as shown:**
```just
default:
    @just --list
    @echo ''
    @echo "branch: $(git branch --show-current 2>/dev/null || echo 'n/a')"
```
**Mistakes to avoid:**
- ❌ Missing the `@echo "branch: ..."` line
- ❌ Placing default somewhere other than first
- ❌ Just `@just --list` without branch output
- ✅ Three lines: list, blank echo, branch echo

### ⚠️ Groups (CRITICAL — every recipe must have one)
**Rule:** Every recipe MUST have a `[group('name')]` attribute immediately before it.
**Standard groups:**
- `setup` — install, init, deps
- `develop` — dev, preview, run, sync, tmux-*
- `quality` — lint, typecheck, test, check, loc-check, format
- `build` — build
- `deploy` — deploy, cf-deploy, push
- `cleanup` — clean

**Common mistake:** Some recipes grouped, others bare → creates confusing `just --list` output
**Check:** `just --list` should show recipes organized under group headers, NO ungrouped recipes

### Variable naming
- Private/internal variables: `_prefix := "value"` (e.g., `_session := "myapp"`)
- Public variables: `name := "value"` (e.g., `port := "8765"`)
- Avoid public config unless it's meant to be overridden

### ⚠️ Recipe style
- **Comment above EVERY recipe:** `# Description of what this does`
- **Suppress echo with `@` for info-only/debug lines** — NOT for commands
  - ✅ `@echo "Starting..."` then `uv run ...`
  - ❌ `echo "Starting..."` then `uv run ...` (pollutes output)
- Use `{{variable}}` for interpolation (not `$var`)
- Variadic args: `*ARGS` (zero-or-more), `+ARGS` (one-or-more)
- Default params: `serve port="8765":` (with colon)
- Dependencies: `build-run *ARGS: build-frontend` (colon syntax)
- Shebang for multi-line scripts: `#!/usr/bin/env bash` or `#!/usr/bin/env zsh`

## Stack-Specific Recipes

### Bun / SvelteKit
```just
set shell := ["zsh", "-euo", "pipefail"]

# List available recipes
default:
    @just --list
    @echo ''
    @echo "branch: $(git branch --show-current 2>/dev/null || echo 'n/a')"

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
set dotenv-load

# List available recipes
default:
    @just --list
    @echo ''
    @echo "branch: $(git branch --show-current 2>/dev/null || echo 'n/a')"

[group('setup')]
install:
    uv sync

[group('develop')]
dev:
    uv run python main.py --dev

[group('quality')]
test *ARGS:
    uv run pytest {{ARGS}}

[group('quality')]
lint:
    uv run ruff check --fix .
    uv run ruff format .

[group('quality')]
check:
    @echo '→ Running lint...'
    just lint
    @echo '→ Running tests...'
    just test

[group('cleanup')]
clean:
    rm -rf build/ dist/ *.egg-info .coverage htmlcov/ .pytest_cache/
    find . -type d -name __pycache__ -exec rm -rf {} +
```

### Node / npm
```just
# List available recipes
default:
    @just --list
    @echo ''
    @echo "branch: $(git branch --show-current 2>/dev/null || echo 'n/a')"

[group('setup')]
install:
    npm install

[group('develop')]
dev:
    npm run dev

[group('build')]
build:
    npm run build

[group('quality')]
test:
    npm run test

[group('quality')]
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

## Verification Checklist (after generating Justfile)

**Before considering the Justfile complete, verify ALL of these:**

```bash
# 1. File exists with capital J
ls -la Justfile  # must exist, not justfile

# 2. List recipes with clear grouping
just --list  # should show:
  #   setup
  #   ├─ install
  #   develop
  #   ├─ dev
  #   ...
  # (all recipes grouped, no ungrouped recipes)

# 3. Default recipe outputs git branch
just  # output should include "branch: <current-branch>"

# 4. Test one recipe to ensure no echo pollution
just <recipe>  # should only output what's needed, not debug lines
```

**Fail conditions (don't mark as done if any of these are true):**
- ❌ File named `justfile` (lowercase)
- ❌ `just --list` shows ungrouped recipes (recipes without `[group(...)]`)
- ❌ Default recipe missing git branch output
- ❌ Shell setting declares `set dotenv-load := false` (should be bare `set dotenv-load`)
- ❌ Info-only lines (echo, logs) don't have `@` prefix

## Common Mistakes & Prevention

| Mistake | Symptom | Prevention |
|---------|---------|-----------|
| **File named `justfile` (lowercase)** | Case-sensitive tools fail, inconsistent with convention | Check: `ls Justfile` must match exactly |
| **Default missing git branch** | `just` runs but doesn't show branch info | Copy default recipe exactly from conventions |
| **Recipes lack `[group(...)]`** | `just --list` is hard to scan, recipes unorganized | Add `[group('...')]` line before EVERY recipe |
| **Ungrouped recipes mixed with grouped** | Some recipes appear under headers, others float | Audit `just --list` output for any bare recipes |
| **Shell setting wrong syntax** | Recipes fail in strict mode or env vars don't load | Use bare `set dotenv-load` (no `:=`), use `set shell := [...]` for custom shells |
| **Info lines lack `@` prefix** | Output pollutes `just -q` and recipe chains | Add `@` to all `echo`, `echo ''`, logging lines |

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
| **Attribute (group)** | **`[group('name')]`** |
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
