# iPhone Mirroring — Internals

Notes on the macOS app itself, the bits that aren't documented anywhere else and that you only learn by poking at it.

## Process and bundle

| Item | Value |
|---|---|
| Bundle ID | `com.apple.ScreenContinuity` |
| Process name | `iPhone Mirroring` |
| App path | `/System/Applications/iPhone Mirroring.app` |
| Window 1 title | The iPhone's name (e.g. "Jurre's iPhone") |

## Activation

```applescript
tell application "iPhone Mirroring" to activate
delay 0.3
tell application "System Events"
    tell process "iPhone Mirroring"
        set frontmost to true
        repeat until exists window 1
            delay 0.1
        end repeat
    end tell
end tell
```

If the iPhone is locked, the window shows a connecting / unlock prompt. The skill should detect this state by:
- `elements.json` contains a `Face ID` icon or a `Slide to unlock` text element.
- Recovery: send Home key (`cliclick kd:cmd t:1 ku:cmd`) and re-capture; if still locked, surface a message — the user has to authenticate on the phone.

## Window-id resolution

```applescript
tell application "System Events" to tell process "iPhone Mirroring" to get id of window 1
-- → integer
```

The id is stable for the lifetime of the window. It changes when the user closes and reopens the window or switches between paired phones (rare).

## Hardware key shortcuts

iPhone Mirroring exposes these via the menu bar (View / Device menus). cliclick's `kd:cmd t:1 ku:cmd` form invokes them as keyboard shortcuts:

| Action | Shortcut | cliclick |
|---|---|---|
| Home / lock screen | `Cmd+1` | `cliclick kd:cmd t:1 ku:cmd` |
| App Switcher | `Cmd+2` | `cliclick kd:cmd t:2 ku:cmd` |
| Spotlight (search) | `Cmd+3` | `cliclick kd:cmd t:3 ku:cmd` |
| Notifications (pull down) | `Cmd+Shift+1` | `cliclick kd:cmd kd:shift t:1 ku:shift ku:cmd` |
| Control Center | `Cmd+Shift+2` | `cliclick kd:cmd kd:shift t:2 ku:shift ku:cmd` |
| Back (one level up, where supported) | `Cmd+[` | `cliclick kd:cmd t:[ ku:cmd` |

`act.py key --name <home|app-switcher|spotlight|notifications|control-center|back>` wraps these.

## Audio routing

Audio from iPhone apps routes to the Mac's default output **only when iPhone Mirroring is the frontmost window** in macOS 15. macOS 26+ keeps audio routed even when the window is in the background. Don't rely on audio routing for state detection — it's not exposed via any API the skill can query.

## Session lifecycle

- iPhone Mirroring drops the connection if:
  - The iPhone is unlocked and used directly by a person (10s grace).
  - The iPhone leaves Bluetooth range or sleeps.
  - macOS sleeps.
- Reconnect path: `open -a "iPhone Mirroring"` brings the window back; the iPhone may show a "Reconnect" prompt requiring a tap on the phone.
- The skill should treat repeated capture-with-no-elements as a likely disconnect and surface that to the user rather than retrying forever.

## Things to avoid

- **Don't open the menu bar mid-loop** — the dropdown overlays elements and confuses OmniParser. Use keyboard shortcuts.
- **Don't resize the window while a loop is running** — every cached coordinate becomes wrong. If you must resize, recapture before acting.
- **Don't use AppleScript `click at {x,y}`** to click into the iPhone — it sends the click to the macOS coordinate, which iPhone Mirroring re-translates inconsistently. Always use cliclick.
- **Don't run two loops in parallel against the same window** — they will fight each other. One agent per window.
