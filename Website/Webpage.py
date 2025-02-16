import eventlet
eventlet.monkey_patch()  # ✅ Ensure this is at the top before importing anything else

import os
import pty
import subprocess
import select
import time
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Command to start Manim and IPython as if run manually
MANIM_CMD = ["manim", "-ql", "-p", "--renderer=opengl", "Canvas.py", "Canvas"]
FFMPEG_CMD = "ffmpeg -f x11grab -r 30 -s 800x600 -i 0x3e00007 -codec:v libx264 -preset ultrafast -f mpegts udp://localhost:1234"

# ✅ Create a pseudo-terminal for Manim + IPython
shell_process, slave_fd = pty.openpty()
manim_process = subprocess.Popen(
    MANIM_CMD,
    stdin=slave_fd,
    stdout=slave_fd,
    stderr=slave_fd,
    bufsize=1,
    universal_newlines=True
)

def start_stream():
    """Start FFmpeg to capture the Pyglet window and stream it."""
    subprocess.Popen(FFMPEG_CMD, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route("/")
def index():
    return render_template("index.html")

@app.before_request
def run_manim():
    """Run Manim and start FFmpeg streaming."""
    if not hasattr(app, "initialized"):
        start_stream()
        app.initialized = True  # Prevent multiple starts

@socketio.on("input")
def handle_input(data):
    """Receive input from web terminal and send it to Manim's IPython."""
    os.write(shell_process, data["input"].encode() + b"\n")  # ✅ Send input to IPython

def read_shell_output():
    """Continuously read IPython output from Manim and send it to the webpage."""
    while True:
        ready, _, _ = select.select([shell_process], [], [], 0.1)
        if ready:
            output = os.read(shell_process, 1024).decode()
            socketio.emit("output", {"output": output})

if __name__ == "__main__":
    eventlet.spawn(read_shell_output)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)