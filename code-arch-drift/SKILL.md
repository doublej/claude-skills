---
name: code-arch-drift
description: "Detect architectural drift — layer/dependency boundaries eroding as code is added (UI importing the DB directly, controllers reaching into repositories, forbidden cross-module deps, cycles). Rules live in a CLAUDE.md ## Architecture block; a stdlib-only checker parses imports and reports violations. Run on-demand to audit a repo, or wire as a Claude Code hook for in-session correction. Python, JS/TS, Go, Rust, Swift. Use on 'architecture drift', 'check layering', 'boundary violations', 'are we leaking layers', '/code-arch-drift'."
---

# code-arch-drift

Catch architectural drift: the slow erosion of layer and dependency boundaries
as code accretes. The rules you already keep in your head ("the UI never touches
the database", "services depend on repos, not the other way round") become
executable checks. **No LLM in the hot path** — the checker is deterministic
import-graph matching. Part of the `code-*` family (see Related skills).

## When to use

- Auditing a repo for boundary violations before a refactor or release
- Wiring an in-session guardrail so edits that cross a layer get flagged immediately
- Turning tribal "you shouldn't import that" knowledge into a CI gate

## The blueprint

Rules live in an `## Architecture` section of `CLAUDE.md` (or `ARCHITECTURE.md` /
`SPEC.md` — first found wins), inside a fenced `arch` block:

````markdown
## Architecture

Layered: routes → services → repos → models. UI never touches the DB.

```arch
layer routes   = src/routes/**, src/api/**
layer services = src/services/**
layer repos    = src/repos/**
layer models   = src/models/**
layer ui       = src/ui/**, src/components/**

routes   -> services
services -> repos
repos    -> models
ui       -> services

forbid ui -> repos
forbid ui -> models
forbid * -> src/legacy/**
```
````

Grammar (one statement per line, `#` for comments):

| Statement                      | Meaning                                          |
|--------------------------------|--------------------------------------------------|
| `layer NAME = glob, glob, ...` | Define a layer by file globs.                    |
| `X -> Y`                       | `X` may depend on `Y`.                           |
| `forbid X -> Y`                | Prohibition (overrides any allow).               |
| `forbid * -> path/glob/**`     | Anything importing `path/...` is forbidden.      |

Default posture: if a layer `X` has any `X -> ...` allow rules, edges from `X`
not covered by an allow are **drift**. Layers with no allow rules are
unconstrained (define them only when you want to constrain them). External
imports (npm/pip/stdlib) are ignored — only intra-repo edges are checked.

## Workflow

1. **No blueprint yet?** Don't invent one. Map the directory structure, propose a
   layer/rule set to the user, and write it into the `## Architecture` block. The
   human owns the rules; you only draft them.
2. **Run the checker** (deterministic, no API cost):

   ```bash
   python3 scripts/archcheck.py --root <repo>            # human-readable report
   python3 scripts/archcheck.py --root <repo> --json     # machine-readable
   python3 scripts/archcheck.py --root <repo> --rules path/to/CLAUDE.md
   ```

3. **Read the report.** Each violation is `severity  src_file [layer] -> target [layer]  (rule)`.
   Severities: `forbidden` (explicit `forbid` hit), `layer` (no allow covers the edge),
   `cycle` (import cycle between layers).
4. **Fix or refine.** A violation is either real drift (fix the import) or a missing
   rule (the boundary was legitimate — add the allow). Decide with the user; don't
   silently relax rules to make the checker pass.

## As a Claude Code hook (optional, in-session guardrail)

Wire the checker into `~/.claude/settings.json` so drift surfaces while editing.
See `references/hook-setup.md` for `PostToolUse` (Write/Edit) and `Stop`
checkpoint configuration, including lenient (advisory) vs strict (block) modes.

## CI gate (optional)

`archcheck.py` exits non-zero when violations exist, so it drops into CI as-is:

```bash
python3 scripts/archcheck.py --root . || exit 1
```

For deterministic regex-rule enforcement across many languages without this
checker, `npx @rickheere/archtest` is a good standalone alternative — see
`references/hook-setup.md`.

## Related skills

- **code-map** — importance-ranked repo map to discover what the layers *should* be before writing rules.
- **code-audit** — call-graph quality audit (dead code, dupes); complements boundary checks.
- **code-refactor** — once drift is found, generate the refactor tasks to fix it.
- **claude-md-tree** — where the `## Architecture` blueprint lives in a multi-package tree.
