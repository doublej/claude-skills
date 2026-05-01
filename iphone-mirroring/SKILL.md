---
name: iphone-mirroring
description: Drive the iPhone Mirroring macOS app (Sequoia+ / macOS 26+) as a vision agent. Capture the mirrored window, label UI elements with local OmniParser v2 on this Mac, reason with Gemma 4 on the home-network Ollama box (Fractal — `192.168.178.197:11434`) or Claude vision, actuate via cliclick + AppleScript (tap, swipe, type, hardware keys, app switcher, Spotlight). Use when the user asks to "control my iphone", "automate iphone via mac", "iphone mirroring automation", "drive iphone from claude", "vision agent iphone", or "omniparser iphone".
---

# iPhone Mirroring — Vision-Driven Agent

Drive the macOS **iPhone Mirroring** app (Sequoia+ / macOS 26+) like a real user.

```
capture (screencapture -l)                              [local: M2]
   ↓ PNG + window bounds
parse (OmniParser v2 server 127.0.0.1:8765)             [local: M2]
   ↓ JSON: [{id, bbox, label, interactable, type}] + annotated PNG
decide (Gemma 4 on Fractal, OR Claude vision)           [remote: 192.168.178.197 / cloud]
   ↓ {element_id, action, args?}
act (cliclick / AppleScript)                            [local: M2]
   ↓ pixel events into the mirrored window
verify (re-capture, re-parse, check goal)
   ↺ loop until goal or max steps
```

## When to use

The user wants Claude to **drive their actual iPhone** — open apps, tap, type, swipe, navigate. This is **not** the iOS Simulator (use `martingeidobler/ios-mcp-server` for that) and **not** Xcode/Appium device automation.

## Preflight (run once per machine)

1. **macOS 15+ (Sequoia) or 26+** — verify with `sw_vers -productVersion`.
2. **iPhone Mirroring is paired**: open the app once, accept on iPhone. Check `defaults read com.apple.ScreenContinuity onenessPairedDeviceID` is non-empty.
3. **Permissions** — see `references/permissions.md`. Required:
   - **Accessibility** for the terminal that runs `cliclick` (and for `osascript` → System Events).
   - **Screen Recording** for `screencapture`.
4. **Tools on M2**: `cliclick` (`brew install cliclick`), Python 3.11+, `uv`.
5. **OmniParser server** (local on M2) — see `references/omniparser-setup.md`. One-time clone + weights download. Then:
   ```bash
   bash scripts/serve_omniparser.sh   # binds 127.0.0.1:8765
   ```
   Health check: `curl -fsS http://127.0.0.1:8765/health`.
6. **Gemma 4 on Fractal** — Ollama lives on the Windows gaming PC (`192.168.178.197:11434`), reached over the home LAN. Health + model check:
   ```bash
   curl -fsS http://192.168.178.197:11434/v1/models | jq '.data[].id'
   # expect: "gemma4-64k:latest" (or a newer gemma4 tag)
   ```
   The skill calls Ollama's OpenAI-compatible endpoint at `/v1/chat/completions`. **Do not run Ollama on M2** — Fractal has the GPU.

`scripts/preflight.sh` runs all checks (local tools + remote Fractal Ollama) and exits non-zero if anything is missing.

## Workflow

### 1. Capture

```bash
bash scripts/capture.sh
# → /tmp/iphone-mirror/capture.png
# → /tmp/iphone-mirror/window.json   {"id": <int>, "x", "y", "w", "h", "scale"}
```

`capture.sh` resolves the window via AppleScript (process "iPhone Mirroring", window 1), captures via `screencapture -l <id>`, and writes bounds + retina scale used by `act.py` for coordinate translation.

### 2. Parse

```bash
uv run scripts/parse.py /tmp/iphone-mirror/capture.png
# → /tmp/iphone-mirror/elements.json
# → /tmp/iphone-mirror/annotated.png
```

`elements.json` is a list of:
```json
{"id": 7, "bbox": [x1, y1, x2, y2], "label": "Spotify icon", "type": "icon", "interactable": true}
```

### 3. Decide — pick a backend

**Default: Gemma 4 on Fractal (home LAN, free, private).**
```bash
uv run scripts/decide_gemma.py \
  --goal "Open Spotify" \
  --annotated /tmp/iphone-mirror/annotated.png \
  --elements /tmp/iphone-mirror/elements.json \
  --model gemma4-64k:latest
# → {"element_id": 7, "action": "tap"}
```

The script POSTs to `http://192.168.178.197:11434/v1/chat/completions` with the annotated PNG inlined as a base64 `image_url`. Override with `OLLAMA_URL` env var if Fractal moves.

