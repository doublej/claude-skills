---
name: build-macos-apps
description: Build, run, test, debug, instrument, sign, and ship native macOS apps with SwiftUI, AppKit interop, Liquid Glass, unified logging, and shell-first desktop workflows. Use when scaffolding a Mac app, refactoring scenes/windows, fixing codesign or notarization, adding telemetry, or running the build/test loop with xcodebuild or SwiftPM.
license: MIT
---

# Build macOS Apps

Eleven focused sub-skills for native macOS development. Top-level SKILL routes to references; each reference is self-contained.

Ported from [openai/plugins · build-macos-apps](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps) (MIT). Codex-app Run-button bits (`.codex/environments/environment.toml`) are kept verbatim — inert in Claude Code, but the `script/build_and_run.sh` itself is universally useful.

## Pick the right reference

| Task | Reference |
|---|---|
| Scaffold a new macOS SwiftUI app — scenes, file structure, state ownership | `references/swiftui-patterns.md` |
| Build / run / debug — wire a `script/build_and_run.sh`, classify build failures | `references/build-run-debug.md` |
| Run Xcode/SwiftPM tests, narrow failing scope, classify failures | `references/test-triage.md` |
| Diagnose codesign, entitlements, hardened runtime, Gatekeeper | `references/signing-entitlements.md` |
| Archive, validate bundle, prep notarization | `references/packaging-notarization.md` |
| Pure SwiftPM macOS package builds | `references/swiftpm-macos.md` |
| Adopt Liquid Glass / modern macOS material design | `references/liquid-glass.md` |
| Customize windows: toolbar, drag region, placement, restoration, borderless | `references/window-management.md` |
| Bridge SwiftUI → AppKit (NSViewRepresentable, NSWindow, panels) | `references/appkit-interop.md` |
| Refactor oversized macOS view files toward stable scenes | `references/view-refactor.md` |
| Add `Logger` / `os.Logger` instrumentation and verify events | `references/telemetry.md` |

### Sub-references (loaded from a parent skill, but readable directly)

- SwiftUI patterns deep-dives: `windowing.md`, `commands-menus.md`, `split-inspectors.md`, `settings.md`, `menu-bar-extra.md`, `components-index.md`
- AppKit interop deep-dives: `representables.md`, `window-panels.md`, `responder-menus.md`, `drag-drop-pasteboard.md`
- Build/run bootstrap (canonical `build_and_run.sh` + `.codex/environments/environment.toml`): `run-button-bootstrap.md`

## What this skill covers

- Discovering local Xcode workspaces, projects, Swift packages
- Shell-first build/run loops via `xcodebuild`, `swift`, `open`, `lldb`, `codesign`, `spctl`, `plutil`, `log stream`
- Native macOS SwiftUI scenes, menus, settings, toolbars, multiwindow flows
- Modern macOS Liquid Glass and design-system adoption
- AppKit interop for representables, responder-chain, panels
- `Logger`/`os.Logger` instrumentation + Console / `log stream` verification
- Triaging unit, integration, UI-hosted macOS tests
- Codesign, entitlements, hardened runtime, notarization

## Out of scope

- iOS / watchOS / tvOS simulator workflows
- Desktop UI automation
- App Store Connect release management
- Pixel-perfect visual design

## Companion commands

If installed at `~/.claude/commands/`:

- `/build-and-run-macos-app` — create or update `script/build_and_run.sh`, then run
- `/fix-codesign-error` — inspect and explain codesign/entitlement failure
- `/test-macos-app` — focused test run with failure classification

## Related skill

The existing `swift` skill covers SwiftUI architecture more broadly (codegen, MVVM, animations, design). Use `build-macos-apps` when the work is desktop-platform-specific (windows, AppKit, codesign, Mac scenes); use `swift` for general Swift architecture and UI patterns.
