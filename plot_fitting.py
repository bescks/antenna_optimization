import csv
from numpy import median, mean
from bokeh.models import HoverTool, Span
import numpy as np
from bokeh.plotting import figure, show, output_file
import math

file_path = "data/neat/beacon5/data"
file_head = "a2-b5"
file_tx = 4
file_distance = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5]
file_order = [1, 2, 3]
output_path = "data/neat/beacon5/plot_fitting"


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


output_file('%s/%s-%sdbm-%sm.html' % (output_path, file_head, file_tx, file_distance))
x_ideal = [i * 0.1 for i in range(1, 101)]
y_ideal = [file_tx - 40 - 20 * math.log10(i) for i in x_ideal]
x = []
y_median = []
y_average = []

for distance in file_distance:
    for order in file_order:
        with open('%s/%s-%sdbm-%sm-%s.csv' % (file_path, file_head, file_tx, distance, order)) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            rssi = []
            for row in reader:
                rssi.append(int(row[-1]))
            rssi.sort(reverse=True)
            rssi = np.array(rssi)
            x.append(distance)
            y_median.append(median(rssi))
            y_average.append(mean(rssi))

hover = HoverTool(
    tooltips=[
        ('x', '@x'),
        ('y', '@y'),  # use @{ } for field names with spaces
    ],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
)
tools = "pan,wheel_zoom,box_zoom,reset,save,box_select,crosshair,zoom_in,zoom_out"
p = figure(title='%s-%dbm' % (file_head, file_tx), width=1000, height=300, tools=[hover, tools], )
p.line(x_ideal, y_ideal, line_width=2, line_color='green')
print(x,y_average)
p.circle(x, y_average)

show(p)
