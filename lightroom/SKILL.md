---
name: lightroom
description: Adobe Lightroom Classic automation via the lightroom-mcp MCP server. Cull, rate, keyword, develop, and export photos by chatting. Covers install, tool selection, develop-settings keys, batch workflow recipes, and offline catalog SQL analytics. Triggers on "lightroom", "lightroom classic", ".lrcat", "edit my photos", "apply preset", "batch export photos", "rate photos", "cull photos", "keyword photos".
---

# Lightroom Classic

Drives Adobe Lightroom Classic through the [Automaat/lightroom-mcp](https://github.com/Automaat/lightroom-mcp) server (npm: `@mskalski/lightroom-mcp`). Two components must both be running: the Node MCP server and the Lua plugin inside Lightroom.

<scope>
- Lightroom **Classic** only (desktop, .lrcat catalog). Not Lightroom CC (cloud).
- Live catalog control via 14 MCP tools.
- Offline catalog analytics via direct SQLite reads — see `references/sql-analytics.md`.
</scope>

## Install

<install_check>
Before any other step, verify the MCP is connected:
```bash
claude mcp list | grep lightroom
```
If absent → run install. If present but tools fail → check Lightroom plugin status.
</install_check>

<install_steps>
1. **Add the MCP server** (one-time):
   ```bash
   claude mcp add lightroom -- npx -y @mskalski/lightroom-mcp
   ```

2. **Install the Lua plugin** (one-time, copies plugin into Lightroom's Modules folder):
   ```bash
   npx -y @mskalski/lightroom-mcp install-plugin
   ```

3. **Start the plugin** in Lightroom (every session):
   - Fully quit and reopen Lightroom Classic (Cmd+Q on macOS, Alt+F4 on Windows).
   - File → Plug-in Manager → **Lightroom MCP** → click **Start Server**.
   - Status should show "Server running".

4. **Verify**: ask "list my Lightroom collections". If names come back, the bridge is live.
</install_steps>

<troubleshoot>
- **Tool calls hang or "failed to open localhost:58763"** → old async task still owns the port. Quit Lightroom fully (not just close window) and reopen. "Reload Plug-in" alone is not enough.
- **"Plugin not connected"** → click **Start Server** in Plug-in Manager.
- **Timeout on `search_photos`** → catalog scan with no filter. Always pass at least one of `filename`, `keywords`, `rating`, or date range.
- **Logs**:
  - Plugin: `~/Documents/LrClassicLogs/LightroomMCP.log`
  - Claude Desktop MCP: `~/Library/Logs/Claude/mcp*.log`
</troubleshoot>

## Tool Selection

| Intent | Tool | Notes |
|---|---|---|
| User said "the photos I have selected" | `get_selected_photos` | Reads filmstrip selection. No filter args. |
| Find by criteria (rating/keyword/date/filename) | `search_photos` | **Always pass a filter** — unfiltered scans time out on large catalogs. |
| Read EXIF + develop state of one photo | `get_photo_metadata` | Use `photo_id` from a prior search/selection result. |
| Browse catalog organization | `list_collections` | |
| New collection / nested collection set | `create_collection` | `parent` is optional collection set name. |
| Add photos to existing collection | `add_to_collection` | |
| Tag with keywords | `set_keywords` | `add_keywords` and/or `remove_keywords` arrays. |
| Star rating (0–5) | `set_rating` | |
| Pull files into catalog | `import_photos` | `source_path` = file or folder. `copy_to` optional. |
| Write JPEG/PNG/TIFF/original to disk | `export_photos` | `destination` required. `format`, `quality`, `width`, `height` optional. |
| Discover preset names | `list_develop_presets` | Returns `[{name, folder}]` for all preset folders. |
| Apply named preset | `apply_develop_preset` | Match is by `name` only — first match across folders wins. |
| Match one photo's look across many | `copy_develop_settings` | Optional `settings` whitelist (array of SDK keys) limits scope. |
| Direct numeric edits (Exposure, Contrast, etc.) | `set_develop_settings` | SDK key names — see `references/develop-settings-keys.md`. |

<photo_id_format>
Photo IDs come back from `search_photos` / `get_selected_photos` results. File paths also work as `photo_id`. Treat IDs as opaque — don't synthesize them.
</photo_id_format>

## Workflow Recipes

Detailed multi-step procedures: `references/workflow-recipes.md`. Quick patterns:

### Cull → rate → export
```
1. search_photos(start_date, end_date)             # narrow to a shoot
2. get_photo_metadata(photo_id) for each candidate # inspect
3. set_rating(photo_ids, rating: N)                # 0=reject, 1-5=keepers
4. search_photos(rating: 5)                        # collect picks
5. export_photos(photo_ids, destination, format: "jpeg", quality: 90, width: 2000)
```

### Match a look across a series
```
1. get_selected_photos()                           # user picks one as reference
2. copy_develop_settings(source_id, target_ids,
     settings: ["Exposure2012", "Contrast2012",
                "Highlights2012", "Shadows2012",
                "Whites2012", "Blacks2012",
                "Vibrance", "Saturation"])
```
Whitelist prevents copying crop / spot-removal / local-adjustments — pure tone match.

### Apply a preset, then tweak
```
1. list_develop_presets()                          # confirm exact name
2. apply_develop_preset(photo_ids, preset_name)
3. set_develop_settings(photo_id, {"Exposure2012": 0.3})  # nudge after
```

### Batch keyword tagging
```
1. search_photos(start_date, end_date)
2. set_keywords(photo_ids, add_keywords: ["client-name", "2026", "delivered"])
```

## Develop Settings — Key Reference

`set_develop_settings` and the `settings` whitelist of `copy_develop_settings` use **Lightroom SDK key names**. The `2012` suffix marks Process Version 2012+ tone keys (Lightroom 4 and later) — using non-suffixed legacy keys silently no-ops on modern process versions.

Common keys (full list: `references/develop-settings-keys.md`):

| Key | Range | Meaning |
|---|---|---|
| `Exposure2012` | -5.0 … +5.0 | Stops |
| `Contrast2012` | -100 … +100 | |
| `Highlights2012` | -100 … +100 | |
| `Shadows2012` | -100 … +100 | |
| `Whites2012` | -100 … +100 | |
| `Blacks2012` | -100 … +100 | |
| `Clarity2012` | -100 … +100 | |
| `Vibrance` | -100 … +100 | (no `2012` suffix) |
| `Saturation` | -100 … +100 | (no `2012` suffix) |
| `Temperature` | 2000 … 50000 | Kelvin |
| `Tint` | -150 … +150 | Green↔Magenta |
| `WhiteBalance` | string | `"As Shot" \| "Auto" \| "Daylight" \| "Cloudy" \| "Shade" \| "Tungsten" \| "Fluorescent" \| "Flash" \| "Custom"` |

<key_traps>
- `Vibrance` / `Saturation` have **no** `2012` suffix. `Vibrance2012` is invalid.
- `Exposure2012` is in stops (float), not a 0–100 slider value.
- Setting `Temperature` numerically forces `WhiteBalance: "Custom"` — don't pass both unless you mean Custom.
</key_traps>

## Offline catalog analytics

For read-only queries that don't need Lightroom running (catalog stats, finding orphans, dedupe), the `.lrcat` file is a SQLite database. See `references/sql-analytics.md` for the schema map and `fdenivac/Lightroom-SQL-tools` (41⭐) usage.

<sql_warning>
SQL access bypasses Lightroom's locking model. **Lightroom must be closed** when querying, and writes via SQL can corrupt the catalog. Read-only is safe; back up `.lrcat` before any experimental write.
</sql_warning>

## Out of scope

- **Lightroom CC (cloud)**: separate product, OAuth2-gated REST API, Python bindings (`lou-k/lightroom-cc-api`) are incomplete. Not covered.
- **Writing custom Lua plugins**: lightroom-mcp covers the common surface. For new tools, fork the MCP repo and add a `Handler*.lua` + `DISPATCH` entry — out of scope here.
- **Generating XMP preset files from scratch**: see `FUTC-Coding/preset-generator` (24⭐). Apply via `apply_develop_preset` once the file is placed in a preset folder.
