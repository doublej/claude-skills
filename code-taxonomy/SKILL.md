---
name: code-taxonomy
description: Audit naming quality across a codebase — style consistency, verb usage, clarity, and anti-patterns. Produces an annotated tree view, optionally enriched with PageRank data from codebase-mapper. Batch-renames to fix issues. Use when naming drift has accumulated or enforcing a style guide.
---

# Code Taxonomy

Audit naming quality across a codebase. Goes beyond style checking (snake_case vs camelCase) to analyse whether names are clear, descriptive, and consistently designed. Detects verb inconsistencies (mixed get/fetch), generic names (data, result, manager), missing boolean prefixes, and more. Produces an annotated tree visualisation of the naming structure.

Scanner does mechanical extraction. Claude does semantic judgment.

## Pipeline

```
Phase 1: SCOPE      run scanner + optional codebase-mapper
Phase 2: ANALYSIS   Claude reviews tree + quality data with semantic judgment
Phase 3: REVIEW     present findings grouped by issue type, user picks categories
Phase 4: PLAN       batch rename proposals (style + verb + clarity)
Phase 5: EXECUTE    apply renames with quality gates per batch
Phase 6: VERIFY     test suite + summary
```

## Phase 1: Scope

1. Detect the target project root from `$ARGUMENTS` or current working directory.
2. Run the naming scanner with tree and quality analysis:

```bash
python3 {SKILL_DIR}/scripts/scan_naming.py <project-root> --json --tree
```

3. Parse JSON output. Key fields:
   - **Style**: `by_language`, `detected_conventions`, `violations`, `violation_count`
   - **Quality**: `quality.verb_usage`, `quality.verb_groups`, `quality.anti_patterns`, `quality.anti_pattern_counts`
   - **Tree**: `tree` (nested directory → file → symbol structure)

4. If `violation_count` is 0 AND `quality.anti_pattern_counts` is empty AND `quality.verb_groups` is empty: notify user "No naming issues found" via consult-user-mcp `notify` and stop.

5. Optionally run codebase-mapper for PageRank ranking of important files:

```bash
MAPPER="{SKILL_DIR}/../codebase-mapper/scripts/repomap.sh"
[ -f "$MAPPER" ] && bash "$MAPPER" <project-root> --root <project-root> --map-tokens 4096 --exclude-unranked
```

If available, use PageRank to prioritise high-ranked files in the analysis.

## Phase 2: Analysis

Claude reads the tree + quality data and applies semantic judgment. The scanner flags mechanical issues; Claude evaluates whether they're real problems in context.

### Verb Consistency

From `quality.verb_groups`, evaluate each inconsistency:
- Is the verb difference intentional? (e.g. `get` = sync, `fetch` = async)
- Is it a real inconsistency that should be unified?
- Which verb should be dominant?

### Anti-Patterns in Context

From `quality.anti_patterns`, evaluate each flag:
- **generic_name**: Is "data" actually vague here, or is it clear from context? (e.g. `parse_data` in a parser is fine)
- **missing_bool_prefix**: Does this variable benefit from `is_`/`has_` prefix?
- **overly_long**: Is truncation possible without losing clarity?
- **unknown_abbreviation**: Is the abbreviation obvious in this domain?

### Cross-Module Consistency

Assess whether similar concepts are named uniformly:
- Are handlers/controllers/services named with the same pattern?
- Do similar modules use the same noun conventions?

### Style Violations

From `violations`, classify by priority:

| Priority | Category | Impact |
|----------|----------|--------|
| P1 | Public API / exported symbols | High — breaks consumers |
| P2 | Internal exported (cross-file) | Medium — breaks internal imports |
| P3 | Private methods (`_prefix`) | Low — single file scope |
| P4 | Local variables | Minimal — function scope only |
| P5 | File names | Medium — affects import paths |

For each violation, use Grep to count references across the codebase:
```
Grep: pattern="\bsymbol_name\b" in project root
```

## Phase 3: Review

Present findings as an annotated tree grouped by issue type.

1. Read the reference files:
```
{SKILL_DIR}/references/naming-conventions.md
{SKILL_DIR}/references/rename-strategies.md
```

2. Present findings grouped by category via consult-user-mcp `form`:

