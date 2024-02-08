from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QMessageBox

from nodeObject import node_list

import json


def save_graph(window, save_path):
    '''
    Saves the graph in a json format
    json contains nodes: a list in which every element represents a node and stores its key and its x, y coordinates
    and edges: a list in which every element represents an edge in the form [node1_key, node2_key]

    Parameters:
        - window (QMainWindow): The main window of the app
        - save_path (str): The path to save the json file
    '''
    nodes_data = [{'key': node.key, 'x': node.x(), 'y': node.y()} for node in node_list]

    edges_data = [[node_list.index(edge.node1), node_list.index(edge.node2)] for edge in window.graphic_view.edges]

    graph_data = {'nodes': nodes_data, 'edges': edges_data}

    with open(save_path, 'w') as json_file:
        json.dump(graph_data, json_file, indent=2)


def load_graph(graphic_view, open_path):
    '''
    Loads the graph from the specified json file
    json contains nodes: a list in which every element represents a node and stores its key and its x, y coordinates
    and edges: a list in which every element represents an edge in the form [node1_key, node2_key]

    Parameters:
        - graphic_view (QGraphicsView): The graphic view of the window where the graph is displayed
        - open_path (str): The path where the json file is stored

    Returns:
        - node_list (list of NodeObject): The nodes of the graph
    '''

    try:
        with open(open_path, 'r') as json_file:
            graph_data = json.load(json_file)

        nodes_data = graph_data.get('nodes', [])
        edges_data = graph_data.get('edges', [])

        # Create nodes
        for node in nodes_data:
            graphic_view.addNode(QPointF(node['x'], node['y']))

        # Create edges
        for edge_data in edges_data:
            if len(edge_data) == 2:
                node1 = node_list[edge_data[0]]
                node2 = node_list[edge_data[1]]
                graphic_view.addLink(node1, node2)

        return node_list

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading graph from {open_path}: {e}")
        return None


def save_dialog(window, close):
    '''
    Creates a QMessageBox with options to Save, Discard, Cancel changes with the following triggers:
    Close the app, Generate another graph, Open another graph, clear all visual elements

    Parameters:
        - window (QMainWindow): The main window of the app
        - close (int): 1 will close the app after the save, 0 won't

    Returns:
        - 0 (int): If the user clicked Cancel
        - 1 (int): Otherwise
    '''

    if node_list:
        reply = QMessageBox.question(window, 'Save Changes', 'Do you want to save changes before exiting?',
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Save:
            # Save the graph
            from mainMenu import save_net
            save_net(window)
            if close:
                window.close()
        elif reply == QMessageBox.StandardButton.Discard:
            # Discard changes, proceed with exit
            if close:
                window.close()
        else:
            # Cancel, do nothing
            return 0

        return 1
