---
name: skill-feedback
description: Report feedback on skills from any project. Choose between spawning a Claude Code session to act immediately or creating a beads ticket for later.
---

# Skill Feedback

Report feedback (bugs, improvements, ideas) on any skill — from whatever project you're in.

## Path Resolution

Resolve the skills project root from this skill's install symlink:

```bash
SKILLS_ROOT="$(dirname "$(readlink -f ~/.claude/skills/skill-feedback)")"
```

Use `$SKILLS_ROOT` for all operations below. Never hardcode paths.

## Workflow

### 1. Gather feedback

Ask the user (prefer consult-user-mcp if available):

- **Which skill?** — free text (skill name or folder)
- **What feedback?** — free text describing the bug, idea, or improvement
- **Mode?** — "Act now" or "Create ticket"

### 2a. Act now (tmux + claude -p)

Spawn a headless Claude Code session in tmux targeting the skills project.

**Important:** Run all commands in a single Bash call so variables persist. Write the prompt to a temp file to avoid quoting issues with `send-keys`.

```bash
# Resolve paths
SKILLS_ROOT="$(dirname "$(readlink -f ~/.claude/skills/skill-feedback)")"
SOCKET_DIR="${TMPDIR:-/tmp}/claude-tmux-sockets"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/claude.sock"
SESSION="claude-skill-feedback"

# Write prompt to temp file (avoids send-keys quoting problems)
PROMPT_FILE="$(mktemp)"
cat > "$PROMPT_FILE" << 'PROMPT'
Skill: <skill_name>. Feedback: <feedback_text>. Investigate and fix or improve as described.
PROMPT

# Kill stale session if it exists
tmux -S "$SOCKET" kill-session -t "$SESSION" 2>/dev/null || true

# Start new session in the skills project
tmux -S "$SOCKET" new-session -d -s "$SESSION" -c "$SKILLS_ROOT"

# Run Claude with prompt from file (cat piped to claude -p)
tmux -S "$SOCKET" send-keys -t "$SESSION" \
  "cat '$PROMPT_FILE' | claude -p --permission-mode acceptEdits; rm '$PROMPT_FILE'" Enter

# Print the ACTUAL resolved socket path for the user
echo "To monitor this session:"
echo "  tmux -S $SOCKET attach -t $SESSION"
```

Print the monitor command with the **resolved** `$SOCKET` path (not hardcoded `/tmp/`). Then poll for completion using `capture-pane` — check for the shell prompt `$` appearing after the claude command finishes. Report the result summary back to the user.

### 2b. Create ticket (beads)

Create a beads issue in the skills project:

```bash
cd "$SKILLS_ROOT"
bd create "<skill_name>: <short_title>"
```

Then optionally set description and labels:

```bash
# Get the issue ID from the create output
bd update <issue_id> --description "<full feedback text>"
bd label add <issue_id> feedback
```

Confirm to the user with the issue ID and a reminder they can view it with `bd list` in the skills project.

## Rules

- Always resolve `SKILLS_ROOT` dynamically — never hardcode
- **Run all tmux setup + send-keys in a single Bash call** so variables persist across commands
- **Never hardcode socket paths** — always use the resolved `$SOCKET` variable when printing monitor commands
- Write long prompts to a temp file and pipe to `claude -p` to avoid send-keys quoting breakage
- Always print the tmux monitor command immediately after spawning
- Keep ticket titles short; put details in the description
- If `bd` is not found, fall back to creating a markdown file at `$SKILLS_ROOT/.beads/manual/<skill_name>-<timestamp>.md`
