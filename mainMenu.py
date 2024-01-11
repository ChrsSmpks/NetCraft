import networkx as nx
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QGraphicsLineItem

from edgeObject import EdgeObject
from netGenerationDialog import NetworkGenerationDialog
from nodeObject import NodeObject


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

        # Generate Erdős-Rényi graph
        erdos_renyi_graph = nx.erdos_renyi_graph(nodes, density)
        pos = nx.spring_layout(erdos_renyi_graph)  # You can use other layout algorithms

        # Clear the existing scene and add nodes and edges to it
        window.graphic_view.scene.clear()

        # Add nodes to the GraphicView scene
        for node in erdos_renyi_graph.nodes:
            '''new_node = NodeObject(erdos_renyi_graph.nodes[node]['pos'][0],
                                  erdos_renyi_graph.nodes[node]['pos'][1],
                                  "NodeIcons\\node11.png", window.graphic_view.edges)'''
            new_node = NodeObject(pos[node][0], pos[node][1], "NodeIcons\\node11.png", window.graphic_view.edges)
            window.graphic_view.nodes.append(new_node)
            window.graphic_view.scene.addItem(new_node)

        # Add edges to the GraphicView scene
        for edge in erdos_renyi_graph.edges:
            '''start_node = erdos_renyi_graph.nodes[edge[0]]['pos']
            end_node = erdos_renyi_graph.nodes[edge[1]]['pos']'''
            start_node = pos[edge[0]]
            end_node = pos[edge[1]]
            new_edge = EdgeObject(window.graphic_view.nodes[edge[0]], window.graphic_view.nodes[edge[1]])
            window.graphic_view.edges.append(new_edge)
            window.graphic_view.scene.addItem(new_edge)

        # Adjust the view to fit the new scene
        window.graphic_view.fitInView(window.graphic_view.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        window.graphic_view.update()

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
