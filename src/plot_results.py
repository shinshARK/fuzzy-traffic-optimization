import json
import matplotlib.pyplot as plt
import numpy as np

def load_data(filename):
    """Membaca file JSON hasil simulasi"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' tidak ditemukan.")
        print("   Pastikan Anda sudah menjalankan 'python -m src.simulation' dulu!")
        return None

def calculate_total_queue(frames):
    """Menghitung total antrian (N+S+E+W) di setiap detik"""
    total_queues = []
    timestamps = []
    
    for frame in frames:
        t = frame['t']
        q = frame['traffic_state']['queues']
        total = q['N'] + q['S'] + q['E'] + q['W']
        
        timestamps.append(t)
        total_queues.append(total)
        
    return timestamps, total_queues

def plot_comparison(fixed_data, fuzzy_data):
    """Membuat grafik perbandingan"""
    
    # 1. Siapkan Data Antrian
    t_fixed, q_fixed = calculate_total_queue(fixed_data['frames'])
    t_fuzzy, q_fuzzy = calculate_total_queue(fuzzy_data['frames'])
    
    # 2. Siapkan Data Waktu Tunggu (dari Metadata)
    wait_fixed = fixed_data['metadata']['avg_wait_time']
    wait_fuzzy = fuzzy_data['metadata']['avg_wait_time']
    
    # --- SETUP PLOT (2 Subplots) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Perbandingan Kinerja: Fixed Timer vs Fuzzy Logic', fontsize=16)
    
    # --- GRAPH 1: QUEUE LENGTH VS TIME (Line Chart) ---
    ax1.plot(t_fixed, q_fixed, label='Fixed Timer (30s)', color='blue', alpha=0.7, linewidth=2)
    ax1.plot(t_fuzzy, q_fuzzy, label='Fuzzy Adaptive', color='red', alpha=0.8, linewidth=2)
    
    ax1.set_title('Total Panjang Antrian per Waktu')
    ax1.set_xlabel('Waktu Simulasi (detik)')
    ax1.set_ylabel('Jumlah Mobil Mengantri (Total)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Highlight area dimana Fuzzy lebih baik
    ax1.fill_between(t_fixed, q_fixed, q_fuzzy, where=(np.array(q_fixed) > np.array(q_fuzzy)), 
                     interpolate=True, color='green', alpha=0.1, label='Efisiensi Fuzzy')

    # --- GRAPH 2: AVERAGE WAIT TIME (Bar Chart) ---
    labels = ['Fixed Timer', 'Fuzzy Logic']
    values = [wait_fixed, wait_fuzzy]
    colors = ['blue', 'red']
    
    bars = ax2.bar(labels, values, color=colors, alpha=0.7, width=0.5)
    
    ax2.set_title('Rata-rata Waktu Tunggu (Lebih Rendah Lebih Baik)')
    ax2.set_ylabel('Detik')
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Tambahkan angka di atas batang
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f} s',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Hitung persentase improvement
    improvement = ((wait_fixed - wait_fuzzy) / wait_fixed) * 100
    ax2.text(0.5, 0.9, f'Peningkatan: {improvement:.1f}%', 
             transform=ax2.transAxes, ha='center', color='green', fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='green'))

    # --- SAVE ---
    plt.tight_layout()
    output_filename = 'docs/results_graph.png'
    plt.savefig(output_filename, dpi=300)
    print(f"\n✅ Grafik berhasil disimpan ke '{output_filename}'")
    
    # Show plot (opsional, kalau mau langsung lihat pop-up)
    # plt.show()

if __name__ == "__main__":
    print("--- Membuat Grafik Visualisasi ---")
    
    # Load Data
    print("📂 Membaca data JSON...")
    data_fixed = load_data('docs/simulation_data_fixed.json')
    data_fuzzy = load_data('docs/simulation_data_fuzzy.json')
    
    if data_fixed and data_fuzzy:
        plot_comparison(data_fixed, data_fuzzy)