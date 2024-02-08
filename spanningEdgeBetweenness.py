import numpy as np


def get_laplacian_matrix(graph_edges, node_list):
    '''
    Creates the Laplacian matrix of the graph by subtracting Adjacency matrix from Degree matrix

    Parameters:
         - graph_edges (list of EdgeObject): The edges of the graph
         - node_list (list of NodeObject): The nodes of the graph

    Returns:
        - laplacian_matrix (numpy.ndarray): The Laplacian matrix of the graph
    '''

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


def spanEdgeBetw(window, node_list):
    '''
    Calculates the Spanning Edge Betweenness centrality for every edge

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of NodeObject): The nodes of the graph

    Algorithm:
        - Calculate the Laplacian matrix of the graph and a cofactor of it
        - According to Kirchhoff's Matrix Tree Theorem the number of MSTs of the graph equals to det of the cofactor of
          Laplacian matrix
        - The number of MSTs containing edge = {u, v} equals the det of Lij which is the laplacian matrix by deleting
          rows u and v and columns u and v
        - The spanning betweenness for each edge equals to MSTs containing the edge / total MSTs
    '''
    laplacian_matrix = get_laplacian_matrix(window.graphic_view.edges, node_list)

    cofactor = np.linalg.det(laplacian_matrix[1:, 1:])

    if np.isinf(cofactor):
        laplacian_matrix = normalize_matrix(laplacian_matrix)

        cofactor = np.linalg.det(laplacian_matrix[1:, 1:])

    # Initialize a dictionary to store results for each edge
    spanning_betweenness_for_edges = {}

    for edge in window.graphic_view.edges:
        i, j = edge.node1.key, edge.node2.key

        laplacian_ij = np.delete(laplacian_matrix, [i, j], axis=0)
        laplacian_ij = np.delete(laplacian_ij, [i, j], axis=1)

        # Number of spanning trees containing the edge
        trees_for_edges = np.linalg.det(laplacian_ij)

        # Store the result for the edge
        spanning_betweenness_for_edges[f'({edge.node1.key},{edge.node2.key})'] = round(trees_for_edges / cofactor, 4)

    window.side_table.update_table(spanning_betweenness_for_edges)
    window.side_label.setText('Algorithm: Spanning Edge Betweenness')
    window.dock_widget.setHidden(False)
