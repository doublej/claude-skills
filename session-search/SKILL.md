---
name: session-search
description: "Search and analyze past Claude Code session history across projects"
---

<initialization>

Display boot sequence:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   SESSION SEARCH v3.0                                        ║
║   History Search & Analysis Engine                           ║
║   github.com/doublej                                         ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   [LOAD] Multi-project session scanner                       ║
║   [LOAD] Exact phrase search engine                          ║
║   [LOAD] Time window builder                                 ║
║   [LOAD] Timeline generator                                  ║
║   [LOAD] Workflow analysis pool                              ║
║                                                              ║
║   System ready.                                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

</initialization>

<phase_intent>

Determine what the user wants based on their request:

**SEARCH** — user provides a search phrase or wants to find specific content:
- Signals: a quoted phrase, "find", "search", "when did I", "recall", "mentions of", "where did I discuss"
- Proceed to **Phase 3a: Search Flow**

**ANALYSE** — user wants a summary or timeline of recent work:
- Signals: "what did I work on", "summarize", "timeline", "analyze history", "recent activity", "review sessions"
- Proceed to **Phase 3b: Analyse Flow**

**INVESTIGATE** — user wants the *state* of work, not a communication summary:
- Signals: "unfinished work", "what's left", "what still needs to happen", "status of", "where did I leave off", auditing sessions that "weren't finished"
- This is a sub-intent of ANALYSE — use **Phase 3b** but follow the **INVESTIGATE path** (Step 3): produce per-session `{goal, accomplishments, unfinished, next_steps}` grounded in git state, not message categories. Skip the Worker A/B/C categoriser pipeline.

**AMBIGUOUS** — intent is unclear:
- Ask via `ask_multiple_choice`:
  - "Search for a specific phrase"
  - "Summarise recent activity"
- If the user cancels or does not respond, default to the **ANALYSE flow** on the current project.

---

## Phase 2: SCOPE DETECTION

Parse scope from the user's request. Apply these rules:

| User says | Flag |
|-----------|------|
| "in all projects" / "across projects" / "everywhere" | `--all-projects` |
| "in web projects" / "under ~/dev/web" / "in the X folder" | `--folder <path>` |
| "in the last 30 minutes" / "past hour" / "today" | `--since <minutes>` |
| "last 50 messages" | `-n 50` |
| Nothing specified | Default: current project only (`-p <cwd>`) |

**Time conversion:** "past hour" = `--since 60`, "today" = `--since 1440`, "this week" = `--since 10080`

**`--folder` takes a real filesystem path**, not the encoded project directory name. When the user names a group of projects ("the simsync projects", "these projects"), pass the real path prefix:
- "in the simsync projects" → `--folder ~/Documents/development/multi-stack/simsync`
- "in this folder" → `--folder $(pwd)`

Never `ls`/`grep ~/.claude/projects/` by project name — directory names are URL-encoded (`-Users-jurrejan-...`, with `/` and `_` both collapsed to `-`) and will not match a plain name.

---

## Phase 3a: SEARCH FLOW

### Step 1: Run search

```bash
python3 {SKILL_DIR}/scripts/session_search.py search "<phrase>" [scope flags] -o .session-search -t
```

The script outputs a summary box, timeline, and JSON.

**Phrases starting with `--`** (e.g. `--allow-live`) are parsed as flags no matter how they are quoted. Put scope flags first and end the flag list with a bare `--`: `search -p <path> -o .session-search -- "--allow-live" "--only"`.

**Zero matches on a phrase you are sure exists?** Search covers message text *and* `tool_use` bodies (Write content, Bash commands, Edit strings) — a match found there is tagged `matched_in: "tool_use"` and its preview is prefixed `[tool_use]`. Two blind spots remain:
- **Full tool bodies are not in `context_messages.json`** (they would balloon it). To read the surrounding body, `grep -rl "<phrase>" ~/.claude/projects/` and read that JSONL line directly.
- **Subagent transcripts are not scanned.** Messages the user types straight into a spawned agent live in `~/.claude/projects/<encoded>/<session_id>/subagents/agent-a<name>-*.jsonl`, not the main session file. When the user asks for requests "to" or "with" a named agent, grep those files directly.

