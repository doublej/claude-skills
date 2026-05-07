# Workflow Recipes

Concrete multi-step procedures for common Lightroom Classic workflows via the MCP. Each recipe is a sequence of `tool_name(args)` calls — exact tool names match the MCP schema in `SKILL.md`.

## 1. Cull a shoot (cull → rate → export selects)

Goal: from a folder of imports, mark keepers and export only 5-star picks as deliverable JPEGs.

```
# Step 1 — narrow to the shoot
search_photos(start_date: "2026-05-06", end_date: "2026-05-07", limit: 500)
  → returns [{photo_id, filename, rating, ...}, ...]

# Step 2 — let user (or AI judgment from metadata) rate
# For AI-driven culling, fetch metadata first:
for each photo_id:
  get_photo_metadata(photo_id)
  → inspect EXIF (sharpness via shutter_speed, ISO, focus distance), histogram

set_rating(photo_ids: [<rejects>], rating: 0)
set_rating(photo_ids: [<maybes>], rating: 3)
set_rating(photo_ids: [<picks>],  rating: 5)

# Step 3 — collect the picks
search_photos(start_date: "2026-05-06", end_date: "2026-05-07", rating: 5)

# Step 4 — export deliverables
export_photos(
  photo_ids: <pick_ids>,
  destination: "/Users/me/Deliveries/2026-05-06-clientname",
  format: "jpeg",
  quality: 90,
  width: 2400
)
```

<cull_tips>
- Avoid scanning the full catalog — always pass dates or filename pattern.
- AI-driven culling from metadata alone is heuristic (shutter speed × focal length / 2 = blur risk; ISO > camera native = noise risk). Eyes-on review wins; use AI to pre-sort.
- `rating: 0` ≠ flagged-as-reject. Use it as "not yet reviewed" or "weak". For Lightroom's reject flag, the MCP currently has no tool — set rating instead.
</cull_tips>

## 2. Match a series to a hero photo

Goal: client picked one image as the look. Apply the same tone/color to 50 siblings without dragging crop or local adjustments along.

```
# Step 1 — establish the reference
get_selected_photos()
  → first id is the hero (or ask user)
  → remaining are targets

# Step 2 — copy only tone+color keys
copy_develop_settings(
  source_id: <hero_id>,
  target_ids: [<sibling_ids>],
  settings: [
    "Exposure2012", "Contrast2012",
    "Highlights2012", "Shadows2012",
    "Whites2012", "Blacks2012",
    "Texture", "Clarity2012", "Dehaze",
    "Vibrance", "Saturation",
    "Temperature", "Tint", "WhiteBalance",
    "ParametricShadows", "ParametricDarks",
    "ParametricLights", "ParametricHighlights",
    "HueRed", "HueOrange", "HueYellow", "HueGreen",
    "HueAqua", "HueBlue", "HuePurple", "HueMagenta",
    "SaturationRed", "SaturationOrange", "SaturationYellow", "SaturationGreen",
    "SaturationAqua", "SaturationBlue", "SaturationPurple", "SaturationMagenta",
    "LuminanceRed", "LuminanceOrange", "LuminanceYellow", "LuminanceGreen",
    "LuminanceAqua", "LuminanceBlue", "LuminancePurple", "LuminanceMagenta"
  ]
)
```

<match_tips>
- Whitelist excludes crop, lens corrections, local masks, calibration. Each sibling keeps its own framing and per-lens fix.
- For black & white series, swap HSL keys for `GrayMixerRed` … `GrayMixerMagenta` and add `ConvertToGrayscale`.
- If white balance was custom-tuned (numeric Temperature/Tint), include all three keys: `WhiteBalance`, `Temperature`, `Tint`.
</match_tips>

## 3. Apply a preset, then nudge

Goal: start from a known preset, then bias exposure or contrast slightly per-image.

```
# Step 1 — discover exact preset name
list_develop_presets()
  → [{name: "VSCO Kodak Portra 400", folder: "Film"}, ...]

# Step 2 — apply
apply_develop_preset(
  photo_ids: <ids>,
  preset_name: "VSCO Kodak Portra 400"
)

# Step 3 — per-photo nudge
for each photo_id with adjustment:
  set_develop_settings(
    photo_id: <id>,
    settings: { "Exposure2012": 0.3, "Highlights2012": -15 }
  )
```

