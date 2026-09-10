# JJ's standing preferences (mined from 6,425 messages, 2026-07-18 → 2026-09-08)

The skill injects only the block that matches the intent. Counts are how often JJ had to
say it by hand; they justify the line, not the wording.

## process (always)
- Finished and verified work is committed and pushed without asking; deployed when the repo has a target. (~45)
- Do not pause between repos, items or phases; report once at the end. (~25 "stop asking, proceed")
- Route by uncertainty and cost of error: sonnet for bounded, clearly specified work; opus owns a normal feature or fix end to end; fable at once for unclear architecture, subtle bugs or costly mistakes. Never make a cheaper tier fail first. Name the tier in every brief. (~19)
- Worker briefs open with VERIFIED CONTEXT, do not re-derive. Workers commit with explicit paths, never push. (~15)
- Never `git add -A`. Never edit the main checkout while worktrees are active. Never delete branches; rename to `closed-*`. (~15)
- Nothing is done until a tool result says so; a "done" claim without proof is the worst outcome. (~38 refutations)
- Reports: outcome first, plain sentences, no arrow chains, terse. Paths bundled at the bottom.

## design (visual intent)
- Approach it as the design lead at a small studio known for versatility, not as a template. (24)
- No em dashes in any generated copy. (~10)
- No border radius, grayscale before color, no Arial, no "cute" themed palettes. (~20)
- One shared component with variants, never near-duplicate components. (~13)
- Alignment is measured, not eyeballed; use `ui-align` on a live page. (4)
- Numeric tuning goes through consult-user-mcp `tweak`, not screenshot round-trips. (357 tuning msgs)
- Finished UI is demoed with a live dev URL, never a gif.

## new project
- `atlas new <family/name>`; gitflow (`feature/*` → `develop` → `main`), annotated tags, no release branches.
- JS/TS: bun. Python: uv. Svelte or FastAPI when the family already uses them.
- Secrets via onenv only; CLAUDE.md names the exact onenv namespace.
- CLAUDE.md carries stack, ports and quirks only. No README padding.

## existing project
- The repo's CLAUDE.md, justfile and package manager win over anything in this file.
- Flow is read from `.atlas`, never assumed. Repos without a `flow` block stay single-line trunk repos. (dev-root rule)
- Parallel work goes in worktrees; the main checkout is never edited while worktrees are active. Cross-session file collisions were a top-6 friction.
- Unrelated local changes are left alone. No stash, no reset, no drive-by refactor.
- Branches are merged, never deleted; a finished branch is renamed `closed-*` if it must go.
- A worktree created for one task is removed once merged; `worktree-orphanage` handles the rest.

## ops
- Remote work goes through `workremotely`; adb through the rig, never local.
- Deploy scripts end with commit SHA, target and a health check, unprompted. (~16 "did it land")
- Default to the non-destructive mode when a sync or write mode is ambiguous.

## autonomous runs
- Budget unless given: 12 haiku, 6 sonnet, 2 opus. Exhausted → stop, report, list what is left.
- Done-condition stated in the first message and held to.
- Fresh-eyes verifier after every merge and when real risk remains outside the checks that ran; it hunts defects, not improvements (Fable only; Opus self-verifies).
- Lessons that outlive the run: one line in the nearest CLAUDE.md, no new docs.
