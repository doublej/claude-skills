---
name: code-optimize
description: "Throw-at-a-codebase optimizer: one entry point that fans out over selectable dimensions (structure, claude-md, smells, simplify, modularize, logging, arch, glossary, docs), each following scan → plan → fix → verify → atomic commit. Replaces full-optimize, code-refactor, and code-simplify. Use this dispatcher for whole-codebase cleanup; invoke a dimension skill (code-audit, code-logging, …) directly only when the user wants exactly one dimension. Triggers on '/code-optimize', 'optimize this codebase', 'full optimize', 'clean up everything', 'refactor the codebase', 'simplify the codebase'."
---

# Code Optimize

One entry point to optimize a whole codebase. The user picks dimensions as
arguments (`/code-optimize smells logging`); zero arguments = all dimensions.
Each dimension follows the same contract — scan with JSON output, plan, fix,
verify, commit atomically — and delegates to a dimension skill or a bundled
reference.

<dimension_registry>

| Dimension | Owner | Scan command |
|---|---|---|
| `structure` | this skill — `references/structure.md` | `python3 ~/.claude/skills/code-optimize/scripts/scan_codebase.py <root> --json` |
| `claude-md` | **claude-md-tree** skill | skill's own audit workflow (no scan script) |
| `smells` | **code-audit** skill | `python3 ~/.claude/skills/code-audit/analyze.py <root> --output /tmp/code-optimize/smells.md` |
| `simplify` | this skill — `references/simplify.md` | `python3 ~/.claude/skills/code-optimize/scripts/scan_codebase.py <root> --json` |
| `modularize` | **code-modularize** skill | `python3 ~/.claude/skills/code-modularize/scripts/scan_files.py <root> --json` |
| `logging` | **code-logging** skill | `python3 ~/.claude/skills/code-logging/scripts/scan_logging.py <root> --json` |
| `arch` | **code-arch-drift** skill | `python3 ~/.claude/skills/code-arch-drift/scripts/archcheck.py --root <root> --json` |
| `glossary` | **code-glossary** skill | skill's own harvest phase (no scan script) |
| `docs` | **audit-docs** skill (only if installed) | skill's own workflow |

For delegated dimensions, load the owning skill's SKILL.md and follow its
pipeline — this dispatcher only sequences, scopes, and commits. For `structure`
and `simplify`, load the named reference from this skill.

</dimension_registry>

<dimension_selection>

1. Parse `$ARGUMENTS` for dimension names (whitespace-separated, matching the
   registry's first column). Unknown names → list valid dimensions and ask once
   via consult-user-mcp `pick`.
2. No arguments → **all dimensions**, minus `docs` when the audit-docs skill is
   not installed and `claude-md`/`glossary` when the repo is a throwaway
   (no CLAUDE.md and user did not ask for one).
3. Resolve target root from `$ARGUMENTS` path (if given) or cwd.

</dimension_selection>

<shared_contract>

Every dimension runs the same five steps:

```
1. SCAN    read-only; machine output via --json where a scan command exists
2. PLAN    findings → prioritised task plan (references/plan-format.md);
           present to user, get approval before any edit
3. FIX     apply approved changes only
4. VERIFY  project quality gates: tests, typecheck, lint (detect from
           package.json / Makefile / pyproject / Cargo.toml / justfile);
           up to 3 fix cycles, then revert the dimension's changes
5. COMMIT  one atomic commit per dimension: `optimize(<dimension>): <summary>`
```

Preconditions (once, before any dimension):
- Clean working tree (`git status --porcelain` empty) — otherwise ask the user
  to commit or stash first.
- Work on a branch: `git checkout -b optimize/$(date +%Y%m%d-%H%M%S)`.

</shared_contract>

<fan_out>

**Scans run in parallel, fixes run serially.**

- Spawn one subagent per selected dimension in a SINGLE message (multiple Task
  calls, `subagent_type: Explore`). Each subagent runs its dimension's SCAN
  and returns findings as JSON/markdown — no edits.
- The lead merges all scan results into one ranked hit list (group by
  dimension, sort by severity/impact) and presents it before touching anything.
- FIX phases then execute one dimension at a time in the execution order below —
  dimensions touch overlapping files, so parallel fixing would conflict.

</fan_out>

<execution_order>

```
structure   → files land in final locations first; every later dimension
              sees stable paths
claude-md   → context tree written against the new layout
arch        → boundary rules checked/fixed before code-level edits
smells      → dead code and duplicates removed before restructuring modules
modularize  → oversized files split
simplify    → behavior-preserving cleanup of what remains
logging     → levels/messages fixed on final code
docs        → documents the final state
glossary    → vocabulary locked last, after all renames settle
```

Skip any dimension whose scan returns zero findings — note it in the summary.

</execution_order>

<project_detection>

Detect project type from root files to calibrate scans and quality gates:

| File found | Project type |
|---|---|
| `package.json` | Node/TypeScript |
| `pyproject.toml` / `setup.py` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `Package.swift` | Swift |
| `*.sln` / `*.csproj` | C# |

Multiple manifests → treat as multi-language; run each dimension across all.

</project_detection>

<output_format>

After all dimensions complete, summarise:

```
## Code Optimize — Complete

### Dimensions run
- structure: [N] files moved, [N] dirs merged
- smells: [N] dead code blocks removed
- simplify: [N] files simplified ([−N] lines)
- ...

### Commits created
- optimize(structure): ...
- optimize(smells): ...

### Skipped
- [dimension]: [reason — zero findings / not installed / user deselected]

Branch: optimize/<timestamp>
```

</output_format>

<reference_files>

- [Structure](references/structure.md) — folder-organisation dimension: detection, target tree, move mechanics with import fixes per language
- [Simplify](references/simplify.md) — behavior-preserving simplification: 6-phase execute loop, refinement rules
- [Simplify Patterns](references/simplify-patterns.md) — language-specific transformation patterns
- [Simplify Agent Prompts](references/simplify-agent-prompts.md) — scanner/analyser/executor prompt templates
- [Plan Format](references/plan-format.md) — standards detection, per-dimension checklists, analysis report + tasks.md formats, approval flow

</reference_files>

<related_skills>

| Skill | Relationship |
|---|---|
| **code-map** | Optional structural context — PageRank map before scanning |
| **code-audit** | Owns the `smells` dimension |
| **code-modularize** | Owns the `modularize` dimension |
| **code-logging** | Owns the `logging` dimension |
| **code-arch-drift** | Owns the `arch` dimension |
| **code-glossary** | Owns the `glossary` dimension |
| **claude-md-tree** | Owns the `claude-md` dimension |
| **audit-docs** | Owns the `docs` dimension (external; skip if absent) |
| **smart-commit** | Optional — split leftover changes into atomic commits |

</related_skills>
