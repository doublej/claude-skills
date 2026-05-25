# Tooling Design System

A data-dense neutral design system in the Linear / Vercel / Stripe lane. Built for dashboard SPAs where **the data is the design** — chrome stays out of the way, borders do the work of shadows, and numerals march down the page in tabular columns.

---

## 1 · Context

**Stack the system was extracted from**

- SvelteKit 2 + Svelte 5 (runes) + TypeScript, Vite, Bun
- Tailwind v4 with the `@theme` directive (no `tailwind.config.js`)
- `bits-ui` headless primitives, `mode-watcher` for light/dark/system
- `@lucide/svelte` icons, `svelte-sonner` toasts, `vaul-svelte` drawer
- `@tanstack/svelte-table` for tables, `lightweight-charts` for finance charts
- `@fontsource-variable/geist` + `geist-mono`
- `adapter-static` (SPA), served by Caddy

**Sources provided to build this system**

- Stack + visual-DNA brief (pasted in chat). No live codebase or Figma file was attached — the system below was derived from the brief and the conventions of the named libraries. Re-attach a codebase or Figma file via the Import menu to tighten the recreation.

**Implied product surface**

The brief calls out `Money`, `Stat`, `PageHeader`, `EmptyState`, `DataTable` with `mobileCard` snippets, Cmd-K palette, Cmd+Shift+P privacy blur, and `lightweight-charts` — i.e. a **finance / portfolio dashboard SPA**. The UI kit recreates that.

---

## 2 · Index

```
.
├── README.md                  — this file
├── SKILL.md                   — Agent Skill manifest (Claude Code compatible)
├── colors_and_type.css        — semantic CSS vars, type scale, reset
├── assets/
│   ├── logo.svg               — brand mark
│   ├── logo-wordmark.svg      — wordmark
│   └── icons/                 — Lucide subset used in UI kit
├── fonts/
│   └── README.md              — Geist Variable + Geist Mono sourcing
├── preview/                   — Design System tab cards (registered)
│   ├── type-*.html
│   ├── colors-*.html
│   ├── spacing-*.html
│   └── component-*.html
└── ui_kits/
    └── finance_dashboard/
        ├── README.md
        ├── index.html         — interactive click-thru
        ├── tokens.css         — kit-scoped theme (extends colors_and_type.css)
        ├── App.jsx            — router + state
        ├── TopNav.jsx
        ├── BottomNav.jsx
        ├── CommandPalette.jsx
        ├── PageHeader.jsx
        ├── Card.jsx
        ├── Stat.jsx
        ├── Money.jsx
        ├── Badge.jsx
        ├── Button.jsx
        ├── DataTable.jsx
        ├── Sparkline.jsx
        ├── PriceChart.jsx
        ├── EmptyState.jsx
        └── screens/
            ├── Overview.jsx
            ├── Accounts.jsx
            ├── Transactions.jsx
            └── Holdings.jsx
```

---

## 3 · Content fundamentals

The voice is **terse, precise, and operational** — closer to a Bloomberg terminal label than a marketing site.

- **Pronouns**: avoid them. Headlines and labels are usually nouns or noun phrases, not sentences. ("Total assets", not "Your total assets". "Add account", not "Click here to add an account".)
- **Casing**: **Sentence case everywhere.** Titles, buttons, menu items, table headers. Not Title Case, not ALL CAPS. The only uppercase is `.t-eyebrow` micro-labels (tracking-wider, 11px).
- **Punctuation**: no trailing periods in labels, buttons, list items, table cells. Periods belong in body prose and toasts.
- **Numbers**: always tabular, always right-aligned in tables. Currency uses the symbol prefix (`$1,240.55`). Percentages use one decimal (`+2.4%`). Deltas always carry their sign (`+`, `−`, not `-`).
- **Time**: relative for recent events ("2m ago", "yesterday"), absolute ISO-ish for older ("Apr 12, 2026"). Never "01/04/26" — ambiguous.
- **Empty states**: a noun, one short sentence of context, a single primary action. No mascots, no apologies. E.g. *No transactions / Connect an account to see activity here. / **+ Connect account***
- **Toasts**: one line, past tense for confirmations ("Account connected"), imperative for errors ("Check your connection and retry").
- **Emoji**: **not used** in product UI. Reserved for user-generated content only.
- **Vibe**: the aesthetic of a power tool. The user is competent. Don't explain what a chart is; label its axes correctly and get out of the way.

**Examples**

> Net worth  
> $128,402.10 · +1.2% today

> Holdings  
> 14 positions across 3 accounts

> No alerts / You're all caught up. / **Configure alerts →**

---

## 4 · Visual foundations

### Color

