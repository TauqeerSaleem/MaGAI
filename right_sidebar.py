from PyQt6.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QWidget, QGridLayout, QPushButton, QSizePolicy

class RightSidebar(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.default_objects_label = QLabel("Default Objects")
        self.addWidget(self.default_objects_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        default_objects = [
            "1D Axis", "2D Axis", "3D Axis", "Circle", "Square", "Rectangle",
            "Polygon", "Arc", "Arrow", "Tex", "Sphere", "Cube", "Cone", "Torus", "Cylinder"
        ]

        for index, obj_name in enumerate(default_objects):
            button = QPushButton(obj_name)
            button.setFixedSize(60, 60)
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self.scroll_layout.addWidget(button, index // 1, index % 1)

        self.scroll_area.setWidget(self.scroll_widget)
        self.addWidget(self.scroll_area)
