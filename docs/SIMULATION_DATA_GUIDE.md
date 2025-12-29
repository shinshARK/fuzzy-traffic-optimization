# Simulation Data Export Guide (For Member A)

This document explains how to export simulation data for the Manim visualization.

## Overview

Member C needs a **JSON file** containing frame-by-frame data of:
1. Traffic light states (which phase is green, timer value)
2. Queue counts for each direction
3. Car spawn/departure events

---

## File Format: JSON

Export to: `simulation_data.json`

### Structure

```json
{
  "metadata": { ... },
  "frames": [
    { "t": 0, "traffic_state": {...}, "car_events": [...], "departures": [...] },
    { "t": 1, ... },
    ...
  ]
}
```

---

## Field Reference

### metadata (top-level)

| Field | Type | Description |
|-------|------|-------------|
| `simulation_duration` | int | Total timesteps (e.g., 100) |
| `time_step` | int | Usually 1 |
| `traffic_mode` | string | `"fuzzy"` or `"fixed"` |

### frames[] (array of frame objects)

Each frame represents one timestep:

| Field | Type | Description |
|-------|------|-------------|
| `t` | int | Current timestep (0, 1, 2, ...) |
| `traffic_state` | object | Light status + queue counts |
| `car_events` | array | Cars that spawned this frame |
| `departures` | array | Cars that left the intersection |

### traffic_state (per frame)

| Field | Type | Values |
|-------|------|--------|
| `current_phase` | string | `"NS"` or `"EW"` |
| `green_timer` | int | Seconds remaining for this phase |
| `queues` | object | `{"N": 3, "S": 2, "E": 5, "W": 4}` |

### car_events[] (spawns)

When a car **arrives** at the intersection:

| Field | Type | Description |
|-------|------|-------------|
| `car_id` | string | Unique ID like `"N_1"`, `"E_3"` (origin + sequence) |
| `event` | string | Always `"spawn"` |
| `origin` | string | `"N"`, `"S"`, `"E"`, or `"W"` |
| `destination` | string | Where the car is going |
| `intent` | string | `"straight"`, `"left"`, or `"right"` |

### departures[] (exits)

When a car **crosses** the intersection:

| Field | Type | Description |
|-------|------|-------------|
| `car_id` | string | Same ID from the spawn event |
| `origin` | string | Where car came from |
| `destination` | string | Where car went |

---

## Movement Rules

```
Phase "NS" is green → Cars from N and S can depart
Phase "EW" is green → Cars from E and W can depart
```

A car can only depart when its origin direction matches the active phase:
- `origin = "N"` or `"S"` → needs phase `"NS"`
- `origin = "E"` or `"W"` → needs phase `"EW"`

---

## Example: One Frame

```json
{
  "t": 5,
  "traffic_state": {
    "current_phase": "NS",
    "green_timer": 25,
    "queues": { "N": 2, "S": 1, "E": 6, "W": 4 }
  },
  "car_events": [
    {
      "car_id": "E_3",
      "event": "spawn",
      "origin": "E",
      "destination": "W",
      "intent": "straight"
    }
  ],
  "departures": [
    {
      "car_id": "N_1",
      "origin": "N",
      "destination": "S"
    }
  ]
}
```

**What this means:**
- At t=5, NS phase is still green (25 seconds left)
- A new car `E_3` arrived from East → added to E queue (must wait)
- Car `N_1` from North crossed through (NS is green, so it can go)

---

## How to Generate This in Python

In your `simulation.py`, after each timestep:

```python
import json

# Track cars with incrementing counters
car_counters = {"N": 0, "S": 0, "E": 0, "W": 0}
frames = []

for t in range(simulation_duration):
    frame = {
        "t": t,
        "traffic_state": {
            "current_phase": intersection.current_phase,
            "green_timer": intersection.green_timer,
            "queues": dict(intersection.queues)
        },
        "car_events": [],
        "departures": []
    }
    
    # When a car arrives (from Poisson generator)
    for direction, arrivals in new_arrivals.items():
        for _ in range(arrivals):
            car_counters[direction] += 1
            frame["car_events"].append({
                "car_id": f"{direction}_{car_counters[direction]}",
                "event": "spawn",
                "origin": direction,
                "destination": get_random_destination(direction),
                "intent": determine_intent(direction, destination)
            })
    
    # When a car departs (queue decreases)
    # ... track which car_ids are leaving
    
    frames.append(frame)

# Save to file
output = {
    "metadata": {
        "simulation_duration": simulation_duration,
        "time_step": 1,
        "traffic_mode": "fuzzy"
    },
    "frames": frames
}

with open("simulation_data.json", "w") as f:
    json.dump(output, f, indent=2)
```

---

## Questions?

Ask Member C (visualizer) if you need clarification on the format!
