# Skill consolidation plan

Date: 2026-07-12 · Status: **EXECUTED 2026-07-12** (all phases; ~15 commits).
Deviations from plan: `git/` deleted rather than flattened (duplicated existing git
slash-skills); legacy `install-codex-skills-interactive.sh` deleted (superseded by
`install-skill.sh --codex`); `skill-description-audit.md` + `xml-prompt-writing-evaluation.md`
deleted (stale snapshots, in git history); proc merge unified enumeration in Python as
planned; hook paths in `~/.claude/settings.json` repointed to `skill-feedback-loop`.
Left for a human call: `~/.claude/skills/google-sheets-sync` (bundles a hand-rolled TS
implementation that repo `cms-sheets` lacks — predecessor, don't delete blindly);
never-tracked dirs `aeo-geo/`, `build-macos-apps/`, `drunk-claude/` (add to git or ignore).
Follow-up to NAMING.md (57 renames, executed 2026-05-28). This pass is about
**deleting superseded skills, merging overlapping ones, and standardizing
scripts + descriptions**. Evidence gathered by 7 parallel analysis agents over
all 148 skill dirs.

Guiding goal (JJ, 2026-07-12): converge on **"throw it at a codebase" skills** —
one entry point where the user picks dimensions (folder organisation, CLAUDE.md
tree, smells, logging, modularity, docs, …) and agents optimize + fix. The
code-* merges below are shaped toward that, not just tidiness.

---

## Phase 1 — Hygiene (no skill behavior changes) · reclaims ~820 MB

| Action | Target | Size | Notes |
|---|---|---|---|
| delete (untracked) | `pixijs-dev/default/` incl. `.venv` | 591M | Stray **Maya1 TTS + browser-use project**, zero PixiJS content. `.venv` unrecoverable after delete — it's rebuildable junk. Also `git rm -r --cached` the 33 tracked files (`default/.idea/`, `default/maya1/`, `__pycache__/*.pyc`) |
| delete (untracked) | `code-map/scripts/repomap/.venv` | 145M | `setup.sh` rebuilds on first run; SKILL.md already says "auto-installs" |
| delete + untrack | `dist/` | 81M | Built `.skill` bundles (`codebase-mapper.skill` alone 75M); rebuild with `package_skill.py` when needed |
| delete + untrack | `backup_2024_12_12/` | 388K | Dated backup, recoverable from git history |
| delete | `tmp/` | 900K | Scratch (naming plan draft + stray PNG) |
| delete | `code-taxonomy/` | 0 | Empty husk from the → ubiquitous-language rename |
| delete + untrack | `skill-index-manager/` | 7.9M | Abandoned scaffold: no SKILL.md, no source, tracked `node_modules/` |
| untrack | 12 `.DS_Store`, 4 `.pyc` | — | Already gitignored but tracked, so rules don't bite → constant git-status noise |
| gitignore | `.beads/backup/`, `*.darc` | — | 100 untracked backup files polluting git status |
| move | `templates/` → `skill-creator/references/templates/` | 44K | Only real content among the loose dirs |
| move or delete | `pixi_data/` | 1.2M | Scraped PixiJS doc JSON; belongs under `pixijs/` if still used as build input |

## Phase 2 — Delete superseded duplicates (hub already replaced them)

The `pdf` and `pixijs` hubs **declare in their own frontmatter** that they
replace the satellites, and their `references/` are byte-identical unions of
the satellites' references. The satellites were simply never deleted.

| Delete | Superseded by | Check first |
|---|---|---|
| `pdf-reportlab/`, `pdf-icc/`, `ghostscript/` | `pdf/` (719-line unified hub) | Spot-check pdf's Color branch vs `pdf-icc` (the one satellite richer than its branch); refs are byte-identical |
| `pixijs-dev/`, `pixijs-debug/`, `pixijs-perf/` | `pixijs/` (unified hub) | pixijs-dev SKILL.md is a 36-line stub; nothing lost |
| `prompt/` (double-nested `prompt/prompt/SKILL.md`) | `prompt-crafter` | Orphaned by the prompt-* rename; not installed |
| `git/` (double-nested `git/git/SKILL.md`) | — | Decide: flatten as `git-workflow` or delete. Name `git` would collide with `.git` if flattened as-is |

Every deletion must also remove the `~/.claude/skills/<name>` and
`~/.codex/skills/<name>` symlinks (ghostscript, pixijs-dev are live symlinks).

## Phase 3 — Merges (8 → kill ~9 dirs, 3 trigger collisions)

| Merge | Into | Why | Risk |
|---|---|---|---|
| `prompt-gpt51` + `prompt-gpt52` | `prompt-gpt` (5.2 body + 5.1 delta section) | ~85 % verbatim overlap; gpt52 already structured as superset with delta/migration tables. Kills a coin-flip trigger collision | low |
| `prompt-xml` | `prompt-crafter/references/xml-patterns.md` | crafter already carries a condensed copy and links to it; descriptions claim the same surfaces → live trigger collision | low; also remove the stale `xml-prompt` copy-dir in `~/.claude/skills` |
| `logo-create` + `logo-mathematical` + `logo-systematic` | `logo` (3 construction modes) | Brief, banned-elements, color table, checklist duplicated verbatim ×3; worst trigger collision in the repo ("make me a logo" = coin flip) | low — keep both generator scripts + preview.html as mode assets |
| `skill-feedback-collector` + `skill-feedback-optimizer` | one `skill-feedback-loop` (collect/optimize) | Producer/consumer over the same beads queue (`source:auto-analysis`) | keep optimizer's `/loop`-friendly trigger wording; `skill-feedback` (iTerm2 handoff) stays separate |
| `write-email` | `writer` (fold `scripts/clean.py` into message modes) | All prose already in writer verbatim; only clean.py is unique | low |
| `swarm` | `teams/references/primitives.md` | swarm is a bare SKILL.md with empty scripts/references; teams already links it as its doc dependency; 3-way spawn-model drift confuses agents | update teams' pointer |
| `proc-cleanup` + `proc-monitor` | `proc` (scan/monitor/kill) | Same scan logic duplicated in bash + python; authored as a pair | only merge if enumeration unifies into one implementation |
| `code-refactor` + `code-simplify` + `full-optimize` | **`code-optimize`** — see Phase 4 | full-optimize is a script-less orchestrator chaining the others via **stale pre-rename names** (broken today); refactor/simplify duplicate language-detect + mapper boilerplate | medium — this is a rebuild, not a paste-merge |

**Keep, but re-scope descriptions (trigger disambiguation, no merge):**
- `design-frontend` (default generalist) vs `design-director` (opt-in persona) — currently both own "distinctive, non-generic UI"
- `ui-readable` (type/spacing/tokens only) vs `ui-usability` (canonical review home; absorb the duplicated form/label/validation guidance)
- `diagram-ascii` vs `diagram-mermaid` — add a medium cue ("text/terminal" vs "rendered") to both descriptions
- `tui-kit` vs `tui-monospace` — de-collide "terminal app"
- `agent-orchestrator` — re-scope to subagents/Task-DAG patterns only; strip stale teammate content (missing TeamCreate + env flag) and point at `teams`
- `claude-skill` — rename to `claude-headless` (name reads as "skill authoring", content is `-p` automation)

## Phase 4 — Build the "throw at a codebase" umbrella (NEW)

Target architecture for the code-* family: **one dispatcher + dimension skills.**

```
code-optimize  (user picks dimensions; fans out agents; fixes; atomic commits)
├── structure   → folder organisation (NEW dimension — no skill covers this today)
├── claude-md   → claude-md-tree (exists)
├── smells      → code-audit over code-map's RepoMap engine (exists)
├── simplify    → behavior-preserving simplification (from code-simplify)
├── modularize  → code-modularize (exists)
├── logging     → code-logging (exists)
├── arch        → code-arch-drift (exists)
├── glossary    → code-glossary (exists)
└── docs        → audit-docs (exists, lives outside repo)
```

- `code-optimize` replaces `full-optimize` + `code-refactor` + `code-simplify`.
  Zero-input default = all dimensions; args select subsets (`/code-optimize smells logging`).
- Dimension skills stay standalone (each still individually invocable) but expose a
  consistent contract: scan script with `--json`, findings → plan → fix → verify → commit.
- **New work:** the `structure` (folder organisation) dimension needs writing.

## Phase 5 — Fix broken cross-references & stale content

| File | Problem |
|---|---|
| `code-audit/analyze.py` (~line 14) | Hardcodes `../codebase-mapper/scripts/repomap.sh` (pre-rename) → never resolves, silently falls back to PATH |
| `full-optimize/SKILL.md:21-24`, `code-refactor/SKILL.md:60,70,119`, `code-audit/SKILL.md:89` | Invoke `codebase-mapper`, `repomap-analyzer`, `dev-refactor`, `codebase-simplify` — all renamed 2026-05-28 |
| `tmux/scripts/tmux-init.sh:64-69`, `tmux/SKILL.md:52,177` | Call `iterm2/scripts/iterm2_run.py` which **was never committed** (`iterm2/scripts/` is empty); auto-visibility silently degrades |
| `iterm2/SKILL.md:198-233` ≡ `tmux/SKILL.md:219-253` | Word-for-word duplicated "Remote Windows Hosts (SSH/SCP)" section → extract one shared reference |
| ~~`prompt-crafter/SKILL.md:10,30-35` + `references/lint-opus*.md`~~ | ~~Lint targets stop at opus-4-7/4-6; no template for current models~~ — **done**: routes + templates added for fable-5, opus-5, sonnet-5, gpt-5.6; `lint-sonnet.md` → `lint-sonnet-4-6.md` |
| `skill-usage-tracker/SKILL.md:107` | Claims PostToolUse hook lives in repo `.claude/settings.json`; it's actually in global `~/.claude/settings.json` |
| Hooks: `track_usage.py` + `mark_skill.sh` | Both parse the same PostToolUse(Skill) payload independently → single marker writer, two consumers |

Add a repo CI-ish check (script in `skill-creator/scripts/`): every path a SKILL.md
references must exist, and no SKILL.md may reference a pre-rename skill name.

## Phase 6 — Standardize scripts, frontmatter, install

**Scripts (house style — document in skill-creator):**
- Python: `#!/usr/bin/env python3`, **argparse** (22 hand-rolled `sys.argv` scripts are outliers), positional root path, `--json` flag for machine output
- Bash: `#!/usr/bin/env bash` + `set -euo pipefail` (mixed `#!/bin/bash`/`set -e` today; 2 scripts have neither)
- One Python runner convention (`python3` vs `uv run` currently mixed)
- Machine output = JSON; kill ad-hoc sentinel lines (`IMAGE_PATH:` in codex-image)
- SKILL.md invokes scripts by **installed absolute path** (`~/.claude/skills/<name>/scripts/…`), not cwd-relative — teams is the model
- One emoji-free output convention (welcome_stats.py is the lone emoji outlier)

**Frontmatter:** all 148 have `name` + `description` ✓, zero folder mismatches ✓.
Canonicalize optional keys to `allowed-tools` + `metadata`; drop the singletons
(`version`, `tags`, `author`, `invocation`, …).

**Description formula** (fixes the trigger collisions systematically):
`<what it does> + <when to use> + <distinguishing cue vs siblings> + <trigger phrases>` —
every family member must name what its siblings do NOT cover.

**install-skill.sh:** add an explicit `.skillignore` skip-list (junk dirs are
currently skipped only by luck of missing SKILL.md).

**~/.claude/skills drift:** 12 dirs installed as **copies, not symlinks**
(`ascii-art`, `modularize`, `xml-prompt`, `mcp-agent-router`, `terminal-ux`, …) —
stale pre-rename names among them; reinstall via install-skill.sh or delete the
renamed-away ones. Foreign `programme-design` symlink points into dj-mix-builder —
leave (managed elsewhere) or adopt.

---

## Tally

- **Delete:** 7 junk dirs + 6 superseded skills + 2 mis-nested dirs ≈ **~820 MB reclaimed**, 148 → ~133 dirs
- **Merge:** 8 merges collapse 9 more dirs → **~124 skills**, 3 live trigger collisions eliminated
- **Build:** `code-optimize` umbrella + `structure` dimension (the "throw at a codebase" goal)
- **Fix:** 7 broken/stale reference clusters
- **Standardize:** script conventions, description formula, `.skillignore`, symlink reinstall

## Execution order & risk

1. Phase 1 hygiene — safe, biggest disk win, do first (venv deletes are the only unrecoverable ones and both are rebuildable)
2. Phase 2 deletes — verify hub coverage (pdf color branch), then delete + unlink
3. Phase 5 reference fixes — cheap, unblocks code-* family immediately
4. Phase 3 merges — one commit per merge, reinstall symlinks each time
5. Phase 4 code-optimize rebuild — the real project; do after the family is clean
6. Phase 6 standardization — sweep last, add the reference-integrity check to keep it clean
