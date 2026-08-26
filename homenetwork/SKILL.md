---
name: homenetwork
description: "SSH access and admin for JJ home network: M2 Pro, Ubuntu, QNAP, PCs"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Home Network Skill

Work with the machines on the JJ home network (`192.168.178.0/24`).

## When to Use

- SSH into a home network machine
- Check or manage services on a machine
- Deploy or configure software on network hosts
- Troubleshoot connectivity or services
- Look up machine specs, IPs, or ports

## Documentation

Full network documentation lives at:
`/Users/jurrejan/Documents/development/_management/homenetwork/`

Read the relevant machine doc before working on a host:
- `machines/m2-pro.md` — this machine (daily driver)
- `machines/ubuntu-server.md` — Ubuntu server
- `machines/qnap-nas.md` — QNAP NAS
- `machines/fractal-pc.md` — Windows gaming PC
- `machines/macbook-pro-old.md` — old MacBook (offline)

## Quick Reference

### Machines & SSH

| Machine | IP | SSH Command | User | OS | `claude` CLI |
|---|---|---|---|---|---|
| **M2 Pro** (this machine) | `192.168.178.145` | — (local) | `jurrejan` | macOS Tahoe | yes (`~/.local/bin/claude`) |
| **Ubuntu Server** | `192.168.178.121` | `ssh ubuntu-server` | `jurrejan` | Ubuntu 24.04 | **no** |
| **QNAP NAS** | `192.168.178.100` | `ssh admin@192.168.178.100` | `admin` | QTS 5.2.6 | **no** |
| **Fractal PC** | `192.168.178.197` | `ssh fractal` (alias `ssh pc`) | `user` (Windows home `C:\Users\jurre`) | Windows 11 Pro | yes (`C:\Users\jurre\.local\bin\claude.exe`) |
| **Old MacBook** | unknown | `ssh macserver` | `jurrejan` | macOS (offline) | unknown (offline) |

Only **M2 Pro** and **Fractal** can run `claude` — spawn remote workers there, no capability probe needed.

### SSH Gotchas

- **NAS:** `jongserve.local` mDNS does not resolve — always use IP `192.168.178.100`
- **Fractal PC:** **always use the `ssh fractal` / `ssh pc` alias**, never the bare IP. The alias config has `IdentitiesOnly yes`; the bare `ssh user@192.168.178.197` hits the catch-all `Host *` rule, so the 1Password agent offers every key and the server drops the connection with **"Too many authentication failures"**.
- **Fractal PC (shell):** default SSH shell is **PowerShell**, not bash. Inline `$variables` in `ssh fractal "..."` get eaten by the outer PowerShell, and `&` is **not** a command separator (fails with `AmpersandNotAllowed`). Put logic in a script file, or run bash via `ssh fractal "wsl -d Ubuntu -e bash -s" < script.sh`.
- **Fractal PC (paths):** the SSH login user is `user`, but the Windows home folder is **`C:\Users\jurre`** — they differ. Never derive a path from the SSH user: `C:\Users\jurre\...` (WSL: `/mnt/c/Users/jurre/...`).
- **Fractal PC (scp):** `scp` cannot handle Windows paths containing spaces, quoting does not help (`No such file or directory`). Copy the file to a space-free path first, then scp from there:
  `ssh fractal 'Copy-Item "C:\Program Files (x86)\...\app.exe" C:\dev\_sandbox\app.exe'` then `scp fractal:C:/dev/_sandbox/app.exe .`
- **Old MacBook:** Currently offline/unreachable
- **All SSH keys** are managed via 1Password SSH Agent on M2

### Key Services

| Service | Machine | Access |
|---|---|---|
| Coolify (PaaS) | Ubuntu | `http://192.168.178.121:8000` |
| Traefik dashboard | Ubuntu | `http://192.168.178.121:8080` |
| Jellyfin | Ubuntu | `http://192.168.178.121:8096` |
| Samba shares | Ubuntu | `smb://192.168.178.121` |
| QTS Web UI | NAS | `https://192.168.178.100` |
| Plex | NAS | via QNAP package |
| WireGuard VPN | NAS | QVPN package |
| RDP | Fractal | `mstsc /v:192.168.178.197` |
| VNC | Fractal | `vnc://192.168.178.197` |
| Sunshine (streaming) | Fractal | ports 47984-48010 |

