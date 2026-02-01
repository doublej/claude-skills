#!/usr/bin/env python3
"""Run iTerm2 Python API commands from CLI arguments.

Usage: iterm2_run.py <command> [args...]

Commands:
  list-windows          List all windows with tabs and sessions
  list-profiles         List available profiles
  new-window [profile]  Create a new window
  new-tab [profile]     Create a new tab in current window
  split-h [profile]     Split current session horizontally
  split-v [profile]     Split current session vertically
  send [--session ID] <text>  Send text to session (default: current)
  read [--session ID] [lines] Read terminal output (default: current, 50 lines)
  focus-tab <id>        Focus a tab by ID
  focus-session <id>    Focus a session by ID
  close-tab <id>        Close a tab by ID
  close-session <id>    Close a session by ID
  set-title <title>     Set current tab title
  set-profile <name>    Change current session profile
  save-arrangement <n>  Save current layout as arrangement
  restore-arrangement   Restore a saved arrangement
  list-arrangements     List saved arrangements
  get-key-mappings      Get key mappings for current profile
  set-colors <preset>   Load a color preset
  set-font-size <size> [--profile name]  Set font size (all profiles+sessions, or specific profile)
  ctrl [--session ID] <char>  Send control char (e.g., C for Ctrl-C, M for Enter)
  find-self             Find this agent's iTerm2 session by TTY
  run [--session ID] <command> [--wait N]  Send command + Enter, wait, read output
  split-and-run [options] <command>  Split pane next to self, run command, return output
"""

import asyncio
import json
import os
import re
import subprocess
import sys

import iterm2


async def list_windows(connection, args):
    app = await iterm2.async_get_app(connection)
    result = []
    for w in app.windows:
        win = {"id": w.window_id, "tabs": []}
        for t in w.tabs:
            tab = {"id": t.tab_id, "sessions": []}
            for s in t.sessions:
                name = await s.async_get_variable("name") or ""
                path = await s.async_get_variable("path") or ""
                tab["sessions"].append({
                    "id": s.session_id,
                    "name": name,
                    "path": path,
                    "grid": f"{s.grid_size.width}x{s.grid_size.height}",
                })
            title = await t.async_get_variable("title") or ""
            tab["title"] = title
            tab["current"] = t == w.current_tab
            win["tabs"].append(tab)
        win["current"] = w == app.current_window
        result.append(win)
    print(json.dumps(result, indent=2))


async def list_profiles(connection, args):
    profiles = await iterm2.PartialProfile.async_query(connection)
    result = [{"name": p.name, "guid": p.guid} for p in profiles]
    print(json.dumps(result, indent=2))


async def new_window(connection, args):
    app = await iterm2.async_get_app(connection)
    profile = args[0] if args else None
    w = await iterm2.Window.async_create(connection, profile=profile)
    if w:
        print(json.dumps({"window_id": w.window_id}))


async def new_tab(connection, args):
    app = await iterm2.async_get_app(connection)
    w = app.current_window
    if not w:
        print(json.dumps({"error": "No current window"}))
        return
    profile = args[0] if args else None
    t = await w.async_create_tab(profile=profile)
    print(json.dumps({"tab_id": t.tab_id}))


async def split_pane(connection, args, vertical):
    app = await iterm2.async_get_app(connection)
    session = app.current_terminal_window.current_tab.current_session
    if not session:
        print(json.dumps({"error": "No current session"}))
        return
    profile = args[0] if args else None
    new = await session.async_split_pane(vertical=vertical, profile=profile)
    print(json.dumps({"session_id": new.session_id}))


async def resolve_session(app, args):
    """Extract --session ID from args. Returns (session, remaining_args)."""
    if len(args) >= 2 and args[0] == "--session":
        session = app.get_session_by_id(args[1])
        if not session:
            return None, args[2:]
        return session, args[2:]
    return app.current_terminal_window.current_tab.current_session, args


async def send_text(connection, args):
    app = await iterm2.async_get_app(connection)
    session, args = await resolve_session(app, args)
    if not session:
        print(json.dumps({"error": "Session not found"}))
        return
    if not args:
        print(json.dumps({"error": "No text provided"}))
        return
    await session.async_send_text(args[0])
    print(json.dumps({"sent": True}))


async def read_output(connection, args):
    app = await iterm2.async_get_app(connection)
    session, args = await resolve_session(app, args)
    if not session:
        print(json.dumps({"error": "Session not found"}))
        return
    lines = int(args[0]) if args else 50
    contents = await session.async_get_screen_contents()
    result = []
    for i in range(contents.number_of_lines):
        line = contents.line(i)
        result.append(line.string)
    output = "\n".join(result[-lines:])
    print(output)


async def focus_tab(connection, args):
    if not args:
        print(json.dumps({"error": "No tab ID"}))
        return
    app = await iterm2.async_get_app(connection)
    tab = app.get_tab_by_id(args[0])
    if tab:
        await tab.async_activate()
        print(json.dumps({"focused": args[0]}))
    else:
        print(json.dumps({"error": f"Tab {args[0]} not found"}))


