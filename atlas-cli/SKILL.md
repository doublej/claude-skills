---
name: atlas-cli
description: "Find an existing project or start a new one with the `atlas` CLI — search/jump/info, scaffold via `atlas new`, branch flow, ports. Use whenever the question is \"where does this project live?\", \"do we already have X?\", or \"create a new project\"."
---

<presentation>
Reference skill: no banner, no report. When invoked directly and the answer is the main output, end with: — atlas-cli · github.com/doublej
</presentation>

<when>

Trigger on any of:

- "where is <project>", "do I have a project for X", "find the repo that…", "open/cd to <project>"
- "start a new project", "scaffold X", "new sveltekit/rust/python app"
- "what does atlas know about this folder", "which port", "what branch flow"

Never hand-roll `find ~/dev` or `ls` sweeps — the atlas scan already has it.

</when>

<finding>

```bash
atlas <query>            # search by name — same as `atlas search <query>`
atlas info               # atlas's record for the cwd project (--json for the raw Project)
atlas info --json        # path, type, framework, runner, git, scripts, deploy, domains, flow
atlas scan               # force a rescan when a folder is missing from results
```

Search prints `name  category/path`, relative to `~/dev`. It matches a substring of the folder name, not keywords: `atlas personal-homepage` finds `personal-homepage-simple`, `atlas "personal simple"` finds nothing. No match prints `No projects matching …` and exits 1; retry with one word of the name before concluding it doesn't exist.

A query that is also a subcommand (`disk`, `info`, `scan`, `flow`, `ports`, `tags` — full list in `atlas help`) runs that command instead. Use `atlas search <query>` for those, and in scripts generally.

**Telling the user how to get there:** `atlas jump <query>` (alias `pj`) cds *their* shell — suggest it as `pj <query>`, don't run it yourself (a child process can't cd the parent). To run something in a project without cd-ing, use `atlas jump <query> --run '<cmd>'`.

Nothing found and it might be archived? Anything under `_archive/` is excluded by design — ask before resurrecting it.

</finding>

<creating>

```bash
atlas templates                                            # families/names available
atlas new <family>/<name> --name <project> --category <cat> # non-interactive
atlas new                                                   # interactive pickers
atlas new typescript/sveltekit --name foo --var key=val      # extra cookiecutter context
```

Order of work:

1. `atlas search <name>` first — confirm it doesn't already exist.
2. `atlas templates` — pick the family/name that matches the stack. STATUS `warns` (currently on every template) is template-authoring lint such as y/n choice order or a template missing from `shared/templates.json`; it says nothing about the generated project, so use the template. Deeper template detail lives in the `cookiecutter-templates` skill.
3. `--category <dir>` picks the depth-1 folder under `~/dev` (e.g. `web`, `python`, `rust`). Pick from what's already there (`ls ~/dev` is the category index; that one-level `ls` is fine); don't invent a category, and never `ai/`, `vr/`, or `sim/`.
4. `atlas new` creates the repo, the scaffold commit, and `develop` — the project is born on the flow and appears in atlas immediately. Don't `git init` or `mkdir` by hand.

</creating>

<adjacent>

```bash
atlas init          # write .atlas metadata into an existing folder atlas mis-detects
atlas flow          # branch flow of this project (feature/* → develop → main → tag)
atlas flow init     # opt an existing repo in (--dry-run first)
atlas ports         # port collisions across daemons and projects
atlas tree view     # the CLAUDE.md context chain for this folder
atlas prime         # crash course: commands, workflows, guardrails — run this first
atlas brief         # session briefing (already wired as a SessionStart hook)
```

</adjacent>

<notes>

- Everything is a thin client to the atlas-api on :47891. A connection error means the daemon is down — `launchctl kickstart com.jurrejan.atlas-api` (no `-k`), then retry.
- The scan caches for 60s (`~/dev/.atlas-cache.json`). A just-created folder that doesn't show up → `atlas scan`.
- `atlas` with an unrecognised first word is a search, so a typo'd subcommand silently searches instead of erroring. Check `atlas help` if a command "returns nothing".

</notes>
