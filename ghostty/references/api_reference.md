# Ghostty extended reference

Load when SKILL.md-level info is insufficient.

## CLI subcommands

```
ghostty +show-config [--default] [--docs] [--changes-only] [--default=false]
ghostty +validate-config <path>
ghostty +list-themes
ghostty +list-fonts
ghostty +list-keybinds [--default]
ghostty +list-actions
ghostty +list-colors
ghostty +show-face <font-family>
ghostty +crash-report
ghostty +version
```

- `--default=false --changes-only` → only user-set values (most useful for debugging).
- `--default --docs` → every option with inline description.

## Keybind grammar

```
trigger := [modifier+]* key
modifier := super|cmd|ctrl|alt|opt|shift
key := single char, named key (arrow_left, page_up, home, end, tab, enter, space, f1..f24, backspace, delete), or KeyA (W3C physical code)

action := name[:param]
sequence := trigger>trigger[>trigger...]=action
scope := (global:|all:|performable:|unconsumed:)?
```

Examples:
```
keybind = unconsumed:cmd+k=clear_screen           # don't consume, pass to app too
keybind = performable:cmd+w=close_surface         # only consume if close is available
keybind = ctrl+b>c=new_tab                        # tmux-style prefix
keybind = ctrl+b>%=new_split:right
```

Key tables (modal):
```
keybind = ctrl+b=activate_key_table:prefix,one_shot
keybind = prefix/c=new_tab
keybind = prefix/h=goto_split:left
```

Clear / unbind:
```
keybind = unbind:cmd+w       # remove one default
keybind = clear              # nuke ALL defaults (explicit rebinding required after)
```

## Theme format

Same syntax as config. Typically only sets:

```
background = 1d2021
foreground = ebdbb2
cursor-color = ebdbb2
selection-background = 3c3836
selection-foreground = ebdbb2
palette = 0=#282828
palette = 1=#cc241d
... (0-15)
```

User config keys after `theme = ...` override theme values.

Put custom themes in `~/.config/ghostty/themes/<name>` then `theme = <name>`, or reference a path.

## macOS-specific options

```
macos-titlebar-style = native|transparent|tabs|hidden
macos-titlebar-proxy-icon = visible|hidden
macos-non-native-fullscreen = false|true|visible-menu|padded-notch
macos-option-as-alt = true|false|left|right     # enable alt key combos
macos-window-shadow = true
macos-auto-secure-input = true                  # detect password prompts
macos-secure-input-indication = true
macos-icon = official|blueprint|chalkboard|glass|holographic|microchip|paper|retro|xray
macos-icon-frame = aluminum|beige|plastic|chrome
background-blur = 20                            # 0-20, radius
```

`macos-option-as-alt = true` is commonly requested — without it, `alt+f`/`alt+b` etc. in shells produce special chars instead of word-jump.

## Shell integration manual setup

Only needed for `/bin/bash` on macOS (non-Homebrew). Top of `~/.bashrc`:

```bash
if [ -n "${GHOSTTY_RESOURCES_DIR}" ]; then
    builtin source "${GHOSTTY_RESOURCES_DIR}/shell-integration/bash/ghostty.bash"
fi
```

Disable auto-injection:
```
shell-integration = none
```

Features flag (comma list, all off by default):
```
shell-integration-features = cursor,sudo,title,ssh-env,ssh-terminfo
```
- `cursor` — bar cursor at prompt, block during command
- `sudo` — preserve terminfo through `sudo`
- `title` — auto-set window title from cwd/command
- `ssh-env` — set `TERM=xterm-256color`, forward env
- `ssh-terminfo` — install ghostty terminfo on remote on first ssh (requires `infocmp`/`tic` on remote)

## Scrollback

```
scrollback-limit = 10000000      # bytes, default 10MB
```

Write scrollback to file:
```
keybind = cmd+shift+s=write_scrollback_file:paste
keybind = cmd+shift+e=write_screen_file:open,plain
```
Modes: `copy` (path to clipboard), `paste` (paste path into terminal), `open` (open file). Formats: `plain`, `history` (with escapes).

## Clipboard behavior

```
clipboard-read = allow|deny|ask
clipboard-write = allow|deny|ask
clipboard-trim-trailing-spaces = true
clipboard-paste-protection = true              # prompt if paste contains newlines/escapes
clipboard-paste-bracketed-safe = true
copy-on-select = false|true|clipboard
```

## Fonts deeper

```
font-family = JetBrains Mono
font-family-bold = ...
font-family-italic = ...
font-family-bold-italic = ...
font-style = auto|auto-italic|<specific style name>
font-synthetic-style = bold,italic,bold-italic
font-feature = -liga                # disable, or +ss01 to enable stylistic set
adjust-cell-width = 5%
adjust-cell-height = 5%
adjust-font-baseline = -1
adjust-underline-position = 2
font-thicken = true                 # macOS
font-thicken-strength = 128         # 0-255
freetype-load-flags = hinting,force-autohint    # Linux
```

`font-family` can be repeated for fallback chain. Symbols/emoji fall back to system fonts automatically.

## Troubleshooting checklist

1. `ghostty +validate-config <path>` — catches typos
2. `ghostty +show-config --default=false --changes-only` — what's actually parsed
3. Wrong file? Check both macOS Application Support and XDG paths
4. Restart required? Many options live-reload, some don't (window chrome, some shell integration features). When in doubt, quit and relaunch.
5. Keybind not firing? `ghostty +list-keybinds` shows resolved bindings including conflicts. Later entries override earlier.
6. Global keybind not working on macOS? Grant Accessibility permission in System Settings → Privacy & Security → Accessibility.