Two themes, one source of truth: semantic CSS vars defined in `colors_and_type.css`, flipped by toggling `.dark` on `<html>`. **Never** use Tailwind's `dark:` utilities — read from `var(--color-*)`.

- **Surfaces** — `--color-bg` (page), `--color-card` (sections), `--color-bg-elev` (popovers). The page is *near*-white (`#fafafa`) or *near*-black (`#0a0a0a`); pure white/black is reserved for cards-on-bg contrast.
- **Text** — `--color-fg`, `--color-fg-2`, `--color-muted`. Three steps, no more.
- **Lines** — `--color-border` is `rgba(0,0,0,0.08)` light / `rgba(255,255,255,0.08)` dark. Thin (1px). Borders are the primary visual divider; shadows are an accent.
- **Accent** — `--color-accent` is a Linear-leaning indigo (`#5e6ad2`). Used for primary buttons, active nav, focus ring, links. Used **sparingly**.
- **Semantic** — `--color-pos` (green-600), `--color-neg` (red-600), `--color-warn`, `--color-info`. Each has a paired `-soft` background for badges/chips.
- **Chart** — categorical palette `--chart-1..8` that holds up in both themes.

### Type

- **Geist Variable** for all chrome text. Geist's geometry reads cleanly at 13–14px — most of the UI lives in that range.
- **Geist Mono** for all *tabular* numerals (table cells, inline figures, captions, deltas). Even when a number sits in body text, wrap it in `.num` for column-correct alignment.
- **Instrument Serif** for **hero / display numerals only** — the big net-worth figure, Stat card values, the donut's center total. Anywhere a single number is the visual anchor of its section. The currency symbol drops to ~70% size and rises ~0.18em above the baseline (`.stat-value .sym`).
- Scale (px): 11 (eyebrow) · 12 (caption) · 13 (small) · 14 (body) · 16 (h3 / lead) · 20 (h2) · 28 (h1) · 36–64 (hero numerals, serif).
- Weights used: 400 (body, serif numerals), 500 (labels, eyebrow), 600 (headings, buttons). 700+ rarely.
- Letter-spacing tightens negatively as size grows (`-0.01em` → `-0.02em`).

**The numeral rule, plainly:** *Hero number? Instrument Serif. Anywhere else? Geist Mono.* If a number is meant to be scanned alongside others in a column, it's mono. If it's the one big number the page is selling, it's serif.

### Spacing

4px base grid. Tokens `--space-1..16`. Cards have 16–24px internal padding. Section gaps are 24–32px. Compact density tables drop to 8px row padding.

### Backgrounds

- Solid. **No gradients on surfaces.** No imagery, no textures, no patterns. The page is one tone; cards are one tone lighter (light theme: card brighter than bg) or darker (dark theme: card darker than `#0a0a0a` is impossible, so card is `#111`).
- The only acceptable gradient is inside a chart fill (line-to-transparent area fill, 0.08 alpha).

### Borders & cards — the hairline system

Every border in the system is **0.5px** (`var(--hairline)`) — and most are stylized rather than flat. This is what gives the UI a recognizable signature.

**The canonical card** carries three layers (codename **C₂ · Diagonal**):

1. **Outer neutral hairline** — `0.5px solid var(--color-border)`, full perimeter.
2. **Inner indigo gradient** — a second 0.5px stroke 4px inside the outer, drawn via `padding + mask-composite: exclude` so the rounded corners stay clean. The gradient is **135°**: full-strength accent at the top-left, dissolving to transparent at the bottom-right.
3. **Directional halo** — two stacked box-shadows offset **up-and-left** in the accent color (`-2px -2px 6px` and `-6px -6px 18px`), with the inner top-edge highlight (`inset 0 0.5px 0 rgba(255,255,255,0.7)`) catching the rim.

Together they read as a single thing: *"this card is lit from the upper-left."* The light source is consistent across every card on every page, which is what turns it into a brand signature instead of a decoration.

**Other recurring 0.5px effects across the system:**

- **Fade-out dividers** — every horizontal divider (table rows, card-head bottoms, page-header rule, popover separators, top/bottom nav lines) is a `linear-gradient(90deg, transparent 0%, border 8%, border 92%, transparent)` painted as a 0.5px background. Lines never quite touch surface edges.
- **Catch-light buttons** — primary + destructive buttons carry a 4-stop gradient border (white-tinted top, black-tinted bottom).
- **Directional focus halo** — focused inputs get the soft accent ring **plus** a 1px brighter accent line on the top edge. Focus arrives from above.
- **Popovers / command palette / toasts** keep the simpler **Aurora** (vertical gradient) border — floating elements are deliberately distinct from embedded cards.

**Hover** still uses background-color shift (`--color-card-2`) — no shadow lift, no border weight change. The hairline system is meant to be quiet.

