import csv
from numpy import median, mean
from bokeh.layouts import column
from bokeh.models import HoverTool, Span
import numpy as np
from os import listdir
from os.path import isfile, join
from bokeh.plotting import figure, show, output_file
import conf
import math

filename_path = "data_new/"
filename_head = "a2-b5"
filename_distance = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5]
filename_order = [1, 2, 3]
output_path = "data_new/plot_formula2/"


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
output_file('%s%s-4dbm.html' % (output_path, filename_head))
x = filename_distance.copy()
y_ideal = [4 - 40 - 20 * math.log10(distance) for distance in filename_distance]
y_measured = []
for distance in filename_distance:
    medians = []
    for order in filename_order:
        with open('%s%s-%sm-4dbm-%s.csv' % (filename_path, filename_head, distance, order)) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            rssi = []
            for row in reader:
                assert len(row) == 7, "multiple lines in: %sm-%s" % (distance, order)
                rssi.append(int(row[-1]))
            assert len(rssi) == conf.SAVED_DATA_NUMBER, "data size is %s, not %s" % (len(rssi), conf.SAVED_DATA_NUMBER)

            rssi.sort()
            rssi = np.array(rssi)
            # percent = (abs(median(rssi)) - 39) * 0.01
            # print(len(rssi), percent)
            # rssi_top = rssi[:int(len(rssi) * percent)]
            # medians.append(median(rssi_top))
            medians.append(median(rssi))
    y_measured.append(sum(medians) / len(medians))

hover = HoverTool(
    tooltips=[
        ('x', '@x'),
        ('y', '@y'),  # use @{ } for field names with spaces
    ],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
)
tools = "pan,wheel_zoom,box_zoom,reset,save,box_select,crosshair,zoom_in,zoom_out"
p = figure(title=filename_head, width=1000, height=300, tools=[hover, tools], )
p.line(x, y_ideal, line_width=2, line_color='green')
p.circle(x, y_ideal)
p.line(x, y_measured, line_width=2, line_color='blue')
p.circle(x, y_measured)

show(p)
