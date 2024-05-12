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
    _plot.triggered.connect(lambda: plot_signal(window.side_table, window.side_label.text(), 'g'))

    histogram = QAction(QtGui.QIcon('Icons\\histogram.png'), 'Histogram', toolbar)
    histogram.triggered.connect(lambda: plot_signal(window.side_table, window.side_label.text(), 'h'))

    # Styling
    toolbar.setStyleSheet(toolbar_style)

    # Add action
    toolbar.addAction(_plot)
    toolbar.addAction(histogram)

    return toolbar


def plot_signal(table, algo_text, plot_type):
    table_data, in_degrees = table.get_data()
    if algo_text and algo_text != 'No edges in the graph!':
        algo_text = algo_text.split(': ')[1]
    plot(table_data, algo_text, plot_type, in_degrees)
