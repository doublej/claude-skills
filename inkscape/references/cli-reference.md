# Inkscape CLI Complete Reference

## Binary path (macOS)
```
/Applications/Inkscape.app/Contents/MacOS/inkscape
```

## Export flags

| Flag | Short | Description |
|------|-------|-------------|
| `--export-filename=FILE` | `-o` | Output filename (`-` for stdout) |
| `--export-type=TYPE[,TYPE]` | | `svg`, `png`, `ps`, `eps`, `pdf`, `emf`, `wmf`, `xaml` |
| `--export-overwrite` | | Overwrite input file |
| `--export-dpi=DPI` | `-d` | Resolution (default: 96) |
| `--export-width=PX` | `-w` | Bitmap width |
| `--export-height=PX` | `-h` | Bitmap height |
| `--export-area-page` | `-C` | Page area (default) |
| `--export-area-drawing` | `-D` | Drawing bounding box |
| `--export-area=x0:y0:x1:y1` | `-a` | Custom rectangle |
| `--export-area-snap` | | Snap to integer pixels |
| `--export-margin=M` | | Add margin |
| `--export-id=ID[;ID]` | `-i` | Export specific object(s) |
| `--export-id-only` | `-j` | Hide everything except export target |
| `--export-use-hints` | `-t` | Use stored filename/DPI hints |
| `--export-page=all\|n[,a-b]` | | Specific pages |
| `--export-background=COLOR` | `-b` | Background color |
| `--export-background-opacity=V` | `-y` | Background opacity (0.0-1.0) |
| `--export-text-to-path` | `-T` | Convert text to paths |
| `--export-plain-svg` | `-l` | Strip Inkscape namespaces |
| `--export-pdf-version=1.4` | | PDF version |
| `--export-ps-level=2\|3` | | PostScript level |
| `--export-png-color-mode=MODE` | | `Gray_1/8/16`, `RGB_8/16`, `RGBA_8/16` |
| `--export-png-compression=0-9` | | PNG compression (default: 6) |
| `--export-png-antialias=0-3` | | Antialiasing (default: 2) |
| `--export-ignore-filters` | | Render filters as vectors |
| `--export-latex` | | Split graphics + LaTeX overlay |

## Query flags

| Flag | Short | Description |
|------|-------|-------------|
| `--query-id=ID[,ID]` | `-I` | Object(s) to query |
| `--query-x` | `-X` | X coordinate |
| `--query-y` | `-Y` | Y coordinate |
| `--query-width` | `-W` | Width |
| `--query-height` | `-H` | Height |
| `--query-all` | `-S` | All objects: id,x,y,w,h |

## Action flags

| Flag | Description |
|------|-------------|
| `--actions="a1;a2:arg"` | Chain actions |
| `--actions-file=FILE` | Actions from file |
| `--action-list` | Print all actions |
| `--select=ID[,ID]` | Pre-select objects |
| `--batch-process` | Auto-close GUI |

## All actions by category

### Selection
- `select-all` / `select-all:all|layers|no-layers|groups|no-groups`
- `select-clear`, `select-invert`, `select-list`
- `select-by-id:ID`, `select-by-class:CLASS`, `select-by-element:TAG`
- `unselect-by-id:ID`

### Path operations
- `object-to-path` — shapes/text to `<path>`
- `path-union` — boolean union
- `path-difference` — bottom minus top
- `path-intersection` — intersection
- `path-exclusion` — XOR
- `path-division` — cut bottom by top
- `path-combine` — compound path
- `path-simplify` — reduce nodes

### Transforms
- `object-flip-horizontal`, `object-flip-vertical`
- `object-rotate-90-cw`, `object-rotate-90-ccw`
- `transform-rotate:ANGLE`, `transform-scale:FACTOR`
- `duplicate`, `delete`

### Export (actions syntax)
- `export-filename:path`, `export-type:fmt`, `export-dpi:N`
- `export-area-page`, `export-area-drawing`
- `export-id:ID`, `export-id-only`
- `export-background:COLOR`, `export-background-opacity:V`
- `export-plain-svg`, `export-text-to-path`
- `export-do` — **triggers the export**

### File
- `file-open:path`, `file-close`

### Cleanup
- `vacuum-defs` — remove unused `<defs>`

## Shell mode
```bash
inkscape --shell
# Enter actions per line, end with `quit`
```

## System info
```bash
inkscape --version
inkscape --system-data-directory
inkscape --user-data-directory
```

## Pipe mode
```bash
cat input.svg | inkscape --pipe --export-type=png -o output.png
```
