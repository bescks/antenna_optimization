import csv
from numpy import median, mean
from bokeh.layouts import column
from bokeh.models import HoverTool, Span
import numpy as np
from os import listdir
from os.path import isfile, join
from bokeh.plotting import figure, show, output_file
import conf

filename_path = "data/tx_power/beacon5/"
filename_head = "20180611-pt-office-room2.01-a2-b5-1m"
filename_dbm = [4, 0, -4, -8, -12, -16, -20, '-30(40)']
filename_order = [1, 2, 3]
output_path = "data/tx_power/beacon5/plot_line_and_bar_chart/"


def plot_line_chart(x, y, title):
    hover = HoverTool(
        tooltips=[
            ('x', '@x'),
            ('y', '@y'),  # use @{ } for field names with spaces
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    tools = "pan,wheel_zoom,box_zoom,reset,save,box_select,crosshair,zoom_in,zoom_out"

    p = figure(title=title, width=1000, height=300, tools=[hover, tools], )
    p.line(x, y, line_width=2)
    p.circle(x, y)
    return p


def plot_bar_chart(x, y, title):
    hover = HoverTool(
        tooltips=[
            ('x', '@x'),
            ('y', '@top'),  # use @{ } for field names with spaces
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    tools = "pan,wheel_zoom,box_zoom,reset,save,box_select,crosshair,zoom_in,zoom_out"
    p = figure(title=title, width=1000, plot_height=300, tools=[hover, tools])
    p.vbar(x=x, top=y, width=1, alpha=0.5)
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    return p


def plot_line(picture, x=None, y=None):
    lines = []
    if x is not None:
        # Horizontal line
        hline = Span(location=-60, dimension='width', line_color='green', line_width=1)
        lines.append(hline)
    if y is not None:
        # Vertical line
        vline = Span(location=20, dimension='height', line_color='red', line_width=1)
        lines.append(vline)
    picture.renderers.extend(lines)


# main plot program
for dbm in filename_dbm:
    output_file('%s%s-%sdbm.html' % (output_path, filename_head, dbm))
    figures = []
    for order in filename_order:
        with open('%s%s-%sdbm-%s.csv' % (filename_path, filename_head, dbm, order)) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            rssi = []
            for row in reader:
                assert len(row) == 7, "multiple lines in: %sdbm-%s" % (dbm, order)
                rssi.append(row[-1])
            assert len(rssi) == conf.SAVED_DATA_NUMBER, "data size is %s, not %s" % (len(rssi), conf.SAVED_DATA_NUMBER)
            x = np.arange(1, len(rssi) + 1, 1)
            y = np.array(rssi, dtype=np.int16)
            title = "%s-%sdbm-%s(size=%s, max=%s, min=%s, avg=%s, median=%s)" % \
                    (filename_head, dbm, order, len(y), max(y), min(y), mean(y), median(y))
            # add line chart
            figures.append(plot_line_chart(x=x, y=y, title=title))
            # add bar chart
            unique_elements, counts_elements = np.unique(y, return_counts=True)
            figures.append(plot_bar_chart(x=unique_elements, y=counts_elements, title=''))
    # open a browser
    show(column(figures))
