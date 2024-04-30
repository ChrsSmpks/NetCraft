from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QMessageBox

from DataStructures.node import node_list

import json


def save_graph(window, save_path, file_format):
    '''
    Saves the graph in either JSON or TXT format
    json contains nodes: a list in which every element represents a node and stores its key and its x, y coordinates
    and edges: a list in which every element represents an edge in the form [node1_key, node2_key]

    Parameters:
        - window (QMainWindow): The main window of the app
        - save_path (str): The path to save the json file
        - file_format (str): The format to save the file in ('json' or 'txt')
    '''
    if file_format == 'json':
        nodes_data = [{'key': node.key, 'x': node.x(), 'y': node.y(), 'color': node.color} for node in node_list]
        edges_data = [[node_list.index(edge.node1), node_list.index(edge.node2), edge.weight] for edge in window.graphic_view.edges]

        graph_data = {'nodes': nodes_data, 'edges': edges_data}

        with open(save_path, 'w') as json_file:
            json.dump(graph_data, json_file, indent=2)
    elif file_format == 'txt':
        with open(save_path, 'w') as txt_file:
            txt_file.write("Nodes:\n")
            for node in node_list:
                txt_file.write(f"{node.key} {node.x()} {node.y()} {node.color}\n")

            txt_file.write("\nEdges:\n")
            for edge in window.graphic_view.edges:
                txt_file.write(f"{node_list.index(edge.node1)} {node_list.index(edge.node2)} {edge.weight}\n")

    window.saved = True


def load_graph(window, open_path):
    '''
    Loads the graph from the specified json file
    json contains nodes: a list in which every element represents a node and stores its key and its x, y coordinates
    and edges: a list in which every element represents an edge in the form [node1_key, node2_key]

    Parameters:
        - window (QMainWindow): The main window of the app
        - open_path (str): The path where the json file is stored

    Returns:
        - node_list (list of Node): The nodes of the graph
    '''

    try:
        if open_path.endswith('.json'):
            with open(open_path, 'r') as json_file:
                graph_data = json.load(json_file)
        elif open_path.endswith('.txt'):
            with open(open_path, 'r') as file:
                graph_data = {'nodes': [], 'edges': []}
                mode = None
                for line in file:
                    line = line.strip()
                    if line == 'Nodes:':
                        mode = 'nodes'
                    elif line == 'Edges:':
                        mode = 'edges'
                    elif mode == 'nodes' and line != '':
                        values = line.split()
                        graph_data['nodes'].append({'key': int(values[0]), 'x': float(values[1]), 'y': float(values[2]), 'color': values[3]})
                    elif mode == 'edges':
                        values = line.split()
                        # node1_key, node2_key = map(int, line.split())
                        graph_data['edges'].append([int(values[0]), int(values[1]), float(values[2]) if values[2] != 'None' else None])

        nodes_data = graph_data.get('nodes', [])
        edges_data = graph_data.get('edges', [])

        # Create nodes
        for node in nodes_data:
            window.graphic_view.addNode(pos=QPointF(node['x'], node['y']), color=node['color'])

        # Create edges
        for edge_data in edges_data:
            if len(edge_data) == 3:
                node1 = node_list[edge_data[0]]
                node2 = node_list[edge_data[1]]
                weight = edge_data[2]
                window.graphic_view.addLink(node1, node2, weight)

        window.saved = True
        window.weighted = bool(edges_data[0][2])

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
