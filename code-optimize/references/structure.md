# Structure — Folder Organisation Dimension

Optimize where files live. Goal: a newcomer (or agent) finds any file on the
first guess, and the tree communicates the architecture. Every move ships with
its import-path fixes in the same commit — the build never breaks mid-dimension.

<scan>

1. Run the bundled scanner for the file inventory, import/consumer map, and
   detected sections:

```bash
python3 ~/.claude/skills/code-optimize/scripts/scan_codebase.py <root> --json
```

Key fields per file: `imports`, `consumed_by`, `loc`; top-level: `sections`
(frontend/backend/shared/tests/scripts or top-level dirs).

2. Get the raw tree: `git ls-files | sort` — gives you every tracked path
   without noise dirs.

3. If the code-map skill is installed, a PageRank map
   (`bash ~/.claude/skills/code-map/scripts/repomap.sh <root> --root <root> --map-tokens 8192 --exclude-unranked`)
   shows which files are load-bearing — move those with extra care and first.

</scan>

<detections>

Work through these five detection classes. Report each finding as
`{path, class, evidence, proposed_target}`.

## 1. Misplaced files

A file is misplaced when its *relationships* point elsewhere than its location:

- **Consumer mismatch** — all of a file's `consumed_by` entries live in another
  directory. `src/components/formatDate.ts` imported only by `src/api/` →
  belongs near its consumers or in `shared/`.
- **Kind mismatch** — file's kind contradicts the dir's purpose: a React
  component in `utils/`, a pure function library in `components/`, SQL in
  `src/models/` when migrations live in `migrations/`.
- **Test placement inconsistency** — the repo has BOTH colocated tests
  (`foo.test.ts` next to `foo.ts`) and a test tree (`tests/`). Pick whichever
  holds the majority and move the minority. Never invent a third convention.
- **Root clutter** — loose scripts, one-off `.py`/`.sh`, scratch files at repo
  root → `scripts/` (or delete if dead; cross-check with the smells dimension).
- **Config sprawl** — configs that tooling does NOT require at root
  (`.eslintrc` must stay; a random `settings.yaml` used by one module should
  live with that module).

## 2. Inconsistent naming

Within one directory, file names must share a casing and suffix convention:

- Mixed casing: `UserCard.tsx` + `nav-bar.tsx` + `footer_component.tsx` in the
  same dir. Detect the dominant style per dir (and per language ecosystem:
  PascalCase for React/Swift components, kebab-case for Svelte/Vue and general
  ts files, snake_case for Python/Rust modules) and rename the outliers.
- Mixed test suffixes: `.test.ts` vs `.spec.ts` — unify to the majority.
- Redundant prefixes that repeat the dir name: `components/ComponentButton.tsx`
  → `components/Button.tsx`.
- Renames are moves: same import-fix mechanics apply (see move mechanics).

## 3. Orphan and junk-drawer directories

- **Orphan dirs** — 0 files (delete), or 1 file with no sibling planned
  (flatten into parent). A dir containing only an `index.ts` that re-exports
  from elsewhere is a dead barrel → inline and delete.
- **Junk drawers** — `utils/`, `helpers/`, `misc/`, `common/` holding >5
  unrelated files. Regroup by what the code is about (`utils/date.ts`,
  `utils/currency.ts` → fine; `utils/stuff.ts` with 12 unrelated exports →
  split by domain, often into the feature dirs that consume them).

## 4. Wrong nesting

- **Single-child chains** — `src/lib/core/internal/engine.ts` where every level
  has exactly one child: collapse to `src/lib/engine.ts` (keep at most one
  grouping level that carries meaning).
- **Flat dumping grounds** — one dir with >15 sibling files at the same level:
  introduce subgroups along the natural seams (per feature, per entity — use
  the import graph: files that import each other heavily belong together).
- **Depth budget** — beyond 4 levels under `src/`, demand justification;
  deep trees hide files and lengthen every import.

## 5. Split / merge folders

- **Split** when one dir mixes domains: `src/api/` containing both HTTP route
  handlers and DB queries → `src/api/` + `src/db/`. Signal: two clusters in the
  import graph with few edges between them.
- **Merge** when two dirs cover one concern: `helpers/` and `utils/`, or
  `types/` and `interfaces/` → one dir, majority name wins.
- **Feature vs layer** — do NOT convert a layer-organised repo to
  feature-organised (or vice versa) unilaterally; that is an architecture
  decision. Flag it, recommend, let the user decide. Everything else in this
  reference is fair game by default.

