import csv
from numpy import median, mean
from bokeh.models import HoverTool, Span
import numpy as np
from bokeh.plotting import figure, show, output_file
import math
from bokeh.palettes import Category10

file_path = "b5/data/distance"
file_antenna = [2]
file_beacon = [5]
file_tx = 4
file_distance = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 7, 10]
file_distance_path_loss = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6.5]
file_order = [1, 2, 3]
output_path = "."

colors = Category10[10]


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


x_ideal = [i * 0.1 for i in range(1, 101)]
y_ideal = [file_tx - 40 - 20 * math.log10(i) for i in x_ideal]
x_measured = file_distance
x_measured_path_loss = file_distance_path_loss
y_measured_avg_medians_top = []
y_measured_avg_medians = []
y_measured_avg_averages = []
y_measured_avg_medians_path_loss = []
y_measured_avg_averages_path_loss = []

for antenna in file_antenna:
    for beacon in file_beacon:
        output_file('%s/a%s-b%s-%sdbm-%sm.html' % (output_path, antenna, beacon, file_tx, file_distance))
        for distance in x_measured:
            medians_top = []
            medians = []
            averages = []
            for order in file_order:
                with open('%s/a%s-b%s-%sdbm-%sm-%s.csv' % (file_path, antenna, beacon, file_tx, distance, order)) as f:
                    reader = csv.reader(f)
                    header_row = next(reader)
                    rssi = []
                    for row in reader:
                        rssi.append(int(row[-1]))
                    rssi.sort(reverse=True)
                    rssi = np.array(rssi)
                    top_numbers = int((abs(median(rssi)) - 39) * 0.01 * len(rssi))
                    medians_top.append(median(rssi[:top_numbers]))
                    medians.append(median(rssi))
                    averages.append(mean(rssi))
            y_measured_avg_medians_top.append(mean(medians_top))
            y_measured_avg_medians.append(mean(medians))
            y_measured_avg_averages.append(mean(averages))
        for distance in x_measured_path_loss:
            medians = []
            averages = []
            for order in file_order:
                with open('%s_path_loss/a%s-b%s-path_loss-%sdbm-%sm-%s.csv' % (
                        file_path, antenna, beacon, file_tx, distance, order)) as f:
                    reader = csv.reader(f)
                    header_row = next(reader)
                    rssi = []
                    for row in reader:
                        rssi.append(int(row[-1]))
                    rssi.sort(reverse=True)
                    rssi = np.array(rssi)
                    medians.append(median(rssi))
                    averages.append(mean(rssi))
            y_measured_avg_medians_path_loss.append(mean(medians))
            y_measured_avg_averages_path_loss.append(mean(averages))

        hover = HoverTool(
            tooltips=[
                ('x', '@x'),
                ('y', '@y'),
            ],
            mode='vline'
        )
        tools = "pan,wheel_zoom,box_zoom,reset,save,box_select,crosshair,zoom_in,zoom_out"
        p = figure(title='a%s-b%s-%dbm' % (antenna, beacon, file_tx), width=1200, height=600, tools=[hover, tools],
                   x_axis_label='distance(meter)', y_axis_label='rssi')
        p.line(x_ideal, y_ideal, line_width=2, line_color=colors.pop(0), legend='ideal curve')
        p.circle(x_measured, [file_tx - 40 - 20 * math.log10(i) for i in x_measured], fill_color="white",
                 legend='ideal curve')
        p.line(x_measured, y_measured_avg_medians_top, line_width=2, line_color=colors.pop(0),
               legend='median((-median-39)% of data)')
        p.circle(x_measured, y_measured_avg_medians_top, fill_color="white", legend='median((-median-39)% of data)')
        p.line(x_measured, y_measured_avg_medians, line_width=2, line_color=colors.pop(0), legend='median')
        p.circle(x_measured, y_measured_avg_medians, fill_color="white", legend='median')
        p.line(x_measured, y_measured_avg_averages, line_width=2, line_color=colors.pop(0), legend='average')
        p.circle(x_measured, y_measured_avg_averages, fill_color="white", legend='average')

        p.line([i + 0.6 for i in x_measured_path_loss], y_measured_avg_medians_path_loss, line_width=2,
               line_color=colors.pop(0), legend='median - with path loss')
        p.circle([i + 0.6 for i in x_measured_path_loss], y_measured_avg_medians_path_loss, fill_color="white",
                 legend='median - with path loss')
        p.line([i + 0.6 for i in x_measured_path_loss], y_measured_avg_averages_path_loss, line_width=2,
               line_color=colors.pop(0), legend='average - with path loss')
        p.circle([i + 0.6 for i in x_measured_path_loss], y_measured_avg_averages_path_loss, fill_color="white",
                 legend='average - with path loss')

        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
        show(p)
