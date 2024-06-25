import numpy as np
from scipy.linalg import det


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
    adj_matrix = np.zeros((node_num, node_num), dtype=float)
    print('laplacian for weight', graph_edges[0].weight)

    # Populate the Adjacency Matrix
    for edge in graph_edges:
        # Given that edge.node1 and edge.node2 are Node instances
        index1 = node_list.index(edge.node1)
        index2 = node_list.index(edge.node2)

        if not edge.weight:
            # Set the corresponding entries in the adjacency matrix to 1
            adj_matrix[index1, index2] = 1.0
            adj_matrix[index2, index1] = 1.0
        else:
            adj_matrix[index1, index2] = edge.weight
            adj_matrix[index2, index1] = edge.weight
            #print(f'edge weight {edge.weight}, adj_matrix[index1, index2]={adj_matrix[index1, index2]}, adj_matrix[index2, index1]={adj_matrix[index2, index1]}')

    try:
        # Create the Degree matrix of the graph
        degree_matrix = np.diag(np.sum(adj_matrix, axis=1))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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

    #msts = np.linalg.det(laplacian_matrix[1:, 1:])
    msts = det(laplacian_matrix[1:, 1:])
    print('msts =', msts)

    if np.isinf(msts):
        laplacian_matrix = normalize_matrix(laplacian_matrix)

        msts = det(laplacian_matrix[1:, 1:])

    return msts, laplacian_matrix


def edge_msts_and_centrality(nodes, edges, laplacian_matrix, msts, spanning_betweenness_for_edges):
    '''
    Computes the number of MSTs containing edge = {u, v} which equals the det of Lij which is the laplacian matrix by
    deleting rows u and v and columns u and v.
    Then computes the Spanning Edge Betweenness centrality for every edge and stores it in spanning_betweenness_for_edges

    Parameters:
        - nodes (list of Node): The nodes of the graph.
        - edges (list of Edge): The edges of the graph.
        - laplacian_matrix (numpy.ndarray): The Laplacian matrix of the graph.
        - msts (int): The number of MSTs in the graph.
        - spanning_betweenness_for_edges (dictionary): Spanning Edge Betweenness centrality for every edge.
    '''
    for edge in edges:
        i, j = nodes.index(edge.node1), nodes.index(edge.node2)

        """laplacian_ij = np.delete(laplacian_matrix, [i, j], axis=0)
        laplacian_ij = np.delete(laplacian_ij, [i, j], axis=1)"""
        laplacian_ij = laplacian_matrix[np.ix_(
            [k for k in range(len(laplacian_matrix)) if k != i and k != j],
            [k for k in range(len(laplacian_matrix)) if k != i and k != j]
        )]

        #print(f'calc edge {edge.node1.key, edge.node2.key}')
        # Number of spanning trees containing the edge
        #edge_msts = np.linalg.det(laplacian_ij)
        edge_msts = det(laplacian_ij)

        # Store the result for the edge
        spanning_betweenness_for_edges[tuple(sorted((edge.node1.key, edge.node2.key)))] = round(edge_msts / msts, 4)


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

    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, False, 'Spanning Edge Betweenness', False):
        return

    import timeit
    start = timeit.default_timer()

    msts, laplacian_matrix = msts_num(window.graphic_view.edges, node_list)
    print('got msts:', msts)

    # Initialize a dictionary to store results for each edge
    spanning_betweenness_for_edges = {}

    edge_msts_and_centrality(node_list, window.graphic_view.edges, laplacian_matrix, msts, spanning_betweenness_for_edges)

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    window.side_table.update_table(spanning_betweenness_for_edges, 'Edge')
    window.side_label.setText('Algorithm: Spanning Edge Betweenness')
    window.dock_widget.setHidden(False)


class UnionFind:
    def __init__(self, vertices):
        """
        Initializes the UnionFind data structure with a dictionary mapping each vertex to itself.

        Parameters:
            - vertices (list of Node): A list of vertices.
        """
        self.parent = {v: v for v in vertices}

    def find(self, vertex):
        """
        Finds the representative (root) of the set that the given vertex belongs to using path compression.

        Parameters:
            - vertex (Node): The vertex to find.

        Returns:
            - parent[vertex] (Node): The representative (root) of the set that the vertex belongs to.
        """
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, u, v):
        """
        Unites the sets that contain vertices u and v by setting the root of one as the parent of the other.

        Patameters:
            - u: A vertex.
            - v: A vertex.
        """
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
    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, False, 'Spanning Edge Betweenness', False):
        return

    import timeit
    start = timeit.default_timer()

    edges = sorted(window.graphic_view.edges, key=lambda _edge: _edge.weight)  # Sort edges by weight
    vertices = node_list.copy()
    uf = UnionFind(vertices)
    i = 0
    spanning_betweenness_for_edges = {tuple(sorted((edge.node1.key, edge.node2.key))): 0.0 for edge in edges}

    while i < len(edges):
        # Find all edges with the same weight
        same_weight_edges = []
        j = i
        while j < len(edges) and edges[j].weight == edges[i].weight:
            same_weight_edges.append(edges[j])
            j += 1

        # Find connected components in the graph formed by mst_edges
        connected_components_edges = find_connected_components(same_weight_edges)

        for component_edges in connected_components_edges:
            comp_nodes = set()
            filtered_component_edges = []
            for edge in component_edges:
                if uf.find(edge.node1) == uf.find(edge.node2):
                    spanning_betweenness_for_edges[tuple(sorted((edge.node1.key, edge.node2.key)))] = float(0)
                else:
                    filtered_component_edges.append(edge)
                    comp_nodes.add(edge.node1)
                    comp_nodes.add(edge.node2)

            component_edges = filtered_component_edges
            if not component_edges:
                continue
            comp_nodes = list(comp_nodes)

            tc, laplacian_matrix = msts_num(component_edges, comp_nodes)
            edge_msts_and_centrality(comp_nodes, component_edges, laplacian_matrix, tc, spanning_betweenness_for_edges)

        for edge in same_weight_edges:
            if uf.find(edge.node1) != uf.find(edge.node2):
                uf.union(edge.node1, edge.node2)

        # Skip to the next set of edges with different weights
        i = j

    stop = timeit.default_timer()
    print('Time: ', stop - start)

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