</detections>

<target_tree>

Before moving anything, produce a **target tree proposal**:

1. Render the current tree and the proposed tree side by side (dirs + moved
   files only, not every unchanged file).
2. Annotate every move/rename/deletion with its detection class.
3. Respect the language's ecosystem conventions:
   - **js/ts**: `src/` root; framework dirs are law (see load-bearing paths)
   - **python**: package dir matches distribution name; keep `tests/` top-level
   - **rust**: `src/` with `main.rs`/`lib.rs`; one module = one file or dir with `mod.rs`
   - **swift**: SwiftPM `Sources/<Target>/`, `Tests/<Target>Tests/`
4. Present via the plan format (`references/plan-format.md`) and get approval.
   Batch moves per subtree so each batch is independently verifiable.

</target_tree>

<load_bearing_paths>

Never move these — location IS the API:

- Framework routing dirs: `pages/`, `app/`, `src/routes/` (Next/SvelteKit/Remix),
  Django app layouts, Rails-style conventions
- Migration dirs (`migrations/`, `alembic/`) — ordering and discovery by path
- `.github/`, `.claude/`, CI config, `Dockerfile` paths referenced by CI
- `public/` / `static/` assets referenced by URL at runtime
- Generated code (check for "do not edit" headers, `*.g.*`, `*_pb2.py`) — fix
  the generator config instead, or leave it
- Entry points named in manifests: `package.json` `main`/`exports`/`bin`,
  `pyproject.toml` `[project.scripts]`, `Cargo.toml` `[[bin]]`, pbxproj refs

When a finding collides with this list, report it as "flagged, not movable".

</load_bearing_paths>

<move_mechanics>

Always `git mv` (preserves history). After each move, fix every reference to
the old path **in the same batch**:

## js / ts

1. `git mv src/old/foo.ts src/new/foo.ts`
2. Fix inbound imports: `grep -rn "from ['\"].*old/foo" src/` → rewrite
   relative paths from each importer's location.
3. Fix the moved file's own relative imports (they broke too).
4. Check alias maps: `tsconfig.json` `paths`, bundler aliases (vite/webpack),
   `package.json` `exports`/`main`/`types`.
5. Update barrel files (`index.ts`) that re-exported the old path.
6. Verify: `tsc --noEmit` (or the project's typecheck script) catches every
   missed import.

## python

1. Module path = import path: moving `pkg/old/foo.py` → `pkg/new/foo.py`
   changes `from pkg.old.foo import X` everywhere.
2. `grep -rn "pkg\.old\.foo\|from pkg\.old import" .` → rewrite; include
   dynamic uses: `importlib`, string references in configs, `patch("pkg.old.foo...")`
   targets in tests.
3. Keep/adjust `__init__.py` in both old and new dirs; delete the old dir only
   when empty.
4. Check `pyproject.toml`/`setup.py`: `packages`, `[project.scripts]`
   entry points, plugin registrations.
5. Verify: run the import smoke test `python -c "import pkg"` plus the test suite.

## rust

1. The module tree is declared, not inferred: after moving a file, update the
   `mod` declaration in the parent (`lib.rs`/`main.rs`/`mod.rs`).
2. Rewrite `use crate::old::foo` paths — `cargo check` lists every break.
3. Dir moves with `mod.rs`: prefer the modern layout (`foo.rs` + `foo/`).
4. Workspace: moving a whole crate needs `[workspace] members` and dependent
   crates' `path = "..."` deps updated.

## swift

1. **SwiftPM**: targets glob their `Sources/<Target>/` dir — moving within a
   target is free; moving across targets changes module imports
   (`import OldTarget`) and `Package.swift` target deps.
2. **Xcode projects**: file paths live in `project.pbxproj`. With
   filesystem-synchronized groups (Xcode 16+), moving on disk is enough;
   otherwise the pbxproj reference must be updated — do it via Xcode or warn
   the user rather than hand-editing blindly.
3. Verify: `xcodebuild build` or `swift build`.

</move_mechanics>

<verify>

Per batch of moves:

1. Build/typecheck (`tsc --noEmit`, `python -c "import pkg"` + `mypy`,
   `cargo check`, `swift build`).
2. Full test suite.
3. Residue grep: search the repo for the old paths/module names — zero hits
   outside CHANGELOG/docs history.
4. Commit the batch: `optimize(structure): move <area> — <reason>`. Moves and
   their import fixes must never be split across commits.

</verify>
