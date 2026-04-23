# CLI reference

Binary: `openclaw`. Every command group summarized below; fetch `docs/cli/<name>.md` for full flag detail.

## Install / bootstrap

```bash
curl -fsSL https://openclaw.ai/install.sh | bash          # macOS/Linux
iwr -useb https://openclaw.ai/install.ps1 | iex           # Windows PowerShell
npm install -g openclaw@latest                             # npm global
sudo npm i -g openclaw@latest                              # Linux with /usr/lib owned by root
```

Also: Docker, Nix (`openclaw/nix-openclaw`), and bun install flows.

## Top-level commands (from `docs/cli/`)

```
acp         agent         agents        approvals     backup
browser     channels      clawbot       completion    config
configure   cron          daemon        dashboard     devices
directory   dns           docs          doctor        flows
gateway     health        hooks         infer         logs
mcp         memory        message       models        node
nodes       onboard       pairing       plugins       qr
reset       sandbox       secrets       security      sessions
setup       skills        status        system        tui
uninstall   update        voicecall     webhooks      wiki
```

## Onboarding

```bash
openclaw onboard                            # interactive wizard
openclaw onboard --install-daemon           # wizard + launchd/systemd install
openclaw onboard --auth-choice openai-api-key
```

Wizard is the canonical setup path on macOS/Linux/Windows (WSL2 strongly recommended).

## Gateway

```bash
openclaw gateway status
openclaw gateway run --bind loopback --port 18789 --force
openclaw gateway restart
```

Foreground nohup pattern (VMs):
```bash
pkill -9 -f openclaw-gateway || true
nohup openclaw gateway run --bind loopback --port 18789 --force > /tmp/openclaw-gateway.log 2>&1 &
```

## Doctor

```bash
openclaw doctor              # diagnostics
openclaw doctor --fix        # apply repairs (legacy config migrations, config drift)
```

Doctor owns extension-specific legacy repairs — prefer it over writing startup-time migrations in core.

## Skills (from `docs/cli/skills.md`)

```bash
openclaw skills search "calendar"
openclaw skills search --limit 20 --json
openclaw skills install <slug>
openclaw skills install <slug> --version <version>
openclaw skills install <slug> --force
openclaw skills update <slug>
openclaw skills update --all
openclaw skills list                 # default action if no subcommand
openclaw skills list --eligible
openclaw skills list --json
openclaw skills list --verbose
openclaw skills info <name>
openclaw skills info <name> --json
openclaw skills check                # debug missing bins/env/config
openclaw skills check --json
```

- `search`/`install`/`update` hit **ClawHub directly** and install into the active workspace `skills/` directory.
- `list`/`info`/`check` inspect local skills visible to the current workspace + config.
- CLI `install` downloads skill folders from ClawHub. Gateway-backed skill dependency installs (from onboarding or Skills settings) use the separate `skills.install` request path.

## Plugins (from `docs/cli/plugins.md`)

```bash
openclaw plugins list [--enabled] [--verbose] [--json]
openclaw plugins install <pkg>                             # ClawHub first, then npm
openclaw plugins install clawhub:<pkg>                     # force ClawHub
openclaw plugins install <pkg>@1.2.3                       # exact version
openclaw plugins install <pkg> --pin                       # pin (npm only)
openclaw plugins install <pkg> --force                     # overwrite existing
openclaw plugins install <path>                            # local archive or dir
openclaw plugins install -l <path>                         # --link (adds to plugins.load.paths)
openclaw plugins install <plugin>@<marketplace>            # Claude marketplace shorthand
openclaw plugins install <plugin> --marketplace <name-or-url>
openclaw plugins install <pkg> --dangerously-force-unsafe-install
openclaw plugins inspect <id> [--json] [--all]
openclaw plugins info <id>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins uninstall <id>
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins doctor
openclaw plugins marketplace list <marketplace> [--json]
```

Install notes:
- Bare specs checked against ClawHub before npm.
- Supported archives: `.zip`, `.tgz`, `.tar.gz`, `.tar`.
- npm specs are **registry-only** — no git/URL/file specs or semver ranges. Dependency installs run with `--ignore-scripts`.
- Bare spec + `@latest` stay on stable track. Prerelease resolution → explicit `@beta`/`@rc` or `@x.y.z-beta.N`.
- If a bare spec matches a bundled plugin id (e.g. `diffs`), OpenClaw installs the bundled plugin. Use scoped spec `@scope/name` to install an npm package with the same name.
- `plugins install` is **also** the install surface for hook packs that expose `openclaw.hooks` in `package.json`. Use `openclaw hooks` for per-hook enablement.

## Channels

```bash
openclaw channels status --probe           # probe all channels for health
```

Per-channel docs in `docs/channels/<channel>.md`.

## Config

```bash
openclaw config set <key> <value>
openclaw config set gateway.mode local
```

Environment overrides:
- `OPENCLAW_HOME` — home dir for internal path resolution
- `OPENCLAW_STATE_DIR` — override state dir
- `OPENCLAW_CONFIG_PATH` — override config file path

## Dashboard

```bash
openclaw dashboard     # opens Control UI in browser; static assets served by Gateway
```

Custom Control UI build:
```json
{
  "gateway": {
    "controlUi": { "enabled": true, "root": "$HOME/.openclaw/control-ui-custom" }
  }
}
```

## Development commands (from repo `AGENTS.md`)

For hacking on `openclaw/openclaw` itself:
```bash
pnpm install
pnpm openclaw ...          # run CLI in dev (bun)
pnpm dev                   # dev loop
pnpm build                 # type-check + build
pnpm tsgo                  # TypeScript checks
pnpm check                 # lint/format (default local gate)
pnpm test                  # vitest full suite (default landing gate on main)
pnpm format                # oxfmt --check
pnpm format:fix            # oxfmt --write
pnpm config:docs:gen       # regen config schema docs + hash
pnpm config:docs:check     # drift check
pnpm plugin-sdk:api:gen    # regen plugin SDK API surface
pnpm plugin-sdk:api:check  # drift check
```

Fast-commit mode: `FAST_COMMIT=1 git commit …` skips repo-wide `pnpm format`/`pnpm check` in the pre-commit hook only. Use only when covering the touched surface separately.
