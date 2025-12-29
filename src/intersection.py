class Intersection:
    def __init__(self):
        """
        Initialize the Intersection with 4 queues (N, S, E, W) and default state.
        """
        self.queues: dict[str, int] = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.green_timer: int = 0
        self.current_phase: str = 'N'  # Default start phase

    def add_cars(self, direction: str, count: int):
        """Add cars to a specific queue."""
        if count < 0:
            raise ValueError("Cannot add negative cars.")
        if direction not in self.queues:
            raise ValueError(f"Invalid direction: {direction}")
            
        self.queues[direction] += count

    def set_green_light(self, duration: int, phase: str):
        """
        Set the traffic light to green for a specific phase.
        Phase order typically: N -> S -> E -> W
        """
        valid_phases = ['N', 'S', 'E', 'W']
        if phase not in valid_phases:
            raise ValueError(f"Invalid phase. Must be one of {valid_phases}")
            
        self.current_phase = phase
        self.green_timer = duration

    def step(self, departure_rate: int = 1) -> dict[str, int]:
        """
        Advance the simulation by one time step.
        Returns a dictionary of departed cars count per direction.
        e.g., {'N': 1, 'S': 0, ...}
        """
        departed_counts = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        
        # Determine active queues based on 4-Phase System
        # Only the direction matching the current_phase gets to go
        if self.green_timer > 0:
            active_dir = self.current_phase  # 'N', 'S', 'E', or 'W'
            
            # Logic: Departure
            if self.queues[active_dir] > 0:
                count = min(self.queues[active_dir], departure_rate)
                self.queues[active_dir] -= count
                departed_counts[active_dir] = count
                
            # Decrease Timer
            self.green_timer -= 1
            
        return departed_counts