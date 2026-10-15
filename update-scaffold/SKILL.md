---
name: update-scaffold
description: "Pull upstream cookiecutter-template updates into a generated project, safely. Use when a [template-update] hook fires, the user says 'update scaffold' / 'pull template updates' / runs /update-scaffold, or asks to sync a project with its template. Merges like git: tooling is overwritten, every other file is 3-way merged so local edits stay."
---

# Update Scaffold

Bring a project generated from the cookiecutter-templates repo up to date with its upstream template, without bulldozing local edits.

The classification + diffing logic already lives in the templates repo at `tools/update_scaffold.py`. This skill does NOT reimplement it — it locates the project, runs that script, and walks the user through the result safely.

## Presentation

Print this banner once, first in the response; close the run with the report below.

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   UPDATE SCAFFOLD                                            ║
║   Upstream template updates, applied without bulldozing      ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
```
UPDATE SCAFFOLD  ──  <template> <local> → <upstream>   mode: <merge|force|bump only>

FILE                    BUCKET             ACTION
──────────────────────────────────────────────────────────────
<path>                  <bucket>           <overwritten|updated|added|merged|conflict→resolved|sidecar>

github.com/doublej
```

A conflict still awaiting the user is a row marked `…` with the one-line question.

## When this runs

- The SessionStart hook prints `[template-update] … <template> <local> -> <upstream>` (the deployed `check_template_update.py`).
- The user invokes `/update-scaffold`, or says "update the scaffold", "pull template updates", "sync with the template".

## Preconditions (check first, bail clearly)

1. **`.template-meta.json` exists** in the project root. It holds `template` (e.g. `python/fastapi`), `template_version`, `context` (original cookiecutter answers), `template_source.path` (absolute path to the templates repo), and optionally `retrofit: true`. If it's missing, this project was not scaffolded from these templates — stop and say so.
2. **The templates repo is reachable.** Resolution order: `$COOKIECUTTER_TEMPLATES` env, else `template_source.path` from the meta file. If neither resolves to an existing dir, stop and explain the v1 limitation: the path is captured at render time, so a moved repo breaks the link — the user must set `$COOKIECUTTER_TEMPLATES` or fix `template_source.path`.

## How the updater merges

`update_scaffold.py` renders the template twice with the saved `context`: at the project's own `template_version` (the merge base) and at the released upstream version. Then it handles each changed file:

| Bucket | Examples | Action |
|--------|----------|--------|
| `template_managed` | `.claude/scripts/*.py` | Overwritten in place — pure tooling |
| `mergeable` | `.atlas` | Shallow JSON merge — upstream keys added, local values kept |
| `merge` | everything else (CLAUDE.md, Justfile, manifests, `src/**`, new files) | 3-way merge with `git merge-file` |

The 3-way merge is what makes this quiet:
- The template did not change the file → left alone, whatever your edits.
- You never edited it → upstream copy (`[updated]`). New in the template → `[added]`. You deleted it → stays deleted.
- Both changed it in different places → merged cleanly (`[merged]`).
- Both changed the same lines → git conflict markers in the file (`[conflict]`), listed at the end of the output.

No merge base (`retrofit: true`, no `template_version`, or a version with no release commit) → seeds fall back to `<file>.upstream` sidecars, with `--include-other` for unclassified files. `--force` overwrites seeds instead of merging; never pass it unless the user explicitly asks.

## Workflow

`$REPO` is `$COOKIECUTTER_TEMPLATES`, else `template_source.path` from `.template-meta.json`:

```bash
python3 "$REPO/tools/update_scaffold.py" --apply .
```

`just update-scaffold --apply` does the same if the project's Justfile has the recipe; on "Justfile does not contain recipe 'update-scaffold'" use the script call directly.

1. **Check git.** If the working tree has uncommitted changes in files the update touches, commit them first or stop and say so. The merge writes in place, and git is the undo button. Do not ask for permission: merging is the safe default.
2. **Apply.** Run with `--apply`. If it prints "Up to date", say so and stop.
3. **Resolve conflicts yourself.** For each file under "Left N file(s) with git conflict markers", read the `<<<<<<< yours` / `||||||| template (old)` / `>>>>>>> template (new)` hunks and write the combination that keeps both intents: the local customization and the template's improvement. That is almost always possible (for example, a renamed recipe plus a local tweak to it, or a new dependency next to a local pin). Only `ask` (consult-user-mcp) when the two sides really are mutually exclusive, with one question per conflict that names both options. AFK/cancelled → keep the local side, and list the conflict as pending.
4. **Sidecars (no-base fallback only).** Merge each `<file>.upstream` into `<file>` the same way, keeping both intents, then `trash` the sidecar (a safe-rm hook blocks `rm -f`; `trash` prints nothing on success).
5. **Verify and commit.** `grep -rn '^<<<<<<< yours' .` must be empty, then run `just check`. Commit as `chore: update scaffold to <template> <version>`.

Bump only (edit `template_version` by hand and change nothing else) is still an option, but only when the user asks for it.

## Retrofit projects

If `meta.retrofit` is true, the project's local files predate the template, so there is no merge base and seeds become sidecars. Merge them the way step 4 describes. Do **not** offer force-overwrite as a casual default.

## Opt-outs (detection only)

These silence the SessionStart *prompt*, not this skill: env `NO_TEMPLATE_UPDATE_CHECK=1` or sentinel `.claude/no-template-update-check`. If a user is annoyed by repeated prompts, point them here.
