#!/usr/bin/env python3
"""Restart the calling Claude Code session in its own terminal pane and resume it.

Spawns a detached watcher that waits, SIGTERMs the claude process, waits for it to
exit, then types `cd <cwd> && claude <original flags> --resume <id> <prompt>` into
the same iTerm2 session or tmux pane. macOS only (argv comes from KERN_PROCARGS2).
"""

import argparse
import ctypes
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

DEFAULT_PROMPT = (
    "You were just restarted by the self-restart skill. Check that the reason for the "
    "restart took effect, then continue where you left off."
)
# Flags that pick or fork the conversation; the relaunch sets --resume itself.
DROP_FLAGS = {"-r", "--resume", "-c", "--continue", "--session-id", "--fork-session", "--from-pr"}
# Option lines in `claude --help` are indented exactly two spaces; wrapped description lines are not.
OPTION_LINE = re.compile(r"^  ((?:-\w, )?--[\w-]+(?:, --[\w-]+)*)(?: (<[^>]+>|\[[^\]]+\]))?", re.M)


def find_claude_pid():
    pid = os.getppid()
    while pid > 1:
        ppid, comm = subprocess.run(
            ["ps", "-o", "ppid=,comm=", "-p", str(pid)], capture_output=True, text=True, check=True
        ).stdout.split(None, 1)
        if Path(comm.strip()).name == "claude":
            return pid
        pid = int(ppid)
    sys.exit("self-restart: no ancestor process named 'claude'; run this from a Claude Code Bash tool call")


def read_argv(pid):
    """Exact argv of pid; `ps -o args` joins with spaces and loses quoting."""
    libc = ctypes.CDLL(None, use_errno=True)
    mib = (ctypes.c_int * 3)(1, 49, pid)  # CTL_KERN, KERN_PROCARGS2
    size = ctypes.c_size_t(0)
    if libc.sysctl(mib, 3, None, ctypes.byref(size), None, 0):
        raise OSError(ctypes.get_errno(), "sysctl KERN_PROCARGS2 size")
    buf = ctypes.create_string_buffer(size.value)
    if libc.sysctl(mib, 3, buf, ctypes.byref(size), None, 0):
        raise OSError(ctypes.get_errno(), "sysctl KERN_PROCARGS2")
    argc = int.from_bytes(buf.raw[:4], sys.byteorder)
    rest = buf.raw[4 : size.value]
    rest = rest[rest.index(b"\0") :].lstrip(b"\0")  # skip exec path and its padding
    return [a.decode() for a in rest.split(b"\0")[:argc]]


def read_flag_arity():
    """Map each flag to None (boolean), 'one', 'opt' ([value]) or 'many' (<values...>)."""
    help_text = subprocess.run(["claude", "--help"], capture_output=True, text=True, check=True).stdout
    arity = {}
    for names, value in OPTION_LINE.findall(help_text):
        kind = None if not value else "many" if "..." in value else "opt" if value[0] == "[" else "one"
        for name in re.findall(r"--?[\w-]+", names):
            arity.setdefault(name, kind)
    return arity


def keep_flags(args, arity):
    """Drop positionals (the original first prompt) and conversation-picking flags."""
    kept, i = [], 0
    while i < len(args):
        token, i = args[i], i + 1
        if not token.startswith("-"):
            continue
        name, taken = token.split("=", 1)[0], [token]
        kind = None if "=" in token else arity.get(name)
        if kind == "one" and i < len(args):
            taken.append(args[i])
            i += 1
        elif kind in ("opt", "many"):
            while i < len(args) and not args[i].startswith("-"):
                taken.append(args[i])
                i += 1
                if kind == "opt":
                    break
        if name not in DROP_FLAGS:
            kept += taken
    return kept


def read_cwd(pid):
    out = subprocess.run(["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"], capture_output=True, text=True, check=True)
    return next(line[1:] for line in out.stdout.splitlines() if line.startswith("n"))


def build_send_command(line):
    # Ctrl-U first: claude's exit leaves terminal replies (e.g. a cursor report "45;3;1R") in the shell's line buffer.
    if pane := os.environ.get("TMUX_PANE"):  # before iTerm2: typing into iTerm would hit the active tmux pane
        return "tmux", ["tmux", "send-keys", "-t", pane, "C-u", line, "Enter"]
    if session := os.environ.get("ITERM_SESSION_ID"):
        return "iterm2", ["it2", "run", "-s", session.split(":")[-1], "\x15" + line]
    return None, None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="first message after resume; '' resumes idle")
    parser.add_argument("--delay", type=float, default=5, help="seconds before SIGTERM, so the current turn can end")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, do not restart")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    opts = parser.parse_args()

    session_id = os.environ.get("CLAUDE_CODE_SESSION_ID") or sys.exit("self-restart: CLAUDE_CODE_SESSION_ID is not set")
    pid = find_claude_pid()
    argv = read_argv(pid)
    flags = keep_flags(argv[1:], read_flag_arity())
    if "-p" in flags or "--print" in flags:
        sys.exit("self-restart: headless (-p) session, there is no pane to restart in")
    command = ["claude", *flags, "--resume", session_id] + ([opts.prompt] if opts.prompt else [])
    line = f"cd {shlex.quote(read_cwd(pid))} && {shlex.join(command)}"
    target, send = build_send_command(line)

    log = Path(os.environ.get("TMPDIR", "/tmp")) / "self-restart" / f"{session_id}.log"
    plan = {"session_id": session_id, "pid": pid, "argv": argv, "target": target, "command": line, "log": str(log)}
    if not target:
        plan["error"] = "not in iTerm2 or tmux; quit claude and run `command` yourself"
    if opts.dry_run or not target:
        print(json.dumps(plan, indent=2) if opts.json else "\n".join(f"{k}: {v}" for k, v in plan.items()))
        sys.exit(0 if target else 1)

    # ponytail: fixed delay, not a turn-ended signal; a Stop hook could trigger it exactly if the tail of a turn gets cut.
    watcher = f"""
sleep {opts.delay}
kill -TERM {pid}
for _ in $(seq 100); do kill -0 {pid} 2>/dev/null || break; sleep 0.2; done
if kill -0 {pid} 2>/dev/null; then echo "claude {pid} still running after 20s, not relaunching"; exit 1; fi
sleep 1
{shlex.join(send)} && echo relaunched
"""
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w") as out:
        subprocess.Popen(
            ["bash", "-c", watcher], stdin=subprocess.DEVNULL, stdout=out, stderr=out, start_new_session=True
        )
    plan["restart_in_seconds"] = opts.delay
    print(json.dumps(plan, indent=2) if opts.json else f"Restarting in {opts.delay:g}s via {target}. Log: {log}")


if __name__ == "__main__":
    main()
