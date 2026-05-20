---
name: justfile
description: "Create and manage Justfiles for project task automation and dev environments"
---

# Justfile

Create Justfiles that match the user's established conventions. Skill is grounded in official just documentation + tested patterns from 40+ projects.

<foundation>
## Foundation: Official Just Manual

This skill references the official Just documentation:
- **Root:** https://just.systems/man/en/
- **Full manual (printable):** https://just.systems/man/en/print.html
- **Key sections:** Settings, Recipe syntax, Attributes, Functions, Parameters, Dependencies, Script/shebang recipes

Skill examples and conventions below are validated against official just behavior. When in doubt, consult the official docs.
</foundation>

<workflow>
## Workflow (Skill Steps)

1. **Check filename:** MUST be `Justfile` (capital J), not `justfile`
2. Check if `Justfile` already exists in the project
3. Detect stack from package.json, pyproject.toml, Cargo.toml, etc.
4. Generate recipes matching detected stack + user conventions below
5. **Verify output:** Run `just --list` to check grouping, git branch, and formatting
</workflow>

<jj_conventions>
## JJ Conventions (Proven across 40+ projects)

### ⚠️ File Naming (CRITICAL — case-sensitive)
- **MUST be `Justfile` (capital J)** — NOT `justfile`
- Just discovers `justfile`, `Justfile`, `JUSTFILE`, `.justfile` (case-insensitive), but JJ convention is capital J
- Check: `ls -la Justfile` must exist (case-sensitive, must be capital J)

### Shell Setting
**Rule:** Set shell **IF** any of these apply:
- Project uses bun/SvelteKit → `set shell := ["zsh", "-euo", "pipefail"]`
- Project uses .env file → `set dotenv-load` (alone, no `:=`)
- Multi-line bash recipes exist → `set shell := ["bash", "-euo", "pipefail"]`
- Otherwise → omit (use default)

**Common mistake:** Declaring `set dotenv-load := false` or `set dotenv-load := true` — use bare `set dotenv-load` only.

### ⚠️ Default Recipe (CRITICAL — must be first recipe)
**Always include exactly as shown:**
```just
# List available recipes
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

**Foundation reference:** [Quick Start](https://just.systems/man/en/quick-start.html), [Mental Model](https://just.systems/man/en/)

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

**Foundation reference:** [Attributes](https://just.systems/man/en/attributes.html) (groups section)

---

## Recipe Syntax (Official Just)

### Basic form
```just
recipe-name:
  command
```

See also [Recipe Syntax](https://just.systems/man/en/features.html) in official docs.

### Comments and aliases
```just
# This is a comment
alias b := build
```

### Sigils (prefix command lines with any combo of `-`, `@`, `?`)
- `@` toggles echoing (default: echo on)
- `-` continues after non-zero exit status
- `?` (1.47.0) stops current recipe if exit code is `1`

Example:
```just
@foo:
  echo FOO

-bar:
  some-command-that-may-fail

?baz:
  [[ -f file ]] # exits 0 or 1
```

### Private recipes and no-cd
```just
[private]
secret-task:
  echo "hidden from --list"

[no-cd]
show-pwd:
  pwd  # runs in invocation dir, not justfile dir
```

**Foundation reference:** [Recipe Syntax](https://just.systems/man/en/features.html)
</jj_conventions>

<variables_expressions>
## Variables and Expressions

### Assignment and interpolation
```just
name := "value"
foo := "hello"
bar := "world"

greet:
  echo {{ foo + " " + bar }}
```

### Backticks and conditionals
```just
localhost := `hostname -I | awk '{print $1}'`

debug := if os() == "linux" { "true" } else { "false" }

serve:
  ./serve {{localhost}} 8080
```

### Built-in functions
Common functions:
- `arch()`, `os()`, `os_family()`, `num_cpus()` — system info
- `env("VAR")`, `env("VAR", "default")` — env vars
- `justfile_directory()`, `invocation_directory()` — paths
- `absolute_path(path)` — expand to absolute path

**Foundation reference:** [Functions](https://just.systems/man/en/functions.html)
</variables_expressions>

<parameters>
## Parameters and Flags

### Positional parameters
```just
build target:
  cd {{target}} && make

backup +FILES:
  scp {{FILES}} me@server.com:
```

### Optional parameters with defaults
```just
serve host="localhost" port="8000":
  python -m http.server --bind {{host}} {{port}}
```

### Named options (1.46.0+)
```just
[arg("target", long="target")]
build target:
  cargo build --target {{target}}
```

Usage:
```sh
just build --target x86_64-unknown-linux-gnu
```

**Foundation reference:** [Recipe Parameters](https://just.systems/man/en/recipe-parameters.html)

---

## Dependencies

### Prior dependencies (run before)
```just
build:
  cargo build

test: build
  cargo test
```

### Subsequent dependencies (run immediately after)
```just
a:
  echo A

b: a && c
  echo B
```

### Parallel dependencies
```just
[parallel]
run-all: task1 task2 task3
  wait
