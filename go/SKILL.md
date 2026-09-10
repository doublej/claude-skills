---
name: go
description: Front door for any task. Turns a one-line ask into a grounded brief, provisions the project (atlas new, branch or worktree), applies JJ's standing preferences, picks the execution shape (inline, orchestrate, autonomous run, loop) and closes out with commit, push, deploy and a report. Use on `/go <ask>` or when JJ opens a session with a bare task line.
---

# go

One input: the ask after `/go`. One output: the finished work, shipped, plus a report.

<context>
I'm JJ. Roughly 400 sessions started with a bare task line and I spent the first turns
supplying the same context: which repo, which branch, what "done" means, which budget,
that I'm AFK, commit and push when finished. This skill supplies all of that once so the
ask can stay one line.
</context>

<inputs>
Ask: `$ARGUMENTS`. If empty, the last user message is the ask. A pasted plan or a path to
one is a change with the brief already written: ground it, do not rewrite it.
Resolve the project first: cwd when it is inside a repo; otherwise the project the ask
names, via `atlas search <name>`, and work from that path. Two plausible matches → the
form asks which.
Ground before anything else: `.atlas` (type, `flow` block), `git status -sb`,
`git worktree list`, the project CLAUDE.md, justfile recipes, `atlas info`. Never re-derive
what these already say. The project's CLAUDE.md wins over `references/preferences.md`;
preferences fill gaps only.
</inputs>

<intent>
Classify the ask into one shape. Signals, not rules:
- new project: nothing under cwd is a repo, or the ask names a product/tool/app that does not exist under ~/dev
- change: bug, feature, refactor in an existing repo
- resume: an open feature branch, worktree or plan file already holds this work; continue it
- research: find, review, list, compare, audit, "what do we have"
- visual: screenshot attached, or design, layout, animation, copy tone
- ops: deploy, host, NAS, ubuntu, launchd, onenv
- loop: watch, poll, until, every N
Ambiguous between two shapes → the cheaper one.
</intent>

<gaps>
Ask JJ exactly once, one `consult-user-mcp` form, only for fields that change the work and
that grounding could not fill. Prefill every field from `references/preferences.md`.
Typical fields: family/name for a new project, done-condition, AFK or interactive, deploy
target. AFK response or no MCP → take the prefilled defaults and note them in the report.
</gaps>

<brief>
Load `prompt-crafter`. Target: the owner tier picked in `<execute>`; sonnet for any
bounded piece it hands off.
Upgrade the one-liner into a brief that carries: the reason and audience, the grounded facts
above, the done-condition, the relevant block of `references/preferences.md`, and the
verifier. The brief is what runs. The one-liner is never run as-is.
</brief>

<provision>
- new project → `atlas new <family/name>` (cookiecutter, gitflow, journal come with it), then
  a CLAUDE.md from the template with only the stack, ports and quirks lines filled.
- existing project → follow the repo's own flow. `.atlas` has a `flow` block: branch from
  `develop` with `/feature <slug>`. No `flow` block: branch from trunk, never create
  `develop` as a side effect. Missing `.atlas` → `atlas init`; missing CLAUDE.md → the
  five-line one (stack, ports, quirks, onenv namespace, test command). Nothing else changes
  in the repo's setup.
- dirty tree or another worktree or session active in this repo → do the work in a fresh
  worktree under the repo's worktree dir. Never stash, reset or touch unrelated local
  changes. A dirty tree that is clearly this same task (branch name or files match) is
  the resume shape: continue on it.
- resume → check out the existing branch or worktree, read its last commits and any plan
  or report file, and continue from the first unfinished item.
- research, visual, ops, loop → nothing to provision.
</provision>

<execute>
Pick the owner by uncertainty and cost of error, before size:
- obvious local edit, clear scope, observable acceptance → sonnet.
- normal feature or fix → opus owns it end to end: investigate, implement, test, finish.
- unclear architecture, elusive bug, conflicting requirements, expensive failure mode →
  fable straight away, and it keeps the implementation when that needs sustained
  judgment. Never make a cheaper tier fail first.
Then pick the shape by size, not by habit:
- fits one context and is one dependent chain → the owner does it inline at low effort.
  This is the default and it is the ponytail rung. Raise effort for one hard decision,
  not for the whole run; effort and tier are separate dials.
- many independent pieces → `/orchestrate` with the brief. Delegate only a piece with a
  clear boundary whose result is cheaper to check than to produce; fan-out saves clock,
  not tokens. Anything that writes gets its own worktree.
- stuck → escalate a question, not the task: objective, code, observed failure, what was
  tried, the exact decision needed. Escalate when the next attempt would repeat the same
  hypothesis with no new evidence.
- JJ is AFK or the run will outlast a sitting → prepend `references/pm-contract.md` to the
  brief and hand it to `run-brief`.
- loop shape → `loop-brief`.
- visual → load `design-frontend` with the design block of preferences; `ui-align` for any
  alignment fix; finish by handing back a live URL, never a gif.
</execute>

<closeout>
Verified and finished means: the repo's own gates green (justfile or CLAUDE.md commands,
else the global minimum: tests, typecheck, lint, format), then `/smart-commit`, push the
feature branch, merge per the repo's flow (`develop` when it has one, else trunk), deploy
when the repo has a target (justfile `deploy*`, deploy-nas, or a CLAUDE.md deploy line),
health check, one line of lasting lessons into the project CLAUDE.md. A worktree you
created is removed after its branch is merged. Report to `.orchestrate/report.md` and to the final message, for a reader who saw
none of this: outcome first, what is verified and how, what is open, what needs JJ.
Notify only on a state change, never "still running".
</closeout>

<boundaries>
Proceed on anything reversible. Stop for destructive actions, a real scope change, or a
call that is only JJ's. No gold-plating: nothing the ask did not require. Before reporting
progress, point at the tool result that proves it.
</boundaries>
