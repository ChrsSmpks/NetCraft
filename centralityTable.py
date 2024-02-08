from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem


class CentralityTable(QTableWidget):
    '''
    Custom QTableWidget class to display the centrality for each edge.
    '''

    def __init__(self, data_dict, parent=None):
        '''
        Initialize a new instance of CentralityTable

        Parameters:
            - data_dict (dictionary): Keys of the dictionary are the edges in the form (u, v) and values are the centralities
        '''
        super().__init__(parent)
        self.setup_table(data_dict)

    def setup_table(self, data_dict):
        '''
        Set the properties of the table and calls another function to populate the table

        Parameters:
            - data_dict (dictionary): Keys of the dictionary are the edges in the form (u, v) and values are the centralities
        '''

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Edge', 'Centrality'])
        self.setRowCount(len(data_dict))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.setSortingEnabled(True)

        self.setAlternatingRowColors(True)

        self.populate_table(data_dict)

    def populate_table(self, data_dict):
        '''
        Populates the table with the keys of the dictionary and their corresponding values

        Parameters:
            - data_dict (dictionary): Keys of the dictionary are the edges in the form (u, v) and values are the centralities
        '''

        for row, (edge, centrality) in enumerate(data_dict.items()):
            edge_item = QTableWidgetItem(str(edge))
            centrality_item = QTableWidgetItem(str(centrality))

            edge_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            centrality_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.setItem(row, 0, edge_item)
            self.setItem(row, 1, centrality_item)

    def update_table(self, new_data_dict):
        '''
        Updates the table to display the new edges and their centralities

        Parameters:
            - new_data_dict (dictionary): A new dictionary containing edges and their centralities to display on the table
        '''

        self.clearContents()
        self.setRowCount(len(new_data_dict))
        self.populate_table(new_data_dict)
