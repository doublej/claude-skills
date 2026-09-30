---
name: credential-stash
description: Find credentials that were created, found, or pasted during this Claude Code session (passwords, API keys, tokens, user:pass URLs) and move them into 1Password as Login / API Credential items with the right website URL so autofill triggers, or into onenv when they are project env vars. Use when the user says "stash credentials", "save that to 1password", "move creds to 1password", "/credential-stash", or after a session that generated or exposed any secret.
allowed-tools:
  - Bash
---

<goal>
Save JJ the copy-paste. Every login the session produced or touched that JJ will type into a form should end up in 1Password with the URL of that form, so 1Password autofills it. **Secrecy is not the bar; convenience is.** Demo accounts, seeded local-dev users, staging logins, and passwords committed in a README are all in scope — those are exactly the ones JJ pastes by hand every time. Only skip a finding when nobody will ever log in with it.
</goal>

<overview>
Scans the session transcript (`~/.claude/projects/<cwd>/<session>.jsonl`) for credential-shaped strings, then files each one in 1Password through `op item create` with a JSON template on stdin. The secret never lands on a command line or in shell history. Env-var style keys for a project go to `onenv` instead.

Script: `python3 ~/.claude/skills/credential-stash/scripts/stash.py`
</overview>

<presentation>
Open the first response with the banner (once); step 5 closes the run with the report.
Never put a secret in either: titles, masked ids, and URLs only.
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   CREDENTIAL STASH                                           ║
║   Session credentials into 1Password and onenv               ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

CREDENTIAL STASH  ──  <session|last <n>h>   found: <n>   stashed: <n>

TITLE                 CATEGORY          VAULT               URL            PLAINTEXT
─────────────────────────────────────────────────────────────────────────────────────
<service role>        <Login|API Cred>  <Private|onenv:ns>  <url|—>        <removed: file|kept: demo|—>

github.com/doublej
```
</presentation>

<workflow>
1. **Scan** the current session (default `$CLAUDE_CODE_SESSION_ID`):
   ```bash
   python3 ~/.claude/skills/credential-stash/scripts/stash.py scan
   # wider net: everything for this project in the last 24h
   python3 ~/.claude/skills/credential-stash/scripts/stash.py scan --all-recent --since 24
   ```
   Output is masked JSON plus a `findings_file` (chmod 600) holding full values. Never `cat` that file.

2. **Triage** the findings. Drop only placeholders (`<your-token>`), duplicates, and values already in 1Password (`op item list --vault X | grep -i <title>`). Keep demo/seed/local logins (see goal). Then add what the scan missed: check every file the session wrote or read for logins (seed scripts, README "log in with" lines, fixtures, `.env`), e.g. `git grep -inE "password|passwd|login with|secret"`; a credential you already know can be stashed without a scan hit using `stash -` (secret on stdin). For each keeper decide:
   - **Login** — has a username and/or a site: needs `--url` (the exact page where 1Password should autofill, e.g. `https://app.example.com/login`, or `http://localhost:8787/login` for local dev; 1Password matches localhost fine) and `--username`.
   - **API Credential** — bare key/token: needs `--url` of the console it was issued from when known.
   - **onenv** — a `KEY=value` the project reads from env: `--onenv <namespace> <KEY>` (namespace = project name, see `onenv list`).
   Account and vault: always the personal account (`my.1password.com`, vault `Private`) unless JJ names another account or vault. Do not infer `pimpelmees.1password.com` from the project.

3. **Stash** each keeper by id:
   ```bash
   S="python3 ~/.claude/skills/credential-stash/scripts/stash.py"
   $S stash c1 --title "Directus haist admin" --url https://cms.haist.nl/admin/login --username admin
   $S stash c2 --title "Porkbun API" --category "API Credential" --url https://porkbun.com/account/api
   $S stash c3 --onenv porkbun PORKBUN_SECRET_KEY
   # scan missed it but you know it (e.g. from a seed script): read the secret from stdin
   grep -o 'demo-[a-z0-9-]*' scripts/seed.ts | head -1 | $S stash - --title "Afzender demo login (local)" --url http://localhost:8787/login --username demo@afzender.nl
   ```
   Each call prints the created item id, vault, and URL. `op` may open a biometric prompt; if it reports `authorization prompt dismissed`, rerun once.

4. **Clean the source** only for real secrets. If a production/API credential also lives in a plaintext file the session wrote (`.env`, a script, a note), replace it with an `op://<vault>/<title>/<field>` reference or an `onenv` lookup and say which file changed. Demo/seed passwords stay where they are (the app needs them); transcripts are left alone.

5. **Report** with the `<presentation>` report: one row per item: title, category, vault, URL, and where the plaintext was removed. Delete the findings file: `rm "$TMPDIR/credential-stash.json"`.
</workflow>

<rules>
- Never echo a full secret into the reply or a command argument; the script exists so `op` reads it from stdin.
- Confirm with the user before stashing when a finding's owner or URL is ambiguous. Vault choice is never the ambiguity: personal `Private` unless told otherwise.
- Do not talk yourself out of a login because it is "just a demo" or "public anyway". If JJ would paste it into a form, stash it. Mention the demo nature in `--notes` instead.
- An empty scan is not "nothing to stash". Step 2's file review is mandatory before reporting nothing.
- Title format: `<service> <role or account>` (e.g. `Cloudflare pimpelmees API token`), so `op item get "<title>"` is unambiguous later.
- Tag `credential-stash` is set automatically; use it to audit what this skill created: `op item list --tags credential-stash`.
- Add a regex to `PATTERNS` in the script when a real credential format slips through the scan.
</rules>
