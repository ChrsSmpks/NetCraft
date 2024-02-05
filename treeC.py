import numpy as np

from spanningEdgeBetweenness import get_laplacian_matrix


def edge_incidence_matrix(graph_edges, node_list):
    n = len(node_list)
    m = len(graph_edges)

    # Create the edge-incidence matrix B
    B = np.zeros((m, n))

    for i, edge in enumerate(graph_edges):
        u, v = edge.node1.key, edge.node2.key
        B[i, u] = -1
        B[i, v] = 1
        # print(f'({u},{v})')

    return B


def treeC(window, node_list):
    # Initialize matrices and Laplacian matrix
    Z = np.empty((0, len(node_list)))
    laplacian_matrix = get_laplacian_matrix(window.graphic_view.edges, node_list)
    print(laplacian_matrix)
    print()

    # Construct edge incidence matrix B
    B = edge_incidence_matrix(window.graphic_view.edges, node_list)
    '''print(B)
    print()'''

    # Construct random projection matrix Q
    k = int(np.ceil(np.log2(len(node_list))))  # k = O(log n)
    m = len(window.graphic_view.edges)
    Q = np.random.choice([-1/np.sqrt(k), 0, 1/np.sqrt(k)], size=(k, m))
    '''print(Q)
    print()'''

    # Compute Y = QB
    Y = np.dot(Q, B)
    '''print(Y)
    print()'''

    #print(Y[:, i])

    # Approximate zi by solving Lzi = Y[:, i]
    for i in range(k):
        # print(Y[i, :])
        zi = np.linalg.solve(laplacian_matrix, Y[i, :])
        Z = np.vstack((Z, zi))
        '''if i == 0 or i == 1:
            print('line', i)
            print(zi)'''
    '''print()
    print(type(Z))
    print(Z)'''

    # Compute and return R(e)
    # R = np.zeros(m)
    R = {}
    for i, edge in enumerate(window.graphic_view.edges):
        u, v = edge.node1.key, edge.node2.key
        # R[i] = np.linalg.norm(Z[:, u] - Z[:, v])**2
        R[f'({u},{v})'] = round(np.linalg.norm(Z[:, u] - Z[:, v])**2, 4)

    print()
    print(R)
