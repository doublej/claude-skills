---
name: code-optimize
argument-hint: "[dimensions…] [path] — structure | practices | claude-md | smells | simplify | modularize | logging | arch | glossary | docs | perf <target> · none = all but perf"
description: "Catch-all codebase improver you can throw at any project: one entry point that reads the project's atlas record, picks safe repo handling (foreign repo, dirty tree, no git, gitflow), then fans out over dimensions (structure, practices, claude-md, smells, simplify, modularize, logging, arch, glossary, docs, perf). Each dimension runs scan → plan → fix → verify → commit, with a count ratchet so gains only go one way. The practices dimension enforces JJ's house rules: atlas catalog, port and dev hostname, dev-tree paths, onenv, one package manager, nothing vendored in git. Replaces full-optimize, code-refactor, and code-simplify. Use it for whole-codebase cleanup; invoke a dimension skill (code-audit, code-logging, …) directly only when the user wants exactly one dimension. Triggers on '/code-optimize', 'optimize this codebase', 'full optimize', 'clean up everything', 'improve this project', 'refactor the codebase', 'simplify the codebase', 'make this faster', 'hill climb', 'ratchet'."
---

# Code Optimize

One entry point to improve a whole codebase. The user picks dimensions as
arguments (`/code-optimize smells logging`); zero arguments = all dimensions.
The run starts with an intake, gets one approval for one merged plan, then
fixes dimension by dimension. Each fix is verified, committed, and ratcheted.

<dimension_registry>

| Dimension | Owner | Scan command |
|---|---|---|
| `structure` | this skill — `references/structure.md` | `python3 ~/.claude/skills/code-optimize/scripts/scan_codebase.py <root> --json` |
| `practices` | this skill — `references/practices.md` | `python3 ~/.claude/skills/code-optimize/scripts/scan_practices.py <root> --json` |
| `claude-md` | **claude-md-tree** skill | skill's own audit workflow (no scan script) |
| `smells` | **code-audit** skill | `python3 ~/.claude/skills/code-audit/analyze.py <root> --json` |
| `simplify` | this skill — `references/simplify.md` | `python3 ~/.claude/skills/code-optimize/scripts/scan_codebase.py <root> --json` |
| `modularize` | **code-modularize** skill | `python3 ~/.claude/skills/code-modularize/scripts/scan_files.py <root> --json` |
| `logging` | **code-logging** skill | `python3 ~/.claude/skills/code-logging/scripts/scan_logging.py <root> --json` |
| `arch` | **code-arch-drift** skill | `python3 ~/.claude/skills/code-arch-drift/scripts/archcheck.py --root <root> --json` |
| `glossary` | **code-glossary** skill | skill's own harvest phase (no scan script) |
| `docs` | **audit-docs**: skill `~/.claude/skills/audit-docs/` or command `~/.claude/commands/audit-docs.md` | its own workflow |
| `perf` | this skill — `references/perf.md` | benchmark built per target; no repo-wide scan |

For delegated dimensions, load the owning skill's SKILL.md (or the audit-docs
command file) and follow its pipeline. This dispatcher only sequences, scopes,
ratchets, and commits. For `structure`, `practices`, `simplify`, and `perf`,
load the named reference from this skill.

</dimension_registry>

<intake>

Run once, before any scan. It ends in a one-line intake summary that the plan
repeats: `type · runner · gates · repo mode · branch · commit style`.

1. **Project record.** From the root: `atlas info --json`. It gives `type`,
   `framework`, `runner`, `scripts`, `justRecipes`, `devCommand`, `slug`, `git`
   (`clean`/`dirty`/`no-repo`) and `flow` (`policy`, `integration`, `owner`).
   `No scanned project` inside `~/dev` → `atlas scan`, retry once (atlas-cli
   skill). Atlas missing, or the root is outside `~/dev` → detect from manifests:

   | Manifest | Stack |
   |---|---|
   | `package.json` (+ `bun.lock`/`pnpm-lock.yaml`/`yarn.lock` → runner) | Node/TS |
   | `pyproject.toml` / `setup.py` (+ `uv.lock`) | Python |
   | `Cargo.toml` · `go.mod` · `Package.swift` | Rust · Go · Swift |
   | `*.sln` / `*.csproj` · `pom.xml` / `build.gradle(.kts)` | C# · Java/Kotlin |
   | `Gemfile` · `composer.json` · `pubspec.yaml` · `CMakeLists.txt` | Ruby · PHP · Dart · C/C++ |

   Several manifests → multi-language; run each dimension across all of them.

2. **Ownership.** The repo is **foreign** when `flow.policy` is `external`, or
   when `git remote get-url origin` names an owner other than `doublej`. For a
   foreign repo: drop `claude-md`, `glossary`, and `practices`; put `.optimize/`
   in `.git/info/exclude`; never push.

