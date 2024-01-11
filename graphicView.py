from PyQt6.QtCore import QTimer, QPointF, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu

from edgeObject import EdgeObject
from nodeObject import NodeObject
from node import Node, node_list


class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.adding_link_node = None

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        #self.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)

        #self.nodes = []
        self.edges = []
        self.nodes_map = {}

        # self.moveObject = MovingObject(50, 50, "C:\\Users\\Raven\\Desktop\\node.png")
        # self.moveObject2 = MovingObject(100, 100, "C:\\Users\\Raven\\Desktop\\node11.png")
        # self.moveObject = MovingObject(50, 50, "NodeIcons\\node1.png")

        #self.node1 = NodeObject(50, 50, "NodeIcons\\node11.png", self.edges)
        #self.node2 = NodeObject(100, 100, "NodeIcons\\node11.png", self.edges)

        # self.scene.addItem(self.node1)
        # self.scene.addItem(self.node2)

        '''self.edge = EdgeObject(self.node1, self.node2)

        self.nodes.extend([self.node1, self.node2])
        self.edges.append(self.edge)

        for node in self.nodes:
            self.scene.addItem(node)

        for edge in self.edges:
            self.scene.addItem(edge)'''

        # Set scroll hand drag mode for panning
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        # Set up zooming parameters
        self.zoom_factor = 1.2
        self.zoom_level = 0

        # Create a QTimer to continuously update the view
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateView)
        self.timer.start(16)  # 16 ms, which is roughly 60 frames per second

    def wheelEvent(self, event):
        # Handle wheel events for zooming
        factor = self.zoom_factor
        if event.angleDelta().y() < 0:
            factor = 1.0 / self.zoom_factor

        self.scale(factor, factor)
        self.zoom_level += 1 if factor > 1 else -1

    def updateView(self):
        self.scene.update()

    def contextMenu(self, pos):
        item = self.itemAt(pos)
        if item is None:
            self.showEmptySpaceContextMenu(pos)
        elif isinstance(item, NodeObject):
            self.showNodeContextMenu(item, pos)
        elif isinstance(item, EdgeObject):
            # Show context menu for a link
            self.showLinkContextMenu(item, pos)

    def showEmptySpaceContextMenu(self, pos):
        context_menu = QMenu(self)

        add_node_action = context_menu.addAction("Add Node")
        add_node_action.triggered.connect(lambda: self.addNode(pos))

        clear_all_action = context_menu.addAction("Clear All")
        clear_all_action.triggered.connect(self.clearAll)

        context_menu.exec(self.mapToGlobal(pos))

    def showNodeContextMenu(self, node, pos):
        context_menu = QMenu(self)

        delete_node_action = context_menu.addAction("Delete Node")
        delete_node_action.triggered.connect(lambda: self.deleteNode(node))

        add_link_action = context_menu.addAction("Add Link")
        add_link_action.triggered.connect(lambda: self.startAddingLink(node, pos))

        # You can add more actions as needed for nodes

        context_menu.exec(self.mapToGlobal(pos))

    def showLinkContextMenu(self, link, pos):
        context_menu = QMenu(self)

        delete_link_action = context_menu.addAction("Delete Link")
        delete_link_action.triggered.connect(lambda: self.deleteLink(link))

        context_menu.exec(self.mapToGlobal(pos))

    def deleteLink(self, link):
        self.scene.removeItem(link)
        self.edges.remove(link)

    def addNode(self, pos):
        new_node = Node(len(node_list) + 1)
        node_list.append(new_node)

        new_node_object = NodeObject(pos.x(), pos.y(), "NodeIcons\\node11.png", self.edges)
        # self.nodes.append(new_node_object)
        self.scene.addItem(new_node)

        self.nodes_map[new_node] = new_node_object

        for node in node_list:
            print('Node', node.key, 'neighbors:', node.neighbors)

    def deleteNode(self, node):
        # Remove only the edges connected to the deleted node
        for edge in self.edges.copy():  # Use copy to avoid modifying the list during iteration
            if edge.node1 == node or edge.node2 == node:
                self.scene.removeItem(edge)
                self.edges.remove(edge)

        # Remove the node from the scene and the list of nodes
        self.scene.removeItem(node)
        #self.nodes.remove(node)
        node_list.remove(node)

        # Clear the edges list from the deleted node
        node.edges = []
        node.neighbors = []

    def startAddingLink(self, node, pos):
        # Set the current node for linking
        self.adding_link_node = node

        # Connect the scene's mouse press event to start the link
        # self.scene.mousePressEvent = self.addLinkStart
        # self.scene.mousePressEvent = lambda event: self.addLinkStart(event, node)
        self.sceneMousePressEvent(pos)

    def sceneMousePressEvent(self, pos):
        if isinstance(pos, QPointF):
            # Convert scene coordinates to view coordinates
            pos = self.mapFromScene(pos)

        # item = self.scene.itemAt(pos)
        item = self.scene.itemAt(pos.x(), pos.y(), self.transform())
        if isinstance(item, NodeObject) and item != self.adding_link_node:
            new_edge = EdgeObject(self.adding_link_node, item)
            self.edges.append(new_edge)
            self.scene.addItem(new_edge)

    def mousePressEvent(self, event):
        if self.adding_link_node is not None:
            self.sceneMousePressEvent(event.pos())
            self.adding_link_node = None
        else:
            super().mousePressEvent(event)

    '''def addLinkStart(self, event):
        print("Custom mousePressEvent is called")
        if isinstance(event, QPointF):
            # Convert scene coordinates to view coordinates
            pos = self.mapFromScene(event)
        else:
            pos = event.pos()

        item = self.scene.itemAt(pos)
        if isinstance(item, NodeObject) and item != self.adding_link_node:
            new_edge = EdgeObject(self.adding_link_node, item)
            self.edges.append(new_edge)
            self.scene.addItem(new_edge)

        self.scene.mousePressEvent = QGraphicsScene.mousePressEvent
        self.adding_link_node = None'''

    def clearAll(self):
        self.scene.clear()
        # self.nodes = []
        self.edges = []
        self.nodes_map = {}
