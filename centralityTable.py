from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem


class CentralityTable(QTableWidget):
    def __init__(self, data_dict, parent=None):
        super().__init__(parent)
        self.setup_table(data_dict)

    def setup_table(self, data_dict):
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Edge', 'Centrality'])
        self.setRowCount(len(data_dict))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.setSortingEnabled(True)

        self.setAlternatingRowColors(True)

        self.populate_table(data_dict)

    def populate_table(self, data_dict):
        for row, (edge, centrality) in enumerate(data_dict.items()):
            edge_item = QTableWidgetItem(str(edge))
            centrality_item = QTableWidgetItem(str(centrality))

            edge_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            centrality_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.setItem(row, 0, edge_item)
            self.setItem(row, 1, centrality_item)

    def update_table(self, new_data_dict):
        self.clearContents()
        self.setRowCount(len(new_data_dict))
        self.populate_table(new_data_dict)
