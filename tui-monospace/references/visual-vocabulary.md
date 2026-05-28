# Visual Vocabulary

The terminal's grammar in detail. SKILL.md cites this; this is where
the charts live.

## Box drawing

Full Unicode chart with codepoints. Memorize the four families.

### Light (default — almost everything)

```
─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
```

Codepoints: U+2500 U+2502 U+250C U+2510 U+2514 U+2518 U+251C U+2524
U+252C U+2534 U+253C.

### Heavy (one focused thing per screen)

```
━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋
```

Codepoints: U+2501 U+2503 U+250F U+2513 U+2517 U+251B U+2523 U+252B
U+2533 U+253B U+254B.

### Rounded (ephemeral surfaces only — toasts, modals, hints)

```
╭ ╮ ╰ ╯
```

Codepoints: U+256D U+256E U+2570 U+256F. Pair with light sides.

### Double (banned for body, accent only)

```
═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
```

Codepoints: U+2550 U+2551 U+2554 U+2557 U+255A U+255D U+2560 U+2563
U+2566 U+2569 U+256C. If you must use them, one accent line per screen,
maximum.

### T-junctions and connector resolution

When adjacent panels share an edge, junctions become explicit:
`├ ┤ ┬ ┴ ┼` for light, `┣ ┫ ┳ ┻ ╋` for heavy. Mix-weight junctions
exist (`╞ ╤ ╧ ╪`) but are render-fragile in many terminals — avoid.

### The atlas-picker maneuver, in a diagram

Two stacked panels. Naive approach draws the shared edge twice:

```
┌──────────────┐    ← upper panel bottom
│  Panel A     │
└──────────────┘    ← drawn here
┌──────────────┐    ← AND drawn here — collision
│  Panel B     │
└──────────────┘
```

Fix: only one panel draws the shared edge. iocraft's `Edges::Bottom`
on the upper panel, no top edge on the lower:

```
┌──────────────┐    Edges::Top | Edges::Left | Edges::Right | Edges::Bottom
│  Panel A     │
├──────────────┤    one line, painted once
│  Panel B     │
└──────────────┘    Edges::Left | Edges::Right | Edges::Bottom
```

### Mixing rules

- Never mix weights inside one box.
- Mix between focused and unfocused panels for affordance: focused
  panel uses heavy, others use light.
- Rounded only for ephemeral surfaces — modals, toasts, hover hints.
  A rounded body panel reads as "marketing landing page TUI."

---

## Block elements

### Bars (1/8 increments, sub-cell resolution)

```
▏▎▍▌▋▊▉█
```

Codepoints: U+258F U+258E U+258D U+258C U+258B U+258A U+2589 U+2588.
Use cases: meters (btop, bottom), sparklines, progress with precision.
One bar style per widget.

### Shading (atmospheric depth)

```
░ ▒ ▓ █
```

Codepoints: U+2591 U+2592 U+2593 U+2588. Pick *one* intensity per
surface. Mixing reads as glitch.

### Half-blocks (2× vertical resolution)

```
▀ ▄
```

Codepoints: U+2580 U+2584. For graphs and pixel-style art that needs
double the vertical resolution of the cell grid. The "Sextants" block
(U+1FB00–U+1FB3F) gives 6× resolution but render support is uneven —
verify before depending.

---

## Glyph palette

### Status

```
● ○ ◐ ◯ ✓ ✗ ⚠
```

Codepoints: U+25CF U+25CB U+25D0 U+25EF U+2713 U+2717 U+26A0.

### Direction

```
▲ ▼ ◀ ▶ ↑ ↓ ← →
```

Codepoints: U+25B2 U+25BC U+25C0 U+25B6 U+2191 U+2193 U+2190 U+2192.

### Selection

`▌` (U+258C, half-block bar) or `▶` (U+25B6, caret). Pick one across
the entire app. Two selection styles in one product reads as
inconsistency, not variety.

### Scroll indicators

`▲` and `▼` shown only when overflow is possible. Drawing them when
content fits is a lie. atlas-picker's scroll-keep rule: when content
fits, no indicator; when it overflows, show direction *and* keep the
selection inside the visible window across resizes.

### Wait

Braille spinner: `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏` (U+280B U+2819 U+2839 U+2838 U+283C
U+2834 U+2826 U+2827 U+2807 U+280F). Cycle at 80–120ms. Suppress
until 200ms have elapsed since the work started.

### Separators

```
· ─ │
```

Codepoints: U+00B7 (middle dot, inline separator), U+2500 (en-rule,
full-width), U+2502 (vertical bar). Pick one per context.

### Truncation

`…` — U+2026, single codepoint. Never `...` (three periods). The
ellipsis is a typographic mark, not a sentence fragment.

### Banned

Emoji 🚀 ✨ 🔥 ✅ ❌ ⭐ 💯. The U+1F300–U+1FAFF range plus the
ZWJ-sequence emoji (👨‍💻 etc.) render at random widths on stranger
machines, alignment dies, and the effect is "I downloaded a TUI
template." Geometric glyphs (◆ ● ▲) are emoji's drop-in replacement.

---

## Themes

### Eleven semantic tokens (every theme defines all eleven)

