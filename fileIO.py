from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QMessageBox

from nodeObject import node_list

import json


def save_graph(window, save_path):
    nodes_data = [{'key': node.key, 'x': node.x(), 'y': node.y()} for node in node_list]

    edges_data = [[node_list.index(edge.node1), node_list.index(edge.node2)] for edge in window.graphic_view.edges]

    graph_data = {'nodes': nodes_data, 'edges': edges_data}

    with open(save_path, 'w') as json_file:
        json.dump(graph_data, json_file, indent=2)


def load_graph(graphic_view, open_path):
    try:
        with open(open_path, 'r') as json_file:
            graph_data = json.load(json_file)

        nodes_data = graph_data.get('nodes', [])
        edges_data = graph_data.get('edges', [])

        # Create nodes
        # node_list = [NodeObject(node['key'], node['x'], node['y'], "NodeIcons\\node.png", graphic_view.edges) for node in nodes_data]
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
    if node_list:
        reply = QMessageBox.question(window, 'Save Changes', 'Do you want to save changes before exiting?',
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Save:
            # Save the graph
            from mainMenu import save_net
            save_net(window)
            if close:
                print('here 1')
                window.close()
        elif reply == QMessageBox.StandardButton.Discard:
            # Discard changes, proceed with exit
            if close:
                print('here 2')
                window.close()
        else:
            # User chose to cancel, do nothing
            return 0

        return 1
