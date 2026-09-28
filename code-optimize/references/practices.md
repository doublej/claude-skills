# Practices — JJ's House Rules

The `practices` dimension checks a project against JJ's standing rules: atlas wiring,
the dev hostname, dev-tree paths, onenv, one package manager, nothing vendored in git,
daemons registered. `scan_practices.py` gives each finding a rule id, file:line and a
fix. The ratchet count is the number of findings.

```bash
python3 ~/.claude/skills/code-optimize/scripts/scan_practices.py <root> --json
```

Runs only on JJ's own repos. A foreign repo (atlas flow policy `external`, or a remote
owner other than `doublej`) skips this dimension.

<rules>

| Rule | Fix | Owner |
|---|---|---|
| `atlas.catalog` | `atlas scan`; still missing → `atlas init` | atlas-cli |
| `atlas.nested` | `depth` entry in `~/dev/.atlas-config.json`, then `atlas scan` | atlas-hostname step 1 |
| `atlas.port` | `curl -s localhost:47891/api/ports/allocate` → `.atlas` `port`, and pin it where the repo already pins ports | atlas-hostname step 2 |
| `atlas.bind` | `--host 0.0.0.0 --port <port>` in the dev script (Vite may use `server.host: true`); each listener in a fan-out wrapper | atlas-hostname step 3 |
| `atlas.allowed-hosts` | delete `allowedHosts`; Caddy already rewrites `Host` | atlas-hostname |
| `atlas.dev-line` | one CLAUDE.md line: `` Dev: `atlas run` → https://<slug>.atlas.local.jurrejan.com (port <N>). `` | atlas-hostname step 6 |
| `atlas.localhost-docs` | swap agent-facing `http://localhost:<port>` for the hostname; config, tests and health probes stay on localhost | atlas-hostname output rule |
| `paths.devtree` | repo-relative path or `$HOME/dev/...`; `~/Documents/development` is a dead symlink | ~/dev CLAUDE.md |
| `secrets.dotenv` | values into onenv (`onenv prime`), delete the file; a tracked one also gets `git rm --cached` and the user is told to rotate those secrets | global CLAUDE.md |
| `pm.lockfiles` | keep the lockfile of the manager the scripts use, delete the others | global CLAUDE.md |
| `pm.commands` | rewrite with the repo's manager (`bun run`/`bunx`, `uv add`/`uv run`) | global CLAUDE.md |
| `vendored.tracked` | `git rm -r --cached <dir>` and add it to `.gitignore` | — |
| `daemons.registry` | add the agent to `multi-stack/project-atlas/shared/daemons.json` | ~/dev CLAUDE.md |

Before an `atlas.*` fix, open the owning skill and name the step you are applying.
That skill has the mechanics; this file only maps rules to them.

</rules>

<limits>

- **Hostname registration costs two ACME certificates.** Don't register during FIX.
  Only the VERIFY smoke run registers one, once per run, and only after the slug is
  settled (atlas-hostname step 4).
- **Branch flow is not a practice finding.** Never run `atlas flow init` and never
  create `develop` as part of an optimize run. The ~/dev CLAUDE.md forbids that
  drive-by. Put the repo's flow policy in the summary, nothing more.
- **Ports inside a container or a deploy** (e.g. `strictPort` shared with a
  Dockerfile): moving the dev port can break the deploy. List these in the plan
  and let the user decide.
- **`secrets.dotenv` never prints values.** Name the file and the keys. Never
  copy a value into a commit message, the plan or the summary.

</limits>
