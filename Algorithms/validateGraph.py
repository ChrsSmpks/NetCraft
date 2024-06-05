from PyQt6.QtWidgets import QMessageBox

import DataStructures


def is_connected(node_list, edge_list):
    if not node_list:
        return True  # An empty graph is considered connected

    """# Create an adjacency list
    adjacency_list = {node: [] for node in node_list}
    for edge in edge_list:
        adjacency_list[edge.node1].append(edge.node2)
        if not edge.directed:
            adjacency_list[edge.node2].append(edge.node1)"""

    # DFS to check connectivity
    '''def dfs(node, visited):
        visited.add(node)
        for neighbor in adjacency_list[node]:
            if neighbor not in visited:
                dfs(neighbor, visited)'''

    def dfs(start_node):
        visited = set()
        stack = [start_node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in node.neighbors: #adjacency_list[node]
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited

    '''visited = set()
    # Start DFS from the first node in node_list
    dfs(node_list[0], visited)'''
    # Start DFS from the first node in node_list
    visited = dfs(node_list[0])
    """for i, node in enumerate(visited):
        if i != node.key:
            print(f'node {node.key} not visited')
            break"""

    # Check if all nodes were visited
    return len(visited) == len(node_list)


def make_connected(node_list, edge_list):
    if not node_list:
        return edge_list  # An empty graph is already connected

    """# Create an adjacency list
    adjacency_list = {node: [] for node in node_list}
    for edge in edge_list:
        adjacency_list[edge.node1].append(edge.node2)
        if not edge.directed:
            adjacency_list[edge.node2].append(edge.node1)"""

    # Helper function to perform DFS
    def dfs(start_node, visited):
        stack = [start_node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in node.neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)

    # Find all connected components
    visited = set()
    components = []
    for node in node_list:
        if node not in visited:
            component = set()
            dfs(node, component)
            components.append(component)
            visited.update(component)

    # If the graph is already connected, return the edge list as is
    if len(components) == 1:
        return edge_list

    # Add edges to connect all components
    new_edges = []
    for i in range(len(components) - 1):
        # Connect a node from component i to a node from component i+1
        node_from = list(components[i])[0]
        node_to = list(components[i + 1])[0]
        """new_edges.append((node_from, node_to))
        adjacency_list[node_from].append(node_to)
        adjacency_list[node_to].append(node_from)"""
        from DataStructures.edge import Edge
        new_edges.append(Edge(node_from, node_to, 1.0))
        node_from.neighbors[node_to] = 1.0
        node_to.neighbors[node_from] = 1.0

    # Combine old and new edges
    combined_edge_list = edge_list + new_edges

    return combined_edge_list


def validateGraph(window, node_list, allow_directed, algorithm, allow_disconnected):
    if not node_list:
        QMessageBox.warning(window, 'No Nodes Found', 'The graph has no nodes.')
        return False
    if window.directed and not allow_directed:
        QMessageBox.warning(window, 'Algorithm Not Applicable', f'{algorithm} can only be applied to undirected graphs.')
        return False
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'}, 'Edge')
        window.dock_widget.setHidden(False)
        return False
    if not allow_disconnected:
        if not is_connected(node_list, window.graphic_view.edges):
            print('not connected')
            new_edges = make_connected(node_list, window.graphic_view.edges)
            old_len = len(window.graphic_view.edges)
            window.graphic_view.edges = new_edges
            print(f'len old {old_len}, len new {len(new_edges)}')
            """i = 0
            while len(new_edges) != len(window.graphic_view.edges):
                new_edges = make_connected(node_list, new_edges)
                i += 1
                if i == 1000:
                    break
                print('new len', len(new_edges))
                print('fuck')"""
            if is_connected(node_list, new_edges):
                return True
            msg = QMessageBox(QMessageBox.Icon.Warning, 'Error', 'Centralities cannot be computed because the '
                                                                 'graph lacks connectivity.',
                              QMessageBox.StandardButton.Ok)
            msg.exec()
            return False

    return True
