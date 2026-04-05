---
name: inkscape
description: "SVG export, batch conversion, path ops, optimization via CLI"
---

# Inkscape

Control Inkscape via CLI for SVG manipulation, export, and vector graphics automation.

## Setup

Inkscape binary on macOS: `/Applications/Inkscape.app/Contents/MacOS/inkscape`

If not installed: `brew install --cask inkscape`

Alias for convenience (add to `~/.zshrc`):
```bash
alias inkscape="/Applications/Inkscape.app/Contents/MacOS/inkscape"
```

Use full path in scripts/MCP configs. Verify: `inkscape --version`

## Export

```bash
# SVG -> PNG (96 DPI default)
inkscape in.svg -o out.png

# High-res PNG
inkscape in.svg -o out.png -d 300

# Specific pixel dimensions
inkscape in.svg -o out.png -w 1024 -h 768

# SVG -> PDF / EPS
inkscape in.svg -o out.pdf
inkscape in.svg -o out.eps

# Crop to drawing content (no page whitespace)
inkscape in.svg -o out.png -D

# Plain SVG (strip Inkscape metadata)
inkscape in.svg -o clean.svg -l

# Export specific object by ID
inkscape in.svg -o icon.png -i myIcon -j

# Multiple formats at once
inkscape in.svg --export-type=png,pdf

# Custom background
inkscape in.svg -o out.png -b "#ffffff" -y 1.0
```

### Export area flags
| Flag | Short | Effect |
|------|-------|--------|
| `--export-area-page` | `-C` | Page bounds (default) |
| `--export-area-drawing` | `-D` | Tight crop to content |
| `--export-area=x0:y0:x1:y1` | `-a` | Custom rectangle |
| `--export-id=ID` | `-i` | Export specific object |
| `--export-id-only` | `-j` | Hide everything else |

## Query

```bash
inkscape in.svg -W -H              # drawing dimensions
inkscape in.svg -I myObj -X -Y -W -H  # object bounding box
inkscape in.svg -S                  # all objects: id,x,y,w,h
```

## Actions

Chain operations with `--actions="action1;action2"`. End exports with `export-do`.

```bash
# Convert all to paths and export
inkscape in.svg --actions="select-all; object-to-path; export-filename:out.svg; export-do"

# Boolean union
inkscape in.svg --select=a,b --actions="path-union; export-filename:merged.svg; export-do"

# Clean unused defs + plain SVG
inkscape in.svg --actions="vacuum-defs; export-plain-svg; export-filename:clean.svg; export-do"
```

### Key actions

| Category | Actions |
|----------|---------|
| **Select** | `select-all`, `select-by-id:ID`, `select-by-element:TAG`, `select-clear` |
| **Path ops** | `object-to-path`, `path-union`, `path-difference`, `path-intersection`, `path-exclusion`, `path-combine`, `path-simplify` |
| **Transform** | `object-flip-horizontal`, `object-flip-vertical`, `object-rotate-90-cw`, `transform-rotate:ANGLE`, `transform-scale:FACTOR` |
| **Export** | `export-filename:path`, `export-type:fmt`, `export-dpi:N`, `export-area-page`, `export-area-drawing`, `export-do` |
| **Cleanup** | `vacuum-defs`, `export-plain-svg` |
| **File** | `file-open:path`, `file-close` |

Full list: `inkscape --action-list`

## Batch Processing

### Shell mode (keeps Inkscape resident, faster for multiple files)
```bash
cat <<'EOF' | inkscape --shell
file-open:f1.svg; export-type:png; export-dpi:300; export-do; file-close
file-open:f2.svg; export-type:png; export-dpi:300; export-do; file-close
quit
EOF
```

### Multi-file export
```bash
inkscape --export-type=png file1.svg file2.svg file3.svg
```

## SVG Optimization

```bash
# Inkscape built-in cleanup
inkscape in.svg --vacuum-defs --export-plain-svg -o clean.svg

# Scour (install: pip install scour)
scour -i in.svg -o out.svg --enable-viewboxing --enable-id-stripping \
  --enable-comment-stripping --shorten-ids --indent=none

# Pipeline: Inkscape cleanup -> scour
inkscape in.svg --vacuum-defs --export-plain-svg --export-filename=- | \
  scour -i - -o optimized.svg --enable-viewboxing --shorten-ids
```

## Python (inkex)

For programmatic SVG manipulation without GUI. Install: `pip install inkex`

```python
import inkex

# Load and manipulate
svg = inkex.load_svg("input.svg")
root = svg.getroot()

rect = inkex.Rectangle()
rect.set("x", "10"); rect.set("y", "10")
rect.set("width", "100"); rect.set("height", "50")
rect.set("style", "fill:#ff0000")
root.append(rect)

# Call Inkscape CLI from Python
from inkex.command import inkscape
inkscape("input.svg", export_type="png", export_filename="out.png")
```

See `references/cli-reference.md` for complete flag/action reference.

## MCP Server

For AI-driven Inkscape automation, use [inkscape-mcps](https://github.com/grumpydevorg/inkscape-mcps) (cross-platform, MIT):

```bash
uv add inkscape-mcp
```

Config for Claude:
```json
{
  "mcpServers": {
    "inkscape-mcp": {
      "command": "inkscape-mcp",
      "env": { "INKS_WORKSPACE": "/path/to/workspace" }
    }
  }
}
```

Tools: `action_list`, `action_run`, `dom_validate`, `dom_set`, `dom_clean`

### Alternative: inkmcp (Linux only)
[inkmcp](https://github.com/Shriinivas/inkmcp) — live Inkscape control via D-Bus. Not compatible with macOS.
