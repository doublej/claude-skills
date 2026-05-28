# Anti-Patterns: 14 Traps That Make a TUI Feel Cheap

For each: the name, the cause-of-death (one line), what to do instead,
and the diagnostic (how to spot it in your own code).

---

## 1. Emoji confetti

**Cause of death.** Emojis render at inconsistent widths across
terminals; even when they render at all, they shift column alignment
and break the grid.

**Do instead.** Unicode block elements and geometric glyphs:
`▲ ✓ ● ◆ ▶`. Single-codepoint, fixed-width, predictable. Never
multi-codepoint sequences (ZWJ — `👨‍💻`).

**Diagnostic.** Grep your source for the emoji range:
`rg '[\x{1F300}-\x{1FAFF}]'`. Anything matching is suspect. If a
designer insisted on one, prove it renders at 1 cell wide on the
target terminals before shipping.

---

## 2. The figlet ritual

**Cause of death.** ASCII banners on every launch announce nothing,
slow startup, novelty wears off in two runs. The tenth time the user
launches your tool, the banner is friction.

**Do instead.** Print art at install or on `--version`. Or never. The
first frame of a TUI should be the working UI.

**Diagnostic.** Does your app print more than three lines of chrome
before showing the actual interface? If yes, the banner has to go.

---

## 3. Mouse-only handoffs

**Cause of death.** Click targets without keyboard equivalents lock
out SSH sessions, screen readers, and muscle memory. Half the user
base can't use what the keyboard can't reach.

**Do instead.** Every click target has a keybind. Mouse is enhancement
on top of a keyboard-complete app, never the only path in.

**Diagnostic.** Unplug your mouse. Try the primary task. Anything you
can't do is an accessibility bug at minimum and a usability bug at
ceiling.

---

## 4. Indeterminate spinners that lie

**Cause of death.** A braille spinner on a job that knows its progress
is a confession that you were too lazy to wire up the progress bar.

**Do instead.** Progress bar for determinate work. Status text
("step 2 of 5") for known step counts. Spinner *only* for genuinely
indeterminate work, *only* after a 200ms delay.

**Diagnostic.** Does your spinner have a known total or step count?
If yes, it's a progress bar in denial.

---

## 5. Mixed border weights

**Cause of death.** Heavy beside light beside rounded reads as render
confusion, not affordance. The user assumes their terminal is broken.

**Do instead.** One weight per surface. One accent weight per screen
maximum, used to mark *one* focused thing. Rounded only for ephemeral
surfaces (modals, toasts). Double banned for body.

**Diagnostic.** Count distinct border styles on the primary screen.
More than two is a fail.

---

## 6. Hidden keybinds

**Cause of death.** Muscle memory beats novelty — but only if the
keys are discoverable. A TUI with hidden bindings is a TUI nobody
masters.

**Do instead.** Footer always shows the relevant keys for the current
mode. `?` opens full help. The footer is the spec — write it before
the layout.

**Diagnostic.** Can a stranger complete the primary task using only
what's visible on screen? If they need to read a manual to navigate,
the navigation has failed.

---

## 7. Truecolor as a requirement

**Cause of death.** Your beautiful 24-bit palette dies in tmux-256, in
SSH sessions to older servers, in CI logs, in any terminal that lies
about its capabilities. Truecolor is enhancement, never floor.

**Do instead.** Design at 256-color first. Enhance to truecolor when
detected. Fall to 16 when forced. Strip on `NO_COLOR`. Every theme
defines all four mappings.

**Diagnostic.** Run with `TERM=xterm-256color` and again with
`NO_COLOR=1`. Both must produce a working, readable UI. Run inside a
fresh tmux session — does it survive?

---

## 8. Twitch motion

**Cause of death.** Continuous decorative animation is noise the user
can't turn off. After 60 seconds it's an interruption, not a delight.

**Do instead.** Motion proves causality. One beat per screen, max.
No looping decorative motion. Respect a `--no-animation` flag.

**Diagnostic.** Does anything move when the user isn't doing anything?
If yes, it's twitch motion. Kill it.

---

## 9. Double-painted lines

