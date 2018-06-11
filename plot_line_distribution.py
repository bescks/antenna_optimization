import csv
import numpy as np
from numpy import median, mean
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import HoverTool
import numpy as np
from bokeh.models import FactorRange
import scipy.special
from os import listdir
from os.path import isfile, join

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
path_head = "/Users/gengdongjie/WorkSpace/Bitbucket/optimization_antenna/"
path = "data4/"

files = [f for f in listdir(path_head + path) if isfile(join(path_head + path, f))]
# output_file(path_head + path + "visualization.html")
figures = []
files.sort()
for file in files:
    if file.startswith("rawData"):
        continue
    output_file(path_head + path + "plot/" + file[:-4] + ".html")
    with open(path_head + path + file) as f:
        reader = csv.reader(f)
        # next(reader) 返回文件下一行，并按照分隔符生成一个list， 第一次调用时读取第一行
        header_row = next(reader)
        rssi = []
        for row in reader:
            rssi.append(row[-1])
    y1 = np.array(rssi, dtype=np.int8)
    x = np.arange(1, 501, 1)

    # line chart
    hover = HoverTool(
        tooltips=[
            ('x', '@x'),
            ('rssi', '@y'),  # use @{ } for field names with spaces
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    tools = "pan,wheel_zoom,box_zoom,reset,crosshair,zoom_in,zoom_out"

    p1 = figure(title=file + " - line chart (max= %s, min= %s, avg= %s, median= %s)" % (
        max(y1), min(y1), mean(y1), median(y1))
                , tools=[hover, tools], width=1000, height=300)
    p1.line(x, y1, line_width=2)
    p1.circle(x, y1)
    figures.append(p1)

    # bar chart
    unique_elements, counts_elements = np.unique(y1, return_counts=True)
    dis = list(zip(unique_elements.tolist(), counts_elements.tolist()))
    hover = HoverTool(
        tooltips=[
            ('rssi', '@x'),
            ('count', '@top'),  # use @{ } for field names with spaces
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    p2 = figure(title=file + " - bar chart", width=1000, plot_height=300, tools=[hover, tools])
    p2.vbar(x=unique_elements, top=counts_elements, width=1, alpha=0.5)
    p2.y_range.start = 0
    p2.x_range.range_padding = 0.1
    p2.xgrid.grid_line_color = None
    figures.append(p2)

    show(column(figures))  # open a browser
