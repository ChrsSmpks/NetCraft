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

    if algo_text == 'Degree Centrality' or algo_text == 'Betweenness' or algo_text == 'Closeness':
        colm_type = 'Node'
    else:
        colm_type = 'Edge'

    import pandas as pd
    from bokeh.models import ColumnDataSource
    if plot_type == 'g':
        data = pd.DataFrame({
            'x_cent': x_cent,
            'y_counts': y_counts
        })
        # Compute rolling average
        #data['rolling_avg'] = data['y_counts'].rolling(window=50).mean()

        p = figure(
            title=f'{algo_text} Centralities Graph',
            x_axis_label='Centralities',
            y_axis_label='Frequency',
            #sizing_mode='stretch_width',
            #x_axis_type='log',
            #y_axis_type='log',
            tools="pan,box_zoom,reset,save",
            toolbar_location="above"
        )
        source = ColumnDataSource(data)
        p.line('x_cent', 'y_counts', source=source)
        #p.scatter('x_cent', 'rolling_avg', source=source, size=4, color='green', alpha=0.6, legend_label='Original Data Points')
        #p.line(x_cent, y_counts)
        #p.scatter(x_cent, y_counts, fill_color='red', line_color='red', size=8)
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

        """counts, bins, _ = plt.hist(x_cent, histtype='bar', edgecolor='black', alpha=0.75, color='blue', log=True, density=True)
        plt.title(f'{algo_text} Centralities Histogram')
        plt.xlabel('Centralities')
        plt.ylabel('Occurrences')
        plt.grid(True)
        plt.xlim(min(x_cent) * 0.5, max(x_cent) * 4)

        # Find the bin with the highest count
        max_bin_index = np.argmax(counts)
        highest_point = counts[max_bin_index]
        plt.ylim(0, highest_point * 1.3)

        mplcursors.cursor().connect('add', functools.partial(show_edge_info, x_cent=x_cent,
                                                             sorted_cent_counts=sorted_cent_counts,
                                                             nodes_edges_with_cents=nodes_edges_with_cents,
                                                             colm_type=colm_type))
        from scipy.stats import lognorm
        # best fit of data for lognorm distribution
        s, loc, scale = lognorm.fit(x_cent, floc=0.0)

        # Find the rightmost point
        rightmost_point = bins[-1]
        x = np.linspace(0, rightmost_point * 1.1, 10000)
        y = lognorm.pdf(x, s, loc=loc, scale=scale)
        plt.plot(x, y, label='lognorm', linewidth=3)"""
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
