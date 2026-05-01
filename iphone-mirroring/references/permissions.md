# macOS Permissions for iPhone Mirroring Automation

The skill needs three TCC (Transparency, Consent, Control) grants. macOS prompts for each on first use; if you dismiss or block, you must re-grant manually.

## Required grants

Grant **the terminal binary that actually launches the scripts** (e.g. `Ghostty.app`, `iTerm.app`, `Terminal.app`, `Warp.app`). If a script is launched from a different terminal than the one you granted, it will silently fail with no events delivered.

| Permission | Why | Where |
|---|---|---|
| **Accessibility** | `cliclick` posts mouse + keyboard events; `osascript` issues UI commands via System Events | System Settings → Privacy & Security → Accessibility |
| **Screen Recording** | `screencapture` reads pixels of the iPhone Mirroring window | System Settings → Privacy & Security → Screen Recording |
| **Automation → System Events** | AppleScript reads window id / position from the iPhone Mirroring process | System Settings → Privacy & Security → Automation → \<terminal\> → ✅ System Events |

## Smoke test

```bash
# Accessibility — if blocked, prints to stderr and posts nothing
cliclick p:.

# Screen Recording — should produce a non-zero PNG. A blank/transparent PNG = denied.
screencapture -x /tmp/_perm_test.png && file /tmp/_perm_test.png

# Automation → System Events — should print a number > 0
osascript -e 'tell application "System Events" to tell process "Finder" to count windows'
```

## Failure modes

| Failure | Diagnosis | Fix |
|---|---|---|
| `cliclick c:100,100` does nothing, no error | Accessibility blocked | Re-add terminal in Privacy → Accessibility, **toggle off then on** to re-prompt |
| Screenshot is empty / cursor only | Screen Recording blocked | Add terminal to Privacy → Screen Recording, **fully quit and relaunch** terminal |
| `Not authorized to send Apple events` (errAEEventNotPermitted) | Automation prompt was denied | Privacy → Automation → terminal → enable System Events checkbox |
| Permissions look correct but still fails after a macOS update | TCC db got reset | `tccutil reset Accessibility`, `tccutil reset ScreenCapture`, `tccutil reset AppleEvents`, then re-grant |

## Notes

- Granting permission to `python` directly does not work in 26+ — TCC tracks the parent app, not the interpreter.
- Running under SSH or a launchd agent has no GUI session and **cannot** receive these grants. Run interactively from a Terminal.app-class host.
- iPhone Mirroring itself does not need any extra grants beyond its first-launch pairing flow.
- `screencapture -l <id>` does **not** require the iPhone Mirroring window to be frontmost, but it must not be minimized.
