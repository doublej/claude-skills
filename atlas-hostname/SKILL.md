---
name: atlas-hostname
description: Make the current project reachable on its atlas dev hostname (https://SLUG.atlas.local.jurrejan.com) and switch the session to handing out that hostname instead of http://localhost:PORT. Use when a project's dev server should be opened from another device, when a hostname answers 502 or is missing, when "atlas run" prints lanReachable false, or when the user says "atlas hostname", "dev hostname", "make this reachable", "why does the .atlas.local URL 502", or "/atlas-hostname". Retrofit path for projects that lack .claude/rules/atlas.md (the cookiecutter atlas-rules branch is unmerged as of 2026-09-21, so that is every project today). NOT for the atlas CLI in general (atlas-cli skill), not for bulk registration.
---

<scope>
Two jobs, nothing else:
1. Make this project reachable on `https://<slug>.atlas.local.jurrejan.com` — check the four conditions, fix what fails, prove it with one request.
2. From then on, hand the user the hostname, never `http://localhost:<port>`.

Routes reach servers on **this Mac** only. Out of scope: a server on another machine (WSL, Fractal: hand out that machine's address; a temporary `ssh -N -g -L <port>:127.0.0.1:<port> <host>` makes the hostname work while it lives, then skip step 6), a scratch server outside the catalog (`/tmp/…`), and borrowing a registered project's port or hostname for unrelated content (it blocks that project's dev server). The Stop hook `~/.claude/hooks/atlas-localhost-guard.py` loads this skill whenever a reply names localhost inside an atlas project; when that localhost URL is one of these cases, say so in one line and stop.

Mechanics live in project-atlas (`atlas-api/src/lib/caddyDev.ts`, `ports.ts`, `scanner.ts`). CLI surface lives in the `atlas-cli` skill. Do not restate either here.
</scope>

<presentation>
Print this banner as plain text in your first reply, before any tool call; close the run with the report (hostname, never localhost; a failure's cause goes on one line under the table). A field the run never reached (stopped before step 5) shows `—`, never `not synced`.
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
ATLAS HOSTNAME  ──  https://<slug>.atlas.local.jurrejan.com   port: <N|—>   nas: <synced|not synced|—>   claude.md: <✓|—>

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
- `ensureRoute` writes `<slug>-atlas.caddy` to the NAS over SSH, reloads Caddy, records `~/dev/.atlas-hostnames.json`. No-op when slug, port and `devPublic` are unchanged. NAS unreachable → the row stays `nasSynced: false` with a retry (console pill, `atlas hostnames doctor --fix`), caller falls back to localhost. A slug another project or a service holds → 409 naming the holder; `atlas hostnames check <slug>` asks first.
- Every registration reloads the shared NAS Caddy. Since 2026-10-01 a DNS-01 wildcard (`sites/atlas-wildcard.caddy`) covers `*.atlas.local` / `*.atlas.remote`, so no new certificate — but still register on demand only and never loop over projects.
- Default slug is `slugify(<path relative to ~/dev>)`: `web/eink` → `web-eink`. `.atlas` `slug` overrides it.
- Caddy rewrites `Host` to `localhost` on the proxy hop, so Vite's host allowlist is already satisfied. Never add `allowedHosts`.
- HMR works over the hostname (verified 2026-09-21 on web/eink): Vite injects `hmrPort = null`, the browser opens `wss://<hostname>/` on the page origin, Caddy upgrades it (101). No `server.hmr` config needed.
</ground_truth>

<procedure>
Run in order. Each step: check → fix → evidence. Stop at the first step that says stop.

Target is the project the user means, not necessarily the cwd: `atlas info`, `atlas run` and `atlas hostnames assign` all take a path.
Already registered (`atlas hostnames --json` has its slug, `nasSynced: true`) → steps 1–4 only confirm; never rename its slug unprompted (it moves the route), mention `atlas set slug` as an option. Go to step 5's `lsof` + curl; `ensureRoute` short-circuits, so `~/dev/.atlas-hostnames.json` mtime stays put.

1. **Something serves a browser?**
   `atlas info --json` → `devCommand`, `justRecipes`, `runner`, `type`. The scanner only reads `package.json` `dev`/`start`/`serve`, so a missing `devCommand` proves nothing on its own:
   - `devCommand` set, and not `build` → continue.
   - No `devCommand`, but something does serve (a `dev`/`serve` just recipe, a uv/uvicorn app, a command the project's CLAUDE.md names) → continue; in step 5 start it yourself and register with `atlas hostnames assign`. `atlas run` refuses without a `devCommand`, and `.atlas` has no override for it.
   - Workspace root (`type: workspace`, children with their own `.atlas`) → the child that serves is the target; see nested project below.
   - Permanent service (`atlas services --json` lists it) → it already has its hostname; run step 5's curl on it and report that. This skill registers nothing for it.
   - Nothing listens: CLI, library, native (`swift`, `dotnet`, `bepinex` in `type`), `devCommand: build` → say "no dev server, nothing to expose" and stop. Never invent a dev script.
   `No scanned project` / "not in the cached scan" → `atlas scan`, retry once. Still missing → the folder is outside the catalog: not under `~/dev`, archived, hidden (`.claude/worktrees/…`) or matched by an `ignore` glob in `~/dev/.atlas-config.json`. Atlas cannot route it: serve the branch from the registered checkout, or stop.
   **Nested project** (`api/` + `ui/` under one root, the normal `multi-stack/` shape): the scan stops at the parent's `.atlas`. `atlas run` in the child exits 1 and prints the exact fix: a `depth` entry in `~/dev/.atlas-config.json`, then `atlas scan`. Do what it says, then `atlas info --json` from the child. Each child that serves a browser or an API gets its own port and its own hostname; two registrations are the price, not a mistake.

2. **Port in range.**
   Read `.atlas` `port`. Must be 4100–4999, and it must be the port a **browser** opens. A root `.atlas` in a multi-stack project often carries the API port; the UI is a separate child (step 1). Missing or outside (3000, 5173, 8000 are the usual offenders) →
   `curl -s localhost:47891/api/ports/allocate` → `{"port":N}`; write `"port": N` into `.atlas` (no `.atlas` yet → create it as a JSON object holding only the fields you set); pin the same N where the project already pins ports (`package.json` dev script, Justfile recipe, uvicorn/flask args, Go `PORT` default).

3. **Bind address.**
   Read the dev script `atlas info` names.
   - Single command (`vite dev`, `next dev`, `uvicorn …`, `flask run`): `atlas run` injects `--host 0.0.0.0` and `--port`, but pin them in the script anyway so `bun run dev` / `just dev` behave the same. Vite may use `server.host: true` in `vite.config.*` instead.
   - Fan-out wrapper (`concurrently`, `turbo`, `npm-run-all`, `honcho`, `foreman`, `pm2`, `overmind`): atlas injects **nothing**. Every sub-command that listens needs its own `--host 0.0.0.0 --port <its port>`.
   Per-stack defaults: Vite family (`[::1]`), uvicorn, flask (`127.0.0.1`) → loopback only: atlas routes it through its NAS-only bridge, which reaches either family, so it works (`atlas run` prints a note). `atlas run` settles on a lone loopback port after ~10s, but waits the full 60s for a LAN bind while the command holds several (wrangler + its inspector). Binding all interfaces stays the direct route. Next.js, node-api, Go `":"+port` → already all interfaces.

4. **Slug — settle it before the first registration.**
   Ugly or ambiguous default → write `"slug": "<short>"` into `.atlas` (it is slugified). `atlas run` and `atlas hostnames assign` re-read `.atlas` right before registering, so no rescan is needed; still print the hostname you expect before running either. `atlas hostnames check <slug>` says free · taken by … · invalid; a wrong slug is fixed with `atlas set slug <new>` (or the console's settings dialog), which moves the route.
   Print the hostname: `https://<slug>.atlas.local.jurrejan.com`. Say plainly: renaming or moving the folder through atlas (console, `/api/rename`, `/api/move`) moves or keeps the route; a move outside atlas leaves the old route behind until `atlas hostnames doctor --fix` releases it.

5. **Register and verify.**
   Server should start → `atlas run` (the daemon spawns it detached, stops the project's previous listeners, waits 60s for the bind, prints the hostname; works from an agent tool shell). No server wanted, or one `atlas run` cannot start (step 1) → `atlas hostnames assign` (bare = current folder). `atlas run` writes the port the server really bound back into `.atlas` (a taken port pushes it to N+1), so re-read `.atlas` before trusting N. Then `lsof -nP -iTCP:<port> -sTCP:LISTEN`: the listener must exist before curling, so a dead server and a loopback bind stay distinguishable.
   Registration is a Caddy route to a port. It survives the server dying; a 502 later means the port is empty or loopback-bound, never "re-register".
   Read the output, do not assume:
   - `lanReachable: false` / "binds localhost only" → the hostname goes through atlas's bridge; it works, and step 3 gives the direct route.
   - "NAS push failed, not synced" (`nasSynced: false`) → NAS unreachable (off-LAN, VPN, NAS down); report it, hand out localhost as stated fallback, retry later (`atlas hostnames doctor --fix`).
   Then one real request:
   ```
   curl -sS -o /dev/null -w '%{http_code}\n' https://<slug>.atlas.local.jurrejan.com/
   ```
   200 → GET passes. 502 with a loopback-only listener → the bridge is not up yet: the service sync bridges every routed port within 60s, whoever started the server; `atlas services sync` does it now. Still 502 → `atlas hostnames assign --json` re-bridges and names the failure in `error`; step 3 skips the bridge. 502 without a listener → server died, read the log. `000` → curl never reached Caddy (DNS, NAS down, off-LAN); `nasSynced` records the last push, not reachability now. Anything else → report the code plus `tail -20 ~/dev/.atlas-logs/<slug>.log`.
   **A 200 is not done when the app talks to anything else.** Caddy rewrites `Host` but not `Origin`, and a browser on another device is not this Mac:
   - Own origin allowlist (better-auth `trustedOrigins`, Auth.js, Django `CSRF_TRUSTED_ORIGINS`, Rails `config.hosts`, Sanctum stateful domains; SvelteKit's `csrf.checkOrigin` is fine under `vite dev`, but an adapter-node build needs `ORIGIN=https://<slug>.atlas.local.jurrejan.com` in its environment): POST once with `-X POST -H 'Origin: https://<slug>.atlas.local.jurrejan.com'` to an auth endpoint. 403 / `INVALID_ORIGIN` → add the hostname to that list.
   - Separate backend: the frontend's baked API base must be the API's hostname, not `127.0.0.1:<port>` (on a phone that is the phone). `curl -sS https://<ui>/ | grep -o '<api-host>'` shows what is baked; `curl -sS -i -X OPTIONS https://<api>/<route> -H 'Origin: https://<ui>' | grep -i allow-origin` shows whether CORS admits it. Put the hostname in `.env.development`, never `.env`; `vite build` reads `.env` and ships it.

6. **Record it.** One line in the project's CLAUDE.md:
   `Dev: \`atlas run\` → https://<slug>.atlas.local.jurrejan.com (port <N>).`
   Existing `.claude/rules/atlas.md` already covers the mechanics; the CLAUDE.md line only names this project's hostname and port. A `just dev` / dev script that starts servers without printing an address can `echo` the hostname too.
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
- `lanReachable: false` → bridged; say so, and fix the bind (step 3) when you touch the dev config anyway.
- Machine-facing config stays on localhost: test runners, Playwright `baseURL`, health probes, `curl` inside scripts. TLS and the NAS hop buy nothing there.
- `atlas.remote` is password-gated and crosses the WAN. Offer it only when the user is off the LAN or `.atlas` has `devPublic: true`.
</output_rule>

<failure_modes>
Check these before reporting success; each has cost a debugging session.
- **Registered but 502** → nothing listens, a loopback bind the 60s service sync has not bridged yet (`atlas services sync`), or a bridge that failed (`atlas hostnames assign --json` → `error`). Always run the curl in step 5.
- **Registered, dead port** → an older dev server still holds the port and the new one moved to port+1. `atlas run` stops the project's own listeners first, including one started by hand in a terminal, but a launchd daemon on the same port respawns; `lsof -nP -iTCP:<port> -sTCP:LISTEN` tells which.
- **Stale registry path** → registry paths are normalised to the `~/dev` realpath (the `~/Documents/development` rows were migrated 2026-10-01); `atlas hostnames doctor` reports any `stale-path` row.
- **Folder renamed** → through atlas (console rename/move, `/api/rename`, `/api/move`) the route follows: same slug keeps it, a new slug moves it (`moveRoute`). Renamed outside atlas → the old `<old-slug>-atlas.caddy` stays until `atlas hostnames doctor` lists it and `--fix` releases it.
- **NAS unreachable** → the row stays `nasSynced: false` and shows a retry in the settings dialog and the doctor. Read `nasSynced` / the "not synced" line.
- **Host header** → already handled by Caddy. Do not add `allowedHosts`.
- **Vite dies with SIGTRAP on the first request** → `bun run dev` ran Vite under Bun because `node` was not on the daemon's PATH (fixed 2026-09-21 in the atlas-api launchd plist). Binds first, dies on request one, so `lsof` right after the bind passes. `lsof` output naming `bun` instead of `node` on the port is the tell.
- **UI hostname 200, app dead** → API base or CORS still points at localhost. Step 5's second check.
</failure_modes>

<non_goals>
- No bulk registration (each push reloads the shared NAS Caddy; without the wildcard file every name costs two certificates again).
- No hand edits to the NAS Caddyfile or `etc/sites/`; `ensureRoute` owns them.
- No new config file, wrapper script or abstraction over `atlas run`.
- No restating the `atlas` CLI: see the `atlas-cli` skill and `.claude/rules/atlas.md` where present.
</non_goals>
