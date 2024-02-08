from PyQt6.QtCore import QTimer, QPointF, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu

from edgeObject import EdgeObject
from nodeObject import NodeObject, node_list
from style_sheets import context_menu_style


class GraphicView(QGraphicsView):
    '''
    Custom QGraphicsView class to visually display the graph with its nodes and edges

    Attributes:
        - main_window (QMainWindow): The main window of the app
        - scene (QGraphicsScene): Place to display the graph
        - edges (list of EdgeObject): List to keep track of connected edges
        - zoom_factor (float): Zoom factor for zooming operations
        - zoom_level (int): Zoom level
        - timer (QTimer): Timer to continuously update the view
    '''
    def __init__(self, main_window):
        '''
        Initialize a new instance of GraphicView

        Parameters:
             - main_window (QMainWindow): The main window of the app
        '''
        super().__init__()

        self.main_window = main_window

        self.source_node = None

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)

        self.edges = []

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
        '''Handle wheel events for zooming'''

        factor = self.zoom_factor
        if event.angleDelta().y() < 0:
            factor = 1.0 / self.zoom_factor

        self.scale(factor, factor)
        self.zoom_level += 1 if factor > 1 else -1

    def updateView(self):
        '''Updates the visual display of the graph'''
        self.scene.update()

    def contextMenu(self, pos):
        '''
        Decide which of the 3 context menus to display based on the clicked position

        Parameters:
            - pos (QPointF): position where the user right-clicked
        '''
        item = self.itemAt(pos)
        if item is None:
            self.showEmptySpaceContextMenu(pos)
        elif isinstance(item, NodeObject):
            self.showNodeContextMenu(item, pos)
        elif isinstance(item, EdgeObject):
            # Show context menu for a link
            self.showLinkContextMenu(item, pos)

    def showEmptySpaceContextMenu(self, pos):
        '''
        Displays the context menu containing actions Add Node, Clear All when right-clicking on empty space

        Parameters:
            - pos (QPointF): position to display the conext menu (where the user right-clicked)
        '''
        context_menu = QMenu(self)
        context_menu.setStyleSheet(context_menu_style)

        add_node_action = context_menu.addAction("Add Node")
        add_node_action.triggered.connect(lambda: self.addNode(pos))

        clear_all_action = context_menu.addAction("Clear All")
        clear_all_action.triggered.connect(self.clearAll)

        context_menu.exec(self.mapToGlobal(pos))

    def showNodeContextMenu(self, node, pos):
        '''
        Displays the context menu containing actions Delete Node, Add Link when right-clicking on a node

        Parameters:
            - pos (QPointF): position to display the conext menu (where the user right-clicked)
        '''
        context_menu = QMenu(self)
        context_menu.setStyleSheet(context_menu_style)

        delete_node_action = context_menu.addAction("Delete Node")
        delete_node_action.triggered.connect(lambda: self.deleteNode(node))

        add_link_action = context_menu.addAction("Add Link")
        add_link_action.triggered.connect(lambda: self.startAddingLink(node, pos))

        # You can add more actions as needed for nodes

        context_menu.exec(self.mapToGlobal(pos))

    def showLinkContextMenu(self, link, pos):
        '''
        Displays the context menu containing action Delete Link when right-clicking on a link

        Parameters:
            - pos (QPointF): position to display the conext menu (where the user right-clicked)
        '''
        context_menu = QMenu(self)
        context_menu.setStyleSheet(context_menu_style)

        delete_link_action = context_menu.addAction("Delete Link")
        delete_link_action.triggered.connect(lambda: self.deleteLink(link))

        context_menu.exec(self.mapToGlobal(pos))

    def addLink(self, node1, node2):
        '''
        Add a link between 2 nodes and update the status bar accordingly

        Parameters:
            - node1, node2 (NodeObject): Nodes which the edge connects.
        '''
        node1.neighbors.add(node2)
        node2.neighbors.add(node1)

        new_edge = EdgeObject(node1, node2)
        new_edge.setZValue(1)
        self.edges.append(new_edge)
        self.scene.addItem(new_edge)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')

    def deleteLink(self, link):
        '''
        Delete a link and update the status bar accordingly

        Parameters:
            - link (EdgeObject): Link to delete
        '''

        self.scene.removeItem(link)
        self.edges.remove(link)

        link.node1.neighbors.discard(link.node2)
        link.node2.neighbors.discard(link.node1)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')

    def addNode(self, pos):
        '''
        Add a node to the graph and update the status bar accordingly

        Parameters:
            - pos (QPointF): position to add the node
        '''

        if not node_list:
            new_node = NodeObject(0, pos.x(), pos.y(), "Icons\\node.png", self.edges)
        else:
            new_node = NodeObject(node_list[-1].key + 1, pos.x(), pos.y(), "Icons\\node.png", self.edges)
        node_list.append(new_node)

        new_node.setZValue(2)
        # self.nodes.append(new_node_object)
        self.scene.addItem(new_node)

        # Add text item for the number-key next to the node
        new_node.graphic_key.setZValue(2)
        self.scene.addItem(new_node.graphic_key)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')

    def deleteNode(self, node):
        '''
        Delete a node and update the status bar accordingly

        Parameters:
            - node (NodeObject): node to delete
        '''

        # Remove only the edges connected to the deleted node
        if node is not None:
            for edge in self.edges.copy():  # Use copy to avoid modifying the list during iteration
                if edge.node1 == node or edge.node2 == node:
                    self.scene.removeItem(edge)
                    self.edges.remove(edge)

        # Remove the node from the scene and the list of nodes
        self.scene.removeItem(node)
        self.scene.removeItem(node.graphic_key)

        # Remove the Node instance from node_list
        node_list.remove(node)

        # Clear the edges list from the deleted node
        node.neighbors.clear()

        # Remove the deleted node from the neighbor sets of other nodes
        for other_node in node_list:
            other_node.neighbors.discard(node)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')

    def startAddingLink(self, node, pos):
        '''
        Starts adding a link between 2 nodes. Sets the source node and waits for the second one to be clicked

        Parameters:
             - node (NodeObject): First of the 2 nodes to add a link
             - pos (QPointF)
        '''

        # Set the current node for linking
        self.source_node = node

        # Connect the scene's mouse press event to start the link
        # self.sceneMousePressEvent(pos)

    def sceneMousePressEvent(self, pos):
        '''
        Selects the second node to add a link and updates the status bar accordingly
        
        Parameters:
            pos pos (QPointF): Position of the destination
        '''

        if isinstance(pos, QPointF):
            # Convert scene coordinates to view coordinates
            pos = self.mapFromScene(pos)

        destination_node = self.scene.itemAt(pos.x(), pos.y(), self.transform())
        if isinstance(destination_node, NodeObject) and destination_node != self.source_node:
            self.source_node.neighbors.add(destination_node)
            destination_node.neighbors.add(self.source_node)

            new_edge = EdgeObject(self.source_node, destination_node)
            self.edges.append(new_edge)
            self.scene.addItem(new_edge)

            self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')

    def mousePressEvent(self, event):
        '''
        Event handler of the mousePressEvent. If there is a source node has already been selected to add a link connect
        the second node

        Parameters:
             - event (QMouseEvent)
        '''
        if self.source_node is not None:
            self.sceneMousePressEvent(event.pos())
            self.source_node = None
        else:
            super().mousePressEvent(event)

    def clearAll(self):
        '''
        Delete all nodes and edges of the graph and update the status bar accordingly

        Returns:
            - 0: If user chose Cancel option in the dialog that pops up
        '''
        from fileIO import save_dialog
        if not save_dialog(self.main_window, 0):
            return 0

        self.scene.clear()
        self.edges = []

        # Reset the neighbor sets of all nodes
        for node in node_list:
            node.neighbors.clear()

        node_list.clear()

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')
