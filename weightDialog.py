from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox


class WeightDialog(QDialog):
    '''
    Custom QDialog class allowing user to specify the edge weight.

    Attributes:
        - edge_weight (QLineEdit): Input space for the edge weight
    '''
    def __init__(self):
        '''
        Initialize a new instance of WeightDialog
        '''
        super(WeightDialog, self).__init__()

        self.edge_weight = QLineEdit(self)
        self.setWindowTitle('Network Properties')
        self.initUI()

    def initUI(self):
        '''
        Initialize dialog window's UI
        '''
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel('Weight (please enter a positive value greater than 0):'))
        layout.addWidget(self.edge_weight)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

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
        edge_weight_text = self.edge_weight.text()

        if not edge_weight_text:
            return True

        try:
            edge_weight = float(edge_weight_text)
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid numeric value.')
            return False

        if edge_weight <= 0:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a positive value.')
            return False

        return True

    def get_user_input(self):
        '''
        Gets user input for the number of notes and density of the graph to be generated

        Returns:
             - float: The weight of the edge as specified by user input
             - None: If dialog was not accepted or there was no input
        '''
        if self.exec() == QDialog.DialogCode.Accepted:
            return float(self.edge_weight.text()) if self.edge_weight.text() else None

        return None
