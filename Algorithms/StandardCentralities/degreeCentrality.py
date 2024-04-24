def degreeCentrality(window, node_list):
    '''
    Calculates the degree centrality for every node

    Parameters:
        - window (QMainWindow): The main window of the app
        - node_list (list of NodeObject): The nodes of the graph
    '''

    if not node_list:
        return
    if not window.graphic_view.edges:
        window.side_label.setText('No edges in the graph!')
        window.side_table.update_table({'-': '-'})
        window.dock_widget.setHidden(False)
        return

    degrees = {node.key: len(node.neighbors) for node in node_list}

    window.side_table.update_table(degrees, 'Node')
    window.side_label.setText('Algorithm: Degree Centrality')
    window.dock_widget.setHidden(False)
