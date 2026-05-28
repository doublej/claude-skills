# Nerd Fonts: The Complete Guide for TUI Design

Nerd Fonts patches developer fonts with glyphs from Font Awesome, Material Design,
Devicons, Octicons, Powerline, and others. 10,764 glyphs total. Not emoji —
purpose-built for terminal rendering, living in Unicode Private Use Areas.

---

## PUA Range Map

Two PUA ranges. Treat them differently.

```
BMP PUA     U+E000–U+F8FF     3,877 glyphs    1 cell wide (spec)
Sup PUA-A   U+F0001–U+F1AF0   6,880 glyphs    WIDTH UNDEFINED
```

**BMP PUA** (U+E000–U+F8FF) — the safe range. Nerd Fonts spec defines all BMP
PUA glyphs as 1-cell wide. Modern terminals (WezTerm, Ghostty, kitty, iTerm2,
Alacritty) honor this. Older terminals and tmux may misread width — always test.

**Supplementary PUA** (U+F0000+) — where Material Design icons live. Terminals
outside the BMP have no Unicode width spec for these; they may render 0 cells
(invisible), 1 cell, or 2 cells depending on terminal + locale. **Never use
Supplementary PUA in alignment-sensitive contexts** — table columns, status
bars, list prefixes. Decorative use only, with a 1-cell pad after the glyph.

---

## Powerline Glyphs (The Core)

The 6 glyphs every status bar uses. All in BMP PUA.

```
U+E0A0   pl-branch           Git branch symbol
U+E0A1   pl-line_number      Line number (editor mode lines)
U+E0A2   pl-readonly         Readonly / hostname lock
U+E0B0   pl-left_hard_divider   ▶ Solid filled arrow right (segment separator)
U+E0B1   pl-left_soft_divider   ╎ Thin line (same-bg segment separator)
U+E0B2   pl-right_hard_divider  ◀ Solid filled arrow left (right-align segments)
U+E0B3   pl-right_soft_divider  Thin line, right-facing
```

### Powerline Extra (Decorative — use sparingly)

```
U+E0B4   ple-right_half_circle_thick   Right "bubble" cap
U+E0B5   ple-right_half_circle_thin    Right "bubble" cap thin
U+E0B6   ple-left_half_circle_thick    Left "bubble" cap
U+E0B7   ple-left_half_circle_thin     Left "bubble" cap thin
U+E0B8   ple-lower_left_triangle       Diagonal cut
U+E0BA   ple-lower_right_triangle      Diagonal cut
U+E0C0   ple-flame_thick               Decorative
U+E0C4   ple-pixelated_squares_small   Decorative
U+E0C8   ple-ice_waveform              Decorative
U+E0CC   ple-honeycomb                 Decorative
```

Bubble caps (E0B4–E0B7) create pill-shaped segments — readable, restrained.
Flames, pixels, honeycomb: novelty that wears off in three sessions. Avoid.

---

## Curated TUI Vocabulary (~30 glyphs)

These appear in real tools. BMP PUA only.

### Status

| Glyph | Codepoint | Name | Fallback |
|-------|-----------|------|----------|
|  | U+EA87 | cod-error | `✗` |
|  | U+EA6C | cod-warning | `⚠` |
|  | U+EA74 | cod-info | `●` |
|  | U+EAB2 | cod-check | `✓` |
|  | U+EA75 | cod-lock | `#` |
|  | U+EB11 | cod-key | `*` |

### Git / VCS

| Glyph | Codepoint | Name | Fallback |
|-------|-----------|------|----------|
|  | U+E0A0 | pl-branch | `[` |
|  | U+E725 | dev-git_branch | `@` |
|  | U+F126 | fa-code_branch | `\|` |
|  | U+EAFC | cod-git_commit | `○` |
|  | U+EAFE | cod-git_merge | `⑂` |

### File System

| Glyph | Codepoint | Name | Fallback |
|-------|-----------|------|----------|
|  | U+EA83 | cod-folder | `+` |
|  | U+EAF7 | cod-folder_opened | `-` |
|  | U+EA7B | cod-file | `·` |
|  | U+EB06 | cod-home | `~` |
|  | U+E5FB | custom-folder_git_branch | `.git/` |

### Dev / Language icons (for file trees)

Use `dev-*` set — it lives in BMP PUA (U+E700–U+E7FF range).

| Glyph | Codepoint | Name |
|-------|-----------|------|
|  | U+E70E | dev-javascript |
|  | U+E73C | dev-typescript |
|  | U+E73F | dev-python |
|  | U+E7A8 | dev-rust |
|  | U+E724 | dev-go |
|  | U+E73B | dev-html5 |
|  | U+E749 | dev-css3 |

