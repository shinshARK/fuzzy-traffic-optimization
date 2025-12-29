# Simulation Data Export Guide (For Member A)

This document explains how to export simulation data for Manim visualization.

## Phase System: 4-Phase (N → S → E → W)

We use a **4-phase system** where only one direction goes at a time:

| Phase | Who Goes | Why? |
|-------|----------|------|
| `"N"` | Only North cars | No conflict with any other direction |
| `"S"` | Only South cars | No conflict |
| `"E"` | Only East cars | No conflict |
| `"W"` | Only West cars | No conflict |

**Fuzzy logic determines duration** for each phase based on queue length.

---

## JSON Structure

Export to: `simulation_data.json`

```json
{
  "metadata": {
    "simulation_duration": 100,
    "phase_order": ["N", "S", "E", "W"],
    "traffic_mode": "fuzzy"
  },
  "frames": [
    {
      "t": 0,
      "traffic_state": {
        "current_phase": "N",
        "green_timer": 15,
        "queues": { "N": 3, "S": 2, "E": 5, "W": 4 }
      },
      "car_events": [...],
      "departures": [...]
    }
  ]
}
```

---

## Field Reference

### car_events[] (when a car arrives)

| Field | Type | Description |
|-------|------|-------------|
| `car_id` | string | `"N_1"`, `"E_3"` (origin + sequence) |
| `origin` | string | `"N"`, `"S"`, `"E"`, or `"W"` |
| `destination` | string | Where car goes |
| `intent` | string | `"straight"`, `"left"`, `"right"` |
| `queue_position` | int | 0, 1, 2... (for visual offset) |

### departures[] (when a car leaves)

| Field | Type | Description |
|-------|------|-------------|
| `car_id` | string | Same ID from spawn |
| `origin` | string | Where car came from |
| `destination` | string | Where car went |

---

## Movement Rules

```
A car can ONLY depart when current_phase matches its origin:
- origin = "N" → needs phase "N"
- origin = "S" → needs phase "S"
- origin = "E" → needs phase "E"
- origin = "W" → needs phase "W"
```

---

## Example: Phase Cycle

```
t=0:  Phase N, green_timer=15  → N cars depart
t=15: Phase S, green_timer=12  → S cars depart  
t=27: Phase E, green_timer=20  → E cars depart (fuzzy gave more time due to high queue)
t=47: Phase W, green_timer=10  → W cars depart
t=57: Phase N again...         → Cycle repeats
```

---

## Generating in Python

```python
import json

# Phase order
PHASES = ["N", "S", "E", "W"]
current_phase_idx = 0
car_counters = {"N": 0, "S": 0, "E": 0, "W": 0}
frames = []

for t in range(simulation_duration):
    current_phase = PHASES[current_phase_idx % 4]
    
    frame = {
        "t": t,
        "traffic_state": {
            "current_phase": current_phase,
            "green_timer": intersection.green_timer,
            "queues": dict(intersection.queues)
        },
        "car_events": [],
        "departures": []
    }
    
    # Spawn new arrivals
    for direction, arrivals in new_arrivals.items():
        queue_pos = intersection.queues[direction]
        for _ in range(arrivals):
            car_counters[direction] += 1
            frame["car_events"].append({
                "car_id": f"{direction}_{car_counters[direction]}",
                "origin": direction,
                "destination": get_destination(direction),
                "intent": get_intent(direction, destination),
                "queue_position": queue_pos
            })
            queue_pos += 1
    
    # Departures (only if current phase matches)
    if current_phase == active_direction:
        # ... record departing cars
    
    # Phase change logic
    if intersection.green_timer == 0:
        current_phase_idx += 1
        # Fuzzy logic sets new green_timer
    
    frames.append(frame)

# Save
with open("simulation_data.json", "w") as f:
    json.dump({"metadata": {...}, "frames": frames}, f, indent=2)
```

---

## Calculating Wait Times (For Paper Stats)

Track when each car spawns and departs to calculate wait times:

```python
# Track spawn times
car_spawn_times = {}  # car_id -> spawn_time

# Track wait times
wait_times = []

for t in range(simulation_duration):
    # When car spawns, record spawn time
    for event in car_events:
        if event["event"] == "spawn":
            car_spawn_times[event["car_id"]] = t
    
    # When car departs, calculate wait time
    for departure in departures:
        car_id = departure["car_id"]
        spawn_t = car_spawn_times[car_id]
        wait_time = t - spawn_t
        wait_times.append(wait_time)

# Calculate statistics
average_wait = sum(wait_times) / len(wait_times)
max_wait = max(wait_times)
min_wait = min(wait_times)
```

### Add Stats to Metadata

```json
{
  "metadata": {
    "traffic_mode": "fuzzy",
    "simulation_duration": 100,
    "total_cars_processed": 85,
    "average_wait_time": 12.5,
    "max_wait_time": 45,
    "min_wait_time": 2,
    "throughput_per_cycle": 21.3
  }
}
```

### Comparing Fixed vs Fuzzy

Run simulation twice with different modes:

| Metric | Fixed Timer | Fuzzy Logic |
|--------|-------------|-------------|
| Avg Wait Time | 18.2s | 12.5s |
| Max Wait Time | 60s | 45s |
| Throughput | 72 cars | 85 cars |

Use these stats to create graphs for the paper!

---

## Questions?

Ask Member C if you need clarification!
