import math
import random

import networkx as nx
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QMenu, QGraphicsLineItem
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
    file_submenu = QMenu('FIle', main_menu)

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
        '''# Here, you can use user_input['nodes'] and user_input['density']
        # to generate the network as per the user's specifications.
        print(f"Number of Nodes: {user_input['nodes']}")
        print(f"Network Density: {user_input['density']}")'''
        nodes = user_input['nodes']
        density = user_input['density']
        min_distance = 40

        '''# Generate Erdős-Rényi graph
        erdos_renyi_graph = nx.erdos_renyi_graph(nodes, density)
        pos = nx.spring_layout(erdos_renyi_graph)  # You can use other layout algorithms

        # Clear the existing scene and add nodes and edges to it
        window.graphic_view.scene.clear()'''

        # Clear existing nodes and edges
        window.graphic_view.clearAll()

        # Generate Erdős-Rényi graph
        erdos_renyi_graph = nx.erdos_renyi_graph(nodes, density)

        # Get the bounds of the scene
        scene_rect = window.graphic_view.sceneRect()

        # Generate random positions for node positions with minimum distance constraint
        '''i = 0
        node_positions = []
        for _ in range(nodes):
            while True:
                random_pos = QPointF(uniform(scene_rect.left(), scene_rect.right()),
                                     uniform(scene_rect.top(), scene_rect.bottom()))
                distances = [math.hypot(pos.x() - random_pos.x(), pos.y() - random_pos.y()) for pos in node_positions]
                if all(distance >= min_distance for distance in distances):
                    node_positions.append(random_pos)
                    break'''
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
            '''estimated_size = math.sqrt(available_scene_area / nodes)

            # Ensure a minimum size to avoid very small nodes
            min_size = 10
            estimated_size = int(max(estimated_size, min_size))

            # Resize the node pixmap based on the estimated size
            original_pixmap = new_node_object.pixmap()
            resized_pixmap = original_pixmap.scaledToWidth(estimated_size)

            new_node_object.setPixmap(resized_pixmap)'''

        # Add edges based on density
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                if random.random() < density:
                    window.graphic_view.addLink(node_list[i], node_list[j])

        # Add nodes to the GraphicView scene
        for node in erdos_renyi_graph.nodes:
            pass
            '''new_node = NodeObject(erdos_renyi_graph.nodes[node]['pos'][0],
                                  erdos_renyi_graph.nodes[node]['pos'][1],
                                  "NodeIcons\\node11.png", window.graphic_view.edges)'''
            """new_node = NodeObject(pos[node][0], pos[node][1], "NodeIcons\\node11.png", window.graphic_view.edges)
            window.graphic_view.nodes.append(new_node)
            window.graphic_view.scene.addItem(new_node)"""
            """# Generate a random position within the scene
            random_pos = QPointF(random.uniform(0, window.graphic_view.sceneRect().width()),
                                 random.uniform(0, window.graphic_view.sceneRect().height()))"""

            """# Generate a random position within the scene, ensuring minimum distance
            random_pos = None
            while random_pos is None or any(random_pos.toPoint().manhattanLength() < min_distance
                                            for node_pos in window.graphic_view.nodes_map.values()):
                random_pos = QPointF(random.uniform(0, window.graphic_view.sceneRect().width()),
                                     random.uniform(0, window.graphic_view.sceneRect().height()))

            # Call addNode to add both logical and visual representations
            window.graphic_view.addNode(random_pos)"""

        # Add edges to the GraphicView scene
        for edge in erdos_renyi_graph.edges:
            pass
            '''start_node = erdos_renyi_graph.nodes[edge[0]]['pos']
            end_node = erdos_renyi_graph.nodes[edge[1]]['pos']'''
            """start_node = pos[edge[0]]
            end_node = pos[edge[1]]
            new_edge = EdgeObject(window.graphic_view.nodes[edge[0]], window.graphic_view.nodes[edge[1]])
            window.graphic_view.edges.append(new_edge)
            window.graphic_view.scene.addItem(new_edge)"""
            """node1 = window.graphic_view.nodes[edge[0]]
            node2 = window.graphic_view.nodes[edge[1]]
            new_edge = EdgeObject(node1, node2)
            window.graphic_view.edges.append(new_edge)
            window.graphic_view.scene.addItem(new_edge)"""

        # Update the view
        window.graphic_view.fitInView(window.graphic_view.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        window.graphic_view.updateView()

        """# Adjust the view to fit the new scene
        window.graphic_view.fitInView(window.graphic_view.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        window.graphic_view.update()"""

        '''for node in erdos_renyi_graph.nodes:
            # Create a QGraphicsEllipseItem for each node
            item = QGraphicsEllipseItem(-10, -10, 20, 20)  # Adjust dimensions as needed
            item.setPos(QPointF(*erdos_renyi_graph.nodes[node]['pos']))
            window.graphic_view.scene.addItem(item)

        for edge in erdos_renyi_graph.edges:
            # Create a QGraphicsLineItem for each edge
            start_node = erdos_renyi_graph.nodes[edge[0]]['pos']
            end_node = erdos_renyi_graph.nodes[edge[1]]['pos']
            line_item = QGraphicsLineItem(start_node[0], start_node[1], end_node[0], end_node[1])
            window.graphic_view.scene.addItem(line_item)

            # Adjust the view to fit the new scene
        window.graphic_view.fitInView(window.graphic_view.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        window.graphic_view.update()'''


'''def update_scene_with_graph(graph):
    # Assuming you have a method to visualize the graph in your existing code
    # For example, you might clear the existing scene and add nodes and edges to it
    self.scene.clear()

    for node in graph.nodes:
        # Create a QGraphicsEllipseItem for each node
        item = QGraphicsEllipseItem(-10, -10, 20, 20)  # Adjust dimensions as needed
        item.setPos(QPointF(*graph.nodes[node]['pos']))
        self.scene.addItem(item)

    for edge in graph.edges:
        # Create a QGraphicsLineItem for each edge
        start_node = graph.nodes[edge[0]]['pos']
        end_node = graph.nodes[edge[1]]['pos']
        line_item = QGraphicsLineItem(start_node[0], start_node[1], end_node[0], end_node[1])
        self.scene.addItem(line_item)

    # Adjust the view to fit the new scene
    self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    self.update()'''
