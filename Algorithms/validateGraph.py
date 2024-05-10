from PyQt6.QtWidgets import QMessageBox


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
        for node in node_list:
            if not node.neighbors:
                msg = QMessageBox(QMessageBox.Icon.Warning, 'Error', 'Centralities cannot be computed because the '
                                                                     'graph lacks connectivity.',
                                  QMessageBox.StandardButton.Ok)
                msg.exec()
                return False

    return True
