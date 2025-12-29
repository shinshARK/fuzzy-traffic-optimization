"""
Car class for Manim traffic visualization.
A car is represented as a labeled dot that can move through the intersection.
Supports queuing, straight movement, and curved turns.
"""
from manim import *
from dataclasses import dataclass
from typing import Literal

# Direction type
Direction = Literal["N", "S", "E", "W"]

# Queue spacing between cars
QUEUE_SPACING = 0.5

# Spawn positions (off-screen edges) for each direction
# In left-hand drive (Indonesia), cars drive on the LEFT side
SPAWN_POSITIONS: dict[str, tuple[float, float, float]] = {
    "N": (0.5, 5, 0),   # Coming from North, on right side of road (their left)
    "S": (-0.5, -5, 0), # Coming from South
    "E": (8, -0.5, 0),  # Coming from East
    "W": (-8, 0.5, 0),  # Coming from West
}

# Wait positions (stop line, just before intersection)
WAIT_POSITIONS: dict[str, tuple[float, float, float]] = {
    "N": (0.5, 1.5, 0),
    "S": (-0.5, -1.5, 0),
    "E": (1.5, -0.5, 0),
    "W": (-1.5, 0.5, 0),
}

# Exit positions (off-screen based on DESTINATION direction)
EXIT_POSITIONS: dict[str, tuple[float, float, float]] = {
    "N": (-0.5, 5, 0),   # Going TO North = exit UP
    "S": (0.5, -5, 0),   # Going TO South = exit DOWN
    "E": (8, 0.5, 0),    # Going TO East = exit RIGHT
    "W": (-8, -0.5, 0),  # Going TO West = exit LEFT
}

# Colors for each direction
DIRECTION_COLORS: dict[str, str] = {
    "N": BLUE,
    "S": RED,
    "E": GREEN,
    "W": ORANGE,
}

# Turn paths defined as a series of points through the intersection
# Format: (origin, destination) -> list of (x, y, z) waypoints
# Cars will travel: wait_position -> waypoints... -> exit_position
#
# LEFT-HAND DRIVE (Indonesia): Cars approach on the RIGHT side of the road
# From North: car is at x=0.5, going down
#   - Left turn (to West): curves LEFT through intersection
#   - Right turn (to East): goes forward deep, then curves RIGHT
#
# Note: queue_position handles multiple cars stacking behind each other

TURN_WAYPOINTS: dict[tuple[str, str], list[tuple]] = {
    # From North (car at x=0.5, y=1.5, going down)
    ("N", "S"): [(0.5, 0, 0)],                           # Straight
    ("N", "W"): [(0.5, -0.3, 0), (-0.5, -0.5, 0)],       # Left - wp2 more toward exit (x=-8)
    ("N", "E"): [(0.5, 0.8, 0), (0.5, 0.5, 0)],          # Right - turn early, stay on x=0.5
    
    # From South (car at x=-0.5, y=-1.5, going up)
    ("S", "N"): [(-0.5, 0, 0)],                          # Straight
    ("S", "E"): [(-0.5, 0.3, 0), (0.5, 0.5, 0)],         # Left - wp2 more toward exit (x=8)
    ("S", "W"): [(-0.5, -0.8, 0), (-0.5, -0.5, 0)],      # Right - turn early
    
    # From East (car at x=1.5, y=-0.5, going left)
    ("E", "W"): [(0, -0.5, 0)],                          # Straight
    ("E", "N"): [(-0.3, -0.5, 0), (-0.5, 0.5, 0)],       # Left - wp2 more toward exit (y=5)
    ("E", "S"): [(0.8, -0.5, 0), (0.5, -0.5, 0)],        # Right - turn early
    
    # From West (car at x=-1.5, y=0.5, going right)  
    ("W", "E"): [(0, 0.5, 0)],                           # Straight
    ("W", "S"): [(0.3, 0.5, 0), (0.5, -0.5, 0)],         # Left - wp2 more toward exit (y=-5)
    ("W", "N"): [(-0.8, 0.5, 0), (-0.5, 0.5, 0)],        # Right - turn early
}


