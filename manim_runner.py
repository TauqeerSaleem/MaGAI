class ManimRunner:
    def __init__(self, terminal):
        self.terminal = terminal

    def start_canvas(self):
        self.terminal.process.start("bash", ["-i"])
        self.terminal.process.write("pyenv shell miniforge3-24.11.2-1/envs/manim_env\n".encode())
        self.terminal.process.write("manim -ql -p --renderer=opengl Canvas.py Canvas\n".encode())

