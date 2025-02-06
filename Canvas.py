from manim import *
from manim.opengl import *
import math

class Canvas(Scene):
    def construct(self):
        self.interactive_embed()  # ✅ Ensures it works in IPython

if __name__ == "__main__":
    scene = Canvas()
    scene.render()


# manim -ql -p --renderer=opengl Canvas.py Canvas
# add(ThreeDAxes)