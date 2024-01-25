from PyQt6.QtCore import QLineF, QPointF, Qt
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen, QColor


class EdgeObject(QGraphicsLineItem):
    def __init__(self, node1, node2):
        super().__init__()

        self.node1 = node1
        self.node2 = node2

        self.updatePosition()

        pen = QPen(QColor("#dbcdf0"), 1)
        self.setPen(pen)

    def updatePosition(self):
        # Find the closest points on the nodes
        node1_point = self.closestPoint(self.node1, self.node2)
        node2_point = self.closestPoint(self.node2, self.node1)

        self.setLine(QLineF(node1_point, node2_point))

    @staticmethod
    def closestPoint(node, reference_node):
        '''# Find the point on the node closest to the reference node
        center_point = node.pos() + QPointF(node.pixmap().width() / 2, node.pixmap().height() / 2)'''
        if node is not None and node.scene() is not None:
            center_point = node.pos() + QPointF(node.pixmap().width() / 2, node.pixmap().height() / 2)
        else:
            return reference_node.pos()

        direction = reference_node.pos() - center_point
        direction /= QLineF(center_point, reference_node.pos()).length()  # Normalize the direction vector

        # return center_point + direction * (node.pixmap().width() / 2, node.pixmap().height() / 2)
        # Multiply the direction components individually
        return center_point + QPointF(direction.x() * (node.pixmap().width() / 2),
                                      direction.y() * (node.pixmap().height() / 2))
