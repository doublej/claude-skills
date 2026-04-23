# SSH workspaces

`cmux ssh user@host` opens a workspace whose shells are remote. cmux still
exports `CMUX_SOCKET_PATH` into the session, so every script in this skill
works unchanged — the surfaces just happen to live on the remote host.

## Canonical invocation

```bash
cmux ssh jj@nas.local --workspace-name "nas:project-atlas"
```

Naming convention (**important**): always include the host in the
workspace name so remote workspaces don't collide with local ones.
Format: `<host-short>:<project>`. Examples:

- `nas:project-atlas`
- `buildbot:wallgen`
- `prod-1:atlas-api`

## Opening from a script

```bash
HOST=jj@nas.local
PROJECT=project-atlas
WS="${HOST%%@*}"          # strip user
WS="${WS%%.*}"            # strip domain → "nas"
WS="${WS}:${PROJECT}"

cmux ssh "$HOST" --workspace-name "$WS" --cwd "/srv/$PROJECT"
```

The helper scripts (`cmux-project.sh`, `cmux-tab.sh`, `cmux-send.sh`) do
not know or care that the workspace is remote. Once the SSH workspace
exists, you address it by name:

```bash
./scripts/cmux-tab.sh  "nas:project-atlas" logs /srv/project-atlas
./scripts/cmux-send.sh "nas:project-atlas" logs "journalctl -u atlas -f" --enter
```

## Socket forwarding caveats

cmux does NOT forward its unix socket over SSH. `CMUX_SOCKET_PATH` inside
the remote shell points to the remote cmux daemon if one is running, or
is unset otherwise. Two consequences:

1. **No nested cmux.** Running `cmux ssh` inside an SSH workspace opens
   a new top-level workspace on the *remote* cmux, not a sub-workspace.
2. **Helpers run locally.** Run `cmux-tab.sh` etc. from the Mac, not from
   inside the SSH shell. They drive the local cmux daemon that owns the
   SSH workspace's tab state.

If you need to run cmux helpers *from* the remote host, install this
skill remotely too and point `CMUX_SOCKET_PATH` at the remote daemon.

## Killing a stale SSH workspace

SSH sessions occasionally desync (host reboot, network drop). cmux keeps
the workspace around but every tab shows "(disconnected)". Clean up:

```bash
# Graceful: close the workspace, which closes every SSH channel
WS_ID=$(./scripts/cmux-find.sh "nas:project-atlas" | jq -r .workspace)
cmux close-workspace --workspace "$WS_ID"
```

Re-run `cmux ssh` to rebuild. If `close-workspace` hangs because a channel
is wedged, `cmux close-surface --surface <id> --force` on each tab first.

## Auth

`cmux ssh` uses the system ssh client, so `~/.ssh/config`, agent
forwarding (`ssh-add -l`), and `ProxyJump` all work. No cmux-specific
config. If a host prompts for password/2FA, cmux surfaces the prompt
in the first tab of the new workspace — answer it there.