```

**Foundation reference:** [Dependencies](https://just.systems/man/en/dependencies.html)

---

## Settings

### Common settings
```just
# Shell for recipe lines and backticks
set shell := ["zsh", "-euo", "pipefail"]

# Windows-specific shell
set windows-shell := ["powershell.exe", "-c"]

# Load .env file before running recipes
set dotenv-load

# Export all variables to recipe environment
set export

# Continue on error (can override per recipe with @)
set quiet

# Pass recipe args as $1, $2, ... / $@
set positional-arguments
```

### Dotenv options
```just
set dotenv-load
set dotenv-path = ".env.local"
set dotenv-filename = ".env.custom"
set dotenv-required
set dotenv-override
```

**Foundation reference:** [Settings](https://just.systems/man/en/settings.html)

---

## Script and Shebang Recipes

### Shebang recipe (linewise by default, but body executed as a script)
```just
build:
  #!/usr/bin/env bash
  set -euxo pipefail
  cargo build
  echo "Build complete!"
```

### Script recipe with explicit interpreter
```just
[script("python3")]
process-data:
  import json
  with open('data.json') as f:
    data = json.load(f)
  print(data)
```

**Foundation reference:** [Shebang Recipes](https://just.systems/man/en/shebang-recipes.html), [Script Recipes](https://just.systems/man/en/script-recipes.html)

---

## Imports and Modules

### Import other justfiles
```just
import 'shared/common.just'

@test:
  just shared:lint
  just run-tests
```

### Modules (isolated namespaces)
```just
mod shared

@build:
  just shared::lint
  cargo build
```

**Foundation reference:** [Imports](https://just.systems/man/en/imports.html), [Modules](https://just.systems/man/en/modules.html)

---

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

---

## tmux Dev Session Recipes

For projects needing multiple processes (worker + client, frontend + backend), use tmux recipes.

Key structure:
- `_session := "name"` — short session name (3-5 chars)
- `tmux-dev` — create session with panes, open a terminal window attached
- `tmux-attach` — attach to existing session (in current shell)
- `tmux-kill` — kill session
- `tmux-restart` — kill + dev
- `tmux-logs-<pane>` — capture last 50 lines from pane
- `tmux-status` — show session and pane info
- `_attach-window` — private helper that auto-detects iTerm / Ghostty / fallback

### Terminal auto-detection (CRITICAL — do not hardcode iTerm)

`tmux-dev` must open a new window using the **user's current terminal**, not a hardcoded `osascript "iTerm"` call. Detect at runtime via `$TERM_PROGRAM`:

| Value of `$TERM_PROGRAM` | Spawn command |
|---|---|
| `iTerm.app` | `osascript -e 'tell application "iTerm" to create window with default profile command "tmux attach -t SESSION"'` |
| `ghostty` | `open -na Ghostty --args --command="tmux attach -t SESSION"` |
| `Apple_Terminal` | `osascript -e 'tell application "Terminal" to do script "tmux attach -t SESSION"'` |
| anything else | print `→ Attach manually: tmux attach -t SESSION` and exit 0 |

Also check `$TMUX` first — if already inside tmux, use `tmux switch-client -t SESSION` instead of opening a new window.

Use a shebang recipe (`#!/usr/bin/env bash`) for the dispatch — line-continuation `\` chains get unreadable fast with `case` statements.

Full template lives in `references/tmux-recipes.md`. Inline example:

```just
_session := "myapp"

[group('develop')]
tmux-dev:
    #!/usr/bin/env bash
    set -euo pipefail
    if tmux has-session -t {{_session}} 2>/dev/null; then
        echo "Session '{{_session}}' already running."
    else
        tmux new-session -d -s {{_session}} -c {{justfile_directory()}}
        tmux send-keys -t {{_session}} 'npm run dev' Enter
        tmux split-window -h -t {{_session}} -c {{justfile_directory()}}
        tmux send-keys -t {{_session}} 'npm run build:watch' Enter
        tmux select-pane -t {{_session}}:0.0
        echo "Started tmux session '{{_session}}'"
        sleep 0.5
    fi
    just _attach-window

# Open a terminal window attached to {{_session}} (auto-detects iTerm/Ghostty/Terminal)
[private]
_attach-window:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -n "${TMUX:-}" ]; then
        tmux switch-client -t {{_session}}
    elif [ "${TERM_PROGRAM:-}" = "iTerm.app" ]; then
        osascript -e 'tell application "iTerm" to create window with default profile command "tmux attach -t {{_session}}"'
    elif [ "${TERM_PROGRAM:-}" = "ghostty" ]; then
        open -na Ghostty --args --command="tmux attach -t {{_session}}"
    elif [ "${TERM_PROGRAM:-}" = "Apple_Terminal" ]; then
        osascript -e 'tell application "Terminal" to do script "tmux attach -t {{_session}}"'
    else
        echo "→ Attach manually: tmux attach -t {{_session}}"
    fi

[group('develop')]
tmux-attach:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux attach -t {{_session}}
    else
        echo "No session '{{_session}}' found. Use 'just tmux-dev' to start."
    fi

[group('develop')]
tmux-kill:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux kill-session -t {{_session}}
        echo "Killed session '{{_session}}'"
    else
        echo "No session '{{_session}}' to kill."
    fi

[group('develop')]
tmux-restart: tmux-kill tmux-dev

[group('develop')]
tmux-logs-dev:
    #!/usr/bin/env bash
    if tmux has-session -t {{_session}} 2>/dev/null; then
        tmux capture-pane -t {{_session}}:0.0 -p -S -50
    else
        echo "No session '{{_session}}' found."
    fi
```

