# cliclick Cookbook

`cliclick` (BlueM) — `brew install cliclick`. All coordinates are **screen logical points**, origin top-left of main display.

## Primitives

| Cmd | Meaning |
|---|---|
| `c:X,Y` | left click at X,Y |
| `cc:X,Y` | left double-click |
| `rc:X,Y` | right click |
| `dd:X,Y` | drag-down (mouse-down, hold) |
| `du:X,Y` | drag-up (mouse-up) |
| `m:X,Y` | move cursor without click |
| `t:string` | type literal text |
| `kp:name` | press a named key (e.g. `return`, `space`, `cmd`, `tab`) |
| `kd:name` | hold key down |
| `ku:name` | release key |
| `w:N` | wait N ms |
| `p` | print current cursor pos (debug) |

Multiple commands chain in one invocation:
```bash
cliclick m:200,400 dd:200,400 w:50 m:200,200 du:200,200
```

## Recipes

All examples assume coordinates have been resolved by `act.py`. Replace `$X $Y` accordingly.

### Tap

```bash
cliclick c:$X,$Y
```

### Long press (e.g. show context menu, app jiggle mode)

```bash
cliclick dd:$X,$Y w:800 du:$X,$Y
```

Tune `w:` (ms): 600–1200 for menu, 1500+ for jiggle mode.

### Swipe

iPhone Mirroring forwards mouse drags as touch swipes. Direction = end - start.

```bash
# Swipe up (next page / pull tab down)
cliclick m:$X,$Y_BOTTOM dd:$X,$Y_BOTTOM w:30 m:$X,$Y_TOP du:$X,$Y_TOP

# Faster flick (scroll a long list)
cliclick dd:$X,$Y_BOT w:20 m:$X,$Y_TOP du:$X,$Y_TOP
```

A move with no `w:` between dd and du is interpreted as a flick (high velocity). Insert `w:200+` to make it a slow drag (e.g. control center swipe).

### Type into a focused field

```bash
cliclick t:"Hello, world"
```

Caveats:
- `cliclick t:` types via the keyboard, so the iPhone field must be focused first (tap-to-focus).
- Quoted strings: shell-escape `"`, `\`, `$`. Or use `cliclick -m verbose t:` and pipe.
- Multi-line: send `\n` as `kp:return`:
  ```bash
  cliclick t:"first line" kp:return t:"second line"
  ```
- Unicode and emoji: works for BMP characters. For complex emoji or composed glyphs, prefer a paste flow:
  ```bash
  echo -n "🎉 hello" | pbcopy
  cliclick kd:cmd t:v ku:cmd
  ```

### Pinch / multi-touch

cliclick can't do multi-finger gestures. Use AppleScript with the iPhone Mirroring menu commands instead, or skip pinch (most apps offer non-pinch alternatives).

### Drag-and-drop

```bash
cliclick m:$SRC_X,$SRC_Y dd:$SRC_X,$SRC_Y w:300 m:$DST_X,$DST_Y w:200 du:$DST_X,$DST_Y
```

The `w:300` after `dd:` is the lift threshold — without it, the iPhone interprets the drag as a flick. `w:200` before `du:` lets the drop animation register.

## Timing reference

| Action | Wait after (ms) |
|---|---|
| Tap on Home Screen icon | 600 |
| Tap inside a busy app | 250 |
| Swipe between screens | 500 |
| Open Spotlight (Cmd+3) | 800 |
| Type one char | 30–50 |
| Long press to enter jiggle | 1500 then 400 to settle |

## Debugging

```bash
# Print where the cursor would land before clicking
cliclick -m verbose c:$X,$Y

# Watch what cliclick is doing in real time
cliclick m:$X,$Y w:1000 c:$X,$Y
# (cursor moves, you see it land on the right pixel before the click)
```
