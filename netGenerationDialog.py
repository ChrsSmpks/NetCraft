from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox


class NetworkGenerationDialog(QDialog):
    '''
    Custom QDialog class allowing the generation of a graph with properties specified by user input.

    Attributes:
        - layout (QVBoxLayout): The layout of the widget
        - label_nodes (QLabel): Text prompting input of node number of the graph
        - edit_nodes (QLineEdit): Input space for the node number
        - label_density (QLabel): Text prompting input of density of the graph
        - edit_density (QLineEdit): Input space for the density
        - button_box (QDialogButtonBox): confirmation button
    '''
    def __init__(self):
        '''
        Initialize a new instance of NodeObject
        '''
        super(NetworkGenerationDialog, self).__init__()

        self.setWindowTitle('Network Properties')
        self.layout = QVBoxLayout(self)

        self.label_nodes = QLabel('Number of Nodes:')
        self.edit_nodes = QLineEdit(self)

        self.label_density = QLabel('Network Density (0 to 1):')
        self.edit_density = QLineEdit(self)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)

        self.layout.addWidget(self.label_nodes)
        self.layout.addWidget(self.edit_nodes)
        self.layout.addWidget(self.label_density)
        self.layout.addWidget(self.edit_density)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

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
                                'Please enter positive values for number of nodes and a network density between 0 and 1.')
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
