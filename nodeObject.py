from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap


class NodeObject(QGraphicsPixmapItem):
    def __init__(self, x, y, image_path, edges):
        super().__init__()

        pixmap = QPixmap(image_path)  # Load your custom image
        self.setPixmap(pixmap)

        self.setPos(x, y)
        # self.setBrush(Qt.GlobalColor.green)
        self.setAcceptHoverEvents(True)

        self.edges = edges  # List to keep track of connected edges

        self.deleted = False  # Flag to track whether the node is deletedψ

    # mouse click event
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            event.accept()

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

        # Move the connected edges when the node is moved
        for edge in self.edges:
            edge.updatePosition()

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))