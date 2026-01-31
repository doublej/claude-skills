# Obsidian + Claude Code: Safe Integration Patterns

**Alternative**: How to get 95% of Obsidian MCP benefits without the maintenance burden.

---

## The Problem with Obsidian MCP Servers

Every candidate wraps **Obsidian's Local REST API** with an MCP interface:

```
Claude Code
    ↓
Obsidian MCP Server (Node.js process)
    ↓
Obsidian Local REST API plugin
    ↓
Obsidian vault (files)
```

**Three failure points** instead of one:
1. MCP server (Node.js, npm dependencies, 8-10 tools)
2. REST API plugin (community-maintained, undocumented)
3. Obsidian (changes API structure without notice)

---

## Better Architecture: Filesystem-First

```
Claude Code
    ↓
[Filesystem MCP] ← Official, Anthropic-maintained
    ↓
Obsidian vault (files)
    ↓
[Optional] Custom scripts (semantic search, tag filtering, etc.)
```

**One failure point**: filesystem (rock-solid, OS-level).

---

## Feature Parity: What You're Actually Losing

| Obsidian MCP Feature | Filesystem MCP Equivalent | Implementation |
|---|---|---|
| **Read note** | ✅ Built-in | `filesystem.read_file("vault/Notes/Topic.md")` |
| **List vault** | ✅ Built-in | `filesystem.list_directory("vault/")` |
| **Create note** | ✅ Built-in | `filesystem.write_file("vault/New.md", content)` |
| **Search by text** | ⚡ Custom script | `grep -r "keyword" vault/` |
| **Search by tag** | ⚡ Custom script | `python scripts/find_tags.py "#project"` |
| **List backlinks** | ⚡ Custom script | `python scripts/find_backlinks.py "Note Title"` |
| **Rename tag** | ⚡ Custom script | `python scripts/rename_tag.py "#old" "#new"` |
| **Graph relations** | 🚫 Not useful | Claude semantic understanding > graph visualization |
| **Sync to daily note** | ⚡ Custom script | `python scripts/append_to_daily.py "text"` |

**Bottom line**: Obsidian MCP tools 1–5 are redundant. 6–9 are nice-to-have and easily scripted.

---

## Example 1: Semantic Note Search

### Via Obsidian MCP Server (cyanheads)

```javascript
// Relies on Obsidian REST API, MCP SDK, Node.js process running
// If any breaks: integration fails silently

const results = await mcpClient.call_tool("search_vault", {
  query: "how to implement authentication",
  vault_id: "default"
});
```

**Risks**:
- MCP server process might crash
- Obsidian REST API might change
- Results cached for 10 minutes (stale)

### Via Filesystem MCP + Script (Better)

```python
# ~/scripts/semantic_search.py

import os
from pathlib import Path
import sys

def search_vault(query: str, vault_path: str = os.path.expanduser("~/Obsidian")):
    """
    Semantic search across vault using Claude's context.
    Claude reads all files via Filesystem MCP, filters locally.
    """
    notes = list(Path(vault_path).glob("**/*.md"))
    results = []

    for note in notes:
        content = note.read_text(errors="ignore")
        # Basic keyword match (Claude can do better with embeddings)
        if query.lower() in content.lower():
            results.append({
                "path": str(note.relative_to(vault_path)),
                "excerpt": content[:200]  # First 200 chars as preview
            })

    return sorted(results, key=lambda x: len(x["excerpt"]))[:10]  # Top 10

if __name__ == "__main__":
    import json
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(search_vault(query), indent=2))
```

**Claude invokes**:
```bash
python ~/scripts/semantic_search.py "authentication patterns"
```