### Router

- Gateway: `192.168.178.1` (Ziggo ISP)
- All IPs are DHCP — no static reservations configured
- DNS: Google DNS (`8.8.8.8`, `8.8.4.4`)

## Working on a Machine

### Ubuntu Server

```bash
ssh ubuntu-server
# Check Docker containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
# Check disk usage
df -h /
# Check Coolify
docker logs coolify --tail 20
# Check Jellyfin
sudo systemctl status jellyfin
```

### QNAP NAS

```bash
ssh admin@192.168.178.100
# Check storage (CRITICAL: currently at 98%)
df -h /share/CACHEDEV1_DATA
# List shared folders
ls /share/CACHEDEV1_DATA/
# Check Docker — NOT in admin's default $PATH, use the full path (or export it)
DOCKER=/share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker; "$DOCKER" ps
# Check installed packages
ls /share/CACHEDEV1_DATA/.qpkg/
# NOTE: ps is BusyBox — GNU flags like `--sort` are unsupported.
# Use `top -b -n 1 | head -30` for process inspection.
```

### Fractal PC (Windows)

**Development work goes in `C:\dev`** — this is the development root on Fractal, deliberately mirroring the structure of `~/Documents/development` on the M2 Pro (same language/domain folder grouping). Clone and work on projects there, not scattered across the disk.

```bash
ssh fractal   # use the alias, never the bare IP (see SSH Gotchas)
# Default shell is PowerShell. Inline $vars get eaten and `&` is not a separator —
# keep multi-step logic in a script file rather than one-liners.
# Go to the development root
cd C:\dev
# Check disk space
Get-PSDrive C | Select-Object Used,Free
# List services
Get-Service | Where-Object {$_.Status -eq 'Running'}
# Check GPU
nvidia-smi
```

**Network drives (NAS):** `Y:` → `\\192.168.178.100\homes`, `Z:` → `\\192.168.178.100\Download`.
Fractal's `Videos` symlinks (`home`, `completed`) point into these. The mappings belong to the
**interactive** desktop session — over SSH `net use` lists them as **Unavailable** and both `Y:\`
and the raw UNC path fail (`UnauthorizedAccessException`), because no NAS credentials are cached
(`cmdkey /list:192.168.178.100` → none). To reach NAS files over SSH, store the credential first:
`cmdkey /add:192.168.178.100 /user:admin /pass:<pw>` — otherwise go via `ssh admin@192.168.178.100`.

**Claude config/history sync:** `~/Documents/development/_management/claude-sync/claude-sync` syncs Claude Code config (skills, agents, commands, CLAUDE.md) and per-project session history between the M2 Pro and Fractal (rsync via `wsl rsync` — no native rsync on Windows). Project pairs (Mac path ↔ `C:\dev\...` path) live in its `config.json`; `claude-sync status` dry-runs, `claude-sync sync` merges two-way. See its README.

### This Machine (M2 Pro)

```bash
# System info
system_profiler SPHardwareDataType
# Network
ifconfig en0
networksetup -getdnsservers Wi-Fi
# Docker
docker ps
# Network discovery
arp -a
```

## After Making Changes

When updating machine state (installing services, changing config, fixing issues):
1. Update the relevant `machines/<name>.md` doc
2. Keep the `network.md` **Services Map** in sync if services changed — a `grep` that
   returns nothing means the row is **missing**, not that there is nothing to do. Add it:

   ```
   | finances | Ubuntu | 3111 | `fin.jurrejan.com` (LAN + home WAN IPs only) |
   | <service> | <Ubuntu|NAS|Fractal> | <port> | <URL or how to reach it> |
   ```
3. Update `gaps.md` — mark resolved items with `- [x] ~~strikethrough~~`
4. Keep `README.md` machine table current if hardware/OS changed
