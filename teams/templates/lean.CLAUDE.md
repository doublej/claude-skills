# LEAN — scoped-down context for teammate worktree

EXPERIMENTAL. Drop this as `<worktree>/CLAUDE.md` (or merge into existing one) to signal the teammate to keep context light. Docs are silent on whether per-worktree CLAUDE.md is picked up for teammates on top of the parent's; if you verify it is, record the result in `~/.claude/skills/teams/references/token-efficiency.md`.

## Scope for this teammate

- Act strictly within the role stated in your spawn prompt.
- Do **not** invoke skills unless the lead explicitly asks.
- Do **not** consult memory (`MEMORY.md`, `memory/`) unless the lead explicitly asks.
- Do **not** use web tools unless the role's `tools` allowlist includes them.
- Do **not** open other projects' files — stay inside this worktree.

## Minimal output contract

- Short, structured messages back to the lead.
- Cite files by `path:line` when quoting.
- Stop at your stated stop condition. Do not volunteer extra work.
