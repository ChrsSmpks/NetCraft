from PyQt6.QtCore import QLineF, QPointF
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QPen, QColor


class Edge(QGraphicsLineItem):
    '''
    Custom QGraphicsLineItem class representing an edge.

    Attributes:
        - node1, node2 (Node): Nodes which the edge connects.
        - weight (bool): Indicates whether the edge is weighted.
        - graphic_weight (QGraphicsTextItem): For visual representation of the weight.
    '''
    def __init__(self, node1, node2, weight=None):
        '''
        Initialize a new instance of EdgeObject

        Parameters:
             - node1, node2 (Node): Nodes which the edge connects.
        '''
        super().__init__()

        self.node1 = node1
        self.node2 = node2

        self.weight = weight

        # Add text item for the weight of the edge
        if self.weight:
            self.graphic_weight = QGraphicsTextItem(str(self.weight), parent=self)
            self.graphic_weight.setDefaultTextColor(QColor('white'))

        self.updatePosition()

        pen = QPen(QColor("#dbcdf0"), 1)
        self.setPen(pen)

    def updatePosition(self):
        '''
        Updates the position of the edge.
        '''

        # Find the closest points on the nodes
        node1_point = self.closestPoint(self.node1, self.node2)
        node2_point = self.closestPoint(self.node2, self.node1)

        line = QLineF(node1_point, node2_point)

        self.setLine(line)

        if self.weight:
            # Calculate midpoint
            midpoint = line.pointAt(0.5)

            # Position the graphic_weight based on line orientation
            if line.dx() == 0:  # Vertical line
                self.graphic_weight.setPos(midpoint + QPointF(10, -self.graphic_weight.boundingRect().height() / 2))
            elif line.dy() == 0:  # Horizontal line
                self.graphic_weight.setPos(midpoint + QPointF(-self.graphic_weight.boundingRect().width() / 2, -20))
            else:  # Diagonal line
                angle = line.angle()
                if 45 <= angle <= 135 or 225 <= angle <= 315:  # Line is close to vertical
                    self.graphic_weight.setPos(midpoint + QPointF(10, -self.graphic_weight.boundingRect().height() / 2))
                else:  # Line is close to horizontal
                    self.graphic_weight.setPos(midpoint + QPointF(-self.graphic_weight.boundingRect().width() / 2, -20))

    @staticmethod
    def closestPoint(node, reference_node):
        '''
        Finds the point on the node closest to the reference node.

        Parameters:
            - node, reference_node (Node): Nodes which the edge connects.

        Returns:
            - QPointF: The point of the node closest to the reference node.
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
