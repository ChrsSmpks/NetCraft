from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox


class NetworkGenerationDialog(QDialog):
    def __init__(self):
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
        nodes_text = self.edit_nodes.text()
        density_text = self.edit_density.text()

        if not nodes_text or not density_text:
            """QMessageBox.warning(self, 'Invalid Input',
                                'Please enter values for both number of nodes and network density.')
            return False"""
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
        if self.exec() == QDialog.DialogCode.Accepted:
            return {
                'nodes': int(self.edit_nodes.text()) if self.edit_nodes.text() else 0,
                'density': float(self.edit_density.text()) if self.edit_density.text() else 0
            }
        return None