### Step 2: Present results

Show the summary box and timeline from stdout. **Never truncate or parse that stream.** It is a summary box, then per-project timelines, then a JSON blob: `tail` drops the box, `head -N` cuts off the later projects' timelines, and a JSON parser chokes on the leading text. Whenever you need the full match list or just a match count, run the search with stdout discarded and read `search_index.json`.

**If matches exceed ~50–100**, the per-window browsing flow below is impractical. Instead: re-run `search` with a more specific phrase, add `--since`/`--folder` scope to narrow, or switch to the **ANALYSE flow** (extract + categorise) for a thematic summary.

**Synonymous phrases: one `--any` run, never parallel processes.** `search "phrase one" "phrase two" --any` matches any of the phrases in a single corpus pass. Do NOT launch multiple concurrent `search` processes for synonyms — each process re-reads the entire session corpus (multi-GB), and parallel copies multiply I/O and CPU until the machine crawls.

**Broad-term guard:** when total matches exceed `--context-limit` (default 500), the script automatically skips context extraction and the timeline — counts, windows, and match previews in `search_index.json` stay complete, and stdout prints a notice. This is the signal the query is too broad: narrow it rather than overriding. `--context-limit 0` forces full extraction when the user explicitly wants everything (can write very large files).

Then proactively surface the top matches by reading `search_index.json` — each `projects[*].matches[]` entry has `{timestamp, type, session_id, preview}`. Show the top ~10 (timestamp, role, preview) so the user sees content, not just window boundaries.

**Steps 2–3 exist so a human can pick a window — skip them when nobody is picking.** Go straight to reading and filtering `context_messages.json` (across every output dir) when any of these hold; this is the documented path, not a deviation:
- **Autonomous / research context** — you are investigating on the user's behalf and will report a conclusion, not a menu of windows.
- **Few matches (≤ ~15)** — the timeline already shows every window; a surfacing pass adds latency and nothing else.
- **Synthesis wanted** — research-style phrasing, no single quoted term, several parallel searches to merge, or > ~100 matches across many sessions.

**Very large context (> ~2000 messages): delegate, do not load inline.** The output files persist on disk — hand a subagent the *absolute* paths to `context_messages.json` and `search_index.json` with a targeted synthesis prompt, and keep the raw messages out of your own context.

**Filter noise matches first.** These are user-turn messages in the JSONL but not things a human typed, and common terms (design words like "serif", flag names) hit them heavily via injected system prompts and agent payloads. Skip any match whose `preview` starts with:

`Base directory for this skill:` · `<task-notification` · `<agent-message` · `<system-reminder>` · `<local-command-stdout>` · `<command-message>` · `<command-name>/` · `Stop hook feedback:` · `This session is being continued from` · `Caveat: The messages below were generated`

Apply it in the snippet itself, not just by eye — the filter is what gets forgotten when you write an ad-hoc surfacing pass:

```python
NOISE = ("Base directory for this skill:", "<task-notification", "<agent-message",
         "<system-reminder>", "<local-command-stdout>", "<command-message>",
         "<command-name>/", "Stop hook feedback:", "This session is being continued from")
real = [m for m in ms if not m["preview"].startswith(NOISE)]
```

The same list is the filter to apply when bulk-extracting human-typed messages from `context_messages.json` (`type == "user"`) for pattern distillation — do not rediscover it by trial and error. `is_system_noise()` in `session_search.py` holds the canonical list and already applies it to `scan`/`extract`; `search` results are deliberately unfiltered so nothing is hidden.

