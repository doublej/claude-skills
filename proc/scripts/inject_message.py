#!/usr/bin/env python3
"""
Inject a message into a Claude Code tmux pane, as if the user typed it.
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime


def inject_message(message: str, target: str) -> bool:
    """Type message into the tmux pane `target` and press Enter."""
    for keys in (["-l", message], ["Enter"]):
        result = subprocess.run(["tmux", "send-keys", "-t", target, *keys], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject a message into a tmux pane")
    parser.add_argument("message", nargs="*", help="Message (default: auto-reminder)")
    parser.add_argument("-t", "--target", default=os.environ.get("TMUX_PANE"),
                        help="tmux pane id or session:window (default: $TMUX_PANE)")
    args = parser.parse_args()
    if not args.target:
        parser.error("no tmux target: run inside tmux or pass --target")
    msg = " ".join(args.message) or f"[Auto-reminder] Check system resources - {datetime.now().strftime('%H:%M')}"
    sys.exit(0 if inject_message(msg, args.target) else 1)
