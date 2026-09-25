# Design patterns

The scaffold's design, and the rules for filling it in. Source of truth is `assets/scaffold/`; this file explains why it looks the way it does.

<direction>
Every site is one title in a series of technical handbooks: the layout is shared, and each project owns one full-bleed colour field, the **plate**. The project name is set huge in a wide monospace on that plate, and the terminal session is the only other loud thing on the page.
</direction>

<plate>
The plate is the per-project character. `src/lib/theme.ts` holds eight named plates as OKLCH triples; `+layout.svelte` injects the chosen one as `--plate-l`, `--plate-c`, `--hue` on `html:root`. Every other colour in `global.css` is derived from `--hue`, so paper, ink and terminal backgrounds all lean toward the plate.

By default the plate is picked by hashing `REPO_NAME`, so two repos rarely match. During step 3, set it on purpose when the project suggests one:

| Plate | Hue | Suits |
|---|---|---|
| `signal` | red, 22 | alerting, security, destructive or "stop the bad thing" tools |
| `marigold` | yellow, 82 | build and release tooling, generators |
| `chartreuse` | yellow-green, 118 | linters, checkers, anything that passes or fails |
| `mint` | green, 165 | data, storage, sync |
| `lagoon` | cyan, 205 | network, streaming, pipes |
| `cobalt` | blue, 262 | infrastructure, CLIs that manage other tools |
| `iris` | violet, 298 | AI, agents, MCP servers |
| `orchid` | pink, 340 | design, media, creative tooling |

```ts
// src/lib/theme.ts
const PLATE: PlateName | null = 'iris'
```

Do not add hex colours. If a new plate is needed, add an entry to `PLATES` with lightness 0.7 to 0.88 so ink text stays readable on it.
</plate>

<tokens>
| Token | Role |
|---|---|
| `--plate` | Hero and CTA fields, prompt `$`, cursor, active step, link underlines, feature markers |
| `--paper` / `--paper-tint` | Page ground / faint panel |
| `--ink` / `--ink-soft` / `--ink-faint` | Headings and text / body copy / inactive controls |
| `--rule` | Table row separators |
| `--term-bg` / `--term-bar` / `--term-text` / `--term-dim` | Terminal and command boxes |
| `--font-text` | Familjen Grotesk: all prose, headings, UI |
| `--font-mono` | Martian Mono: wordmark (width 112.5%), commands and terminals (width 87.5%) |
| `--section-padding`, `--container-*`, `--grid-gap` | Fluid spacing; `.container` is global |
</tokens>

<type>
Two families, clearly distinct. Scale in rem: body 1.0625, h3 1.25, tagline 1.3 to 1.75, h2 1.75 to 2.5, CTA h2 2 to 3.5, page h1 2.25 to 4.5. The hero wordmark is sized from its character count (`--chars`) so it fills the container width on one line at any viewport.

- Sentence case everywhere. No all-caps labels, no eyebrows above headings.
- No arrows appended to link text. Links are ink with a plate-coloured underline.
- Headings use `text-wrap: balance`; prose runs through `obliterate` for orphans.
</type>

<layout>
Left-aligned throughout, on a 4:7 two-column grid that collapses to one column at 860px.

```
Home                                   Features
[nav: ■ wordmark ........ links]       [nav]
██ PLATE █████████████████████████     ██ PLATE ██████████████████
██ WORDMARK (fills width)       ██     ██ What X does │ description ██
██ tagline      │ toggle        ██     █████████████████████████████
██              │ $ command     ██     feature text │ Terminal
█████████████████████████████████      feature text │ Terminal
steps (numbered) │ Terminal            ─────────────────────────
─────────────────────────────────      Compared with the alternatives
What it does │ ■ dt  ■ dt              [compare-table, .ours column tinted]
             │ ■ dt  ■ dt
██ PLATE: Install X │ $ command ██
```

- The plate appears at most twice per page: the top field and the closing CTA.
- Numbered markers only on the demo steps, because they are a real sequence. Features are a `<dl>`, not numbered and not cards.
- A 2px ink rule opens the features and comparison sections. No other dividers.
- Radius is small and hierarchical: 6px terminals, 4px command boxes and toggles, 3px buttons.
</layout>

<components>
**Nav** (`Nav.svelte`): sticky, paper at 84% with blur. Plate square + wordmark in wide mono. Active link gets a plate underline and `aria-current="page"`. Edit `links`; keep GitHub last.

**Terminal** (`Terminal.svelte`): `<figure>` with a title bar (`title`, default `zsh`) and a body that prints lines in on mount. Props: `title`, `maxWidth`, children. Each direct child is one line. Classes for output:

| Class | Use |
|---|---|
| `.t-prompt` | Empty span before a command; renders the `$` in plate colour |
| `.t-hi` | The line the user came for |
| `.t-dim` | Headers, hints, secondary output |
| `.t-ok` / `.t-err` | Success / failure |

```svelte
<Terminal title="~/{{REPO_NAME}}">
  <div><span class="t-prompt"></span>tool run --fast</div>
  <div class="t-dim">scanning 214 files</div>
  <div class="t-ok">0 problems</div>
</Terminal>
```

**Command box** (home page): dark box with `$`, the command and a Copy button that reads "Copied" for two seconds. The Run/Install/Agent toggle uses `aria-pressed`; delete modes that do not apply.

**Comparison table** (`.compare-table`, global): first column is `<th scope="row">`; mark the project's column cells with `class="ours"`. Wrap in `.table-scroll` so it scrolls at 375px.
</components>

<responsive>
- 860px: all two-column grids stack; the command block drops under the tagline.
- 560px: feature list goes to one column; command and terminal text shrink.
- Long commands scroll inside their box; the page itself never scrolls sideways. Grid columns use `minmax(0, 1fr)` for this; keep that when adding columns.
- Check 375, 768 and 1440px.
</responsive>