**Do not use `md-*` icons** (U+F0000+) in file trees with alignment — their
width is undefined in the Supplementary PUA.

---

## The Capability Contract

**There is no reliable env var that signals nerd font support.** `TERM`,
`TERM_PROGRAM`, `COLORTERM` report color and protocol — not what glyphs the
user's font renders.

How real tools handle it:

| Tool | Pattern |
|------|---------|
| lazygit | `nerdFontsVersion: ""` — user sets `"2"` or `"3"` in config |
| lf | `set icons true` — user opt-in in lfrc |
| yazi | theme.toml icons section — user configures |
| starship | Assumes NF is installed; breaks on non-NF terminals |

**The correct pattern:**
1. Default to no icons (nerd fonts off)
2. Expose a config key: `icons: "nf3" | "nf2" | "ascii" | "none"`
3. Alternatively, honor `$NERD_FONTS_VERSION` env var (emerging convention)
4. Never auto-detect; always let the user declare

If you must auto-probe: check `$TERM_PROGRAM` for known NF-capable terminals
(WezTerm, Ghostty, Kitty — they set this). But treat the probe as a soft hint,
not a hard requirement. Any positive detection should be overridable.

```
TERM_PROGRAM=WezTerm      → likely NF capable (but not guaranteed)
TERM_PROGRAM=Apple_Terminal → not NF capable
TERM_PROGRAM=iTerm.app    → NF capable if user installed a NF font
COLORTERM=truecolor       → tells you about color, not fonts
NO_COLOR=1                → icons should also be suppressed
```

---

## NF v2 vs NF v3: The Version Contract

Nerd Fonts v3 (released 2023) remapped hundreds of glyphs to new codepoints.
The git branch symbol moved; the dev icon set reorganized. Apps that hardcode
NF v2 addresses break on NF v3 fonts and vice versa.

**Always declare a version requirement** — and expose a config toggle. Lazygit's
`nerdFontsVersion` is the pattern. Your app should do the same.

If you build a glyph constants module:

```rust
// glyph_constants.rs
pub struct Glyphs {
    pub branch: &'static str,
    pub folder: &'static str,
    pub file: &'static str,
    pub check: &'static str,
    pub error: &'static str,
}

pub const NF3: Glyphs = Glyphs {
    branch: "\u{E0A0}",
    folder: "\u{EA83}",
    file: "\u{EA7B}",
    check: "\u{EAB2}",
    error: "\u{EA87}",
};

pub const ASCII: Glyphs = Glyphs {
    branch: "[",
    folder: "+",
    file: "·",
    check: "✓",
    error: "✗",
};
```

One constants module. Two sets. The rest of the app names glyphs, not codepoints.

---

## Width-Safe Rendering

BMP PUA glyphs are spec'd as 1-cell wide by nerd fonts. In practice:

1. **Always pad with a space after an icon when followed by text.**
   `" main"` not `"main"`. Many terminals don't advance the cursor correctly
   after a PUA glyph unless a space follows.

2. **Never trust `wcswidth()` / `unicode_width` crates for PUA ranges.**
   They return 1 for most BMP PUA — correct by nerd fonts spec, but a few
   terminals render 2. Test on the terminal matrix below.

3. **Supplementary PUA glyphs: +1 explicit pad cell always.**
   If you must use a MD icon (U+F0000+), render it as if it's 2 cells wide.
   Some terminals will eat the extra space; none will break.

4. **In aligned tables: stick to BMP PUA or geometric glyphs only.**
   Column alignment is a promise. Don't make that promise with a glyph whose
   width the terminal didn't read from the font.

### Terminal matrix (test on all of these)

| Terminal | NF support | BMP PUA width | Sup PUA width |
|----------|------------|---------------|---------------|
| WezTerm | Excellent | 1 cell | 2 cells |
| Ghostty | Excellent | 1 cell | 2 cells |
| kitty | Excellent | 1 cell | 2 cells |
| iTerm2 | Good (with NF font) | 1 cell | varies |
| Alacritty | Good | 1 cell | varies |
| tmux (passthrough) | Wraps host | wraps host | wraps host |
| Apple Terminal | None | box char | box char |
| xterm | None | 1 cell (box) | 0 or 1 |
| SSH + PuTTY | None | varies | varies |

Your app must not crash on Apple Terminal or xterm rows. It must degrade.

---

## Powerline Status Bar Patterns

### Basic segmented bar

```
  main  src/components   ✓   
```

