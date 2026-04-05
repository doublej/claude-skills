# Device Control Patterns

Best practices for controlling devices, triggering from Zigbee buttons/remotes, and structuring service calls.

---

## Entity ID vs Device ID

`device_id` changes when a device is re-added (Zigbee mesh repair, re-setup, hardware replacement). Automations using `device_id` break silently.

```yaml
# WRONG - device_id changes if device is re-added
triggers:
  - trigger: device
    device_id: abc123def456
    domain: binary_sensor
    type: motion

# RIGHT - entity_id is stable and renameable
triggers:
  - trigger: state
    entity_id: binary_sensor.hallway_motion
    to: "on"
```

**When device_id is acceptable:** Z2M autodiscovered device triggers (managed by Z2M), temporary automations.

---

## Service Call Structure

```yaml
actions:
  - action: domain.service_name   # Required
    target:                       # Optional but recommended
      entity_id: entity.id        # Single or list
      area_id: area_name          # Single or list (prefer over device_id)
      device_id: device_id        # Avoid except for Z2M
    data:                         # Service-specific parameters
      parameter: value
    response_variable: result     # Capture response (if needed)
```

**Common mistake:** `brightness_pct` at the wrong level. It must be inside `data:`.

### Target Types

| Type | Persistence |
|------|-------------|
| `entity_id` | Stable (recommended) |
| `area_id` | Stable |
| `device_id` | Changes on re-add — avoid |

### Capturing Response Data

```yaml
actions:
  - action: weather.get_forecasts
    target:
      entity_id: weather.home
    data:
      type: hourly
    response_variable: forecast
  - action: notify.mobile_app_phone
    data:
      message: "Tomorrow's high: {{ forecast['weather.home'].forecast[0].temperature }}°C"
```

---

## Zigbee Button/Remote Patterns

### ZHA

Use **event triggers** with `device_ieee` (persistent across re-adds).

```yaml
triggers:
  - trigger: event
    event_type: zha_event
    event_data:
      device_ieee: "00:15:8d:00:07:26:f2:8a"
      command: "toggle"
```

Find device_ieee and command: Developer Tools → Events → subscribe to `zha_event` → press button.

### Zigbee2MQTT

Use device triggers (autodiscovered by Z2M) or explicit MQTT triggers.

```yaml
# Z2M device trigger - autodiscovered
triggers:
  - trigger: device
    device_id: abc123def456
    domain: mqtt
    type: action
    subtype: single

# Alternative: MQTT topic trigger (more explicit)
triggers:
  - trigger: mqtt
    topic: "zigbee2mqtt/Bedroom Button/action"
    payload: "single"
```

### ZHA vs Z2M Comparison

| Aspect | ZHA | Zigbee2MQTT |
|--------|-----|-------------|
| Trigger type | `event` (zha_event) | `device` or `mqtt` |
| Identifier | `device_ieee` (persistent) | `device_id` (autodiscovered) |
| Button actions | `command` field | `type` and `subtype` |

---

## Domain-Specific Patterns

### Lights

```yaml
actions:
  - action: light.turn_on
    target:
      entity_id: light.living_room
    data:
      brightness_pct: 80
      transition: 2
      color_temp_kelvin: 3000
```

### Climate

```yaml
actions:
  - action: climate.set_temperature
    target:
      entity_id: climate.living_room
    data:
      temperature: 22
      hvac_mode: heat
```

### Covers

```yaml
# 0 = closed, 100 = open
actions:
  - action: cover.set_cover_position
    target:
      entity_id: cover.living_room_blinds
    data:
      position: 50
```

### Media Players

```yaml
actions:
  - action: media_player.volume_set
    target:
      entity_id: media_player.living_room_speaker
    data:
      volume_level: 0.5  # 0.0 to 1.0
```

### Notifications

```yaml
actions:
  - action: notify.mobile_app_phone
    data:
      title: "Motion Detected"
      message: "Motion in {{ trigger.to_state.attributes.friendly_name }}"
      data:
        tag: "motion-alert"
        actions:
          - action: "DISMISS"
            title: "Dismiss"
```

---

## Quick Reference: Trigger Types for Devices

| Device Type | ZHA | Zigbee2MQTT | Generic |
|-------------|-----|-------------|---------|
| Button/Remote | `event` (zha_event) | `device` or `mqtt` | N/A |
| Motion sensor | `state` | `state` | `state` |
| Door/Window | `state` | `state` | `state` |
| Temperature | `state` or `numeric_state` | `state` or `numeric_state` | `state` or `numeric_state` |

Always prefer `state` triggers with `entity_id` for sensors and switches. Only use event/device triggers for stateless devices (buttons, remotes).
