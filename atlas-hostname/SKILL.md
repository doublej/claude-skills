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

<presentation>
Print this banner once, first; close the run with the report (hostname, never localhost; a failure's cause goes on one line under the table).
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ATLAS HOSTNAME                                             ║
║   Expose a dev server on its atlas LAN hostname              ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
```
ATLAS HOSTNAME  ──  https://<slug>.atlas.local.jurrejan.com   port: <N>   nas: <synced|not synced>   claude.md: <✓|—>

STEP                 RESULT   DETAIL
────────────────────────────────────────────────────────────
dev server           <✓|✗>    <devCommand|none: stopped>
port · bind          <✓|✗>    <N> on 0.0.0.0 (<unchanged|was <old>>)
GET hostname         <✓|✗>    <http code>
origin · API base    <✓|✗|—>  <POST/CORS result|n/a>

github.com/doublej
```
</presentation>

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
   **Nested project** (`api/` + `ui/` under one root, the normal `multi-stack/` shape): the scan stops at the parent's `.atlas`. `atlas run` in the child exits 1 and prints the exact fix: a `depth` entry in `~/dev/.atlas-config.json`, then `atlas scan`. Do what it says, then `atlas info --json` from the child. Each child that serves a browser or an API gets its own port and its own hostname; two registrations are the price, not a mistake.

2. **Port in range.**
   Read `.atlas` `port`. Must be 4100–4999, and it must be the port a **browser** opens. A root `.atlas` in a multi-stack project often carries the API port; the UI is a separate child (step 1). Missing or outside (3000, 5173, 8000 are the usual offenders) →
   `curl -s localhost:47891/api/ports/allocate` → `{"port":N}`; write `"port": N` into `.atlas`; pin the same N where the project already pins ports (`package.json` dev script, Justfile recipe, uvicorn/flask args, Go `PORT` default).

3. **Bind address.**
   Read the dev script `atlas info` names.
   - Single command (`vite dev`, `next dev`, `uvicorn …`, `flask run`): `atlas run` injects `--host 0.0.0.0` and `--port`, but pin them in the script anyway so `bun run dev` / `just dev` behave the same. Vite may use `server.host: true` in `vite.config.*` instead.
   - Fan-out wrapper (`concurrently`, `turbo`, `npm-run-all`, `honcho`, `foreman`, `pm2`, `overmind`): atlas injects **nothing**. Every sub-command that listens needs its own `--host 0.0.0.0 --port <its port>`.
   Per-stack defaults: Vite family, uvicorn, flask → loopback only, fix needed. Next.js, node-api, Go `":"+port` → already all interfaces.

4. **Slug — settle it before the first registration.**
   Ugly or ambiguous default → write `"slug": "<short>"` into `.atlas` (it is slugified). `atlas run` and `atlas hostnames assign` re-read `.atlas` right before registering, so no rescan is needed; still print the hostname you expect before running either, because a wrong slug costs two certificates to register and two more to fix (`atlas hostnames rm`, re-register).
   Print the hostname: `https://<slug>.atlas.local.jurrejan.com`. Say plainly: moving or renaming the folder changes the slug and orphans the old NAS file; run `atlas hostnames rm` (bare: current folder) before a move.

5. **Register and verify.**
   Server should start → `atlas run` (the daemon spawns it detached, stops the project's previous listeners, waits 60s for the bind, prints the hostname; works from an agent tool shell). No server wanted → `atlas hostnames assign` (bare = current folder). Then `lsof -nP -iTCP:<port> -sTCP:LISTEN`: the listener must exist before curling, so a dead server and a loopback bind stay distinguishable.
   Registration is a Caddy route to a port. It survives the server dying; a 502 later means the port is empty or loopback-bound, never "re-register".
   Read the output, do not assume:
   - `lanReachable: false` / "binds localhost only" → step 3 was missed; fix and rerun.
   - "NAS push failed, not synced" (`nasSynced: false`) → NAS unreachable (off-LAN, VPN, NAS down); report it, hand out localhost as stated fallback.
   Then one real request:
   ```
   curl -sS -o /dev/null -w '%{http_code}\n' https://<slug>.atlas.local.jurrejan.com/
   ```
   200 → GET passes. 502 with a listener → loopback bind, back to step 3. 502 without a listener → server died, read the log. Anything else → report the code plus `tail -20 ~/dev/.atlas-logs/<slug>.log`.
   **A 200 is not done when the app talks to anything else.** Caddy rewrites `Host` but not `Origin`, and a browser on another device is not this Mac:
   - Own origin allowlist (better-auth `trustedOrigins`, Auth.js, Django `CSRF_TRUSTED_ORIGINS`, Rails `config.hosts`, Sanctum stateful domains; SvelteKit's `csrf.checkOrigin` is fine): POST once with `-X POST -H 'Origin: https://<slug>.atlas.local.jurrejan.com'` to an auth endpoint. 403 / `INVALID_ORIGIN` → add the hostname to that list.
   - Separate backend: the frontend's baked API base must be the API's hostname, not `127.0.0.1:<port>` (on a phone that is the phone). `curl -sS https://<ui>/ | grep -o '<api-host>'` shows what is baked; `curl -sS -i -X OPTIONS https://<api>/<route> -H 'Origin: https://<ui>' | grep -i allow-origin` shows whether CORS admits it. Put the hostname in `.env.development`, never `.env`; `vite build` reads `.env` and ships it.

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
- **Vite dies with SIGTRAP on the first request** → `bun run dev` ran Vite under Bun because `node` was not on the daemon's PATH (fixed 2026-09-21 in the atlas-api launchd plist). Binds first, dies on request one, so `lsof` right after the bind passes. `lsof` output naming `bun` instead of `node` on the port is the tell.
- **UI hostname 200, app dead** → API base or CORS still points at localhost. Step 5's second check.
</failure_modes>

<non_goals>
- No bulk registration (certificate cost).
- No hand edits to the NAS Caddyfile or `etc/sites/`; `ensureRoute` owns them.
- No new config file, wrapper script or abstraction over `atlas run`.
- No restating the `atlas` CLI: see the `atlas-cli` skill and `.claude/rules/atlas.md` where present.
</non_goals>
