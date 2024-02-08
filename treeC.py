import numpy as np

from spanningEdgeBetweenness import get_laplacian_matrix


def edge_incidence_matrix(graph_edges, node_list):
    '''
    Creates the Edge Incidence matrix, matrix of size m x n such that each row corresponds to an edge and each column
    to a node of the graph.

    Parameters:
         - graph_edges (list of EdgeObject): The edges of the graph
         - node_list (list of NodeObject): The nodes of the graph

    Returns:
        - B (numpy.ndarray): Edge Incidence matrix of the graph
    '''

    n = len(node_list)
    m = len(graph_edges)

    # Create the edge-incidence matrix B
    B = np.zeros((m, n))

    for i, edge in enumerate(graph_edges):
        u, v = edge.node1.key, edge.node2.key
        B[i, u] = -1
        B[i, v] = 1

    return B


def treeC(window, node_list):
    '''
    Calculates the Spanning Edge Betweenness centrality for every edge by using the TreeC algorithm

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of NodeObject): The nodes of the graph

    TreeC Algorithm:
        - Construct the Laplacian matrix of the graph
        - Construct random {0, +-1/sqrt(k)} projection matrix Q of size k x m where k = O(log n) , m: number of graph edges
        - Construct the Edge Incidence matrix B and compute the matrix Y = QB
        - for i ... k do
            Approximate zi by solving Lzi = Y(i, :)
            Append zi as a row to matrix Z
        - Calculate for each edge e = {u, v} R(e) = ||Z(:,u) - Z(:,v)||_2^2 which is equivalent to the
          spanning betweenness centrality of the edge e
    '''

    # Initialize matrices and Laplacian matrix
    Z = np.empty((0, len(node_list)))
    laplacian_matrix = get_laplacian_matrix(window.graphic_view.edges, node_list)

    # Construct edge incidence matrix B
    B = edge_incidence_matrix(window.graphic_view.edges, node_list)

    # Construct random projection matrix Q
    k = int(np.ceil(np.log2(len(node_list))))  # k = O(log n)
    m = len(window.graphic_view.edges)
    Q = np.random.choice([-1/np.sqrt(k), 0, 1/np.sqrt(k)], size=(k, m))

    # Compute Y = QB
    Y = np.dot(Q, B)

    # Approximate zi by solving Lzi = Y[:, i]
    for i in range(k):
        try:
            zi = np.linalg.solve(laplacian_matrix, Y[i, :])
        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                # If matrix is singular use a least squares solution
                zi = np.linalg.lstsq(laplacian_matrix, Y[i, :], rcond=None)[0]
            else:
                print('Error:', e)
        Z = np.vstack((Z, zi))

    # Compute and return R(e)
    # R = np.zeros(m)
    R = {}
    for i, edge in enumerate(window.graphic_view.edges):
        u, v = edge.node1.key, edge.node2.key

        R[f'({u},{v})'] = round(np.linalg.norm(Z[:, u] - Z[:, v])**2, 4)

    window.side_table.update_table(R)
    window.side_label.setText('Algorithm: TreeC')
    window.dock_widget.setHidden(False)
