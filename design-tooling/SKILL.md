---
name: design-toolingdescription: Use this skill to generate well-branded interfaces and assets for Tooling — a data-dense neutral design system (Linear/Vercel/Stripe lane) for SvelteKit 2 + Tailwind v4 dashboards. Use for production code or throwaway prototypes/mocks. Contains design guidelines, semantic color/type tokens, fonts, logo assets, preview spec cards, and UI kit components.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick orientation

- **Voice & content rules** — `README.md` §3 "Content fundamentals". Sentence case, no trailing periods on labels, math minus for negatives, no emoji in chrome.
- **Visual foundations** — `README.md` §4. Borders not shadows. Solid surfaces, no gradients. Linear-leaning indigo accent used sparingly.
- **Tokens** — `colors_and_type.css`. Semantic CSS vars only (`--color-bg`, `--color-fg`, `--color-muted`, `--color-pos`, `--color-neg`, `--color-accent`, …). Flip the theme by toggling `.dark` on `<html>`; never use Tailwind `dark:` utilities.
- **Type** — Geist Variable (sans) for chrome, Geist Mono (with `tabular-nums`) for tabular numerals in tables/captions, and **Instrument Serif** for hero / display numerals only — the one big number per section (Stat card values, donut center, headline figures). If a number lives in a column, it's mono; if it's the anchor of its section, it's serif.
- **Iconography** — Lucide, 1.5px stroke, currentColor. The `ui_kits/finance_dashboard/icons.jsx` file ships a typed subset (`I.Home`, `I.Search`, …); copy more from lucide.dev as needed.
- **Layout** — centered `max-width: 1100px` column, sticky 56px TopNav, 64px BottomNav on mobile, 12-col grid with 24px gutters.
- **Live reference** — `ui_kits/finance_dashboard/index.html` is a working SPA. Open it before prototyping to see real components in motion.

## When making artifacts

1. Link `colors_and_type.css` and load Geist via Google Fonts.
2. Reuse `<Money/>`, `<Stat/>`, `<DataTable/>`, `<Card/>`, `<Button/>` shapes from `components.jsx`.
3. Right-align all numerics. Use `.num` for any number that isn't already inside a `<Money/>` component.
4. Use `--color-accent` sparingly — primary buttons, active nav, focus rings, links. Everything else is fg / muted / border.
5. No drop shadows on chrome. Shadows belong on popovers, the command palette, and toasts.
6. Test the dark theme by adding `class="dark"` to `<html>`. If it doesn't look right, you're reading a hardcoded color somewhere — fix the token.

## When writing production code

The reference stack is SvelteKit 2 (Svelte 5 runes) + Tailwind v4 (`@theme` directive only, no `tailwind.config.js`) + bits-ui + `@lucide/svelte`. Mirror the React components in this kit into Svelte components with the same names and prop shapes (`Money`, `Stat`, `DataTable`, `PageHeader`, `EmptyState`, etc.). Keep semantic CSS vars as the single source of truth — Tailwind utilities should read from them, not redefine colors.
