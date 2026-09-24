# Perf — Runtime Speed Dimension

Make a named hot path faster by climbing a deterministic count instead of noisy
timings. Runs only when the user names `perf` and a target (a function, command,
page, or user journey). There is no repo-wide perf scan.

<find_a_count>

Pick the first candidate that runs on this machine and fits the target:

| Target | Deterministic count |
|---|---|
| Pure JS/TS hot path | V8 precise coverage call counts (`Profiler.startPreciseCoverage({callCount: true, detailed: true})`), or Valgrind `Ir` under `node --predictable` |
| Python hot path | `cProfile` total `ncalls`; `python -X importtime` for startup |
| Native / any CLI | CPU instructions: `perf stat -e instructions` (Linux) or Valgrind `--tool=callgrind` `Ir` |
| React UI | React commits per interaction (Profiler `onRender` count) |
| Browser page | style-recalc and layout counts, DOM mutations (MutationObserver), Layout Instability `layout-shift` entries mapped by `sources` to named regions |
| Animation / streaming | over-budget frames at a fixed frame rate: DevTools `HeadlessExperimental.beginFrame` stepping at 8.33 ms (120 Hz), headless Chrome with `--enable-begin-frame-control` |
| DB-backed path | query count per request |

Mainline Valgrind, `perf`, and begin-frame control do not run on Apple Silicon
macOS. Run those in a Linux container.

Write a benchmark that prints one number as the last token of stdout.

</find_a_count>

<prove_it>

A count qualifies only if it tracks wall-clock time:

1. Drive the count down on the target.
2. Time the before and after with warm runs (report the run count).
3. Count moved and time didn't → drop the count and try the next candidate.

Report: the benchmark command, count before → after, time before → after.
Reference points from the source sprint: −48% instructions gave −78% time,
and −31% gave −44%.

</prove_it>

<ratchet_it>

Register the qualified count in `<root>/.optimize/baseline.json`:

```json
{"perf:<name>": {"cmd": "<command that prints the count>"}}
```

then `ratchet.py <root> lower --dimensions perf:<name>` sets its ceiling.
From here the FIX step follows references/hill-climb.md <loop>, with
wall-clock re-measured on the final state.

</ratchet_it>

<known_traps>

Proven in the source sprint, worth one check each on a JS front end:
- Non-Latin-1 characters (em dash, curly quotes) make V8 store the whole string
  as UTF-16, putting every regex on the slow two-byte path. Copy the substring
  into a one-byte string before regex-heavy work.
- One `:root:has()` selector can add tens of ms to every DOM change.
- Stray `location.reload()` and main-thread IndexedDB writes of unchanged data
  are invisible to load metrics. Look for them in profiles of idle tabs.
- Hooks and store subscriptions on the typing path re-render on every keystroke.
  Take a census.

</known_traps>
