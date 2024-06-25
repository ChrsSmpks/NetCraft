import numpy as np


def get_eigen(graph_edges, node_list):
    '''# Compute the Degree Matrix (D)
    D = np.diag(np.sum(A, axis=1))

    # Compute the Transition Matrix (P)
    P = np.divide(A, np.sum(A, axis=1)[:, np.newaxis], where=np.sum(A, axis=1)[:, np.newaxis] != 0)'''

    # Initialize the Adjacency Matrix
    node_num = len(node_list)
    A = np.zeros((node_num, node_num), dtype=float)

    # Populate the Adjacency Matrix
    for edge in graph_edges:
        # Given that edge.node1 and edge.node2 are Node instances
        index1 = node_list.index(edge.node1)
        index2 = node_list.index(edge.node2)

        # Set the corresponding entries in the adjacency matrix to 1
        if not edge.weight:
            A[index1, index2] = 1.0
            A[index2, index1] = 1.0
        else:
            A[index1, index2] = edge.weight
            A[index2, index1] = edge.weight

    # Create the Degree matrix of the graph
    D = np.diag(np.sum(A, axis=1))
    D = np.dot(D, 0.5/len(graph_edges))

    # Compute the square root of the degree matrix (D^(1/2))
    D_sqrt = np.sqrt(D)

    # Compute the inverse of the square root of the degree matrix (D^(-1/2))
    try:
        D_sqrt_inv = np.linalg.inv(D_sqrt)
    except np.linalg.LinAlgError:
        # If the matrix is singular, use the pseudoinverse
        D_sqrt_inv = np.linalg.pinv(D_sqrt)

    # Compute the Transition Matrix (P)
    P = np.divide(A, np.sum(np.abs(A), axis=1, keepdims=True))

    # Compute D^(1/2) * P * D^(-1/2)
    L_norm = np.matmul(np.matmul(D_sqrt, P), D_sqrt_inv)

    # Compute Eigenvalues and Eigenvectors of D^(1/2) * P * D^(-1/2)
    eigenvalues, eigenvectors = np.linalg.eig(L_norm)

    eigenvalues = np.real(eigenvalues)
    eigenvectors = np.real(eigenvectors)

    # Sort eigenvalues and eigenvectors by absolute value of eigenvalues in descending order
    idx = np.argsort(np.abs(eigenvalues))[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Take the top `omega` eigenvalues and eigenvectors
    if node_num > 128:
        eigenvalues = eigenvalues[:128]
        eigenvectors = eigenvectors[:, :128]

    # Transform the eigenvectors
    eigenvectors = D_sqrt_inv.dot(eigenvectors).T

    # Convert eigenvalues and eigenvectors to list format
    eigenvalues = eigenvalues.tolist()
    eigenvectors = eigenvectors.tolist()

    # Create a list of (eigenvalue, eigenvector) pairs
    #eigens = list(zip(eigenvalues, eigenvectors))
    eigens = sorted(zip(eigenvalues, eigenvectors), key=lambda x: abs(x[0]))
    """for eigen in eigens:
        print(type(eigen))
        print(eigen)"""

    return eigens


def get_delta(eigens, t, omega, node_list, node1, node2, m):
    Delta_t = 0
    for k in range(1, omega - 1):
        eigenvalue = eigens[k][0]
        f = eigens[k][1]
        idx1 = node_list.index(node1)
        idx2 = node_list.index(node2)
        Delta_t += ((f[idx1] - f[idx2]) ** 2) * (eigenvalue ** (t + 1)) / (1 - eigenvalue)

    return Delta_t / (2 * m)


def get_upsilon(eigens, omega, node_list, node1, node2, m):
    Y = 0
    for k in range(1, omega - 1):
        eigenvalue = eigens[k][0]
        f = eigens[k][1]
        idx1 = node_list.index(node1)
        idx2 = node_list.index(node2)
        Y += ((f[idx1] - f[idx2]) ** 2) * (1 + eigenvalue)

    return Y / (2 * m)


def get_tau(lamba, deg1, deg2, Y, Delta_t, epsilon):
    #print(f'deg1={deg1}, deg2={deg2}, lamba={lamba}, Y={Y}, Delta_t={Delta_t}, epsilon={epsilon}')
    a1 = 1 / deg1 + 1 / deg2 - 2 / (deg1 * deg2) - Y
    #a2 = max(epsilon - Delta_t, epsilon)
    a2 = epsilon - Delta_t
    #a3 = max(1 - (lamba ** 2), 1.0)
    a3 = 1 - (lamba ** 2)
    #a = np.log(max(np.abs(a1 / (a2 * a3)), 1.0))
    a = np.log(a1 / a2 / a3)
    if np.isnan(a):
        a = 0
    b = np.log(1 / np.abs(lamba))
    #print(f'a1 = {a1} a2={a2} a3={a3} a= {a}, b={b}')
    if not b:
        b = 1.0
    tau_ij = max(round(abs(a / b - 1)), 1)
    #print(f'tau_ij={tau_ij}')

    return int(tau_ij + 1) if tau_ij % 2 == 0 else int(tau_ij)


def calTau(graph_edges, node_list, node1, node2, epsilon, eigens, weighted):
    m = len(graph_edges)
    omega = len(eigens[0][1]) if len(eigens[0][1]) < 128 else 128
    lamba = eigens[1][0]

    # Calculate original tau_ij
    if not weighted:
        deg1 = len(node1.neighbors.keys())
        deg2 = len(node2.neighbors.keys())
    else:
        deg1 = sum(node1.neighbors.values())
        deg2 = sum(node2.neighbors.values())

    tau_ij = get_tau(lamba, deg1, deg2, 0, 0, epsilon)

    Y = get_upsilon(eigens, omega, node_list, node1, node2, m)
    #lamba = eigens[omega - 2][0]
    t = 1
    while True:
        #print('t=', t)
        Delta_t = get_delta(eigens, t, omega, node_list, node1, node2, m)
        new_tau_ij = get_tau(lamba, deg1, deg2, Y, Delta_t, epsilon)
        #print(f'new tau={new_tau_ij}, Dt={Delta_t}')

        # Check if tau_ij is less than or equal to t
        if t <= new_tau_ij and tau_ij < new_tau_ij: #  < tau_ij
            tau_ij = new_tau_ij
            t += 2
        else:
            break

    #print(f'final tau={tau_ij}')
    return tau_ij


def maxCalTau(graph_edges, node_list, node, epsilon, eigens, weighted):
    max_tau = 1

    # Iterate over the neighboring nodes of the current node
    for neighbor in node.neighbors.keys():
        tau_ij = calTau(graph_edges, node_list, node, neighbor, epsilon, eigens, weighted)

        # Update tau_p if tau_ij is greater
        if tau_ij > max_tau:
            max_tau = tau_ij
        """# Find the edge that connects the current node and its neighbor
        for edge in graph_edges:
            if (edge.node1 == node and edge.node2 == neighbor) or (edge.node1 == node and edge.node2 == node):
                # Calculate tau_ij for the current edge
                # tau_ij = calTau(graph_edges, edge, epsilon, eigenvalues, feature_vectors, node_list)
                tau_ij = calTau(graph_edges, node_list, edge, epsilon, eigens, weighted)

                # Update tau_p if tau_ij is greater
                if tau_ij > max_tau:
                    max_tau = tau_ij"""

    #print('max_tau=', max_tau)
    return max_tau


def tgt(window, node_list):
    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, False, 'TGT', False):
        return

    import timeit
    start = timeit.default_timer()
    #eigenvalues, feature_vectors = get_eigen(window.graphic_view.edges, node_list)
    eigens = get_eigen(window.graphic_view.edges, node_list)

    #epsilon = 1e-4
    #epsilon = 0.05
    epsilon = 0.1

    node_num = len(node_list)
    gt = np.zeros((node_num, node_num), dtype=float)

    for node in node_list:
        # tp = maxCalTau(node, window.graphic_view.edges, epsilon, eigenvalues, feature_vectors, node_list)
        tp = maxCalTau(window.graphic_view.edges, node_list, node, epsilon, eigens, bool(window.weighted))

        deg_src = len(node.neighbors.keys()) if not window.weighted else sum(node.neighbors.values())
        for neighbor in node.neighbors.keys():
            gt[node_list.index(node), node_list.index(neighbor)] = 1 / deg_src

        # Initialize transition probability matrices
        p = [np.zeros((node_num, node_num), dtype=float) for _ in range(tp)]

        # Initialize P[0]
        src_idx = node_list.index(node)
        p[0][src_idx, src_idx] = 1

        for l in range(0, tp):
            # Compute transition probabilities for hop level l
            for j in range(node_num):
                p[l][j, node_list.index(node)] = 0  # Set all off-diagonal elements to 0

            for other_node in node_list:
                if p[l - 1][node_list.index(other_node), node_list.index(node)] > 0:
                    for neighbor in other_node.neighbors.keys():
                        deg = len(neighbor.neighbors.keys()) if not window.weighted else sum(
                            neighbor.neighbors.values())
                        p[l][node_list.index(neighbor), node_list.index(node)] += p[l-1][node_list.index(
                            other_node), node_list.index(node)] / deg

            for neighbor in node.neighbors.keys():
                gt[node_list.index(node), node_list.index(neighbor)] += p[l][src_idx, src_idx] / deg_src - p[l][
                                                                            node_list.index(neighbor), src_idx] / deg_src
        #print('DID NODE', node.key)

    st = {}
    for edge in window.graphic_view.edges:
        st[tuple(sorted((edge.node1.key, edge.node2.key)))] = round(
            gt[node_list.index(edge.node1), node_list.index(edge.node2)] + gt[
                node_list.index(edge.node2), node_list.index(edge.node1)], 4)

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    window.side_table.update_table(st, 'Edge')
    window.side_label.setText('Algorithm: TGT')
    window.dock_widget.setHidden(False)
