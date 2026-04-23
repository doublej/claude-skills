# cmux skill — feedback log

Append-only. Each entry is a real friction point an agent ran into while
using this skill. See SKILL.md §Feedback loop for the rules and format.

The user harvests this file to tighten docs, add helpers, or fix
spec-drift. Empty stretches mean things are working — do NOT log "no
issues" entries.

---

<!-- Template for new entries — copy, fill, append below this line.

### YYYY-MM-DD — <1-line subject line, imperative>
**Tried:**   <command or intent — 1 line>
**Broke:**   <concrete friction — error text, surprise, missing helper>
**Fix idea:** <doc line / new helper / clearer error / schema change>

-->

### 2026-04-24 — `cmux list-workspaces --json` returns column text, not JSON
**Tried:**   `cmux list-workspaces --json | jq ...` per SKILL.md §Discovery
**Broke:**   CLI silently ignores `--json`; output is columns like
             `workspace:7  pimpelmees`. jq errors with "Invalid numeric literal".
             All three core helpers (cmux-project.sh / cmux-tab.sh / cmux-send.sh)
             assume JSON — they're broken against the current cmux build.
**Fix idea:** Port the helpers to `cmux rpc <method>` (verified to return JSON
             via `cmux capabilities`). Or document an `--id-format uuids` +
             awk fallback in SKILL.md so agents don't burn a cycle on this.

### 2026-04-24 — `~/.claude/projects/` encoding drops `_` not just `/`
**Tried:**   Built `_encode_cwd_for_claude` as `path.replace('/', '-')` per plan
**Broke:**   Real folder name for `/Users/.../​_management/claude-skills` is
             `-Users-...--management-claude-skills` (double-dash). Naive encoder
             produced `-Users-...-_management-...` → file-not-found.
**Fix idea:** Document the encoding rule `(/|_) → -` explicitly in
             `references/workspace-spec.md` and in any new SKILL.md section that
             mentions session paths. Reference `session-search` as the
             canonical implementation.