```json
{
  "type": "form",
  "body": "Naming audit complete. Select which issue categories to address.",
  "questions": [
    {
      "id": "categories",
      "question": "Which issue types to fix?",
      "options": [
        "Style issues (mechanical convention violations)",
        "Clarity issues (generic names, missing prefixes)",
        "Consistency issues (verb consolidation)",
        "All of the above"
      ]
    },
    {
      "id": "allowlist",
      "question": "Terms to allowlist (skip during renames)?",
      "type": "text",
      "placeholder": "API, URL, ID, HTML (comma-separated)",
      "default": ""
    }
  ]
}
```

3. If user provided allowlist terms, re-run the scanner:
```bash
python3 {SKILL_DIR}/scripts/scan_naming.py <project-root> --json --tree --allowlist "API,URL,ID"
```

## Phase 4: Plan

Present rename proposals to the user based on selected categories.

1. Group renames into batches:
   - **By directory/module** — changes within one module per batch
   - **Max 15 renames per batch** — keeps commits reviewable
   - **Never mix P1 (public API) with lower priorities** in the same batch
   - **Verb consolidation renames in their own batch** (see references/rename-strategies.md)
   - **File renames always in a separate final batch**

2. For each batch, compute:
   - Symbol count
   - Total reference count
   - Risk level: `low` (P3-P4 only), `medium` (P2), `high` (P1 or file renames)
   - Issue type: `style`, `clarity`, or `consistency`

3. Present via consult-user-mcp `form`:

```json
{
  "type": "form",
  "body": "Rename plan: {total} renames across {batch_count} batches",
  "questions": [
    {
      "id": "scope",
      "question": "Which batches to apply?",
      "options": [
        "All batches",
        "Safe only (P3-P4, low risk)",
        "Let me pick specific batches"
      ]
    }
  ]
}
```

4. If user picks "Let me pick", follow up with consult-user-mcp `pick` with `multi: true` listing each batch:
```
"Batch 1: src/utils/ — 8 style renames, 23 refs (low risk)"
"Batch 2: src/api/ — 5 verb renames: fetch→get, 12 refs (medium risk)"
```

## Phase 5: Execute

Apply renames in safe order with quality gates.

### Pre-flight

1. **Clean git required.** Run `git status --porcelain` — if non-empty, ask user to commit or stash first.

2. **Create branch:**
```bash
git checkout -b taxonomy/$(date +%Y%m%d-%H%M%S)
```

3. **Detect quality gate commands** from project manifests:
   - Typecheck: `tsc --noEmit`, `mypy .`, `pyright`, `go vet ./...`, `cargo check`
   - Test: `npm test`, `pytest`, `go test ./...`, `cargo test`
   - Lint: `eslint .`, `ruff check .`, `golangci-lint run`

### Per-Batch Execution

For each approved batch, in order (P4 → P3 → P2 → P1 → verb consolidation → P5):

1. **Apply renames** using Edit tool:
   - For each symbol in the batch:
     a. Read the defining file
     b. Grep for all references: `\bOLD_NAME\b`
     c. Rename references first (in importing files), then the definition
     d. For file renames: update imports first, then `git mv old new`
     e. For verb renames: check for name collisions before applying

2. **Quality gate** after each batch:
   - Run typecheck + test commands
   - If failure: fix cycle (up to 3 attempts)
   - If still failing after 3 cycles: revert the batch:
     ```bash
     git checkout HEAD -- .
     git clean -fd
     ```
   - Notify user which batch was reverted and why

3. **Commit** successful batch:
   ```bash
   git add <files_in_batch>
   git commit -m "taxonomy: rename {category} in {module} to {style}"
   ```

4. Proceed to next batch.

### File Rename Batch (P5)

File renames are the most impactful — always executed last in their own batch:

1. For each file rename:
   a. Grep all files for imports of the old filename
   b. Update import paths in all consuming files using Edit
   c. `git mv old_path new_path`
2. Quality gate as above
3. Commit: `taxonomy: rename files to {style}`

## Phase 6: Verify

After all batches:

1. **Full test suite** — run the project's full test command.
2. **Summary** via consult-user-mcp `notify`:

```
Code Taxonomy complete:
- {applied} of {total} batches applied
- {reverted} batches reverted
- {symbols_renamed} symbols renamed ({style_renames} style, {verb_renames} verb, {clarity_renames} clarity)
- {files_renamed} files renamed
- Branch: taxonomy/YYYYMMDD-HHMMSS
```

3. If any batches were reverted, list them with failure reasons so the user can address manually.

## Reference Files

- [Naming Conventions](references/naming-conventions.md) — per-language canonical conventions
- [Rename Strategies](references/rename-strategies.md) — safe rename patterns, verb consolidation, pitfalls, rollback
