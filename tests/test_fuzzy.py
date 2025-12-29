import pytest
from src.fuzzy_brain import create_fuzzy_system

def test_fuzzy_system_creation():
    """
    Test dasar untuk memastikan sistem fuzzy
    berhasil dibuat tanpa error.

    Jika test ini gagal, berarti ada masalah
    pada definisi membership, rule, atau struktur sistem.
    """
    sim = create_fuzzy_system()
    assert sim is not None

def test_fuzzy_inference_50cars_45sec():
    """
    Skenario:
    - Queue panjang (50 mobil)
    - Arrival tinggi (8)
    
    Ekspektasi:
    - Sistem fuzzy memberikan perpanjangan lampu
      sekitar 45 detik (tidak terlalu rendah atau ekstrem).
    """
    sim = create_fuzzy_system()

    sim.input['queue'] = 50
    sim.input['arrival'] = 8
    sim.compute()

    output = sim.output['extension']
    
    # Print untuk melihat hasil inferensi saat pytest dijalankan
    print(
        f"\n[test_fuzzy_inference_50cars_45sec]\n"
        f"Queue    : 50\n"
        f"Arrival  : 8\n"
        f"Extension: {output:.2f} sec"
    )
    
    # Output harus berada di rentang target (±45 detik)
    assert 40 <= output <= 50


def test_fuzzy_inference_basic():
    """
    Test perilaku umum sistem.

    Skenario:
    - Queue relatif panjang (45)
    - Arrival tinggi (8)

    Ekspektasi:
    - Sistem menghasilkan perpanjangan minimal
      pada kategori medium hingga long.
    """
    sim = create_fuzzy_system()
    
    sim.input['queue'] = 45
    sim.input['arrival'] = 8
    sim.compute()
    
    output = sim.output['extension']

    print(
        f"[test_fuzzy_inference_basic] "
        f"Queue=45 Arrival=8 → Extension={output:.2f} sec"
    )
     # Tidak boleh terlalu pendek
    assert output > 30

def test_short_queue_low_arrival_short_extension():
    """
    Skenario lalu lintas lengang.

    - Queue sangat pendek (5)
    - Arrival rendah (2)

    Ekspektasi:
    - Tidak perlu perpanjangan lama
    - Output berada di kategori short
    """
    
    sim = create_fuzzy_system()

    sim.input['queue'] = 5
    sim.input['arrival'] = 2
    sim.compute()

    output = sim.output['extension']
    print(
        f"[test_short_queue_low_arrival_short_extension] "
        f"Queue=5 Arrival=2 → Extension={output:.2f} sec"
    )
    
    assert output <= 20
    
def test_medium_queue_medium_arrival_medium_extension():
    """
    Skenario lalu lintas normal.

    - Queue sedang (30)
    - Arrival sedang (5)

    Ekspektasi:
    - Sistem memberikan perpanjangan
      di kategori medium (tidak ekstrem).
    """
    
    sim = create_fuzzy_system()

    sim.input['queue'] = 30
    sim.input['arrival'] = 5
    sim.compute()

    output = sim.output['extension']
    
    print(
        f"[test_medium_queue_medium_arrival_medium_extension] "
        f"Queue=30 Arrival=5 → Extension={output:.2f} sec"
    )
    
    assert 20 < output < 40

def test_high_arrival_with_short_queue_not_extreme():
    """
    Edge case penting.

    - Arrival tinggi (8)
    - Queue pendek (10)

    Ekspektasi:
    - Sistem TIDAK langsung memberi perpanjangan maksimum
    - Output masih dalam batas wajar (medium).
    """
    sim = create_fuzzy_system()

    sim.input['queue'] = 10
    sim.input['arrival'] = 8
    sim.compute()

    output = sim.output['extension']
    print(
        f"[test_high_arrival_with_short_queue_not_extreme] "
        f"Queue=10 Arrival=8 → Extension={output:.2f} sec"
    )
    
    assert output < 45
    
def test_output_within_valid_range():
    """
    Test validasi batas sistem (safety test).

    - Queue maksimum (60)
    - Arrival maksimum (10)

    Ekspektasi:
    - Output tidak negatif
    - Output tidak melebihi batas maksimum (60 detik)
    """
    sim = create_fuzzy_system()

    sim.input['queue'] = 60
    sim.input['arrival'] = 10
    sim.compute()

    output = sim.output['extension']
    print(
        f"[test_output_within_valid_range] "
        f"Queue=60 Arrival=10 → Extension={output:.2f} sec"
    )
    assert 0 <= output <= 60

