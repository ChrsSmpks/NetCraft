import numpy as np


def get_eigen(graph_edges, node_list):
    '''# Compute the Degree Matrix (D)
    D = np.diag(np.sum(A, axis=1))

    # Compute the Transition Matrix (P)
    P = np.divide(A, np.sum(A, axis=1)[:, np.newaxis], where=np.sum(A, axis=1)[:, np.newaxis] != 0)'''

    # Initialize the Adjacency Matrix
    node_num = len(node_list)
    A = np.zeros((node_num, node_num), dtype=int)

    # Populate the Adjacency Matrix
    for edge in graph_edges:
        # Given that edge.node1 and edge.node2 are NodeObject instances
        index1 = node_list.index(edge.node1)
        index2 = node_list.index(edge.node2)

        # Set the corresponding entries in the adjacency matrix to 1
        A[index1, index2] = 1
        A[index2, index1] = 1

    # Create the Degree matrix of the graph
    D = np.diag(np.sum(A, axis=1))

    # Compute the square root of the degree matrix (D^(1/2))
    D_sqrt = np.sqrt(D)

    # Compute the inverse of the square root of the degree matrix (D^(-1/2))
    D_sqrt_inv = np.linalg.inv(D_sqrt)

    # Compute the Transition Matrix (P)
    D_inv = np.diag(1 / np.diag(D))
    # P1 = np.divide(A, np.sum(A, axis=1)[:, np.newaxis], where=np.sum(A, axis=1)[:, np.newaxis] != 0)
    P = np.matmul(D_inv, A)

    # Compute D^(1/2) * P * D^(-1/2)
    L_norm = np.matmul(np.matmul(D_sqrt, P), D_sqrt_inv)

    # Compute Eigenvalues and Eigenvectors of D^(1/2) * P * D^(-1/2)
    eigenvalues, eigenvectors = np.linalg.eig(L_norm)

    # Take the absolute values of eigenvalues
    eigenvalues_abs = np.abs(eigenvalues)
    eigenvalues_abs[0] = 1

    # Normalize the eigenvectors
    normalized_eigenvectors = eigenvectors / np.linalg.norm(eigenvectors, axis=0)

    # Extract the first normalized eigenvector
    first_eigenvector = normalized_eigenvectors[0]

    # Adjust the first eigenvector to ensure the first eigenvalue is 1
    adjusted_first_eigenvector = first_eigenvector / np.linalg.norm(first_eigenvector)

    # Update the normalized eigenvectors with the adjusted first eigenvector
    normalized_eigenvectors[0] = adjusted_first_eigenvector

    # Sort Eigenvalues and Eigenvectors
    sorted_indices = np.argsort(eigenvalues_abs)[::-1]
    sorted_eigenvalues = eigenvalues_abs[sorted_indices]
    sorted_eigenvectors = eigenvectors[sorted_indices]

    # Compute f
    f = np.sqrt(2 * len(graph_edges)) * np.dot(D_sqrt_inv, sorted_eigenvectors)

    # Normalize the first eigenvector
    f[0] = 1

    return sorted_eigenvalues, f


