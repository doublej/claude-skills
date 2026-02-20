---
name: codebase-simplify
description: Simplify an entire codebase for clarity and maintainability using parallel agents. Preserves ALL functionality. Use when reducing complexity across a project.
---

# Codebase Simplify

Simplify an entire codebase using parallel agents. Read-only analysis phases, then batched edits with atomic commits and quality gates. All functionality is preserved.

## Pipeline

```
Phase 1: SCOPE      lead (sonnet)            → detect language, determine scope
Phase 2: SCAN       haiku Explore (×N)       → fast pattern inventory
Phase 3: ANALYZE    sonnet Explore (×N)      → semantic analysis, proposals
Phase 4: PLAN       lead (opus reasoning)    → prioritise, batch, present to user
Phase 5: EXECUTE    sonnet general-purpose (×N) → apply simplifications
Phase 6: VERIFY     lead (sonnet)            → run checks, commit atomically
```

## Phase 1: Scope

1. Detect the target project root from `$ARGUMENTS` or current working directory.
2. Detect primary language from manifest files (`package.json`, `go.mod`, `Cargo.toml`, `Package.swift`, `pyproject.toml`, `setup.py`).
3. Run the scan script for a file inventory:

```bash
python3 {SKILL_DIR}/scripts/scan_codebase.py <project-root> --json
```

4. **(Optional)** If the codebase-mapper skill is installed, generate a codebase map for structural context:

```bash
MAPPER_SCRIPT="${HOME}/.claude/skills/codebase-mapper/scripts/repomap.sh"
[ -f "$MAPPER_SCRIPT" ] && bash "$MAPPER_SCRIPT" <project-root> --root <project-root> --map-tokens 8192 --exclude-unranked
```

If the map was generated, present it to the user. Highlight:
- Top-ranked files (most referenced / depended upon)
- Architectural layers visible in the map
- High-complexity hotspots from the scan

5. Determine codebase size tier from file count:

| Size | Files | Scanners | Analysers | Executors |
|------|-------|----------|-----------|-----------|
| Small | 1-20 | skip | 1 | 1 |
| Medium | 21-100 | 3-5 | 2-4 | 2-3 |
| Large | 101-500 | 5-8 | 4-6 | 3-5 |
| XL | 500+ | 8 cap | 6 cap | 5 cap |

6. **Scope selection** — varies by codebase size:

**Small/Medium (≤100 files)** — ask via consult-user-mcp `pick`:
- **Full codebase** — simplify everything
- **High complexity only** — files with complexity score > 5
- **Specific directories** — follow up with `text` input

**Large/XL (100+ files)** — the scan script auto-detects logical sections (frontend, backend, shared, tests, scripts) from directory patterns. Present detected sections with file counts and complexity scores, then ask via consult-user-mcp `pick` with `multi: true`:
- One choice per detected section (e.g. "Frontend (142 files, avg 4.2)" / "Backend (89 files, avg 5.8)")
- **All sections** — simplify everything
- **High complexity only** — files with complexity score > 5 across all sections

This prevents accidentally simplifying an entire monorepo when the user only wants to target the frontend.

7. **Require clean working tree** before any edits. Run `git status --porcelain` — if output is non-empty, ask the user to commit or stash changes first. This ensures rollback in Phase 6 cannot destroy pre-existing work.

8. Create a git branch before any edits:
```bash
git checkout -b simplify/$(date +%Y%m%d-%H%M%S)
```

## Phase 2: Scan (read-only)

**Skip for Small codebases** — lead reads files directly.

For Medium+, distribute files evenly across scanner agents. Spawn all scanners in a **single message** (multiple Task calls):

```
subagent_type: Explore
model: haiku
```

Each scanner prompt:

```
You are scanning files for simplification opportunities. For each file, identify:
1. Functions >20 lines (with line numbers)
2. Nesting depth >2 levels
3. Duplicate/near-duplicate logic across files
4. Dead exports (exported but not imported by other files in the batch)
5. Overly complex conditionals

Files to scan:
{file_list}

Scan data from scan_codebase.py:
{scan_json_subset}

Return a JSON array of findings:
[{"file": "...", "line": N, "category": "oversized|nesting|duplication|dead-export|complex-conditional", "description": "...", "severity": "high|medium|low"}]
```

Merge all scanner results into a single findings list.

## Phase 3: Analyse (read-only)

Distribute findings across analyser agents. Spawn all in a **single message**:

