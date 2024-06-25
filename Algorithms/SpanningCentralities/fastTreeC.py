import numpy as np
import os
import psutil
from scipy.sparse import spdiags
from scipy.sparse.linalg import gmres
import concurrent.futures
from functools import partial
from joblib import Parallel, delayed

from .spanningEdgeBetweenness import get_laplacian_matrix
from .treeC import edge_incidence_matrix


def compute_resistance_for_iteration(i, B, L, node_list, edges, k, preconditioned_A, preconditioner_mat):
    # Construct a random vector q
    q = np.random.choice([-1 / np.sqrt(k), 0, 1 / np.sqrt(k)], size=(1, len(edges)))

    # Compute y = qB
    y = np.dot(q, B)

    # Approximate z by solving Lz = y
    try:
        preconditioned_b = preconditioner_mat.dot(y.T)
        z, _ = gmres(preconditioned_A, preconditioned_b)
    except np.linalg.LinAlgError as e:
        if 'Singular matrix' in str(e):
            # If matrix is singular use a least squares solution
            z = np.linalg.lstsq(L, y.T, rcond=None)[0]
        else:
            print('Error:', e)
            return {}

    # Initialize resistance distances for this iteration
    R_iter = {}

    # Update resistance distances for each edge
    for edge in edges:
        key1, key2 = edge[0], edge[1]
        u, v = node_list.index(edge[0]), node_list.index(edge[1])

        # Update resistance for the edge
        if (key1, key2) not in R_iter:
            R_iter[tuple(sorted((key1, key2)))] = 0

        R_iter[tuple(sorted((key1, key2)))] += np.linalg.norm(z[u] - z[v]) ** 2

    return R_iter


def merge_resistances(R, R_iter):
    for edge, resistance in R_iter.items():
        if edge not in R:
            R[edge] = 0
        R[edge] += resistance


def fastTreeC(window, node_list):
    '''
    Calculates the Spanning Edge Betweenness centrality for every edge by using the Fast-TreeC algorithm

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of Node): The nodes of the graph

    Fast-TreeC Algorithm:
        - Construct the Laplacian matrix of the graph
        - Construct the Edge Incidence matrix B and compute the matrix Y = QB
        - for i ... k do
            Construct a random {0, +-1/sqrt(k)} projection vector q of size 1 x m
            Compute y = qB
            Approximate z by solving Lz = y
            Compute R(e) = R(e) + ||z(u) - z(v)||_2^2, R(e) is equivalent to the spanning betweenness centrality of the edge e
    '''

    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, False, 'Fast-TreeC', False):
        return

    edges = []
    for edge in window.graphic_view.edges:
        edges.append([edge.node1.key, edge.node2.key])

    nodes = []
    for node in node_list:
        nodes.append(node.key)
    print('converted edges, nodes')

    import timeit
    start = timeit.default_timer()

    # Construct the Edge Incidence matrix
    B = edge_incidence_matrix(window.graphic_view.edges, node_list)

    # Compute Laplacian matrix L
    if not window.weighted:
        L = get_laplacian_matrix(window.graphic_view.edges, node_list)
    else:
        m = len(window.graphic_view.edges)
        W = np.zeros((m, m))

        for i, edge in enumerate(window.graphic_view.edges):
            W[i, i] = edge.weight if edge.weight is not None else 1

        B_T = np.transpose(B)
        L = np.dot(B_T, np.dot(W, B))

    # Jacobi (Diagonal) Preconditioner
    preconditioner = spdiags(1.0 / L.diagonal(), [0], L.shape[0], L.shape[1])

    # Compute the preconditioner
    preconditioner_mat = preconditioner.toarray()

    # Modify the linear system with preconditioning
    preconditioned_A = preconditioner_mat.dot(L)
    #print('did precondition A')

    # Number of nodes and edges in the graph
    n = len(node_list)
    m = len(window.graphic_view.edges)

    # Initialize resistance distances
    R = {}

    # Iterate over k dimensions
    k = int(np.ceil(np.log2(n)))  # k = O(log n)
    process = psutil.Process(os.getpid())
    #print(f"Memory usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
    func = partial(compute_resistance_for_iteration, B=B, L=L, node_list=nodes,
                   edges=edges,
                   k=k, preconditioned_A=preconditioned_A, preconditioner_mat=preconditioner_mat)
    results = Parallel(n_jobs=4)(delayed(func)(i) for i in range(k))
    #print(f"Memory usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
    """with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        func = partial(compute_resistance_for_iteration, B=B, L=L, node_list=nodes,
                       edges=edges,
                       k=k, preconditioned_A=preconditioned_A, preconditioner_mat=preconditioner_mat)
        results = list(executor.map(func, range(k)))
        print(f"Memory usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")"""
    """try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            func = partial(compute_resistance_for_iteration, B=B, L=L, node_list=nodes,
                           edges=edges,
                           k=k, preconditioned_A=preconditioned_A, preconditioner_mat=preconditioner_mat)
            results = list(executor.map(func, range(k)))
            print(f"Memory usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
    except Exception as e:
        print(f"An error occurred: {str(e)}")"""

    # Merge results from all iterations
    for R_iter in results:
        merge_resistances(R, R_iter)

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    for edge in R:
        R[edge] = round(R[edge], 4)

    window.side_table.update_table(R, 'Edge')
    window.side_label.setText('Algorithm: Fast-TreeC')
    window.dock_widget.setHidden(False)
