#!/usr/bin/env bash
# file-assoc.sh — Change default app for a file extension on macOS
# Usage:
#   file-assoc.sh set <extension> <app-name>    Set default app
#   file-assoc.sh get <extension>                Show current default
#   file-assoc.sh list <extension>               List all registered apps
#   file-assoc.sh uti <extension>                Show UTI for extension
#   file-assoc.sh id <app-name>                  Show bundle ID for app
set -euo pipefail

ensure_duti() {
  if ! command -v duti &>/dev/null; then
    echo "Installing duti via Homebrew..."
    brew install duti
  fi
}

get_uti() {
  local ext="$1"
  swift -e "import UniformTypeIdentifiers; if let t = UTType(filenameExtension: \"$ext\") { print(t.identifier) } else { print(\"unknown\") }" 2>/dev/null
}

get_bundle_id() {
  local app="$1"
  osascript -e "id of app \"$app\"" 2>/dev/null
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  set)
    ext="${1:?Usage: file-assoc.sh set <extension> <app-name>}"
    app="${2:?Usage: file-assoc.sh set <extension> <app-name>}"
    ext="${ext#.}"
    ensure_duti
    bundle_id=$(get_bundle_id "$app") || { echo "Error: app '$app' not found"; exit 1; }
    uti=$(get_uti "$ext")
    echo "Extension:  .$ext"
    echo "UTI:        $uti"
    echo "App:        $app"
    echo "Bundle ID:  $bundle_id"
    echo ""
    duti -s "$bundle_id" ".$ext" all
    echo "Done. Verifying:"
    duti -x "$ext"
    ;;
  get)
    ext="${1:?Usage: file-assoc.sh get <extension>}"
    ext="${ext#.}"
    ensure_duti
    duti -x "$ext"
    ;;
  list)
    ext="${1:?Usage: file-assoc.sh list <extension>}"
    ext="${ext#.}"
    swift -e '
import AppKit
import UniformTypeIdentifiers
let ext = "'"$ext"'"
guard let uti = UTType(filenameExtension: ext) else { print("Unknown extension: .\(ext)"); exit(1) }
print("UTI: \(uti.identifier)")

// Warn about known UTI conflicts (e.g. .ts = MPEG-2 not TypeScript)
let codeExts: Set = ["ts","tsx","mts","cts","jsx","mjs","cjs","svelte","vue"]
if codeExts.contains(ext) && !uti.conforms(to: .sourceCode) {
    print("⚠  macOS maps .\(ext) to \(uti.identifier), not source code")
    print("   The set command binds by extension to avoid this.\n")
}

let tmp = NSTemporaryDirectory() + "file-assoc-probe." + ext
FileManager.default.createFile(atPath: tmp, contents: nil)
defer { try? FileManager.default.removeItem(atPath: tmp) }
let url = URL(fileURLWithPath: tmp)

// Collect apps from both the file URL and source-code UTI to catch editors
var seen = Set<URL>()
var apps = [URL]()
for u in NSWorkspace.shared.urlsForApplications(toOpen: url) {
    if seen.insert(u).inserted { apps.append(u) }
}
if codeExts.contains(ext) {
    for u in NSWorkspace.shared.urlsForApplications(toOpen: UTType.sourceCode) {
        if seen.insert(u).inserted { apps.append(u) }
    }
}

if apps.isEmpty { print("No registered apps found"); exit(0) }
print("Registered apps:")
for app in apps {
    let bid = Bundle(url: app)?.bundleIdentifier ?? "?"
    let name = app.deletingPathExtension().lastPathComponent
    print("  \(name) (\(bid))")
}
' 2>/dev/null
    ;;
  uti)
    ext="${1:?Usage: file-assoc.sh uti <extension>}"
    ext="${ext#.}"
    echo "$(get_uti "$ext")"
    ;;
  id)
    app="${1:?Usage: file-assoc.sh id <app-name>}"
    echo "$(get_bundle_id "$app")"
    ;;
  help|*)
    echo "file-assoc.sh — Change default app for file extensions on macOS"
    echo ""
    echo "Commands:"
    echo "  set <ext> <app>   Set default app for extension"
    echo "  get <ext>         Show current default for extension"
    echo "  list <ext>        List all registered apps for extension"
    echo "  uti <ext>         Show UTI for extension"
    echo "  id <app>          Show bundle ID for app"
    ;;
esac
