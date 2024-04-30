from collections import deque


def closeness(window, node_list):
    '''
    Calculates the closeness centrality for every node

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of Node): The nodes of the graph
    '''

    if not node_list:
        return
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'}, 'Node')
        window.dock_widget.setHidden(False)
        return

    # Initialize closeness centrality dictionary
    closeness_centralities = {node.key: 0 for node in node_list}

    for node in node_list:
        # Perform bfs to calculate the distances from node
        distances = {node.key: float('inf') for node in node_list}
        distances[node.key] = 0
        queue = deque([node])

        if not window.weighted:
            while queue:
                current_node = queue.popleft()

                for neighbor in current_node.neighbors.keys():
                    if distances[neighbor.key] == float('inf'):
                        queue.append(neighbor)
                        distances[neighbor.key] = distances[current_node.key] + 1
        else:
            while queue:
                # Extract v from queue with minimum distance
                current_node = min(queue, key=lambda x: distances[x.key])
                queue.remove(current_node)

                for neighbor in current_node.neighbors.keys():
                    if distances[neighbor.key] > distances[current_node.key] + current_node.neighbors[neighbor]:
                        distances[neighbor.key] = distances[current_node.key] + current_node.neighbors[neighbor]

                        # Insert/update neighbor in queue with new key
                        if neighbor in queue:
                            queue.remove(neighbor)
                        queue.append(neighbor)

        sum_distances = sum(distances.values())
        closeness_centralities[node.key] = round((len(node_list) - 1) / sum_distances, 4) if sum_distances != 0 else 0

        window.side_table.update_table(closeness_centralities, 'Node')
        window.side_label.setText('Algorithm: Closeness')
        window.dock_widget.setHidden(False)