```
subagent_type: Explore
model: sonnet
```

Each analyser prompt — load the reference file first:

```
Read {SKILL_DIR}/references/simplification-patterns.md for language-specific patterns.
Read {SKILL_DIR}/references/agent-prompts.md for the analyser template, then follow it.

Language: {language}
Project standards: {standards_from_claude_md}

Findings to analyse:
{findings_subset}

For each finding, propose a concrete simplification:
- What to change (specific code transformation)
- Why it's simpler (clarity, fewer lines, reduced nesting)
- Risk level (safe / needs-test / breaking)
- Estimated line delta

Return JSON array of proposals:
[{"file": "...", "line": N, "category": "...", "action": "...", "before_sketch": "...", "after_sketch": "...", "risk": "safe|needs-test|breaking", "line_delta": -N}]

CRITICAL: Never propose changes that alter functionality. Only simplify HOW code works, not WHAT it does.
```

## Phase 4: Plan

Switch to opus reasoning for this phase only. Consume all proposals and:

1. **Deduplicate** — remove conflicting proposals for the same code region.
2. **Prioritise** by impact (line_delta × severity) descending.
3. **Batch** into groups of 5-15 changes that can be applied and tested independently. Each batch targets a logical unit (module/directory).
4. **Present** the plan to the user via consult-user-mcp `form`:
   - Show batch count, total estimated line reduction, risk breakdown
   - For each batch: files affected, summary of changes, risk level
   - Options: **Apply all**, **Select batches** (follow up with multi-pick), **Cancel**

If user selects specific batches, proceed only with those.

## Phase 5: Execute

For each approved batch, spawn executor agents. Spawn all executors for a batch in a **single message**:

```
subagent_type: general-purpose
model: sonnet
```

Each executor prompt:

```
Read {SKILL_DIR}/references/agent-prompts.md for the executor template, then follow it.

Apply these simplifications to the codebase. Each change MUST preserve exact functionality.

Batch: {batch_name}
Changes:
{proposals_for_this_batch}

Rules:
1. Read each file before editing
2. Apply changes using Edit tool (prefer small, targeted edits)
3. Never change what code does — only how it does it
4. Follow existing code style and conventions
5. If a change seems risky after reading the actual code, skip it and note why

Report: list of files modified, changes applied, any skipped changes with reasons.
```

## Phase 6: Verify

After each batch of executors completes:

1. **Quality gates** — run the project's check commands (detect from package.json scripts, Makefile, etc.):
   - Typecheck (tsc, mypy, go vet, etc.)
   - Test (npm test, pytest, go test, cargo test, etc.)
   - Lint (eslint, ruff, golangci-lint, etc.)

2. If checks fail: iterate up to 3 fix cycles. If still failing, **revert the batch** back to the last commit (safe because we required a clean tree in Phase 1 and commit after each successful batch):
```bash
# Reset all changes back to last commit on the simplify branch
git checkout HEAD -- .
# Remove any new untracked files created during the batch
git clean -fd
```

3. If checks pass: commit atomically:
```bash
git add <files_in_batch>
git commit -m "simplify: {batch_summary}"
```

4. Repeat for next batch.

5. After all batches: summarise results via consult-user-mcp `notify`:
   - Batches applied / reverted
   - Total lines removed
   - Files modified
   - Branch name for review

## Refinement Rules

These rules apply to ALL simplification proposals and edits:

1. **Preserve Functionality**: Never change what the code does — only how it does it.
2. **Apply Project Standards**: Follow coding standards from CLAUDE.md. Detect the language/framework and apply appropriate conventions.
3. **Enhance Clarity**:
   - Reduce unnecessary complexity and nesting (use guard clauses)
   - Eliminate redundant code and abstractions
   - Improve readability through clear names
   - Consolidate related logic
   - Remove comments that describe obvious code
   - Avoid nested ternaries — prefer switch/if-else for multiple conditions
   - Choose clarity over brevity
4. **Maintain Balance** — avoid over-simplification that could:
   - Reduce clarity or maintainability
   - Create overly clever solutions
   - Combine too many concerns into single functions
   - Remove helpful abstractions
   - Make code harder to debug or extend

## Reference Files

- [Simplification Patterns](references/simplification-patterns.md) — language-specific transformation patterns
- [Agent Prompts](references/agent-prompts.md) — parameterised prompt templates for scanner, analyser, executor
