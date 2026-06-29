---
name: rename-project
description: "Rename end-to-end: folder, GitHub repo, remote, manifests, imports, venv"
---

<intro>

Rename a project across all its roots — folder, GitHub repo, git remote, manifests, packages, imports, and docs — in a safe, ordered sequence.

</intro>

<scripts>

All scripts are in `~/.claude/skills/rename-project/scripts/`.

### Scan

```bash
python3 ~/.claude/skills/rename-project/scripts/scan_project.py /path/to/project new-name        # human summary
python3 ~/.claude/skills/rename-project/scripts/scan_project.py /path/to/project new-name --json  # structured JSON
```

Detects: folder name, GitHub remote, pyproject.toml, package.json, Cargo.toml, go.mod, Python package dirs, Python imports, lock files, .venv, and doc references. A final catch-all pass (`git grep`, with a manual-walk fallback) finds every other text file that still mentions the old name — string literals, nested manifests (`src-tauri/Cargo.toml`), framework configs (`tauri.conf.json`, `capabilities/*.json`), non-Python source (`.svelte`, `.java`, `.rs`), and JSON metadata (`.template-meta.json`) — emitted as an `update_references` action.

</scripts>

<workflow>

### Phase 1 — Scan

Run the scan script on the target project:

```bash
python3 ~/.claude/skills/rename-project/scripts/scan_project.py <project-path> <new-name> --json
```

Parse the JSON output. This gives an ordered action plan with zero side effects.

### Phase 1.5 — Collision check

Before trusting any text-replace step, check whether the old slug is also a common word or appears in non-brand contexts. Risk signals:

- Old slug is a common English word, color, unit, or generic noun (e.g. `cobalt` is also a CSS color and may appear as `--cobalt-*` tokens or a `COBALT` constant — unrelated to the project's identity).
- The catch-all `update_references` hits include CSS custom properties, color values, or prose where the term is not the project name.

If the old slug collides with non-brand usage, surface the ambiguous hits in the review table and confirm with the user which occurrences to replace before executing any text-replace step. Do not blindly replace every match.

### Phase 2 — Review

Present the action plan to the user as a numbered table:

| # | Type | Description |
|---|------|-------------|
| 1 | rename_github_repo | Rename GitHub repo org/old → org/new |
| 2 | update_git_remote | Update origin remote URL |
| ... | ... | ... |

Get explicit confirmation before proceeding. If user wants to skip actions, note which ones.

### Phase 3 — Execute

Run actions in this exact order. Each step must succeed before the next.

**Pre-flight checks:**
- `git status` — must be clean (no uncommitted changes)
- `gh auth status` — must be authenticated (needed for GitHub rename)

**Execution order:**

1. **Rename GitHub repo** (most likely to fail — permissions, name conflicts)
   ```bash
   gh api -X PATCH repos/{org}/{old_repo} -f name={new_slug}
   ```

2. **Update git remote URL**
   ```bash
   git remote set-url origin <new_url>
   ```

3. **Update manifests** — edit `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod` using the scan output's old/new values. Use targeted search-replace on the specific fields.

4. **Rename Python package dirs** — `mv src/old_snake/ src/new_snake/`

5. **Fix Python imports** — search-replace `import old_snake` → `import new_snake` and `from old_snake` → `from new_snake` in all `.py` files listed by the scan.

6. **Update docs** — search-replace old slug and old snake case name in README.md, CLAUDE.md, and other docs listed by the scan.

7. **Update other references** — for each file in the `update_references` action, replace old slug/snake references. These are string literals, nested manifests, framework configs, and non-Python source the structured scanners don't parse. Review each hit — some may be false positives (see Phase 1.5 collision check).

8. **Recreate venv** (if flagged by scan)
   ```bash
   rm -rf .venv && uv venv && uv sync
   ```

9. **Regenerate lock files** — run the appropriate command per lock file:
   - `uv.lock` → `uv lock`
   - `bun.lock` → `bun install`
   - `package-lock.json` → `npm install`
   - `Cargo.lock` → `cargo generate-lockfile`
   - `go.sum` → `go mod tidy`

10. **Rename folder on disk** (LAST — so partial failure keeps project at old path)
   ```bash
   mv /path/to/old-name /path/to/new-name
   ```
   After this, `cd` into the new path for remaining work.

</workflow>

<post_rename>

1. **Commit all changes** in the renamed project:
   ```
   rename: old-name → new-name
   ```

2. **Remind the user** about manual follow-ups:
   - CI/CD pipelines referencing old name
   - Other repos that depend on this project
   - Bookmarks, documentation links, deployment configs
   - Docker images, container names
   - Environment variables referencing old name

</post_rename>

<safety>

- **Folder rename is last** — all other operations work from the current path. If any step fails, the project stays at its old location and is fully usable.
- **GitHub rename is first in execution** — it's the most likely to fail (permissions, name conflicts). If it fails, nothing else has changed yet.
- **No automatic rollback** — ordered execution makes partial states safe. Manual fix is simpler and more predictable than rollback logic.
- **Always confirm** before executing. Show the full action plan first.
- **Clean git required** — refuse to proceed if there are uncommitted changes.
- Never skip the scan phase — it catches edge cases the workflow alone would miss.

</safety>

<action_types>

| Type | What it does |
|------|-------------|
| `rename_github_repo` | Rename the GitHub repository |
| `update_git_remote` | Update the origin remote URL |
| `update_manifest` | Change name field in a package manifest |
| `rename_package_dir` | Rename a Python package directory |
| `fix_python_imports` | Update import statements in .py files |
| `update_docs` | Replace old name references in markdown docs |
| `update_references` | Catch-all: replace old name in other text files (string literals, nested manifests, framework configs, non-Python source) |
| `regenerate_lock_files` | Re-generate dependency lock files |
| `recreate_venv` | Delete and recreate Python virtual environment |
| `rename_folder` | Rename the project folder on disk (always last) |

</action_types>
