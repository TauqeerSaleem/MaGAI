import sys
import subprocess
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit


class ManimCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MAAG - Manim Ai And Gui")
        self.setGeometry(200, 200, 800, 600)

        # ✅ Layout
        self.layout = QVBoxLayout()

        # ✅ Prompt Input
        self.prompt_label = QLabel("Enter your prompt:")
        self.layout.addWidget(self.prompt_label)

        self.prompt_input = QTextEdit()
        self.prompt_input.setFixedHeight(50)
        self.layout.addWidget(self.prompt_input)

        # ✅ Generate Button
        self.generate_button = QPushButton("Generate Code")
        self.generate_button.clicked.connect(self.generate_manim_code)
        self.layout.addWidget(self.generate_button)

        # ✅ Output Box
        self.output_label = QLabel("Generated Manim Code:")
        self.layout.addWidget(self.output_label)

        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)  # Make output read-only
        self.layout.addWidget(self.code_output)

        # ✅ Embedded Terminal
        self.terminal_label = QLabel("Manim Terminal:")
        self.layout.addWidget(self.terminal_label)

        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)  # Allow only output
        self.layout.addWidget(self.terminal_output)

        # ✅ Terminal Input Field
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Enter a command and press Enter...")
        self.terminal_input.returnPressed.connect(self.send_terminal_command)
        self.layout.addWidget(self.terminal_input)

        # ✅ Set Layout
        self.setLayout(self.layout)

        # ✅ Start Terminal Process
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.update_terminal_output)
        self.process.readyReadStandardError.connect(self.update_terminal_output)
        self.process.start("bash", ["-i"])  # ✅ Start interactive shell

        # ✅ Run Manim Automatically on Startup
        self.run_manim()

    def generate_manim_code(self):
        """✅ Generate Manim code using fine-tuned LLaMA model and display it in the output box."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.code_output.setPlainText("Please enter a prompt!")
            return
        else:
            prev = 'You are an AI called MAAG that gives code for manim-comminity animation.\n'
            prev += 'You will only respond in code with no explanation.\n'
            prev += 'You will not import libraries\n'
            prev += 'The scene has already been defined and started in interactive mode, so you will not define the scene again\n'
            #prev += 'The code is already running in an interactive mode and the following is code:'
            #prev += '\nfrom manim import *'
            #prev += '\nfrom manim.opengl import *'
            #prev += '\nclass Canvas(Scene):'
            #prev += '\n\tdef construct(self):'
            #prev += '\n\t\tself.interactive_embed()\n'
            #prev += ' Note that the libraries have already been imported, so no need to import them again'
            #prev += ' Note that the scene has already been defined as class Canvas(Scene), so no need to create a scene'
            #prev += ' Note that the line self.interactive_embed() has started the interactive session has already started'
            #prev += ' Your job is to add code after this, so do not repeat what is already written.  Use only the Manim Community library\n'
            prev += ' When asked add 3d axes use the code: add(ThreeDAxes())'
            prompt = prev + prompt

        response = subprocess.run(
            ["ollama", "run", "llama3.2:1b", "Using manim community library: " + prompt], 
            capture_output=True, text=True
        )
        manim_code = response.stdout.strip()
        if not manim_code:
            manim_code = "self.wait(1)"  # Default fallback code

        # ✅ Display generated code in output box
        self.code_output.setPlainText(manim_code)

        # ✅ Clear input box
        self.prompt_input.clear()

        # ✅ Send generated code to the terminal input box
        self.terminal_input.setText(manim_code)
        self.send_terminal_command()  # ✅ Automatically run the code

    
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

    def run_manim(self):
        """✅ Automatically runs 'manim -ql -p --renderer=opengl Canvas.py Canvas' inside the terminal."""
        self.process.write("pyenv shell miniforge3-24.11.2-1/envs/manim_env\n".encode())
        self.process.write("manim -ql -p --renderer=opengl Canvas.py Canvas\n".encode())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManimCodeGenerator()
    window.show()
    sys.exit(app.exec())
