from manim import *

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
