import warnings
# Suppress specific SyntaxWarnings from pydub (used by Manim)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pydub")
from manim import *

class TestScene(Scene):
    def construct(self):
        # Create a text object
        text = Text("WSL + Manim = ❤️").scale(1.5)
        # Create a circle
        circle = Circle()
        
        # Animate
        self.play(Write(text))
        self.wait(1)
        self.play(ReplacementTransform(text, circle))
        self.play(circle.animate.set_fill(PINK, opacity=0.5))
        self.wait(1)

# To run this, use the terminal command below, not just "python file.py"
# uv run manim -qm src/test_manim.py TestScene