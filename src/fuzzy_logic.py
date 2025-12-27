import warnings
# Suppress specific SyntaxWarnings from pydub
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pydub")

from manim import *

class TestLatex(Scene):
    def construct(self):
        # 1. Standard Text (Uses standard font)
        title = Text("Windows Manim Setup").to_edge(UP)
        
        # 2. Math Formula (Uses MikTeX)
        # If MikTeX is missing/broken, this crashes.
        equation = MathTex(
            r"\int_{a}^{b} f(x) \,dx = F(b) - F(a)"
        ).scale(1.5)
        
        # Animate
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(equation))
        self.wait(1)