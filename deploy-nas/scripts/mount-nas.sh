#!/bin/bash

# mount-nas.sh — dependably mount the QNAP "Container" SMB share on macOS.
# Idempotent: safe to call from deploy scripts, login items, or by hand.
# Exit 0 = share is mounted and verified; exit 1 = could not mount.
#
# Credentials come from onenv (1Password), NOT the macOS Keychain.
# One-time setup (stores the share password in 1Password):
#   onenv set nas SMB_PASSWORD     # the 'admin' share password
#   onenv set nas SMB_USER         # optional; defaults to 'admin'
# Override the namespace with NAS_ONENV_NS=<ns>.

set -uo pipefail

SHARE="Container"
MOUNT="/Volumes/${SHARE}"
SENTINEL="caddy"                              # path under the share proving it's the right volume
ADDRS=("jongserve.local" "192.168.178.100")   # mDNS name first, raw IP as fallback
POLL_TRIES=30                                 # 30 * 0.5s = 15s for the mount to appear
NS="${NAS_ONENV_NS:-nas}"                      # onenv namespace holding the SMB credentials

log() { printf '[mount-nas] %s\n' "$*" >&2; }

is_mounted() { mount | grep -q " on ${MOUNT} (smbfs"; }
is_healthy() { [ -d "${MOUNT}/${SENTINEL}" ]; }

# `onenv get` emits a JSON envelope when stdout is a pipe; pull out .value.
onenv_value() {
    onenv get "$NS" "$1" 2>/dev/null | python3 -c 'import sys,json
try: sys.stdout.write(json.load(sys.stdin).get("value",""))
except Exception: pass'
}

# URL-encode stdin so credentials are safe to embed in the smb:// URL.
urlenc() { python3 -c 'import sys,urllib.parse; sys.stdout.write(urllib.parse.quote(sys.stdin.read(), safe=""))'; }

# 0. Already mounted and pointing at the right volume → nothing to do.
if is_mounted; then
    if is_healthy; then log "already mounted: ${MOUNT}"; exit 0; fi
    log "stale mount at ${MOUNT}; unmounting"
    diskutil unmount force "${MOUNT}" >/dev/null 2>&1 || umount -f "${MOUNT}" 2>/dev/null || true
fi

# A leftover empty /Volumes/Container makes the mounter fall back to "Container-1". Clear it.
if [ -d "${MOUNT}" ] && ! is_mounted; then rmdir "${MOUNT}" 2>/dev/null || true; fi

# 1. Credentials from onenv (user defaults to 'admin' if the key is absent).
SMB_USER="$(onenv_value SMB_USER)"; [ -n "$SMB_USER" ] || SMB_USER="admin"
SMB_PASSWORD="$(onenv_value SMB_PASSWORD)"
[ -n "$SMB_PASSWORD" ] || { log "no SMB password in onenv (${NS}/SMB_PASSWORD). Run: onenv set ${NS} SMB_PASSWORD"; exit 1; }

# 2. First reachable address wins.
host=""
for a in "${ADDRS[@]}"; do
    if ping -c1 -t2 "$a" >/dev/null 2>&1; then host="$a"; break; fi
done
[ -n "$host" ] || { log "NAS unreachable on: ${ADDRS[*]}"; exit 1; }

# 3. Mount via AppleScript `mount volume` with the onenv creds. The automounter
#    creates the /Volumes mountpoint (no sudo, no Keychain); the credentials are
#    passed via the heredoc (stdin), so the password never lands in any argv.
enc_user="$(printf '%s' "$SMB_USER" | urlenc)"
enc_pw="$(printf '%s' "$SMB_PASSWORD" | urlenc)"
log "mounting //${SMB_USER}@${host}/${SHARE} -> ${MOUNT}"
osascript >/dev/null 2>&1 <<APPLESCRIPT || log "mount volume reported an error (check: onenv get ${NS} SMB_PASSWORD)"
mount volume "smb://${enc_user}:${enc_pw}@${host}/${SHARE}"
APPLESCRIPT

# 4. Wait for the mount to settle.
for _ in $(seq 1 "$POLL_TRIES"); do is_mounted && break; sleep 0.5; done

# 5. Verify it is mounted AND is the expected volume.
if is_mounted && is_healthy; then
    log "mounted: ${MOUNT} (via ${host})"
    exit 0
fi

log "FAILED to mount ${MOUNT}."
log "Verify the onenv password is correct and the NAS is reachable on: ${ADDRS[*]}"
exit 1
