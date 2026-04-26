---
name: codex-launch
description: "Spawn a Codex session visibly for the user — either in the Codex desktop app (`:app`) or live in their frontmost terminal (`:cli`). Use when the user wants to hand a task to Codex, see Codex run something side-by-side, get a Codex second opinion in a separate window, or 'open this in Codex'. Triggers on '/codex-launch', 'launch in codex', 'open codex', 'fire up codex', 'kick off codex', 'codex this', 'send this to codex'. The user watches the session run; this skill does not capture Codex's output back into Claude."
---

# codex-launch

Hand a task off to a Codex session the user can see and steer. Two variants:

- `:app` — opens the **Codex desktop app**, prompt prefilled on clipboard (user pastes).
- `:cli` — keystrokes `codex "<prompt>"` into the **frontmost terminal** (user watches it run).

This is a fire-and-forget handoff. Codex's output stays with the user. Do not try to scrape it back unless the user explicitly asks for that follow-up.

<when_to_use>

- User says "open this in Codex", "let Codex handle this", "kick off codex", "second opinion from codex"
- User wants Codex working in parallel while Claude continues
- A long task where the user prefers to watch Codex live rather than have Claude relay results

**Skip** if the user wants Claude to *call* Codex and *use* its answer — that's the `codex:rescue` subagent, not this skill.

</when_to_use>

<picking_a_variant>

| User signal | Use |
|---|---|
| "in the app", "Codex desktop", "in the GUI" | `:app` |
| "in the terminal", "in this shell", "right here", or already in iTerm/Ghostty/cmux | `:cli` |
| Ambiguous | Ask which one — one short pick. Do not guess. |

</picking_a_variant>

<variant_app>

## `:app` — Codex desktop app

```bash
scripts/launch_app.sh "<prompt>"
```

What it does:
1. Copies prompt to clipboard (`pbcopy`)
2. `open -a "Codex"` — brings the desktop app to the front
3. Notifies the user to paste with ⌘V

After running, tell the user one line: *"Codex app opened — prompt is on your clipboard, ⌘V to paste."* Do not wait for output.

</variant_app>

<variant_cli>

## `:cli` — frontmost terminal

```bash
scripts/launch_cli.sh "<prompt>" [extra codex flags]
```

What it does:
1. Builds `codex "<prompt>"` (with optional flags like `-a full-auto`)
2. Uses `osascript` + System Events to keystroke it into whatever app is currently frontmost
3. Presses Return

The user must have a terminal window focused. If unsure, ask: *"Make sure your terminal is the frontmost window — ready?"*

**Extra flags** pass straight through to `codex`:

```bash
scripts/launch_cli.sh "fix the failing tests" -a full-auto
scripts/launch_cli.sh "review this PR" -a suggest
```

Common flags worth offering:
- `-a suggest` — read-only (default, safe)
- `-a auto-edit` — can edit files, asks before shell
- `-a full-auto` — sandboxed, no approvals
- `-m <model>` — override model

</variant_cli>

<prompt_construction>

Before launching, shape the prompt so Codex starts well:

- Include the **goal**, not just the trigger ("fix the failing auth tests in `apps/api/tests/auth.test.ts`" beats "fix tests")
- Include the **working directory** if the user's terminal might be elsewhere — Codex picks up CWD from where it's launched
- Keep it one paragraph; Codex's TUI handles long pastes fine but the keystroke path (`:cli`) is faster with shorter prompts

If the user gave a vague handoff ("send this to codex"), summarize the conversation context into a self-contained prompt — Codex has none of Claude's context.

</prompt_construction>

<accessibility_permission>

`:cli` requires macOS Accessibility permission for whichever process invokes `osascript` (Terminal, iTerm2, Claude Code's harness, etc.). If the keystroke silently no-ops:

> System Settings → Privacy & Security → Accessibility → enable the relevant app.

Surface this once if `:cli` appears to do nothing — do not retry blindly.

</accessibility_permission>

<anti_patterns>

- **Don't** try to read Codex's output back into Claude. This skill is a handoff, not a pipe. For a programmatic Codex call, use `codex:rescue` or `codex -q` directly.
- **Don't** chain multiple launches without checking the first worked. If `:cli` keystroked into the wrong window, the user needs to know.
- **Don't** invent codex flags. If a flag isn't documented in `codex --help`, ask first.
- **Don't** assume the desktop app accepts URL schemes or CLI args — at time of writing, clipboard paste is the reliable path.

</anti_patterns>
