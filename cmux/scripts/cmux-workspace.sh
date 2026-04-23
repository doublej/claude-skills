#!/usr/bin/env bash
# cmux-workspace.sh — spin up a whole project workspace from a single name.
#
# Resolution order for "what tabs does this workspace need?":
#   1. <project-path>/.cmux/workspace.json   (or --config <path>)
#   2. references/ecosystems.json            (by project name)
#   3. atlas API /api/projects               (single-project auto-derivation)
#   4. minimal fallback: one `code` tab at the project root
#
# Usage:
#   cmux-workspace.sh <project> [flags]
#
# Flags:
#   -r, --resume-claude     resume most recent Claude Code session in `code`
#   --continue-claude       use `claude -c` instead of resuming by id
#   --no-launch             create tabs + cd, but don't send launch commands
#   --layout <name>         override auto layout (single|code-dev|code-dev-logs|grid)
#   --config <path>         explicit workspace.json path, skips lookup
#   --dry-run               print plan as JSON, don't touch cmux
#
# Output (JSON on stdout):
#   { "workspace", "project", "source",
#     "tabs": [ { "role", "surface", "created", "launched", "resumed" }, ... ] }

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$SCRIPT_DIR/_lib.sh"

project=""
resume_claude=false
continue_claude=false
no_launch=false
layout_override=""
config_override=""
dry_run=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -r|--resume-claude)  resume_claude=true;  shift ;;
    --continue-claude)   continue_claude=true; shift ;;
    --no-launch)         no_launch=true;      shift ;;
    --layout)            layout_override="${2:-}"; shift 2 ;;
    --config)            config_override="${2:-}"; shift 2 ;;
    --dry-run)           dry_run=true;        shift ;;
    -h|--help)
      sed -n '3,27p' "$0"; exit 0 ;;
    -*)  _die "unknown flag: $1" ;;
    *)   [[ -z "$project" ]] && project="$1" || _die "too many args: $1"
         shift ;;
  esac
done
[[ -n "$project" ]] || _die "project name required"
$resume_claude && $continue_claude \
  && _die "--resume-claude and --continue-claude are mutually exclusive"

if ! $dry_run; then
  _require_cmux
else
  command -v jq >/dev/null 2>&1 || _die "jq required (brew install jq)"
fi

ATLAS_URL="${ATLAS_API:-http://localhost:47891}/api/projects"
DEV_ROOT="${DEV_ROOT:-$HOME/Documents/development}"
ECOSYSTEMS_JSON="$SCRIPT_DIR/../references/ecosystems.json"

# _resolve_project_path <name-or-path>
# Print absolute path to the project. Exit 1 if nothing plausible found.
# Order: literal path → ecosystem base → atlas → $DEV_ROOT/<arg>.
_resolve_project_path() {
  local arg="$1"
  if [[ -d "$arg" ]]; then
    (cd "$arg" && pwd); return 0
  fi
  # Ecosystem base
  if [[ -f "$ECOSYSTEMS_JSON" ]]; then
    local eco_base
    eco_base="$(jq -r --arg n "$arg" '.[$n].base // empty' "$ECOSYSTEMS_JSON")"
    if [[ -n "$eco_base" && -d "$DEV_ROOT/$eco_base" ]]; then
      printf '%s' "$DEV_ROOT/$eco_base"; return 0
    fi
  fi
  # Atlas
  local atlas_path
  atlas_path="$(curl -s --max-time 3 "$ATLAS_URL" 2>/dev/null \
    | jq -r --arg n "$arg" '.projects[] | select(.name == $n) | .path' \
    | head -1)"
  if [[ -n "$atlas_path" && -d "$atlas_path" ]]; then
    printf '%s' "$atlas_path"; return 0
  fi
  # Guess: $DEV_ROOT/<arg>
  if [[ -d "$DEV_ROOT/$arg" ]]; then
    printf '%s' "$DEV_ROOT/$arg"; return 0
  fi
  _die "cannot resolve project '$arg' — not a path, not in atlas, not at $DEV_ROOT/$arg"
}

# _atlas_project_json <name>
# Emit atlas project object as JSON or empty string.
_atlas_project_json() {
  local name="$1"
  curl -s --max-time 3 "$ATLAS_URL" 2>/dev/null \
    | jq -c --arg n "$name" '.projects[] | select(.name == $n)' \
    | head -1
}

