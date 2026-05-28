# Wiring code-arch-drift as a Claude Code hook

The checker is a plain script, so it drops into Claude Code hooks for in-session
drift correction. Two useful hook points:

- **`PostToolUse` on `Write|Edit`** — re-check after each edit, surface drift the
  edit introduced while the model is still in context to fix it.
- **`Stop`** — a final checkpoint so unresolved drift is flagged before the turn ends.

## Lenient (advisory) — recommended default

Drift is reported as context; the model tends to self-correct on the next step.
Add to `~/.claude/settings.json` (adjust the script path to the installed skill):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/code-arch-drift/scripts/archcheck.py --root \"$CLAUDE_PROJECT_DIR\" 2>/dev/null | head -30"
          }
        ]
      }
    ]
  }
}
```

The script prints to stdout and exits 1 on violations; in `PostToolUse` that
output is surfaced to the model as additional context without blocking.

## Strict (block) — force resolution

To make drift block the turn until fixed, wrap the checker so it emits a hook
decision. Create `scripts/hook-strict.sh` (or inline) that converts a non-zero
exit into a `{"decision": "block", "reason": "..."}` JSON payload on stdout per
the Claude Code hooks contract. Use sparingly — strict mode on a noisy blueprint
stalls the session.

## Performance

`archcheck.py` is O(files) with regex import extraction — milliseconds on small
repos, sub-second on a few thousand files. For very large monorepos, scope the
hook with `--root` to the active package rather than the whole tree.

## Alternative: archtest (standalone, language-agnostic)

If you want rule enforcement decoupled from this skill — e.g. a CI-owned check in
a repo that doesn't use Claude Code — [`@rickheere/archtest`](https://github.com/rickheere/archtest)
enforces declarative YAML boundary rules via deterministic grep. The LLM authors
the rules once (`npx @rickheere/archtest interview`), CI runs them with no LLM in
the loop. Complementary to this skill, not a replacement: archtest is grep over
import lines; `archcheck.py` resolves imports to actual repo files and maps them
to layers.
