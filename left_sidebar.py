from PyQt6.QtWidgets import QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QInputDialog

class LeftSidebar(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Animations Section
        self.anim_label = QLabel("Animations")
        self.anim_list = QListWidget()
        self.anim_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        for i in range(1, 4):
            self.anim_list.addItem(f"Anim {i}")

        self.addWidget(self.anim_label)
        self.addWidget(self.anim_list)

        # Objects Section
        self.obj_label = QLabel("Objects")
        self.obj_list = QListWidget()
        self.obj_list.addItems(["Camera", "Light"])

        self.obj_button_layout = QHBoxLayout()
        self.new_obj_button = QPushButton("New Object")
        self.new_obj_button.clicked.connect(self.add_new_object)
        self.delete_obj_button = QPushButton("Delete Object")
        self.delete_obj_button.clicked.connect(self.delete_selected_object)

        self.obj_button_layout.addWidget(self.new_obj_button)
        self.obj_button_layout.addWidget(self.delete_obj_button)

        self.addWidget(self.obj_label)
        self.addWidget(self.obj_list)
        self.addLayout(self.obj_button_layout)
    

        # Utilties/ Functions Section
        self.func_label = QLabel("Functions/ Utilites")
        self.func_list = QListWidget()
        self.func_list.addItems(["Quadratic-1", "Quadratic-2", "Cubic-1"])

        self.func_button_layout = QHBoxLayout()
        self.new_func_button = QPushButton("New Function")
        self.new_func_button.clicked.connect(self.add_new_function)
        self.delete_func_button = QPushButton("Delete Function")
        self.delete_func_button.clicked.connect(self.delete_selected_function)

        self.func_button_layout.addWidget(self.new_func_button)
        self.func_button_layout.addWidget(self.delete_func_button)

        self.addWidget(self.func_label)
        self.addWidget(self.func_list)
        self.addLayout(self.func_button_layout)

    def add_new_function(self):
        text, ok = QInputDialog.getText(None, "New Function", "Write it:")
        if ok and text.strip():
            self.obj_list.addItem(text.strip())

    def delete_selected_function(self):
        selected_item = self.obj_list.currentItem()
        if selected_item:
            self.obj_list.takeItem(self.obj_list.row(selected_item))
    
    def add_new_object(self):
        text, ok = QInputDialog.getText(None, "New Object", "Name of Object:")
        if ok and text.strip():
            self.obj_list.addItem(text.strip())

    def delete_selected_object(self):
        selected_item = self.obj_list.currentItem()
        if selected_item:
            self.obj_list.takeItem(self.obj_list.row(selected_item))

