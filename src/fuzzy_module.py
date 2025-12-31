import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- BAGIAN 1: LOGIKA FUZZY MEMBER B ---
def create_fuzzy_system():
    """Membangun sistem fuzzy logic (Otak)."""
    # 1. INPUT
    queue = ctrl.Antecedent(np.arange(0, 81, 1), 'queue') 
    arrival = ctrl.Antecedent(np.arange(0, 11, 1), 'arrival')
    
    # 2. OUTPUT
    extension = ctrl.Consequent(np.arange(0, 61, 1), 'extension')

    # 3. MEMBERSHIP FUNCTIONS
    queue['short']  = fuzz.trimf(queue.universe, [0, 0, 20])
    queue['medium'] = fuzz.trimf(queue.universe, [15, 30, 45])
    queue['long']   = fuzz.trimf(queue.universe, [40, 80, 80])

    arrival['low']    = fuzz.trimf(arrival.universe, [0, 0, 4])
    arrival['medium'] = fuzz.trimf(arrival.universe, [2, 5, 8])
    arrival['high']   = fuzz.trimf(arrival.universe, [6, 10, 10])

    extension['short']  = fuzz.trimf(extension.universe, [0, 0, 20])
    extension['medium'] = fuzz.trimf(extension.universe, [15, 30, 45])
    extension['long']   = fuzz.trimf(extension.universe, [35, 60, 60])
    
    # 4. RULES
    rules = [
        ctrl.Rule(queue['short'] & arrival['low'], extension['short']),
        ctrl.Rule(queue['short'] & arrival['medium'], extension['short']),
        ctrl.Rule(queue['short'] & arrival['high'], extension['medium']),
        
        ctrl.Rule(queue['medium'] & arrival['low'], extension['medium']),
        ctrl.Rule(queue['medium'] & arrival['medium'], extension['medium']),
        ctrl.Rule(queue['medium'] & arrival['high'], extension['medium']),
        
        ctrl.Rule(queue['long'] & arrival['low'], extension['medium']),
        ctrl.Rule(queue['long'] & arrival['medium'], extension['long']),
        ctrl.Rule(queue['long'] & arrival['high'], extension['long']),
    ]

    # 5. CONTROL SYSTEM
    traffic_ctrl = ctrl.ControlSystem(rules)
    traffic_sim = ctrl.ControlSystemSimulation(traffic_ctrl)
    return traffic_sim

# --- BAGIAN 2: JEMBATAN KE SIMULATION.PY ---
_FUZZY_SYSTEM = None

def get_green_duration(current_queue: int, arrival_rate: float) -> int:
    global _FUZZY_SYSTEM
    if _FUZZY_SYSTEM is None:
        _FUZZY_SYSTEM = create_fuzzy_system()
    
    safe_queue = min(current_queue, 80)
    safe_arrival = min(arrival_rate * 10, 10) 
    
    _FUZZY_SYSTEM.input['queue'] = safe_queue
    _FUZZY_SYSTEM.input['arrival'] = safe_arrival
    
    try:
        _FUZZY_SYSTEM.compute()
        duration = _FUZZY_SYSTEM.output['extension']
    except:
        duration = 15
        
    return int(duration)