def get_queue_offset(origin: str, queue_position: int) -> tuple[float, float, float]:
    """
    Calculate position offset for a car in queue.
    Cars stack away from the intersection based on their queue position.
    """
    offset_multipliers = {
        "N": (0, 1, 0),   # Stack upward (away from intersection)
        "S": (0, -1, 0),  # Stack downward
        "E": (1, 0, 0),   # Stack rightward
        "W": (-1, 0, 0),  # Stack leftward
    }
    mult = offset_multipliers[origin]
    return (
        mult[0] * queue_position * QUEUE_SPACING,
        mult[1] * queue_position * QUEUE_SPACING,
        0
    )


@dataclass
class CarData:
    """Data class holding car information."""
    car_id: str
    origin: Direction
    destination: Direction
    intent: str  # "straight", "left", "right"
    queue_position: int = 0


class Car(VGroup):
    """
    A car in the traffic simulation.
    Displayed as a colored dot with a label showing origin:queue_count.
    """
    
    def __init__(self, car_data: CarData, queue_count: int = 0, **kwargs):
        super().__init__(**kwargs)
        
        self.car_data = car_data
        self.car_id = car_data.car_id
        self.origin = car_data.origin
        self.destination = car_data.destination
        self.intent = car_data.intent
        self.queue_position = car_data.queue_position
        self.state = "spawned"  # spawned, approaching, waiting, crossing, exited
        
        # Calculate spawn position with queue offset
        base_spawn = SPAWN_POSITIONS[self.origin]
        offset = get_queue_offset(self.origin, self.queue_position)
        spawn_pos = (base_spawn[0] + offset[0], base_spawn[1] + offset[1], 0)
        
        # Create the dot (car body)
        self.dot = Dot(
            point=spawn_pos,
            radius=0.18,
            color=DIRECTION_COLORS[self.origin],
            fill_opacity=0.9
        )
        
        # Create label showing "N:5" (origin:queue_count)
        self.label = Text(
            f"{self.origin}:{queue_count}",
            font_size=12,
            color=WHITE
        ).move_to(self.dot.get_center())
        
        self.add(self.dot, self.label)
    
    def get_wait_position(self) -> np.ndarray:
        """Get the position where this car should wait, with queue offset."""
        base = WAIT_POSITIONS[self.origin]
        offset = get_queue_offset(self.origin, self.queue_position)
        return np.array([base[0] + offset[0], base[1] + offset[1], 0])
    
    def get_exit_position(self) -> np.ndarray:
        """Get the exit position based on destination."""
        return np.array(EXIT_POSITIONS[self.destination])
    
    def get_turn_path(self) -> VMobject:
        """
        Generate a smooth path through the intersection using waypoints.
        Returns a VMobject path for MoveAlongPath animation.
        """
        # Start from current position (should be at wait position)
        start = self.get_wait_position()
        end = self.get_exit_position()
        
        # Get waypoints for this turn
        key = (self.origin, self.destination)
        if key in TURN_WAYPOINTS:
            waypoints = [np.array(p) for p in TURN_WAYPOINTS[key]]
        else:
            # Fallback: straight line through center
            waypoints = [(start + end) / 2]
        
        # Build full path: start -> waypoints -> end
        all_points = [start] + waypoints + [end]
        
        # Create path through all points (corners = no overshoot)
        path = VMobject()
        path.set_points_as_corners(all_points)
        
        return path


def spawn_car(scene: Scene, car: Car, run_time: float = 0.3) -> Animation:
    """Spawn a car into the scene with a fade-in animation."""
    return FadeIn(car, run_time=run_time)


def move_car_to_wait(car: Car, run_time: float = 0.8) -> Animation:
    """Move a car from spawn position to the wait position."""
    car.state = "approaching"
    wait_pos = car.get_wait_position()
    return car.animate(run_time=run_time).move_to(wait_pos)


def move_car_through_intersection(car: Car, run_time: float = 1.2) -> Animation:
    """
    Move a car through the intersection using a curved path.
    """
    car.state = "crossing"
    path = car.get_turn_path()
    return MoveAlongPath(car, path, run_time=run_time)


def despawn_car(car: Car, run_time: float = 0.2) -> Animation:
    """Remove a car from the scene with fade-out."""
    car.state = "exited"
    return FadeOut(car, run_time=run_time)
