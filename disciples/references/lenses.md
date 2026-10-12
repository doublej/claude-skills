# Lens catalogue

Each `## <name>` block is pasted whole into a disciple's `{{MISSION}}`. The catalogue order is the default order for `/disciples N`.

## design
Lens: visual design. Find the one or two places where the UI looks least finished and fix them.
1. Find the design direction the repo already has, in its CLAUDE.md, design docs, tokens, or existing components. Follow it. Your job is to make the design consistent with its own direction, not to restyle it.
2. Screenshot the running or built UI headless at a desktop size (1440x900) and a phone size (390x844). Save the shots to a scratch folder that git ignores (`.orchestrate/` if it exists, otherwise the system temp dir). Never drive a browser tab the user has open.
3. Pick the weakest spot: misalignment, off-scale spacing, inconsistent components, poor hierarchy, or broken states (hover, focus, empty, error).
4. Fix it, then reshoot at both sizes.
If the repo states no direction, don't use: a cream or off-white background, italic accent words in headings, numbered section labels, monospace labels, pill-shaped buttons. Never invent copy or content the owner didn't write.
Evidence: before and after screenshot paths at both sizes, and one sentence per change naming the rule or component it now matches. If the UI can't be run, say so and pick a static fix you can verify with the check.

## performance
Lens: runtime and load performance, measured.
1. Use the repo's own profiler, benchmark, or perf script if it has one (look in scripts/, the justfile, and package.json). Otherwise measure what fits the stack: bundle size and a headless load trace for web, a timed benchmark for libraries and CLIs.
2. Measure three times before you change anything, and record the median and the spread.
3. Change the single biggest cost you can cut without changing the output.
4. Measure three times again. Keep the change only if the median improves by more than the run-to-run spread. Otherwise discard the uncommitted edit and report the attempt as rejected.
Evidence: a before/after table with the metric, the median, the spread, and the top cost.

## simplify
Lens: less code with the same behaviour.
1. Find the largest files (by any thresholds the repo sets, such as `.quality.json` or a loc-check), dead exports, and logic that duplicates a helper the repo already has.
2. Pick the change that removes the most code: delete dead code, reuse the existing helper, or split a file by responsibility while keeping the architecture. Before you call something dead, run a search that would find an importer if one existed.
3. Update every importer of anything you move or rename.
The existing tests must pass unmodified. Logic that moves keeps a test that would fail if it broke.
Evidence: `git diff --shortstat` for the net lines, and the size of each touched file before and after.

## bugs
Lens: correctness.
1. Open the tracker (`bd ready` if `.beads/` exists, otherwise `gh issue list --label bug` if there is a GitHub remote). Take the highest-priority bug with a concrete symptom, and claim it if the tracker supports claiming.
2. If no bug is open, hunt for one: run the app or CLI and look at its console errors and warnings, failing edge inputs, or unhandled rejections.
3. Find the root cause. Before you edit, search for every caller of the function you're fixing, and put the fix where all of them route through. Add one test that fails without the fix.
4. Close the ticket with a one-line reason.
A bug the owner reported happened on real hardware. If you can't reproduce it, fix the cause the code shows rather than closing it as unreproducible.
Evidence: the test name, failing before the fix and passing after, plus the symptom before and after.

## tests
Lens: missing tests on risky logic.
1. Find logic with branches, parsing, money, or state machines that no test exercises. A filename match isn't proof either way: check imports and integration tests before you call something untested.
2. Add the smallest test that fails if that logic breaks. Use the repo's existing test framework and helpers.
3. If the new test exposes a bug, fix the bug and say so.
Evidence: each test name, the logic it guards, and proof that it fails when the guarded line is broken (break it, run the test, restore it).

## a11y
Lens: accessibility.
1. Run any automated checker the repo has. Otherwise check by hand, headless: keyboard order and focus visibility, accessible names on controls and images, text contrast, and reduced-motion handling.
2. Fix the worst barrier: something a keyboard or screen-reader user can't do at all.
Evidence: the barrier, the element, and how you confirmed the fix (checker output, or the keyboard path you walked).

## security
Lens: security at trust boundaries.
1. Look at input that enters from outside (requests, files, URLs, env), secrets in the repo or the build output, and known-vulnerable dependencies (use the stack's audit command).
2. Fix one confirmed issue: add validation at the boundary, remove an exposed secret from the code (and tell the owner to rotate it), or upgrade the affected dependency.
Report each finding with file:line, the triggering case, confidence, and estimated severity. Keep uncertain findings separate from confirmed ones. Never print a secret's value.
Evidence: the triggering input before and after, or the audit output before and after.

## docs
Lens: instructions that match the code.
1. Compare the CLAUDE.md, AGENTS.md, and README files with the code. Check commands, paths, ports, scripts, and the invariants they state.
2. Fix the drift: correct each wrong line, and delete the ones that describe code that no longer exists. Add only what an agent would otherwise get wrong.
Evidence: each corrected claim, and the command or file:line that proves the new text.

## custom
Lens: {{LENS}}. Decide what this lens means for this repo: name the two or three things you'll judge it by, and the evidence that shows each one improved. Then make the change that improves it most and show that evidence before and after.
