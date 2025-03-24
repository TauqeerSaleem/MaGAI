from manim import *
from manim.opengl import *
# import numpy as np ALREADY IN THE INTERACTIVE MODE

class Canvas(Scene):
    def construct(self):
        
        # ENTER INTERACTIVE MODE
        self.interactive_embed()
