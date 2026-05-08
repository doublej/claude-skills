---
name: browser-router
description: "Edit Browser Router rules from natural language: 'open figma in Chrome', 'always ask for meet.google.com', 'remove drive rule', 'make Dia the default', 'list rules'. Triggers on Browser Router rule/routing/default-browser changes."
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

# Browser Router

Manage routing rules in the Browser Router macOS app by editing
`~/Library/Application Support/Browser Router/config.yaml`.

<authoritative_reference>

The schema, `matchType` semantics, priority rules, bundleID lookup table, and editing
checklist live in:

```
~/Library/Application Support/Browser Router/CLAUDE.md
```

**Read this file at the start of every invocation.** It is the source of truth and stays
in sync with the Swift app. Never duplicate the schema here.

</authoritative_reference>

<workflow>

Every invocation, in order:

1. **Read the reference**: `~/Library/Application Support/Browser Router/CLAUDE.md`.
2. **Read current state**: `~/Library/Application Support/Browser Router/config.yaml`.
   If missing, create from the template in `<bootstrap>` below.
3. **Parse intent** into one of: `add`, `update`, `remove`, `enable`, `disable`,
   `reorder`, `set-default`, `ask-mode`, `list`, `notifications`.
4. **Confirm** when destructive (see `<confirmation_policy>`).
5. **Quit the app** if running, wait until gone:
   `bash "$SKILL_DIR/scripts/app-control.sh" quit`
6. **Edit `config.yaml`** following the checklist in the reference (preserve UUIDs,
   contiguous priorities, catch-all last, two-space indent, bare booleans, quoted
   strings, `promptUser:` line only when `true`).
7. **Relaunch** if it was running before step 5:
   `bash "$SKILL_DIR/scripts/app-control.sh" relaunch`
8. **Report** the diff in human terms and show the affected YAML block.

</workflow>

<intent_parsing>

| User says | Intent | Notes |
|-----------|--------|-------|
| "open X in Chrome", "route X to Arc", "send X to Firefox" | `add` | Bare hostname → `domain`. Path/glob → `wildcard`. Regex literal → `regex`. |
| "always ask for X", "let me choose for X" | `ask-mode` | New rule with `promptUser: true`, `browserID: ""`. |
| "remove the X rule", "delete X" | `remove` | Confirm. Renormalise priorities. |
| "disable X temporarily", "turn off X" | `disable` | Flip `enabled: false`, keep in place. |
| "enable X", "turn X back on" | `enable` | Flip `enabled: true`. |
| "make Dia the default", "default to Chrome" | `set-default` | Update catch-all `browserID`. Create catch-all if missing. |
| "move X above Y", "make X higher priority" | `reorder` | Confirm. |
| "list rules", "show me the rules" | `list` | Run `bash "$SKILL_DIR/scripts/list-rules.sh"`. Read-only. |
| "stop the notification sound", "turn off banners" | `notifications` | Toggle keys under `notificationSettings`. |

**Pattern-type defaults** (from a bare user phrase):
- bare hostname (`figma.com`, `github.com`) → `matchType: domain`
- path or `*` glob (`*.github.com/*`, `github.com/issues`) → `matchType: wildcard`
- starts with `^`, contains `\\` or `[` → `matchType: regex`
- Anything ambiguous → ask via consult-user-mcp.

**Port range**: phrases like "localhost:3000", "send 3000 to X" → add
`portRange: {start: 3000, end: 3000}`.

</intent_parsing>

<confirmation_policy>

| Operation | Confirm first? |
|-----------|----------------|
| `list`, default lookup | No |
| Single `add` / `enable` / `disable` | No |
| `remove`, `reorder`, `set-default` | **Yes** — show what changes |
| Bulk (multiple rules in one invocation) | **Yes** |

Use `consult-user-mcp` `ask` (`type: "confirm"`) for confirmations.

</confirmation_policy>

<resolving_browsers>