```
bg              page background
surface         primary panel background
panel           elevated panel / overlay background
fg              primary text
fg-muted        secondary text, metadata
fg-subtle       tertiary text, hints
accent          primary brand color
accent-muted    accent variant for non-emphasized elements
success         success state
warning         warning state
error           error state
```

Optional: `focus` (when distinct from `accent`).

### Default themes (full RGB)

**Catppuccin Mocha (dark)**
```
bg            #1e1e2e
surface       #181825
panel         #313244
fg            #cdd6f4
fg-muted      #a6adc8
fg-subtle     #6c7086
accent        #89b4fa
accent-muted  #74c7ec
success       #a6e3a1
warning       #f9e2af
error         #f38ba8
```

**Catppuccin Latte (light)**
```
bg            #eff1f5
surface       #e6e9ef
panel         #ccd0da
fg            #4c4f69
fg-muted      #6c6f85
fg-subtle     #8c8fa1
accent        #1e66f5
accent-muted  #209fb5
success       #40a02b
warning       #df8e1d
error         #d20f39
```

**Tokyo Night (dark, recommended)** — atlas-picker's default. See
`multi-stack/project-atlas/atlas-picker/src/theme.rs:30` for the full
struct, RGB-by-RGB.

**Rosé Pine (dark, recommended)** — atlas-picker also ships this.

### COLORFGBG auto-detect (the atlas-picker pattern)

Many terminals export `COLORFGBG=fg;bg` where `fg` and `bg` are 0–15
ANSI indices. The trailing field tells you the perceived background
brightness. Algorithm:

```
1. Read COLORFGBG from env.
2. Split on ';'. Take the trailing field.
3. Parse as u8.
4. If parsed and >= 7, use the light theme.
5. Otherwise (parsed and < 7, or missing, or unparseable), use the
   dark theme.
```

Rust source for reference: atlas-picker
`src/theme.rs:129–139`. Twelve lines. No reason not to.

### ANSI 16-color fallback per token

When the terminal can't do 256 or truecolor, every token degrades to
one of 16. Pick deliberately — auto-fallbacks are usually wrong.

```
bg            black              (or default — let terminal decide)
surface       black              (slightly brighter if available)
panel         bright-black
fg            white              (or default)
fg-muted      bright-black
fg-subtle     bright-black
accent        cyan               (or theme's hero color)
accent-muted  blue
success       green
warning       yellow
error         red
```

### NO_COLOR env var

`NO_COLOR=1` is a hard off-switch. Every color call routes through the
token layer; the token layer checks `NO_COLOR` and short-circuits to
unstyled. Hierarchy survives via weight (bold), reverse video, and
position. If hierarchy collapses without color, the design was
color-dependent — not designed.

---

## Spacing rules

- **2 cols horizontal padding inside panels.** atlas-picker default.
- **The breathing-room move.** Selected list item gets one empty row
  *above* and one *below*, both painted in the row's surface color.
  Focus indicated by space first, color second. atlas-picker
  `ui.rs:994` — the selected row is rendered as a 3-row block.
- **1 cell between inline items.** Tags, glyphs, key hints.
- **No tabs.** Ever. Tab width varies by terminal config; the grid
  stops being a grid.
- **Never set padding 0 against a border.** Content collides with the
  line and reads as a render bug.
- **Gutters between panes.** 1 col is modern minimum. 2 cols feels
  luxurious. 3 cols starts wasting cells.
- **Generous wins at the floor.** At 80×24, dense always loses.

---

## Motion thresholds

- **Spinners after 200ms delay.** Suppress the flash on fast ops.
  Nothing reads cheaper than a spinner that appears for one frame.
- **Progress bars for determinate work.** Spinner only when no total
  is known.
- **After 10s, append "this is taking longer than usual…"** plus a
  cancel hint. Long waits without status read as hangs.
- **Decorative motion is forbidden.** Motion exists to prove
  causality — focus shift, new pane, work completing.
- **Frame rate.** Text frames are 30fps max useful; spinner cadence
  80–120ms; transitions ≤200ms or skip entirely.
- **Toast lifecycle.** 1.5s default, 3s on error. Never blocks input.
  atlas-picker pattern: `Duration::from_millis(1500)` plus async
  dismiss via `smol::Timer`. (`ui.rs:259`.)
- **Respect the user.** A `--no-animation` flag ships. `prefers-
  reduced-motion` analog where the platform offers one.

---

## Typography of the monospace world

The grid is the type. There are no font weights to play with — only
contrast tokens. So the rules are different.

- **Bold** = primary action, current heading, focused text.
- **Dim (faint, SGR 2)** = secondary, metadata, hints.
- **Reverse video** = active selection. Works monochrome — the
  hierarchy survives `NO_COLOR=1`.
- **Underline** = links and focused fields.
- **Italic** = supported but unreliable across terminals; never
  load-bearing. Decorative only.
- **Uppercase** = shouting. Reserve for one label per screen, max
  (e.g. a section header).
- **Truncate with `…`** (U+2026), never `...`.

A monospace UI's "type system" is a list of weights, dim, reverse,
underline, and one uppercase rule. That is the entire palette. It is
enough.
