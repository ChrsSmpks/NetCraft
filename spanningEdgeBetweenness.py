# Input: list of EdgeObjects of the graph
import numpy as np


def get_laplacian_matrix(graph_edges, node_list):
    # Initialize the Adjacency Matrix
    node_num = len(node_list)
    adj_matrix = np.zeros((node_num, node_num), dtype=int)

    # Populate the Adjacency Matrix
    for edge in graph_edges:
        # Given that edge.node1 and edge.node2 are NodeObject instances
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
    # Find max absolute value in the matrix
    max_abs_value = np.max(np.abs(matrix))

    # Set a threshold to prevent division by very small numbers
    threshold = 1e-12

    # Calculate the scaling factor
    scale_factor = 1.0 / max(max_abs_value, threshold)

    # Normalize the matrix
    normalized_matrix = matrix * scale_factor

    return normalized_matrix


def spanEdgeBetw(window, node_list):
    laplacian_matrix = get_laplacian_matrix(window.graphic_view.edges, node_list)
    print(laplacian_matrix)

    # cofactor = round(float(np.linalg.det(laplacian_matrix[1:, 1:])), 4)
    cofactor = np.linalg.det(laplacian_matrix[1:, 1:])
    print('cofactor:', cofactor)
    if np.isinf(cofactor):
        laplacian_matrix = normalize_matrix(laplacian_matrix)

        cofactor = np.linalg.det(laplacian_matrix[1:, 1:])
        print('new cofactor:', cofactor)

    # Initialize a dictionary to store results for each edge
    spanning_betweenness_for_edges = {}

    for edge in window.graphic_view.edges:
        i, j = edge.node1.key, edge.node2.key

        laplacian_ij = np.delete(laplacian_matrix, [i, j], axis=0)
        laplacian_ij = np.delete(laplacian_ij, [i, j], axis=1)

        # Number of spanning trees containing the edge
        # trees_for_edges = round(float(np.linalg.det(laplacian_ij)), 4)
        trees_for_edges = np.linalg.det(laplacian_ij)
        # print('tress for', f'{edge.node1.key}-{edge.node2.key}', trees_for_edges)
        if edge.node1.key == 0 and edge.node2.key == 1:
            print('tress for', f'{edge.node1.key}-{edge.node2.key}', trees_for_edges)

        # Store the result for the edge
        spanning_betweenness_for_edges[f'({edge.node1.key},{edge.node2.key})'] = round(trees_for_edges / cofactor, 4)

    print(spanning_betweenness_for_edges)
