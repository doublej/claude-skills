# Safe Refactoring Workflow

Follow this workflow whenever you modify existing Home Assistant configuration: renaming entities, replacing template sensors with helpers, converting device triggers, or restructuring automations.

**Core rule:** Search all consumers BEFORE changing anything. Verify zero stale references AFTER.

---

## Universal Workflow

### Step 1: Identify the full scope of change

1. What changes? (entity ID, automation structure, sensor type, trigger semantics)
2. What sibling entities share the same device? (battery sensor, update entity, diagnostic button)
3. Rename one entity or all device entities?

### Step 2: Search ALL consumers

| Component | How to search |
|-----------|---------------|
| Automations | `ha_deep_search` or `ha_config_get_automation` |
| Dashboards | `ha_config_get_dashboard` for each dashboard |
| Scripts | `ha_config_get_script` |
| Scenes | HA API |
| Config-Entry groups | `GET /api/config/config_entries/entry?type=config&domain=group` — members in `options.entities` |
| Config-Entry integrations | `GET /api/config/config_entries/entry` — check `data` and `options` fields |

Record every location found. This becomes your update checklist for Step 4.

### Step 3: Make the change

Rename the entity, replace the template sensor, or restructure the automation.

### Step 4: Update every consumer

Work through each location from Step 2.

### Step 5: Verify

1. Search for the OLD identifier — expect zero results
2. Search for the NEW identifier — confirm all expected locations reference it
3. Reload/check dashboards if entity IDs changed
4. If stale references remain that you cannot update — rename back, report to user

---

## Entity Renames

**Device-sibling discovery (Step 1):**
HA devices bundle multiple entities. A smart plug might expose `switch.*`, `sensor.*_energy`, and `update.*`. Rename all siblings together for consistency.

**Dashboard locations to search:**
- `entity:` field
- `tap_action` and `hold_action` targets
- Conditional card conditions
- Template card Jinja2 blocks
- `views[n].badges` — badge rows per view (searched separately from cards)
- `views[n].header.card` — sections view header (HA 2025.3+)

---

## Helper Replacements

When replacing a template sensor with a built-in helper:

1. The new helper has a different `entity_id` — update every consumer of the old entity_id
2. Verify equivalence: same values, units, precision, unavailable-state handling

---

## Trigger Restructuring

`wait_for_trigger` waits for a state *change*; `wait_template` polls for *current state*. These differ when the target state is already true at wait start — `wait_for_trigger` blocks indefinitely, `wait_template` returns immediately.

---

## Config-Entry Groups

Entity registry renames do NOT update group members automatically. Group member entity IDs are stored in `options.entities` of the Config Entry — not in the entity registry.

**Detection:** List groups via `GET /api/config/config_entries/entry?type=config&domain=group`

**Fix:** Update membership via the Options Flow:
```http
POST /api/config/config_entries/options/flow
{"handler": "<group_config_entry_id>"}
```
Then submit updated entity list. Only one active Options Flow per Config Entry at a time — abandon first if a detection flow is open.

---

## Config-Entry Data (Blind Spots for renames)

Affected integrations that store entity_ids in Config Entry data:

| Integration | Storage field | Fields |
|---|---|---|
| Better Thermostat | `data` | `temperature_sensor`, `humidity_sensor`, `outdoor_sensor`, `window_sensors` |
| Generic Thermostat | `options` | `heater`, `target_sensor` |
| Generic Hygrostat | `options` | `humidifier`, `target_sensor` |
| Threshold Helper | `options` | `entity_id` |
| Min/Max Helper | `options` | `entity_ids` |

**Patch BEFORE the HA restart.** Scan via `GET /api/config/config_entries/entry` and check `data`/`options` fields.

For `options`-based integrations: fix via Options Flow (same pattern as Config-Entry-Groups).
For `data`-based integrations (Better Thermostat): no API-based fix path exists — inform the user.

---

## Storage-Mode Dashboards

Entity registry renames do NOT update Lovelace storage dashboards. Use the Lovelace WebSocket API:

```
1. Read: WebSocket {"type": "lovelace/config", "url_path": "<path>"}
   (use "url_path": null for the default Overview dashboard)

2. Replace entity IDs (JSON-aware, not string replace):
   def _replace_ids(obj, old_id, new_id):
       if isinstance(obj, str): return new_id if obj == old_id else obj
       if isinstance(obj, list): return [_replace_ids(i, old_id, new_id) for i in obj]
       if isinstance(obj, dict): return {(new_id if k == old_id else k): _replace_ids(v, old_id, new_id) for k, v in obj.items()}
       return obj

3. Write: WebSocket {"type": "lovelace/config/save", "url_path": "<path>", "config": new_config}
   → takes effect immediately, no restart required
```

List all dashboards: WebSocket `{"type": "lovelace/dashboards/list"}`
