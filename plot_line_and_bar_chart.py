import csv
from os.path import isfile, join
from numpy import median, mean
from bokeh.layouts import column
from bokeh.models import HoverTool
import numpy as np
from os import listdir
from bokeh.plotting import figure, show, output_file

file_path = "b5"
file_category = ['distance', 'distance_path_loss', 'tx']
# file_category = ['tx']
file_antenna = [2]
file_beacon = [5]
file_tx = [4, 0, -4, -8, -12, -16, -20, -30]
file_distance = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6.5, 7, 10, ]
file_order = [1, 2, 3]
output_path = "plot_line_and_bar_chart"


def plot_line_chart(x, y, title):
    hover = HoverTool(
        tooltips=[
            ('x', '@x'),
            ('y', '@y'),  # use @{ } for field names with spaces
        ],
        # display a tooltip whenever the cursor is vertically in line with a
        # glyph
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
        # display a tooltip whenever the cursor is vertically in line with a
        # glyph
        mode='vline'
    )
    tools = "pan,wheel_zoom,box_zoom,reset,save,box_select,crosshair,zoom_in,zoom_out"
    p = figure(title=title, width=1000, plot_height=300, tools=[hover, tools])
    p.vbar(x=x, top=y, width=1, alpha=0.5)
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    return p


for category in file_category:
    path_loss = '-path_loss' if category == 'distance_path_loss' else ''
    for antenna in file_distance:
        for beacon in file_beacon:
            for tx in file_tx:
                for distance in file_distance:
                    file_exist = False
                    for file in listdir('%s/data/%s' % (file_path, category)):
                        if "a%s-b%s%s-%sdbm-%sm" % (antenna, beacon, path_loss, tx, distance) in file:
                            file_exist = True
                    if file_exist:
                        figures = []
                        output_file(
                            '%s/%s/%s/a%s-b%s%s-%sdbm-%sm.html' %
                            (file_path, output_path, category, antenna, beacon, path_loss, tx, distance))
                        for order in file_order:
                            filename = ('%s/data/%s/a%s-b%s%s-%sdbm-%sm-%s.csv' %
                                        (file_path, category, antenna, beacon, path_loss, tx, distance, order))
                            with open(filename) as f:
                                reader = csv.reader(f)
                                header_row = next(reader)
                                rssi = []
                                for row in reader:
                                    rssi.append(int(row[-1]))
                                x = np.arange(1, len(rssi) + 1, 1)
                                y = np.array(rssi, dtype=np.int16)
                                title = "%s(size=%s, max=%s, min=%s, avg=%s, median=%s)" % (
                                    filename.split('/')[-1], len(y), max(y), min(y), mean(y), median(y))
                                # add line chart
                                figures.append(
                                    plot_line_chart(
                                        x=x, y=y, title=title))
                                # add bar chart
                                unique_elements, counts_elements = np.unique(
                                    y, return_counts=True)
                                figures.append(
                                    plot_bar_chart(
                                        x=unique_elements,
                                        y=counts_elements,
                                        title=''))
                        # open a browser
                        show(column(figures))
