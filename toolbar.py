from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar

from style_sheets import toolbar_style
from plot import plot


def create_toolbar(window):
    toolbar = QToolBar(window)
    toolbar.setMovable(False)
    window.addToolBar(toolbar)

    _plot = QAction(QtGui.QIcon('Icons\\plot.png'), 'Plot Centralities', toolbar)
    _plot.triggered.connect(lambda: plot_signal(window.side_table, window.side_label.text()))

    # Styling
    toolbar.setStyleSheet(toolbar_style)

    # Add action
    toolbar.addAction(_plot)

    return toolbar


def plot_signal(table, algo_text):
    table_data = table.get_data()
    if algo_text and algo_text != 'No edges in the graph!':
        algo_text = algo_text.split(': ')[1]
    plot(table_data, algo_text)
