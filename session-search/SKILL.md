---
name: session-search
description: "Search and analyze past Claude Code session history across projects"
---

<initialization>

Display boot sequence:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   SESSION SEARCH v2.0                                        ║
║   History Search & Analysis Engine                           ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   [LOAD] Multi-project session scanner                       ║
║   [LOAD] Exact phrase search engine                          ║
║   [LOAD] Time window builder                                 ║
║   [LOAD] Timeline generator                                  ║
║   [LOAD] Haiku analysis pool                                 ║
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

### Step 2: Present results

Show the summary box and timeline from stdout. The summary box is printed **first** — do not pipe stdout through `tail`, or you will lose it.

**If matches exceed ~50–100**, the per-window browsing flow below is impractical. Instead: re-run `search` with a more specific phrase, add `--since`/`--folder` scope to narrow, run several targeted searches in parallel for synonymous phrases, or switch to the **ANALYSE flow** (extract + categorise) for a thematic summary.

Then proactively surface the top matches by reading `search_index.json` — each `projects[*].matches[]` entry has `{timestamp, type, session_id, preview}`. Show the top ~10 (timestamp, role, preview) so the user sees content, not just window boundaries.

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

Report extraction stats.

### Step 3: Analyse

**Pick a path before spawning workers:**

- **Direct synthesis (default for ≤ ~300 messages):** the extracted messages already fit in context. Read `.session-search/user_messages.json` directly and synthesise the summary inline — skip the Haiku worker chain entirely. Supplement freely from `bd list` (open tickets) and recent `git log`. This is faster and richer than the multi-agent flow for small corpora.
- **INVESTIGATE path (unfinished-work / status queries):** read the extracted messages inline, then cross-reference ground truth from git: `git status`, unpushed commits (`git log @{u}..`), uncommitted diffs, and the last `TodoWrite` state visible in the transcript. Produce per-session `{goal, accomplishments, unfinished, next_steps}` records. Do not run the message-categoriser pipeline — it answers "what was discussed", not "what is left".
- **Multi-agent pipeline (large corpora, > ~300–500 messages):** when the message volume risks context overflow, fan out to the Haiku workers below.

**Multi-agent pipeline — launch two Haiku subagents in parallel** using Task tool with `model: haiku`:

```
[ANALYZE] Spawning Worker A: Message Categorizer
[ANALYZE] Spawning Worker B: Context Resolver
```

**Worker A — Message Categorizer:**
Read `.session-search/user_messages.json` (or per-project subdirectories if multi-project). Categorize each message:
- TASK: Direct work requests ("create", "build", "fix", "add")
- QUESTION: Information queries ("how", "what", "where", "why")
- CORRECTION: Fixes/adjustments ("no", "wrong", "instead", "actually")
- FEEDBACK: Reactions ("good", "thanks", "perfect", interrupts)
- META: Commands, model switches, configuration

Write `.session-search/categorized_messages.json`:
`[{timestamp, project, category, original, one_line_summary}]`

**Worker B — Context Resolver:**
Read `.session-search/user_messages.json`. For messages with unresolved references ("that", "it", "the thing", "this", "above"), infer what they refer to based on timestamp proximity and project context.

Write `.session-search/resolved_context.json`:
`[{uuid, timestamp, original, inferred_context, clarified_prompt}]`

### Step 4: Synthesise

Launch one Haiku subagent:

**Worker C — Timeline Synthesiser:**
Read `.session-search/categorized_messages.json` and `.session-search/resolved_context.json`.

Write `.session-search/timeline_summary.md`:

```markdown
# Project Timeline: <project_name>
Period: <start_date> to <end_date>
Messages analyzed: <N>

## Executive Summary
2-3 sentences: main themes, accomplishments, patterns.

## Chronological Timeline
| Date | Original | Clarified | Category |
|------|----------|-----------|----------|
Key requests with clarified versions.

## Communication Patterns
- Common request types
- Prompting style observations
- Areas where context was often missing

## Suggested Prompt Improvements
Rewritten versions of ambiguous prompts.
```

### Step 5: Present

Read and display `.session-search/timeline_summary.md`.

---

## Output Files

All output goes to `.session-search/` (configurable via `-o`):

| File | Subcommand | Content |
|------|------------|---------|
| `search_index.json` | search | Match metadata, window definitions, per-project |
| `context_messages.json` | search | Full messages within all time windows. Each entry: `{timestamp, type, content, session_id, project}` — message body is in `content` (not `text`/`preview`) |
| `timeline.txt` | search | ASCII timeline visualisation |
| `message_index.json` | extract | Message references (uuid, source file/line) |
| `user_messages.json` | extract | Full user message content |
| `categorized_messages.json` | analyse | Haiku-categorised messages |
| `resolved_context.json` | analyse | Haiku-resolved context |
| `timeline_summary.md` | analyse | Final analysis report |

---

## Technical Reference

**Script:** `{SKILL_DIR}/scripts/session_search.py`

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
| `--since MINUTES` | Sessions modified in past N minutes |
| `-o, --output DIR` | Output directory (default: `.session-search`) |

**Search flags:**
| Flag | Purpose |
|------|---------|
| `-m, --margin N` | Context margin minutes (default: 5) |
| `-g, --gap N` | Merge gap minutes (default: 10) |
| `-t, --timeline` | Generate ASCII timeline |

**Extract flags:**
| Flag | Purpose |
|------|---------|
| `-n, --limit N` | Message count limit (default: 100) |

**Data source:** `~/.claude/projects/<encoded-path>/<uuid>.jsonl`
- Uses each project's `sessions-index.json` for fast discovery **when present**; project dirs without an index fall back to a direct `*.jsonl` scan (deriving the real path from each session's `cwd`), so a missing index never silently hides a project
- Filters by `projectPath` and `fileMtime` before reading session files
- Extracts full conversation context (user + assistant + speak MCP dialogs)

**Troubleshooting — `--all-projects`/`--folder` returns 0:** the script no longer depends on a top-level `sessions-index.json`. If a scope genuinely yields nothing the script prints `Error: No projects found for scope` and exits non-zero. Verify the `--folder` argument is a real filesystem path prefix (see Phase 2), or widen the scope.

</phase_intent>
