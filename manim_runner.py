class ManimRunner:
    def __init__(self, terminal):
        self.terminal = terminal

    def start_canvas(self):
        self.terminal.process.start("bash", ["-i"])

        # The following line sets the environment
        # Make sure in the final version user can set it up themselves
        # Or installation has option to set a default environment automatically
        self.terminal.process.write("pyenv shell miniforge3-24.11.2-1/envs/manim_env\n".encode())

        # Starts the canvas
        self.terminal.process.write("manim -ql -p --renderer=opengl Canvas.py Canvas\n".encode())

        # Import libararies
        self.terminal.process.write(("import pandas as pd\n").encode())

