import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import functools


def plot(cent_dict, algo_text):
    cent_counts = {}
    nodes_edges_with_cents = {}
    for edge, cent in cent_dict.items():
        # Count occurrences of each centrality value
        cent_counts[cent] = cent_counts.get(cent, 0) + 1

        # Identify edges with specific centrality
        if cent not in nodes_edges_with_cents:
            nodes_edges_with_cents[cent] = []
        nodes_edges_with_cents[cent].append(edge)

    sorted_cent_counts = {k: cent_counts[k] for k in sorted(cent_counts)}

    x_cent = list(sorted_cent_counts.keys())
    y_counts = list(sorted_cent_counts.values())

    # Plot the graph
    fig, ax = plt.subplots()
    ax.plot(x_cent, y_counts, marker='o', linestyle='-')
    ax.set_title(f'{algo_text} Centralities Graph')
    ax.set_xlabel('Centralities')
    ax.set_ylabel('Occurrences')
    ax.grid(True)

    if algo_text == 'Degree Centrality' or algo_text == 'Betweenness' or algo_text == 'Closeness':
        colm_type = 'Node'
    else:
        colm_type = 'Edge'

    mplcursors.cursor(ax).connect('add', functools.partial(show_edge_info, x_cent=x_cent, sorted_cent_counts=sorted_cent_counts, nodes_edges_with_cents=nodes_edges_with_cents, colm_type=colm_type))

    plt.show()


def show_edge_info(sel, x_cent, sorted_cent_counts, nodes_edges_with_cents, colm_type):
    x_val = x_cent[np.abs(x_cent - sel.target[0]).argmin()]
    if x_val in nodes_edges_with_cents:
        if colm_type == 'Edge':
            nodes_edges_text = '\n'.join(['({}, {})'.format(x[0], x[1]) for x in nodes_edges_with_cents[x_val]])
            coord_text = f'X: {x_val}\nY: {sorted_cent_counts[x_val]}'
            sel.annotation.set_text(f'{coord_text}\n\nEdges:\n{nodes_edges_text}')
        else:
            nodes_edges_text = '\n'.join(map(str, nodes_edges_with_cents[x_val]))
            coord_text = f'X: {x_val}\nY: {sorted_cent_counts[x_val]}'
            sel.annotation.set_text(f'{coord_text}\n\nNodes:\n{nodes_edges_text}')
