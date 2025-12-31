from manim import *
from car import Car, CarData, spawn_car, move_car_to_wait, move_car_through_intersection, despawn_car


class TrafficIntersectionScene(Scene):
    def construct(self):
        # 1. Draw Roads
        # Vertical Road (Height 16 to go off-screen)
        road_v = Rectangle(width=2, height=16, color=WHITE, fill_opacity=0).set_z_index(0)
        # Horizontal Road (Width 20 to go off-screen)
        road_h = Rectangle(width=20, height=2, color=WHITE, fill_opacity=0).set_z_index(0)
        
        # Road Markings (Dashed Lines)
        line_v = DashedLine(start=UP*4, end=DOWN*4, color=YELLOW)
        line_h = DashedLine(start=LEFT*7, end=RIGHT*7, color=YELLOW)

        # 2. Traffic Light
        # Represented by a circle in the corner
        traffic_light_body = Rectangle(width=0.5, height=1.5, color=GRAY, fill_opacity=1).move_to(UR * 0.5)
        light_red = Circle(radius=0.2, color=RED, fill_opacity=0.2).move_to(traffic_light_body.get_top() + DOWN*0.3)
        light_green = Circle(radius=0.2, color=GREEN, fill_opacity=0.2).move_to(traffic_light_body.get_bottom() + UP*0.3)
        
        traffic_light_group = VGroup(traffic_light_body, light_red, light_green).shift(RIGHT*1.5 + UP*1.5)

        # 3. Add to Scene
        self.add(road_v, road_h, line_v, line_h)
        self.add(traffic_light_group)
        
        # 4. Simple Animation
        self.play(Create(road_v), Create(road_h))
        self.play(FadeIn(traffic_light_group))
        
        # Toggle Light
        self.wait(1)
        self.play(light_red.animate.set_fill(opacity=1), light_green.animate.set_fill(opacity=0.2))
        self.wait(1)
        self.play(light_red.animate.set_fill(opacity=0.2), light_green.animate.set_fill(opacity=1))
        self.wait(1)


