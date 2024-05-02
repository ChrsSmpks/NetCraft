import networkx as nx
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QFileDialog
from networkx import fruchterman_reingold_layout

from Algorithms.StandardCentralities.edgeBetweenness import edgeBetweenness
from Algorithms.StandardCentralities.betweenness import betweenness
from Algorithms.StandardCentralities.closeness import closeness
from Algorithms.SpanningCentralities.spanningEdgeBetweenness import spanEdgeBetw, spanEdgeBetwWeighted
from Algorithms.StandardCentralities.degreeCentrality import degreeCentrality
from Algorithms.SpanningCentralities.treeC import treeC
from Algorithms.SpanningCentralities.fastTreeC import fastTreeC
from Algorithms.SpanningCentralities.tgt import tgt
from netGenerationDialog import NetworkGenerationDialog
from propertiesDialog import PropertiesDialog
from DataStructures.node import node_list
from fileIO import save_graph, load_graph
from style_sheets import menu_style


def create_main_menu(window):
    '''
    Creates the main menu of the app which includes File and Centralities submenus

    Parameters:
        - window (QMainWindow): The main window of the app

    Returns:
        - main_menu (QMenuBar): The created menu of the app
    '''

    # Create main menu
    main_menu = window.menuBar()

    # Create submenus
    file_menu = create_file_menu(main_menu, window)
    standard_centralities_menu = create_standard_cenrtalities_menu(main_menu, window)
    spanning_centralities_menu = create_spanning_centralities_menu(main_menu, window)
    options_menu = create_options_menu(main_menu, window)

    # Add submenus
    main_menu.addMenu(file_menu)
    main_menu.addMenu(standard_centralities_menu)
    main_menu.addMenu(spanning_centralities_menu)
    main_menu.addMenu(options_menu)
    main_menu.addAction(QAction('Hello'))

    # Styling
    main_menu.setStyleSheet(menu_style)

    return main_menu


def create_file_menu(main_menu, window):
    '''
    Creates the file submenu containing Generate Network, Open Network, Save Network, Exit actions

    Parameters:
        - window (QMainWindow): The main window of the app
        - main_menu (QMenuBar): The created menu of the app

    Returns:
        - file_submenu (QMenu): The created File menu
    '''

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
    file_submenu.addSeparator()
    file_submenu.addAction(open_action)
    file_submenu.addAction(save_action)
    file_submenu.addSeparator()
    file_submenu.addAction(exit_action)

    return file_submenu


def create_standard_cenrtalities_menu(main_menu, window):
    # Create Centralities submenu
    centralities_submenu = QMenu('Standard-Centralities', main_menu)

    # Create actions for Centralities submenu
    deg = QAction('Degree', centralities_submenu)
    edge_btw = QAction('Edge Betweenness', centralities_submenu)
    btw = QAction('Betweenness', centralities_submenu)
    clos = QAction('Closeness', centralities_submenu)

    # Connect the created actions
    deg.triggered.connect(lambda: degreeCentrality(window, node_list, window.weighted))
    edge_btw.triggered.connect(lambda: edgeBetweenness(window, node_list))
    btw.triggered.connect(lambda: betweenness(window, node_list))
    clos.triggered.connect(lambda: closeness(window, node_list))

    # Add the actions to Centralities submenu
    centralities_submenu.addAction(deg)
    centralities_submenu.addAction(edge_btw)
    centralities_submenu.addAction(btw)
    centralities_submenu.addAction(clos)

    return centralities_submenu


