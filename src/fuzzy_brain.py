import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_system():
    """
    Define the fuzzy logic system for traffic control.
    
    Returns:
        ControlSystemSimulation: The fuzzy control system.
    """
    # Antecedents (Inputs)
    queue = ctrl.Antecedent(np.arange(0, 51, 1), 'queue')
    arrival = ctrl.Antecedent(np.arange(0, 11, 1), 'arrival')
    
    # Consequent (Output)
    extension = ctrl.Consequent(np.arange(0, 61, 1), 'extension')

    # Membership Functions
    # Queue: Short, Medium, Long
    queue['short'] = fuzz.trimf(queue.universe, [0, 0, 20])
    queue['medium'] = fuzz.trimf(queue.universe, [10, 25, 40])
    queue['long'] = fuzz.trimf(queue.universe, [30, 50, 50])

    # Arrival: Low, Medium, High
    arrival['low'] = fuzz.trimf(arrival.universe, [0, 0, 4])
    arrival['medium'] = fuzz.trimf(arrival.universe, [2, 5, 8])
    arrival['high'] = fuzz.trimf(arrival.universe, [6, 10, 10])

    # Extension: Short, Medium, Long
    extension['short'] = fuzz.trimf(extension.universe, [0, 0, 20])
    extension['medium'] = fuzz.trimf(extension.universe, [10, 30, 50])
    extension['long'] = fuzz.trimf(extension.universe, [40, 60, 60])

    # Rules (Placeholder for Day 2, but defining basic ones for structure)
    # Just to ensure system is valid
    rule1 = ctrl.Rule(queue['short'] & arrival['low'], extension['short'])
    rule2 = ctrl.Rule(queue['long'] | arrival['high'], extension['long'])
    rule3 = ctrl.Rule(queue['medium'], extension['medium'])

    traffic_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    traffic_sim = ctrl.ControlSystemSimulation(traffic_ctrl)
    
    return traffic_sim
