---
name: tui-monospace
description: >
  Ship terminal interfaces that earn the medium — cross-library TUI design
  taste: layout, theming, keybinds, focus, capability detection for ratatui,
  Textual, Ink, Bubble Tea, iocraft, OpenTUI, vaxis. Nerd font icons,
  powerline glyphs, PUA range safety, NF v2/v3 version contracts. For the
  Node.js terminal-kit library API reference use tui-kit. Triggers on "TUI",
  "terminal app", "interactive CLI", "fzf-style", "lazygit-style", "make
  this terminal app feel good", "nerd font", "powerline", "status bar",
  "file tree icons".
---

# Monospace Conviction

<intro>
The terminal isn't a fallback. It's the constraint that makes the
conviction visible. A grid of cells, a keyboard, a few hundred glyphs,
maybe color. Everything that ships here ships because it earned the cell.
</intro>

<manifesto>

## The Manifesto

I do not "wrap a CLI in a TUI." I do not add a frame because the output
felt naked. I do not reach for a spinner because waiting felt awkward.
Every cell is a decision. Every keystroke is a contract.

The monospace grid is the most honest medium in software. There is no
Photoshop here. No `box-shadow: 0 1px 2px rgba(0,0,0,.04)` to soften a
weak edit. The line is on or it is off. The character renders or it
doesn't. The keystroke advances the task or it wastes it.

Eighty by twenty-four is not a limit. It is a proposal. A floor written
into VT100 in 1978 and respected by every SSH session, every CI runner,
every laptop docked sideways. Design for it first. The luxury of a
3440-wide terminal is enhancement, never assumption.

Color is opt-in. The black-and-white version must already work. The user
running with `NO_COLOR=1` is not a failure case. They are the test.

The terminal is fast. Your TUI must not be the slow part.

One thesis. One verb. One focus. The rest obeys or dies.

</manifesto>

<enemies>

## The Enemies

Ten patterns that mark a TUI as cheap. Long versions in
`references/anti-patterns.md`.

1. **Emoji confetti** — codepoints in U+1F300–U+1FAFF render at random
   widths on stranger machines. Alignment dies.
2. **The figlet ritual** — ASCII banners on every launch. Slow startup,
   novelty wears off in two runs, announces nothing.
3. **Mouse-only handoffs** — the click target with no key. SSH, screen
   readers, and muscle memory all locked out at once.
4. **Lying spinners** — a braille spin on a job that knows its progress.
   A confession of laziness rendered as motion.
5. **Mixed border weights** — heavy beside light beside rounded reads
   as render confusion, not affordance.
6. **Hidden keybinds** — the footer is empty, the help screen is buried.
   Discovery is your job, not the user's.
7. **Truecolor required** — the 24-bit palette that dies in tmux-256,
   in CI logs, in any terminal that lies about its capabilities.
8. **Twitch motion** — decorative animation that loops while the user
   isn't doing anything. Noise without a verb.
9. **Double-painted edges** — adjacent panels both drawing the shared
   line. Reads as a render bug even when intentional.
10. **The TUI-shaped flag-CLI** — a frame around output that `cmd | jq`
    would have done better. The frame was the point. There was no point.

---

## The Paradoxes

Held without resolving.

**Constraint is the brief.** Eighty by twenty-four isn't where the design
gets cramped. It's where the design has to be true. Below the floor,
redirect — don't render.

**Color is opt-in.** The monochrome version must already carry hierarchy.
If `NO_COLOR=1` collapses the screen, the screen never had hierarchy —
it had a paint job.

**Keyboard discoverable, mouse forgivable.** Every action keyed. Mouse
support is enhancement on top, never the only path in.

**The terminal is fast. Your TUI must not be the slow part.** Every
decision the user makes faster than your render is friction your taste
imported.

</paradoxes>

<cell_brief>

## Pre-flight: The Cell Brief

Six commitments before any code. No "TBD." No "we'll see at runtime."

1. **Cell floor.** Specific cols × rows you commit to (e.g. 80×24).
   Below the floor, the program redirects to plain output.
2. **Capability floor.** 256 or truecolor? Unicode level? Mouse?
   Bracketed paste? Pick a floor. State the enhancement path.
3. **Single dominant focus.** One panel reads as primary. One cursor.
   One verb (browse, edit, monitor, run, search — pick one).
4. **Keybind contract.** Write the footer text *before* the layout.
   The footer is the navigation spec. If a key isn't on it, it doesn't
   exist.
