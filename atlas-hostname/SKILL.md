---
name: atlas-hostname
description: Make the current project reachable on its atlas dev hostname (https://SLUG.atlas.local.jurrejan.com) and switch the session to handing out that hostname instead of http://localhost:PORT. Use when a project's dev server should be opened from another device, when a hostname answers 502 or is missing, when "atlas run" prints lanReachable false, or when the user says "atlas hostname", "dev hostname", "make this reachable", "why does the .atlas.local URL 502", or "/atlas-hostname". Retrofit path for projects that lack .claude/rules/atlas.md (the cookiecutter atlas-rules branch is unmerged as of 2026-09-21, so that is every project today). NOT for the atlas CLI in general (atlas-cli skill), not for bulk registration.
---

<scope>
Two jobs, nothing else:
1. Make this project reachable on `https://<slug>.atlas.local.jurrejan.com` — check the four conditions, fix what fails, prove it with one request.
2. From then on, hand the user the hostname, never `http://localhost:<port>`.

Mechanics live in project-atlas (`atlas-api/src/lib/caddyDev.ts`, `ports.ts`, `scanner.ts`). CLI surface lives in the `atlas-cli` skill. Do not restate either here.
</scope>

<ground_truth>
- Hostname label is `atlas`: `<slug>.atlas.local.jurrejan.com` (LAN), `<slug>.atlas.remote.jurrejan.com` (WAN, basic auth unless `.atlas` has `devPublic: true`). project-atlas's own CLAUDE.md still says `.dev.`; it is stale.
- Only `atlas run`, the web console run buttons and `atlas hostnames assign` register a hostname (`ensureRoute`). Raycast run and `atlas jump --run` register nothing.
- `ensureRoute` writes `<slug>-atlas.caddy` to the NAS over SSH, reloads Caddy, records `~/dev/.atlas-hostnames.json`. No-op when slug, port and `devPublic` are unchanged. NAS unreachable → returns null, caller falls back to localhost, **no error raised**.
- Every registration costs two ACME certificates plus a Caddy reload. Register on demand only. Never loop over projects.
- Default slug is `slugify(<path relative to ~/dev>)`: `web/eink` → `web-eink`. `.atlas` `slug` overrides it.
- Caddy rewrites `Host` to `localhost` on the proxy hop, so Vite's host allowlist is already satisfied. Never add `allowedHosts`.
- HMR works over the hostname (verified 2026-09-21 on web/eink): Vite injects `hmrPort = null`, the browser opens `wss://<hostname>/` on the page origin, Caddy upgrades it (101). No `server.hmr` config needed.
</ground_truth>

<procedure>
Run in order. Each step: check → fix → evidence. Stop at the first step that says stop.

1. **Dev server exists?**
   `atlas info --json` → look at `devCommand`.
   Missing → say "no dev server, nothing to expose" and stop. Never invent a dev script for a CLI, library or native project.
   Failing with `No scanned project` → `atlas scan`, retry once. Still missing → the folder is not under `~/dev` or is archived; stop.

2. **Port in range.**
   Read `.atlas` `port`. Must be 4100–4999. Missing or outside (3000, 5173, 8000 are the usual offenders) →
   `curl -s localhost:47891/api/ports/allocate` → `{"port":N}`; write `"port": N` into `.atlas`; pin the same N where the project already pins ports (`package.json` dev script, Justfile recipe, uvicorn/flask args, Go `PORT` default).

3. **Bind address.**
   Read the dev script `atlas info` names.
   - Single command (`vite dev`, `next dev`, `uvicorn …`, `flask run`): `atlas run` injects `--host 0.0.0.0` and `--port`, but pin them in the script anyway so `bun run dev` / `just dev` behave the same. Vite may use `server.host: true` in `vite.config.*` instead.
   - Fan-out wrapper (`concurrently`, `turbo`, `npm-run-all`, `honcho`, `foreman`, `pm2`, `overmind`): atlas injects **nothing**. Every sub-command that listens needs its own `--host 0.0.0.0 --port <its port>`.
   Per-stack defaults: Vite family, uvicorn, flask → loopback only, fix needed. Next.js, node-api, Go `":"+port` → already all interfaces.

4. **Slug.**
   Print the hostname before registering: `https://<slug>.atlas.local.jurrejan.com`. Ugly or ambiguous slug → offer `"slug": "<short>"` in `.atlas` (it is slugified). Say plainly: moving or renaming the folder changes the slug and orphans the old NAS file; run `atlas hostnames rm` before a move.

5. **Register and verify.**
   Server should start → `atlas run` (stops the project's previous listeners, waits 60s for the bind, prints the hostname). No server wanted → `atlas hostnames assign`.
   Read the output, do not assume:
   - `lanReachable: false` / "binds localhost only" → step 3 was missed; fix and rerun.
   - "NAS push failed, not synced" (`nasSynced: false`) → NAS unreachable (off-LAN, VPN, NAS down); report it, hand out localhost as stated fallback.
   Then one real request:
   ```
   curl -sS -o /dev/null -w '%{http_code}\n' https://<slug>.atlas.local.jurrejan.com/
   ```
   200 → done. 502 → loopback bind, back to step 3. Anything else → report the code plus `tail -20 ~/dev/.atlas-logs/<slug>.log`.

6. **Record it.** One line in the project's CLAUDE.md:
   `Dev: \`atlas run\` → https://<slug>.atlas.local.jurrejan.com (port <N>).`
   Existing `.claude/rules/atlas.md` already covers the mechanics; the CLAUDE.md line only names this project's hostname and port.

Second run on the same project is a no-op: steps 1–4 pass, `atlas run` prints the hostname, `ensureRoute` short-circuits. Confirm `~/dev/.atlas-hostnames.json` mtime did not change if asked.
</procedure>

<output_rule>
Standing instruction for the rest of the session, not a step:

Once this project has a registered dev hostname, every URL you hand the user is the hostname. `http://localhost:<port>` is an internal detail: it appears in logs and config, never in a sentence addressed to the user.

Where it leaks:
- the sentence after starting a dev server
- "open http://localhost:… to see it"
- browser automation: `claude-in-chrome` navigates to the hostname
- screenshots and reports quoting the address bar

Exceptions, stated out loud when they apply:
- Not registered yet, or `nasSynced: false` → say that, then give localhost as the named fallback.
- `lanReachable: false` → fix the bind (step 3); do not quietly fall back.
- Machine-facing config stays on localhost: test runners, Playwright `baseURL`, health probes, `curl` inside scripts. TLS and the NAS hop buy nothing there.
- `atlas.remote` is password-gated and crosses the WAN. Offer it only when the user is off the LAN or `.atlas` has `devPublic: true`.
</output_rule>

<failure_modes>
Check these before reporting success; each has cost a debugging session.
- **Registered but 502** → loopback bind. The most common outcome. Always run the curl in step 5.
- **Registered, dead port** → an older dev server still holds the port and the new one moved to port+1. `atlas run` stops the project's own listeners first, including one started by hand in a terminal, but a launchd daemon on the same port respawns; `lsof -nP -iTCP:<port> -sTCP:LISTEN` tells which.
- **Stale registry path** → entries from before the `~/Documents/development` → `~/dev` move still carry the old path. Match `.atlas-hostnames.json` on slug, never on path.
- **Folder renamed** → new slug, new hostname, orphaned `<old-slug>-atlas.caddy` on the NAS. Nothing cleans it up. `atlas hostnames rm` before the move.
- **NAS unreachable** → no hostname, no error. Read `nasSynced` / the "not synced" line.
- **Host header** → already handled by Caddy. Do not add `allowedHosts`.
- **Started from a tool shell that exits** → a dev server launched under `timeout` or a subshell that ends can die with SIGTRAP. Launch it with `atlas run` from a shell that stays open, or `nohup … & disown`.
</failure_modes>

<non_goals>
- No bulk registration (certificate cost).
- No hand edits to the NAS Caddyfile or `etc/sites/`; `ensureRoute` owns them.
- No new config file, wrapper script or abstraction over `atlas run`.
- No restating the `atlas` CLI: see the `atlas-cli` skill and `.claude/rules/atlas.md` where present.
</non_goals>