def create_spanning_centralities_menu(main_menu, window):
    '''
    Creates the centralities submenu containing Spanning Edge Betweenness, TreeC, Fast-TreeC algorithms

    Parameters:
        - window (QMainWindow): The main window of the app
        - main_menu (QMenuBar): The created menu of the app

    Returns:
        - centralities_submenu (QMenu): The created File menu
    '''

    # Create Centralities submenu
    centralities_submenu = QMenu('Spanning-Centralities', main_menu)

    # Create actions for Centralities submenu
    spanning_edge_btw = QAction('Spanning Edge Betweenness', centralities_submenu)
    treec = QAction('TreeC', centralities_submenu)
    fastTree = QAction('Fast-TreeC', centralities_submenu)
    _tgt = QAction('TGT', centralities_submenu)

    # Connect the created actions
    spanning_edge_btw.triggered.connect(lambda: connect_spanning_edge_btw(window, node_list))
    treec.triggered.connect(lambda: treeC(window, node_list))
    fastTree.triggered.connect(lambda: fastTreeC(window, node_list))
    _tgt.triggered.connect(lambda: tgt(window, node_list))

    # Add the actions to Centralities submenu
    centralities_submenu.addAction(spanning_edge_btw)
    centralities_submenu.addAction(treec)
    centralities_submenu.addAction(fastTree)
    centralities_submenu.addAction(_tgt)

    return centralities_submenu


def connect_spanning_edge_btw(window, node_list):
    if not window.weighted:
        spanEdgeBetw(window, node_list)
    else:
        spanEdgeBetwWeighted(window, node_list)


def create_options_menu(main_menu, window):
    # Create Properties submenu
    options_menu = QMenu('Options', main_menu)

    # Create properties action
    options_act = QAction('Options...', main_menu)
    options_act.triggered.connect(lambda: options_action(window))

    # Add action
    options_menu.addAction(options_act)

    return options_menu


def options_action(window):
    properties_dialog = PropertiesDialog(window)
    properties_dialog.exec()


def generate_net(window):
    '''
    Generates a random Erdos - Renyi graph in a Fruchterman_Reingold based on the user input of number of nodes and density

    Parameters:
        - window (QMainWindow): The main window of the app
    '''

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
                layout[node] = (layout[node][0] - min_x + 12, layout[node][1] - min_y + 12)

        # Add nodes to GraphicView using Fruchterman-Reingold layout positions
        for node, pos in layout.items():
            window.graphic_view.addNode(QPointF(pos[0], pos[1]), window.node_color)

        # Add edges to the network
        for edge in erdos_renyi_graph.edges:
            node1 = node_list[edge[0]]
            node2 = node_list[edge[1]]
            window.graphic_view.addLink(node1, node2)

        for node in node_list:
            if not node.neighbors.keys():
                import random
                while True:
                    rnd_node_idx = random.randint(0, len(node_list)-1)
                    if node != node_list[rnd_node_idx]:
                        break
                window.graphic_view.addLink(node, node_list[rnd_node_idx])

        window.weighted = False
        window.statusBar().showMessage(f'Nodes: {erdos_renyi_graph.number_of_nodes()} | Edges: {erdos_renyi_graph.number_of_edges()} | Random Erdos - Renyi Graph')

        # Update the view
        window.graphic_view.updateView()


def open_net(window):
    '''
    Creates a QFileDialog to browse the file system and select the json file where network info is stored.
    Then calls load_graph to generate the graph saved in the specified json file

    Parameters:
        - window (QMainWindow): The main window of the app
    '''

    options = QFileDialog.Option.ReadOnly
    open_path, _ = QFileDialog.getOpenFileName(window, "Open Graph File", "", "JSON Files (*.json);;Text Files (*.txt)",
                                               options=options)

    if open_path:
        if not window.graphic_view.clearAll() and node_list:
            return
        load_graph(window, open_path)  # Adjust based on your project structure


def save_net(window):
    '''
    Creates a QFileDialog to browse the file system and select save location for the json file.
    Then calls save_graph to save the graph saved in the specified json file

    Parameters:
        - window (QMainWindow): The main window of the app
    '''

    save_path, _ = QFileDialog.getSaveFileName(window, "Save Graph File", "", "JSON Files (*.json);;Text Files (*.txt)")

    if save_path:
        # Determine file format based on file extension
        file_format = 'json' if save_path.endswith('.json') else 'txt'

        save_graph(window, save_path, file_format)  # Adjust based on your project structure


def exit_app(window):
    window.close()
