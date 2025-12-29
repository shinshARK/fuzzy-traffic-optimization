import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_system():
    """
    Membuat dan mengembalikan sistem fuzzy logic
    untuk mengatur durasi perpanjangan lampu hijau
    berdasarkan kondisi lalu lintas.

    Output:
        ControlSystemSimulation
    """
    
    # =========================
    # INPUT (ANTECEDENTS)
    # =========================
    
    # Jumlah kendaraan dalam antrian (0–60 mobil)
    queue = ctrl.Antecedent(np.arange(0, 61, 1), 'queue')
    
    # Laju kedatangan kendaraan (misalnya mobil/menit)
    arrival = ctrl.Antecedent(np.arange(0, 11, 1), 'arrival')
    
    # =========================
    # OUTPUT (CONSEQUENT)
    # =========================
    
    # Durasi perpanjangan lampu hijau (dalam detik)
    extension = ctrl.Consequent(np.arange(0, 61, 1), 'extension')

    # =========================
    # MEMBERSHIP FUNCTIONS
    # =========================
    
    # --- Queue (jumlah antrian) ---
    # short  : antrian sedikit
    # medium : antrian sedang
    # long   : antrian panjang
    queue['short'] = fuzz.trimf(queue.universe, [0, 0, 20])
    queue['medium'] = fuzz.trimf(queue.universe, [15, 30, 45])
    queue['long'] = fuzz.trimf(queue.universe, [40, 60, 60])

    # --- Arrival (laju kedatangan kendaraan) ---
    # low    : kendaraan datang lambat
    # medium : kendaraan datang sedang
    # high   : kendaraan datang cepat
    arrival['low'] = fuzz.trimf(arrival.universe, [0, 0, 4])
    arrival['medium'] = fuzz.trimf(arrival.universe, [2, 5, 8])
    arrival['high'] = fuzz.trimf(arrival.universe, [6, 10, 10])

     # --- Extension (perpanjangan lampu hijau) ---
    # short  : perpanjangan singkat
    # medium : perpanjangan sedang
    # long   : perpanjangan lama
    extension['short']  = fuzz.trimf(extension.universe, [0, 0, 20])
    extension['medium'] = fuzz.trimf(extension.universe, [15, 30, 45])
    extension['long']   = fuzz.trimf(extension.universe, [35, 45, 55])
    
    # =========================
    # FUZZY RULE BASE
    # =========================
    # Aturan dibuat berdasarkan logika lalu lintas:
    #
    # Queue \ Arrival | Low     | Medium  | High
    # Short           | Short   | Short   | Medium
    # Medium          | Medium  | Medium  | Medium
    # Long            | Medium  | Long    | Long
    rules = [
        # Antrian pendek
        ctrl.Rule(queue['short'] & arrival['low'], extension['short']),
        ctrl.Rule(queue['short'] & arrival['medium'], extension['short']),
        ctrl.Rule(queue['short'] & arrival['high'], extension['medium']),
        
        # Antrian sedang
        ctrl.Rule(queue['medium'] & arrival['low'], extension['medium']),
        ctrl.Rule(queue['medium'] & arrival['medium'], extension['medium']),
        ctrl.Rule(queue['medium'] & arrival['high'], extension['medium']),
        
        # Antrian panjang
        ctrl.Rule(queue['long'] & arrival['low'], extension['medium']),
        ctrl.Rule(queue['long'] & arrival['medium'], extension['long']),
        ctrl.Rule(queue['long'] & arrival['high'], extension['long']),
    ]

    # =========================
    # BUILD & RETURN SYSTEM
    # =========================
    
    # Membuat sistem kontrol fuzzy
    traffic_ctrl = ctrl.ControlSystem(rules)
    
    # Membuat simulator untuk menjalankan inferensi fuzzy
    traffic_sim = ctrl.ControlSystemSimulation(traffic_ctrl)
    
    return traffic_sim
