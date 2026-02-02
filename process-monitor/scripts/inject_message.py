#!/usr/bin/env python3
"""
Inject a message into Claude Code terminal using AppleScript.
This simulates typing a message as if the user typed it.
"""

import subprocess
import sys
from datetime import datetime


def inject_message(message: str, app_name: str = "Terminal"):
    """
    Inject message into the active terminal using AppleScript.
    Works with Terminal.app, iTerm2, Warp, or other terminal emulators.
    """
    # Escape special characters for AppleScript
    escaped = message.replace("\\", "\\\\").replace('"', '\\"')

    script = f'''
    tell application "{app_name}"
        activate
        delay 0.1
        tell application "System Events"
            keystroke "{escaped}"
            keystroke return
        end tell
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False
    return True


def inject_to_claude_code():
    """
    Inject the auto-reminder message to Claude Code.
    Tries to find the correct terminal app.
    """
    message = f"[Auto-reminder] Check system resources - {datetime.now().strftime('%H:%M')}"

    # Try common terminal apps
    for app in ["Terminal", "iTerm", "Warp", "Alacritty"]:
        if inject_message(message, app):
            return True

    return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        inject_message(msg)
    else:
        inject_to_claude_code()
