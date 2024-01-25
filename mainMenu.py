import math
import random

import networkx as nx
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QMenu, QGraphicsLineItem
from networkx import fruchterman_reingold_layout
from shapely.geometry import Point
from random import uniform


from edgeObject import EdgeObject
from netGenerationDialog import NetworkGenerationDialog
from nodeObject import NodeObject
from node import node_list


def create_main_menu(window):
    # Create main menu
    main_menu = window.menuBar()

    # Create submenus
    file_menu = create_file_menu(main_menu, window)
    centralities_menu = create_centralities_menu(main_menu)

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

    # Add the actions to File submenu
    file_submenu.addAction(generate_action)
    file_submenu.addAction(open_action)
    file_submenu.addAction(save_action)
    file_submenu.addAction(exit_action)

    return file_submenu


def create_centralities_menu(main_menu):
    # Create Centralities submenu
    centralities_submenu = QMenu('Centralities', main_menu)

    return centralities_submenu


def generate_net(window):
    dialog = NetworkGenerationDialog()
    user_input = dialog.get_user_input()

    if user_input:
        nodes = user_input['nodes']
        density = user_input['density']
        min_distance = 40

        # Clear existing nodes and edges
        window.graphic_view.clearAll()

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

        '''NEW'''
        # Add nodes to GraphicView using Fruchterman-Reingold layout positions
        for node, pos in layout.items():
            print('main', 'node', node)
            print(pos[0], pos[1])
            window.graphic_view.addNode(QPointF(pos[0], pos[1]))

        print('node keys')
        for node in node_list:
            print(node.key)

        # Add edges to the network
        for edge in erdos_renyi_graph.edges:
            print(type(edge[0]))
            node1 = node_list[edge[0]]
            node2 = node_list[edge[1]]
            window.graphic_view.addLink(node1, node2)

        print('im getting triggered')
        window.statusBar().showMessage(f'Nodes: {erdos_renyi_graph.number_of_nodes()} | Edges: {erdos_renyi_graph.number_of_edges()}')
        '''for edge in erdos_renyi_graph.edges:
            print(type(edge[0]))
            node1 = window.graphic_view.nodes_map[edge[0]]
            node2 = window.graphic_view.nodes_map[edge[1]]
            window.graphic_view.addLink(node1, node2)'''
        '''new'''

        # scene_rect = window.graphic_view.sceneRect()
        """# Get the bounds of the scene
        scene_rect = window.graphic_view.sceneRect()

        # Generate random positions for node positions with minimum distance constraint
        max_attempts = 100  # Set a reasonable maximum number of attempts

        node_positions = []
        for _ in range(nodes):
            for _ in range(max_attempts):
                random_pos = QPointF(uniform(scene_rect.left(), scene_rect.right()),
                                     uniform(scene_rect.top(), scene_rect.bottom()))

                distances = [math.hypot(pos.x() - random_pos.x(), pos.y() - random_pos.y()) for pos in node_positions]

                if all(distance >= min_distance for distance in distances):
                    node_positions.append(random_pos)
                    break
            else:
                # If the inner loop completes without a valid position, handle it here
                print("Unable to find a valid position after multiple attempts.")

        # available_scene_area = scene_rect.width() * scene_rect.height()

        # Add nodes to GraphicView
        for node, pos in zip(erdos_renyi_graph.nodes, node_positions):
            window.graphic_view.addNode(pos)

        # Add edges based on density
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                if random.random() < density:
                    window.graphic_view.addLink(node_list[i], node_list[j])"""

        # Update the view
        #window.graphic_view.fitInView(window.graphic_view.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        window.graphic_view.updateView()