1. Try the bundleID table in the reference first ("chrome" → `com.google.Chrome`, "arc" →
   `company.thebrowser.Browser`, "dia" → `company.thebrowser.dia`, etc.).
2. Fallback for unlisted apps:
   ```bash
   mdls -name kMDItemCFBundleIdentifier -raw "/Applications/<App Name>.app"
   ```
3. If multiple installs match (e.g. Chrome + Chrome Canary + Chrome Beta), ask which one
   via `consult-user-mcp`.
4. App not installed → warn but allow; the runtime falls back to the system default.

**Profiles** (`profileID`) are not listed in YAML — the app discovers them at runtime.
When the user names a profile and you can't disambiguate, ask. Common values: Chrome
`"Profile 1"` / `"Profile 2"` / `"Default"`; Arc `"Personal"` / `"Work"`.

</resolving_browsers>

<uuid_generation>

New rules need fresh UUIDs. Use `uuidgen` (uppercase 8-4-4-4-12, matches existing
format):

```bash
uuidgen
# e.g. F921C3C5-7930-4771-B942-BA7DFE4AC583
```

**Never** reuse an existing rule's UUID for a new rule. Preserve every existing UUID on
unchanged rules.

</uuid_generation>

<priority_handling>

- Lower number = evaluated first.
- Catch-all (`pattern: "*"`, `matchType: wildcard`) sits at the largest priority.
- Keep priorities contiguous starting at 0.
- Adding a new specific rule: append before the catch-all at `priority = current_catch_all_priority`,
  then bump catch-all by 1.
- Removing: delete, then renormalise to a contiguous `0…n` sequence.
- Reordering: swap or shift, then renormalise.

</priority_handling>

<edge_cases>

- **App is running** — quit first; else edits get clobbered on next save.
- **Rule doesn't exist** — list candidates and ask which one.
- **Browser not installed** — warn, allow; runtime falls back.
- **Ambiguous reference** ("the github rule" with two matches) — show pattern + priority
  for each, ask.
- **Catch-all conflict** when adding — push catch-all priority up and renormalise.
- **`config.yaml` missing** — bootstrap from `<bootstrap>` then proceed.
- **Unknown top-level keys** — leave alone; parser drops unknowns silently but a future
  version may use them.

</edge_cases>

<bootstrap>

If `config.yaml` is missing, write this minimal template:

```yaml
routingEnabled: true

notificationSettings:
  showBanner: true
  flashIcon: true
  trackRecent: true
  playSound: true
  soundName: "Bottle"
  maxRecentURLs: 10

rules: []

fileTypeMappings: []
```

</bootstrap>

<hard_limits>

NEVER:
- Edit Swift source in `~/Documents/development/swift/browser-router/`. This skill is
  runtime config only.
- Invent fields outside the schema in the reference.
- Reuse an existing rule's UUID for a new rule.
- Run any `git` command. `~/Library/Application Support/` is not a repo.
- Edit `config.yaml` while the app is running.

</hard_limits>

<scripts>

Resolve `$SKILL_DIR` with:

```bash
SKILL_DIR="$(dirname "$(readlink -f ~/.claude/skills/browser-router/SKILL.md)")"
```

`scripts/app-control.sh` — app lifecycle wrapper:

```bash
bash "$SKILL_DIR/scripts/app-control.sh" quit       # quit if running, wait until gone
bash "$SKILL_DIR/scripts/app-control.sh" running    # exit 0 if running, 1 otherwise
bash "$SKILL_DIR/scripts/app-control.sh" relaunch   # open -a "Browser Router"
```

`scripts/list-rules.sh` — pretty-print current rules sorted by priority. Read-only.

```bash
bash "$SKILL_DIR/scripts/list-rules.sh"
```

</scripts>

<reporting>

After any write, report:
- One sentence summary: "Added rule: github.com → Arc (Work), priority 2."
- The affected YAML block (the new rule or the changed lines).
- Whether the app was relaunched.

Skip the YAML block for `list` and read-only ops.

</reporting>
