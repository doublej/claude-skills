---
name: session-catchup
description: Catch up on recent Claude Code sessions in the current project or folder (subprojects included; all projects on request) using session-search, establish where each one left off (checked against git), and produce a ranked plan to finish or continue that work, with a resume command per thread. Use when the user says "catch up", "where did I leave off", "what was I working on", "what's still open", "pick up where we left off", "morning catchup", "plan my unfinished work", or "/session-catchup". Use session-search instead for finding a phrase in history, and handoff for briefing a single new session.
---

# Session Catchup

Turns the last N hours of sessions into threads of work, checks each thread against git, and writes a plan: what to finish, what to continue, what to drop.

<presentation>
Tier: run. Print the banner as plain text before the first tool call, once.

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   SESSION CATCHUP                                            ║
║   Where every recent session left off, and what comes next   ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

Close with this report, one row per thread, ordered as in the plan:

```
SESSION CATCHUP  ──  <scope>   since: <window>   sessions: <n>   threads: <n>

STATE      PROJECT              THREAD                      LAST         NEXT
──────────────────────────────────────────────────────────────────────────────────
FINISH     <project>            <thread>                    <mm-dd hh:mm> <first step>

github.com/doublej
```

States: `FINISH` · `CONTINUE` · `BLOCKED` · `LIVE` · `STALE` · `DONE`. DONE threads go on one summary line under the table, not in rows. The plan path and the first resume command go after the block.
</presentation>

<step_1_scope>
Defaults: the folder the session runs in (cwd, every project below it included) and the last 48 hours. Map the request onto flags:

| User says | Flags |
|-----------|-------|
| nothing | none: the script scopes to cwd and 2880 minutes |
| "today" / "last 8 hours" / "this week" | `--since 1440` / `--since 480` / `--since 10080` |
| "in web projects" / "only this repo, not subfolders" | `--folder ~/dev/web` / `-p $(pwd)` |
| "everywhere" / "all projects" | `--all-projects` |

Always exclude the running session: its id is the session-directory name in the scratchpad path.
</step_1_scope>

<step_2_digest>
```bash
python3 ~/.claude/skills/session-catchup/scripts/catchup_digest.py --exclude <this-session-id> [scope flags]
```

The script reuses session-search's discovery, parsing and noise filter. It drops `claude -p` one-shots (fewer than 2 real prompts; `--min-user-msgs` changes that) and writes `~/dev/_data/session-catchup/catchup.json`:

- `projects{path: {branch, dirty_files, unpushed, last_commit} | null}`. `unpushed: null` means no upstream, and `null` instead of the object means the path is not a git repo.
- `sessions[]` holds `{session_id, project (realpath), cwd, first, last, age_min, user_messages, ended_on, goal, tail[], resume}`. `ended_on: "user"` means the last prompt never got a text reply (interrupted, crashed or still running).

Stdout is one row per session. Show it as-is. Do not load `catchup.json` into the main context when it holds more than 6 sessions; step 3 delegates it.
</step_2_digest>

<step_3_investigate>
Group sessions by `project`. Spawn investigators with the Agent tool, `model: "opus"`, all in one message: one per project, merging small projects (1–2 sessions) into shared agents so there are at most 8 agents. With 6 sessions or fewer in total, do this step inline instead.

Investigator prompt (fill in the placeholders):

```
Load your sessions (git state per project is in the same file under "projects"):
jq --argjson p '[<paths as JSON strings>]' '[.sessions[] | select(.project as $x | $p | index($x))]' ~/dev/_data/session-catchup/catchup.json
For each, the "goal" is the first prompt and "tail" is the last messages, which show where it stopped.
Ground every claim in the repo, not in what the assistant said:
- the project's git state is in catchup.json "projects"; also run `git log --oneline -10` and `git status --short` there
- if the tail names another repo or path (work often lands outside the cwd), check that repo the same way
- if the repo has .beads/, run `bd list --status open` and link tickets the sessions mention
Mark anything you couldn't confirm, and say where you looked.
Merge sessions that worked on the same thing into one thread. Per thread return JSON:
{"thread": "<5-word name>", "project": "<path>", "sessions": ["<id>"], "last": "<iso>",
 "state": "DONE|FINISH|CONTINUE|BLOCKED|LIVE|STALE",
 "evidence": "<commit sha / dirty files / ticket that proves the state>",
 "left_off": "<one sentence>", "next_step": "<first concrete action>",
 "effort": "<minutes>", "resume": "<resume command of the latest session>"}
States: DONE = landed and verified, nothing left. FINISH = one short step left (commit, push, verify, deploy).
CONTINUE = multi-step work in progress. BLOCKED = waiting on JJ's decision or an external party; name it.
LIVE = age_min < 15, or ended_on "user" with age_min < 60. It may still be running, so do not plan over it.
STALE = abandoned or superseded by a later session/commit.
Return only the JSON list. Read-only: do not commit, push or edit anything.
```
</step_3_investigate>

<step_4_plan>
Merge the threads, collapsing duplicates across agents. When a subagent reports back, check its evidence before you accept it: `git -C <project> cat-file -e <sha>` for each sha cited on a DONE or FINISH thread. A thread whose sha does not resolve goes back to CONTINUE. Order the threads:

1. **FINISH**: cheapest first. Uncommitted or unpushed work is at risk, so it leads.
2. **BLOCKED**: list the exact question JJ has to answer.
3. **CONTINUE**: by recency, each with its first concrete step.
4. **LIVE / STALE**: one line each; STALE threads get a suggestion to drop or archive them.

Write the plan to `~/dev/_data/session-catchup/plan-<yyyy-mm-dd-hhmm>.md`. Each thread section holds the state, the evidence, where it left off, numbered next steps, an effort estimate and the `resume` command. Then print the report from `<presentation>`.

Done means the plan file exists and the report is printed. Stop there, because JJ picks the thread. If the digest exits with `No projects found for scope` or reports 0 sessions, print the report with that one line under the table and stop.
</step_4_plan>

<rules>
- Read-only. Do not commit, push, edit or close tickets in the investigated repos. The plan says what to do, and JJ chooses.
- A session's own "done" is a claim. A thread is DONE only with a commit or a verified artifact as evidence.
- `resume` keeps the original `cwd`, even a `~/Documents/development/...` one. Sessions are stored under the directory they started in, so the resumed session gets back its own history and folder.
- Sessions with cwd `~/dev` (no git) did their work in a subrepo. Find it from the tail.
- If an investigator returns nothing, report that project as a row with `✗` in STATE and the cause in NEXT. Do not leave it out.
</rules>

<self_check>
`python3 ~/.claude/skills/session-catchup/scripts/test_catchup_digest.py` prints `ok`.
</self_check>
