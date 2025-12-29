import json
import random
import numpy as np
from collections import deque
from src.traffic_gen import generate_arrivals
from src.intersection import Intersection

# --- KONFIGURASI SIMULASI ---
SIMULATION_DURATION = 100  # Lebih pendek untuk tes JSON
ARRIVAL_RATE = 0.4         # Lambda
DEPARTURE_RATE = 1         # Mu

# --- KONFIGURASI FASE (4 PHASE SYSTEM) ---
PHASE_ORDER = ['N', 'S', 'E', 'W']

def get_destination_and_intent(origin):
    """
    Menentukan tujuan berdasarkan arah asal (origin) dan niat (intent).
    Menggunakan urutan Clockwise (N-E-S-W) untuk perhitungan yang akurat.
    """
    opts = ['straight', 'left', 'right']
    probs = [0.6, 0.2, 0.2] # 60% Lurus
    intent = np.random.choice(opts, p=probs)
    
    # PENTING: Urutan harus Clockwise (Jarum Jam)
    compass = ['N', 'E', 'S', 'W']
    
    if origin not in compass:
        raise ValueError(f"Invalid origin: {origin}")
        
    current_idx = compass.index(origin)
    
    # Logika Navigasi
    if intent == 'straight':
        # Lurus = Seberang jalan (Index + 2)
        dest_idx = (current_idx + 2) % 4
    elif intent == 'left':
        # Belok Kiri = Arah selanjutnya dalam jarum jam (Index + 1)
        # Contoh: Dari N (Utara) belok kiri bagi pengemudi adalah ke E (Timur) di sistem koordinat ini
        # *Catatan: Ini tergantung sistem lajur (kiri/kanan), tapi untuk topologi graf sederhana:
        dest_idx = (current_idx + 1) % 4 
    else: # right
        # Belok Kanan = Arah sebelumnya (Index - 1)
        dest_idx = (current_idx - 1) % 4
        
    destination = compass[dest_idx]
        
    return destination, intent

def run_simulation():
    print(f"--- Memulai Simulasi (Export Mode) ---")
    
    intersection = Intersection()
    intersection.set_green_light(15, 'N') # Start Phase N
    
    # Data Structures untuk JSON Export
    frames = []
    
    # Tracking ID Mobil: Kita butuh antrian ID terpisah dari hitungan matematika
    # Format: queue_ids['N'] = ['N_1', 'N_2', ...]
    queue_ids = {k: deque() for k in ['N', 'S', 'E', 'W']} 
    car_counters = {k: 0 for k in ['N', 'S', 'E', 'W']} # Untuk generate ID unik
    
    current_phase_idx = 0

    for t in range(SIMULATION_DURATION):
        
        # --- 1. PREPARE FRAME DATA ---
        frame = {
            "t": t,
            "traffic_state": {
                "current_phase": intersection.current_phase,
                "green_timer": intersection.green_timer,
                "queues": intersection.queues.copy() # Copy agar nilai tidak berubah
            },
            "car_events": [],
            "departures": []
        }
        
        # --- 2. GENERATE ARRIVALS ---
        arrivals = {}
        for direction in ['N', 'S', 'E', 'W']:
            count = generate_arrivals(ARRIVAL_RATE)
            arrivals[direction] = count
            
            # Tambahkan ke Intersection (Math Logic)
            intersection.add_cars(direction, count)
            
            # Tambahkan ke Tracking ID (Log Logic)
            current_q_len = len(queue_ids[direction]) # Posisi antrian mobil baru
            
            for i in range(count):
                car_counters[direction] += 1
                car_id = f"{direction}_{car_counters[direction]}"
                
                # Generate Metadata
                dest, intent = get_destination_and_intent(direction)
                
                # --- PERBAIKAN DI SINI ---
                # Simpan ID DAN Destination ke dalam antrian memori
                car_info = {
                    "id": car_id,
                    "destination": dest,
                    "intent": intent # Opsional, kalau mau track intent saat keluar juga
                }
                queue_ids[direction].append(car_info)
                # -------------------------
                
                # Masukkan ke event log (JSON)
                frame["car_events"].append({
                    "car_id": car_id,
                    "event": "spawn",
                    "origin": direction,
                    "destination": dest,   # Ini sudah benar
                    "intent": intent,      # Ini sudah benar
                    "queue_position": current_q_len + i
                })

        # --- 3. PROCESS STEP & DEPARTURES ---
        # Step sekarang mengembalikan info berapa mobil yang keluar
        departed_counts = intersection.step(departure_rate=DEPARTURE_RATE)
        
        # Proses ID mobil yang keluar (FIFO)
        for direction, count in departed_counts.items():
            for _ in range(count):
                if queue_ids[direction]:
                    # --- PERBAIKAN DI SINI ---
                    # Ambil paket info mobil yang paling depan
                    car_data = queue_ids[direction].popleft()
                    
                    frame["departures"].append({
                        "car_id": car_data["id"],      # Ambil ID dari paket
                        "origin": direction,
                        "destination": car_data["destination"] # Ambil Destinasi dari paket
                    })
                    # -------------------------

        # --- 4. PHASE SWITCHING (4-PHASE CYCLE) ---
        if intersection.green_timer <= 0:
            current_phase_idx = (current_phase_idx + 1) % 4
            next_phase = PHASE_ORDER[current_phase_idx]
            
            # --- FUZZY LOGIC HOOK (Nanti di sini) ---
            duration = 15 # Fixed for now
            
            intersection.set_green_light(duration, next_phase)
            
        # Simpan Frame
        frames.append(frame)
        
        # Print progress tipis-tipis
        if t % 10 == 0:
            print(f"Time {t}: {intersection.queues}")

    # --- 5. EXPORT JSON ---
    output_data = {
        "metadata": {
            "simulation_duration": SIMULATION_DURATION,
            "phase_order": PHASE_ORDER,
            "traffic_mode": "fuzzy_ready" # Placeholder name
        },
        "frames": frames
    }
    
    with open("simulation_data.json", "w") as f:
        json.dump(output_data, f, indent=2)
        
    print("\n✅ Data exported to simulation_data.json")

if __name__ == "__main__":
    run_simulation()