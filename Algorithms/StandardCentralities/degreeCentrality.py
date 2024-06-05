def degreeCentrality(window, node_list, weighted, directed):
    '''
    Calculates the degree centrality for every node

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of Node): The nodes of the graph
    '''
    from ..validateGraph import validateGraph
    if not validateGraph(window, node_list, True, None, True):
        return

    import timeit
    start = timeit.default_timer()

    if not directed:
        degrees_in = None
        if not weighted:
            degrees = {node.key: len(node.neighbors) for node in node_list}
        else:
            degrees = {node.key: sum(node.neighbors.values()) for node in node_list}
    else:
        if not weighted:
            degrees = {node.key: len(node.neighbors) for node in node_list}
            degrees_in = {node.key: len(node.neighbors_in) for node in node_list}
        else:
            degrees = {node.key: sum(node.neighbors.values()) for node in node_list}
            degrees_in = {node.key: sum(node.neighbors_in.values()) for node in node_list}

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    window.side_table.update_table(degrees, 'Node', degrees_in)
    window.side_label.setText('Algorithm: Degree Centrality')
    window.dock_widget.setHidden(False)
