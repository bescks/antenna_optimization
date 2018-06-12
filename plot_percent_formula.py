import csv
import numpy as np
from numpy import median, mean
from bokeh.layouts import column
from bokeh.models import HoverTool
from bokeh.models import Span, Label
import conf
from bokeh.plotting import figure, show, output_file

filename_path = "data/tx_power/beacon5/"
filename_head = "20180611-pt-office-room2.01-a2-b5-1m"
filename_dbm = [4, 0, -4, -8, -12, -16, -20, '-30(40)']
filename_order = [1, 2, 3]
output_path = "data/tx_power/beacon5/plot_percent_formula/"


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
            rssi.sort()
            rssi = np.array(rssi, dtype=np.int16)
            medians = []
            for i in range(1, 101):
                med = median(rssi[:int(len(rssi) * i * 0.01)])
                medians.append(median(rssi[:int(len(rssi) * i * 0.01)]))
            x = np.arange(1, 101, 1)
            y = np.array(medians, dtype=np.int16)
            rssi = np.array(rssi, dtype=np.int16)
            title = "%s-%sdbm-%s(size=%s, max=%s, min=%s, avg=%s, median=%s)" % \
                    (filename_head, dbm, order, len(rssi), max(rssi), min(rssi), mean(rssi), median(rssi))
            p = plot_line_chart(x=x, y=y, title=title)
            hline1 = (-30 if type(dbm) is str else dbm) - 40
            percent = int(abs(median(rssi)) - 39)
            hline2 = y[percent + 1]
            plot_line(picture=p, y=[hline1, hline2], color=['green', 'red'])
            p.add_layout(
                Label(x=0, y=0, x_units='screen', y_units='screen', text='median=%s,formula=%s' % (hline1, hline2)))
            figures.append(p)

    # open a browser
    show(column(figures))
