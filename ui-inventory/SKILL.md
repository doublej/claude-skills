---
name: ui-inventory
description: "Read-only audit of every page in a SvelteKit app, producing one component inventory that would make the UI fully consistent. It goes page by page in route order, matches each visible UI block to a kit component or to a proposed extension or new component, and flags hand-rolled markup with file:line. Writes docs/ui-component-inventory.md and changes nothing else. Use when asked for a 'component inventory', 'UI consistency audit', 'which components does each page use', 'harmonize the UI', 'find hand-rolled markup', 'map pages to the kit', or '/ui-inventory'. For alignment of a live page use ui-align; for typography from screenshots use ui-type-lint."
---

# ui-inventory

Audit every page of a SvelteKit app and build one component inventory that would make the UI fully consistent. This is an assessment. Write the report file and change no other file. The fixes come later, from the report.

<arguments>
- App directory: the argument if one is given, otherwise the nearest directory at or above cwd that has `svelte.config.js` or `svelte.config.ts`. All paths below are relative to it. If there is no SvelteKit app, reply `No SvelteKit app found at <path>` and stop.
- Report path: `docs/ui-component-inventory.md` unless the user names another one.
</arguments>

<setup>
1. **Pages.** List every route page: `find src/routes -name '+page*.svelte' | sort`. This includes `+page@*.svelte` layout resets. Put them in route order: sort by URL path with `(group)` segments left out, parents before children. Record the count N. This list is the scope.
2. **Kit.** Find the shared component directory (usually `src/lib/components/ui/`) and any doc that already lists its blocks: a `CLAUDE.md` or `README.md` in that directory, or a design doc under `docs/`. Seed the inventory from it, one entry per existing component, with its real path and props. When the report file already exists, read it too and carry over its entries. Build on an inventory that is already there instead of starting from nothing.
3. **Dev server.** Find the port in `vite.config.*` (`server.port`) or the project `CLAUDE.md`. Check it with `curl -s -o /dev/null -w '%{http_code}' http://localhost:<port>/`. If it answers, you may open a page to look at it. Do not start a server. For pages that need data you cannot load, work from the code.
</setup>

<extraction>
For each page, read the `+page*.svelte`, every `+layout.svelte` above it that adds UI, and the components it renders. List its visible UI blocks: the units a user sees as one thing, such as a header, button, tabs, table, form field, banner, empty state, dialog, card or toolbar. Leave out layout-only wrappers. For each block note the file:line, whether it uses a kit component or is hand-rolled, and its structure and behaviour.

If N is more than 15, split the extraction. Dispatch read-only subagents (`model: "opus"`), each with about 8 pages that share a route prefix. Each one returns the block list above for each of its pages and edits nothing. The matching pass below always stays in the main session, because its decisions depend on order.
</extraction>

<matching>
Go through the pages one at a time, in route order, and match every block to an inventory entry:
1. Fits an entry as-is → record the match.
2. Almost fits → extend that entry with a new prop or variant, when the need has the same structure and behaviour: the same parts and the same interaction. Note which earlier pages the change touches.
3. Different structure or behaviour → add a new entry, with the reason an extension would not work. An example is a sortable table next to a static list.

Hand-rolled markup that copies a kit component counts as a mismatch, even when it looks right. So does a kit component that a page restyles locally.
When a later page changes an entry, update the earlier pages' rows too, so the final tables describe one consistent set.
A page is `full-page` when the shell layout does not wrap it: a `@` layout reset, or a condition in the shell layout that renders it bare.
</matching>

<report>
Write the report path with these sections, in this order:

1. **Components**: one row per entry: name · purpose · file (existing path, or `new`) · props/variants · pages that use it.
2. **Pages**: one row per route, in route order: route · components used · mismatches (hand-rolled or divergent markup, with file:line; `none` when clean) · `full-page` when it runs outside the shell.
3. **Decisions**: one row per extend/new decision, in the order made: entry · extend or new · reason · pages affected.
4. **Not inspected**: only when a page could not be read. Give each one with the reason.

Before you reply, count the Pages rows plus the Not inspected rows. The total must equal N. If it does not, find the missing routes and add them.
</report>

<reply>
Reply with:
- the report path
- `<rows> of <N> pages covered` (plus the Not inspected count, if any)
- the five changes that would harmonize the most pages, ranked by how many pages each one clears, each with its page count.

Done when every page file from setup step 1 appears in the Pages table or under Not inspected. Stop there. Do not start fixing pages.
</reply>
