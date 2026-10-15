#!/usr/bin/env bash
set -euo pipefail

# Opens a tmux split pane to process skill feedback via Claude,
# leaving the current session untouched.
#
# Usage: handoff.sh SKILLS_ROOT ORIG_DIR TMUX_PANE SKILL_NAME FEEDBACK

SKILLS_ROOT="$1"
ORIG_DIR="$2"
ORIG_PANE="$3"
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

# --- Write the command to run in the split pane ---
CONT_SCRIPT="$(mktemp)"
cat > "$CONT_SCRIPT" <<SCRIPT
#!/usr/bin/env bash
set -euo pipefail

# Process feedback in skills project
cd "$SKILLS_ROOT"
claude --dangerously-skip-permissions --chrome "\$(cat '$PROMPT_FILE')"
rm -f "$PROMPT_FILE"

echo ""
echo "Feedback processed. Notifying original session..."
echo ""

# Notify the original session
tmux send-keys -t "$ORIG_PANE" C-c
sleep 1
tmux send-keys -t "$ORIG_PANE" -l '/exit'
tmux send-keys -t "$ORIG_PANE" Enter
sleep 2
tmux send-keys -t "$ORIG_PANE" -l 'echo "Skill feedback for $SKILL_NAME has been processed."'
tmux send-keys -t "$ORIG_PANE" Enter
sleep 1
tmux send-keys -t "$ORIG_PANE" -l 'claude --resume'
tmux send-keys -t "$ORIG_PANE" Enter

# The pane closes when this script exits
rm -f "$CONT_SCRIPT"
SCRIPT
chmod +x "$CONT_SCRIPT"

# --- Run the feedback session in a split pane next to the source pane ---
tmux split-window -h -t "$ORIG_PANE" -c "$SKILLS_ROOT" "bash $CONT_SCRIPT"

echo "Feedback session launched in split pane."
