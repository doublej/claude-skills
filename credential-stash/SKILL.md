---
name: credential-stash
description: Find credentials that were created, found, or pasted during this Claude Code session (passwords, API keys, tokens, user:pass URLs) and move them into 1Password as Login / API Credential items with the right website URL so autofill triggers, or into onenv when they are project env vars. Use when the user says "stash credentials", "save that to 1password", "move creds to 1password", "/credential-stash", or after a session that generated or exposed any secret.
allowed-tools:
  - Bash
---

<overview>
Scans the session transcript (`~/.claude/projects/<cwd>/<session>.jsonl`) for credential-shaped strings, then files each one in 1Password through `op item create` with a JSON template on stdin. The secret never lands on a command line or in shell history. Env-var style keys for a project go to `onenv` instead.

Script: `python3 ~/.claude/skills/credential-stash/scripts/stash.py`
</overview>

<workflow>
1. **Scan** the current session (default `$CLAUDE_CODE_SESSION_ID`):
   ```bash
   python3 ~/.claude/skills/credential-stash/scripts/stash.py scan
   # wider net: everything for this project in the last 24h
   python3 ~/.claude/skills/credential-stash/scripts/stash.py scan --all-recent --since 24
   ```
   Output is masked JSON plus a `findings_file` (chmod 600) holding full values. Never `cat` that file.

2. **Triage** the findings. Drop placeholders, test fixtures, values already in 1Password (`op item list --vault X | grep -i <title>`), and duplicates. For each keeper decide:
   - **Login** — has a username and/or a site: needs `--url` (the page where 1Password should autofill, e.g. `https://app.example.com/login`) and `--username`.
   - **API Credential** — bare key/token: needs `--url` of the console it was issued from when known.
   - **onenv** — a `KEY=value` the project reads from env: `--onenv <namespace> <KEY>` (namespace = project name, see `onenv list`).
   Pick the account: `pimpelmees.1password.com` for Pimpelmees / client work, `my.1password.com` for personal. Vault default `Private`; run `op vault list --account <acct>` if unsure.

3. **Stash** each keeper by id:
   ```bash
   S="python3 ~/.claude/skills/credential-stash/scripts/stash.py"
   $S stash c1 --title "Directus haist admin" --url https://cms.haist.nl/admin/login --username admin --vault Private --account pimpelmees.1password.com
   $S stash c2 --title "Porkbun API" --category "API Credential" --url https://porkbun.com/account/api
   $S stash c3 --onenv porkbun PORKBUN_SECRET_KEY
   ```
   Each call prints the created item id, vault, and URL. `op` may open a biometric prompt; if it reports `authorization prompt dismissed`, rerun once.

4. **Clean the source.** If the credential also lives in a plaintext file the session wrote (`.env`, a script, a note), replace it with an `op://<vault>/<title>/<field>` reference or an `onenv` lookup and say which file changed. Transcripts are left alone.

5. **Report**: one line per item: title, category, vault, URL, and where the plaintext was removed. Delete the findings file: `rm "$TMPDIR/credential-stash.json"`.
</workflow>

<rules>
- Never echo a full secret into the reply or a command argument; the script exists so `op` reads it from stdin.
- Confirm with the user before stashing when a finding's owner or URL is ambiguous. Wrong-vault items are worse than a delayed one.
- Title format: `<service> <role or account>` (e.g. `Cloudflare pimpelmees API token`), so `op item get "<title>"` is unambiguous later.
- Tag `credential-stash` is set automatically; use it to audit what this skill created: `op item list --tags credential-stash`.
- Add a regex to `PATTERNS` in the script when a real credential format slips through the scan.
</rules>