async def focus_session(connection, args):
    if not args:
        print(json.dumps({"error": "No session ID"}))
        return
    app = await iterm2.async_get_app(connection)
    session = app.get_session_by_id(args[0])
    if session:
        await session.async_activate()
        print(json.dumps({"focused": args[0]}))
    else:
        print(json.dumps({"error": f"Session {args[0]} not found"}))


async def close_tab(connection, args):
    if not args:
        print(json.dumps({"error": "No tab ID"}))
        return
    app = await iterm2.async_get_app(connection)
    tab = app.get_tab_by_id(args[0])
    if tab:
        await tab.async_close(force=True)
        print(json.dumps({"closed": args[0]}))
    else:
        print(json.dumps({"error": f"Tab {args[0]} not found"}))


async def close_session(connection, args):
    if not args:
        print(json.dumps({"error": "No session ID"}))
        return
    app = await iterm2.async_get_app(connection)
    session = app.get_session_by_id(args[0])
    if session:
        await session.async_close(force=True)
        print(json.dumps({"closed": args[0]}))
    else:
        print(json.dumps({"error": f"Session {args[0]} not found"}))


async def set_tab_title(connection, args):
    if not args:
        print(json.dumps({"error": "No title provided"}))
        return
    app = await iterm2.async_get_app(connection)
    tab = app.current_terminal_window.current_tab
    await tab.async_set_title(args[0])
    print(json.dumps({"title": args[0]}))


async def set_profile(connection, args):
    if not args:
        print(json.dumps({"error": "No profile name"}))
        return
    app = await iterm2.async_get_app(connection)
    session = app.current_terminal_window.current_tab.current_session
    await session.async_set_profile_properties(
        iterm2.LocalWriteOnlyProfile()
    )
    print(json.dumps({"error": "Use set-profile with profile name via new-tab/split"}))


async def save_arrangement(connection, args):
    if not args:
        print(json.dumps({"error": "No arrangement name"}))
        return
    await iterm2.Arrangement.async_save(connection, args[0])
    print(json.dumps({"saved": args[0]}))


async def restore_arrangement(connection, args):
    if not args:
        print(json.dumps({"error": "No arrangement name"}))
        return
    await iterm2.Arrangement.async_restore(connection, args[0])
    print(json.dumps({"restored": args[0]}))


async def list_arrangements(connection, args):
    names = await iterm2.Arrangement.async_list(connection)
    print(json.dumps(list(names)))


async def get_key_mappings(connection, args):
    app = await iterm2.async_get_app(connection)
    session = app.current_terminal_window.current_tab.current_session
    profile = await session.async_get_profile()
    mappings = profile.key_mappings
    print(json.dumps(mappings or {}, indent=2, default=str))


async def set_colors(connection, args):
    if not args:
        print(json.dumps({"error": "No color preset name"}))
        return
    presets = await iterm2.ColorPreset.async_get_list(connection)
    if args[0] not in presets:
        print(json.dumps({"error": f"Preset '{args[0]}' not found", "available": presets}))
        return
    preset = await iterm2.ColorPreset.async_get(connection, args[0])
    app = await iterm2.async_get_app(connection)
    session = app.current_terminal_window.current_tab.current_session
    profile = await session.async_get_profile()
    await profile.async_set_color_preset(preset)
    print(json.dumps({"applied": args[0]}))


async def set_font_size(connection, args):
    if not args:
        print(json.dumps({"error": "No size provided. Usage: set-font-size <size> [--profile name]"}))
        return
    size = int(args[0])
    profile_filter = None
    if len(args) >= 3 and args[1] == "--profile":
        profile_filter = args[2]

    def _apply_size(font_string, new_size):
        return re.sub(r'\b\d+(\.\d+)?$', str(new_size), font_string)

    app = await iterm2.async_get_app(connection)
    updated = []
    for partial in await iterm2.PartialProfile.async_query(connection):
        if profile_filter and partial.name != profile_filter:
            continue
        full = await partial.async_get_full_profile()
        new_font = _apply_size(full.normal_font, size)
        await full.async_set_normal_font(new_font)
        updated.append({"name": full.name, "font": new_font})

    sessions_updated = 0
    for w in app.windows:
        for t in w.tabs:
            for s in t.sessions:
                profile = await s.async_get_profile()
                if profile_filter and profile.name != profile_filter:
                    continue
                new_font = _apply_size(profile.normal_font, size)
                await profile.async_set_normal_font(new_font)
                sessions_updated += 1

    print(json.dumps({"size": size, "profiles": updated, "sessions_updated": sessions_updated}, indent=2))


