---
name: ghostty
description: Configure and customize Ghostty terminal emulator (Mitchell Hashimoto's GPU-accelerated terminal). Use when the user wants to edit ghostty config, add keybinds, set themes/fonts, configure splits/tabs/quick terminal, enable shell integration/ssh-terminfo, debug why a ghostty setting is not applying, or automate/script Ghostty (open windows/tabs/splits, run commands in them) — on macOS ALWAYS via AppleScript, never by launching the binary. Triggers on "ghostty", mentions of `config.ghostty`, `~/.config/ghostty/`, or Ghostty-specific actions like `toggle_quick_terminal`, `new_split`, `goto_split`.
---

# Ghostty

Ghostty is a fast, native, GPU-accelerated terminal emulator. Installed version on this machine is detected via `ghostty --version`.

<config_file>
Edit, don't create fresh — config may already exist.

macOS (preferred location on this machine):
- `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty` (1.2.3+)
- Older: same path, filename `config`

XDG (Linux / fallback):
- `~/.config/ghostty/config.ghostty`

Check both. Ghostty loads all and later overrides earlier.

**Find the active file:**
```bash
ghostty +show-config --default=false --changes-only
```
Lists only user-set values. Useful to see what's actually applied.
</config_file>

<syntax>
```
key = value
# comments start with hash
font-family = JetBrains Mono
background = 282c34
theme = GruvboxDark
```

- Keys lowercase, hyphen-separated
- Whitespace around `=` ignored
- Every key also a CLI flag: `ghostty --background=282c34`
- Include other files: `config-file = path/to/other` (prefix `?` to make optional)
</syntax>

<reload>
- In-app: `cmd+shift+,` (macOS) / `ctrl+shift+,` (Linux)
- Some options only apply to NEW surfaces/windows (font, theme often do; padding sometimes doesn't until new window)
- Some options are startup-only — restart required

Tell user which type after editing when unsure. When in doubt: restart.
</reload>

<keybinds>
Syntax: `keybind = trigger=action[:parameter]`

```
keybind = cmd+t=new_tab
keybind = cmd+d=new_split:right
keybind = cmd+shift+d=new_split:down
keybind = cmd+alt+left=goto_split:left
keybind = cmd+alt+right=goto_split:right
keybind = cmd+backtick=toggle_quick_terminal
keybind = ctrl+a>n=new_window          # sequence: ctrl+a then n
keybind = global:cmd+backtick=toggle_quick_terminal   # system-wide
keybind = unbind:cmd+w                 # remove a default
keybind = clear                        # clear ALL defaults (use sparingly)
```

Prefixes: `global:` (system-wide, requires accessibility permission on macOS), `all:` (all surfaces), `performable:` (only consume if action can run).

### Common actions

Splits: `new_split:right|down|left|up|auto`, `goto_split:<dir>|previous|next`, `resize_split:<dir>,<px>`, `equalize_splits`, `toggle_split_zoom`
Tabs: `new_tab`, `next_tab`, `previous_tab`, `goto_tab:N`, `move_tab:N`, `close_tab`, `toggle_tab_overview`
  - `move_tab:N` only **reorders** a tab within its window — it cannot detach a tab to a new window. No tab-detach action exists yet (upstream issue #2630).
Windows: `new_window`, `close_window`, `toggle_fullscreen`, `toggle_maximize`
Quick terminal: `toggle_quick_terminal`, `toggle_visibility`
Clipboard: `copy_to_clipboard`, `paste_from_clipboard`, `copy_url_to_clipboard`
Font: `increase_font_size:N`, `decrease_font_size:N`, `reset_font_size`, `set_font_size:N`
Scroll: `scroll_to_top`, `scroll_to_bottom`, `scroll_page_up`, `jump_to_prompt:prev|next`
Config: `reload_config`, `open_config`

Full list: `ghostty +list-actions`
Current bindings: `ghostty +list-keybinds`
</keybinds>

<themes>
```
theme = GruvboxDark              # one of bundled
theme = dark:GruvboxDark,light:Catppuccin Latte   # auto light/dark
theme = ./relative/to/config.theme                # custom file
```

List bundled: `ghostty +list-themes` (hundreds, including Dracula, Tokyo Night, Catppuccin variants, Solarized, Nord, etc.)

A theme is just a config file containing palette/background/foreground. User config values override theme values.
</themes>

<fonts>
```
font-family = JetBrains Mono
font-family-bold = JetBrains Mono Bold
font-size = 14
font-feature = -liga,-calt         # disable ligatures
font-thicken = true                # macOS-only, thicker rendering
adjust-cell-height = 10%
```

List available: `ghostty +list-fonts`
Ghostty ships JetBrains Mono + Nerd Font symbols embedded — no install needed.
</fonts>

<quick_terminal>
## Quick terminal (macOS + GTK)

Drop-down terminal triggered by a keybind.

```
keybind = global:cmd+backtick=toggle_quick_terminal
quick-terminal-position = top      # top|bottom|left|right|center
quick-terminal-screen = mouse      # mouse|main|macos-menu-bar
quick-terminal-animation-duration = 0.2
quick-terminal-autohide = true
```

`global:` prefix needed to toggle when Ghostty isn't focused. macOS will prompt for Accessibility permission on first use.
</quick_terminal>

<shell_integration>
Auto-injected for bash, elvish, fish, nushell, zsh. Features:
- New windows inherit working directory of focused surface
- `jump_to_prompt` keybind navigation
- Smart close (no prompt when at shell prompt)
- Command-output selection via `cmd+triple-click`

Enable extras (off by default):
```
shell-integration-features = ssh-env,ssh-terminfo,sudo
```
- `ssh-terminfo` — installs ghostty terminfo on remote host on first ssh (recommended if user ssh'es often)
- `ssh-env` — forwards `TERM=xterm-256color` + env vars
- `sudo` — preserves terminfo through `sudo`

Manual setup (only needed for `/bin/bash` on macOS): see `references/shell-integration.md`.
</shell_integration>

<window_appearance>
```
window-padding-x = 12
window-padding-y = 12
window-padding-balance = true
background-opacity = 0.95
background-blur = 20               # macOS only, blur radius
macos-titlebar-style = tabs        # native|transparent|tabs|hidden
macos-option-as-alt = true         # so alt-key combos work
cursor-style = block               # block|bar|underline|block_hollow
cursor-style-blink = true
```
</window_appearance>

<links>
```
link-url = true          # detect http(s) URLs and make them clickable (cmd/ctrl+click)
link-previews = true     # macOS: hover-preview the target URL — true|false|osc8
```

- `link-url` — auto-detect plain `http://` / `https://` URLs in output and make them clickable. Default `true`.
- `link-previews` — whether to show the URL preview popover on hover. `true` (all links), `false` (none), or `osc8` (only links created via the OSC 8 escape sequence). macOS only.
- `link` — the custom regex matcher (`link = <regex>,<action>`) for turning arbitrary patterns into clickable links. **Currently not settable:** Ghostty's own docs mark it "TODO: This can't currently be set!" — do not hand the user a `link = …` config line expecting it to work.

**Custom schemes (until `link` lands):** emit an OSC 8 hyperlink directly from your program instead of relying on config-side matching:
```bash
printf '\e]8;;myapp://open/123\e\\clickable text\e]8;;\e\\'
```
With `link-previews = osc8`, only these explicitly-emitted links get a hover preview.
</links>

<common_tasks>
**Add/edit config:** find file (check macOS path first), edit, reload with `cmd+shift+,`. For font/theme changes, usually need new window.

**Setting not applying:** check for typo (`ghostty +validate-config path`), check `ghostty +show-config --default=false --changes-only` to see what's parsed, restart Ghostty if startup-only.

**Validate before restart:**
```bash
ghostty +validate-config ~/Library/Application\ Support/com.mitchellh.ghostty/config.ghostty
```

**Show all options with docs:** `ghostty +show-config --default --docs | less`
</common_tasks>

<automation_macos>
## Automating Ghostty on macOS (1.3+) — NEVER launch the binary

**Critical:** `ghostty` on PATH is the app binary itself (`/Applications/Ghostty.app/Contents/MacOS/ghostty`). Running `ghostty -e …`, `ghostty --…`, or `open -na Ghostty` boots a **second app instance** — two Ghostty processes in the Dock. Never do this. `ghostty +new-window` is Linux-only (`not supported on this platform`).

The correct channel is **AppleScript** (Ghostty 1.3+ ships a full scripting dictionary, `Ghostty.sdef`). It always targets the running instance (and launches a single one if none is running):

```applescript
tell application "Ghostty"
  activate
  -- plain new window / tab
  new window
  new tab
  -- with command, cwd, initial input
  set cfg to new surface configuration
  set initial working directory of cfg to "/Users/jurrejan/Documents/development"
  set command of cfg to "htop"          -- run instead of shell
  set initial input of cfg to "git status\n"  -- or type into the shell
  new window with configuration cfg
end tell
```

Also available: `split <terminal> direction right/down/…`, `input text "…" to <terminal>` (paste-like), `send key "enter" to <terminal>`, `focus`, `select tab`, `close tab/window`, `perform action "<ghostty action string>" on <terminal>`, and read-only access to windows/tabs/terminals (`id`, `name`, `working directory`). Explore with `sdef /Applications/Ghostty.app`.

From bash: `osascript -e 'tell application "Ghostty" to new window'`.
</automation_macos>

<known_limitations>
- Tab **detach** to a new window still has no scriptable path (`move_tab:N` only reorders; upstream issue #2630).
- `ghostty +new-window` IPC is Linux (D-Bus) only.
- Don't reach for Accessibility automation (System Events / cliclick) — use the AppleScript dictionary above.
</known_limitations>

<references>
- `references/api_reference.md` — extended option tables and macOS-specific notes
- Upstream docs: https://ghostty.org/docs
- Actions list: `ghostty +list-actions`
- Themes list: `ghostty +list-themes`
</references>
