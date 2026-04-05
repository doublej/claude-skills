# Helper Selection Guide

Use built-in helpers instead of template sensors wherever possible.

## Decision Matrix

| Need | Helper | Not |
|------|--------|-----|
| Average/sum multiple sensors | `min_max` (type: mean/sum) | Template with math |
| Average over time | `statistics` | Template tracking history |
| Rate of change | `derivative` | Template calculating delta |
| On/off at threshold | `threshold` | Template binary sensor |
| Consumption per period | `utility_meter` | Counter + reset automation |
| Time in state | `history_stats` | Template tracking timestamps |
| Power to energy | `integration` | Template approximating |
| User toggle | `input_boolean` | — |
| User number | `input_number` | — |
| User selection | `input_select` | — |
| Count events | `counter` | input_number + automation |
| Countdown timer | `timer` | delay + input_datetime |
| Weekly schedule | `schedule` | Template with weekday checks |
| Time of day mode | `tod` | Template with time checks |
| Any-on / all-on | `group` | Template binary sensor |

---

## Numeric Aggregation

### min_max

Average/min/max/sum across multiple sensors.

```yaml
# RIGHT - min_max helper
sensor:
  - platform: min_max
    name: "Average Temperature"
    type: mean       # min, max, mean, median, last, sum
    entity_ids:
      - sensor.temp_bedroom
      - sensor.temp_living
      - sensor.temp_kitchen
```

### statistics

Statistical analysis over time for a single sensor.

```yaml
sensor:
  - platform: statistics
    name: "Temperature Change (5 min)"
    entity_id: sensor.temperature
    state_characteristic: change   # mean, median, stdev, change, count, ...
    max_age:
      minutes: 5
```

---

## Rate and Change

### derivative

Rate of change over time (e.g., power rate from cumulative energy).

```yaml
sensor:
  - platform: derivative
    name: "Power Rate of Change"
    source: sensor.power
    unit_time: min
    time_window:
      minutes: 5
```

### threshold

Binary sensor that turns on/off when a numeric sensor crosses a threshold.

```yaml
# RIGHT - with hysteresis to prevent rapid toggling
binary_sensor:
  - platform: threshold
    name: "High Temperature"
    entity_id: sensor.temperature
    upper: 25
    hysteresis: 1   # ON above 26, OFF below 24
```

---

## Time-Based Tracking

### utility_meter

Consumption tracking with periodic resets.

```yaml
utility_meter:
  daily_energy:
    source: sensor.energy_consumption
    cycle: daily    # quarter-hourly, hourly, daily, weekly, monthly, yearly
  monthly_energy:
    source: sensor.energy_consumption
    cycle: monthly
```

### history_stats

How long/often an entity has been in a state.

```yaml
sensor:
  - platform: history_stats
    name: "Lights on today"
    entity_id: light.living_room
    state: "on"
    type: time      # time (hours), ratio (%), count (changes)
    start: "{{ now().replace(hour=0, minute=0, second=0) }}"
    end: "{{ now() }}"
```

### integration (Riemann sum)

Convert power (W) to energy (kWh).

```yaml
sensor:
  - platform: integration
    name: "Solar Energy"
    source: sensor.solar_power
    unit_prefix: k
    unit_time: h
    method: left    # left (recommended for sparse data), right, trapezoidal
```

---

## State Storage

| Helper | Use for |
|--------|---------|
| `input_boolean` | Toggle flags (guest mode, vacation mode) |
| `input_number` | Adjustable thresholds, target temperatures |
| `input_select` | Dropdown state selections |
| `input_text` | Storing text strings |
| `input_datetime` | Alarm times, future dates |
| `input_button` | Manual automation triggers |

---

## Counting and Timing

### counter

```yaml
# RIGHT - dedicated counter helper
counter:
  coffee_count:
    name: "Coffees Today"
    initial: 0
    step: 1
    minimum: 0
    maximum: 100
    restore: true
```

Actions: `counter.increment`, `counter.decrement`, `counter.reset`, `counter.set_value`

### timer

Pausable/restartable countdown timers.

```yaml
timer:
  laundry:
    name: "Laundry Timer"
    duration: "01:00:00"
    restore: true
```

Actions: `timer.start`, `timer.pause`, `timer.cancel`, `timer.finish`
Events: `timer.started`, `timer.paused`, `timer.cancelled`, `timer.finished`

---

## Scheduling

### schedule

Weekly on/off schedule (creates a binary sensor).

```yaml
schedule:
  work_hours:
    name: "Work Hours"
    monday:
      - from: "09:00:00"
        to: "17:00:00"
    tuesday:
      - from: "09:00:00"
        to: "17:00:00"
```

### time of day (tod)

Binary sensor based on current time with sunrise/sunset support.

```yaml
binary_sensor:
  - platform: tod
    name: "Night Time"
    after: sunset
    after_offset: "01:00:00"
    before: sunrise
```

---

## Entity Grouping

### group

Combine entities for collective state and control.

```yaml
group:
  all_lights:
    name: "All Lights"
    entities:
      - light.living_room
      - light.bedroom
    all: false  # ON if ANY member is on (true = ALL must be on)
```
