import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import functools


def plot(cent_dict):
    print(cent_dict)

    cent_counts = {}
    edges_with_cents = {}
    for edge, cent in cent_dict.items():
        # Count occurrences of each centrality value
        cent_counts[cent] = cent_counts.get(cent, 0) + 1

        # Identify edges with specific centrality
        if cent not in edges_with_cents:
            edges_with_cents[cent] = []
        edges_with_cents[cent].append(edge)

    sorted_cent_counts = {k: cent_counts[k] for k in sorted(cent_counts)}

    x_cent = list(sorted_cent_counts.keys())
    y_counts = list(sorted_cent_counts.values())

    # Plot the graph
    fig, ax = plt.subplots()
    ax.plot(x_cent, y_counts, marker='o', linestyle='-')
    ax.set_title('Centralities Graph')
    ax.set_xlabel('Centralities')
    ax.set_ylabel('Occurrences')
    ax.grid(True)

    mplcursors.cursor(ax).connect('add', functools.partial(show_edge_info, x_cent=x_cent, sorted_cent_counts=sorted_cent_counts, edges_with_cents=edges_with_cents))

    plt.show()

    for cent, count in cent_counts.items():
        print(f'Centrality {cent}: {count} edges')

    for cent, edges in edges_with_cents.items():
        edgs = ', '.join(edges)
        print(f'Centrality {cent}: {edgs}')


def show_edge_info(sel, x_cent, sorted_cent_counts, edges_with_cents):
    x_val = x_cent[np.abs(x_cent - sel.target[0]).argmin()]
    if x_val in edges_with_cents:
        #sel.annotation.set_text('\n'.join(edges_with_cents[x_val]))
        edges_text = '\n'.join(edges_with_cents[x_val])
        #coord_text = f'X: {sel.target[0]:.4f}\nY: {sel.target[1]:.4f}'
        coord_text = f'X: {x_val}\nY: {sorted_cent_counts[x_val]}'
        sel.annotation.set_text(f'{coord_text}\n\nEdges:\n{edges_text}')