### Radii

`4 / 6 / 8 / 12 / 16 / 9999`. Inputs and small buttons → 6. Cards and large buttons → 8–12. Pills/avatars → full.

### Shadows

Reserved for **floating** elements — popovers, dropdowns, command palette, toasts. Body chrome uses borders, not shadows. `--shadow-sm` for popovers, `--shadow-lg` for the command palette.

### Hover / press states

- **Hover** — surfaces: `--color-card-2` background. Buttons: 6% darker via `filter: brightness(0.96)` (light) / `brightness(1.08)` (dark). Links: underline appears.
- **Press** — `transform: translateY(0.5px)` and 4% darker. Never a scale-shrink.
- **Active nav** — `aria-current="page"` triggers `color: var(--color-fg)` + `background: var(--color-card-2)`. No underline.
- **Disabled** — `color: var(--color-disabled)`, no background change, `cursor: not-allowed`, no hover response.

### Focus

Always-visible `:focus-visible` ring: `2px solid var(--color-ring)`, `outline-offset: 2px`. Never removed.

### Motion

- Durations: 120ms (micro), 180ms (default), 240ms (overlays).
- Easing: `cubic-bezier(0.16, 1, 0.3, 1)` for entrances (a snappy ease-out).
- No bounces, no springs, no parallax. Fades and short translates only.
- `prefers-reduced-motion` collapses all durations to 1ms.

### Transparency & blur

- Popover/dropdown backgrounds are **solid** `--color-bg-elev`. No `backdrop-filter` on chrome.
- The **only** blur in the system is `Cmd+Shift+P` privacy mode — applies `filter: blur(8px)` to `.privacy` elements (the `Money` component opts in automatically).
- Modal overlay uses `--color-overlay` (40% black) — opaque, no blur.

### Layout

- Centered single column, `max-width: 1100px`, horizontal padding `24px` desktop / `16px` mobile.
- **Sticky TopNav** at 56px height, full-bleed with a 1px bottom border. Grouped dropdowns via `bits-ui`.
- **Mobile BottomNav** at 64px height, full-bleed top border, 4–5 items. Hit targets ≥ 44px.
- Page body grid: 12-col on desktop (24px gutter), 4-col on mobile (16px gutter). Most pages use a single column of cards.

### A11y baked in

- `SkipLink` first focusable.
- `aria-current="page"` on the active nav item — drives active styling.
- All interactive elements have ≥ 44px touch targets on `(max-width: 768px)`.
- `prefers-reduced-motion` honored globally.
- Color contrast ≥ 4.5:1 for text in both themes.

---

## 5 · Iconography

- **Library** — [Lucide](https://lucide.dev/) (`@lucide/svelte` in the source stack). 1.5px stroke, 24px nominal, currentColor.
- **Rendering** — icons inherit `color` from their parent (use `--color-fg`, `--color-muted`, etc). Never recolor a Lucide icon with a hex value.
- **Size** — 14px inline with body text, 16px in buttons and nav, 20px for empty-state visuals. Never larger than 24px in chrome.
- **Stroke** — keep Lucide's default 1.5px. Don't fill, don't add backgrounds.
- **Substitutes** — if a needed icon isn't in Lucide, **flag it and ask** rather than reaching for another library. Mixing icon families is forbidden.
- **Emoji** — not used in chrome. Allowed only in user-generated content (e.g. an account nickname).
- **Unicode glyphs** — `↑`, `↓`, `→`, `·`, `−`, `…` are fine inline. Math minus (`−` U+2212), not hyphen, for negative numbers.
- **Logos / brand marks** — `assets/logo.svg` (mark only) and `assets/logo-wordmark.svg` (mark + wordmark). Monochrome, drawn in currentColor.

A small Lucide subset used by the UI kit is mirrored in `assets/icons/` for offline use; production code should keep importing from the package.

---

## 6 · Caveats

- **No codebase or Figma was attached.** The system is derived from the stack/DNA brief and the conventions of Linear, Vercel, Stripe, and the named libraries. If you have an actual repo or Figma file, re-attach via Import and the kit will be tightened to match.
- **Geist fonts** are loaded via Google Fonts CDN. If you need self-hosted variable WOFF2 files, drop them into `fonts/` and the `@font-face` rule will pick them up first.
- **Brand mark** is a placeholder — a square monogram. Replace `assets/logo.svg` with the real asset.
- **Iconography** uses Lucide via CDN. If your product ships a different set, point me at it.

---

## 7 · Where to go next

- Open the **Design System tab** for the visual reference cards.
- Open `ui_kits/finance_dashboard/index.html` for the interactive product mockup.
- Drop new fonts into `fonts/` and new icons into `assets/icons/` as you tighten the brand.
