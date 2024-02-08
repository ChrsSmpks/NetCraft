from PyQt6.QtCore import QLineF, QPointF, Qt
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen, QColor


class EdgeObject(QGraphicsLineItem):
    '''
    Custom QGraphicsLineItem class representing an edge.

    Attributes:
        - node1, node2 (NodeObject): Nodes which the edge connects.
    '''
    def __init__(self, node1, node2):
        '''
        Initialize a new instance of EdgeObject

        Parameters:
             - node1, node2 (NodeObject): Nodes which the edge connects.
        '''
        super().__init__()

        self.node1 = node1
        self.node2 = node2

        self.updatePosition()

        pen = QPen(QColor("#dbcdf0"), 1)
        self.setPen(pen)

    def updatePosition(self):
        '''
        Updates the position of the edge
        '''

        # Find the closest points on the nodes
        node1_point = self.closestPoint(self.node1, self.node2)
        node2_point = self.closestPoint(self.node2, self.node1)

        self.setLine(QLineF(node1_point, node2_point))

    @staticmethod
    def closestPoint(node, reference_node):
        '''
        Finds the point on the node closest to the reference node

        Parameters:
            - node, reference_node (NodeObject): Nodes which the edge connects.

        Returns:
            - QPointF: The point of the node closest to the reference node
        '''
        if node is not None and node.scene() is not None:
            center_point = node.pos() + QPointF(node.pixmap().width() / 2, node.pixmap().height() / 2)
        else:
            return reference_node.pos()

        direction = reference_node.pos() - center_point
        direction /= QLineF(center_point, reference_node.pos()).length()  # Normalize the direction vector

        # Multiply the direction components individually
        return center_point + QPointF(direction.x() * (node.pixmap().width() / 2),
                                      direction.y() * (node.pixmap().height() / 2))