def calTau(graph_edges, edge, epsilon, eigenvalues, feature_vectors, node_list):
    m = len(graph_edges)
    omega = len(feature_vectors)

    # Calculate original tau_ij
    deg1 = len(edge.node1.neighbors)
    deg2 = len(edge.node2.neighbors)

    a = np.log((1 / deg1 + 1 / deg2 - 2 / (deg1 * deg2)) / (epsilon * (1 - eigenvalues[2])))
    b = np.log(1 / np.abs(eigenvalues[2]))
    tau_ij = round(a / b - 1)

    # Calculate Y
    Y = 0
    for k in range(2, omega - 1):
        Y += ((feature_vectors[k][node_list.index(edge.node1)] - feature_vectors[k][node_list.index(edge.node2)]) ** 2) * (1 + eigenvalues[k])

    Y /= (2 * m)

    t = 1
    while True:
        # Calculate Delta_t
        Delta_t = 0
        for k in range(2, omega - 1):
            Delta_t += ((feature_vectors[k][node_list.index(edge.node1)] - feature_vectors[k][node_list.index(edge.node2)]) ** 2) * (
                        eigenvalues[k] ** (t + 1)) / (1 - eigenvalues[k])

        Delta_t /= (2 * m)

        # Calculate new tau
        a1 = 1 / deg1 + 1 / deg2 - 2 / (deg1 * deg2) - Y
        a2 = epsilon - Delta_t
        a3 = 1 - (eigenvalues[2] ** 2)
        # print('a1:', a1, 'a2:', a2, 'a3:', a3)
        a = np.log(np.abs(a1 / (a2 * a3)))
        # a = np.log((1 / deg1 + 1 / deg2 - 2 / (deg1 * deg2) - Y) / ((epsilon - Delta_t) * (1 - eigenvalues[2])))
        # print('a:', a)
        b = np.log(1 / np.abs(eigenvalues[2]))
        # print('b:', b)
        new_tau_ij = round(a / b - 1)

        # Check if tau_ij is less than or equal to t
        # if t <= tau_ij:
        if t <= new_tau_ij:
            tau_ij = new_tau_ij
            t += 2
        else:
            break

    return tau_ij


def maxCalTau(node, graph_edges, epsilon, eigenvalues, feature_vectors, node_list):
    tau_p = 1

    # Iterate over the neighboring nodes of the current node
    for neighbor in node.neighbors:
        # Find the edge that connects the current node and its neighbor
        for edge in graph_edges:
            if (edge.node1 == node and edge.node2 == neighbor) or (edge.node1 == node and edge.node2 == node):
                # Calculate tau_ij for the current edge
                tau_ij = calTau(graph_edges, edge, epsilon, eigenvalues, feature_vectors, node_list)

                # Update tau_p if tau_ij is greater
                if tau_ij > tau_p:
                    tau_p = tau_ij

    return tau_p


def tgt(window, node_list):
    if not node_list:
        return
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'})
        window.dock_widget.setHidden(False)
        return

    eigenvalues, feature_vectors = get_eigen(window.graphic_view.edges, node_list)

    epsilon = 1e-4
    node_num = len(node_list)
    gt = np.zeros((node_num, node_num), dtype=float)

    for node in node_list:
        tp = maxCalTau(node, window.graphic_view.edges, epsilon, eigenvalues, feature_vectors, node_list)

        # gt = np.zeros((node_num, node_num), dtype=float)
        for neighbor in node.neighbors:
            gt[node_list.index(node), node_list.index(neighbor)] = 1 / len(node.neighbors)

        # Initialize transition probability matrices
        p = [np.zeros((node_num, node_num), dtype=float) for _ in range(tp)]

        # Initialize P[0]
        for i in range(node_num):
            p[0][i, i] = 1  # Diagonal elements are set to 1
            for j in range(node_num):
                if i != j:
                    p[0][i, j] = 0  # Off-diagonal elements are set to 0

        for l in range(1, tp):
            # print('tp:', tp)
            # Compute transition probabilities for hop level l
            for j in range(node_num):
                p[l][j, node_list.index(node)] = 0  # Set all off-diagonal elements to 0

            for other_node in node_list:
                if p[l - 1][node_list.index(other_node), node_list.index(node)] > 0:
                    for neighbor in node.neighbors:
                        p[l][node_list.index(neighbor), node_list.index(node)] += p[l][node_list.index(other_node), node_list.index(node)] / len(neighbor.neighbors)

            for neighbor in node.neighbors:
                gt[node_list.index(node), node_list.index(neighbor)] += p[l][node_list.index(node), node_list.index(node)] / len(node.neighbors) - p[l][
                    node_list.index(neighbor), node_list.index(node)] / len(node.neighbors)

    st = {}
    for edge in window.graphic_view.edges:
        st[f'({edge.node1.key},{edge.node2.key})'] = round(gt[node_list.index(edge.node1), node_list.index(edge.node2)] + gt[
            node_list.index(edge.node2), node_list.index(edge.node1)], 4)

    window.side_table.update_table(st)
    window.side_label.setText('Algorithm: TGT')
    window.dock_widget.setHidden(False)
