import sys
from PyQt6.QtWidgets import QApplication
from ui_main import ManimUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManimUI()
    window.show()
    sys.exit(app.exec())