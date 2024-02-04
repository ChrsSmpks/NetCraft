import networkx as nx
import numpy as np
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QFileDialog
from networkx import fruchterman_reingold_layout

from netGenerationDialog import NetworkGenerationDialog
from nodeObject import node_list
from fileIO import save_graph, load_graph
from spanningEdgeBetweenness import spanEdgeBetw


def create_main_menu(window):
    # Create main menu
    main_menu = window.menuBar()

    # Create submenus
    file_menu = create_file_menu(main_menu, window)
    centralities_menu = create_centralities_menu(main_menu, window)

    # Add submenus
    main_menu.addMenu(file_menu)
    main_menu.addMenu(centralities_menu)

    # Styling
    # main_menu.setStyleSheet(menu_style)

    return main_menu


def create_file_menu(main_menu, window):
    # Create File submenu
    file_submenu = QMenu('File', main_menu)

    # Create actions for the File submenu
    generate_action = QAction('Generate Network', file_submenu)
    open_action = QAction('Open Network', file_submenu)
    save_action = QAction('Save Network', file_submenu)
    exit_action = QAction('Exit', file_submenu)

    # Connect the created actions
    generate_action.triggered.connect(lambda: generate_net(window))
    open_action.triggered.connect(lambda: open_net(window))
    save_action.triggered.connect(lambda: save_net(window))
    exit_action.triggered.connect(lambda: exit_app(window))

    # Add the actions to File submenu
    file_submenu.addAction(generate_action)
    file_submenu.addAction(open_action)
    file_submenu.addAction(save_action)
    file_submenu.addAction(exit_action)

    return file_submenu


def create_centralities_menu(main_menu, window):
    # Create Centralities submenu
    centralities_submenu = QMenu('Centralities', main_menu)

    # Create actions for Centralities submenu
    spanning_edge_btw = QAction('Spanning Edge Betweenness', centralities_submenu)

    # Connect the created actions
    spanning_edge_btw.triggered.connect(lambda: spanEdgeBetw(window, node_list))

    # Add the actions to Centralities submenu
    centralities_submenu.addAction(spanning_edge_btw)

    return centralities_submenu


def generate_net(window):
    dialog = NetworkGenerationDialog()
    user_input = dialog.get_user_input()

    if user_input:
        nodes = user_input['nodes']
        density = user_input['density']

        # Clear existing nodes and edges
        if not window.graphic_view.clearAll() and node_list:
            return

        # Generate Erdős-Rényi graph
        erdos_renyi_graph = nx.erdos_renyi_graph(nodes, density)

        # Get Fruchterman-Reingold layout
        layout = fruchterman_reingold_layout(erdos_renyi_graph, scale=500)

        # Adjust layout coordinates to be positive
        min_x = min(layout.values(), key=lambda x: x[0])[0]
        min_y = min(layout.values(), key=lambda x: x[1])[1]

        if min_x < 0 or min_y < 0:
            # Shift all nodes to make coordinates non-negative
            for node in layout:
                layout[node] = (layout[node][0] - min_x, layout[node][1] - min_y)

        # Add nodes to GraphicView using Fruchterman-Reingold layout positions
        for node, pos in layout.items():
            window.graphic_view.addNode(QPointF(pos[0], pos[1]))

        # Add edges to the network
        for edge in erdos_renyi_graph.edges:
            node1 = node_list[edge[0]]
            node2 = node_list[edge[1]]
            window.graphic_view.addLink(node1, node2)

        window.statusBar().showMessage(f'Nodes: {erdos_renyi_graph.number_of_nodes()} | Edges: {erdos_renyi_graph.number_of_edges()}')

        # Update the view
        #window.graphic_view.fitInView(window.graphic_view.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        window.graphic_view.updateView()


def open_net(window):
    options = QFileDialog.Option.ReadOnly
    open_path, _ = QFileDialog.getOpenFileName(window, "Open Graph File", "", "JSON Files (*.json);;All Files (*)",
                                               options=options)

    if open_path:
        load_graph(window.graphic_view, open_path)  # Adjust based on your project structure


def save_net(window):
    save_path, _ = QFileDialog.getSaveFileName(window, "Save Graph File", "", "JSON Files (*.json);;All Files (*)")

    if save_path:
        save_graph(window, save_path)  # Adjust based on your project structure


def exit_app(window):
    window.close()
