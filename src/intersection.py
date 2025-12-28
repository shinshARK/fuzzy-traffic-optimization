class Intersection:
    def __init__(self):
        """
        Initialize the Intersection with 4 queues (N, S, E, W) and default state.
        """
        self.queues: dict[str, int] = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.green_timer: int = 0
        self.current_phase: str = 'NS' # 'NS' or 'EW'

    def add_cars(self, direction: str, count: int):
        """
        Add cars to a specific queue.
        
        Args:
            direction (str): 'N', 'S', 'E', or 'W'.
            count (int): Number of cars to add.
        """
        if count < 0:
            raise ValueError("Cannot add negative cars.")
        if direction not in self.queues:
            raise ValueError(f"Invalid direction: {direction}")
            
        self.queues[direction] += count

    def set_green_light(self, duration: int, phase: str):
        """
        Set the traffic light to green for a specific phase.
        
        Args:
            duration (int): Time in seconds.
            phase (str): 'NS' or 'EW'.
        """
        if phase not in ['NS', 'EW']:
            raise ValueError("Invalid phase. Must be 'NS' or 'EW'.")
            
        self.current_phase = phase
        self.green_timer = duration

    def step(self, departure_rate: int = 1):
        """
        Advance the simulation by one time step.
        Reduces queues for the active phase.
        """
        # Determine active queues based on phase
        active_dirs = []
        if self.green_timer > 0:
            if self.current_phase == 'NS':
                active_dirs = ['N', 'S']
            elif self.current_phase == 'EW':
                active_dirs = ['E', 'W']

        # Departures
        for direction in active_dirs:
            departed = min(self.queues[direction], departure_rate)
            self.queues[direction] -= departed
        
        # Timer logic
        if self.green_timer > 0:
            self.green_timer -= 1