5. **Motion budget.** None / one beat / continuous. Pick one. Spinners
   only after a 200ms delay. Decorative loops are forbidden.
6. **NO_COLOR fallback.** What does the screen look like with color
   stripped? Describe it before color tokens are picked.

</cell_brief>

<vocabulary>

## Visual Vocabulary

Condensed. Full charts in `references/visual-vocabulary.md`.

### Box weight discipline

- **Light** (`─ │ ┌ ┐ └ ┘`) is the default. Almost everything.
- **Heavy** (`━ ┃ ┏ ┓ ┗ ┛`) for *one* focused panel. Affordance, not
  decoration.
- **Rounded** (`╭ ╮ ╰ ╯`) only for ephemeral surfaces — toasts, modals,
  hover hints.
- **Double** (`═ ║ ╔ ╗`) banned for body. Acceptable as one accent line,
  once per screen, max.
- Never mix weights inside one box.
- **The atlas-picker maneuver:** when two panels stack, only one draws
  the shared edge. iocraft `Edges::Bottom` on the upper panel, no top
  edge on the lower. Same line, painted once. (atlas-picker `ui.rs:781`,
  `ui.rs:954`.)

### Block elements for density

- Horizontal bars: `▏▎▍▌▋▊▉█` — eighths, sub-cell resolution. Meters,
  sparklines, progress with precision.
- Shading: `░ ▒ ▓ █` — pick one intensity per surface. Mixing
  intensities reads as glitch.
- Half-blocks: `▀ ▄` — double the vertical resolution in graphs.

### Glyph palette

- **Status**: `● ○ ◐ ✓ ✗ ⚠`
- **Direction**: `▲ ▼ ◀ ▶`
- **Selection**: `▌` (bar) or `▶` (caret) — pick one across the app.
- **Scroll**: `▲ ▼` shown only when overflow is possible. Do not draw
  scroll indicators that lie. (atlas-picker scroll-keep rule.)
- **Wait**: `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏` braille spinner.
- **Truncation**: `…` (single codepoint U+2026), never `...`.
- **Banned**: emoji 🚀 ✨ 🔥 ✅ ❌. Render varies. Treat as broken.

### Color tokens (eleven names, every theme defines all eleven)

`bg`, `surface`, `panel`, `fg`, `fg-muted`, `fg-subtle`, `accent`,
`accent-muted`, `success`, `warning`, `error`. Optionally `focus` if it
diverges from `accent`.

Default themes: Catppuccin Mocha (dark) + Latte (light). Both ship.
Honor `COLORFGBG` for auto-detection — the atlas-picker pattern parses
the trailing field of `fg;bg`, treats `>= 7` as light, falls back to
dark on missing. (atlas-picker `theme.rs:129`.) Live theme cycle on
`Ctrl+T` is one of the cheapest delights you can ship.
(atlas-picker `ui.rs:371`.)

`NO_COLOR=1` is a hard off-switch. Never optional.

### Spacing rules

- 2 cols horizontal padding inside panels.
- **The atlas-picker maneuver, again:** the selected row gets one empty
  row above and one below it, in the same background as the row itself.
  Focus indicated by *space*, not just color. (atlas-picker `ui.rs:994`,
  rendered as a 3-row block.)
- 1 cell between inline items.
- Never set padding 0 against a border — content collides with the line.
- Gutters between panes: 1 col modern minimum, 2 cols luxurious.

Full RGB tables, ANSI fallbacks, and the COLORFGBG algorithm are in
`references/visual-vocabulary.md`.

</vocabulary>

<workflow>

1. **Probe capabilities.** Read `TERM`, `COLORTERM`, `NO_COLOR`,
   `FORCE_COLOR`, `COLUMNS`, `LINES`. Or commit to a floor in the brief
   and refuse below it.
2. **Choose the library.** See `references/library-decision.md` —
   ratatui, iocraft, Bubble Tea, Textual, Ink, OpenTUI, vaxis.
3. **Write the tokens file before any layout.** Eleven color tokens, a
   spacing scale, a glyph constants module. The screen is rendered
   *through* the tokens.
4. **Draft the keybind footer text.** This is the navigation spec.
   It exists before the panels do.
5. **Sketch the layout in ASCII at the floor cell size.** 80×24.
   Boxes drawn with `─│┌┐`. If it doesn't fit at the floor, the floor
   is wrong or the screen is.
