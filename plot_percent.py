import csv
from os import listdir

import numpy as np
import math
from numpy import median, mean
from bokeh.layouts import column
from bokeh.models import HoverTool
from bokeh.models import Span, Label
import conf
from bokeh.plotting import figure, show, output_file

file_path = "data/neat/beacon3/data"
file_antenna = [2]
file_beacon = [3]
file_distance = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5]
file_tx = [4, 0, -4, -8, -16, -20, -30]
file_order = [1, 2, 3]
output_path = "data/neat/beacon3/plot_percent"


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


def plot_line(picture, color, x=None, y=None):
    lines = []
    if x is not None:
        for i, c in zip(x, color):
            # Vertical line
            vline = Span(location=i, dimension='height', line_color=c, line_width=1)
            lines.append(vline)
    if y is not None:
        for i, c in zip(y, color):
            # Horizontal line
            hline = Span(location=i, dimension='width', line_color=c, line_width=1)
            lines.append(hline)
    picture.renderers.extend(lines)


# main plot program
for antenna in file_antenna:
    for beacon in file_beacon:
        for distance in file_distance:
            for tx in file_tx:
                file_exist = False
                for file in listdir(file_path):
                    if "a%s-b%s-%sdbm-%sm" % (antenna, beacon, tx, distance) in file:
                        file_exist = True
                if file_exist:
                    output_file('%s/a%s-b%s-%sdbm-%sm.html' % (output_path, antenna, beacon, tx, distance))
                    figures = []
                    for order in file_order:
                        filename = 'a%s-b%s-%sdbm-%sm-%s.csv' % (antenna, beacon, tx, distance, order)
                        with open(('%s/%s') % (file_path, filename)) as f:
                            reader = csv.reader(f)
                            header_row = next(reader)
                            rssi = []
                            for row in reader:
                                rssi.append(int(row[-1]))
                            rssi.sort(reverse=True)
                            rssi = np.array(rssi, dtype=np.int16)
                            medians = []
                            for i in range(1, 101):
                                med = median(rssi[:int(len(rssi) * i * 0.01)])
                                medians.append(median(rssi[:int(len(rssi) * i * 0.01)]))
                            x = np.arange(1, 101, 1)
                            y = np.array(medians, dtype=np.int16)
                            rssi = np.array(rssi, dtype=np.int16)
                            title = "%s(size=%s, max=%s, min=%s, avg=%s, median=%s)" % \
                                    (filename, len(rssi), max(rssi), min(rssi), mean(rssi), median(rssi))
                            p = plot_line_chart(x=x, y=y, title=title)
                            hline1 = tx - 40 - 20 * math.log10(distance)
                            percent = int(abs(median(rssi)) - 39)
                            hline2 = y[percent + 1]
                            plot_line(picture=p, y=[hline1, hline2], color=['green', 'red'])
                            p.add_layout(
                                Label(x=0, y=0, x_units='screen', y_units='screen',
                                      text='median=%d,formula=%d' % (hline1, hline2)))
                            figures.append(p)

                        # open a browser
                    show(column(figures))
