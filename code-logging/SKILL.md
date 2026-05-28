---
name: code-loggingdescription: "Audit and improve logging across a codebase: relevel mismatched log calls, rewrite vague messages into scannable structured form, and add logs at silent error branches and external calls. Cross-language (Python, JS/TS, Rust, Go, Swift). Use when the user asks to 'clean up logging', 'optimize log levels', 'add more logging', 'make logs scannable', or '/logging-audit'."
---

# Logging Audit

Audit log call sites across a codebase. Fix three classes of issue: **wrong level** (debug-as-error, info-in-catch), **bad message** (vague, no context, prose), **missing logs** (silent error branches, silent external calls). Apply changes in reviewable batches with quality gates.

Scanner does mechanical extraction. Claude does semantic judgment.

<pipeline>
```
Phase 1: SCOPE      run scan_logging.py, detect loggers in use
Phase 2: ANALYSIS   Claude reviews issues + gaps with semantic judgment
Phase 3: REVIEW     present findings grouped by category, user picks scope
Phase 4: PLAN       batch edits per file/module, classify risk
Phase 5: APPLY      rewrite + add logs per batch with quality gates
Phase 6: VERIFY     test suite + summary
```

Default mode is **audit-only**. Phase 5 only runs after explicit confirmation.
</pipeline>

<phase_1_scope>

1. Resolve target root from `$ARGUMENTS` or current working directory.

2. Run the scanner:
```bash
python3 {SKILL_DIR}/scripts/scan_logging.py <project-root> --json > /tmp/logging-audit.json
```

3. Read `/tmp/logging-audit.json`. Key fields:
   - `summary.loggers_detected` — which logger frameworks are in use, per file count
   - `summary.issue_counts` — mechanical issues by type
   - `summary.gap_counts` — silent error branches, silent external calls
   - `top_issues` — pre-ranked highest-severity call sites
   - `files[*]` — full per-file detail with `calls` and `gaps`

4. If `summary.log_calls_found` is 0 AND `gap_counts` is empty: notify "No logging found and no gap candidates" via `consult-user-mcp.notify` and stop.

5. If multiple loggers appear in `loggers_detected` for the same language (e.g. `python:logging` AND `python:loguru`), flag as a separate observation in Phase 3 — do not auto-unify.
</phase_1_scope>

<phase_2_analysis>

Claude reads `top_issues` and `files[*]` and applies semantic judgment. The scanner flags candidates; you decide whether each is real.

Load reference files first:
- `{SKILL_DIR}/references/log-style-guide.md` — format spec, level semantics, scannability rules
- `{SKILL_DIR}/references/language-patterns.md` — idiomatic structured-field syntax per logger
- `{SKILL_DIR}/references/gap-detection.md` — when to add logs, when to skip

### Issue triage

For each entry in `top_issues`, decide: real issue, false positive, or skip-with-reason.

| Issue tag | What to evaluate |
|-----------|------------------|
| `vague_message` | Read the surrounding scope. "done" inside `process_payment` is vague. "ok" as a heartbeat reply might be fine. |
| `level_too_low_critical` | Does the message actually describe a critical condition, or just contain the word? |
| `level_too_low_error_word` | Same — is "error" the topic or part of an unrelated phrase? |
| `error_branch_low_level` | Is the branch genuinely an error, or expected control flow (e.g. cache miss)? |
| `hot_loop_candidate` | Is the loop bounded and small (≤10 iterations)? Then it's not really hot. |
| `no_context_fields` | Is the message self-contained ("server.start port=8080" inline is fine), or referring to something the caller can't see? |
| `string_concat_format` | Always rewrite — concat loses structure. |

### Gap triage

For each entry in `files[*].gaps`:

- **`silent_error_branch`**: Open the file with Read at the line. Confirm the handler does work (returns, sets state, swallows). If `pass` is genuinely intentional (e.g. probe `except json.JSONDecodeError: pass` for optional config) — skip. Otherwise it's a real gap.
- **`silent_external_call`**: Check whether a tracing span / `instrument` / OpenTelemetry middleware is already wrapping it (read 20 lines around). If yes — skip. If no — real gap.

Do not surface false positives in Phase 3. Only present gaps you'd commit to.

### Output of this phase

A working list, grouped by category:

```
RELEVEL    (count) — log calls with wrong level
REWRITE    (count) — vague / context-less / prose messages
ADD_ERR    (count) — silent error branches needing logs
ADD_EXT    (count) — silent external calls needing logs
NOISE      (count) — redundant/start+end/hot-loop logs to delete
```
</phase_2_analysis>

<phase_3_review>

Present the analysis to the user via `consult-user-mcp.ask` with `type: form`.

Pre-form: send a `notify` with the summary counts so the user has context before answering.

```json
{
  "type": "form",
  "title": "logging-audit findings",
  "body": "<insert summary: N files scanned, M log calls, K issues, G gap candidates. Top 3 most-affected files.>",
  "questions": [
    {
      "id": "categories",
      "question": "Which categories to act on?",
      "type": "choice",
      "multi": true,
      "options": [
        "RELEVEL — fix log levels",
        "REWRITE — rewrite vague messages into structured form",
        "ADD_ERR — log silent error branches",
        "ADD_EXT — log silent external calls",
        "NOISE — delete redundant logs"
      ]
    },
    {
      "id": "mode",
      "question": "Stop after report, or continue to apply?",
      "type": "choice",
      "options": [
        "Audit-only — write report and stop",
        "Apply — proceed through Phase 4 + 5 with per-batch confirmation"
      ]
    },
    {
      "id": "scope_filter",
      "question": "Limit scope?",
      "type": "text",
      "placeholder": "e.g. src/api/ only, or leave blank for full scope"
    }
  ]
}
```