class CarDemoScene(Scene):
    """
    Demo scene showing 4-phase traffic system.
    Phase order: N → S → E → W (one direction at a time, no conflicts)
    """
    
    def construct(self):
        # 1. Draw Roads
        road_v = Rectangle(width=2, height=16, color=WHITE, fill_opacity=0)
        road_h = Rectangle(width=20, height=2, color=WHITE, fill_opacity=0)
        line_v = DashedLine(start=UP*4, end=DOWN*4, color=YELLOW)
        line_h = DashedLine(start=LEFT*7, end=RIGHT*7, color=YELLOW)
        
        self.add(road_v, road_h, line_v, line_h)
        
        # 2. Traffic Lights - One per direction
        def create_light(position, direction_color, initial_green=False):
            body = Rectangle(width=0.4, height=0.9, color=GRAY, fill_opacity=1)
            red = Circle(radius=0.12, color=RED, fill_opacity=0.2 if initial_green else 1)
            red.move_to(body.get_top() + DOWN*0.2)
            green = Circle(radius=0.12, color=GREEN, fill_opacity=1 if initial_green else 0.2)
            green.move_to(body.get_bottom() + UP*0.2)
            # Add direction indicator
            indicator = Dot(radius=0.05, color=direction_color).move_to(body.get_top() + UP*0.15)
            light = VGroup(body, red, green, indicator).move_to(position)
            return light, red, green
        
        # Create all 4 lights (N starts green)
        light_n, red_n, green_n = create_light(UP*2.5 + LEFT*1.5, BLUE, initial_green=True)
        light_s, red_s, green_s = create_light(DOWN*2.5 + RIGHT*1.5, RED, initial_green=False)
        light_e, red_e, green_e = create_light(RIGHT*2.5 + UP*1.5, GREEN, initial_green=False)
        light_w, red_w, green_w = create_light(LEFT*2.5 + DOWN*1.5, ORANGE, initial_green=False)
        
        lights = {"N": (red_n, green_n), "S": (red_s, green_s), "E": (red_e, green_e), "W": (red_w, green_w)}
        
        # Labels
        label_n = Text("N", font_size=16, color=BLUE).next_to(light_n, LEFT, buff=0.1)
        label_s = Text("S", font_size=16, color=RED).next_to(light_s, RIGHT, buff=0.1)
        label_e = Text("E", font_size=16, color=GREEN).next_to(light_e, UP, buff=0.1)
        label_w = Text("W", font_size=16, color=ORANGE).next_to(light_w, DOWN, buff=0.1)
        
        self.add(light_n, light_s, light_e, light_w)
        self.add(label_n, label_s, label_e, label_w)
        
        # Phase indicator
        phase_text = Text("Phase: N", font_size=20, color=BLUE).to_corner(UR)
        self.add(phase_text)
        
        # 3. Create cars - 3 per direction with queue positions
        def create_cars_for_direction(origin, destinations, queue_count):
            """Create 3 cars (straight, left, right) with proper queue positions."""
            intents = ["straight", "left", "right"]
            cars = []
            for i, (dest, intent) in enumerate(zip(destinations, intents)):
                car = Car(
                    CarData(
                        car_id=f"{origin}_{i+1}",
                        origin=origin,
                        destination=dest,
                        intent=intent,
                        queue_position=i  # 0, 1, 2 for queue offset
                    ),
                    queue_count=queue_count
                )
                cars.append(car)
            return cars
        
        # Create cars for each direction
        # From N: straight→S, left→W, right→E
        cars_n = create_cars_for_direction("N", ["S", "W", "E"], 3)
        # From S: straight→N, left→E, right→W
        cars_s = create_cars_for_direction("S", ["N", "E", "W"], 2)
        # From E: straight→W, left→N, right→S
        cars_e = create_cars_for_direction("E", ["W", "N", "S"], 5)
        # From W: straight→E, left→S, right→N
        cars_w = create_cars_for_direction("W", ["E", "S", "N"], 4)
        
        all_cars = cars_n + cars_s + cars_e + cars_w
        
        # 4. Spawn all cars and move to wait positions
        self.play(*[spawn_car(self, car) for car in all_cars])
        self.wait(0.2)
        self.play(*[move_car_to_wait(car) for car in all_cars])
        self.wait(0.3)
        
        # 5. Helper function for phase changes
        def set_phase(direction, phase_text_obj):
            """Set one direction green, all others red."""
            animations = []
            colors = {"N": BLUE, "S": RED, "E": GREEN, "W": ORANGE}
            
            for d, (red_light, green_light) in lights.items():
                if d == direction:
                    animations.append(red_light.animate.set_fill(opacity=0.2))
                    animations.append(green_light.animate.set_fill(opacity=1))
                else:
                    animations.append(red_light.animate.set_fill(opacity=1))
                    animations.append(green_light.animate.set_fill(opacity=0.2))
            
            new_text = Text(f"Phase: {direction}", font_size=20, color=colors[direction]).to_corner(UR)
            animations.append(Transform(phase_text_obj, new_text))
            
            return animations
        
        # 6. Run 4-phase cycle: N → S → E → W
        phase_order = [("N", cars_n), ("S", cars_s), ("E", cars_e), ("W", cars_w)]
        
        for i, (direction, cars) in enumerate(phase_order):
            if i > 0:  # Phase N is already green
                self.play(*set_phase(direction, phase_text))
            self.wait(0.2)
            
            # Cars go through ONE AT A TIME (front of queue first)
            for car in cars:
                self.play(move_car_through_intersection(car, run_time=1.5))
            
            # Despawn all at once (they're already off-screen)
            self.play(*[despawn_car(car) for car in cars])
        
        self.wait(1)


