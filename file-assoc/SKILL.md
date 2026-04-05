---
name: file-assoc
description: "Change or check default application for file extensions on macOS"
---

Change default file extension associations on macOS using `duti` and LaunchServices.

## Workflow

1. Ask the user for the file extension and desired application name (use consult-user-mcp if available)
2. Run the bundled script to make the change

## Script

`scripts/file-assoc.sh` handles all operations. Auto-installs `duti` via Homebrew if missing.

```bash
SKILL_DIR="$(dirname "$(readlink -f ~/.claude/skills/file-assoc/SKILL.md)")"

# Set default app for an extension
bash "$SKILL_DIR/scripts/file-assoc.sh" set <extension> "<App Name>"

# Check current default
bash "$SKILL_DIR/scripts/file-assoc.sh" get <extension>

# List all registered apps for an extension
bash "$SKILL_DIR/scripts/file-assoc.sh" list <extension>

# Look up UTI for an extension
bash "$SKILL_DIR/scripts/file-assoc.sh" uti <extension>

# Look up bundle ID for an app
bash "$SKILL_DIR/scripts/file-assoc.sh" id "<App Name>"
```

## Examples

```bash
# Open .md files in Zed
bash "$SKILL_DIR/scripts/file-assoc.sh" set md "Zed"

# Open .pdf files in Preview
bash "$SKILL_DIR/scripts/file-assoc.sh" set pdf "Preview"

# Check what opens .json files
bash "$SKILL_DIR/scripts/file-assoc.sh" get json
```

## Notes

- App names are case-sensitive and must match the name in `/Applications` (without `.app`)
- The `.` prefix on extensions is optional — both `md` and `.md` work
- Uses `duti -s <bundle-id> .<ext> all` under the hood (sets for all roles: viewer, editor, shell)
- UTI lookup for `.ts` returns MPEG-2 transport stream, not TypeScript — the script uses extension-based binding (`.ts`) to avoid this
