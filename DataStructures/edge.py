import math

from PyQt6.QtCore import QLineF, QPointF, Qt
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsPathItem
from PyQt6.QtGui import QPen, QColor, QPolygonF, QPainterPath


class Edge(QGraphicsPathItem):
    '''
    Custom QGraphicsLineItem class representing an edge.

    Attributes:
        - node1, node2 (Node): Nodes which the edge connects.
        - weight (bool): Indicates whether the edge is weighted.
        - graphic_weight (QGraphicsTextItem): For visual representation of the weight.
    '''
    def __init__(self, node1, node2, weight=None, directed=False, bidirectional=0):
        '''
        Initialize a new instance of EdgeObject

        Parameters:
             - node1, node2 (Node): Nodes which the edge connects.
        '''
        super().__init__()

        self.node1 = node1
        self.node2 = node2

        self.weight = weight
        self.directed = directed

        self.bidirectional = bidirectional

        # Add text item for the weight of the edge
        if self.weight:
            self.graphic_weight = QGraphicsTextItem(str(self.weight), parent=self)
            self.graphic_weight.setDefaultTextColor(QColor('white'))

        self.updatePosition()

        pen = QPen(QColor("#dbcdf0"), 1)
        self.setPen(pen)

    def paint(self, painter, option, widget):
        if self.directed:
            # Find the closest points on the nodes
            node1_point = self.closestPoint(self.node1, self.node2)
            node2_point = self.closestPoint(self.node2, self.node1)

            arrow_size = 15

            if not self.bidirectional:
                line = QLineF(node1_point, node2_point)

                # Create a QPainterPath representing the line segment
                path = QPainterPath()
                path.moveTo(line.p1())
                path.lineTo(line.p2())

                # Set the QPainterPath to the QGraphicsPathItem
                self.setPath(path)

                painter.setPen(QPen(QColor("#dbcdf0"), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                    Qt.PenJoinStyle.RoundJoin))
                painter.drawLine(line)

                # Draw arrow
                angle = math.atan2(line.y1() - line.y2(), line.x1() - line.x2())

                arrow_p1 = line.p2() + QPointF(
                    arrow_size * math.cos(angle + math.pi / 5),
                    arrow_size * math.sin(angle + math.pi / 5)
                )
                arrow_p2 = line.p2() + QPointF(
                    arrow_size * math.cos(angle - math.pi / 5),
                    arrow_size * math.sin(angle - math.pi / 5)
                )
            else:
                midpoint = QPointF((node1_point.x() + node2_point.x()) / 2, (node1_point.y() + node2_point.y()) / 2)

                # Calculate the control point to create a slight arc
                if self.bidirectional == 2:
                    control_point = QPointF(midpoint.x(), midpoint.y() + 20)
                else:
                    control_point = QPointF(midpoint.x(), midpoint.y() - 20)

                # Create a QPainterPath to draw the curved line
                path = QPainterPath()
                path.moveTo(node1_point)
                path.quadTo(control_point, node2_point)

                # Set the QPainterPath to the QGraphicsPathItem
                self.setPath(path)

                # Draw the path
                painter.setPen(QPen(QColor("#dbcdf0"), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.drawPath(path)

                # Calculate angle for arrow
                angle = math.atan2(node2_point.y() - control_point.y(), node2_point.x() - control_point.x())

                # Calculate the position for the arrow, slightly back from the endpoint
                arrow_length = 25  # Adjust this value as needed
                arrow_x = node2_point.x() - arrow_length * math.cos(angle)
                arrow_y = node2_point.y() - arrow_length * math.sin(angle)
                arrow_end_point = QPointF(arrow_x, arrow_y)

                # Draw arrow
                arrow_p1 = arrow_end_point + QPointF(
                    arrow_size * math.cos(angle + math.pi / 5),
                    arrow_size * math.sin(angle + math.pi / 5)
                )
                arrow_p2 = arrow_end_point + QPointF(
                    arrow_size * math.cos(angle - math.pi / 5),
                    arrow_size * math.sin(angle - math.pi / 5)
                )

            arrow_points = QPolygonF([node2_point, arrow_p1, arrow_p2])
            painter.setBrush(QColor("#dbcdf0"))
            painter.drawPolygon(arrow_points)
        else:
            super().paint(painter, option, widget)

    def updatePosition(self):
        '''
        Updates the position of the edge.
        '''

        # Find the closest points on the nodes
        node1_point = self.closestPoint(self.node1, self.node2)
        node2_point = self.closestPoint(self.node2, self.node1)

        line = QLineF(node1_point, node2_point)

        # Create a QPainterPath representing the line segment
        path = QPainterPath()
        path.moveTo(line.p1())
        path.lineTo(line.p2())

        # Set the QPainterPath to the QGraphicsPathItem
        self.setPath(path)

        if self.weight:
            # Calculate midpoint
            midpoint = line.pointAt(0.5)

            if self.bidirectional == 2:
                # Position the graphic_weight based on line orientation
                if line.dx() == 0:  # Vertical line
                    self.graphic_weight.setPos(midpoint + QPointF(-30, self.graphic_weight.boundingRect().height() / 2))
                elif line.dy() == 0:  # Horizontal line
                    self.graphic_weight.setPos(midpoint + QPointF(-self.graphic_weight.boundingRect().width() / 2, 10))
                else:  # Diagonal line
                    angle = line.angle()
                    if 45 <= angle <= 135 or 225 <= angle <= 315:  # Line is close to vertical
                        self.graphic_weight.setPos(
                            midpoint + QPointF(-30, -self.graphic_weight.boundingRect().height() / 2))
                    else:  # Line is close to horizontal
                        self.graphic_weight.setPos(
                            midpoint + QPointF(-self.graphic_weight.boundingRect().width() / 2, 10))
            else:
                # Position the graphic_weight based on line orientation
                if line.dx() == 0:  # Vertical line
                    self.graphic_weight.setPos(midpoint + QPointF(10, -self.graphic_weight.boundingRect().height() / 2))
                elif line.dy() == 0:  # Horizontal line
                    val = -20 if not self.bidirectional else -30
                    self.graphic_weight.setPos(midpoint + QPointF(-self.graphic_weight.boundingRect().width() / 2, val))
                else:  # Diagonal line
                    angle = line.angle()
                    if 45 <= angle <= 135 or 225 <= angle <= 315:  # Line is close to vertical
                        self.graphic_weight.setPos(midpoint + QPointF(10, -self.graphic_weight.boundingRect().height() / 2))
                    else:  # Line is close to horizontal
                        val = -20 if not self.bidirectional else -30
                        self.graphic_weight.setPos(midpoint + QPointF(-self.graphic_weight.boundingRect().width() / 2, val))

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

    def updateWeight(self, new_weight):
        '''
        Updates the weight for the edge and node's neighbors dictionary.

        Parameters:
            -new_weight (float): The new weight of the edge.
        '''
        self.weight = new_weight
        self.graphic_weight.setPlainText(str(new_weight))
        self.node1.neighbors[self.node2] = new_weight
        self.node2.neighbors[self.node1] = new_weight

    def updateBidirectional(self, bidirectional):
        self.bidirectional = bidirectional
        self.updatePosition()
