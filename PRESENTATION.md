# Skill presentation — house pattern

Every skill JJ writes presents a run the same way: a **banner** when it starts, a
**report** when it ends, and the **signature** `github.com/doublej` on both.
Sources: the session-search boot banner and the pimpelmees `/land` report.

Each SKILL.md carries its own filled-in `<presentation>` block (real banner text,
real report columns). Installed skills are symlinked one by one, so the block may
not point back to this file.

<tiers>
Pick one per skill.

- **run**: the skill does work and reports on it (search, deploy, audit, build,
  migrate, analyse). Banner and report.
- **deliverable**: the output is text the user pastes elsewhere (lyrics, prompts,
  copy, posts, commit messages). Banner and report around it. The deliverable
  itself stays clean: no box art and no signature inside it.
- **reference**: knowledge consulted mid-task (API docs, framework guides). No
  banner, no report. When the user invoked the skill directly and its answer is
  the main output, end with the footer line.
- **mode**: changes how Claude behaves for the rest of the session. No banner, no
  report. One activation line that ends with the footer.
</tiers>

<banner>
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   SKILL NAME                                                 ║
║   One-line purpose                                           ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

- 64 columns. Every line has the same width; pad with spaces up to the right `║`.
- Name in capitals, hyphens become spaces. Add `vN.N` only if the skill tracks a version.
- Multi-phase runs may add a `╠═…═╣` divider, up to five `[LOAD] <step>` lines and
  `System ready.`, as session-search does.
- Print it once, as the first thing in the response. Not again on follow-ups.
</banner>

<report>
```
SKILL NAME  ──  <subject>   <key>: <value>   <key>: <value>

<COLUMN>          <COLUMN>    <COLUMN>
──────────────────────────────────────────
<row>             ✓           <value|—>

github.com/doublej
```

- Header: the name in capitals, ` ── `, what was acted on, then at most three
  `key: value` run facts.
- Body: a fixed-width table with one row per item (file, repo, match, finding,
  track). With no rows, use at most five aligned `key  value` lines.
- Marks: `✓` done or passed, `✗` failed, `—` none or not applicable, `…` still
  running. No emoji.
- A failure is a row, with its cause in the last column or on one line under the
  table.
- The last line of the block is `github.com/doublej`.
- Detail that does not fit a row (findings, links, the next step) goes after the
  block as short prose.
</report>

<footer>
Reference and mode skills use one line: `— <skill-name> · github.com/doublej`
</footer>

<in_a_skill>
- Place the `<presentation>` block straight after the title and intro, so it is read
  before the workflow.
- Keep it under 25 lines, filled in for that skill.
- A skill that already has an output or report section gets that section converted
  to the pattern. Do not add a second one next to it.
- Skill-specific output rules (return formats, file deliverables) stay. The pattern
  wraps them and does not replace them.
</in_a_skill>
