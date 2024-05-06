import math
from collections import defaultdict
from itertools import groupby

import numpy as np
from PyQt6.QtWidgets import QMessageBox


def get_laplacian_matrix(graph_edges, node_list):
    '''
    Creates the Laplacian matrix of the graph by subtracting Adjacency matrix from Degree matrix

    Parameters:
         - graph_edges (list of Edge): The edges of the graph
         - node_list (list of Node): The nodes of the graph

    Returns:
        - laplacian_matrix (numpy.ndarray): The Laplacian matrix of the graph
    '''

    # Initialize the Adjacency Matrix
    node_num = len(node_list)
    adj_matrix = np.zeros((node_num, node_num), dtype=int)

    # Populate the Adjacency Matrix
    for edge in graph_edges:
        # Given that edge.node1 and edge.node2 are Node instances
        index1 = node_list.index(edge.node1)
        index2 = node_list.index(edge.node2)

        # Set the corresponding entries in the adjacency matrix to 1
        adj_matrix[index1, index2] = 1
        adj_matrix[index2, index1] = 1

    # Create the Degree matrix of the graph
    degree_matrix = np.diag(np.sum(adj_matrix, axis=1))

    # Create the Laplacian matrix by subtracting Adjacency matrix from Degree matrix
    laplacian_matrix = degree_matrix - adj_matrix

    return laplacian_matrix


def normalize_matrix(matrix):
    '''
    Normalizes the (Laplacian) matrix to scale down matrices with inf elements

    Parameters:
        - matrix (numpy.ndarray): The matrix to normalize

    Returns:
        - normalized_matrix (numpy.ndarray): The normalized matrix
    '''
    # Find max absolute value in the matrix
    max_abs_value = np.max(np.abs(matrix))

    # Set a threshold to prevent division by very small numbers
    threshold = 1e-12

    # Calculate the scaling factor
    scale_factor = 1.0 / max(max_abs_value, threshold)

    # Normalize the matrix
    normalized_matrix = matrix * scale_factor

    return normalized_matrix


def msts_num(edges, nodes):
    '''
    Computes the number of MSTs of the graph consisting of the edges,nodes as the det of the cofactor of the Laplacian
    matrix of the graph as described in Kirchhoff's Matrix Tree Theorem.

    Parameters:
        - edges (list of Edge): The edges of the graph.
        - nodes (list of Node): The nodes of the graph.

    Returns:
         - msts (int): The number of MSTs in the graph.
         - laplacian_matrix (numpy.ndarray): The Laplacian matrix of the graph.
    '''
    laplacian_matrix = get_laplacian_matrix(edges, nodes)

    msts = np.linalg.det(laplacian_matrix[1:, 1:])

    if np.isinf(msts):
        laplacian_matrix = normalize_matrix(laplacian_matrix)

        msts = np.linalg.det(laplacian_matrix[1:, 1:])

    return msts, laplacian_matrix


def edge_msts_and_centrality(nodes, edges, laplacian_matrix, msts, spanning_betweenness_for_edges):
    for edge in edges:
        i, j = nodes.index(edge.node1), nodes.index(edge.node2)

        laplacian_ij = np.delete(laplacian_matrix, [i, j], axis=0)
        laplacian_ij = np.delete(laplacian_ij, [i, j], axis=1)

        # Number of spanning trees containing the edge
        trees_for_edges = np.linalg.det(laplacian_ij)

        # Store the result for the edge - Equation 1
        spanning_betweenness_for_edges[tuple(sorted((edge.node1.key, edge.node2.key)))] = round(trees_for_edges / msts,
                                                                                                4)


def spanEdgeBetw(window, node_list):
    '''
    Calculates the Spanning Edge Betweenness centrality for every edge

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of Node): The nodes of the graph

    Algorithm:
        - Calculate the Laplacian matrix of the graph and a cofactor of it
        - According to Kirchhoff's Matrix Tree Theorem the number of MSTs of the graph equals to det of the cofactor of
          Laplacian matrix
        - The number of MSTs containing edge = {u, v} equals the det of Lij which is the laplacian matrix by deleting
          rows u and v and columns u and v
        - The spanning betweenness for each edge equals to MSTs containing the edge / total MSTs
    '''

    if not node_list:
        return
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'}, 'Edge')
        window.dock_widget.setHidden(False)
        return
    for node in node_list:
        if not node.neighbors:
            msg = QMessageBox(QMessageBox.Icon.Warning, 'Error', 'Centralities cannot be computed because the graph '
                                                                 'lacks connectivity.', QMessageBox.StandardButton.Ok)
            msg.exec()
            return

    """laplacian_matrix = get_laplacian_matrix(window.graphic_view.edges, node_list)

    cofactor = np.linalg.det(laplacian_matrix[1:, 1:])

    if np.isinf(cofactor):
        laplacian_matrix = normalize_matrix(laplacian_matrix)

        cofactor = np.linalg.det(laplacian_matrix[1:, 1:])"""

    msts, laplacian_matrix = msts_num(window.graphic_view.edges, node_list)

    # Initialize a dictionary to store results for each edge
    spanning_betweenness_for_edges = {}

    edge_msts_and_centrality(node_list, window.graphic_view.edges, laplacian_matrix, msts, spanning_betweenness_for_edges)

    """for edge in window.graphic_view.edges:
        i, j = node_list.index(edge.node1), node_list.index(edge.node2)

        laplacian_ij = np.delete(laplacian_matrix, [i, j], axis=0)
        laplacian_ij = np.delete(laplacian_ij, [i, j], axis=1)

        # Number of spanning trees containing the edge
        trees_for_edges = np.linalg.det(laplacian_ij)

        # Store the result for the edge
        spanning_betweenness_for_edges[tuple(sorted((edge.node1.key, edge.node2.key)))] = round(
            trees_for_edges / cofactor, 4)"""

    window.side_table.update_table(spanning_betweenness_for_edges, 'Edge')
    window.side_label.setText('Algorithm: Spanning Edge Betweenness')
    window.dock_widget.setHidden(False)


