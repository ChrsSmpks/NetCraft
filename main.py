import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.uic.properties import QtGui

from graphicView import GraphicView
from mainMenu import create_main_menu


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
        layout = QVBoxLayout(self.main_view)

        # Set the main widget as the central widget
        self.setCentralWidget(self.main_view)

        # Create the GraphicView for network visualization
        self.graphic_view = GraphicView()
        layout.addWidget(self.graphic_view)

        # Create main menu
        self.main_menu = create_main_menu(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    Gui = Window()
    Gui.show()
    sys.exit(app.exec())
