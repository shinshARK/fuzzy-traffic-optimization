import pytest
import numpy as np
from src.traffic_gen import generate_arrivals

def test_generate_arrivals_output_type():
    arrivals = generate_arrivals(5)
    assert isinstance(arrivals, int)

def test_generate_arrivals_non_negative():
    for _ in range(100):
        arrivals = generate_arrivals(5)
        assert arrivals >= 0

def test_generate_arrivals_negative_lambda():
    with pytest.raises(ValueError):
        generate_arrivals(-1)
