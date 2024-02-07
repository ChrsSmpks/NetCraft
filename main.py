import sys

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QDockWidget

from centralityTable import CentralityTable
from graphicView import GraphicView
from mainMenu import create_main_menu
from fileIO import save_dialog
from nodeObject import node_list
from style_sheets import main_page_style, graphic_view_style, side_style, table_style


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        # Set window properties
        self.setWindowTitle('NetCraft Insight')
        #self.setWindowIcon(QtGui.QIcon(logo_path))
        #self.resize(960, 720)

        # Get the primary screen from QGuiApplication
        screen = QGuiApplication.primaryScreen()

        # Get the screen's geometry
        screen_geometry = screen.geometry()

        # Set window size
        self.resize(int(0.625 * screen_geometry.width()), int(0.83 * screen_geometry.height()))

        # Calculate the position to center the main window
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Set the position
        self.move(x, y-20)

        # Create the main widget and layout
        self.main_view = QWidget(self)
        # self.main_view.setStyleSheet(main_page_style)
        layout = QVBoxLayout(self.main_view)

        # Set the main widget as the central widget
        self.setCentralWidget(self.main_view)

        # Create the GraphicView for network visualization
        self.graphic_view = GraphicView(self)
        self.graphic_view.setStyleSheet(graphic_view_style)
        layout.addWidget(self.graphic_view)

        # Create status bar to display number of nodes and edges
        self.statusBar().showMessage('Nodes: 0 | Edges: 0')

        # Create main menu
        self.main_menu = create_main_menu(self)

        # Create side dock for Centrality info

        # Create a side widget
        side_widget = QWidget(self)

        side_widget.setStyleSheet(side_style)
        side_layout = QVBoxLayout(side_widget)

        # Create a label to display info about the algorithm used
        self.side_label = QLabel(side_widget)

        # Create an empty table to display centralities
        self.side_table = CentralityTable({})
        self.side_table.setStyleSheet(table_style)

        side_layout.addWidget(self.side_label)
        side_layout.addWidget(self.side_table)

        # Create a dock widget
        self.dock_widget = QDockWidget('Centralities', self)
        self.dock_widget.setWidget(side_widget)
        self.dock_widget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.dock_widget.setHidden(True)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget, Qt.Orientation.Vertical)

    def event(self, e):
        if e.type() == QEvent.Type.StatusTip:
            return True
        return super().event(e)

    def closeEvent(self, event):
        if not save_dialog(self, 1) and node_list:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    Gui = Window()
    Gui.show()
    sys.exit(app.exec())