6. **Implement the primary screen at the floor.** Make it work at
   80×24 first. Resize handling comes after.
7. **Add focus state.** The breathing-room move: extra row above and
   below the selected item, same surface color, before any text-color
   change. Color is the second carrier.
8. **Add scroll/overflow handling — only when content overflows.**
   Empty scroll indicators are lies. (atlas-picker scroll-keep rule:
   keep selection in view across resizes.)
9. **Add async state.** Idle / loading / success / error rendered as
   colored status text in a single status slot, not modal overlays.
10. **Add the toast/feedback layer.** 1.5s ephemeral, non-modal,
    non-blocking. Theme change confirms in one. Clipboard copy confirms
    in one. (atlas-picker pattern: `Duration::from_millis(1500)`,
    async dismiss via timer, never blocks input. `ui.rs:259`.)
11. **Wire hierarchical Esc.** Closes help → closes submenu → closes
    root menu → quits. Not "always quits." (atlas-picker `ui.rs:379`.)
12. **Verify.** Run the Taste Rubric below.

---

## Output Discipline

Four artifacts, in order, no exceptions.

1. **The Cell Brief.** Six commitments above, written out as prose.
   ≤150 words. No options. No "we could."
2. **The tokens file.** One source file naming the eleven color
   tokens, the spacing scale, the glyph constants. Theme switching
   reads from here.
3. **Working code at the floor cell size.** Demonstrates the brief.
   Renders at 80×24. NO_COLOR clean.
4. **The keybind footer text.** Matches the contract from the brief.
   Every advertised key is bound.

No "let me know if you'd like X." No three options. Ship the four.
Stop.

</output_discipline>

<taste_rubric>

## The Taste Rubric

Run before declaring done. Any failure means not done.

1. **The 80×24 read.** Readable at the floor cell size without scroll
   on the primary screen.
2. **The footer test.** Every advertised key is bound. Every bound
   key the user needs is advertised.
3. **The NO_COLOR pass.** `NO_COLOR=1` preserves the hierarchy. State
   is still legible.
4. **The single-focus check.** Exactly one panel reads as primary. If
   two compete, you don't have a design — you have a layout.
5. **The breathing-room move.** Focus is indicated by *space* before
   color. (atlas-picker maneuver.)
6. **The border audit.** ≤2 distinct border styles on the primary
   screen. Mixing weights is affordance only — focused vs. unfocused.
7. **The emoji grep.** Zero codepoints in U+1F300–U+1FAFF. Geometric
   glyphs only.
8. **The keystroke count.** Primary task ≤5 keystrokes from launch.
9. **The Esc-reverses test.** Esc moves up the navigation hierarchy
   before it quits. (atlas-picker pattern.)
10. **The async honesty.** Non-instant work shows
    idle/loading/success/error in a colored status slot. Not a modal.
11. **The 16-color fallback.** Design degrades, doesn't collapse, on
    a 16-color terminal.
12. **The resize test.** Layout reflows. Selection stays in view.
    (atlas-picker scroll-keep rule.)
13. **The toast budget.** Feedback is ephemeral (≤2s) and never
    blocks input.
14. **The "could this be JSON" check.** If `cmd | jq` plus a `--watch`
    flag would do the job, ship the pipe instead. The TUI must justify
    the frame.
15. **The nerd font fallback check.** Every BMP PUA glyph has an ASCII
    fallback defined. No Supplementary PUA (U+F0000+) in aligned
    contexts. A space follows every icon glyph. NF version declared in
    config.
16. **The capability-off test.** Run with icons disabled or on Apple
    Terminal. Hierarchy survives — no boxes, no alignment breaks, no
    missing state.

---

## The Interrogation

### What Does It Refuse?

1. What capability did you assume that you should detect?
2. What did you draw that the keyboard can't reach?
3. Which symbol will be broken on a stranger's machine?
4. What animation runs when the user isn't looking?
5. Which border will collide with the panel next to it?

### What Does It Believe?

6. What does the user feel in the first frame? In the first keystroke?
7. What is this app's verb? Browse, edit, monitor, run, search — pick
   one and bleed for it.
8. What's the keystroke count for the primary task?
9. If `COLORFGBG` is empty, what does this look like?
10. What is the one thing this TUI does that no flag-based CLI could?

### What Will It Ship?

11. What's the cell-floor? Below it, redirect — don't render.
12. Which capability is required, which is enhancement?
13. What latency makes a keystroke feel broken?
14. What happens on resize during async work?
15. What's the smallest demo that proves the thesis?

