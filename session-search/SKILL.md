---
name: session-search
description: "Search Claude Code session history by exact phrase with smart time windowing and timeline visualization. Use when (1) User wants to find past conversations about a topic, (2) User asks 'when did I work on X', (3) User needs context from previous sessions, (4) User wants to recall what was discussed. Triggers on 'search history', 'find in sessions', 'when did I', 'recall conversation about'."
---

# Session Search

## Initialization

Display boot sequence:

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   SESSION SEARCH v1.0                                      ║
║   Phrase-Based History Retrieval                           ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║   [LOAD] Project session scanner                           ║
║   [LOAD] Exact phrase search engine                        ║
║   [LOAD] Time window builder                               ║
║   [LOAD] Timeline generator                                ║
║                                                            ║
║   System ready.                                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## Phase 1: QUERY

Ask the user what they want to search for:

```
What phrase would you like to search for in your session history?

Enter exact phrase to match (e.g. "swift app" or "api integration"):
```

**IMPORTANT:** The search uses EXACT PHRASE matching. The user should provide the complete phrase they want to find, not individual keywords.

Optional parameters (ask if user wants to customize):
- **Margin**: Minutes of context before/after matches (default: 5)
- **Gap**: Max gap to merge adjacent windows (default: 10)

---

## Phase 2: SEARCH

Run the search with timeline generation:

```bash
python3 {SKILL_DIR}/scripts/search_session.py "<phrase>" -m <margin> -g <gap> -o .session-search -t
```

The script outputs:
- Summary box with match count
- Visual timeline of activities
- JSON result data

---

## Phase 3: TIMELINE

The `-t` flag generates a visual timeline showing:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                            TIMELINE: "search phrase"                           ║
║                            2025-12-05 - 2025-12-10                             ║
╠════════════════════════════════════════════════════════════════════════════════╣

  Dec 05   ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●
  21:36   │ 14m session
          │ • User request or activity description
          │ • Another activity in this window
          └─────────────────────────────────────────────────────────────────────

  Dec 07   ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●
  09:11   │ 28m session
          │ • Activities extracted from matches
          └─────────────────────────────────────────────────────────────────────

╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Phase 4: REVIEW

Present options to explore:
- "Show timeline" - Display the generated timeline
- "Show window N" - Read context_messages.json for specific window
- "Show all matches" - List all matching messages with previews

Based on user selection, read `.session-search/context_messages.json` and display chronological conversation.

---

## Output Files

Search creates:
- `.session-search/search_index.json` - Match metadata and window definitions
- `.session-search/context_messages.json` - Full messages within all windows
- `.session-search/timeline.txt` - ASCII timeline visualization

---

## Technical Reference

**Search behavior:**
- **EXACT PHRASE** matching (case-insensitive)
- Searches both user AND assistant messages
- Time windows have configurable margins (default ±5 min)
- Adjacent windows within gap threshold merge (default 10 min)

**Timeline generation:**
- Groups matches by date
- Extracts meaningful activities from user requests and assistant completions
- Filters out boilerplate messages
- Shows up to 4 activities per time window

**Data source:** `~/.claude/projects/<encoded-path>/<uuid>.jsonl`
- Scans only current project sessions
- Extracts full conversation context (user + assistant)
