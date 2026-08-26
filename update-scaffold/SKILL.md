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

**Net-new template files.** Files added upstream that don't exist locally are collected like any other change, but two things bite:

- Without `--include-other`, the `other` bucket is emptied *before* the summary prints — those files show up in no count and no diff. They are invisible, not merely skipped. Always preview with `--include-other` (step 1).
- A net-new *seed* file lands as `<file>.upstream`, never as `<file>`. You must `mv` it into place yourself.

## Workflow

The reliable path is the script itself — `$REPO` is `$COOKIECUTTER_TEMPLATES`, else `template_source.path` from `.template-meta.json`:

```bash
python3 "$REPO/tools/update_scaffold.py" [--diffs|--apply|--force|--include-other] .
```

`just update-scaffold <args>` is a convenience alias that resolves `$REPO` for you, **but only if the project's Justfile already has that recipe**. The Justfile is a `seed` file, so a project generated before the recipe existed never receives it and `just` fails with "Justfile does not contain recipe 'update-scaffold'". On that error, fall straight through to the script call — don't debug the Justfile.

```bash
just update-scaffold                   # report-only
just update-scaffold --diffs           # report-only + short per-file diffs
just update-scaffold --apply           # safe apply (tooling overwritten, seeds → sidecars)
just update-scaffold --apply --force   # also overwrite seeds (destructive)
```

1. **Preview.** Run with `--diffs --include-other` (always both — see *Net-new template files*). Summarize: version jump, count per bucket, how many `seed` files will need manual merge, and any `other`/net-new files. If it reports "Up to date", say so and stop.
2. **Confirm, SAFE by default.** Call consult-user-mcp `ask` (`type: "confirm"`, or `type: "pick"` when force is worth offering) with the bucket counts in the body. This is a real tool call, not a rhetorical pause — do not write "Applying safely" and proceed. The built-in `AskUserQuestion` tool is disabled in this environment; `ask` is the only channel.
   - `ask` returns `{"afk": true}` or `{"cancelled": true}` → apply the **safe** default (never `--force`), say in one line that you applied it unattended, and carry the unanswered choice into the final report.
   - `--force` requires an explicit human "force" answer. AFK, cancelled, or an autonomous session policy is never consent to force.
   - Four options, not three: **safe** / **no** / **force** / **bump only**. Bump only = edit `template_version` in `.template-meta.json` to the upstream version by hand and change nothing else (the script has no flag for it). Offer it when the diff is entirely noise — e.g. upstream stripping this project's customizations — and the user just wants the SessionStart prompt to stop.
3. **Apply.** `--apply` (safe) or `--apply --force` (destructive). Never pass `--force` unless the user explicitly chose it.
4. **Report — one sidecar at a time.** List every `<file>.upstream` written, then walk them individually: show `diff -u <file> <file>.upstream`, `ask` what to keep, edit `<file>`, then `trash <file>.upstream` (a safe-rm hook blocks `rm -f`; `/usr/bin/trash` is recoverable and prints nothing on success — exit 0 with no output means it worked, don't retry through `npx`/`bunx`). Never batch-diff, never cherry-pick on your own judgement, never delete all sidecars in one glob, and never install a dependency a sidecar implies without asking. If `ask` returns AFK/cancelled: leave every sidecar on disk untouched and list them as pending decisions — an unreviewed sidecar is not a decision you may make.
5. **Net-new files.** If the preview showed `other` files, add `--include-other` to the apply so they land as `.upstream` sidecars too — the rendered template lives in a temp dir that is gone afterwards, and the on-disk template still has unexpanded `{{cookiecutter.*}}` vars, so a sidecar is the only clean copy. Then `mv <file>.upstream <file>` for the ones worth having (agents, scripts, docs the project lacks), and `trash` the rest. Skip template skeleton files like `src/**` unless the user wants them. Recommend `just check` afterward.

## Retrofit projects

If `meta.retrofit` is true, the project's local files predate the template — seeds are guaranteed to differ. Do **not** offer force-overwrite as a casual default; lead with sidecars and manual merge.

## Opt-outs (detection only)

These silence the SessionStart *prompt*, not this skill: env `NO_TEMPLATE_UPDATE_CHECK=1` or sentinel `.claude/no-template-update-check`. If a user is annoyed by repeated prompts, point them here.
