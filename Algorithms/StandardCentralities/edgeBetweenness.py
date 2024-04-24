def edgeBetweenness(window, node_list):
    '''
    Calculates the Edge Betweenness centrality for every edge

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of NodeObject): The nodes of the graph

    Algorithm:
        - Initialize edge_betweenness dictionary to store edge betweenness centrality values for each edge
        - For each node in the graph:
            - Perform Breadth-First Search (BFS) to find the shortest paths and their counts from the current node to all other nodes
            - Back-propagate dependencies from the last node visited to the source node
            - Update edge betweenness centrality values based on the dependencies
    '''

    if not node_list:
        return
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'})
        window.dock_widget.setHidden(False)
        return

    # Initialize betweenness centrality dictionary
    edge_betweenness = {tuple(sorted((edge.node1.key, edge.node2.key))): 0 for edge in window.graphic_view.edges}

    for node in node_list:
        # Initialization
        S = []
        pred = {node.key: [] for node in node_list}             # list of predecessors on shortest paths from source
        shortest_paths = {node.key: 0 for node in node_list}    # number of shortest path from source to every other node
        shortest_paths[node.key] = 1
        distances = {node.key: -1 for node in node_list}        # distances from source
        distances[node.key] = 0
        queue = [node]

        # Breadth-first search
        while queue:
            v = queue.pop(0)
            S.append(v)
            for neighbor in v.neighbors:
                if distances[neighbor.key] < 0:
                    queue.append(neighbor)
                    distances[neighbor.key] = distances[v.key] + 1
                if distances[neighbor.key] == distances[v.key] + 1:
                    shortest_paths[neighbor.key] += shortest_paths[v.key]
                    pred[neighbor.key].append(v)

        # Dependency calculation
        dependencies = {node.key: 0 for node in node_list}
        while S:
            w = S.pop()
            for v in pred[w.key]:
                c = shortest_paths[v.key] / shortest_paths[w.key] * (1 + dependencies[w.key])
                if (v.key, w.key) in edge_betweenness.keys():
                    edge_betweenness[(v.key, w.key)] += c
                dependencies[v.key] += c

    # Round centralities to 4 decimals
    for edge in edge_betweenness:
        edge_betweenness[edge] = round(edge_betweenness[edge], 4)

    window.side_table.update_table(edge_betweenness, 'Edge')
    window.side_label.setText('Algorithm: Edge Betweenness')
    window.dock_widget.setHidden(False)

