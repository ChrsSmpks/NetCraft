import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import functools

from PyQt6.QtWidgets import QMessageBox
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file


def plot(cent_dict, algo_text, plot_type, in_degrees=None):
    if not cent_dict:
        QMessageBox.warning(None, 'No Centralities Found', 'The centralities have not been computed.')
        return

    cent_counts = {}
    nodes_edges_with_cents = {}
    for edge, cent in cent_dict.items():
        # Count occurrences of each centrality value
        cent_counts[cent] = cent_counts.get(cent, 0) + 1

        # Identify edges with specific centrality
        if cent not in nodes_edges_with_cents:
            nodes_edges_with_cents[cent] = []
        nodes_edges_with_cents[cent].append(edge)

    if in_degrees:
        for edge, cent in in_degrees.items():
            # Count occurrences of each centrality value
            cent_counts[cent] = cent_counts.get(cent, 0) + 1

            # Identify edges with specific centrality
            if cent not in nodes_edges_with_cents:
                nodes_edges_with_cents[cent] = []
            nodes_edges_with_cents[cent].append(edge)

    sorted_cent_counts = {k: cent_counts[k] for k in sorted(cent_counts)}

    x_cent = list(sorted_cent_counts.keys())
    y_counts = list(sorted_cent_counts.values())

    import pandas as pd
    from bokeh.models import ColumnDataSource
    if plot_type == 'g':
        data = pd.DataFrame({
            'x_cent': x_cent,
            'y_counts': y_counts
        })

        p = figure(
            title=f'{algo_text} Centralities Graph',
            x_axis_label='Centralities',
            y_axis_label='Frequency',
            tools="pan,box_zoom,reset,save",
            toolbar_location="above"
        )
        source = ColumnDataSource(data)
        p.line('x_cent', 'y_counts', source=source)
        show(p)
    else:
        centrality_values = list(cent_dict.values())
        hist, edges = np.histogram(centrality_values, density=True, bins=50)

        data = {
            'top': hist,
            'left': edges[:-1],
            'right': edges[1:]
        }

        source = ColumnDataSource(data)

        from scipy.stats import norm
        mean, std = norm.fit(centrality_values)

        x = np.linspace(min(centrality_values), max(centrality_values), 1000)
        pdf = norm.pdf(x, mean, std)

        source_pdf = ColumnDataSource(data={
            'x': x,
            'pdf': pdf
        })

        p = figure(
            title=f'{algo_text} Centralities Histogram',
            x_axis_label='Centralities',
            y_axis_label='Frequency',
            background_fill_color='#fafafa'
        )

        p.quad(top='top', bottom=0, left='left', right='right', fill_color='lightgreen', line_color='black', alpha=0.7,
               source=source)

        p.line('x', 'pdf', line_width=2, color='orange', alpha=0.7, source=source_pdf)

        p.xgrid.grid_line_color = None

        show(p)

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