---

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

---

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

---

## Common Mistakes & Prevention

| Mistake | Symptom | Prevention |
|---------|---------|-----------|
| **File named `justfile` (lowercase)** | Case-sensitive tools fail, inconsistent with convention | Check: `ls Justfile` must match exactly |
| **Default missing git branch** | `just` runs but doesn't show branch info | Copy default recipe exactly from conventions |
| **Recipes lack `[group(...)]`** | `just --list` is hard to scan, recipes unorganized | Add `[group('...')]` line before EVERY recipe |
| **Ungrouped recipes mixed with grouped** | Some recipes appear under headers, others float | Audit `just --list` output for any bare recipes |
| **Shell setting wrong syntax** | Recipes fail in strict mode or env vars don't load | Use bare `set dotenv-load` (no `:=`), use `set shell := [...]` for custom shells |
| **Info lines lack `@` prefix** | Output pollutes `just -q` and recipe chains | Add `@` to all `echo`, `echo ''`, logging lines |

---

## Recipe Style Guide

- **Comment above EVERY recipe:** `# Description of what this does`
- **Suppress echo with `@` for info-only/debug lines** — NOT for commands
  - ✅ `@echo "Starting..."` then `uv run ...`
  - ❌ `echo "Starting..."` then `uv run ...` (pollutes output)
- Use `{{variable}}` for interpolation (not `$var`)
- Variadic args: `*ARGS` (zero-or-more), `+ARGS` (one-or-more)
- Default params: `serve port="8765":` (with colon)
- Dependencies: `build-run *ARGS: build-frontend` (colon syntax)
- Shebang for multi-line scripts: `#!/usr/bin/env bash` or `#!/usr/bin/env zsh`
- Private/internal variables: `_prefix := "value"` (e.g., `_session := "myapp"`)
- Public variables: `name := "value"` (e.g., `port := "8765"`)

---

## Syntax Quick Reference

| Feature | Syntax |
|---------|--------|
| Variable | `name := "value"` |
| Private var | `_name := "value"` |
| Interpolation | `{{name}}` |
| Param with default | `recipe param="default":` |
| Variadic (0+) | `recipe *ARGS:` |
| Variadic (1+) | `recipe +ARGS:` |
| Dependency | `recipe: dep1 dep2` |
| Subsequent dep | `recipe: a && b` |
| **Attribute (group)** | **`[group('name')]`** |
| Silent line | `@echo "quiet"` |
| Continue on error | `-command` |
| Shebang recipe | `#!/usr/bin/env bash` |
| Script recipe | `[script("python3")]` |
| **Shell setting** | **`set shell := ["zsh", "-euo", "pipefail"]`** |
| **Dotenv** | **`set dotenv-load`** |
| Private recipe | `[private]` |
| No cd | `[no-cd]` |
| Confirm | `[confirm]` or `[confirm("message")]` |
| OS conditional | `[linux]`, `[macos]`, `[windows]`, etc. |
| Built-in | `{{justfile_directory()}}`, `{{os()}}`, etc. |

---

## Command-Line Reference (Common)

```sh
# List recipes with group organization
just --list

# Show one recipe details
just --show build

# Run a recipe
just build

# Run multiple recipes
just build test

# Interactive chooser
just --choose

# Evaluate expression or variable
just --evaluate
just --evaluate FOO

# Dump parsed justfile as JSON
just --dump --dump-format json

# Global justfile (~/.justfile)
just -g

# Generate shell completions
just --completions zsh > ~/.zsh/completions/_just
```

**Full reference:** [Command-line Options](https://just.systems/man/en/command-line-options.html)

---

## Further Reading

**Official Just Documentation:**
- Root: https://just.systems/man/en/
- Full manual: https://just.systems/man/en/print.html

**Key chapters:**
- [Quick Start](https://just.systems/man/en/quick-start.html)
- [Recipe Syntax](https://just.systems/man/en/features.html)
- [Settings](https://just.systems/man/en/settings.html)
- [Attributes](https://just.systems/man/en/attributes.html)
- [Parameters & Flags](https://just.systems/man/en/recipe-parameters.html)
- [Dependencies](https://just.systems/man/en/dependencies.html)
- [Functions](https://just.systems/man/en/functions.html)
- [Shebang Recipes](https://just.systems/man/en/shebang-recipes.html)
- [Script Recipes](https://just.systems/man/en/script-recipes.html)
- [Imports & Modules](https://just.systems/man/en/imports.html)
- [Command-line Options](https://just.systems/man/en/command-line-options.html)

</parameters>