**Also filter the current session.** Matches whose `session_id` is this live session are the skill's own SKILL.md text, indexed as it loaded. Get the current `session_id` from the session-directory name in your scratchpad path (`.../<project>/<session_id>/scratchpad`); failing that, treat any match whose window overlaps the last few minutes as a candidate.

**If filtering leaves nothing, widen before reporting zero.** All-hits-are-current-session means the single-project scope missed the real history. Re-run with `--folder <parent of cwd>` automatically, and say in the summary that the scope was widened.

### Step 3: Offer review options

- "Show window N" — read `.session-search/context_messages.json`, filter by window timestamps, display chronological conversation
- "Show all matches" — list all matching messages with previews from `search_index.json`
- "Search for something else" — loop back to Phase 1

**`context_messages.json` schema** (so you can filter directly without probing the structure): a flat JSON list of message objects, each with `timestamp` (ISO string), `type` (`"user"`/`"assistant"`), `content` (full text — this is the message body, not `text`/`preview`), `session_id`, and `project`. To show window N, filter by `start`/`end` from that window in `search_index.json` and compare each message's `timestamp`. This is also the path for programmatic/autonomous use — read and filter the JSON directly rather than re-deriving the schema.

---

## Phase 3b: ANALYSE FLOW

### Step 1: Scan

```bash
python3 {SKILL_DIR}/scripts/session_search.py scan [scope flags]
```

`scan` stdout is mixed the same way: human-readable boxes first, then the JSON. Do not `tail` it, and do not feed it to a JSON parser. `scan` accepts `-o` but writes no file, so to consume it programmatically redirect stdout to a file and slice from the first `[`. Guard for nulls — `oldest`/`newest` are `null` for projects with no messages, and an unguarded sort on them raises `TypeError`.

**If the question needs data this skill does not hold** — correlating history with a project database, `git log`, a ticket store — use `scan` for the session-side baseline and then stop: the correlation is out of scope, so handle it with ad-hoc tooling rather than forcing it through the extract → analyse → present pipeline.

Present stats. **If the scoped user-message count is ≤ ~300**, skip the size prompt and extract all automatically — the token cost is small and the choice adds friction. Only ask when the count is large enough that token cost matters:

```
How many recent messages would you like to analyze?
- 25 messages (~8K tokens)
- 50 messages (~16K tokens)
- All <N> messages (~<X>K tokens)
```

### Step 2: Extract

```bash
python3 {SKILL_DIR}/scripts/session_search.py extract -n <limit> [scope flags] -o .session-search
```

Report extraction stats. If `--since` was used, `user_messages.json` will contain messages older than the window (see Technical Reference) — filter it by message `timestamp` before synthesising, and report the filtered count.

### Step 3: Analyse

**Pick a path before spawning workers:**

