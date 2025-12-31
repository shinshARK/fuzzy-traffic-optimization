import json
import numpy as np
from collections import deque
from src.traffic_gen import generate_arrivals
from src.intersection import Intersection
from src.fuzzy_module import get_green_duration

# --- KONFIGURASI GLOBAL ---
SIMULATION_DURATION = 300  # Durasi diperpanjang (5 menit) untuk data lebih valid
ARRIVAL_RATE = 0.4         # Lambda (Tingkat kepadatan traffic)
DEPARTURE_RATE = 1         # Mu
PHASE_ORDER = ['N', 'E', 'S', 'W']

def get_destination_and_intent(origin):
    opts = ['straight', 'left', 'right']
    probs = [0.6, 0.2, 0.2] 
    intent = np.random.choice(opts, p=probs)
    compass = ['N', 'E', 'S', 'W']
    current_idx = compass.index(origin)
    
    if intent == 'straight': dest_idx = (current_idx + 2) % 4
    elif intent == 'left':   dest_idx = (current_idx + 1) % 4 
    else:                    dest_idx = (current_idx - 1) % 4
    return compass[dest_idx], intent

def run_simulation(mode="FUZZY", fixed_duration=30):
    """
    Menjalankan simulasi dengan mode tertentu.
    mode: "FUZZY" atau "FIXED"
    fixed_duration: Detik lampu hijau jika mode FIXED (default 30s)
    """
    print(f"\n🚀 Memulai Simulasi Mode: {mode}...")
    
    intersection = Intersection()
    intersection.set_green_light(10, 'N') 
    
    frames = []
    queue_ids = {k: deque() for k in ['N', 'S', 'E', 'W']} 
    car_counters = {k: 0 for k in ['N', 'S', 'E', 'W']} 
    
    # --- STATISTIK METRICS ---
    wait_times = []      # Menyimpan waktu tunggu setiap mobil yang berhasil keluar
    total_cars_spawned = 0
    total_cars_departed = 0
    
    current_phase_idx = 0

    for t in range(SIMULATION_DURATION):
        
        frame = {
            "t": t,
            "traffic_state": {
                "current_phase": intersection.current_phase,
                "green_timer": intersection.green_timer,
                "queues": intersection.queues.copy()
            },
            "car_events": [],
            "departures": []
        }
        
        # --- 1. GENERATE ARRIVALS ---
        for direction in ['N', 'S', 'E', 'W']:
            count = generate_arrivals(ARRIVAL_RATE)
            intersection.add_cars(direction, count)
            
            total_cars_spawned += count
            current_q_len = len(queue_ids[direction])
            
            for i in range(count):
                car_counters[direction] += 1
                car_id = f"{direction}_{car_counters[direction]}"
                dest, intent = get_destination_and_intent(direction)
                
                # SIMPAN WAKTU KEDATANGAN (t) UNTUK HITUNG WAIT TIME
                car_info = {
                    "id": car_id,
                    "dest": dest,
                    "spawn_time": t  # <--- METRIC PENTING
                }
                queue_ids[direction].append(car_info)
                
                frame["car_events"].append({
                    "car_id": car_id,
                    "event": "spawn",
                    "origin": direction,
                    "destination": dest,
                    "intent": intent,
                    "queue_position": current_q_len + i
                })

        # --- 2. DEPARTURES & METRIC CALCULATION ---
        departed_counts = intersection.step(departure_rate=DEPARTURE_RATE)
        
        for direction, count in departed_counts.items():
            for _ in range(count):
                if queue_ids[direction]:
                    car_data = queue_ids[direction].popleft()
                    
                    # HITUNG WAITING TIME
                    wait_time = t - car_data["spawn_time"]
                    wait_times.append(wait_time)
                    total_cars_departed += 1
                    
                    frame["departures"].append({
                        "car_id": car_data["id"],
                        "origin": direction,
                        "destination": car_data["dest"]
                    })

        # --- 3. PHASE SWITCHING (DUAL MODE) ---
        if intersection.green_timer <= 0:
            current_phase_idx = (current_phase_idx + 1) % 4
            next_phase = PHASE_ORDER[current_phase_idx]
            
            # --- LOGIKA MODE ---
            if mode == "FUZZY":
                queue_next = intersection.queues[next_phase]
                # Panggil Fuzzy Module
                duration = get_green_duration(queue_next, ARRIVAL_RATE)
                duration = max(5, duration) # Safety clamp
            else:
                # Mode FIXED (Timer konvensional)
                duration = fixed_duration
            
            intersection.set_green_light(duration, next_phase)
            
        frames.append(frame)

    # --- 4. EXPORT JSON (Beda nama file per mode) ---
    filename = f"docs/simulation_data_{mode.lower()}.json"
    output_data = {
        "metadata": {
            "mode": mode,
            "duration": SIMULATION_DURATION,
            "avg_wait_time": np.mean(wait_times) if wait_times else 0
        },
        "frames": frames
    }
    with open(filename, "w") as f:
        json.dump(output_data, f, indent=2)

    # --- 5. RETURN STATS ---
    avg_wait = np.mean(wait_times) if wait_times else 0
    max_wait = np.max(wait_times) if wait_times else 0
    return {
        "mode": mode,
        "avg_wait": avg_wait,
        "max_wait": max_wait,
        "served": total_cars_departed,
        "leftover": sum(intersection.queues.values())
    }

if __name__ == "__main__":
    print("=== PERBANDINGAN PERFORMA  ===")
    
    # 1. Jalankan Skenario A: FIXED TIMER (misal 30 detik)
    stats_fixed = run_simulation(mode="FIXED", fixed_duration=30)
    
    # 2. Jalankan Skenario B: FUZZY LOGIC
    stats_fuzzy = run_simulation(mode="FUZZY")
    
    # 3. Print Hasil Head-to-Head
    print("\n" + "="*40)
    print(f"{'METRIC':<20} | {'FIXED (30s)':<12} | {'FUZZY (Adaptive)':<12}")
    print("-" * 50)
    print(f"{'Avg Wait Time':<20} | {stats_fixed['avg_wait']:<12.2f} | {stats_fuzzy['avg_wait']:<12.2f}")
    print(f"{'Max Wait Time':<20} | {stats_fixed['max_wait']:<12} | {stats_fuzzy['max_wait']:<12}")
    print(f"{'Cars Served':<20} | {stats_fixed['served']:<12} | {stats_fuzzy['served']:<12}")
    print(f"{'Queue Leftover':<20} | {stats_fixed['leftover']:<12} | {stats_fuzzy['leftover']:<12}")
    print("="*40)
    
    # Analisis Singkat
    diff = stats_fixed['avg_wait'] - stats_fuzzy['avg_wait']
    if diff > 0:
        print(f"\n✅ KESIMPULAN: Fuzzy Logic lebih cepat {diff:.2f} detik per mobil!")
    else:
        print(f"\n⚠️ KESIMPULAN: Fuzzy Logic belum optimal (atau traffic terlalu rendah).")