async def send_ctrl(connection, args):
    app = await iterm2.async_get_app(connection)
    session, args = await resolve_session(app, args)
    if not session:
        print(json.dumps({"error": "Session not found"}))
        return
    if not args:
        print(json.dumps({"error": "No character provided"}))
        return
    char = args[0].upper()
    code = ord(char) - 64
    await session.async_send_text(chr(code))
    print(json.dumps({"sent": f"Ctrl-{char}"}))


def _get_my_tty():
    """Get the TTY for this process by walking up the process tree."""
    pid = os.getpid()
    for _ in range(10):
        try:
            out = subprocess.check_output(
                ["ps", "-o", "tty=,ppid=", "-p", str(pid)]
            ).decode().strip()
            parts = out.split()
            if len(parts) < 2:
                break
            tty_short, ppid_str = parts[0], parts[1]
            if tty_short and tty_short != "??":
                return f"/dev/{tty_short}"
            pid = int(ppid_str)
            if pid <= 1:
                break
        except Exception:
            break
    return None


async def _find_self_session(app):
    """Find the session whose TTY matches this process's TTY."""
    my_tty = _get_my_tty()
    if not my_tty:
        return None, None
    for w in app.windows:
        for t in w.tabs:
            for s in t.sessions:
                s_tty = await s.async_get_variable("tty") or ""
                if s_tty == my_tty:
                    return s, {"session_id": s.session_id, "tab_id": t.tab_id,
                               "window_id": w.window_id, "tty": my_tty}
    return None, None


async def find_self(connection, args):
    app = await iterm2.async_get_app(connection)
    session, info = await _find_self_session(app)
    if not info:
        print(json.dumps({"error": "Could not find own session by TTY"}))
        return
    print(json.dumps(info))


async def run_command(connection, args):
    app = await iterm2.async_get_app(connection)
    session, args = await resolve_session(app, args)
    if not session:
        print(json.dumps({"error": "Session not found"}))
        return
    wait = 2
    command_text = None
    i = 0
    while i < len(args):
        if args[i] == "--wait" and i + 1 < len(args):
            wait = float(args[i + 1])
            i += 2
        elif command_text is None:
            command_text = args[i]
            i += 1
        else:
            i += 1
    if not command_text:
        print(json.dumps({"error": "No command provided"}))
        return
    await session.async_send_text(command_text + "\r")
    await asyncio.sleep(wait)
    contents = await session.async_get_screen_contents()
    lines = []
    for j in range(contents.number_of_lines):
        line = contents.line(j).string
        if line.strip():
            lines.append(line)
    print("\n".join(lines))


async def split_and_run(connection, args):
    app = await iterm2.async_get_app(connection)
    direction = True  # vertical by default
    title = None
    wait = 2
    source_session = None
    command_text = None
    i = 0
    while i < len(args):
        if args[i] == "--direction" and i + 1 < len(args):
            direction = args[i + 1] != "h"
            i += 2
        elif args[i] == "--session" and i + 1 < len(args):
            source_session = app.get_session_by_id(args[i + 1])
            i += 2
        elif args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--wait" and i + 1 < len(args):
            wait = float(args[i + 1])
            i += 2
        elif command_text is None:
            command_text = args[i]
            i += 1
        else:
            i += 1
    if not source_session:
        source_session, _ = await _find_self_session(app)
    if not source_session:
        source_session = app.current_terminal_window.current_tab.current_session
    if not source_session:
        print(json.dumps({"error": "No source session found"}))
        return
    new_session = await source_session.async_split_pane(vertical=direction)
    if title:
        for w in app.windows:
            for t in w.tabs:
                if new_session in t.sessions:
                    await t.async_set_title(title)
                    break
    if command_text:
        await new_session.async_send_text(command_text + "\r")
        await asyncio.sleep(wait)
    contents = await new_session.async_get_screen_contents()
    lines = []
    for j in range(contents.number_of_lines):
        line = contents.line(j).string
        if line.strip():
            lines.append(line)
    result = {"session_id": new_session.session_id}
    if title:
        result["title"] = title
    result["output"] = "\n".join(lines)
    print(json.dumps(result))


COMMANDS = {
    "list-windows": list_windows,
    "list-profiles": list_profiles,
    "new-window": new_window,
    "new-tab": new_tab,
    "split-h": lambda c, a: split_pane(c, a, vertical=False),
    "split-v": lambda c, a: split_pane(c, a, vertical=True),
    "send": send_text,
    "read": read_output,
    "focus-tab": focus_tab,
    "focus-session": focus_session,
    "close-tab": close_tab,
    "close-session": close_session,
    "set-title": set_tab_title,
    "set-profile": set_profile,
    "save-arrangement": save_arrangement,
    "restore-arrangement": restore_arrangement,
    "list-arrangements": list_arrangements,
    "get-key-mappings": get_key_mappings,
    "set-colors": set_colors,
    "set-font-size": set_font_size,
    "ctrl": send_ctrl,
    "find-self": find_self,
    "run": run_command,
    "split-and-run": split_and_run,
}


async def main(connection):
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    await COMMANDS[cmd](connection, args)


iterm2.run_until_complete(main)
