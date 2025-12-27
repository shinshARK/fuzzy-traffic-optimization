import warnings
# Suppress specific SyntaxWarnings from pydub (used by Manim)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pydub")

import numpy as np
import skfuzzy as fuzz
from manim import *

def test_environment():
    print("✅ Numpy version:", np.__version__)
    print("✅ Scikit-Fuzzy version:", fuzz.__version__)
    print("✅ Manim is importable!")

if __name__ == "__main__":
    test_environment()