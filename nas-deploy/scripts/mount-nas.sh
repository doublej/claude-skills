#!/bin/bash

# mount-nas.sh — dependably mount the QNAP "Container" SMB share on macOS.
# Idempotent: safe to call from deploy scripts, login items, or by hand.
# Exit 0 = share is mounted and verified; exit 1 = could not mount.
#
# One-time setup (so this runs without prompting):
#   In Finder press Cmd-K, connect to  smb://jongserve.local/Container
#   authenticate as 'admin', and tick "Remember this password in my keychain".
#   That stores the credential under the SAME server string this script uses.

set -uo pipefail

SHARE="Container"
MOUNT="/Volumes/${SHARE}"
SMB_USER="admin"
SENTINEL="caddy"                              # path under the share proving it's the right volume
ADDRS=("jongserve.local" "192.168.178.100")   # mDNS name first, raw IP as fallback
POLL_TRIES=30                                 # 30 * 0.5s = 15s for the async mount to appear

log() { printf '[mount-nas] %s\n' "$*" >&2; }

is_mounted() { mount | grep -q " on ${MOUNT} (smbfs"; }
is_healthy() { [ -d "${MOUNT}/${SENTINEL}" ]; }

# 0. Already mounted and pointing at the right volume → nothing to do.
if is_mounted; then
    if is_healthy; then log "already mounted: ${MOUNT}"; exit 0; fi
    log "stale mount at ${MOUNT}; unmounting"
    diskutil unmount force "${MOUNT}" >/dev/null 2>&1 || umount -f "${MOUNT}" 2>/dev/null || true
fi

# A leftover empty /Volumes/Container makes Finder mount at "Container-1". Clear it.
if [ -d "${MOUNT}" ] && ! is_mounted; then rmdir "${MOUNT}" 2>/dev/null || true; fi

# 1. First reachable address wins.
host=""
for a in "${ADDRS[@]}"; do
    if ping -c1 -t2 "$a" >/dev/null 2>&1; then host="$a"; break; fi
done
[ -n "$host" ] || { log "NAS unreachable on: ${ADDRS[*]}"; exit 1; }

# 2. Mount via NetAuth so the saved Keychain credential is reused (no prompt
#    once the one-time setup above is done). open returns immediately; we poll.
log "mounting //${SMB_USER}@${host}/${SHARE} -> ${MOUNT}"
open "smb://${SMB_USER}@${host}/${SHARE}"

# 3. Wait for the async mount.
for _ in $(seq 1 "$POLL_TRIES"); do is_mounted && break; sleep 0.5; done

# 4. Verify it is mounted AND is the expected volume.
if is_mounted && is_healthy; then
    log "mounted: ${MOUNT} (via ${host})"
    exit 0
fi

log "FAILED to mount ${MOUNT}."
log "If a Finder auth dialog appeared, save the password to Keychain (see setup note at top)."
exit 1
