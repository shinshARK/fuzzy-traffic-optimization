import pytest
from src.intersection import Intersection

def test_intersection_initialization():
    intersection = Intersection()
    # Pastikan default queue kosong
    assert intersection.queues == {'N': 0, 'S': 0, 'E': 0, 'W': 0}
    assert intersection.green_timer == 0
    # Update: Default phase sekarang 'N' (sesuai kode Intersection terbaru)
    assert intersection.current_phase == 'N'

def test_add_cars():
    intersection = Intersection()
    intersection.add_cars('N', 5)
    assert intersection.queues['N'] == 5
    intersection.add_cars('E', 3)
    assert intersection.queues['E'] == 3
    
    # Cek error handling
    with pytest.raises(ValueError):
        intersection.add_cars('Invalid', 1)

def test_traffic_light_control():
    intersection = Intersection()
    
    # Update: Test fase tunggal (Single Phase)
    intersection.set_green_light(10, 'S')
    assert intersection.current_phase == 'S'
    assert intersection.green_timer == 10
    
    # Update: 'NS' atau 'EW' sekarang harus dianggap Error
    with pytest.raises(ValueError):
        intersection.set_green_light(10, 'NS') 
    
    with pytest.raises(ValueError):
        intersection.set_green_light(10, 'Invalid')

def test_step_logic_4_phase():
    """
    Test logika pergerakan untuk sistem 4 Fase (N -> S -> E -> W).
    Hanya satu arah yang boleh jalan dalam satu waktu.
    """
    intersection = Intersection()
    
    # 1. Isi semua antrian
    intersection.add_cars('N', 10)
    intersection.add_cars('S', 10)
    intersection.add_cars('E', 10)
    intersection.add_cars('W', 10)
    
    # 2. Set Lampu Hijau untuk 'N' saja
    intersection.set_green_light(5, 'N')
    
    # 3. Jalankan Step (Simulasi 1 detik)
    # Rate = 2 mobil/detik
    departed = intersection.step(departure_rate=2)
    
    # EXPECTATION:
    # 'N' berkurang 2 (jadi 8)
    assert intersection.queues['N'] == 8
    # 'S', 'E', 'W' HARUS TETAP 10 (karena merah)
    assert intersection.queues['S'] == 10
    assert intersection.queues['E'] == 10
    assert intersection.queues['W'] == 10
    
    # Cek timer berkurang
    assert intersection.green_timer == 4
    
    # Cek return value (dictionary mobil yang keluar)
    assert departed['N'] == 2
    assert departed['S'] == 0

def test_step_timer_exhaustion():
    """Test apakah timer berhenti di 0 dan mobil berhenti bergerak."""
    intersection = Intersection()
    intersection.add_cars('N', 5)
    intersection.set_green_light(2, 'N') # Cuma 2 detik
    
    # Detik 1
    intersection.step(departure_rate=1)
    assert intersection.queues['N'] == 4
    assert intersection.green_timer == 1
    
    # Detik 2
    intersection.step(departure_rate=1)
    assert intersection.queues['N'] == 3
    assert intersection.green_timer == 0
    
    # Detik 3 (Lampu sudah merah/habis) -> Mobil tidak boleh keluar
    departed = intersection.step(departure_rate=1)
    assert intersection.queues['N'] == 3 # Tetap 3
    assert departed['N'] == 0