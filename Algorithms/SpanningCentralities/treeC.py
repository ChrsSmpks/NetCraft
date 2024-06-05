import numpy as np
from scipy.sparse import spdiags

from .spanningEdgeBetweenness import get_laplacian_matrix


def edge_incidence_matrix(graph_edges, node_list):
    '''
    Creates the Edge Incidence matrix, matrix of size m x n such that each row corresponds to an edge and each column
    to a node of the graph.

    Parameters:
         - graph_edges (list of Edge): The edges of the graph
         - node_list (list of Node): The nodes of the graph

    Returns:
        - B (numpy.ndarray): Edge Incidence matrix of the graph
    '''

    n = len(node_list)
    m = len(graph_edges)

    # Create the edge-incidence matrix B
    B = np.zeros((m, n))

    for i, edge in enumerate(graph_edges):
        # u, v = edge.node1.key, edge.node2.key
        u, v = node_list.index(edge.node1), node_list.index(edge.node2)
        B[i, u] = -1
        B[i, v] = 1

    return B


def treeC(window, node_list):
    '''
    Calculates the Spanning Edge Betweenness centrality for every edge by using the TreeC algorithm

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of Node): The nodes of the graph

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

    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, False, 'TreeC', False):
        return

    import timeit
    start = timeit.default_timer()

    # Initialize matrices
    Z = np.empty((0, len(node_list)))

    # Construct edge incidence matrix B
    B = edge_incidence_matrix(window.graphic_view.edges, node_list)

    # Initialize Laplacian matrix
    if not window.weighted:
        laplacian_matrix = get_laplacian_matrix(window.graphic_view.edges, node_list)
    else:
        m = len(window.graphic_view.edges)
        W = np.zeros((m, m))

        for i, edge in enumerate(window.graphic_view.edges):
            W[i, i] = edge.weight if edge.weight is not None else 1

        B_T = np.transpose(B)
        laplacian_matrix = np.dot(B_T, np.dot(W, B))

    # Construct random projection matrix Q
    k = int(np.ceil(np.log2(len(node_list))))  # k = O(log n)
    m = len(window.graphic_view.edges)
    Q = np.random.choice([-1 / np.sqrt(k), 0, 1 / np.sqrt(k)], size=(k, m))

    # Compute Y = QB
    Y = np.dot(Q, B)
    from scipy.sparse.linalg import gmres

    # Jacobi (Diagonal) Preconditioner
    preconditioner = spdiags(1.0 / laplacian_matrix.diagonal(), [0], laplacian_matrix.shape[0],
                             laplacian_matrix.shape[1])

    # Compute the preconditioner
    preconditioner_mat = preconditioner.toarray()

    # Modify the linear system with preconditioning
    preconditioned_A = preconditioner_mat.dot(laplacian_matrix)

    # Approximate zi by solving Lzi = Y[i, :]
    for i in range(k):
        try:
            preconditioned_b = preconditioner_mat.dot(Y[i, :])

            zi, _ = gmres(preconditioned_A, preconditioned_b)
            #zi = np.linalg.solve(laplacian_matrix, Y[i, :])
            #print(f'did z{i}')
        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                # If matrix is singular use a least squares solution
                zi = np.linalg.lstsq(laplacian_matrix, Y[i, :], rcond=None)[0]
            else:
                print('Error:', e)
        Z = np.vstack((Z, zi))

    # Compute and return R(e)
    R = {}
    for i, edge in enumerate(window.graphic_view.edges):
        key1, key2 = edge.node1.key, edge.node2.key
        u, v = node_list.index(edge.node1), node_list.index(edge.node2)

        R[tuple(sorted((key1, key2)))] = round(np.linalg.norm(Z[:, u] - Z[:, v]) ** 2, 4)

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    window.side_table.update_table(R, 'Edge')
    window.side_label.setText('Algorithm: TreeC')
    window.dock_widget.setHidden(False)