Composition:
```
[accent-bg] [U+E0A0] [branch] [space] [U+E0B0] [surface-bg fg-accent] [path] [U+E0B0]
```
The hard divider (U+E0B0) uses the foreground color of the *source* segment
and the background color of the *target* segment. Alignment is pixel-perfect
because it's a full-cell filled triangle.

### Soft divider for same-color segments

```
  12:34  Mon 26 Apr  
```
Segments with the same background use the soft divider (U+E0B1) — a thin
vertical line in a mid-tone between the bg and fg.

### Pill / bubble segments (restraint required)

```
 ◖ main ◗   ◖ ✓ ◗
```
Left cap U+E0B6, right cap U+E0B4, inner content, full accent background.
Reads as "elevated" — use for the single most important status item, not
for every segment. More than two pill segments on one bar = decoration, not design.

### Right-aligned segments

Flip to U+E0B2 (right hard divider) and U+E0B3 (right soft divider).
The right side of a status bar reads right-to-left; segment order inverts.

---

## Icon Set Selection Guide

When you need an icon, pick the set in this order:

1. **Geometric Unicode** (U+2500–U+25FF) — always safe, no nerd font needed
2. **Codicons** (`cod-`, U+EA60–U+EBEB) — VS Code icon set, clean, minimal, BMP PUA
3. **Octicons** (`oct-`, U+F400–U+F533) — GitHub icons, BMP PUA, developer-familiar
4. **dev-icons** (`dev-`, U+E700–U+E7FF) — language/tool logos, BMP PUA
5. **Font Awesome** (`fa-`, U+E000–U+E0FF, U+F000–U+F3FF) — large set, BMP PUA
6. **Material Design** (`md-`, U+F0001+) — only for decorative, non-aligned use

Never reach for MD first. It's the largest set (6,880 icons) and the most
dangerous for alignment. Codicons and Octicons cover 95% of TUI needs.

---

## Anti-Patterns (Nerd Font Edition)

### 1. Assuming nerd font support
No env var reliably signals it. Default off. User declares.

### 2. Using Supplementary PUA in aligned columns
Material Design icons (U+F0000+) have undefined terminal width. Use in prose
or single-item decorative contexts only — never in table columns or list prefixes.

### 3. Hardcoding NF v2 addresses
Glyphs moved in v3. Your app will show boxes on v3 fonts. Declare version; use a
constants module for both; let users configure which.

### 4. No ASCII fallback per icon
Every nerd font glyph needs a plain-text fallback. The user on Apple Terminal is
real. The CI runner with `TERM=dumb` is real. The glyphs constants module (above)
enforces this — if a fallback key is missing at compile time, it didn't exist.

### 5. Mixing icon sets for the same concept
One file-type icon set. One status icon set. One VCS icon set. Mixing `cod-`
folders with `fa-` files reads as inconsistency — same as mixing border weights.

### 6. Forgetting the space after the icon
`"\u{E0A0}branch"` breaks on most terminals. `"\u{E0A0} branch"` works. The
space is part of the glyph's logical cell.

### 7. Using powerline decorative separators (flames, pixels, waveforms)
Novelty. They announce "I used a powerline tutorial from 2019" not "I designed
this." Hard dividers only. Bubble caps if you have taste and restraint.

### 8. Icons as the only distinction between states
NF icons are enhancement. The state must be legible from the ASCII fallback first.
Don't use  vs  as the only difference between success and failure — pair with
color and with a text label.

---

## The Fallback Chain

```
Nerd Font enabled (NF3) → use BMP PUA glyph
Nerd Font enabled (NF2) → use NF2 BMP PUA glyph (different address)
NF disabled, Unicode available → use geometric glyph (✓ ✗ ⚠ ● ◆)
ASCII mode / LANG=C → use ASCII punctuation (+ - * # ~)
NO_COLOR=1 → suppress icons (or use ASCII), strip colors
```

The geometric glyph layer (the existing visual vocabulary) is the natural
NF-disabled tier. You don't need a dedicated "icon off" mode — you need the
vocabulary fallback chart from `visual-vocabulary.md` populated before any
nerd font glyph is chosen.

---

## Diagnostic

```bash
# Does your icon set expose all fallbacks?
grep -r 'U+[EF][0-9A-F]' src/ | grep -v fallback   # PUA without fallback annotation

# Are you using Supplementary PUA in aligned output?
grep -rP '[\x{F0000}-\x{10FFFF}]' src/              # any sup PUA chars

# Version declared?
grep -i 'nerd_fonts_version\|NERD_FONTS\|icons_version' .env config.*

# Space after icon?  icon + text with no space is the bug
grep -rP '\\u[Ee][0-9A-Fa-f]{3}[^\s"'"'"'\\]' src/ # PUA glyph immediately followed by non-space
```
