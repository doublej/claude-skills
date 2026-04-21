#!/usr/bin/env bash
# install.sh — post-install for the teams skill. Idempotent.
#
# What it does:
#   1. Verify the skill is symlinked at ~/.claude/skills/teams.
#   2. Copy commands/*.md  → ~/.claude/commands/teams/
#   3. Copy hooks/*.sh     → ~/.claude/hooks/teams/    (chmod +x)
#   4. Backup ~/.claude/settings.json + jq-merge hook entries (no duplicates).
#   5. Create ~/.claude/team-presets/ + README.md.
#   6. Print a "restart Claude Code" notice.

set -euo pipefail

say() { printf "[teams:install] %s\n" "$*" >&2; }

CLAUDE_DIR="$HOME/.claude"
SKILL_LINK="$CLAUDE_DIR/skills/teams"
CMD_DST="$CLAUDE_DIR/commands/teams"
HOOK_DST="$CLAUDE_DIR/hooks/teams"
PRESETS_DST="$CLAUDE_DIR/team-presets"
SETTINGS="$CLAUDE_DIR/settings.json"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 1. Sanity check symlink.
if [[ ! -L "$SKILL_LINK" ]] && [[ ! -d "$SKILL_LINK" ]]; then
  say "skill is not installed at $SKILL_LINK."
  say "run ./install-skill.sh teams from the claude-skills repo first."
  exit 2
fi

# 2. Copy commands.
mkdir -p "$CMD_DST"
if compgen -G "$SKILL_ROOT/commands/*.md" >/dev/null; then
  cp -f "$SKILL_ROOT"/commands/*.md "$CMD_DST/"
  say "copied commands → $CMD_DST"
fi

# 3. Copy hooks.
mkdir -p "$HOOK_DST"
if compgen -G "$SKILL_ROOT/hooks/*.sh" >/dev/null; then
  cp -f "$SKILL_ROOT"/hooks/*.sh "$HOOK_DST/"
  chmod +x "$HOOK_DST"/*.sh
  say "copied hooks → $HOOK_DST"
fi

# 4. Hook merge.
if ! command -v jq >/dev/null 2>&1; then
  say "jq not installed — skipping hook merge. Install jq to enable safety gates."
else
  mkdir -p "$CLAUDE_DIR"
  if [[ ! -f "$SETTINGS" ]]; then
    echo '{}' > "$SETTINGS"
  fi
  BACKUP="$SETTINGS.pre-teams-$(date +%Y%m%dT%H%M%S)"
  cp -f "$SETTINGS" "$BACKUP"
  say "backed up settings → $BACKUP"

  TMP="$(mktemp)"
  # Use jq to idempotently add hook entries. `source` marker keeps our entries identifiable.
  jq --arg base "$HOOK_DST" '
    def ensure_key(k): if has(k) then . else .[k] = {} end;
    def upsert_hook(event; matcher; cmd):
      .hooks[event] |= (. // []) |
      (.hooks[event] | map(select(.command == cmd)) | length) as $already |
      if $already == 0 then
        .hooks[event] += [
          (if matcher != null
            then {matcher: matcher, hooks: [{type: "command", command: cmd, source: "teams-skill"}]}
            else {hooks: [{type: "command", command: cmd, source: "teams-skill"}]}
          end)
        ]
      else . end;

    ensure_key("hooks")
    | upsert_hook("PreToolUse";    "Agent"; "\($base)/preflight-agent.sh")
    | upsert_hook("TaskCreated";   null;     "\($base)/task-created.sh")
    | upsert_hook("TaskCompleted"; null;     "\($base)/task-completed.sh")
    | upsert_hook("TeammateIdle";  null;     "\($base)/teammate-idle.sh")
  ' "$SETTINGS" > "$TMP"

  if jq . "$TMP" >/dev/null 2>&1; then
    mv "$TMP" "$SETTINGS"
    say "merged hooks into $SETTINGS"
  else
    rm -f "$TMP"
    say "hook merge produced invalid JSON; settings left untouched. Backup: $BACKUP"
    exit 2
  fi
fi

# 5. Presets dir.
mkdir -p "$PRESETS_DST"
if [[ ! -f "$PRESETS_DST/README.md" ]]; then
  cat > "$PRESETS_DST/README.md" <<'EOF'
# ~/.claude/team-presets/

Drop `<name>.yaml` files here to override bundled presets or add new ones.

- Schema: `~/.claude/skills/teams/presets/_schema.yaml`
- Full guide: `~/.claude/skills/teams/references/preset-authoring.md`

User overrides win over bundled presets on name collision.
List all presets: `/teams:list`.
EOF
  say "created $PRESETS_DST/README.md"
fi

say "install complete."
say "Restart Claude Code to activate hooks."