- **Direct synthesis (default for ≤ ~300 messages):** the extracted messages already fit in context. Read `.session-search/user_messages.json` directly and synthesise the summary inline — skip the Haiku worker chain entirely. Supplement freely from `bd list` (open tickets) and recent `git log`. This is faster and richer than the multi-agent flow for small corpora.
- **INVESTIGATE path (unfinished-work / status queries):** read the extracted messages inline, then cross-reference ground truth from git: `git status`, unpushed commits (`git log @{u}..`), uncommitted diffs, and the last `TodoWrite` state visible in the transcript. Produce per-session `{goal, accomplishments, unfinished, next_steps}` records. Do not run the message-categoriser pipeline — it answers "what was discussed", not "what is left".
  - **GIT SAFETY sub-case — skip the session pipeline entirely.** "did anything get lost", "conflicts", "verify nothing was lost", "git sweep": the answer lives in git, not in the transcripts, and per-session `{goal, unfinished}` records would not address it at any session count. Go straight to forensics: `git reflog` for resets/reverts, `git fsck --lost-found` for dangling commits, then a content-presence check of each dangling commit against `HEAD`.
  - **Known topic list → targeted searches instead.** When the scope is a fixed set of topics, branches or worktree names, one `search` per name (then read `search_index.json` / `context_messages.json`) is a valid and much faster substitute for `scan` → `extract`. Reserve the full pipeline for open-ended scopes where you do not yet know what to look for.
  - **Many sessions (> ~10):** fan out one investigator per session via the bundled workflow instead of reading everything inline:
    ```
    Workflow tool:
      scriptPath: ~/.claude/skills/session-search/scripts/investigate_workflow.js
      args: {"outputDir": "<abs path to .session-search>", "sessionIds": ["<id>", ...], "projectDir": "<abs repo path>"}
    ```
    Collect the distinct `session_id` values from `user_messages.json` first. The workflow returns `{sessions: [{session_id, goal, accomplishments, unfinished, next_steps}], dropped}` — present it directly; if `dropped > 0`, say which sessions failed rather than implying full coverage.
  - **"This session" / "current session" scopes to one session_id, not a time window.** `--since` merges every session touched in that window on a project — for a multi-session project that pulls in unrelated sessions. When the user means the active session, filter `user_messages.json` by the current `session_id` (it is the session-directory name in the scratchpad path) rather than relying on `--since`: `python3 -c "import json;print([m for m in json.load(open('.session-search/user_messages.json')) if m['session_id']=='<id>'])"`.
- **Workflow pipeline (large corpora, > ~300–500 messages):** when the message volume risks context overflow, run the bundled analysis workflow below.

**Override:** the path above is a size-based *default*. If the user explicitly asks for the multi-agent pipeline (mentions "haiku agents", "workers", "full pipeline", "workflow"), run it regardless of corpus size — it stays valid for small corpora when the user chose it deliberately. Honour the request instead of contradicting an earlier size-based decision.

**Workflow pipeline** — one Workflow call replaces the old Worker A/B/C Task-tool chain (no file polling, no manual synchronisation):

```
Workflow tool:
  scriptPath: ~/.claude/skills/session-search/scripts/analyse_workflow.js
  args: {"outputDir": "<abs path to .session-search>", "messageCount": <N from extract>, "projectName": "<name>", "chunkSize": 150}
```

- `outputDir` must be **absolute** — workflow agents may not share this cwd.
- `messageCount` is the extracted-message count reported by `extract`; the script chunks it (~150/chunk), fans out one Haiku categorizer per chunk plus one context resolver concurrently, then a synthesis agent merges everything into `timeline_summary.md`.
- The workflow runs in the background; wait for its completion notification. It returns `{summary, categorizedFiles, resolvedContext}` — `summary` is the path to `timeline_summary.md`.
- If the result looks empty or wrong, Read `journal.jsonl` in the workflow's transcript directory before re-running.

### Step 4: Present

Read and display `.session-search/timeline_summary.md`.

---

## Output Files

All output goes to `.session-search/` (configurable via `-o`):

| File | Subcommand | Content |
|------|------------|---------|
| `search_index.json` | search | Top-level `{query, total_matches, total_windows, total_context_messages, context_skipped, project_count, projects[]}`; each `projects[]` entry is `{project, query, match_count, window_count, context_messages, windows[], matches[]}` (the project path key is `project`, **not** `name`), and each `matches[]` entry is `{timestamp, type, session_id, matched_in, preview}` where `matched_in` is `"message"` or `"tool_use"`. `total_matches` is an int (0 when none) — read it directly, no need to parse the stdout box. `context_skipped: true` means the broad-term guard fired: `context_messages.json` is empty and the timeline was skipped (previews/windows here are still complete). Stdout JSON caps windows at 20/project (`windows_omitted` gives the rest) — the full list is always in this file |
| `context_messages.json` | search | Full messages within all time windows. Each entry: `{timestamp, type, content, session_id, project}` — message body is in `content` (not `text`/`preview`) |
| `timeline.txt` | search | ASCII timeline visualisation |
| `message_index.json` | extract | Message references (uuid, source file/line) |
| `user_messages.json` | extract | Flat JSON list of user messages, each `{type, uuid, timestamp, content, session_id}` — message body is in `content` (not `text`); no `project` field (single-project per file) |
| `categorized_<i>.json` | analyse workflow | Haiku-categorised messages, one file per chunk |
| `resolved_context.json` | analyse workflow | Haiku-resolved context |
| `timeline_summary.md` | analyse workflow | Final analysis report |

