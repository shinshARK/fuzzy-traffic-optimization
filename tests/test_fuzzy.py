import pytest
from src.fuzzy_brain import create_fuzzy_system

def test_fuzzy_system_creation():
    sim = create_fuzzy_system()
    assert sim is not None

def test_fuzzy_inference_basic():
    sim = create_fuzzy_system()
    
    # Case: Long Queue -> Long Extension
    sim.input['queue'] = 45
    sim.input['arrival'] = 8
    sim.compute()
    
    output = sim.output['extension']
    assert output > 30 # Should be in medium/long range
