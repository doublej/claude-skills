---
name: home-assistant
description: "Control smart home devices, automations, dashboards, entities via ha-mcp"

  DO NOT TRIGGER when the user is building their own HA integration or add-on from scratch.
---

# Home Assistant Skill

Uses the **ha-mcp** MCP server (homeassistant-ai/ha-mcp). If MCP tools are not available, guide the user to install the server first.

<mcp_server_setup>
## MCP Server Setup

The fastest path for Claude Code:

```bash
# stdio (local)
claude mcp add home-assistant \
  --env HOMEASSISTANT_URL=http://homeassistant.local:8123 \
  --env HOMEASSISTANT_TOKEN=<long-lived-token> \
  -- uvx ha-mcp@latest

# HTTP (remote / HA add-on)
claude mcp add --transport http home-assistant <MCP_SERVER_URL>
```

Get a long-lived token: HA UI → Profile → Security → Long-Lived Access Tokens.

For the HA add-on (no token needed): Settings → Add-ons → Install "Home Assistant MCP Server" from the `homeassistant-ai/ha-mcp` repository.
</mcp_server_setup>

<core_principles>
## Core Principles

1. Use the MCP tools — never generate YAML snippets for the user to paste manually.
2. Prefer native HA constructs over Jinja2 templates. See `references/automation-patterns.md` and `references/helper-selection.md`.
3. Use `entity_id` over `device_id`. `device_id` breaks when devices are re-added.
</core_principles>

<key_tool_groups>
## Key Tool Groups

| Goal | Primary tools |
|------|---------------|
| Find entities | `ha_search_entities`, `ha_get_state`, `ha_deep_search` |
| Control devices | `ha_call_service`, `ha_bulk_control` |
| Manage automations | `ha_config_get_automation`, `ha_config_set_automation` |
| Manage dashboards | `ha_config_get_dashboard`, `ha_config_set_dashboard`, `ha_dashboard_find_card` |
| Manage helpers | `ha_config_list_helpers`, `ha_config_set_helper`, `ha_get_helper_schema` |
| Debug | `ha_get_automation_traces`, `ha_get_history`, `ha_get_logbook` |
| System | `ha_get_system_health`, `ha_backup_create`, `ha_check_config` |
</key_tool_groups>

<automation_best_practices>
## Automation Best Practices

Read `references/automation-patterns.md` when writing or editing automations.

**Quick mode selector:**

| Scenario | Mode |
|----------|------|
| Motion light with timeout | `restart` |
| Sequential (door locks) | `queued` |
| Per-entity independent actions | `parallel` |
| One-shot notification | `single` (default) |

**Common anti-patterns:**

| Instead of | Use |
|-----------|-----|
| `condition: template` with `float > 25` | `condition: numeric_state` with `above: 25` |
| `wait_template: "{{ is_state(...) }}"` | `wait_for_trigger` with state trigger |
| `device_id` in triggers | `entity_id` (or `device_ieee` for ZHA buttons) |
| `mode: single` on motion lights | `mode: restart` |
</automation_best_practices>

<helper_selection>
## Helper Selection

Read `references/helper-selection.md` before creating a template sensor.

**Quick substitution table:**

| Need | Helper | Not |
|------|--------|-----|
| Average/sum multiple sensors | `min_max` | Template with math |
| Rate of change | `derivative` | Template delta |
| Binary threshold | `threshold` | Template binary sensor |
| Consumption per period | `utility_meter` | Counter + reset automation |
| Any-on / all-on | `group` | Template binary sensor |
| Count events | `counter` | input_number + automation |
| Countdown timer | `timer` | delay + input_datetime |
| Weekly schedule | `schedule` | Template with weekday checks |
</helper_selection>

<modifying_existing>
## Modifying Existing Config

Before renaming entities, replacing helpers, or restructuring automations — read `references/safe-refactoring.md`. Renames silently break dashboards, scripts, Config-Entry data, and storage dashboards.
</modifying_existing>

<workflow>
## Workflow: Creating an Automation

1. `ha_search_entities` — find the right entity IDs
2. Check `references/automation-patterns.md` for native trigger/condition
3. Check `references/helper-selection.md` if a derived sensor is needed
4. `ha_config_set_automation` — create via API (validates, no file edits needed)
5. `ha_get_automation_traces` — verify it runs correctly
</workflow>

<troubleshooting>
## Troubleshooting

- **Entity not found:** `ha_deep_search` with broader terms; check `ha_get_overview`
- **Automation not firing:** `ha_get_automation_traces` — inspect trigger info, condition results
- **Config errors:** `ha_check_config` after any YAML change
- **Logbook gaps:** `ha_get_logbook` with time range; check recorder settings
</troubleshooting>
