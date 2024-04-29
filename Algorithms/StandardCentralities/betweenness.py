def betweenness(window, node_list):
    '''
    Calculates the Betweenness centrality for every node

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of NodeObject): The nodes of the graph

    Algorithm:
        - Initialize betweenness centrality dictionary
        - For each node in the graph:
            - Perform Breadth-First Search (BFS) to find shortest paths and their counts from the current node to all other nodes
            - Back-propagate dependencies from the last node visited to the source node
            - Update betweenness centrality for each node based on dependencies
    '''

    if not node_list:
        return
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'}, 'Node')
        window.dock_widget.setHidden(False)
        return

    # Initialize betweenness centrality dictionary
    betweenness_centralities = {node.key: 0 for node in node_list}

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

        # Back-propagation of dependencies
        dependencies = {node.key: 0 for node in node_list}
        while S:
            w = S.pop()
            for v in pred[w.key]:
                dependencies[v.key] += shortest_paths[v.key] / shortest_paths[w.key] * (1 + dependencies[w.key])
            if w != node:
                betweenness_centralities[w.key] += dependencies[w.key]

    # Divide centralities by 2 because it wields double scores for undirected graphs since each pair is considered twice
    for node in betweenness_centralities:
        betweenness_centralities[node] = round(betweenness_centralities[node]/2, 4)

    window.side_table.update_table(betweenness_centralities, 'Node')
    window.side_label.setText('Algorithm: Betweenness')
    window.dock_widget.setHidden(False)
