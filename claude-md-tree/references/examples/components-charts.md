# Example: src/components/charts/CLAUDE.md (UI sub-domain packet)

Worked example for a UI folder with non-obvious product context. UI folders usually don't need a CLAUDE.md, but charts and forms are common exceptions.

```markdown
# Charts Context

## What this folder owns
Reusable chart components for analytics and reporting views. **Does not
own:** the analytics data pipeline (lives in `src/analytics/`), or the
chart-page containers (those live in `apps/web/app/(dashboard)/`).

## Mental model
Chart components are **dumb renderers**. They receive normalized,
already-filtered data from a page-level container. They do not fetch.
A chart that fetches is a bug — it duplicates state and breaks
filter sync across the page.

Each chart cleanly separates four concerns:
1. Data normalization (a pure function: raw rows → chart series).
2. Visual rendering (the SVG / canvas output).
3. Interactive behavior (tooltip, legend, hover).
4. Empty / loading / error states.

Splitting these makes test, story, and design-review small.

## Important invariants
- Chart components do not fetch. Why: page containers own data; if a
  chart fetches, two filters can disagree and the user sees a paradox.
- Empty states explain *why* no data is visible. Why: "No data" is
  the most common bug-report trigger. We say "No sessions in the
  selected range" instead.
- Tooltips use product vocabulary, not raw column names. Why: users
  see `monthly_active_users`, not `mau_cnt`.
- Colors come from `packages/ui/tokens.ts`. Why: chart-local color
  constants are a long tail of inconsistency.

## Common change patterns
- New chart type:
  - Add component in this folder.
  - Add a normalization function in `normalize.ts` (one per chart).
  - Storybook stories for: default, empty, loading, error, dark mode.
  - Visual test in `__tests__/<Name>.test.tsx`.

## Verification
- `pnpm test charts` — unit tests for normalization + states
- `pnpm storybook` and manually visit the new chart's stories
- `pnpm e2e:visual charts` — Playwright visual diffs

## Related context
- `packages/ui/CLAUDE.md` — design tokens, color usage
- `docs/design/charts.md` — visual conventions
- `.claude/rules/accessibility.md` — a11y for chart tooltips and legends
```

Notes:

- **UI folders usually don't get a CLAUDE.md.** Charts qualify because there's non-obvious *product* context — when to show "No sessions in range" vs "No data," when to fetch, how to handle empty states. A button doesn't have any of that.
- **Anti-scope blocks the wrong direction.** "Does not own the analytics pipeline" tells Claude where the data layer lives.
- **The four-concern split is the entire reason this packet exists.** Without it, every chart accumulates fetch logic and tooltip strings.
- **Verification names the visual test path** — a chart that passes unit tests but fails a visual diff is a half-shipped chart.
