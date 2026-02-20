---
name: full-optimize
description: >
  Zero-input project optimizer. Chains analysis, simplification, docs audit, verification, and
  smart commits into a single automated pipeline. Use when user says "optimize the project",
  "clean up everything", "full optimize", or invokes /full-optimize with no arguments.
---

# Full Optimize

Orchestrate a full optimization pipeline on the current project. No user input needed — auto-detect and go.

## Pipeline

Run phases in order. Skip phases that don't apply.

### Phase 1 — Discover (parallel, read-only)

Invoke these three skills concurrently via subagents:

1. **`codebase-mapper`** — map structure, rank files by importance
2. **`repomap-analyzer`** — find deprecated patterns, dead code, duplicates, mixed conventions
3. **`dev-refactor`** — analyse against language/framework standards; identify architecture gaps

After all three return, synthesise findings into a **ranked hit list**:
- Group by: Dead code · Complexity · Pattern violations · Doc rot
- Sort by impact (highest first)
- Present to user as a brief table before touching anything

### Phase 2 — Simplify (conditional)

If repomap or dev-refactor flagged complexity issues (files >150 lines, nested logic, duplicates):
→ Invoke **`codebase-simplify`**

Skip if codebase is already lean (< 5 files flagged).

### Phase 3 — Docs Audit (conditional)

If the project has any of: `README.md`, `docs/`, `CHANGELOG.md`, JSDoc, docstrings:
→ Invoke **`audit-docs`**

Skip if no documentation exists.

### Phase 4 — Verify

→ Invoke **`verify`**

If verify fails: fix issues (up to 3 cycles). Do NOT proceed to Phase 5 until green.

### Phase 5 — Commit

→ Invoke **`smart-commit`**

Produces atomic commits per logical change group.

## Auto-Detection

Detect project type from root files:

| File found | Project type |
|---|---|
| `package.json` | Node/TypeScript |
| `pyproject.toml` / `setup.py` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `Package.swift` | Swift |
| `*.sln` / `*.csproj` | C# |

Use this to calibrate what `dev-refactor` and `verify` should focus on.

## Output Format

After the pipeline completes, summarise:

```
## Full Optimize — Complete

### What was found
- [N] dead code blocks removed
- [N] files simplified
- [N] doc issues fixed

### Commits created
- [list smart-commit output]

### Skipped
- [any phases skipped + reason]
```