If `mode` = audit-only: write `LOGGING_AUDIT_REPORT.md` at the project root with the categorised findings (file:line, current → proposed). Stop. Do not modify code.

If `mode` = apply: proceed to Phase 4 with the selected categories and scope filter applied.
</phase_3_review>

<phase_4_plan>

Build batches. Each batch = changes within one file or one tightly-coupled module.

### Batching rules

- **Max 12 changes per batch** — keeps diffs reviewable and quality gates fast.
- **One file per batch** unless the changes share a logger swap or a module-wide pattern.
- **Separate batches by category** — never mix a relevel batch with a gap-fill batch. Reverts stay clean.
- **Order**: NOISE first (deletes), then REWRITE, then RELEVEL, then ADD_ERR, then ADD_EXT.
- **Risk**:
  - `low` — message rewrite, level lowering (info → debug)
  - `medium` — level raising (info → error), new logs in error branches
  - `high` — new logs at external calls (touches more lines, may need imports)

### Per-batch metadata

Compute and surface:
- file count, change count, category, risk
- a 3-line preview of one representative change (file:line, current, proposed)

### Batch approval

Send a single `pick` with `multi: true` listing all batches:

```json
{
  "type": "pick",
  "multi": true,
  "title": "logging-audit batches",
  "body": "Select batches to apply. Order: NOISE → REWRITE → RELEVEL → ADD_ERR → ADD_EXT.",
  "choices": [
    "Batch 1: src/payments.py — 8 RELEVEL (medium risk)",
    "Batch 2: src/api/checkout.py — 5 ADD_EXT (high risk)",
    "Batch 3: src/queue/worker.py — 3 NOISE deletes (low risk)"
  ]
}
```
</phase_4_plan>

<phase_5_apply>

Apply approved batches in safe order with quality gates.

### Pre-flight

1. **Clean git required.** Run `git status --porcelain` — if non-empty, ask user to commit or stash first.

2. **Create branch:**
```bash
git checkout -b logging-audit/$(date +%Y%m%d-%H%M%S)
```

3. **Detect quality gate commands** from project manifests:
   - Typecheck: `tsc --noEmit`, `mypy .`, `pyright`, `cargo check`, `go vet ./...`, `swift build`
   - Test: `pytest`, `npm test`, `cargo test`, `go test ./...`, `swift test`
   - Lint: `ruff check .`, `eslint .`, `clippy`, `golangci-lint run`

   If a project has none, skip gates and inform the user via `notify`.

### Per-batch execution

For each approved batch in order:

1. **Apply edits.** Use the `Edit` tool. For each change:
   - Read the file once (cache for the batch)
   - Use `old_string` / `new_string` with enough surrounding context to be unique
   - For ADD_EXT and ADD_ERR: import the logger module if not already imported (check first via Grep on the import line)
   - For language-specific syntax: follow `references/language-patterns.md` exactly — do not invent variants

2. **Quality gate.** Run the project's typecheck + test commands.
   - Pass → commit and continue.
   - Fail → up to 3 fix attempts. Each attempt: read failure, narrow the regression to a specific change, fix it, re-run.
   - Still failing → revert the batch:
     ```bash
     git checkout HEAD -- <files_in_batch>
     ```
     Notify user which batch was reverted and why.

3. **Commit:**
   ```bash
   git add <files_in_batch>
   git commit -m "logging-audit: <category> in <module> (N changes)"
   ```

4. Proceed to next batch.
</phase_5_apply>

<phase_6_verify>

After all batches:

1. **Full test suite** — run the project's full test command once more.

2. **Re-scan.** Run `scan_logging.py` again and diff issue/gap counts:
   ```
   Before:  vague_message=12  silent_error_branch=8  silent_external_call=22
   After:   vague_message=2   silent_error_branch=1  silent_external_call=4
   ```

3. **Summary** via `consult-user-mcp.notify`:
```
logging-audit complete:
- {applied} of {selected} batches applied
- {reverted} batches reverted
- {rewrites} messages rewritten
- {relevels} levels changed
- {gaps_filled} new logs added
- Issue count: {before} → {after} ({pct_reduction}% reduction)
- Branch: logging-audit/YYYYMMDD-HHMMSS
```

4. If any batches were reverted, list each with the failing test and a one-line cause so the user can address manually.
</phase_6_verify>

<reference_files>
- [Log Style Guide](references/log-style-guide.md) — format spec, level semantics, scannability, noise
- [Language Patterns](references/language-patterns.md) — idiomatic structured-field syntax per logger
- [Gap Detection](references/gap-detection.md) — when to add logs, where to skip, false-positive filters
</reference_files>

<related_skills>
| Skill | Relationship |
|-------|-------------|
| `code-taxonomy` | Same audit→batch→apply pattern, naming instead of logs |
| `dev-refactor` | Can consume this skill's report as a finding source |
| `codebase-mapper` | Optional — PageRank to prioritise high-importance files first |
</related_skills>
