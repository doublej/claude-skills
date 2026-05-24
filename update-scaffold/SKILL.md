---
name: update-scaffold
description: "Pull upstream cookiecutter-template updates into a generated project, safely. Use when a [template-update] hook fires, the user says 'update scaffold' / 'pull template updates' / runs /update-scaffold, or asks to sync a project with its template. Defaults to non-destructive: tooling is overwritten, your edits become .upstream sidecars."
---

# Update Scaffold

Bring a project generated from the cookiecutter-templates repo up to date with its upstream template, without bulldozing local edits.

The classification + diffing logic already lives in the templates repo at `tools/update_scaffold.py`. This skill does NOT reimplement it — it locates the project, runs that script, and walks the user through the result safely.

## When this runs

- The SessionStart hook prints `[template-update] … <template> <local> -> <upstream>` (the deployed `check_template_update.py`).
- The user invokes `/update-scaffold`, or says "update the scaffold", "pull template updates", "sync with the template".

## Preconditions (check first, bail clearly)

1. **`.template-meta.json` exists** in the project root. It holds `template` (e.g. `python/fastapi`), `template_version`, `context` (original cookiecutter answers), `template_source.path` (absolute path to the templates repo), and optionally `retrofit: true`. If it's missing, this project was not scaffolded from these templates — stop and say so.
2. **The templates repo is reachable.** Resolution order: `$COOKIECUTTER_TEMPLATES` env, else `template_source.path` from the meta file. If neither resolves to an existing dir, stop and explain the v1 limitation: the path is captured at render time, so a moved repo breaks the link — the user must set `$COOKIECUTTER_TEMPLATES` or fix `template_source.path`.

## How the updater classifies files

`update_scaffold.py` re-renders the template with the saved `context` and diffs each changed file into a bucket. Know these — they drive what you tell the user:

| Bucket | Examples | Default action |
|--------|----------|----------------|
| `template_managed` | `.claude/scripts/*.py` | **Overwritten in place** — pure tooling, safe |
| `mergeable` | `.atlas` (per `sync_manifest.json` → `merge_paths`) | Shallow JSON merge — upstream keys added, local values kept |
| `seed` | CLAUDE.md, Justfile, README.md, agent.md, .gitignore, .quality.json, .swiftlint.yml, lang manifests, `src/**` | **Never overwritten** — upstream copy written to `<file>.upstream` for manual merge |
| `other` | anything unclassified | Skipped unless `--include-other` |

`--force` makes seeds overwrite in place (destructive — local edits lost). On `--apply`, the script bumps `.template-meta.json` to the upstream version.

## Workflow

Run the updater via the project's Just recipe (every generated project has it; it resolves the repo path for you):

```bash
just update-scaffold              # report-only
just update-scaffold --diffs      # report-only + short per-file diffs
just update-scaffold --apply      # safe apply (tooling overwritten, seeds → sidecars)
just update-scaffold --apply --force   # also overwrite seeds (destructive)
```

If `just` is unavailable, call the script directly:
`python3 "$REPO/tools/update_scaffold.py" [--diffs|--apply|--force|--include-other] .`

1. **Preview.** Run `just update-scaffold --diffs`. Summarize: version jump, count per bucket, and — most important — how many `seed` files will need manual merge. If it reports "Up to date", say so and stop.
2. **Confirm, SAFE by default.** Ask the user yes / no / force. Default = safe: `template_managed` overwritten, `mergeable` merged, `seed` files written as `.upstream` sidecars. Offer `force` only as an explicit, warned opt-in.
3. **Apply.** `--apply` (safe) or `--apply --force` (destructive). Never pass `--force` unless the user explicitly chose it.
4. **Report.** List every `<file>.upstream` sidecar written. For each, offer to `diff -u <file> <file>.upstream`, help cherry-pick wanted changes into `<file>`, then `rm <file>.upstream`. Recommend running `just check` afterward.

## Retrofit projects

If `meta.retrofit` is true, the project's local files predate the template — seeds are guaranteed to differ. Do **not** offer force-overwrite as a casual default; lead with sidecars and manual merge.

## Opt-outs (detection only)

These silence the SessionStart *prompt*, not this skill: env `NO_TEMPLATE_UPDATE_CHECK=1` or sentinel `.claude/no-template-update-check`. If a user is annoyed by repeated prompts, point them here.
