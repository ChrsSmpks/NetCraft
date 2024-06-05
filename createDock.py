import csv

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog

from centralityTable import CentralityTable
from style_sheets import table_style, side_style


def create_dock(window):
    # Create a side widget
    side_widget = QWidget(window)

    side_widget.setStyleSheet(side_style)
    side_layout = QVBoxLayout(side_widget)

    side_header_layout = QHBoxLayout()

    # Create a label to display info about the algorithm used
    side_label = QLabel(side_widget)
    side_label.setStyleSheet('color: white;')

    # Create Export Button
    export_button = QPushButton()
    export_button.setIcon(QIcon('Icons\\export.png'))
    export_button.setToolTip('Export CSV')
    export_button.clicked.connect(lambda: export_button_clicked(window))

    side_header_layout.addWidget(side_label)
    side_header_layout.addWidget(export_button)

    # Create an empty table to display centralities
    side_table = CentralityTable({})
    side_table.setStyleSheet(table_style)

    #side_layout.addWidget(side_label)
    side_layout.addLayout(side_header_layout)
    side_layout.addSpacing(10)
    side_layout.addWidget(side_table)

    return side_widget, side_label, side_table


def export_button_clicked(window):
    data, _ = window.side_table.get_data()

    save_path, _ = QFileDialog.getSaveFileName(window, "Save Centralities Table", "", "CSV Files (*.csv)")

    # Writing to CSV file
    if save_path:
        with open(save_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for edge_node, centrality in data.items():
                writer.writerow([edge_node, centrality])
