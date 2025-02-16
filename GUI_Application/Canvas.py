import os
import pyglet
from manim import *
from manim.opengl import *

class Canvas(Scene):
    def construct(self):
        self.add(ThreeDAxes())
        self.interactive_embed()  # ✅ Interactive Mode

if __name__ == "__main__":
    os.environ["DISPLAY"] = ":99"  # ✅ Use a virtual display if needed (optional)
    
    # ✅ Create an offscreen Pyglet context
    config = pyglet.gl.Config(double_buffer=True)
    pyglet_window = pyglet.window.Window(visible=False, config=config)  # Hide external window

    scene = Canvas()
    scene.render()

    pyglet.app.run()