3. **Repo mode.** Pick the first row that matches:

   | State | Mode |
   |---|---|
   | no git | Ask once (consult-user-mcp `confirm`): "Put this folder under git with a snapshot commit so every fix can be reverted?" Yes → write a `.gitignore` for the stack's vendored and build dirs, then `git init -q && git add -A && git commit -qm "chore: snapshot before optimize"`. No → **report-only**: SCAN and PLAN, save the plan, stop. |
   | dirty tree | Ask once (`pick`): commit it first (smart-commit), stash, or work in a worktree. On cancel or AFK, use a worktree: `git worktree add -b <branch> .claude/worktrees/optimize-<ts> <base>`, then add `.claude/worktrees/` to `.git/info/exclude`. Uncommitted work is never touched. |
   | clean | Branch in place. |

4. **Branch.** If `flow.policy` is `gitflow`, branch `feature/optimize-<ts>` off
   `flow.integration` (usually `develop`). Otherwise branch `optimize/<ts>` off
   the current HEAD. Never create `develop` and never run `atlas flow init` during
   this run.

5. **Gates.** Build the verify list from what the repo already has, in this order:
   a `just check` recipe; else the `lint`/`typecheck`/`test` recipes that exist;
   else package scripts run through `runner` (`bun run test`, `uv run pytest`);
   else stack defaults (`cargo clippy && cargo test`, `go vet ./... && go test ./...`).
   Also note a build command (`just build`, `bun run build`, `cargo build`) for the
   end-of-run smoke. **Run the gates once now.** A gate that is already red becomes
   the baseline: from then on a cluster passes when it adds no new failures, and
   the plan names the red gates.

6. **Commit style.** Read `git log -20 --format=%s`. For conventional commits
   use `refactor(<dimension>): <summary>` (`chore(practices): …` for config-only
   fixes). For any other house style, follow it and keep the dimension name in the
   subject. No history → `refactor(<dimension>): <summary>`.

</intake>

<dimension_selection>