**Fallback: Claude vision (this agent).** When Gemma is uncertain or the task is novel:
- Read the annotated PNG via the Read tool.
- Read `elements.json`.
- Reason about which `id` matches the goal and what `action` is needed.
- Output a single JSON line, hand to `act.py`.

Choose Claude when:
- Multi-step planning is required ("book a flight", "compose a long message").
- Visual reasoning is subtle (small icons, ambiguous labels, non-English UI).
- Gemma returns low confidence twice in a row.
- Fractal is offline / asleep — the skill will fail-fast on the connection check; switch with `--backend claude`.

### 4. Act

```bash
uv run scripts/act.py tap --id 7
uv run scripts/act.py swipe --from-id 7 --direction up
uv run scripts/act.py type --text "Hello world"
uv run scripts/act.py key --name home          # Cmd+1
uv run scripts/act.py key --name app-switcher  # Cmd+2
uv run scripts/act.py key --name spotlight     # Cmd+3
uv run scripts/act.py long-press --id 7 --ms 800
```

Coords come from `window.json` + `elements.json`. See `references/coordinate-translation.md` for the math (window origin offset + retina scale).

### 5. Loop

```bash
uv run scripts/loop.py --goal "Open Spotify and play Deftones" \
  --backend gemma --max-steps 12
```

`loop.py` orchestrates capture → parse → decide → act → verify, stopping when the model emits `{"action": "done"}` or `--max-steps` is hit. Trajectory written to `/tmp/iphone-mirror/run-<ts>/`. Backends: `gemma` (Fractal Ollama) | `claude` (in-session handoff).

## Decision tree

```
Is the iPhone Mirroring window frontmost and unlocked?
├─ no  → AppleScript: tell process "iPhone Mirroring" to activate; wait for window
└─ yes → continue

Is OmniParser server up at :8765?
├─ no  → bash scripts/serve_omniparser.sh & ; wait for /health
└─ yes → continue

Capture → Parse → has interactable elements?
├─ no  → swipe up (might be locked) or send Home key, retry once
└─ yes → Decide

Is Fractal reachable? curl http://192.168.178.197:11434/v1/models
├─ no  → backend = claude
└─ yes → backend = gemma (default)

Decide backend?
├─ gemma (default) → run decide_gemma.py against Fractal
│   ├─ confidence ≥ 0.6 → Act
│   └─ confidence < 0.6 → fall through to Claude vision
└─ claude vision → Read annotated.png + elements.json, output {id, action}

Act → re-Capture → did the screen change?
├─ no  → retry once with longer wait, then escalate
└─ yes → goal reached? loop or finish
```

## Permissions failure recipes

| Symptom | Cause | Fix |
|---|---|---|
| `screencapture` returns transparent PNG | Screen Recording perm missing | System Settings → Privacy → Screen Recording → enable terminal |
| `cliclick` clicks the wrong place | Accessibility perm missing | System Settings → Privacy → Accessibility → enable terminal |
| AppleScript: "Not authorized to send Apple events" | Automation perm missing | System Settings → Privacy → Automation → enable terminal → System Events |
| Window id not found | iPhone Mirroring not running | `open -a "iPhone Mirroring"` and wait 2s |

## References

| File | Use when |
|---|---|
| `references/permissions.md` | Setting up TCC perms or troubleshooting |
| `references/omniparser-setup.md` | First-time install, server crashes, model swap |
| `references/coordinate-translation.md` | Coords are off, retina/scaling debugging |
| `references/cliclick-cookbook.md` | Composing a new gesture (multi-finger, drag) |
| `references/iphone-mirroring-internals.md` | Window naming, hardware keys, app activation |

## Prior art

- microsoft/OmniParser (24.7k⭐) — vision parsing engine: https://github.com/microsoft/OmniParser
- OmniParser v2 weights: https://huggingface.co/microsoft/OmniParser-v2.0
- Technical-1/iPhone-Mirroring-Auto-Scripts (5⭐) — AppleScript+cliclick calibration pattern
- BlueM/cliclick — click/type CLI: https://github.com/BlueM/cliclick

## Constraints

- macOS Sequoia (15+) or Tahoe (26+) only.
- Both Apple devices on same Apple ID, Bluetooth + Wi-Fi on, iPhone within range.
- OmniParser server runs **on the M2** at `127.0.0.1:8765` (loopback only).
- Ollama / Gemma 4 runs **on Fractal** at `192.168.178.197:11434`. Fractal must be powered on. See the `homenetwork` skill for SSH/wake details.
- Model: `gemma4-64k:latest`. **Gemma 4, not 3.** If Fractal lists only `gemma3:*`, pull the v4 tag first (`ollama pull gemma4-64k:latest`) before running.
- iPhone Mirroring window must be visible when capturing — minimized windows return blank PNGs.
- iPhone forwards keystrokes to the focused field only; tap-to-focus first when typing.
