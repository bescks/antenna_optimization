from functools import partial
import random
from threading import Thread
import time
import pandas
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure
from tornado import gen
import conf
from bokeh.palettes import Category10
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Button, TextInput
from bokeh.models import HoverTool
import sys
from logger import data_logger

# this must only be modified from a Bokeh session callback
# source are used to keep all data

sources = {}
colors = {"all": Category10[10]}
i = 0
for ip in conf.ANTENNAS:
    sources[ip] = ColumnDataSource(data=dict(x=[0], y=[conf.MEASURED_DISTANCE]))
    colors[ip] = colors["all"][i]
    i += 1

# Save curdoc() to make sure all threads see the same document
doc = curdoc()

# update coordinate x regularly
x = 0


def x_update():
    global x
    while True:
        time.sleep(conf.BEACON_FREQUENCY)
        x += 1


Thread(target=x_update).start()


@gen.coroutine
def update(ip, rssi):
    global sources, x
    sources[ip].stream(dict(x=[x], y=[rssi]))


hover = HoverTool(
    tooltips=[
        ('x', '@x'),
        ('rssi', '@y'),  # use @{ } for field names with spaces
        ("(x,y)", "($x, $y)"),
        ("screen(x,y)", "($sx, $sy)"),
        ("index", "$index"),
    ],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
)
tools = "pan,wheel_zoom,box_zoom,reset,crosshair,zoom_in,zoom_out"
plot_line = figure(width=1260, height=600, title="Realtime RSSI", x_axis_label='Time Sequence', y_axis_label='RSSI',
                   tools=[hover, tools])

for ip, prop in conf.ANTENNAS.items():
    plot_line.line(x='x', y='y', source=sources[ip], legend=prop["ID"], line_color=colors[ip], line_width=2)
    plot_line.circle(x='x', y='y', source=sources[ip], legend=prop["ID"], fill_color="white", size=3)

plot_line.legend.location = "top_left"
plot_line.legend.click_policy = "hide"
doc.add_root(plot_line)


def update_plot(ip, rssi):
    doc.add_next_tick_callback(partial(update, ip=ip, rssi=rssi))


###########################################################################
# add a button and label

label_num = 0
text_input = TextInput(value="label")
button = Button(label="Add label", button_type="success")


def save_data():
    global label_num
    label_num += 1
    label = text_input.value
    data_logger.warning("Label " + str(label_num) + ": " + label)


button.on_click(save_data)

curdoc().add_root(widgetbox(children=[text_input, button], width=150))
###########################################################################
# add a boxplot
# for source in sources:
#     source.to_df()
# import numpy as np
# import pandas as pd
#
# from bokeh.plotting import figure, show, output_file
#
# # generate some synthetic time series for six different categories
# cats = list("abcdef")
# yy = np.random.randn(2000)
# g = np.random.choice(cats, 2000)
# for i, l in enumerate(cats):
#     yy[g == l] += i // 2
# df = pd.DataFrame(dict(score=yy, group=g))
#
# # find the quartiles and IQR for each category
# groups = df.groupby('group')
# q1 = groups.quantile(q=0.25)
# q2 = groups.quantile(q=0.5)
# q3 = groups.quantile(q=0.75)
# iqr = q3 - q1
# upper = q3 + 1.5 * iqr
# lower = q1 - 1.5 * iqr
#
#
# # find the outliers for each category
# def outliers(group):
#     cat = group.name
#     return group[(group.score > upper.loc[cat]['score']) | (group.score < lower.loc[cat]['score'])]['score']
#
#
# out = groups.apply(outliers).dropna()
#
# # prepare outlier data for plotting, we need coordinates for every outlier.
# if not out.empty:
#     outx = []
#     outy = []
#     for cat in cats:
#         # only add outliers if they exist
#         if not out.loc[cat].empty:
#             for value in out[cat]:
#                 outx.append(cat)
#                 outy.append(value)
#
# p = figure(tools="save", background_fill_color="#EFE8E2", title="", x_range=cats)
#
# # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
# qmin = groups.quantile(q=0.00)
# qmax = groups.quantile(q=1.00)
# upper.score = [min([x, y]) for (x, y) in zip(list(qmax.loc[:, 'score']), upper.score)]
# lower.score = [max([x, y]) for (x, y) in zip(list(qmin.loc[:, 'score']), lower.score)]
#
# # stems
# p.segment(cats, upper.score, cats, q3.score, line_color="black")
# p.segment(cats, lower.score, cats, q1.score, line_color="black")
#
# # boxes
# p.vbar(cats, 0.7, q2.score, q3.score, fill_color="#E08E79", line_color="black")
# p.vbar(cats, 0.7, q1.score, q2.score, fill_color="#3B8686", line_color="black")
#
# # whiskers (almost-0 height rects simpler than segments)
# p.rect(cats, lower.score, 0.2, 0.01, line_color="black")
# p.rect(cats, upper.score, 0.2, 0.01, line_color="black")
#
# # outliers
# if not out.empty:
#     p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
#
# p.xgrid.grid_line_color = None
# p.ygrid.grid_line_color = "white"
# p.grid.grid_line_width = 2
# p.xaxis.major_label_text_font_size = "12pt"
# doc.add_root(p)
