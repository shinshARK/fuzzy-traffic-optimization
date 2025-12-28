import numpy as np

def generate_arrivals(lambda_rate: float) -> int:
    """
    Generate the number of car arrivals based on a Poisson distribution.
    
    Args:
        lambda_rate (float): The average number of arrivals per time step.
        
    Returns:
        int: The number of cars arriving.
    """
    if lambda_rate < 0:
        raise ValueError("Lambda rate must be non-negative.")
    return int(np.random.poisson(lambda_rate))
