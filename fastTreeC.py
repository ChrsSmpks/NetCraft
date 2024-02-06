import numpy as np

from spanningEdgeBetweenness import get_laplacian_matrix
from treeC import edge_incidence_matrix


def fastTreeC(window, node_list):
    # Compute Laplacian matrix L
    L = get_laplacian_matrix(window.graphic_view.edges, node_list)

    # Number of nodes and edges in the graph
    n = len(node_list)
    m = len(window.graphic_view.edges)

    # Initialize resistance distances
    R = {}

    # Iterate over k dimensions
    k = int(np.ceil(np.log2(len(node_list))))  # k = O(log n)
    for i in range(k):
        # Construct a random vector q
        q = np.random.choice([-1/np.sqrt(k), 0, 1/np.sqrt(k)], size=(1, m))

        # Compute y = qB
        B = edge_incidence_matrix(window.graphic_view.edges, node_list)
        y = np.dot(q, B)

        # Approximate z by solving Lz = y
        try:
            z = np.linalg.solve(L, y.T)
        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                # If matrix is singular use a least squares solution
                z = np.linalg.lstsq(L, y.T, rcond=None)[0]
            else:
                print('Error:', e)

        # Update resistance distances for each edge
        for edge in window.graphic_view.edges:
            u, v = edge.node1.key, edge.node2.key

            # If the edge is not in the dictionary add it
            if f'({u},{v})' not in R:
                R[f'({u},{v})'] = 0

            # Update resistance for the edge
            R[f'({u},{v})'] += np.linalg.norm(z[u] - z[v])**2

    for edge in R:
        R[edge] = round(R[edge], 4)

    # print(R)
    window.side_table.update_table(R)
    window.side_label.setText('Algorithm: Fast-TreeC')
    window.dock_widget.setHidden(False)