1. Parse `$ARGUMENTS` for dimension names (whitespace-separated, matching the
   registry's first column). Unknown names → list valid dimensions and ask once
   via consult-user-mcp `pick`.
2. No arguments → **all dimensions**. The **only** conditions that drop a
   dimension from the default set are:
   - `docs`: audit-docs is neither a skill nor a command.
   - `claude-md` / `glossary`: the repo is a throwaway (no CLAUDE.md **and**
     the user did not ask for one), or the repo is foreign.
   - `practices`: the repo is foreign.
   - `perf`: always opt-in. It needs a named target (`/code-optimize perf <target>`);
     named without one → ask once for the hot path or journey.
3. Resolve target root from `$ARGUMENTS` path (if given) or cwd.

**No other reason, including token budget, time, or "seems low-value", justifies
silently dropping a dimension.** To skip one for a reason not listed above, ask
the user first via consult-user-mcp `confirm`. Don't just announce the skip in
the final message and carry on.

**Dropped means off.** Don't improvise a substitute agent for a dropped dimension.
`arch` without a blueprint is not dropped: code-arch-drift's no-blueprint mode
reports the layer split, and the dimension has no ratchet.

</dimension_selection>

<coverage>

Every scan script reports `coverage.scanned` and `coverage.unscanned` (source
files by extension). A dimension that scanned **zero** files of the project's
stack reports `no scanner for <exts>`, not "zero findings", and gets no
ratchet. Partial coverage appears in the plan as one blind-spots line, for
example `logging: .lua (12) unscanned`.

</coverage>

<shared_contract>

Every dimension runs the same five steps:

```
1. SCAN    read-only, no writes at all (no ratchet, no caches in the repo);
           machine output via --json where a scan command exists
2. PLAN    all dimensions' findings → ONE merged plan (references/plan-format.md),
           saved under .optimize/runs/<ts>/; a dimension ratcheted for the
           first time in this repo also runs <prove_the_count>; ONE approval
           for the whole run: the user may drop dimensions or clusters
3. FIX     per dimension, in <execution_order>. First
           `ratchet.py <root> lower --dimensions <d>` (earlier dimensions have
           moved the code), then the hill-climb loop (references/hill-climb.md
           <loop>) until a full pass lowers the count by < 5%
4. VERIFY  the intake gate list per cluster: no new failures against the
           baseline; up to 3 fix cycles, then revert that cluster
5. COMMIT  one commit per cluster in the intake commit style, together with
           the lowered .optimize/baseline.json
```

Start the FIX step by quoting the <loop> stop rule from references/hill-climb.md.
Dimensions without a count (structure, claude-md, glossary, docs) run steps
1–5 once, without the ratchet.

`.optimize/baseline.json` is committed: it is the CI ceiling. `.optimize/runs/`
is not. Write `runs/` into `.optimize/.gitignore` the first time.

</shared_contract>

<fan_out>

**Scans run in parallel, fixes run serially.**

- Spawn one subagent per selected dimension in a SINGLE message (multiple Agent
  calls, `subagent_type: Explore`). Each subagent runs its dimension's SCAN and
  returns findings plus `coverage` as JSON/markdown. It makes no edits and does
  not run `ratchet.py`. Only the lead writes `baseline.json`, so there is one writer.
- The lead merges all scan results into one ranked hit list (group by
  dimension, sort by severity/impact) and presents it before touching anything.
- FIX phases then execute one dimension at a time in the order below, because
  dimensions touch overlapping files and parallel fixing would conflict. When the
  user asks for speed, use references/hill-climb.md <parallel> instead.

</fan_out>

<execution_order>

```
structure   → files land in final locations first; every later dimension
              sees stable paths
practices   → untrack vendored dirs, fix paths, ports and project wiring before
              code-level edits; shrinks the file set later scans see
claude-md   → context tree written against the new layout (keeps the
              practices dev-hostname line)
arch        → boundary rules checked/fixed before code-level edits
smells      → dead code and duplicates removed before restructuring modules
modularize  → oversized files split
simplify    → behavior-preserving cleanup of what remains
logging     → levels/messages fixed on final code
docs        → documents the final state
glossary    → vocabulary locked last, after all renames settle
perf        → runs on the cleaned code; only when named
```

Skip any dimension whose scan returns zero findings (with coverage), and note it
in the summary.

</execution_order>

<smoke_run>

After the last dimension, once per run:

1. The build command from the intake. A build that passed at intake and fails
   now is a regression: bisect the run's commits (`git bisect run <build>`) and
   revert the culprit cluster.
2. The project serves (a `devCommand` of `dev`/`start`/`serve`, or practices saw
   a dev server), the repo is not foreign, and atlas is present: follow
   atlas-hostname step 5 (`atlas run`, `lsof` the listener, `curl` the hostname).
   This is the only hostname registration in the run. Settle the slug first
   (step 4), because each registration costs two certificates.
3. Every URL in the summary is `https://<slug>.atlas.local.jurrejan.com`. Use
   localhost only as the stated fallback when `nasSynced: false` or when the
   project has no registration.

</smoke_run>

<output_format>

After all dimensions complete, summarise:

```
## Code Optimize — Complete

Intake: <type · runner · gates · repo mode · branch · commit style>

### Dimensions run
- structure: [N] files moved, [N] dirs merged
- practices: count [before] → [after] ([rules fixed])
- smells: count [before] → [after], [N] dead code blocks removed
- simplify: count [before] → [after], [N] files simplified ([−N] lines)
- perf:<name>: count [before] → [after], wall-clock [before] → [after] ([N] runs)
- ...

### Blind spots
- [dimension]: [exts] unscanned

### Verify
Gates: [green / baseline-red: <gate>, no new failures] · Build: [ok / regression reverted]
Smoke: https://<slug>.atlas.local.jurrejan.com → [code] (or: not a served project)

### Ratchet
`ratchet.py <root> check` exit [code]; wired into gates: [yes: where / offered, declined]

### Commits created
- refactor(structure): ...

### Skipped
- [dimension]: [reason — zero findings / no scanner / not installed / foreign repo / user deselected]

Branch: <branch> · Flow: <policy> · Worktree: <path, remove with `git worktree remove <path>`>
```

</output_format>

<reference_files>

- [Structure](references/structure.md) — folder-organisation dimension: detection, target tree, move mechanics with import fixes per language
- [Practices](references/practices.md) — JJ's house rules: rule → fix → owning skill (atlas-cli, atlas-hostname), and limits
- [Simplify](references/simplify.md) — behavior-preserving simplification: 6-phase execute loop, refinement rules
- [Simplify Patterns](references/simplify-patterns.md) — language-specific transformation patterns
- [Simplify Agent Prompts](references/simplify-agent-prompts.md) — scanner/analyser/executor prompt templates
- [Plan Format](references/plan-format.md) — standards detection, per-dimension checklists, analysis report + tasks.md formats, approval flow
- [Hill Climb](references/hill-climb.md) — count ratchet, prove-the-count, cluster loop and stop rule, complexity veto, parallel mode, steering nudges
- [Perf](references/perf.md) — perf dimension: deterministic counts per stack, proving them against wall-clock, known JS traps

</reference_files>

<related_skills>

| Skill | Relationship |
|---|---|
| **atlas-cli** | Intake project record, catalog fixes, flow policy |
| **atlas-hostname** | `atlas.*` practices fixes and the smoke run |
| **code-map** | Optional structural context — PageRank map before scanning |
| **code-audit** | Owns the `smells` dimension |
| **code-modularize** | Owns the `modularize` dimension |
| **code-logging** | Owns the `logging` dimension |
| **code-arch-drift** | Owns the `arch` dimension |
| **code-glossary** | Owns the `glossary` dimension |
| **claude-md-tree** | Owns the `claude-md` dimension |
| **audit-docs** | Owns the `docs` dimension (skill or command; off if neither) |
| **smart-commit** | Skill or command. Dirty-tree intake option, and splitting leftover changes |

</related_skills>