</interrogation>

<nerd_fonts>

## Nerd Fonts

Full detail in `references/nerd-fonts.md`. Summary rules:

### The PUA contract

Two ranges. Different rules.

- **BMP PUA** (U+E000–U+F8FF) — 3,877 glyphs. Spec'd as 1-cell wide.
  The safe range for all aligned contexts. Powerline, Codicons, Octicons,
  dev-icons all live here.
- **Supplementary PUA** (U+F0000+) — 6,880 glyphs. Material Design icons.
  **Width undefined by Unicode.** Terminals render these as 0, 1, or 2 cells.
  Never in aligned columns, tables, or list prefixes. Decorative use only,
  +1 explicit pad cell.

### The capability contract

No env var reliably signals nerd font support. **Default off. User declares.**

```
Pattern: expose a config key   icons: "nf3" | "nf2" | "ascii" | "none"
         or honor              $NERD_FONTS_VERSION env var
Never:   assume support based on TERM, COLORTERM, or TERM_PROGRAM alone
```

### The version contract

NF v3 (2023) remapped hundreds of glyphs. Declare version. Expose config.
Build a glyph constants module with both NF3 and ASCII sets — every icon
has a fallback at compile time. See `references/nerd-fonts.md` for the module
pattern.

### Powerline core (6 glyphs — all you need)

```
U+E0A0  pl-branch              git branch ()
U+E0A1  pl-line_number         line number
U+E0A2  pl-readonly            readonly / lock
U+E0B0  pl-left_hard_divider   solid arrow → (segment separator)
U+E0B1  pl-left_soft_divider   thin line (same-bg separator)
U+E0B2  pl-right_hard_divider  solid arrow ← (right-align segments)
```

Hard dividers: fg = source segment color, bg = target segment color.
Soft dividers: between segments sharing the same background.

### Icon set priority

1. Geometric Unicode (`▲ ● ◆ ✓ ✗ ⚠`) — no nerd font needed
2. Codicons (`cod-`, U+EA60–EBEB) — clean, minimal, BMP PUA
3. Octicons (`oct-`, U+F400–F533) — GitHub icons, BMP PUA
4. dev-icons (`dev-`, U+E700–E7FF) — language logos, BMP PUA
5. Font Awesome (`fa-`) — BMP PUA, larger set
6. Material Design (`md-`, U+F0000+) — decorative only, never aligned

Never reach for MD first. 95% of TUI needs are covered by Codicons + Octicons.

### Fallback chain

```
NF3 enabled  → BMP PUA glyph (version-declared constants)
NF2 enabled  → NF2 BMP PUA glyph (different address)
NF off       → geometric glyph from visual-vocabulary.md
ASCII mode   → ASCII punctuation (+ - * # ~)
NO_COLOR=1   → suppress icons or use ASCII, strip colors
```

### Width rule

Always pad with a space after an icon when followed by text.
`"\u{E0A0} branch"` not `"\u{E0A0}branch"` — cursor advancement breaks
without the space on many terminals.

### The 3 nerd font anti-patterns to avoid

1. **Supplementary PUA in aligned contexts** — undefined width kills columns
2. **No ASCII fallback per icon** — CI runners and Apple Terminal users are real
3. **Skipping the space after the glyph** — misalignment on most terminals

See `references/nerd-fonts.md` for the full 8-pattern list, the glyph
vocabulary table, powerline composition patterns, and the terminal test matrix.

</nerd_fonts>

<references>

- `references/library-decision.md` — pick the right toolkit, when not
  to ship a TUI at all.
- `references/visual-vocabulary.md` — full Unicode charts, RGB tables,
  COLORFGBG algorithm.
- `references/anti-patterns.md` — fourteen traps with fixes and
  diagnostics.
- `references/nerd-fonts.md` — PUA ranges, powerline glyphs, icon sets,
  capability detection, NF v2/v3 version contract, width-safe rendering,
  terminal matrix, fallback chain, powerline composition patterns.

Inline reference (no separate file): atlas-picker
(`multi-stack/project-atlas/atlas-picker/`) is cited throughout as the
canonical pattern source — breathing-room focus, `Edges::Bottom`-only
shared edges, hierarchical Esc, `COLORFGBG` auto-detect, `Ctrl+T` live
theme cycle, 1.5s non-modal toasts, scroll-keep on resize.

</references>

<closing>
The terminal is honest. Render less. Mean more.
</closing>
