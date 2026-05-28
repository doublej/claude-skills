# Library Decision Matrix

## The decision in one sentence

Pick the toolkit your team can ship with, then make it obey the
manifesto. The library is the smallest decision in this skill.

## Decision matrix

| Stack  | Library                     | Pick when                                              | Avoid when                              | Watch for                              |
|--------|-----------------------------|--------------------------------------------------------|-----------------------------------------|----------------------------------------|
| Rust   | ratatui                     | dense data, perf-critical, lazygit-class app           | flexbox-style layouts feel right        | mixed-weight border traps              |
| Rust   | iocraft                     | flexbox feels right, atlas-picker-class app            | minimum binary size matters             | younger ecosystem, smaller community   |
| Go     | bubbletea + lipgloss + bubbles | speed-of-build wins, Charm conventions are fine     | non-Elm-arch teams that want OO state   | lipgloss border doubling on adjacency  |
| Python | Textual                     | CSS fluency on team, theming/web parity desired        | startup time matters                    | over-styling temptation                |
| Python | Rich (output only)          | output formatting, no interactivity                    | input or interactive state needed       | DON'T treat Rich as a TUI lib          |
| TS     | Ink                         | Node ecosystem, React mental model, dev-tool TUI       | latency-sensitive workloads             | flexbox cell-rounding bugs             |
| TS     | OpenTUI                     | perf required, Bun/Deno hosts, signals fit             | community size matters                  | API churn, docs gaps                   |
| Zig    | vaxis                       | Zig project anyway, modern terminfo                    | non-Zig stack                           | nascent ecosystem                      |

## When the right answer is "no TUI"

Three cases, no shame in any of them.

- **One-shot output.** Plain stdout plus a Rich/lipgloss table is
  faster, pipeable, and survives in a CI log. Ship the pipe.
- **Long-running daemon.** Log file plus a separate dashboard
  (web, Grafana, lazyjournal). Don't trap the daemon's UI inside its
  own process.
- **Truly graphical needs.** Image previews, drag-and-drop, scrubbing
  timelines. Ship a desktop app — Tauri, native, web. Don't fight the
  cell grid.

The Taste Rubric's "could this be JSON" check is the same idea: if
`cmd | jq --watch` would do the job, the TUI is overkill.

## Capability floor by library

Quick reference. None of this is exhaustive — verify before depending.

| Library     | Truecolor       | Mouse       | Bracketed paste | Focus events | Synchronized output |
|-------------|-----------------|-------------|-----------------|--------------|---------------------|
| ratatui     | yes             | yes         | yes (crossterm) | yes          | yes (recent)        |
| iocraft     | yes             | partial     | partial         | partial      | partial             |
| bubbletea   | yes             | yes         | yes             | yes          | yes                 |
| Textual     | yes             | yes         | yes             | yes          | yes                 |
| Ink         | yes             | partial     | partial         | partial      | manual              |
| OpenTUI     | yes             | partial     | partial         | partial      | yes                 |
| vaxis       | yes             | yes         | yes             | yes          | yes                 |

When a row says "partial," budget time to write the polyfill or pick
another lib.

## Async + reactivity reference

The shape of state and redraw in each. Pick by *who owns the loop*.

- **ratatui** — pull-based. You own the event loop, you call `terminal
  .draw(|f| …)`. Async state lives in your code, not the lib.
- **iocraft** — hook-based, smol async. `hooks.use_state`,
  `use_async_handler`. Atlas-picker is the canonical example.
- **bubbletea** — Elm architecture. `Init` / `Update(msg) -> (model,
  cmd)` / `View`. Commands wrap async work and feed back as messages.
- **Textual** — asyncio plus reactive attributes. `@reactive`, async
  event handlers. CSS-driven styling.
- **Ink** — React. `useState`, `useEffect`, components. `useInput` for
  keys.
- **OpenTUI** — signals. Fine-grained reactivity, Bun-native. Mental
  model closer to SolidJS than React.
- **vaxis** — pull-based, like ratatui. You own the loop in Zig idiom.

The architectural choice is *who owns the redraw* — the lib or you.
Ratatui and vaxis hand it back to you. Bubble Tea, Textual, Ink, iocraft,
OpenTUI hide it behind a render tree. Both are valid; pick by team
fluency.

## Cross-cutting rules

These hold regardless of library:

- Every library can be made to look like AI slop. None enforce taste.
- Every library supports themes. Configure two minimum: light and dark.
- Every library can leak emoji into output. The discipline is yours.
- Capability detection is the user's terminal's job, not the lib's. The
  lib reports what it sees; you decide what to do about it.
- Every library has a "default look" that announces the library more
  loudly than the product. Override it. Tokens first, components after.

## Reference TUIs by library

Read these before designing. They are the bar.

- **ratatui** — lazygit, gitui, bottom, atuin, yazi, helix's prompt.
- **bubbletea** — gum, glow, soft-serve, charm's full catalog.
- **Textual** — posting, harlequin, frogmouth, dolphie, memray's TUI.
- **Ink** — claude-code itself, gemini-cli, ink-ui's gallery.
- **iocraft** — atlas-picker (this user's reference, in
  `multi-stack/project-atlas/atlas-picker/`).
- **vaxis** — zenith.
- **OpenTUI** — opentui's own examples; smaller corpus, growing.

A pattern that ships in two of these is a pattern. A pattern that ships
in zero is an experiment. Know which you are running.
