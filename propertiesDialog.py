from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog, QFrame, QHBoxLayout, QRadioButton, QComboBox, QPushButton, \
    QButtonGroup


class PropertiesDialog(QDialog):
    '''
    Custom QDialog class allowing user to specify the properties of the graph.

    Attributes:
        - main_window (QMainWindow): The main window of the app.
        - edge_weight_radio (QRadioButton): Indicates whether the graph is weighted.
        - edge_directed_radio (QRadioButton): Indicates whether the graph is directed.
        - color_combo (QComboBox): Contains options for the default node color.
    '''
    def __init__(self, main_window, parent=None):
        '''
        Initialize a new instance of PropertiesDialog

        Parameters:
            - main_window (QMainWindow): The main window of the app.
        '''
        super().__init__(parent)

        self.main_window = main_window
        self.color_combo = None
        self.edge_weight_radio = None
        self.edge_directed_radio = None
        self.setWindowTitle("Properties")
        self.initUI()

    def initUI(self):
        '''
        Initialize dialog window's UI
        '''
        layout = QVBoxLayout()

        # Title
        title = QLabel('Properties & Behaviour')
        title.setStyleSheet('font-size: 13px;')
        layout.addWidget(title)

        # Empty line
        layout.addSpacing(20)

        # Graph properties section
        graph_label = QLabel("Graph Properties")
        layout.addWidget(graph_label)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Edge Weight section
        edge_group = QHBoxLayout()
        edge_label = QLabel("Edge Weight:")
        edge_label.setFixedWidth(100)
        edge_unweight_radio = QRadioButton("Unweighted")
        self.edge_weight_radio = QRadioButton("Weighted")

        if not self.main_window.weighted and self.main_window.graphic_view.edges:
            self.edge_weight_radio.setEnabled(False)
            edge_unweight_radio.setChecked(True)
        elif self.main_window.weighted and self.main_window.graphic_view.edges:
            edge_unweight_radio.setEnabled(False)
            self.edge_weight_radio.setChecked(True)
        elif not self.main_window.weighted:
            edge_unweight_radio.setChecked(True)
        else:
            self.edge_weight_radio.setChecked(True)

        edge_group.addWidget(edge_label)
        edge_group.addWidget(edge_unweight_radio)
        edge_group.addWidget(self.edge_weight_radio)

        layout.addLayout(edge_group)

        # Edge Directionality section
        directionality_group = QHBoxLayout()
        directionality_label = QLabel("Edge Directionality:")
        directionality_label.setFixedWidth(100)
        edge_undirected_radio = QRadioButton("Undirected")
        self.edge_directed_radio = QRadioButton("Directed")

        if not self.main_window.directed and self.main_window.graphic_view.edges:
            self.edge_directed_radio.setEnabled(False)
            edge_undirected_radio.setChecked(True)
        elif self.main_window.directed and self.main_window.graphic_view.edges:
            edge_undirected_radio.setEnabled(False)
            self.edge_directed_radio.setChecked(True)
        elif not self.main_window.directed:
            edge_undirected_radio.setChecked(True)
        else:
            self.edge_directed_radio.setChecked(True)

        directionality_group.addWidget(directionality_label)
        directionality_group.addWidget(edge_undirected_radio)
        directionality_group.addWidget(self.edge_directed_radio)

        layout.addLayout(directionality_group)

        weight_buttons = QButtonGroup(self)
        directionality_buttons = QButtonGroup(self)

        weight_buttons.addButton(edge_unweight_radio)
        weight_buttons.addButton(self.edge_weight_radio)
        directionality_buttons.addButton(edge_undirected_radio)
        directionality_buttons.addButton(self.edge_directed_radio)

        # Empty line
        layout.addSpacing(20)

        # UI Options section
        ui_label = QLabel("UI Options")
        layout.addWidget(ui_label)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Node Color section
        color_group = QHBoxLayout()
        color_label = QLabel("Node Color:")
        color_label.setFixedWidth(100)
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Green", "Pink", "Blue", "Purple", "Red"])
        color_group.addWidget(color_label)
        color_group.addWidget(self.color_combo)
        layout.addLayout(color_group)

        # Empty line
        layout.addSpacing(20)

        # Horizontal separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # OK and Cancel buttons
        button_group = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.acceptProperties)
        cancel_button.clicked.connect(self.reject)

        button_group.addStretch(1)
        button_group.addWidget(ok_button)
        button_group.addWidget(cancel_button)
        layout.addLayout(button_group)

        self.setLayout(layout)

    def acceptProperties(self):
        self.main_window.weighted = self.edge_weight_radio.isChecked()
        self.main_window.directed = self.edge_directed_radio.isChecked()
        self.main_window.node_color = self.color_combo.currentText().lower()
        self.accept()
