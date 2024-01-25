from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsTextItem
from PyQt6.QtGui import QPixmap


class NodeObject(QGraphicsPixmapItem):
    def __init__(self, key, x, y, image_path, edges):
        super().__init__()

        self.key = key
        self.neighbors = set()

        pixmap = QPixmap(image_path)  # Load your custom image
        #pixmap.scaledToWidth(5)
        self.setPixmap(pixmap)

        self.setPos(x, y)
        # self.setBrush(Qt.GlobalColor.green)
        self.setAcceptHoverEvents(True)

        self.edges = edges  # List to keep track of connected edges

        # Add text item for the number-key next to the node
        self.graphic_key = QGraphicsTextItem(str(self.key))
        self.graphic_key.setPos(x - 15, y - 15)  # Adjust the position as needed

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

        # Update the visual position of the key
        self.graphic_key.setPos(self.x() - 15, self.y() - 15)

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))


node_list = []
