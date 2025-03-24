from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QInputDialog,
    QDialog, QTreeWidget, QTreeWidgetItem)

class LeftSidebar(QVBoxLayout):
    def __init__(self, terminal):
        super().__init__()

        # Inter-connected files
        self.terminal = terminal
        self.terminal_label = terminal.terminal_label
        self.terminal_output = terminal.terminal_output 

        # Animations Section
        self.anim_label = QLabel("Animations")
        self.anim_list = QListWidget()
        self.anim_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        # Animation Buttons
        self.anim_button_layout = QHBoxLayout()
        self.new_anim_button = QPushButton("New Animation")
        self.new_anim_button.clicked.connect(self.add_new_animation)
        self.delete_anim_button = QPushButton("Delete Animation")
        self.delete_anim_button.clicked.connect(self.delete_selected_animation)

        self.anim_button_layout.addWidget(self.new_anim_button)
        self.anim_button_layout.addWidget(self.delete_anim_button)

        self.addWidget(self.anim_label)
        self.addWidget(self.anim_list)
        self.addLayout(self.anim_button_layout)

        # Objects Section
        self.obj_label = QLabel("Objects")
        self.obj_list = QListWidget()
        self.obj_list.itemDoubleClicked.connect(self.open_object_actions_window)

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
            self.func_list.addItem(text.strip())

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

    def add_new_animation(self):
        text, ok = QInputDialog.getText(None, "New Animation", "Name your animation:")
        if ok and text.strip():
            self.anim_list.addItem(text.strip())

    def delete_selected_animation(self):
        selected_item = self.anim_list.currentItem()
        if selected_item:
            self.anim_list.takeItem(self.anim_list.row(selected_item))

    def open_object_actions_window(self, item):
        selected_object_name = item.text()  # <- Save the clicked object name

        dialog = QDialog()
        dialog.setWindowTitle(f"{selected_object_name} — Available Actions")
        layout = QVBoxLayout(dialog)

        tree = QTreeWidget()
        tree.setHeaderLabel("Select Action")

        animation_categories = {
            "animation": ["Add", "Animation", "Wait", "override_animation()", "prepare_animation()"],
            "changing": ["AnimatedBoundary", "TracedPath"],
            "composition": ["AnimationGroup", "LaggedStart", "LaggedStartMap", "Succession"],
            "creation": [
                "AddTextLetterByLetter", "AddTextWordByWord", "Create", "DrawBorderThenFill",
                "RemoveTextLetterByLetter", "ShowIncreasingSubsets", "ShowPartial", "ShowSubmobjectsOneByOne",
                "SpiralIn", "TypeWithCursor", "Uncreate", "UntypeWithCursor", "Unwrite", "Write"
            ],
            "fading": ["FadeIn", "FadeOut"],
            "growing": ["GrowArrow", "GrowFromCenter", "GrowFromEdge", "GrowFromPoint", "SpinInFromNothing"],
            "indication": [
                "ApplyWave", "Blink", "Circumscribe", "Flash", "FocusOn", "Indicate",
                "ShowPassingFlash", "ShowPassingFlashWithThinningStrokeWidth", "Wiggle"
            ],
            "movement": ["ComplexHomotopy", "Homotopy", "MoveAlongPath", "PhaseFlow", "SmoothedVectorizedHomotopy"],
            "numbers": ["ChangeDecimalToValue", "ChangingDecimal"],
            "rotation": ["Rotate", "Rotating"],
            "specialized": ["Broadcast"],
            "speedmodifier": ["ChangeSpeed"],
            "transform": [
                "ApplyComplexFunction", "ApplyFunction", "ApplyMatrix", "ApplyMethod", "ApplyPointwiseFunction",
                "ApplyPointwiseFunctionToCenter", "ClockwiseTransform", "CounterclockwiseTransform", "CyclicReplace",
                "FadeToColor", "FadeTransform", "FadeTransformPieces", "MoveToTarget", "ReplacementTransform", "Restore",
                "ScaleInPlace", "ShrinkToCenter", "Swap", "Transform", "TransformAnimations", "TransformFromCopy"
            ],
            "transform_matching_parts": ["TransformMatchingAbstractBase", "TransformMatchingShapes", "TransformMatchingTex"],
            "updaters": ["Modules"]
        }

        for category, actions in animation_categories.items():
            parent_item = QTreeWidgetItem([category])
            for action in actions:
                child = QTreeWidgetItem(parent_item, [action])
            tree.addTopLevelItem(parent_item)

        tree.expandToDepth(0)  # show only first level
        layout.addWidget(tree)
        dialog.setLayout(layout)
        dialog.resize(400, 500)

        # 🔥 Add this: On double click of an action
        def handle_action_click(action_item):
            parent = action_item.parent()
            if parent is not None:
                category = parent.text(0)
                action_name = action_item.text(0)

                if category == "animation" and action_name == "Add":
                    command = f"add({selected_object_name})"
                    self.terminal.terminal_input.setText(command)
                    self.terminal. terminal_input.returnPressed.emit()
                    object_name = selected_object_name
                    self.anim_list.addItem(object_name)
                dialog.accept()

        tree.itemDoubleClicked.connect(handle_action_click)
        dialog.exec()
