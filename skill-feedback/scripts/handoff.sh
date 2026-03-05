#!/usr/bin/env bash
set -euo pipefail

# Opens an iTerm2 split pane to process skill feedback via Claude,
# leaving the current session untouched.
#
# Usage: handoff.sh SKILLS_ROOT ORIG_DIR ITERM_SESSION_ID SKILL_NAME FEEDBACK

SKILLS_ROOT="$1"
ORIG_DIR="$2"
RAW_SESSION_ID="$3"
SKILL_NAME="$4"
FEEDBACK="$5"

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
7. Exit when done — the handoff script will notify the original session that feedback was processed
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
echo "Feedback processed. Restarting original session..."
echo ""

# Exit Claude in the original session, then restart it
it2 send -s "$RAW_SESSION_ID" $'\x03'
sleep 1
it2 send -s "$RAW_SESSION_ID" $'/exit\n'
sleep 2
it2 send -s "$RAW_SESSION_ID" $'echo "Skill feedback for $SKILL_NAME has been processed."\n'
sleep 1
it2 send -s "$RAW_SESSION_ID" $'claude --resume\n'

rm -f "$CONT_SCRIPT"

# Close this feedback pane
sleep 1
osascript -e 'tell application "iTerm2" to tell current session of current window to close'
SCRIPT
chmod +x "$CONT_SCRIPT"

# --- Open a new tab and run the feedback session there ---
it2 hsplit -c "bash $CONT_SCRIPT"

echo "Feedback session launched in a split pane."
