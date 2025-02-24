from PyQt6.QtWidgets import QTextEdit, QLabel, QLineEdit
from PyQt6.QtCore import QProcess

class Terminal(QTextEdit):
    def __init__(self):
        super().__init__()
        # Terminal Output and Input
        self.terminal_label = QLabel("Terminal")
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        
        # ✅ Terminal Input Field
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Terminal Input")
        self.terminal_input.returnPressed.connect(self.send_terminal_command)

        # Start Terminal Process
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.update_terminal_output)
        self.process.readyReadStandardError.connect(self.update_terminal_output)
        self.process.start("bash", ["-i"])  # ✅ Start interactive shell
        
    def update_terminal_output(self):
        """✅ Capture live terminal output and display it in the GUI."""
        output = self.process.readAllStandardOutput().data().decode()
        error = self.process.readAllStandardError().data().decode()
        if output:
            self.terminal_output.append(output.strip())
        if error:
            self.terminal_output.append(f"<span style='color:red;'>{error.strip()}</span>")

    def send_terminal_command(self):
        """✅ Send user input to the embedded terminal."""
        command = self.terminal_input.text().strip()
        if command:
            self.terminal_output.append(f"$ {command}")  # Show command in terminal output
            self.process.write((command + "\n").encode())  # Send command to subprocess
            self.terminal_input.clear()  # Clear input field after sending