# _derive_tabs_from_atlas <atlas-json> <base-path>
# Emit a tabs JSON array derived from atlas metadata. Never errors —
# returns minimal [{role:code}] if nothing useful can be inferred.
_derive_tabs_from_atlas() {
  local ap="$1" base="$2" cmd=""
  local runner framework has_just recipes
  runner="$(jq -r '.runner // ""' <<<"$ap")"
  framework="$(jq -r '.framework // ""' <<<"$ap")"
  has_just="$(jq -r '.hasJustfile // false' <<<"$ap")"
  recipes="$(jq -r '.justRecipes // [] | join(",")' <<<"$ap")"

  if [[ "$has_just" == "true" ]]; then
    if [[ ",$recipes," == *",dev,"* ]]; then cmd="just dev"
    elif [[ ",$recipes," == *",serve,"* ]]; then cmd="just serve"
    elif [[ ",$recipes," == *",run,"* ]]; then cmd="just run"
    fi
  fi
  if [[ -z "$cmd" ]]; then
    case "$framework" in
      sveltekit|nextjs|vite|astro|solid|remix)
        [[ "$runner" == "bun" ]] && cmd="bun dev" || cmd="npm run dev" ;;
      fastapi|django|flask)
        [[ "$runner" == "uv" ]] && cmd="" ;;  # no safe default
    esac
  fi

  if [[ -n "$cmd" ]]; then
    jq -n --arg cmd "$cmd" '[
      {role:"code", cwd:".", claudeResume:true},
      {role:"dev",  cwd:".", cmd:$cmd}
    ]'
  else
    jq -n '[{role:"code", cwd:".", claudeResume:true}]'
  fi
}

# _load_ecosystem_tabs <name>
# Emit {base, layout, tabs} if the project is a known ecosystem, else "".
_load_ecosystem_tabs() {
  local name="$1"
  [[ -f "$ECOSYSTEMS_JSON" ]] || { printf ''; return; }
  jq -c --arg n "$name" '.[$n] // empty' "$ECOSYSTEMS_JSON"
}

