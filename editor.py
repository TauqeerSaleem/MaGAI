from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from tool_call import ToolCall
import asyncio

class Editor(QVBoxLayout):
    def __init__(self, terminal):
        super().__init__()

        self.terminal = terminal  # Store reference to Terminal instance

        # ✅ File Editor
        self.file_editor_label = QLabel("File Editor")
        self.file_editor = QTextEdit()

        # ✅ AI Prompt Section
        self.prompt_label = QLabel("AI Prompt")
        self.prompt_input = QTextEdit()
        self.prompt_input.setFixedHeight(50)
        self.generate_button = QPushButton("Generate Code")
        self.generate_button.clicked.connect(self.generate_manim_code)

        # ✅ AI Output
        self.output_label = QLabel("Generated Manim Code:")
        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)

        # ✅ Terminal Section (Output)
        self.terminal_label = terminal.terminal_label
        self.terminal_output = terminal.terminal_output 

        # ✅ Terminal Input Field
        self.terminal_input = terminal.terminal_input

        # ✅ Add widgets to layout
        self.addWidget(self.file_editor_label)
        self.addWidget(self.file_editor)
        self.addWidget(self.prompt_label)
        self.addWidget(self.prompt_input)
        self.addWidget(self.generate_button)
        self.addWidget(self.output_label)
        self.addWidget(self.code_output)
        self.addWidget(self.terminal_label)
        self.addWidget(self.terminal_output)
        self.addWidget(self.terminal_input)

    async def main(self, prompt):
            tool = ToolCall()
            result = await tool.get_code(prompt)
            return result

    def generate_manim_code(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.code_output.setPlainText("Please enter a prompt!")
            return
        
        result = asyncio.run(self.main(prompt))
        self.code_output.setPlainText(result)
        self.prompt_input.clear()
        self.terminal_input.setText(result)
        self.terminal_input.returnPressed.emit()
