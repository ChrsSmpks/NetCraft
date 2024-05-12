from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem


class CentralityTable(QTableWidget):
    '''
    Custom QTableWidget class to display the centrality for each edge.

    Attributes:
        - data_dict (dictionary): Keys of the dictionary are the edges in the form (u, v) and values are the centralities
    '''

    def __init__(self, data_dict, parent=None):
        '''
        Initialize a new instance of CentralityTable

        Parameters:
            - data_dict (dictionary): Keys of the dictionary are the nodes or the edges in the form (u, v) and values are the centralities
            - in_degree_dict (dictionary): Keys of the dictionary are the nodes and values are the in degree centralities
        '''
        super().__init__(parent)
        self.data_dict = data_dict
        self.in_degree_dict = None
        self.setup_table()

    def setup_table(self):
        '''
        Set the properties of the table and calls another function to populate the table
        '''

        self.setColumnCount(2)
        self.setRowCount(len(self.data_dict))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.setSortingEnabled(True)

        self.setAlternatingRowColors(True)

        self.populate_table()

    def populate_table(self):
        '''
        Populates the table with the keys of the dictionary and their corresponding values
        '''

        for row, (node_or_edge, centrality) in enumerate(self.data_dict.items()):
            edge_item = QTableWidgetItem(str(node_or_edge))
            centrality_item = QTableWidgetItem(str(centrality))

            edge_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            centrality_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.setItem(row, 0, edge_item)
            self.setItem(row, 1, centrality_item)

            if self.in_degree_dict:
                in_degree_centrality = self.in_degree_dict.get(node_or_edge, "")
                in_degree_item = QTableWidgetItem(str(in_degree_centrality))
                in_degree_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, 2, in_degree_item)

    def update_table(self, new_data_dict, heading, in_degree_dict=None):
        '''
        Updates the table to display the new edges and their centralities.

        Parameters:
            - new_data_dict (dictionary): A new dictionary containing nodes or edges and their centralities to display on the table.
            - heading (string): Heading of the table adjusted to "Node" or "Edge" depending on the centrality type.
        '''

        # Temporally disable sorting to eliminate problem due to mismatch of the previous row count and the length of
        # the new dictionary
        self.setSortingEnabled(False)

        self.clearContents()
        self.setRowCount(len(new_data_dict))
        self.in_degree_dict = in_degree_dict
        self.setColumnCount(2) if not in_degree_dict else self.setColumnCount(3)
        self.data_dict = new_data_dict
        self.populate_table()
        if not in_degree_dict:
            self.setHorizontalHeaderLabels([heading, 'Centrality'])
        else:
            self.setHorizontalHeaderLabels([heading, 'Out Degree', 'In Degree'])

        self.setSortingEnabled(True)

    def get_data(self):
        '''
        Retrieve the data dictionary.

        Returns:
            - data_dict (dictionary): Keys of the dictionary are the nodes or the edges in the form (u, v) and values are the centralities
            - in_degree_dict (dictionary): Keys of the dictionary are the nodes and values are the in degree centralities
        '''
        return self.data_dict, self.in_degree_dict
