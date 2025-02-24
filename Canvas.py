from manim import *
from manim.opengl import *
import numpy as np
import math

class Canvas(Scene):
    def construct(self):
        
        # ENTER INTERACTIVE MODE
        self.interactive_embed()