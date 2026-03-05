#!/usr/bin/env bash
set -euo pipefail

# Opens a new iTerm2 tab to process skill feedback via Claude,
# leaving the current session untouched.
#
# Usage: handoff.sh SKILLS_ROOT ORIG_DIR ITERM_SESSION_ID SKILL_NAME FEEDBACK

SKILLS_ROOT="$1"
ORIG_DIR="$2"
RAW_SESSION_ID="$3"
SKILL_NAME="$4"
FEEDBACK="$5"

# --- Resolve original Claude Code session ID ---
ENCODED_DIR="$(echo "$ORIG_DIR" | sed 's|[/_.]|-|g')"
SESSIONS_FILE="$HOME/.claude/projects/$ENCODED_DIR/sessions-index.json"

if [[ ! -f "$SESSIONS_FILE" ]]; then
  echo "Error: No sessions-index.json found at $SESSIONS_FILE" >&2
  exit 1
fi

SESSION_ID=$(python3 -c "
import json, sys
d = json.load(open('$SESSIONS_FILE'))
entries = [e for e in d.get('entries', []) if not e.get('isSidechain', False)]
if not entries:
    sys.exit(1)
entries.sort(key=lambda e: e.get('modified', ''), reverse=True)
print(entries[0]['sessionId'])
") || {
  echo "Error: Could not extract session ID from $SESSIONS_FILE" >&2
  exit 1
}

# --- Write prompt file ---
PROMPT_FILE="$(mktemp)"
cat > "$PROMPT_FILE" <<PROMPT
You are processing skill feedback for the skills project.

Skill: $SKILL_NAME
Feedback: $FEEDBACK

Instructions:
1. Read the skill's SKILL.md at $SKILL_NAME/SKILL.md
2. Investigate the feedback — read relevant files, understand the issue
3. Apply the fix or improvement
4. Run any relevant checks (lint, test)
5. Commit the changes with a descriptive message
6. Run ./install-skill.sh $SKILL_NAME
7. Exit when done — do NOT start another task
PROMPT

# --- Write the command to run in the new tab ---
CONT_SCRIPT="$(mktemp)"
cat > "$CONT_SCRIPT" <<SCRIPT
#!/usr/bin/env bash
set -euo pipefail

# Process feedback in skills project
cd "$SKILLS_ROOT"
claude --dangerously-skip-permissions --chrome "\$(cat '$PROMPT_FILE')"
rm -f "$PROMPT_FILE"

echo ""
echo "Feedback processed. Resuming original session..."
echo ""

# Resume original session
cd "$ORIG_DIR"
claude --dangerously-skip-permissions --chrome -r "$SESSION_ID"

rm -f "$CONT_SCRIPT"
SCRIPT
chmod +x "$CONT_SCRIPT"

# --- Open a new tab and run the feedback session there ---
it2 newtab -c "bash $CONT_SCRIPT"

echo "Feedback session launched in a new tab."
