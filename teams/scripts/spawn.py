#!/usr/bin/env python3
"""
spawn.py — read a teams preset + emit a JSON spec the lead turns into
TeamCreate + Agent() calls.

Usage:
    python3 spawn.py <preset-name> [team-name]

Resolution order:
    1. $HOME/.claude/team-presets/<preset>.yaml   (user override)
    2. $SKILL_DIR/presets/<preset>.yaml           (bundled)
    3. unknown → invoke _consult.sh pick with the union of both sources.

Before emitting, runs preflight.sh and snapshot.sh. If preflight exits 2,
spawn.py aborts with the same code.

Output: a single JSON object printed to stdout. The lead parses it and
executes TeamCreate + Agent() per member.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import secrets
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("[teams:spawn] PyYAML not installed; run: pip install pyyaml\n")
    sys.exit(2)

SKILL_DIR = Path(os.environ.get("TEAMS_SKILL_DIR", Path.home() / ".claude/skills/teams"))
USER_PRESETS = Path.home() / ".claude/team-presets"
BUNDLED_PRESETS = SKILL_DIR / "presets"

ACCEPTED_MODELS = {"claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5"}
ACCEPTED_MODES = {"plan", "default", "acceptEdits", "dontAsk", "auto", "bypassPermissions"}
ACCEPTED_ISOLATION = {"worktree", "none"}
WRITABLE_TOOLS = {"Edit", "Write", "NotebookEdit"}


def log(msg: str) -> None:
    sys.stderr.write(f"[teams:spawn] {msg}\n")


def list_presets() -> dict[str, Path]:
    """Return a merged dict preset_name -> path, user overrides winning."""
    found: dict[str, Path] = {}
    for d in (BUNDLED_PRESETS, USER_PRESETS):
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.yaml")):
            if p.name == "_schema.yaml":
                continue
            found[p.stem] = p
    return found


def resolve_preset(name: str) -> Path:
    """Find a preset by name; fall back to consult pick on unknown."""
    user = USER_PRESETS / f"{name}.yaml"
    if user.is_file():
        return user
    bundled = BUNDLED_PRESETS / f"{name}.yaml"
    if bundled.is_file():
        return bundled
    # Unknown — ask user via _consult.sh
    presets = list_presets()
    if not presets:
        log("no presets installed.")
        sys.exit(2)
    consult = SKILL_DIR / "scripts/_consult.sh"
    opts = "|".join(sorted(presets.keys()))
    try:
        res = subprocess.run(
            [str(consult), "pick", f"Preset '{name}' not found. Pick one:", opts],
            capture_output=True, text=True, check=True,
        )
        chosen = res.stdout.strip()
    except subprocess.CalledProcessError:
        log(f"preset '{name}' not found and consult failed.")
        sys.exit(2)
    if not chosen or chosen not in presets:
        log(f"preset '{name}' not found; no fallback selected.")
        sys.exit(2)
    log(f"using preset '{chosen}' (user-selected fallback).")
    return presets[chosen]


def validate(preset: dict, name: str) -> None:
    errs: list[str] = []
    if preset.get("name") != name:
        errs.append(f"preset.name '{preset.get('name')}' != filename '{name}'")
    members = preset.get("members") or []
    if not members:
        errs.append("preset has no members")
    seen = set()
    write_access = bool(preset.get("write_access", False))
    for m in members:
        mn = m.get("name")
        if not mn:
            errs.append("a member has no name")
            continue
        if mn in seen:
            errs.append(f"duplicate member name: {mn}")
        seen.add(mn)
        if m.get("model") not in ACCEPTED_MODELS:
            errs.append(f"member {mn}: model '{m.get('model')}' not in {sorted(ACCEPTED_MODELS)}")
        if m.get("mode") not in ACCEPTED_MODES:
            errs.append(f"member {mn}: mode '{m.get('mode')}' not in {sorted(ACCEPTED_MODES)}")
        iso = m.get("isolation", "none")
        if iso not in ACCEPTED_ISOLATION:
            errs.append(f"member {mn}: isolation '{iso}' not in {sorted(ACCEPTED_ISOLATION)}")
        if write_access and iso != "worktree":
            errs.append(f"member {mn}: write_access=true requires isolation=worktree")
    if errs:
        for e in errs:
            log(f"validation error: {e}")
        sys.exit(2)


def run_preflight() -> None:
    script = SKILL_DIR / "scripts/preflight.sh"
    rc = subprocess.call(["bash", str(script)])
    if rc != 0:
        log(f"preflight failed (exit {rc}); aborting spawn.")
        sys.exit(rc if rc in (1, 2) else 2)


def run_snapshot(team_name: str) -> str:
    script = SKILL_DIR / "scripts/snapshot.sh"
    res = subprocess.run(
        ["bash", str(script), team_name],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        log(f"snapshot failed: {res.stderr.strip()}")
        sys.exit(2)
    tag = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else ""
    return tag or f"teams/{team_name}-snapshot"


def build_team_name(preset: dict, user_name: str | None) -> str:
    if user_name:
        return user_name
    prefix = preset.get("default_team_name_prefix") or preset.get("name") or "team"
    date = dt.date.today().isoformat()
    suffix = secrets.token_hex(2)
    return f"{prefix}-{date}-{suffix}"


def assemble_member(m: dict, team_name: str) -> dict:
    spawn_prompt = (m.get("spawn_prompt") or "").replace("{team_name}", team_name).strip()
    additional_tools = m.get("tools") or []
    agent_args = {
        "name": m["name"],
        "team_name": team_name,
        "subagent_type": m["subagent_type"],
        "model": m["model"],
        "mode": m["mode"],
        "isolation": m.get("isolation", "none"),
        "run_in_background": True,
        "prompt": spawn_prompt,
    }
    if additional_tools:
        agent_args["additional_tools"] = additional_tools
    return {"agent_args": agent_args, "initial_messages": [], "shutdown_on": m.get("shutdown_on", "explicit")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("preset")
    ap.add_argument("team_name", nargs="?", default=None)
    ap.add_argument("--skip-preflight", action="store_true", help="internal; tests only")
    ap.add_argument("--skip-snapshot", action="store_true", help="internal; tests only")
    args = ap.parse_args()

    preset_path = resolve_preset(args.preset)
    preset_name = preset_path.stem
    with preset_path.open() as f:
        preset = yaml.safe_load(f)

    validate(preset, preset_name)

    team_name = build_team_name(preset, args.team_name)

    if not args.skip_preflight:
        run_preflight()

    snapshot_tag = ""
    if not args.skip_snapshot:
        snapshot_tag = run_snapshot(team_name)

    spec = {
        "team_name": team_name,
        "preset_name": preset_name,
        "preset_path": str(preset_path),
        "snapshot_tag": snapshot_tag,
        "team_create_args": {"team_name": team_name},
        "members": [assemble_member(m, team_name) for m in preset["members"]],
        "lead_behavior": preset.get("lead_behavior", "").strip(),
        "coordination": preset.get("coordination", {}),
        "escalation": preset.get("escalation", {}),
        "hooks": preset.get("hooks", {}),
    }
    print(json.dumps(spec, indent=2))
    log(f"spec emitted for team '{team_name}' (preset={preset_name}, members={len(spec['members'])}).")
    log("lead must: 1) TeamCreate(team_create_args), 2) Agent(agent_args) per member, 3) send initial_messages, 4) implement lead_behavior.")


if __name__ == "__main__":
    main()
