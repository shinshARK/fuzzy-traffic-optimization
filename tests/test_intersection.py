import pytest
from src.intersection import Intersection

def test_intersection_initialization():
    intersection = Intersection()
    assert intersection.queues == {'N': 0, 'S': 0, 'E': 0, 'W': 0}
    assert intersection.green_timer == 0
    assert intersection.current_phase == 'NS'

def test_add_cars():
    intersection = Intersection()
    intersection.add_cars('N', 5)
    assert intersection.queues['N'] == 5
    intersection.add_cars('E', 3)
    assert intersection.queues['E'] == 3
    
    with pytest.raises(ValueError):
        intersection.add_cars('Invalid', 1)

def test_traffic_light_control():
    intersection = Intersection()
    intersection.set_green_light(10, 'EW')
    assert intersection.current_phase == 'EW'
    assert intersection.green_timer == 10
    
    with pytest.raises(ValueError):
        intersection.set_green_light(10, 'Invalid')

def test_step_logic():
    intersection = Intersection()
    # Add cars to all directions
    intersection.add_cars('N', 10)
    intersection.add_cars('S', 10)
    intersection.add_cars('E', 10)
    intersection.add_cars('W', 10)
    
    # Set Green for NS
    intersection.set_green_light(5, 'NS')
    
    # Step 1: NS should move, EW should stay
    intersection.step(departure_rate=2)
    assert intersection.queues['N'] == 8
    assert intersection.queues['S'] == 8
    assert intersection.queues['E'] == 10
    assert intersection.queues['W'] == 10
    assert intersection.green_timer == 4
    
    # Run until timer 0
    for _ in range(4):
        intersection.step(departure_rate=2)
        
    assert intersection.queues['N'] == 0
    assert intersection.queues['S'] == 0
    assert intersection.green_timer == 0
    
    # Timer is 0, no one should move
    intersection.step(departure_rate=2)
    assert intersection.queues['E'] == 10 # Still waiting