class DataDrivenScene(Scene):
    """
    Animates traffic based on JSON simulation data.
    
    Usage:
        # Default path (docs/simulation_data_schema.json):
        uv run manim -pql visualizer.py DataDrivenScene
        
        # Custom path via environment variable:
        JSON_PATH=path/to/data.json uv run manim -pql visualizer.py DataDrivenScene
    """
    
    def construct(self):
        import json
        import os
        
        # Get JSON path from environment variable or use default
        # json_path = os.environ.get("JSON_PATH", "../docs/simulation_data_schema.json")
        # json_path = os.environ.get("JSON_PATH", "../docs/simulation_data_fixed.json")
        json_path = os.environ.get("JSON_PATH", "../docs/simulation_data_fuzzy.json")
        
        # Load simulation data
        with open(json_path, "r") as f:
            data = json.load(f)
        
        # 1. Setup roads and lights
        road_v = Rectangle(width=2, height=16, color=WHITE, fill_opacity=0)
        road_h = Rectangle(width=20, height=2, color=WHITE, fill_opacity=0)
        line_v = DashedLine(start=UP*4, end=DOWN*4, color=YELLOW)
        line_h = DashedLine(start=LEFT*7, end=RIGHT*7, color=YELLOW)
        self.add(road_v, road_h, line_v, line_h)
        
        # Traffic lights - one per direction
        def create_light(position, direction_color):
            body = Rectangle(width=0.4, height=0.9, color=GRAY, fill_opacity=1)
            red = Circle(radius=0.12, color=RED, fill_opacity=1)
            red.move_to(body.get_top() + DOWN*0.2)
            green = Circle(radius=0.12, color=GREEN, fill_opacity=0.2)
            green.move_to(body.get_bottom() + UP*0.2)
            indicator = Dot(radius=0.05, color=direction_color).move_to(body.get_top() + UP*0.15)
            light = VGroup(body, red, green, indicator).move_to(position)
            return light, red, green
        
        light_n, red_n, green_n = create_light(UP*2.5 + LEFT*1.5, BLUE)
        light_s, red_s, green_s = create_light(DOWN*2.5 + RIGHT*1.5, RED)
        light_e, red_e, green_e = create_light(RIGHT*2.5 + UP*1.5, GREEN)
        light_w, red_w, green_w = create_light(LEFT*2.5 + DOWN*1.5, ORANGE)
        
        lights = {
            "N": (red_n, green_n), 
            "S": (red_s, green_s), 
            "E": (red_e, green_e), 
            "W": (red_w, green_w)
        }
        
        self.add(light_n, light_s, light_e, light_w)
        
        # HUD elements
        phase_text = Text("Phase: -", font_size=20, color=WHITE).to_corner(UR)
        timer_text = Text("Timer: -", font_size=16, color=WHITE).next_to(phase_text, DOWN)
        queue_text = Text("Queues: N:0 S:0 E:0 W:0", font_size=14, color=WHITE).to_corner(UL)
        
        # Time display (large, bottom center)
        time_display = Text("t=0", font_size=24, color=YELLOW).to_edge(DOWN)
        
        # Event log (bottom left, shows recent events)
        event_log = Text("Events: -", font_size=12, color=GRAY).to_corner(DL)
        
        self.add(phase_text, timer_text, queue_text, time_display, event_log)
        
        # 2. Track active cars
        active_cars: dict[str, Car] = {}
        current_phase = None
        colors = {"N": BLUE, "S": RED, "E": GREEN, "W": ORANGE}
        
        # 3. Process each frame
        for frame in data["frames"]:
            t = frame["t"]
            state = frame["traffic_state"]
            new_phase = state["current_phase"]
            
            animations = []
            
            # Phase change
            if new_phase != current_phase:
                current_phase = new_phase
                
                # Update lights
                for d, (red_light, green_light) in lights.items():
                    if d == current_phase:
                        animations.append(red_light.animate.set_fill(opacity=0.2))
                        animations.append(green_light.animate.set_fill(opacity=1))
                    else:
                        animations.append(red_light.animate.set_fill(opacity=1))
                        animations.append(green_light.animate.set_fill(opacity=0.2))
                
                # Update phase text
                new_phase_text = Text(f"Phase: {current_phase}", font_size=20, color=colors[current_phase]).to_corner(UR)
                animations.append(Transform(phase_text, new_phase_text))
            
            # Update timer
            new_timer = Text(f"Timer: {state['green_timer']}", font_size=16, color=WHITE).next_to(phase_text, DOWN)
            animations.append(Transform(timer_text, new_timer))
            
            # Update time display
            new_time = Text(f"t={t}", font_size=24, color=YELLOW).to_edge(DOWN)
            animations.append(Transform(time_display, new_time))
            
            # Update queue display
            q = state["queues"]
            new_queue = Text(f"N:{q['N']} S:{q['S']} E:{q['E']} W:{q['W']}", font_size=14, color=WHITE).to_corner(UL)
            animations.append(Transform(queue_text, new_queue))
            
            # Build event log string
            events_str = []
            for event in frame.get("car_events", []):
                if event["event"] == "spawn":
                    events_str.append(f"+{event['car_id']}")
            for dep in frame.get("departures", []):
                events_str.append(f"-{dep['car_id']}")
            log_text = " ".join(events_str) if events_str else "-"
            new_log = Text(f"Events: {log_text}", font_size=12, color=GRAY).to_corner(DL)
            animations.append(Transform(event_log, new_log))
            
            # Spawn new cars
            for event in frame.get("car_events", []):
                if event["event"] == "spawn":
                    car = Car(
                        CarData(
                            car_id=event["car_id"],
                            origin=event["origin"],
                            destination=event["destination"],
                            intent=event["intent"],
                            queue_position=event.get("queue_position", 0)
                        ),
                        queue_count=q[event["origin"]]
                    )
                    active_cars[event["car_id"]] = car
                    animations.append(spawn_car(self, car))
            
            # Play frame updates
            if animations:
                self.play(*animations, run_time=0.3)
            
            # Move spawned cars to wait position
            new_car_ids = [e["car_id"] for e in frame.get("car_events", []) if e["event"] == "spawn"]
            if new_car_ids:
                move_anims = [move_car_to_wait(active_cars[cid]) for cid in new_car_ids if cid in active_cars]
                if move_anims:
                    self.play(*move_anims, run_time=0.5)
            
            # Handle departures
            for departure in frame.get("departures", []):
                car_id = departure["car_id"]
                if car_id in active_cars:
                    car = active_cars[car_id]
                    self.play(move_car_through_intersection(car, run_time=1.0))
                    self.play(despawn_car(car, run_time=0.2))
                    del active_cars[car_id]
            
            self.wait(0.1)
        
        self.wait(1)