# _absolute_cwd <project-path> <tab-cwd>
# Resolve the tab's cwd (relative or absolute or ".") to an absolute path.
_absolute_cwd() {
  local base="$1" cwd="$2"
  case "$cwd" in
    /*) printf '%s' "$cwd" ;;
    ""|.) printf '%s' "$base" ;;
    *) printf '%s/%s' "$base" "$cwd" ;;
  esac
}

# _auto_layout <tabs-json>
# Pick a cmux layout that doesn't leave orphaned pre-created tabs. Only
# returns a non-single layout when every tab role overlaps with the
# layout's pre-named tabs.
_auto_layout() {
  local tabs="$1"
  local roles
  roles="$(jq -r '.[].role' <<<"$tabs" | sort -u | paste -sd, -)"
  case "$roles" in
    "code,dev,logs") printf 'code-dev-logs' ;;
    "code,dev")      printf 'code-dev' ;;
    *)               printf 'single' ;;
  esac
}

# _most_recent_session_id <project-cwd>
# Emit the sessionId of the most recent non-sidechain Claude session for
# this cwd, or empty if none.
_most_recent_session_id() {
  local cwd="$1" enc idx
  enc="$(_encode_cwd_for_claude "$cwd")"
  idx="$HOME/.claude/projects/$enc/sessions-index.json"
  [[ -f "$idx" ]] || { printf ''; return; }
  jq -r '.entries
           | map(select(.isSidechain==false))
           | sort_by(-.fileMtime)
           | .[0].sessionId // ""' "$idx" 2>/dev/null
}

# ── 1. Resolve project + load spec ──────────────────────────────────────

project_path="$(_resolve_project_path "$project")"
name="$(basename "$project_path")"

source="fallback"
spec=""

config_path="${config_override:-$project_path/.cmux/workspace.json}"
if [[ -f "$config_path" ]]; then
  source="config"
  spec="$(jq -c '.' "$config_path")"
fi

if [[ -z "$spec" ]]; then
  eco="$(_load_ecosystem_tabs "$name")"
  if [[ -n "$eco" ]]; then
    source="ecosystem"
    # Ecosystem base may override project_path
    eco_base="$(jq -r '.base // empty' <<<"$eco")"
    if [[ -n "$eco_base" ]]; then
      project_path="$DEV_ROOT/$eco_base"
      [[ -d "$project_path" ]] || _log "warn: ecosystem base $project_path missing"
    fi
    spec="$eco"
  fi
fi

if [[ -z "$spec" ]]; then
  ap="$(_atlas_project_json "$name")"
  if [[ -n "$ap" ]]; then
    source="atlas"
    tabs_json="$(_derive_tabs_from_atlas "$ap" "$project_path")"
    spec="$(jq -nc --argjson t "$tabs_json" '{tabs:$t}')"
  fi
fi

if [[ -z "$spec" ]]; then
  spec='{"tabs":[{"role":"code","cwd":".","claudeResume":true}]}'
fi

tabs_json="$(jq -c '.tabs' <<<"$spec")"
[[ "$tabs_json" != "null" && -n "$tabs_json" ]] \
  || _die "spec has no 'tabs' array (source: $source)"

# ── 2. Pick layout ──────────────────────────────────────────────────────

if [[ -n "$layout_override" ]]; then
  layout="$layout_override"
elif [[ "$(jq -r '.layout // ""' <<<"$spec")" != "" ]]; then
  layout="$(jq -r '.layout' <<<"$spec")"
else
  layout="$(_auto_layout "$tabs_json")"
fi

_log "source=$source  layout=$layout  project_path=$project_path  tabs=$(jq 'length' <<<"$tabs_json")"

# ── 3. Dry-run short-circuit ────────────────────────────────────────────

if $dry_run; then
  jq -nc \
     --arg project "$name" \
     --arg source "$source" \
     --arg layout "$layout" \
     --arg path "$project_path" \
     --argjson tabs "$tabs_json" \
     '{project:$project, source:$source, layout:$layout, projectPath:$path, tabs:$tabs, dryRun:true}'
  exit 0
fi

# ── 4. Create workspace ─────────────────────────────────────────────────

ws_out="$("$SCRIPT_DIR/cmux-project.sh" "$name" "$layout")"
ws_id="$(jq -r '.workspace' <<<"$ws_out")"
ws_created="$(jq -r '.created' <<<"$ws_out")"

# ── 5. Create tabs + launch ─────────────────────────────────────────────

results="[]"

tab_count="$(jq 'length' <<<"$tabs_json")"
for i in $(seq 0 $((tab_count - 1))); do
  tab="$(jq -c ".[$i]" <<<"$tabs_json")"
  role="$(jq -r '.role' <<<"$tab")"
  rel_cwd="$(jq -r '.cwd // "."' <<<"$tab")"
  cmd="$(jq -r '.cmd // ""' <<<"$tab")"
  auto_launch="$(jq -r '.autoLaunch // true' <<<"$tab")"
  claude_resume_spec="$(jq -r '.claudeResume // false' <<<"$tab")"
  abs_cwd="$(_absolute_cwd "$project_path" "$rel_cwd")"

  tab_out="$("$SCRIPT_DIR/cmux-tab.sh" "$name" "$role" "$abs_cwd")"
  surface="$(jq -r '.surface' <<<"$tab_out")"
  created="$(jq -r '.created' <<<"$tab_out")"

  launched=false
  resumed=false

  # Claude resume on the code tab
  if [[ "$role" == "code" ]]; then
    do_resume=false
    resume_cmd=""
    if $resume_claude; then
      do_resume=true
    elif $continue_claude; then
      do_resume=true
    elif [[ "$claude_resume_spec" == "true" && "$created" == "true" ]]; then
      do_resume=true
    fi

    if $do_resume && ! $no_launch; then
      if $continue_claude; then
        resume_cmd="claude -c"
      else
        sid="$(_most_recent_session_id "$abs_cwd")"
        if [[ -n "$sid" ]]; then
          resume_cmd="claude -r $sid"
        else
          _log "warn: no prior session for $abs_cwd — launching plain 'claude'"
          resume_cmd="claude"
        fi
      fi
      "$SCRIPT_DIR/cmux-send.sh" "$name" "$role" "$resume_cmd" --enter >/dev/null
      resumed=true
      launched=true
    fi
  fi

  # Generic cmd launch for non-resumed tabs
  if ! $resumed && [[ -n "$cmd" ]] && [[ "$created" == "true" ]] \
       && [[ "$auto_launch" == "true" ]] && ! $no_launch; then
    "$SCRIPT_DIR/cmux-send.sh" "$name" "$role" "$cmd" --enter >/dev/null
    launched=true
  fi

  entry="$(jq -nc \
    --arg role "$role" \
    --arg surface "$surface" \
    --argjson created "$created" \
    --argjson launched "$launched" \
    --argjson resumed "$resumed" \
    '{role:$role, surface:$surface, created:$created, launched:$launched, resumed:$resumed}')"
  results="$(jq -c --argjson e "$entry" '. + [$e]' <<<"$results")"
done

# ── 6. Emit final JSON ──────────────────────────────────────────────────

jq -nc \
   --arg workspace "$ws_id" \
   --arg project "$name" \
   --arg source "$source" \
   --arg layout "$layout" \
   --argjson wsCreated "$ws_created" \
   --argjson tabs "$results" \
   '{workspace:$workspace, project:$project, source:$source, layout:$layout, workspaceCreated:$wsCreated, tabs:$tabs}'
