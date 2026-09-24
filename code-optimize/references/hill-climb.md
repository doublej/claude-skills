# Hill Climb — Count, Prove, Climb, Ratchet

How the FIX step runs inside a dimension. Source: Anthropic's claude.ai speed
sprint (Aug 2026), where the rule was "once Claude can measure something, it can
make it faster": every deterministic count became both a target to drive down and
a CI ceiling that only goes down.

<ratchet>

One count per dimension, stored in `<root>/.optimize/baseline.json`:

```bash
python3 ~/.claude/skills/code-optimize/scripts/ratchet.py <root> lower [--dimensions logging smells]
python3 ~/.claude/skills/code-optimize/scripts/ratchet.py <root> check [--json]   # exit 1 = a count rose
```

| Dimension | Count |
|---|---|
| `arch` | violations from archcheck (skipped when the repo has no blueprint) |
| `logging` | sum of `issue_counts` + `gap_counts` |
| `smells` | code-audit `count` (deprecated + conventions + deadcode + duplicates) |
| `modularize` | files over the line threshold |
| `simplify` | summed per-file `complexity` |
| `perf:<name>` | custom `cmd` entry, see references/perf.md |

`structure`, `claude-md`, `glossary`, `docs` have no deterministic count: they
run the normal plan → fix flow without a ratchet.

`lower` never raises a ceiling. Raising one is a manual edit to
`baseline.json` that the user approves first.

</ratchet>

<prove_the_count>

Before climbing a count for the first time in a repo, show that it tracks real
problems. A count that doesn't gets tightened or dropped. Climbing it would
optimize noise.

1. Pick 5 findings at random (record the seed).
2. For each: file:line, and one line on whether a senior reviewer on this repo
   would fix it.
3. Present the table to the user: `dimension | real (n/5) | keep / tighten / drop`.
   Fewer than 4 of 5 real → propose a scanner filter or drop the dimension's
   ratchet. The user decides.

Skip this step when `baseline.json` already has the dimension: it was proved
on an earlier run.

</prove_the_count>

<loop>

After plan approval, the approval covers the whole dimension, not just the
first cluster. Work one cluster at a time:

1. Take the largest cluster of findings from the latest scan.
2. Find or write the smallest check that fails on it: a test, a scan filter, a grep.
3. Fix it. Run the quality gates. Commit `optimize(<dimension>): <summary>`,
   one commit per cluster.
4. `ratchet.py <root> lower --dimensions <dimension>`. The count dropped and
   the gates are green: commit the baseline with the fix. Otherwise revert
   that cluster's commit and try another approach.
5. Go to the next cluster. The first plan's target is not the stopping point.
   Stop the dimension when one full pass lowers its count by less than 5%, or
   the count reaches zero.

Reject any fix that adds more code or tooling than the findings it removes.
Say "not worth the complexity: <gain> vs <cost>" and take the next cluster.

Ask before: changing a public API, deleting files, touching another
dimension's findings, raising a ceiling.

</loop>

<ci_ratchet>

At the end of the run, offer once to add `ratchet.py <root> check` to the
repo's gates (justfile recipe, pre-push hook, or CI step, whichever the repo
already uses). Add it only on a yes. Without it the ceilings are advisory.

</ci_ratchet>

<parallel>

Dimensions that move files (`structure`, `modularize`) run first and serially.
The rest can run as one subagent each, in a single message, with model
"opus", each in its own worktree on `optimize/<dimension>`, each given this
file's <loop> and its own count. Merge the branches one at a time and re-run
the gates plus `ratchet.py check` after each merge. Use this only when the
user asks for speed, because serial is the default.

</parallel>

<nudges>

Lines the user can paste when a dimension stalls. When the user sends one,
act on it as written.

- "Put it up now. The tests and the ratchet are the safety net, not your caution. Be bolder about scope inside this dimension."
- "The baseline is not the stopping point. What's the next largest cluster? Keep going."
- "Your current check can only see <X>. Build a stricter one that sees <Y>, then climb that."
- "Vetoing that one: <gain> isn't worth maintaining <thing>. Revert and take the next cluster."
- "What haven't we measured? List 5 counts this repo could add that expose problems the current scans miss, each with the command that produces it and one example finding. Mark the wacky ones."

</nudges>
