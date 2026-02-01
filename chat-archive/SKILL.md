---
name: chat-archive
description: "Search through exported ChatGPT and Claude.ai conversations using SQLite FTS5. Use when user wants to search chat history exports, import conversation archives, find past discussions, or query across AI conversation platforms."
---

# Chat Archive

Search exported ChatGPT and Claude.ai conversations via SQLite full-text search.

## Initialization

```
╔══════════════════════════════════════════════╗
║  CHAT ARCHIVE v1.0                           ║
║  Conversation Search Engine (SQLite FTS5)    ║
╚══════════════════════════════════════════════╝
```

DB location: `~/.chat-archive/conversations.db`

## Context Budget Rules

**NEVER** let raw script JSON reach the main agent context. All script execution goes through haiku subagents that return **concise formatted summaries only**.

Delegate to **haiku** subagents (`Task` tool, `model: "haiku"`) for:
- Running scripts and returning formatted markdown (not raw JSON)
- Displaying search results and conversation messages
- Stats checks

Subagent output caps — instruct each subagent to:
- Return **max 80 lines** of formatted text
- Truncate or summarize if output would exceed that
- Include metadata (total count, showing N of M, truncated notice) so main agent can offer pagination

The main agent handles: query intent, refinement decisions, user interaction, and deciding what to fetch next.

## Phase 1: STATUS

Delegate to a **haiku** subagent:

> Run `python3 {SKILL_DIR}/scripts/search_conversations.py --stats --db ~/.chat-archive/conversations.db`.
> Return the stats summary. If DB not found, say so.

If DB doesn't exist or is empty, go to Phase 2 (IMPORT).
If DB has data, show stats and ask user what they want to do: import more, or search.

## Phase 2: IMPORT

Ask user for the export file path using `consult-user-mcp` text input:
- "Path to your ChatGPT or Claude.ai export JSON file:"

Run import:

```bash
python3 {SKILL_DIR}/scripts/import_conversations.py <file_path> --db ~/.chat-archive/conversations.db
```

Platform is auto-detected from JSON structure. Override with `--platform chatgpt|claude` if needed.

Output is JSON with `imported`, `skipped`, `total_conversations`, `total_messages`.
Report results to user, then offer to search or import more.

## Phase 3: SEARCH

Ask user for search query via `consult-user-mcp`. Optional filters:
- `--platform chatgpt|claude` — filter by platform
- `--after YYYY-MM-DD` / `--before YYYY-MM-DD` — date range
- `--title <text>` — filter by conversation title
- `--limit N` — max results (default 20)
- `--no-group` — flat per-message results instead of conversation grouping

**NOTE:** Results are limited to 20 by default. Always inform the user that a limit is active and offer to increase it with `--limit` if they need more results.

### Query syntax (FTS5)

- `"exact phrase"` — match exact sequence of words
- `prefix*` — match words starting with prefix
- `term1 NEAR/5 term2` — terms within 5 words of each other
- `term1 OR term2` — match either term
- `term1 NOT term2` — exclude term2

Delegate search + result formatting to a **haiku** subagent:

> Run `python3 {SKILL_DIR}/scripts/search_conversations.py "<query>" --db ~/.chat-archive/conversations.db [filters]`.
> Parse the JSON output and format as **concise** markdown:
> - For each conversation group: one line with **title**, platform, date, match count
> - For each snippet: render `>>>text<<<` markers as **bold**, show role — keep each snippet to 1-2 lines max
> - Show context (previous message) in *italic* when present — single line
> - End with numbered list of conversation IDs for follow-up
> Return **max 80 lines**. If more results exist, note "N more results available — increase --limit".

## Phase 4: FOLLOW-UP

After receiving formatted results from the subagent, the main agent offers:
- **Show full conversation**: delegate to haiku subagent with `--conversation <id>`
- **Refine search**: adjust query or add filters
- **New search**: start fresh query

For showing a conversation, delegate to a **haiku** subagent. The script auto-limits output:
- `--max-messages N` — max messages returned (default 40)
- `--truncate N` — truncate each message to N chars (default 300, use 0 for full)
- `--around N` — center the window around message index N (useful after search)

> Run `python3 {SKILL_DIR}/scripts/search_conversations.py --conversation <id> --db ~/.chat-archive/conversations.db [--max-messages 30] [--around <index>]`.
> Format each message as: `**role** (timestamp): content`
> At the top, show: "Showing messages X–Y of Z (truncated at N chars)"
> If there are more messages, note it so the main agent can offer to load more with `--around`.
> Return **max 80 lines** of formatted text.

## Export Format Reference

**ChatGPT**: Array of objects with `title`, `create_time`, `mapping` (tree of nodes with `message.content.parts[]`). Walk from `current_node` up parent chain, reverse for chronological.

**Claude.ai**: Array of objects with `name`, `created_at`, `updated_at`, `chat_messages[]` each having `sender` (human/assistant), `text`, `created_at`.
