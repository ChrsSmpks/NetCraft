def edgeBetweenness(window, node_list):
    '''
    Calculates the Edge Betweenness centrality for every edge

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of Node): The nodes of the graph

    Algorithm:
        - Initialize edge_betweenness dictionary to store edge betweenness centrality values for each edge
        - For each node in the graph:
            - Perform Breadth-First Search (BFS) to find the shortest paths and their counts from the current node to all other nodes
            - Back-propagate dependencies from the last node visited to the source node
            - Update edge betweenness centrality values based on the dependencies
    '''
    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, True, None, True):
        return

    import timeit
    start = timeit.default_timer()

    # Initialize betweenness centrality dictionary
    if not window.directed:
        edge_betweenness = {tuple(sorted((edge.node1.key, edge.node2.key))): 0 for edge in window.graphic_view.edges}
    else:
        edge_betweenness = {(edge.node1.key, edge.node2.key): 0 for edge in window.graphic_view.edges}

    for node in node_list:
        # Initialization
        S = []
        pred = {node.key: [] for node in node_list}             # list of predecessors on shortest paths from source
        shortest_paths = {node.key: 0 for node in node_list}    # number of shortest path from source to every other node
        shortest_paths[node.key] = 1
        distances = {node.key: float('inf') for node in node_list}        # distances from source
        distances[node.key] = 0
        queue = [node]

        if not window.weighted:
            # Breadth-first search
            while queue:
                v = queue.pop(0)
                S.append(v)
                for neighbor in v.neighbors.keys():
                    if distances[neighbor.key] == float('inf'):
                        queue.append(neighbor)
                        distances[neighbor.key] = distances[v.key] + 1
                    if distances[neighbor.key] == distances[v.key] + 1:
                        shortest_paths[neighbor.key] += shortest_paths[v.key]
                        pred[neighbor.key].append(v)
        else:
            while queue:
                # Extract v from queue with minimum distance
                v = min(queue, key=lambda x: distances[x.key])
                queue.remove(v)
                S.append(v)
                for neighbor in v.neighbors.keys():
                    if distances[neighbor.key] > distances[v.key] + v.neighbors[neighbor]:
                        distances[neighbor.key] = distances[v.key] + v.neighbors[neighbor]

                        # Insert/update neighbor in queue with new key
                        if neighbor in queue:
                            queue.remove(neighbor)
                        queue.append(neighbor)

                        shortest_paths[neighbor.key] = 0
                        pred[neighbor.key].clear()
                    if distances[neighbor.key] == distances[v.key] + v.neighbors[neighbor]:
                        shortest_paths[neighbor.key] += shortest_paths[v.key]
                        pred[neighbor.key].append(v)

        # Back-propagation of dependencies
        dependencies = {node.key: 0 for node in node_list}
        while S:
            w = S.pop()
            for v in pred[w.key]:
                c = shortest_paths[v.key] / shortest_paths[w.key] * (1 + dependencies[w.key])
                if (v.key, w.key) in edge_betweenness.keys():
                    edge_betweenness[(v.key, w.key)] += c
                dependencies[v.key] += c

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    # Round centralities to 4 decimals
    for edge in edge_betweenness:
        edge_betweenness[edge] = round(edge_betweenness[edge], 4)

    window.side_table.update_table(edge_betweenness, 'Edge')
    window.side_label.setText('Algorithm: Edge Betweenness')
    window.dock_widget.setHidden(False)

