# Subagent lifecycle in named tabs

Run each Claude Code subagent in a dedicated `<project>:agent:<id>` tab
inside the project workspace. Five phases: **spawn → trust → prompt →
wait → harvest**. Every phase has a verb in this skill.

## Why named tabs (not windows, not unnamed splits)

- **Findable.** `cmux-find.sh myproj` lists every agent currently running
  on the project. No ambiguity about which window holds what.
- **Addressable.** `cmux-send.sh myproj agent:1 "…" --enter` works from
  any script, any session, any day.
- **Cleanable.** `close-surface` by tab name, no "which one was it again".

## Phase 1: spawn

```bash
PROJECT=myproj
AGENT_ID=1
CWD=$(pwd)

./scripts/cmux-tab.sh "$PROJECT" "agent:$AGENT_ID" "$CWD"
./scripts/cmux-send.sh "$PROJECT" "agent:$AGENT_ID" \
  "claude code --dangerously-skip-permissions" --enter
```

`cmux-tab.sh` is idempotent — re-running it just reuses the tab. Safe to
call from a for-loop that spawns N agents.

## Phase 2: trust detection

Claude Code's first prompt on an untrusted dir is the "Trust the files in
this folder?" dialog. Detect and answer before sending the real prompt:

```bash
SID=$(./scripts/cmux-find.sh "$PROJECT" \
      | jq -r '.tabs[] | select(.tab == "'"$PROJECT:agent:$AGENT_ID"'") | .surface')

# Refresh screen state before reading (see troubleshooting.md)
cmux refresh-surfaces --surface "$SID"
SCREEN=$(cmux read-screen --surface "$SID")

if [[ "$SCREEN" == *"Trust the files"* ]]; then
  ./scripts/cmux-send.sh "$PROJECT" "agent:$AGENT_ID" "" --key Return
  sleep 0.5
fi
```

## Phase 3: prompt

Send the task. Use `--enter` so Claude actually runs:

```bash
./scripts/cmux-send.sh "$PROJECT" "agent:$AGENT_ID" \
  "Implement the cache layer from docs/plan.md. Commit when done." --enter
```

For multi-line prompts, send the body with a heredoc-style approach: many
agents tolerate `\n` in the input, but the safest pattern is one line at
a time with `--key Return` between:

```bash
./scripts/cmux-send.sh "$PROJECT" "agent:$AGENT_ID" "Line one"
./scripts/cmux-send.sh "$PROJECT" "agent:$AGENT_ID" "" --key Return
./scripts/cmux-send.sh "$PROJECT" "agent:$AGENT_ID" "Line two" --enter
```

## Phase 4: wait for completion

Claude Code drops back to the shell prompt when done. Poll `read-screen`
for the prompt pattern, with a generous timeout:

```bash
completed_at=""
deadline=$(( $(date +%s) + 1800 ))   # 30 min
while [[ -z "$completed_at" && $(date +%s) -lt $deadline ]]; do
  sleep 5
  cmux refresh-surfaces --surface "$SID"
  last=$(cmux read-screen --surface "$SID" | tail -3)
  # Shell prompt has the user@host format; Claude UI does not.
  if grep -qE '[[:alnum:]_-]+@[[:alnum:].-]+' <<<"$last" \
     && ! grep -q '│' <<<"$last"; then
    completed_at=$(date +%s)
  fi
done
```

Prefer this over `sleep 600` — agents sometimes finish in 30s, sometimes
in 20min. A poll with a real completion signal is faster AND safer.

## Phase 5: harvest

Read transcript, commit, notify:

```bash
cmux read-screen --surface "$SID" --scrollback 2000 > "/tmp/$AGENT_ID.log"

# Optional: flag completion in cmux's status bar
cmux set-status --surface "$SID" "done"
cmux notify --workspace "$WS" --title "Agent $AGENT_ID done" \
  --body "See /tmp/$AGENT_ID.log"
```

## Phase 6: teardown (optional)

If you don't plan to reuse the agent slot:

```bash
cmux close-surface --surface "$SID"
```

Keep it open if you'll spawn more agents into `agent:1` over the session
— reusing a live shell is faster than rebuilding.

## Driving N agents in parallel

```bash
PROJECT=multi
./scripts/cmux-project.sh "$PROJECT" grid

# Fan-out: one prompt per agent, all running concurrently
for id in 0 1 2 3; do
  ./scripts/cmux-tab.sh  "$PROJECT" "agent:$id" "$(pwd)"
  ./scripts/cmux-send.sh "$PROJECT" "agent:$id" \
    "claude code --dangerously-skip-permissions" --enter
  sleep 1
  ./scripts/cmux-send.sh "$PROJECT" "agent:$id" \
    "Task $id: $(task_for $id)" --enter
done
```

The 1s sleep between spawns dodges the PTY init race documented in
`references/troubleshooting.md`.

## Anti-patterns

- **Unnamed splits.** `cmux new-split` without `--tab` gives you `srf_abc`.
  Impossible to address from another session. Always name.
- **One workspace per agent.** Defeats the point. One project → one
  workspace → N agent tabs.
- **Polling with `sleep N` as the only completion signal.** Read the
  screen. Look for the shell prompt. Fail if timeout exceeds.
- **Reusing a tab for a different agent slot.** If `agent:1` finishes and
  you want to run a different task, that's fine — same slot. If it's a
  genuinely different agent identity, use `agent:2`.
