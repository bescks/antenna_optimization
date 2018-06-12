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
from bokeh.models import Span

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
path_head = "/Users/gengdongjie/WorkSpace/Bitbucket/optimization_antenna/"
path = "data5/"

files = [f for f in listdir(path_head + path) if isfile(join(path_head + path, f))]
# output_file(path_head + path + "visualization.html")
figures = []
files.sort()


def write_to_percent(str):
    with open("percent.csv") as f:
        f.write(str + '\n')


transmission_power = 4
for file in files:
    if file not in ["data-20180611-pt-office-room11-1m-a2-b5--20dbm-1.csv",
                    "data-20180611-pt-office-room11-1m-a2-b5--20dbm-2.csv",
                    "data-20180611-pt-office-room11-1m-a2-b5--20dbm-3.csv"]:
        continue
    # output_file(path_head + path + "plot/" + file[:-4] + ".html")
    print(file)
    output_file(path_head + path + "plot2/" + "pt-office-room11-1m-a2-b5--20dbm" + ".html")

    with open(path_head + path + file) as f:
        reader = csv.reader(f)
        # next(reader) 返回文件下一行，并按照分隔符生成一个list， 第一次调用时读取第一行
        header_row = next(reader)
        rssi = []
        for row in reader:
            rssi.append(int(row[-1]))
    rssi_array = np.array(rssi)
    rssi.sort(reverse=True)
    medians = []
    for i in range(1, 101):
        med = median(rssi[:int(len(rssi) * i * 0.01)])
        medians.append(median(rssi[:int(len(rssi) * i * 0.01)]))
        write_to_percent("%s,%s" % (i * 0.01, abs(med - transmission_power)))
    y1 = np.array(medians, dtype=np.int8)
    x = np.arange(1, 101, 1)

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
        max(rssi_array), min(rssi_array), mean(rssi_array), median(rssi_array))
                , tools=[hover, tools], width=1000, height=300)
    p1.line(x, y1, line_width=2)
    p1.circle(x, y1)
    hline = Span(location=transmission_power - 40, dimension='width', line_color='green', line_width=1)
    p1.renderers.extend([hline])
    figures.append(p1)

show(column(figures))  # open a browser
