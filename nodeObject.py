from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsTextItem
from PyQt6.QtGui import QPixmap, QColor


class NodeObject(QGraphicsPixmapItem):
    '''
    Custom QGraphicsPixmapItem class representing a node.

    Attributes:
        - key (int): Node's key
        - neiboghbors (set of NodeObject): Stores all neighbors of the node
        - edges (list of EdgeObject): List to keep track of connected edges
        - graphic_key (QGraphicsTextItem): For visual representation of the key
    '''
    def __init__(self, key, x, y, image_path, edges):
        '''
        Initialize a new instance of NodeObject

        Parameters:
            - key (int): Node's key
            - x (float): x coordinate of the node
            - y (float): y coordinate of the node
            - image_path (str): file path of the image which represents the node
            - edges (list of EdgeObject): List to keep track of connected edges
        '''
        super().__init__()

        self.key = key
        self.neighbors = set()

        pixmap = QPixmap(image_path)  # Load custom node image
        self.setPixmap(pixmap)

        self.setPos(x, y)
        self.setAcceptHoverEvents(True)

        self.edges = edges

        # Add text item for the number-key next to the node
        self.graphic_key = QGraphicsTextItem(str(self.key))
        self.graphic_key.setDefaultTextColor(QColor('white'))
        self.graphic_key.setPos(x - 15, y - 15)  # Adjust the position as needed

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            event.accept()

    def mouseMoveEvent(self, event):
        '''
        Event handler. Updates the visual position of the node and its key.

        Parameters:
            - event(QQGraphicsSceneMouseEvent): The mouse event object
        '''
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


# List of NodeObject used in other files
node_list = []