**Cause of death.** When two adjacent panels both draw the shared
edge, the line renders heavier than the rest of the layout. Reads as
a render bug even when intentional.

**Do instead.** The atlas-picker maneuver. Only one panel draws the
shared edge. iocraft `Edges::Bottom` on the upper panel, no top edge
on the lower. Same line, painted once.

**Diagnostic.** Zoom into the borders where two panels meet. Heavier
than the rest of the line? Doubled. Compare against a single-panel
border in the same screen — they should match weight.

---

## 10. The TUI-shaped flag-based CLI

**Cause of death.** Not every interactive thought needs a frame. If
`cmd | jq` plus `--watch` would do the job, a TUI is overkill — and
you've blocked piping, scripting, and CI use.

**Do instead.** Ship the pipe. Or ship both — the TUI as opt-in, the
pipe as default. The TUI must justify the frame.

**Diagnostic.** Write the equivalent shell pipeline. Is the TUI
actually better, or are you decorating output that didn't need it?
If `--json | jq` is faster for the user, ship that path too.

---

## 11. Color as the sole carrier of meaning

**Cause of death.** Roughly 8% of men are red/green colorblind.
`NO_COLOR=1` users get nothing. State distinguished only by hue
fails for a meaningful portion of your users.

**Do instead.** Pair color with shape, label, or position. `✓ pass`
not just green text. `✗ fail` not just red text. Color is reinforcement,
never the only signal.

**Diagnostic.** Print the screen in monochrome (or screenshot then
desaturate). Does state still read? If "all the items look the same
without color," color was carrying meaning that the design didn't.

---

## 12. Re-printing the entire screen every frame

**Cause of death.** Causes flicker, breaks scrollback, slow on SSH.
The terminal's job is to be fast; full clears throw the speed away.

**Do instead.** Diff the render tree; overwrite cells that changed.
Every modern TUI library does this — make sure you're using its diff
path, not bypassing with `clear()` calls. Synchronized Output protocol
(begin/end with DCS sequences) eliminates tearing where supported.

**Diagnostic.** Scroll up after a state change. Did history survive,
or is the scrollback now full of redrawn screens? If the latter,
you're full-clearing.

---

## 13. Unicode no-fallback strategies

**Cause of death.** Boxes assembled with `─│┌┐` crater on cp1252,
basic SSH clients, log scrapers, and CI viewers that lie about their
encoding. Your users on those clients see `???|+++`.

**Do instead.** Support an `--ascii` mode that uses `+-|` plus 7-bit
text. Or detect `LANG=C` / `LC_ALL=C` and degrade automatically. The
ASCII version doesn't need to look as good — just legible.

**Diagnostic.** Pipe the output through `iconv -t ASCII//TRANSLIT`.
Survives? Then your fallback works. Crashes or shows replacement
chars? You don't have one.

---

## 14. Hardcoded ANSI escapes

**Cause of death.** A `\033[31m` in the source bypasses theming, ignores
`NO_COLOR`, defies capability detection, and locks the color forever.
The token layer can't help what doesn't go through it.

**Do instead.** Every color call routes through the token module. The
token module knows how to degrade — to 256, to 16, to none. The rest
of the app names tokens; only the module knows escape codes.

**Diagnostic.** `rg '\\033\[|\\x1b\['` outside the token module. None
should exist. The token module is the only place ANSI escapes are
allowed to live.

---

## Diagnostic checklist summary

A 5-minute scan to spot most of these in someone else's TUI (or
your own):

- `rg '[\x{1F300}-\x{1FAFF}]'` — emoji codepoints anywhere
- count distinct border styles on the primary screen — over 2 is a fail
- run with `NO_COLOR=1` — does hierarchy survive?
- run at 80×24 — does the primary task still work?
- run with the mouse unplugged — can you complete the primary task?
- resize the terminal mid-session — does layout reflow, selection
  stay in view?
- screenshot, then desaturate — does state still read in monochrome?
- `rg '\\033\[|\\x1b\['` outside the token module — should be empty
- `cmd | jq --watch` test — would the pipe have done it?

Five minutes. Catches twelve of the fourteen.
