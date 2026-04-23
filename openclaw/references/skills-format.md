# OpenClaw skill format

A "skill" in OpenClaw is a lightweight capability: a markdown `SKILL.md` file with YAML frontmatter, optionally bundled with scripts/templates. Distinct from Claude Code skills (this format has an `openclaw` metadata block in the frontmatter).

**Context.** Per `VISION.md`, skills are baseline-UX only. **New capabilities should ship as plugins, not skills.** Core skill additions require a strong product/security reason. Skills are still the right format for prompt workflows + shell-based tooling that don't need runtime registration.

## Install locations

| Scope | Path | Priority |
|---|---|---|
| Workspace | `<project>/skills/` | HIGHEST |
| Global | `~/.openclaw/skills/` | middle |
| Bundled | inside core repo `skills/` | lowest |

Resolution: **workspace > global > bundled**. Workspace always wins.

## Install methods

```bash
# Via CLI (ClawHub-backed)
openclaw skills install <slug>
openclaw skills install <slug> --version 1.2.3
openclaw skills install <slug> --force

# Manual — drop a folder into the right dir
cp -r my-skill ~/.openclaw/skills/
cp -r my-skill <project>/skills/

# Alternative — paste the skill's GitHub URL into the OpenClaw chat
# The agent handles the install automatically.
```

## SKILL.md frontmatter

Minimum:

```yaml
---
name: <slug>
description: "<what it does AND when to use it>"
---
```

With OpenClaw metadata block (as seen in bundled skills like `skills/github/SKILL.md`):

```yaml
---
name: github
description: "GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs. NOT for: complex web UI interactions requiring manual browser flows, bulk operations across many repos (script with gh api), or when gh auth is not configured."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["gh"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)"
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (apt)"
            }
          ]
      }
  }
---
```

### `metadata.openclaw` fields

| Field | Purpose |
|---|---|
| `emoji` | Icon shown in Skills settings / surfaces |
| `requires.bins` | Required binaries on PATH. `openclaw skills check` validates these. |
| `install[]` | Install descriptors for auto-dependency install. Each entry has `id`, `kind`, `bins`, `label`, plus kind-specific fields (`formula` for brew, `package` for apt, …). |

Skill body is free-form markdown. Convention: include `## When to Use` / `## When NOT to Use` sections so the assistant can quickly route between skills.

## Description field — triggering contract

The `description` IS the routing signal. Structure it as:
1. One sentence — what it does
2. "Use when:" — bullet list of triggers
3. "NOT for:" — bullet list of anti-triggers

The bundled `github` skill is the canonical example above.

## Body structure (pattern from bundled skills)

```markdown
# <Skill Name>

<One-paragraph overview.>

## When to Use
✅ USE this skill when:
- …

## When NOT to Use
❌ DON'T use this skill when:
- …

## Setup
<bin install, auth commands>

## Common Commands
<code blocks grouped by task>

## Templates
<reusable command snippets>

## Notes
<pitfalls, rate limits, flags>
```

## Debug / inspect

```bash
openclaw skills list                 # see what's loaded
openclaw skills list --eligible      # only skills that pass requires checks
openclaw skills info <name>          # deep dive on one
openclaw skills check                # surface missing bins/env/config
openclaw skills check --json         # machine-readable
```

## Publishing to ClawHub

Per `VoltAgent/awesome-openclaw-skills` CONTRIBUTING: only skills already published in the `github.com/openclaw/skills` repository are accepted into the awesome list. Publish there first — no personal repos / gists / external sources. PRs must include both the ClawHub link (`https://clawhub.ai/<user>/<slug>`) and the GitHub link (`https://github.com/openclaw/skills/tree/main/skills/<user>/<slug>`).

## Related docs

- `/tools/skills` — skills system overview
- `/tools/skills-config` — skills config reference
- `/tools/clawhub` — ClawHub integration details
- `/cli/skills` — `openclaw skills` CLI reference
