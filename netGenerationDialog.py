from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox


class NetworkGenerationDialog(QDialog):
    '''
    Custom QDialog class allowing the generation of a graph with properties specified by user input.

    Attributes:
        - edit_nodes (QLineEdit): Input space for the node number
        - edit_density (QLineEdit): Input space for the density
    '''
    def __init__(self):
        '''
        Initialize a new instance of NetworkGenerationDialog
        '''
        super(NetworkGenerationDialog, self).__init__()

        self.edit_nodes = QLineEdit(self)
        self.edit_density = QLineEdit(self)
        self.setWindowTitle('Network Properties')
        self.setWindowIcon(QIcon('Icons\\logo.png'))
        self.initUI()

    def initUI(self):
        '''
        Initialize dialog window's UI
        '''
        layout = QVBoxLayout(self)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(QLabel('Generate Random Erdos-Renyi Graph'))
        layout.addSpacing(10)
        layout.addWidget(QLabel('Number of Nodes:'))
        layout.addWidget(self.edit_nodes)
        layout.addWidget(QLabel('Network Density (0 to 1):'))
        layout.addWidget(self.edit_density)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_and_accept(self):
        if self.validate_input():
            self.accept()

    def validate_input(self):
        '''
        Validates user input

        Returns:
            - True: If input is valid
            - False: Otherwise
        '''
        nodes_text = self.edit_nodes.text()
        density_text = self.edit_density.text()

        if not nodes_text or not density_text:
            return True

        try:
            nodes = int(nodes_text)
            density = float(density_text)
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid numeric values.')
            return False

        if nodes <= 0 or density < 0 or density > 1:
            QMessageBox.warning(self, 'Invalid Input',
                                'Please enter positive values for the number of nodes and a network density between 0 and 1.')
            return False

        return True

    def get_user_input(self):
        '''
        Gets user input for the number of notes and density of the graph to be generated

        Returns:
             - dictionary: Dictionary with keys nodes and density as specified by user input
             - None: If dialog was not accepted
        '''
        if self.exec() == QDialog.DialogCode.Accepted:
            return {
                'nodes': int(self.edit_nodes.text()) if self.edit_nodes.text() else 0,
                'density': float(self.edit_density.text()) if self.edit_density.text() else 0
            }
        return None
