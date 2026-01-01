import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. HELPER FUNCTIONS (LOAD & EXTRACT DATA) ---

def load_data(filename):
    try:
        with open(filename, 'r') as f: return json.load(f)
    except: return None

def extract_phase_history(data):
    """
    Mengekstrak urutan pergantian lampu untuk Timeline & Histogram.
    Returns: list of dict {'start_time': t, 'phase': 'N', 'duration': 30}
    """
    history = []
    prev_phase = None
    
    for frame in data['frames']:
        t = frame['t']
        state = frame['traffic_state']
        curr_phase = state['current_phase']
        timer = state['green_timer']
        
        # Deteksi perubahan fase
        if curr_phase != prev_phase:
            history.append({
                'start_time': t,
                'phase': curr_phase,
                'duration': timer
            })
            prev_phase = curr_phase
    return history

def get_wait_times(data):
    """Menghitung waktu tunggu individu setiap mobil untuk Boxplot"""
    spawn_times = {}
    wait_times = []
    
    for frame in data['frames']:
        t = frame['t']
        # Catat spawn time
        for event in frame['car_events']:
            if event['event'] == 'spawn':
                spawn_times[event['car_id']] = t
        # Hitung wait time saat departure
        for dep in frame['departures']:
            cid = dep['car_id']
            if cid in spawn_times:
                wait_times.append(t - spawn_times[cid])
    return wait_times

# --- 2. PLOTTING FUNCTIONS ---

def plot_all_analysis(fixed_data, fuzzy_data):
    print("🚀 Sedang men-generate 4 Grafik Analisis...")

    # Siapkan Data
    hist_fixed = extract_phase_history(fixed_data)
    hist_fuzzy = extract_phase_history(fuzzy_data)
    
    durations_fixed = [h['duration'] for h in hist_fixed]
    durations_fuzzy = [h['duration'] for h in hist_fuzzy]
    
    waits_fixed = get_wait_times(fixed_data)
    waits_fuzzy = get_wait_times(fuzzy_data)
    
    # Warna Konsisten untuk Arah
    color_map = {'N': 'blue', 'S': 'red', 'E': 'green', 'W': 'orange'}

    # ==========================================
    # GRAFIK 1: TIMELINE CHART (Kronologis)
    # ==========================================
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig1.suptitle('Analisis Kronologis: Pola Durasi Lampu Hijau', fontsize=16)

    def plot_timeline_bars(ax, history, title):
        times = [h['start_time'] for h in history]
        durs = [h['duration'] for h in history]
        cols = [color_map[h['phase']] for h in history]
        
        bars = ax.bar(times, durs, color=cols, width=2.0, alpha=0.7, align='edge')
        
        # Labeli durasi jika cukup tinggi
        for rect in bars:
            height = rect.get_height()
            if height > 5:
                ax.text(rect.get_x() + rect.get_width()/2.0, height, f'{int(height)}', 
                        ha='center', va='bottom', fontsize=7)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_ylabel('Durasi (Detik)')
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)

    plot_timeline_bars(ax1, hist_fixed, "Mode FIXED (Pola Statis)")
    plot_timeline_bars(ax2, hist_fuzzy, "Mode FUZZY (Pola Dinamis Adaptif)")
    ax2.set_xlabel('Waktu Simulasi (detik)')
    
    # Legenda Arah
    patches = [mpatches.Patch(color=c, label=f"Arah {p}") for p, c in color_map.items()]
    fig1.legend(handles=patches, loc='upper right')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('docs/analysis_1_timeline.png', dpi=300)
    print("✅ [1/4] Saved: analysis_1_timeline.png")

    # ==========================================
    # GRAFIK 2: HISTOGRAM (Distribusi Adaptabilitas)
    # ==========================================
    plt.figure(figsize=(10, 6))
    plt.hist(durations_fixed, bins=15, alpha=0.6, label='Fixed', color='blue', density=False)
    plt.hist(durations_fuzzy, bins=15, alpha=0.6, label='Fuzzy', color='red', density=False)
    plt.title('Distribusi Durasi Lampu Hijau')
    plt.xlabel('Durasi Lampu (Detik)')
    plt.ylabel('Frekuensi Kejadian')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('docs/analysis_2_histogram.png', dpi=300)
    print("✅ [2/4] Saved: analysis_2_histogram.png")

    # ==========================================
    # GRAFIK 3: BOXPLOT (Fairness / Outlier)
    # ==========================================
    plt.figure(figsize=(8, 6))
    plt.boxplot([waits_fixed, waits_fuzzy], labels=['Fixed Timer', 'Fuzzy Logic'], 
                patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=2))
    plt.title('Sebaran Waktu Tunggu (Deteksi Outlier)')
    plt.ylabel('Waktu Tunggu (Detik)')
    plt.grid(True, axis='y', alpha=0.3)
    plt.savefig('docs/analysis_3_boxplot.png', dpi=300)
    print("✅ [3/4] Saved: analysis_3_boxplot.png")

    # ==========================================
    # GRAFIK 4: QUEUE DYNAMICS (Load Balancing)
    # ==========================================
    frames = fuzzy_data['frames']
    t = [f['t'] for f in frames]
    q_n = [f['traffic_state']['queues']['N'] for f in frames]
    q_s = [f['traffic_state']['queues']['S'] for f in frames]
    q_e = [f['traffic_state']['queues']['E'] for f in frames]
    q_w = [f['traffic_state']['queues']['W'] for f in frames]

    plt.figure(figsize=(12, 6))
    plt.plot(t, q_n, label='North', color='blue', alpha=0.7)
    plt.plot(t, q_s, label='South', color='red', alpha=0.7)
    plt.plot(t, q_e, label='East', color='green', alpha=0.7)
    plt.plot(t, q_w, label='West', color='orange', alpha=0.7)
    plt.title('Dinamika Antrian per Arah (Mode Fuzzy)')
    plt.xlabel('Waktu (detik)')
    plt.ylabel('Panjang Antrian')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('docs/analysis_4_queues.png', dpi=300)
    print("✅ [4/4] Saved: analysis_4_queues.png")

if __name__ == "__main__":
    d_fixed = load_data('docs/simulation_data_fixed.json')
    d_fuzzy = load_data('docs/simulation_data_fuzzy.json')
    
    if d_fixed and d_fuzzy:
        plot_all_analysis(d_fixed, d_fuzzy)
    else:
        print("❌ Error: File JSON data tidak ditemukan. Jalankan simulation.py dulu!")