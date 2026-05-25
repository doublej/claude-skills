# Finance Dashboard — UI Kit

Interactive recreation of the implied product surface: a personal finance / portfolio dashboard SPA. Linear/Vercel-style data-dense neutral aesthetic.

## Run

Just open `index.html` — it's a self-contained React + Babel app. No build step.

## What's in it

| File | Role |
|---|---|
| `index.html` | Shell; loads fonts, root CSS, and all JSX modules in order |
| `tokens.css` | Kit-scoped styles. Extends `../../colors_and_type.css` |
| `data.js` | Sample portfolio data + formatters (`fmt.money`, `fmt.pct`, `fmt.num`) |
| `icons.jsx` | Lucide-shaped React icon set (`I.Home`, `I.Search`, …) |
| `components.jsx` | `Button`, `Badge`, `Tag`, `Money`, `Pct`, `Sparkline`, `Card`, `Stat`, `EmptyState`, `PageHeader`, `DataTable`, `Toast`, `useTheme`, `usePrivacy` |
| `nav.jsx` | `TopNav` (sticky, grouped dropdowns), `BottomNav` (mobile), `CommandPalette` (⌘K) |
| `charts.jsx` | `PriceChart` (area + crosshair), `AllocationDonut` |
| `screens.jsx` | `OverviewScreen`, `AccountsScreen`, `TransactionsScreen`, `HoldingsScreen`, `ReportsScreen` |
| `app.jsx` | Entry: route state, ⌘K handler, mounts root |

## Interactive things to try

- **⌘K** — open the command palette; ↑/↓ + Enter to navigate
- **⌘⇧P** — toggle privacy blur on the `Money` component
- Top-nav **Accounts** / **Holdings** — grouped dropdowns
- Theme toggle (top-right) — flips `.dark` on `<html>`; tokens swap
- Recent activity → **View all** → Transactions
- Filter tabs on Transactions (All / Trade / Income / Transfer)
- Connect account / New transfer / Export — fire `svelte-sonner`-style toasts
- Resize narrow — `DataTable` collapses to `mobileCard` rows; mobile `BottomNav` appears

## Component conventions

- Money values render through `<Money value={...}/>` so privacy mode picks them up automatically.
- Tables use `num: true` on the column descriptor for right-aligned tabular cells.
- Every interactive surface has a `:focus-visible` ring and a hover state that uses `--color-card-2` (no shadow lift).
- Color is always read from `var(--color-*)`. No `dark:` utilities — `.dark` on the root flips the token set.

## Caveats vs the production stack

This is a hi-fi visual prototype, not a 1:1 of the Svelte source:

- Built in **React + Babel** in-browser instead of SvelteKit + Vite. Component shapes mirror what the brief implies (`Money`, `Stat`, `DataTable` with `mobileCard`, etc.) — port them to Svelte 5 runes by hand when ready.
- Charts are hand-rolled SVG instead of `lightweight-charts`. Drop the real library in for production candles/areas.
- `bits-ui` primitives are replicated lo-fi (the dropdown is a plain popover). Swap for real `Popover` / `DropdownMenu` from `bits-ui`.
- Toasts are local state, not `svelte-sonner`.
- `vaul-svelte` drawer not yet implemented.
- Cmd-K palette is local; production should use a dedicated library or build on top of `bits-ui`'s dialog.

## Adding new screens

1. Add a screen component in `screens.jsx` that returns `<><PageHeader/> ... </>`.
2. Add a route in `app.jsx`'s screen switch.
3. Add a `TopNav` entry in `nav.jsx`'s `items`, and a `BottomNav` entry if appropriate.
4. Add a Cmd-K navigate item in `CommandPalette`'s `allItems`.
