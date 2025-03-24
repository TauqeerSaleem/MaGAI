from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from left_sidebar import LeftSidebar
from editor import Editor
from right_sidebar import RightSidebar
from terminal import Terminal
from manim_runner import ManimRunner

class ManimUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MaGAI - Manim Gui AI")
        self.setGeometry(200, 200, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()

        # ✅ Initialize terminal
        self.terminal = Terminal()

        # ✅ Add modular components
        self.left_sidebar = LeftSidebar(self.terminal)
        self.editor = Editor(self.terminal)  # Pass terminal to Editor
        self.right_sidebar = RightSidebar(self.terminal, self.left_sidebar)

        # Start 
        self.manim_runner = ManimRunner(self.terminal)

        # ✅ Layout Management
        self.layout.addLayout(self.left_sidebar, 1)
        self.layout.addLayout(self.editor, 5)
        self.layout.addLayout(self.right_sidebar, 1)
        self.central_widget.setLayout(self.layout)

        # ✅ Start Manim
        self.manim_runner.start_canvas()