<preset_tips>
- Preset names are matched by `name` only — first match across folders wins. If two folders have a preset named `"Punchy"`, behavior is undefined; rename one.
- Nudges are additive **on top of** the applied preset, not relative to RAW. Stacking `set_develop_settings` after `apply_develop_preset` overwrites only the keys you pass.
- To revert to RAW defaults, apply the built-in `"Adobe Default"` preset (folder: `"Lightroom Develop Presets"`).
</preset_tips>

## 4. Batch keyword tagging

Goal: tag every photo from a shoot with project / client / status keywords.

```
search_photos(start_date: "2026-05-01", end_date: "2026-05-31")

set_keywords(
  photo_ids: <ids>,
  add_keywords: ["may-2026", "client-acme", "wedding"]
)
```

To **rename** a keyword: add new + remove old in one call:
```
set_keywords(
  photo_ids: <ids>,
  add_keywords: ["delivered"],
  remove_keywords: ["pending-delivery"]
)
```

## 5. Import + organize a shoot

Goal: copy from SD card, import, place in a dated collection.

```
# Step 1 — import (copies files + adds to catalog)
import_photos(
  source_path: "/Volumes/SD_CARD/DCIM/100CANON",
  copy_to: "/Users/me/Photos/2026/2026-05-06_acme_wedding"
)

# Step 2 — find what was just imported (by date)
search_photos(start_date: "2026-05-06", end_date: "2026-05-06")

# Step 3 — collect them
create_collection(name: "2026-05-06 Acme Wedding", parent: "Weddings 2026")

add_to_collection(
  collection_name: "2026-05-06 Acme Wedding",
  photo_ids: <ids>
)
```

<import_tips>
- `copy_to` only copies; it does not move from the SD card. Eject manually after.
- Without `copy_to`, photos are added in-place — risky if source is removable storage.
- `parent` for `create_collection` must be an existing collection set; if it doesn't exist, create the set first (or omit and place at root).
</import_tips>

## 6. Preset-from-AI then library install

Goal: have GPT-4o (or Claude) generate an XMP preset, drop it into Lightroom's preset folder, then apply via the MCP.

```
# Outside the MCP — write XMP file directly:
# macOS: ~/Library/Application Support/Adobe/CameraRaw/Settings/<Name>.xmp
# Windows: %APPDATA%\Adobe\CameraRaw\Settings\<Name>.xmp
# Format reference: FUTC-Coding/preset-generator (24⭐) on GitHub

# Restart Lightroom (preset folder scan happens at boot).

# Then:
list_develop_presets()
  → confirm new preset shows up

apply_develop_preset(photo_ids: <ids>, preset_name: "<Name>")
```

The MCP **cannot create preset files** — it only applies existing ones. Preset authoring is a file-system operation, not a tool call.

## 7. Find develop-status of a photo before tweaking

```
get_photo_metadata(photo_id)
  → returns develop_settings dictionary
  → inspect current Exposure2012, ToneCurveName2012, etc.

# Then make an informed delta:
set_develop_settings(photo_id, settings: { "Exposure2012": <new_value> })
```

Useful when the user says "make it brighter" — read current `Exposure2012`, add `+0.3`, write back. Don't guess from zero.

## Anti-patterns

- **Don't loop `apply_develop_preset` per photo** when one call accepts an array. Use `photo_ids: [a, b, c]`.
- **Don't write local-adjustment masks via `set_develop_settings`** — they're nested structures and will silently fail or corrupt. Apply via preset or `copy_develop_settings`.
- **Don't run `search_photos` without filters** on a 100k+ catalog. It will time out at the LR Lua side.
- **Don't `import_photos` from a folder with non-image files** without a Lightroom-side filter — the SDK skips them but logs warnings; cleaner to point at a folder of only RAW/JPEG.
- **Don't try to set `ProcessVersion` directly** to "upgrade" old photos — apply a recent preset (or `"Adobe Default"`) instead.
