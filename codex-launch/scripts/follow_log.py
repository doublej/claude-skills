#!/usr/bin/env python3
"""Display a growing Codex log in a visible terminal.

`codex exec --json` events are rendered as a readable feed; any other line
passes through unchanged. The log file itself keeps the raw events.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

DIM, BOLD, RED, GREEN, CYAN, YELLOW, RESET = (
    "\033[2m", "\033[1m", "\033[31m", "\033[32m", "\033[36m", "\033[33m", "\033[0m")
SHELL_WRAP = re.compile(r"""^\S*/(?:ba|z)?sh -lc (['"])(.*)\1$""", re.S)


def clip(text, width=160):
    text = " ".join(str(text).split())
    return text if len(text) <= width else text[:width - 1] + "…"


def tail(output, lines=6):
    rows = output.rstrip().splitlines()[-lines:]
    return "".join(f"{DIM}    │ {clip(row, 150)}{RESET}\n" for row in rows)


def render_item(phase, item):
    kind = item.get("type")
    if kind == "agent_message" and phase == "item.completed":
        return f"\n{BOLD}Codex:{RESET} {item.get('text', '').strip()}\n\n"
    if kind == "reasoning" and phase == "item.completed":
        return f"{DIM}  thinking: {clip(item.get('text', ''), 300)}{RESET}\n"
    if kind == "command_execution":
        if phase == "item.started":
            command = SHELL_WRAP.sub(r"\2", item.get("command", ""))
            return f"{CYAN}$ {clip(command)}{RESET}\n"
        if phase == "item.completed":
            code, output = item.get("exit_code"), item.get("aggregated_output") or ""
            count = len(output.splitlines())
            if code == 0:
                return f"{DIM}  ✓ {count} lines{RESET}\n"
            return f"{RED}  ✗ exit {code} · {count} lines{RESET}\n" + tail(output)
    if kind == "file_change" and phase == "item.completed":
        return "".join(f"{YELLOW}  {c.get('kind', 'edit')}: {c.get('path')}{RESET}\n"
                       for c in item.get("changes", []))
    if kind == "web_search" and phase == "item.completed":
        action = item.get("action") or {}
        query = item.get("query") or action.get("pattern") or " | ".join(action.get("queries", []))
        return f"{CYAN}  search: {clip(query)}{RESET}\n"
    if kind == "mcp_tool_call":
        name = f"{item.get('server')}.{item.get('tool')}"
        if phase == "item.started":
            return f"{CYAN}  tool: {name}{RESET}\n"
        if item.get("error"):
            return f"{RED}  ✗ {name}: {clip(item['error'])}{RESET}\n"
    if kind == "todo_list" and phase != "item.started":
        return "".join(f"  [{'x' if t.get('completed') else ' '}] {t.get('text')}\n"
                       for t in item.get("items", []))
    if kind == "error":
        return f"{YELLOW}  ! {clip(item.get('message', ''), 300)}{RESET}\n"
    return ""


def render_line(line):
    """Return the display text for one raw log line."""
    try:
        event = json.loads(line)
    except ValueError:
        return line + "\n"
    if not isinstance(event, dict) or "type" not in event:
        return line + "\n"
    kind = event["type"]
    if kind.startswith("item."):
        return render_item(kind, event.get("item") or {})
    if kind == "thread.started":
        return f"{DIM}── thread {event.get('thread_id')}{RESET}\n"
    if kind == "turn.completed":
        usage = event.get("usage") or {}
        return (f"{GREEN}── turn done · in {usage.get('input_tokens', '?')} "
                f"(cached {usage.get('cached_input_tokens', '?')}) · "
                f"out {usage.get('output_tokens', '?')}{RESET}\n")
    if kind in ("turn.failed", "error"):
        message = (event.get("error") or {}).get("message") or event.get("message", "")
        return f"{RED}✗ {kind}: {message}{RESET}\n"
    return ""


def follow_log(args):
    print(f"{args.label}\nLog: {args.log}\nClose this window to stop watching.\n", flush=True)
    if args.ready_file:
        args.ready_file.touch()
    pending = ""

    def drain(final=False):
        nonlocal pending
        pending += stream.read()
        *lines, pending = pending.split("\n")
        if final and pending:
            lines, pending = lines + [pending], ""
        sys.stdout.write("".join(render_line(line) for line in lines))
        sys.stdout.flush()

    with args.log.open(encoding="utf-8", errors="replace") as stream:
        while True:
            drain()
            if args.exit_file and args.exit_file.exists():
                drain(final=True)
                code = args.exit_file.read_text().strip()
                print(f"\nCodex finished (exit {code}). Log retained.", flush=True)
                return
            time.sleep(0.25)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("exit_file", nargs="?", default="")
    parser.add_argument("label", nargs="?", default="Codex live monitor")
    parser.add_argument("ready_file", nargs="?", default="")
    args = parser.parse_args()
    args.exit_file = Path(args.exit_file) if args.exit_file else None
    args.ready_file = Path(args.ready_file) if args.ready_file else None
    return args


if __name__ == "__main__":
    follow_log(parse_args())
