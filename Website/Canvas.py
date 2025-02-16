import os
from manim import *
from manim.opengl import *
import math

class Canvas(Scene):
    def construct(self):
        self.interactive_embed()

# manim -ql -p --renderer=opengl Canvas.py Canvas
# add(ThreeDAxes)