**Advantages**:
- No MCP server process needed
- Transparent logic (Claude can see exactly what's happening)
- Can improve with embeddings anytime
- No API dependencies
- Instant search (no cache)

---

## Example 2: Tag-Based Filtering

### Via Obsidian MCP Server

```javascript
// Relies on MCP server + Obsidian API
const notes_with_tag = await mcpClient.call_tool("add_tags", {
  note_id: "file-id",
  tags: ["#project", "#active"]
});
```

**Problems**:
- MCP tool returns generic response
- No way to search tags efficiently
- Tag metadata lives in Obsidian's cache, not files

### Via Filesystem MCP + Script (Better)

```python
# ~/scripts/tag_operations.py

from pathlib import Path
import re
import sys
import json

def find_notes_with_tag(tag: str, vault_path: str = os.path.expanduser("~/Obsidian")):
    """Find all notes containing a specific tag."""
    tag_pattern = f"#{tag.lstrip('#')}"  # Normalize to #tag
    notes = list(Path(vault_path).glob("**/*.md"))

    matching = []
    for note in notes:
        content = note.read_text(errors="ignore")
        if tag_pattern in content:
            matching.append(str(note.relative_to(vault_path)))

    return sorted(matching)

def add_tag_to_note(note_path: str, tag: str, vault_path: str = os.path.expanduser("~/Obsidian")):
    """Add a tag to a note's metadata section."""
    full_path = Path(vault_path) / note_path
    content = full_path.read_text(errors="ignore")

    # Append tag to frontmatter or note body
    tag_normalized = f"#{tag.lstrip('#')}"
    if tag_normalized not in content:
        content += f"\n{tag_normalized}"
        full_path.write_text(content)
        return True
    return False

def rename_tag_in_vault(old_tag: str, new_tag: str, vault_path: str = os.path.expanduser("~/Obsidian")):
    """Rename a tag across all notes."""
    old_pattern = f"#{old_tag.lstrip('#')}"
    new_tag_normalized = f"#{new_tag.lstrip('#')}"

    notes = list(Path(vault_path).glob("**/*.md"))
    count = 0

    for note in notes:
        content = note.read_text(errors="ignore")
        if old_pattern in content:
            new_content = content.replace(old_pattern, new_tag_normalized)
            note.write_text(new_content)
            count += 1

    return count

# CLI interface
if __name__ == "__main__":
    if sys.argv[1] == "find":
        results = find_notes_with_tag(sys.argv[2])
        print(json.dumps(results))
    elif sys.argv[1] == "add":
        added = add_tag_to_note(sys.argv[2], sys.argv[3])
        print(json.dumps({"success": added}))
    elif sys.argv[1] == "rename":
        count = rename_tag_in_vault(sys.argv[2], sys.argv[3])
        print(json.dumps({"renamed": count}))
```

**Claude invokes**:
```bash
# Find all notes tagged #project
python ~/scripts/tag_operations.py find project

# Add tag to a note
python ~/scripts/tag_operations.py add "2026-01/Notes.md" "archived"

# Rename a tag across vault
python ~/scripts/tag_operations.py rename "wip" "in-progress"
```

**Advantages**:
- Plain-text tags in files (no Obsidian dependency)
- Batch operations work (rename-all-tags in seconds)
- Full control over tag format
- No MCP server process needed

---

## Example 3: Daily Note Synchronization

### Via Obsidian MCP Server

```javascript
// Complex: relies on Obsidian's daily note format detection
// What if user changes daily note folder? MCP server breaks.

const result = await mcpClient.call_tool("append_to_daily", {
  text: "## Claude Session\n- Analyzed project X\n- Resolved bug Y",
  vault_id: "default"
});
```

### Via Filesystem MCP + Script (Better)

```python
# ~/scripts/daily_note.py

from pathlib import Path
from datetime import datetime
import os
import sys

def get_daily_note_path(vault_path: str = os.path.expanduser("~/Obsidian")) -> Path:
    """
    Determine daily note path.
    Customize this for your vault's structure (e.g., /Daily/2026-01-31.md).
    """
    # Example: Daily/YYYY-MM-DD.md
    today = datetime.now().strftime("%Y-%m-%d")
    daily_dir = Path(vault_path) / "Daily"
    daily_dir.mkdir(exist_ok=True)
    return daily_dir / f"{today}.md"

def append_to_daily(text: str, vault_path: str = os.path.expanduser("~/Obsidian")) -> bool:
    """Append text to today's daily note."""
    note_path = get_daily_note_path(vault_path)

    # Create if doesn't exist
    if not note_path.exists():
        header = f"# {datetime.now().strftime('%A, %B %d, %Y')}\n\n"
        note_path.write_text(header)

    # Append with timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"\n- [{timestamp}] {text}"

    with open(note_path, "a") as f:
        f.write(entry)

    return True

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    success = append_to_daily(text)
    print(success)
```

**Claude invokes**:
```bash
python ~/scripts/daily_note.py "Analyzed authentication architecture"
```

**Advantages**:
- No Obsidian dependency (just filesystem)
- Works even if Obsidian is closed
- Customizable note format
- Transparent timestamp/formatting

---

## Setup: Complete Example

### Directory Structure

```
~/claude-skills/
├── obsidian-tools/                    # Claude integration scripts
│   ├── __init__.py
│   ├── semantic_search.py             # Example 1
│   ├── tag_operations.py              # Example 2
│   ├── daily_note.py                  # Example 3
│   └── vault_backup.py                # Bonus: auto-backup
├── config/
│   └── mcp-servers.json               # Filesystem MCP config
└── README.md                          # Documentation

~/.claude/
├── config.json                        # Claude Code settings
└── mcp-servers/
    └── filesystem.json                # Filesystem MCP config
```

### 1. Configure Filesystem MCP

**File**: `~/.claude/mcp-servers.json`

```json
{
  "filesystem": {
    "command": "node",
    "args": ["/path/to/mcp-filesystem-server"],
    "env": {
      "MCP_ALLOWED_DIRECTORIES": "/Users/jurrejan/Obsidian"
    }
  }
}
```

### 2. Add Custom Scripts to PATH

**File**: `~/.bash_profile` or `~/.zshrc`

```bash
export CLAUDE_SCRIPTS="$HOME/claude-skills/obsidian-tools"
export PATH="$CLAUDE_SCRIPTS:$PATH"
```

### 3. Claude Invokes Scripts

```bash
# Example: Claude searches vault
python semantic_search.py "authentication"

# Example: Claude adds tag
python tag_operations.py add "Notes/AI.md" "research"

# Example: Claude logs to daily
python daily_note.py "Completed feature X"
```

---

## Comparison: Maintenance Burden Over Time

### Year 1: Obsidian MCP Server (cyanheads)

```
Month 1:  Setup (2 hours) → MCP server running, exciting!
Month 3:  Node.js 20.14 released → npm audit warnings (1 hour)
Month 6:  Obsidian v1.5 released → REST API changed slightly (4 hours debugging)
Month 8:  MCP SDK 1.14 released → Update dependencies (30 min)
Month 10: Obsidian v1.6 → REST API breaking change (8 hours + fork + maintain)
Month 12: Still maintaining a fork, monitoring upstream for fixes

Total: ~15 hours + psychological burden + risk of data loss
```

### Year 1: Filesystem MCP + Scripts

```
Month 1:  Setup (30 min) → Scripts working
Month 3:  Python 3.11 released → No action needed (Python 3.10 compatible)
Month 6:  Add semantic search feature → 1 hour (new script)
Month 8:  Add tag rename feature → 30 min (new script)
Month 10: Obsidian v1.6 → No action needed (doesn't affect scripts)
Month 12: Still working, zero maintenance debt

Total: ~2 hours + peace of mind + easy to change
```

**Cost Difference**: 13 hours + risk vs. 2 hours + stability.

---

## When to Use Obsidian MCP Anyway

**Only if ALL of these are true**:

1. You need **Obsidian graph visualization** in Claude (rare; Claude understands relations natively)
2. You need **Obsidian plugin integration** (e.g., Templater prompts in Claude workflows)
3. You have **no Python scripting expertise** (can't write `tag_operations.py`)
4. You **trust** the MCP server maintainer for 18+ months
5. You're **willing to fork and maintain** if they go dormant

For everyone else: **use Filesystem MCP + scripts**.

---

## Bonus: Auto-Backup Script

Since Filesystem MCP allows writes, add a safety net:

```python
# ~/scripts/vault_backup.py

from pathlib import Path
from datetime import datetime
import shutil
import os

def backup_vault(vault_path: str = os.path.expanduser("~/Obsidian")):
    """Create timestamped backup of vault."""
    backup_dir = Path(vault_path).parent / "Obsidian-backups"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = backup_dir / f"backup_{timestamp}"

    shutil.copytree(vault_path, backup_path)
    print(f"Backed up to {backup_path}")

    # Cleanup old backups (keep last 7)
    backups = sorted(backup_dir.glob("backup_*"), reverse=True)
    for old_backup in backups[7:]:
        shutil.rmtree(old_backup)
        print(f"Cleaned up {old_backup}")

if __name__ == "__main__":
    backup_vault()
```

**Claude can call before risky operations**:
```bash
python vault_backup.py && python tag_operations.py rename "old" "new"
```

---

## Summary: Safe Obsidian + Claude Integration

| Approach | Setup Time | Maintenance | Risk | Flexibility |
|---|---|---|---|---|
| Obsidian MCP Server | 2–8 hours | ~15 hrs/year | HIGH | Medium |
| Filesystem MCP + Scripts | 30 min | ~2 hrs/year | LOW | HIGH |
| **Recommendation** | | | | **→ Use this** |

**Start with Filesystem MCP**. Add custom scripts as needs arise. Never need to touch Obsidian MCP servers.

If in Q3 2026 the ecosystem stabilizes, you can still revisit. But for now, **treat Obsidian MCP as experimental**.

---

**Next Steps**:
1. Set up Filesystem MCP (30 min)
2. Create `~/scripts/semantic_search.py` (template provided above)
3. Test with Claude Code: `python semantic_search.py "topic"`
4. Add more scripts as needed (tag_operations.py, daily_note.py, etc.)
5. Document your vault's structure in a README
6. Backup regularly with `vault_backup.py`
7. Revisit this decision in Q3 2026

That's it. No Obsidian MCP server required.
