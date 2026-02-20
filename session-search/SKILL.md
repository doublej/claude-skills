---
name: session-search
description: "Search and analyse Claude Code session history with multi-project support. Use when (1) User wants to find past conversations about a topic, (2) User asks 'when did I work on X', (3) User wants a summary of what they worked on, (4) User needs to recall or analyse previous sessions. Triggers on 'search history', 'find in sessions', 'when did I', 'what did I work on', 'summarize history', 'analyze session', 'session timeline'."
---

# Session Search & Analyzer

## Initialization

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

---

## Phase 1: INTENT DETECTION

Determine what the user wants based on their request:

**SEARCH** — user provides a search phrase or wants to find specific content:
- Signals: a quoted phrase, "find", "search", "when did I", "recall", "mentions of", "where did I discuss"
- Proceed to **Phase 3a: Search Flow**

**ANALYSE** — user wants a summary or timeline of recent work:
- Signals: "what did I work on", "summarize", "timeline", "analyze history", "recent activity", "review sessions"
- Proceed to **Phase 3b: Analyse Flow**

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

---

## Phase 3a: SEARCH FLOW

### Step 1: Run search

```bash
python3 {SKILL_DIR}/scripts/session_search.py search "<phrase>" [scope flags] -o .session-search -t
```

The script outputs a summary box, timeline, and JSON.

### Step 2: Present results

Show the summary box and timeline from stdout.

### Step 3: Offer review options

- "Show window N" — read `.session-search/context_messages.json`, filter by window timestamps, display chronological conversation
- "Show all matches" — list all matching messages with previews from `search_index.json`
- "Search for something else" — loop back to Phase 1

---

## Phase 3b: ANALYSE FLOW

### Step 1: Scan

```bash
python3 {SKILL_DIR}/scripts/session_search.py scan [scope flags]
```

Present stats. Ask how many recent messages to analyse:

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

### Step 3: Analyse (parallel Haiku workers)

Launch two Haiku subagents in parallel using Task tool with `model: haiku`:

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
| `context_messages.json` | search | Full messages within all time windows |
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
```

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
- Uses `sessions-index.json` for fast multi-project discovery
- Filters by `projectPath` and `fileMtime` before reading session files
- Extracts full conversation context (user + assistant + speak MCP dialogs)
