from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QScrollArea, QWidget, QGridLayout, 
    QPushButton, QSizePolicy, QDialog, QLineEdit, QFormLayout, 
    QDialogButtonBox, QVBoxLayout, QTextEdit
)
import sys
from PyQt6.QtWidgets import QApplication

class BarPlotDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bar Plot Settings")

        layout = QVBoxLayout()

        # Form layout for input fields
        form_layout = QFormLayout()

        # Input fields with default values
        self.inputs = {
            "name": QLineEdit("Bar_Plot"),
            "values": QLineEdit("[10, 20, 30, 40]"),
            "bar_names": QLineEdit("None"),
            "y_range": QLineEdit("None"),
            "x_length": QLineEdit("None"),
            "y_length": QLineEdit("None"),
            "bar_colors": QLineEdit("['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600']"),
            "bar_width": QLineEdit("0.6"),
            "bar_fill_opacity": QLineEdit("0.7"),
            "bar_stroke_width": QLineEdit("3")
        }

        for label, widget in self.inputs.items():
            form_layout.addRow(label, widget)

        layout.addLayout(form_layout)

        # OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_values(self):
        """ Returns the user input as a dictionary """
        return {key: field.text() for key, field in self.inputs.items()}

class HistDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bar Plot Settings")

        layout = QVBoxLayout()

        # Form layout for input fields
        form_layout = QFormLayout()

        # Input fields with default values
        self.inputs = {
            "name": QLineEdit("Histogram"),
            "data": QLineEdit("np.random.normal(loc=0, scale=1, size=100)"),
            "bins": QLineEdit("10")
        }

        for label, widget in self.inputs.items():
            form_layout.addRow(label, widget)

        layout.addLayout(form_layout)

        # OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_values(self):
        """ Returns the user input as a dictionary """
        return {key: field.text() for key, field in self.inputs.items()}

class RightSidebar(QVBoxLayout):
    def __init__(self, terminal, left_sidebar):
        super().__init__()
        
        # Inter-connected files
        self.terminal = terminal
        self.left_sidebar = left_sidebar

        # ✅ Terminal Section (Output)
        self.terminal_label = terminal.terminal_label
        self.terminal_output = terminal.terminal_output 

        # ✅ Terminal Input Field
        self.terminal_input = terminal.terminal_input

        # All the functions available
        self.list_of_functions = [self.show_bar_plot_dialog,
                                  self.show_histogram_dialog]

        # Default Objects Widget
        self.default_objects_label = QLabel("Default Objects")
        self.addWidget(self.default_objects_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        default_objects = ["Bar Plot", "Histogram"]

        for index, obj_name in enumerate(default_objects):
            button = QPushButton(obj_name)
            button.setFixedSize(100, 50)
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.clicked.connect(self.list_of_functions[index])
            self.scroll_layout.addWidget(button, index, 0)

        self.scroll_area.setWidget(self.scroll_widget)
        self.addWidget(self.scroll_area)

    def show_bar_plot_dialog(self):
        """ Opens the popup for Bar Plot configuration """
        dialog = BarPlotDialog()
        if dialog.exec():
            inputs = dialog.get_values()

            # Convert 'None' strings to actual None and parse list correctly
            for key in ["bar_names", "y_range", "x_length", "y_length"]:
                if inputs[key].lower() == "none":
                    inputs[key] = "None"

            # Generate command string
            command = (
                f"{inputs['name']} = BarChart({inputs['values']}, {inputs['bar_names']}, {inputs['y_range']}, "
                f"{inputs['x_length']}, {inputs['y_length']}, {inputs['bar_colors']}, "
                f"{inputs['bar_width']}, {inputs['bar_fill_opacity']}, {inputs['bar_stroke_width']})"
            )

            # Add object to the "Object" list
            object_name = inputs["name"]
            self.left_sidebar.obj_list.addItem(object_name)

            # Send to terminal
            self.terminal_input.setText(command)
            self.terminal_input.returnPressed.emit()

    def show_histogram_dialog(self):
        """ Opens the popup for Bar Plot configuration """
        dialog = HistDialog()
        if dialog.exec():
            inputs = dialog.get_values()
            command_1 = f"binned = pd.cut({inputs['data']}, bins = {inputs['bins']}, right = False)"
            command_2 = f"counts = list(binned.value_counts().sort_index())"
            
            self.terminal_input.setText(command_1)
            self.terminal_input.returnPressed.emit()
            self.terminal_input.setText(command_2)
            self.terminal_input.returnPressed.emit()
            #binned = pd.cut(inputs['data'], bins = inputs['bins'], right=False)  # right=False means intervals like [1,2)
            #counts = pd.value_counts(binned).sort_index()
            
            # Convert 'None' strings to actual None and parse list correctly
            #for key in ["bar_names", "y_range", "x_length", "y_length"]:
            #    if inputs[key].lower() == "none":
            #        inputs[key] = "None"

            # Generate command string
            command = f"{inputs['name']} = BarChart(counts, bar_width=1)"

            # Add object to the "Object" list
            object_name = inputs["name"]
            self.left_sidebar.obj_list.addItem(object_name)

            # Send to terminal
            self.terminal_input.setText(command)
            self.terminal_input.returnPressed.emit()