class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}

    def find(self, vertex):
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        self.parent[root_v] = root_u


def spanEdgeBetwWeighted(window, node_list):
    '''
    Calculates the Spanning Edge Betweenness centrality for every edge in a weighted graph.

    Parameters:
        - window (QMainWindow): The main window of the app.
        - node_list (list of Node): The nodes of the graph.

    Algorithm:
        - Sort graph edges with respect to their weight in increasing order.
        - Initialize an empty graph and add to it edges with the same weight and their respective verteces.
        - Find the connected components in the created graph.
        - For each connected component of the created graph compute the number of MSTs in the component:
            - Calculate the Laplacian matrix of the graph and a cofactor of it.
            - According to Kirchhoff's Matrix Tree Theorem the number of MSTs of the graph equals to det of the cofactor
              of Laplacian matrix.
        - For each edge in each connected component of the created graph compute the number of MSTs containing the edge
          in the component:
            - The number of MSTs containing edge = {u, v} equals the det of Lij which is the laplacian matrix by
              deleting rows u and v and columns u and v.
        - The spanning betweenness for each edge in each component equals to
          MSTs of the component containing the edge / total MSTs in the component.
          This is the spanning betweenness of the edge both with respect to the component and the original graph.
    '''
    edges = sorted(window.graphic_view.edges, key=lambda _edge: _edge.weight)  # Sort edges by weight
    vertices = node_list.copy()
    uf = UnionFind(vertices)
    # msts = []
    i = 0
    tg = 1
    spanning_betweenness_for_edges = {tuple(sorted((edge.node1.key, edge.node2.key))): 0.0 for edge in edges}

    while i < len(edges):
        # Find all edges with the same weight
        same_weight_edges = []
        j = i
        while j < len(edges) and edges[j].weight == edges[i].weight:
            same_weight_edges.append(edges[j])
            j += 1

        """for edge in same_weight_edges:
            print(f'weighted ({edge.node1.key}, {edge.node2.key})')"""

        # Find connected components in the graph formed by mst_edges
        connected_components = find_connected_components(same_weight_edges)

        """for component in connected_components:
            for edge in component:
                print(f'component edge ({edge.node1.key}, {edge.node2.key})', end=' ')
            print()"""

        for component in connected_components:
            comp_nodes = set()
            brk = False
            for edge in component:
                if uf.find(edge.node1) == uf.find(edge.node2):
                    brk = True
                    spanning_betweenness_for_edges[tuple(sorted((edge.node1.key, edge.node2.key)))] = float(0)
                    break
                comp_nodes.add(edge.node1)
                comp_nodes.add(edge.node2)
            if brk:
                continue
            comp_nodes = list(comp_nodes)
            """print('component nodes:', end=' ')
            for node in comp_nodes:
                print(node.key, end=' ')
            print()"""
            tc, laplacian_matrix = msts_num(component, comp_nodes)
            # print('tc:', tc)
            tg *= tc
            # laplacian_matrix = get_laplacian_matrix(component, comp_nodes)
            edge_msts_and_centrality(comp_nodes, component, laplacian_matrix, tc, spanning_betweenness_for_edges)

        mst_edges = []
        for edge in same_weight_edges:
            if uf.find(edge.node1) != uf.find(edge.node2):
                mst_edges.append(edge)
                uf.union(edge.node1, edge.node2)
                # print(f'added ({edge.node1.key}, {edge.node2.key})')
                # print(f'set parent of {edge.node1.key} to {uf.find(edge.node1).key}, {edge.node2.key} to {uf.find(edge.node2).key}')

        """bnodes = node_list.copy()
        print('bnodes')
        for node in bnodes:
            print(node.key, end=' ')
        for node in vertices:
            if same_weight_edges[0].weight == 42.0 and node.key == 8:
                print('parent of', node.key, ':', uf.find(node).key)
            if uf.find(node) != node:
                bnodes.remove(node)
                print('removed', node.key, end=' ')
            if node.key == 6 or node.key == 8:
                print('parent', node.key, ':', uf.find(node).key)
        if len(bnodes) == 1:
            break

        # Run Kruskal's algorithm for each set of edges with the same weight
        msts.append(mst_edges)
        print('msts:')
        for mst in msts:
            for edge in mst:
                print(f'({edge.node1.key}, {edge.node2.key})', end=' ')
            print()"""

        # Skip to the next set of edges with different weights
        i = j

    window.side_table.update_table(spanning_betweenness_for_edges, 'Edge')
    window.side_label.setText('Algorithm: Spanning Edge Betweenness')
    window.dock_widget.setHidden(False)


def find_connected_components(edges):
    '''
    Finds the connected components of a graph.

    Parameters:
         - edges (list of Edge): The edges of the graph.

    Returns:
        - components.values() (list of lists of Edge): Each sub-list in the list contains the edges of the connected
          component.
    '''
    vertices = []
    for edge in edges:
        vertices.append(edge.node1)
        vertices.append(edge.node2)
    uf = UnionFind(vertices)

    # Create a dictionary to store the components
    components = {}

    # Contract all nodes to one in each connected component
    for edge in edges:
        if uf.find(edge.node1) != uf.find(edge.node2):
            uf.union(edge.node1, edge.node2)

    # Populate edge_dict with edges belonging to each component
    for edge in edges:
        root = uf.find(edge.node1)
        if root not in components.keys():
            components[root] = []
        components[root].append(edge)

    return components.values()