---

## Technical Reference

**Script:** `{SKILL_DIR}/scripts/session_search.py`

**Workflow scripts** (invoked via the Workflow tool with `scriptPath`, never executed directly):
| Script | Args | Purpose |
|--------|------|---------|
| `scripts/analyse_workflow.js` | `{outputDir, messageCount, projectName, chunkSize?}` | Chunked Haiku categorization + context resolution → `timeline_summary.md` |
| `scripts/investigate_workflow.js` | `{outputDir, sessionIds[], projectDir}` | Per-session state records grounded in git |

**Subcommands:**
```
session_search.py search <query> [scope] [search flags]
session_search.py scan [scope]
session_search.py extract [scope] [-n limit]
session_search.py list [scope]
```

`list` enumerates each session file with its first/last timestamp, sorted chronologically — use it to locate sessions surrounding a search result (e.g. "was there a session between Jun 1 and Jun 15") when `context_messages.json` does not hold the answer.

**Scope flags (all subcommands):**
| Flag | Purpose |
|------|---------|
| `-p, --project PATH` | Single project (default: cwd) |
| `--all-projects` | All projects under `~/.claude/projects/` |
| `--folder PATH` | Projects whose projectPath starts with PATH |
| `--since MINUTES` | Sessions whose **file mtime** falls in the past N minutes |
| `-o, --output DIR` | Output directory (default: `.session-search`) |

**Search flags:**
| Flag | Purpose |
|------|---------|
| `-m, --margin N` | Context margin minutes (default: 5) |
| `-g, --gap N` | Merge gap minutes (default: 10) |
| `-t, --timeline` | Generate ASCII timeline |
| `--any` | Each query argument is an alternative phrase (OR, single corpus pass) |
| `--context-limit N` | Skip context/timeline when matches exceed N (default 500; 0 = no limit) |

**Extract flags:**
| Flag | Purpose |
|------|---------|
| `-n, --limit N` | Message count limit (default: 100) |

**`--since` filters by session file mtime, not by message timestamp.** A long-running session touched inside the window drags its *entire* history in, so `extract --since 120` can return messages days older than two hours. When the user asked for a real time window, filter `user_messages.json` by each message's own `timestamp` after extracting, and report the filtered count.

**Data source:** `~/.claude/projects/<encoded-path>/<uuid>.jsonl`
- Uses each project's `sessions-index.json` as a *fast path only*; index entries whose `fullPath` has gone stale are backfilled from a direct `*.jsonl` scan of the project dir, so neither a missing nor a stale index can hide sessions
- Filters by `projectPath` and `fileMtime` before reading session files
- Extracts full conversation context (user + assistant + speak MCP dialogs), plus `tool_use` inputs for `search` only
- **Not covered:** subagent transcripts under `<session_id>/subagents/agent-*.jsonl` and top-level `agent-*.jsonl` — grep those directly (see Phase 3a Step 1)

**Troubleshooting — a scope returns 0:** the script depends on no index at any level. If a scope genuinely yields nothing it prints `Error: No projects found for scope` and exits non-zero. Verify the `--folder` argument is a real filesystem path prefix (see Phase 2), or widen the scope. If one project inside a `--folder` scan shows 0 sessions while its project dir clearly holds `*.jsonl` files, re-run that path alone with `extract -p <path>` and report the discrepancy — the on-disk fallback should make this impossible.

</phase_intent>
