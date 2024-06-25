from PyQt6 import QtGui
from PyQt6.QtCore import QTimer, QPointF, Qt, QPoint
from PyQt6.QtGui import QPainter, QAction
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu, QMessageBox

from DataStructures.edge import Edge
from DataStructures.node import Node, node_list
from weightDialog import WeightDialog
from style_sheets import context_menu_style


class GraphicView(QGraphicsView):
    '''
    Custom QGraphicsView class to visually display the graph with its nodes and edges

    Attributes:
        - main_window (QMainWindow): The main window of the app
        - scene (QGraphicsScene): Place to display the graph
        - edges (list of Edge): List to keep track of connected edges
        - seen_edges (set of Edge): Set to make search for duplicate edges faster
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
        self.scene_pos = None

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        # self.setOptimizationFlags(QGraphicsView.OptimizationFlag.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)

        self.edges = []
        self.seen_edges = set()

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

        # Get the global cursor position at the time of the wheel event
        global_cursor_pos = event.globalPosition()

        # Map the global cursor position to the local coordinate system of the widget
        cursor_position = self.mapFromGlobal(global_cursor_pos)

        # Map the cursor position to scene coordinates
        scene_pos = self.mapToScene(cursor_position.toPoint())

        self.centerOn(scene_pos)

        # Adjust the transformation matrix to zoom around the cursor position
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
        elif isinstance(item, Node):
            self.showNodeContextMenu(item, pos)
        elif isinstance(item, Edge):
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
        add_node_action.triggered.connect(lambda: self.addNode(pos, self.main_window.node_color))

        clear_all_action = context_menu.addAction("Clear All")
        clear_all_action.triggered.connect(self.clearAll)

        context_menu.exec(self.mapToGlobal(pos))

    def showNodeContextMenu(self, node, pos):
        '''
        Displays the context menu containing actions Delete Node, Add Link when right-clicking on a node

        Parameters:
            - node (Node): The node that was right-clicked.
            - pos (QPointF): Position to display the context menu (where the user right-clicked).
        '''
        context_menu = QMenu(self)
        context_menu.setStyleSheet(context_menu_style)

        delete_node_action = context_menu.addAction("Delete Node")
        delete_node_action.triggered.connect(lambda: self.deleteNode(node))

        add_link_action = context_menu.addAction("Add Link")
        add_link_action.triggered.connect(lambda: self.startAddingLink(node))

        # Create Colors submenu
        color_menu = context_menu.addMenu('Color')

        colors_acts = [QAction(QtGui.QIcon('Icons\\green.png'), 'Green'),
                       QAction(QtGui.QIcon('Icons\\pink.png'), 'Pink'),
                       QAction(QtGui.QIcon('Icons\\blue.png'), 'Blue'),
                       QAction(QtGui.QIcon('Icons\\purple.png'), 'Purple'),
                       QAction(QtGui.QIcon('Icons\\red.png'), 'Red')]

        color_menu.addActions(colors_acts)

        for act in colors_acts:
            act.triggered.connect(lambda checked, nod=node, color=act.text(): self.changeColor(nod, color))

        context_menu.exec(self.mapToGlobal(pos))

    def showLinkContextMenu(self, link, pos):
        '''
        Displays the context menu containing action Delete Link and Change Weight (if graph is weighted)
        when right-clicking on a link.

        Parameters:
            - link (Edge): The edge that was right-clicked.
            - pos (QPointF): Position to display the conext menu (where the user right-clicked).
        '''
        context_menu = QMenu(self)
        context_menu.setStyleSheet(context_menu_style)

        delete_link_action = context_menu.addAction("Delete Link")
        delete_link_action.triggered.connect(lambda: self.deleteLink(link))

        if self.main_window.weighted:
            change_wait_action = context_menu.addAction("Change Weight")
            change_wait_action.triggered.connect(lambda: self.changeWeight(link))

        context_menu.exec(self.mapToGlobal(pos))

    def changeWeight(self, edge):
        '''
        Changes the weight of the given edge.

        Parameters:
            - edge (Edge): The edge to change weight of.
        '''
        dialog = WeightDialog()
        weight_input = dialog.get_user_input()
        if weight_input:
            edge.updateWeight(weight_input)
            self.main_window.saved = False

    def changeColor(self, node, color):
        '''
        Changes the icon of a node to have a different color.

        Parameters:
            - node (Node): The node to change color of.
            - color (String): The new color to change to.
        '''
        node.changeColor(color)
        self.main_window.saved = False

    def recalculate(self):
        '''
        Recalculates the centralities and updates the centrality table when centralities have already been calculated.
        '''
        algo_text = self.main_window.side_label.text()
        if not self.main_window.dock_widget.isHidden() and algo_text != 'No edges in the graph!':
            if algo_text == 'Algorithm: Spanning Edge Betweenness':
                from mainMenu import connect_spanning_edge_btw
                connect_spanning_edge_btw(self.main_window, node_list)
            elif algo_text == 'Algorithm: TreeC':
                from Algorithms.SpanningCentralities.treeC import treeC
                treeC(self.main_window, node_list)
            elif algo_text == 'Algorithm: Fast-TreeC':
                from Algorithms.SpanningCentralities.fastTreeC import fastTreeC
                fastTreeC(self.main_window, node_list)
            elif algo_text == 'Algorithm: TGT':
                from Algorithms.SpanningCentralities.tgt import tgt
                tgt(self.main_window, node_list)
            elif algo_text == 'Algorithm: Degree Centrality':
                from Algorithms.StandardCentralities.degreeCentrality import degreeCentrality
                degreeCentrality(self.main_window, node_list, self.main_window.weighted, self.main_window.directed)
            elif algo_text == 'Algorithm: Edge Betweenness':
                from Algorithms.StandardCentralities.edgeBetweenness import edgeBetweenness
                edgeBetweenness(self.main_window, node_list)
            elif algo_text == 'Algorithm: Betweenness':
                from Algorithms.StandardCentralities.betweenness import betweenness
                betweenness(self.main_window, node_list)
            elif algo_text == 'Algorithm: Closeness':
                from Algorithms.StandardCentralities.closeness import closeness
                closeness(self.main_window, node_list)

    def addLink(self, node1, node2, weight=None, check_duplicates=True):
        '''
        Add a link between 2 nodes and update the status bar and centrality table accordingly.

        Parameters:
            - node1, node2 (Node): Nodes which the edge connects.
        '''
        bidirectional = 0
        if not self.main_window.directed:
            pass
            """if check_duplicates:
                # If edge already exists return
                if tuple(sorted((node1.key, node2.key))) in self.seen_edges:
                    QMessageBox.warning(self, 'Invalid Input', f'Link {node1.key, node2.key} already exists.')
                    return
                else:
                    self.seen_edges.add(tuple(sorted((node1.key, node2.key))))"""
        else:
            """if (node1.key, node2.key) in self.seen_edges:
                QMessageBox.warning(self, 'Invalid Input', f'Link {node1.key, node2.key} already exists.')
                return
            else:
                self.seen_edges.add((node1.key, node2.key))
            for edge in self.edges:
                if edge.node1 == node2 and edge.node2 == node1:
                    bidirectional = 2
                    break"""
            pass

        # If the link added creates a bidirectional path between the 2 nodes redraw the other link between them.
        if bidirectional:
            for edge in self.edges.copy():
                if edge.node1 == node2 and edge.node2 == node1:
                    edge.updateBidirectional(1)

        node1.neighbors[node2] = weight
        if not self.main_window.directed:
            node2.neighbors[node1] = weight
        else:
            node2.neighbors_in[node1] = weight

        new_edge = Edge(node1, node2, weight, self.main_window.directed, bidirectional)
        new_edge.setZValue(1)
        self.edges.append(new_edge)
        self.scene.addItem(new_edge)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)} | Custom Graph')
        self.main_window.saved = False

    def deleteLink(self, link):
        '''
        Delete a link and update the status bar and centrality table accordingly.

        Parameters:
            - link (Edge): Link to delete.
        '''
        # If there is a bidirectional path between the 2 nodes of the link redraw the other link between them.
        if link.bidirectional:
            for edge in self.edges:
                if edge.node1 == link.node2 and edge.node2 == link.node1:
                    edge.updateBidirectional(0)

        if (link.node1.key, link.node2.key) in self.seen_edges:
            self.seen_edges.remove((link.node1.key, link.node2.key))
        elif not self.main_window.directed and (link.node2.key, link.node1.key) in self.seen_edges:
            self.seen_edges.remove((link.node2.key, link.node1.key))

        self.scene.removeItem(link)
        self.edges.remove(link)

        link.node1.neighbors.pop(link.node2)
        if not self.main_window.directed:
            link.node2.neighbors.pop(link.node1)
        else:
            link.node2.neighbors_in.pop(link.node1)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)} | Custom Graph')
        self.main_window.saved = False

        self.recalculate()

    def addNode(self, pos, color='green'):
        '''
        Add a node to the graph and update the status bar and centrality table accordingly.

        Parameters:
            - pos (QPointF): Position to add the node.
        '''

        # Convert the cursor position to scene coordinates
        if isinstance(pos, QPointF):
            scene_pos = self.mapToScene(pos.toPoint())
        else:
            scene_pos = self.mapToScene(pos)

        # If not already in scene coordinates, transform the position
        if not self.main_window.graphic_view.transform().isIdentity():
            if isinstance(pos, QPoint):
                scene_pos = self.main_window.graphic_view.mapToScene(pos)
            else:
                scene_pos = self.main_window.graphic_view.mapToScene(pos.toPoint())

        if not node_list:
            new_node = Node(0, scene_pos.x(), scene_pos.y(), self.edges, color)
        else:
            new_node = Node(node_list[-1].key + 1, scene_pos.x(), scene_pos.y(), self.edges, color)
        node_list.append(new_node)

        new_node.setZValue(2)
        self.scene.addItem(new_node)

        # Add text item for the number-key next to the node
        new_node.graphic_key.setZValue(2)
        self.scene.addItem(new_node.graphic_key)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)} | Custom Graph')
        self.main_window.saved = False

    def deleteNode(self, node):
        '''
        Delete a node and update the status bar and centrality table accordingly.

        Parameters:
            - node (Node): Node to delete.
        '''

        # Remove only the edges connected to the deleted node
        if node is not None:
            for edge in self.edges.copy():  # Use copy to avoid modifying the list during iteration
                if edge.node1 == node or edge.node2 == node:
                    self.scene.removeItem(edge)
                    self.edges.remove(edge)
                    if (edge.node1.key, edge.node2.key) in self.seen_edges:
                        self.seen_edges.remove((edge.node1.key, edge.node2.key))
                    elif not self.main_window.directed and (edge.node2.key, edge.node1.key) in self.seen_edges:
                        self.seen_edges.remove((edge.node2.key, edge.node1.key))

        # Remove the node from the scene and the list of nodes
        self.scene.removeItem(node)
        self.scene.removeItem(node.graphic_key)

        # Remove the Node instance from node_list
        node_list.remove(node)

        # Clear the neighbors lists from the deleted node
        node.neighbors.clear()
        node.neighbors_in.clear()

        # Remove the deleted node from the neighbor sets of other nodes
        for other_node in node_list:
            if node in other_node.neighbors.keys():
                other_node.neighbors.pop(node)
            if node in other_node.neighbors_in.keys():
                other_node.neighbors_in.pop(node)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)} | Custom Graph')
        self.main_window.saved = False

        self.recalculate()

    def startAddingLink(self, node):
        '''
        Starts adding a link between 2 nodes. Sets the source node and waits for the second one to be clicked.

        Parameters:
             - node (Node): First of the 2 nodes to add a link.
        '''

        # Set the current node for linking
        self.source_node = node

    def sceneMousePressEvent(self, pos):
        '''
        Selects the second node to add a link and updates the status bar and centrality table accordingly.
        
        Parameters:
            pos pos (QPointF): Position of the destination.
        '''
        destination_node = self.scene.itemAt(pos.x(), pos.y(), self.transform())

        if isinstance(destination_node, Node) and destination_node != self.source_node:
            bidirectional = 0
            if not self.main_window.directed:
                if tuple(sorted((self.source_node.key, destination_node.key))) in self.seen_edges:
                    QMessageBox.warning(self, 'Invalid Input', f'Link {self.source_node.key, destination_node.key} already exists.')
                    return
                else:
                    self.seen_edges.add(tuple(sorted((self.source_node.key, destination_node.key))))
            else:
                if (self.source_node.key, destination_node.key) in self.seen_edges:
                    QMessageBox.warning(self, 'Invalid Input', f'Link {self.source_node.key, destination_node.key} already exists.')
                    return
                else:
                    self.seen_edges.add((self.source_node.key, destination_node.key))
                for edge in self.edges:
                    if edge.node1 == destination_node and edge.node2 == self.source_node:
                        bidirectional = 2
                        break

            weight_input = None

            if self.main_window.weighted:
                dialog = WeightDialog()
                weight_input = dialog.get_user_input()
                if not weight_input:
                    return

            # If the link added creates a bidirectional path between the 2 nodes redraw the other link between them.
            if bidirectional:
                for edge in self.edges.copy():
                    if edge.node1 == destination_node and edge.node2 == self.source_node:
                        edge.updateBidirectional(1)

            self.source_node.neighbors[destination_node] = weight_input
            if not self.main_window.directed:
                destination_node.neighbors[self.source_node] = weight_input
            else:
                destination_node.neighbors_in[self.source_node] = weight_input

            new_edge = Edge(self.source_node, destination_node, weight_input, self.main_window.directed, bidirectional)
            new_edge.setZValue(1)

            self.edges.append(new_edge)
            self.scene.addItem(new_edge)

            self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)} | Custom Graph')
            self.main_window.saved = False

            self.recalculate()

    def mousePressEvent(self, event):
        '''
        Event handler of the mousePressEvent. If there is a source node has already been selected to add a link connect
        the second node.

        Parameters:
             - event (QMouseEvent)
        '''
        if self.source_node is not None:
            scene_pos = self.mapToScene(event.pos())

            if not self.main_window.graphic_view.transform().isIdentity():
                scene_pos = self.main_window.graphic_view.mapToScene(event.pos())

            self.sceneMousePressEvent(scene_pos)
            self.source_node = None
        else:
            super().mousePressEvent(event)

    def clearAll(self):
        '''
        Delete all nodes and edges of the graph and update the status bar and centrality table accordingly.

        Returns:
            - 0: If user chose Cancel option in the dialog that pops up.
        '''
        from fileIO import save_dialog
        if not self.main_window.saved and not save_dialog(self.main_window, 0):
            return 0

        self.scene.clear()
        self.edges = []
        self.seen_edges.clear()

        # Reset the neighbor sets of all nodes
        for node in node_list:
            node.neighbors.clear()
            node.neighbors_in.clear()

        node_list.clear()

        self.main_window.side_label.setText('')
        self.main_window.side_table.update_table({}, 'Node')
        self.main_window.dock_widget.setHidden(True)

        self.main_window.statusBar().showMessage(f'Nodes: {len(node_list)} | Edges: {len(self.edges)}')
