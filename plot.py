from functools import partial
from threading import Thread
import time
from bokeh.plotting import curdoc, figure
import os
from tornado import gen
import conf
import numpy as np
from bokeh.palettes import Category10
from bokeh.layouts import row, column
from bokeh.models.widgets import Button, Div
from bokeh.models import ColumnDataSource, Label
from bokeh.models import HoverTool
from file_writer import write_data, write_raw_data
import multiprocessing as mp

# this must only be modified from a Bokeh session callback
# source are used to keep all data

sources = {}  # {beaconsID:{antennaID: source}}
colors = {"all": Category10[10]}
i = 0
for antenna_id in conf.ANTENNAS:
    sources[antenna_id] = {}
    colors[antenna_id] = {}
    for beacon_id in conf.BEACONS:
        sources[antenna_id][beacon_id] = ColumnDataSource(
            data=dict(x=[], y=[]))  # x, y indicate the first set of data
        colors[antenna_id][beacon_id] = colors["all"][i]
        i += 1

# Save curdoc() to make sure all threads see the same document
doc = curdoc()

# add figure
hover = HoverTool(
    tooltips=[
        ('x', '@x'),
        ('rssi', '@y'),  # use @{ } for field names with spaces
        ("(x,y)", "($x, $y)"),
        ("screen(x,y)", "($sx, $sy)"),
        ("index", "$index"),
    ],
    mode='vline'  # display a tooltip whenever the cursor is vertically in line with a glyph
)
tools = "pan,wheel_zoom,box_zoom,reset,crosshair,zoom_in,zoom_out"
plot_line = figure(
    width=1260,
    height=600,
    title="Realtime RSSI",
    x_axis_label='Time Sequence',
    y_axis_label='RSSI',
    tools=[
        hover,
        tools])
for antenna_id in conf.ANTENNAS:
    for beacon_id in conf.BEACONS:
        plot_line.line(
            x='x',
            y='y',
            source=sources[antenna_id][beacon_id],
            legend="Antenna %s,Beacon %s" % (antenna_id, beacon_id),
            line_color=colors[antenna_id][beacon_id],
            line_width=1.5)
        plot_line.circle(
            x='x',
            y='y',
            source=sources[antenna_id][beacon_id],
            legend="Antenna %s,Beacon %s" % (antenna_id, beacon_id),
            fill_color="white",
            size=2.5)

plot_line.legend.location = "top_left"
plot_line.legend.click_policy = "hide"
doc.add_root(plot_line)

# update x-coordinate regularly
x = 0


def x_update():
    global x
    while True:
        time.sleep(conf.BEACON_FREQUENCY)
        x += conf.BEACON_FREQUENCY


Thread(target=x_update).start()

# add labels
label1 = Label(x=0, y=0, x_units='screen', y_units='screen',
               text='saved: 0/0', render_mode='css',
               background_fill_alpha=0)
label2 = Label(x=0, y=20, x_units='screen', y_units='screen',
               text='max=0, min=0, avg=0', render_mode='css',
               background_fill_alpha=0)
plot_line.add_layout(label1)
plot_line.add_layout(label2)

# add a button
label_num = 0
button = Button(label="Save Data", button_type="success")

saving = False
saving_num = 0
saving_start = 0
saving_end = 0
statistics = {'min': 999, 'max': -999, 'sum': 0, 'data': [], 'median': 0, 'start': 0, 'end': 0}


def save_data():
    global saving
    button.disabled = True
    saving = True
    statistics['start'] = 'n'
    label1.text = "saved: 0/%s" % (conf.SAVED_DATA_NUMBER)
    write_raw_data("start saving")
    os.system("say 'start'")


def show_statistics():
    y = np.array(statistics['data'], dtype=np.int8)

    unique_elements, counts_elements = np.unique(y, return_counts=True)
    dis = list(zip(unique_elements.tolist(), counts_elements.tolist()))
    hover = HoverTool(
        tooltips=[
            ('rssi', '@x'),
            ('count', '@top'),  # use @{ } for field names with spaces
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    plot_bar = figure(width=1000, plot_height=300, tools=[hover, tools])
    plot_bar.vbar(x=unique_elements, top=counts_elements, width=1, alpha=0.5)
    plot_bar.y_range.start = 0
    plot_bar.x_range.range_padding = 0.1
    plot_bar.xgrid.grid_line_color = None
    doc.add_root(plot_bar)


# stream new data
@gen.coroutine
def update(client_data):
    global sources, x, saving, saving_num, statistics
    write_raw_data(client_data)
    client_data_list = client_data.split(',')
    data_num = int(client_data_list[1])
    antenna_id = int(client_data_list[2])
    beacon_id = int(client_data_list[3])
    rssi = int(client_data_list[-1])
    sources[antenna_id][beacon_id].stream(dict(x=[x], y=[rssi]))
    if data_num == conf.AUTO_START_NUMBER:
        save_data()
    if saving:
        write_data(client_data)
        saving_num += 1
        label1.text = "saved: %s/%s" % (saving_num, conf.SAVED_DATA_NUMBER)
        statistics['data'].append(rssi)
        if rssi < statistics['min']:
            statistics['min'] = rssi
        elif rssi > statistics['max']:
            statistics['max'] = rssi
        statistics['sum'] = statistics['sum'] + rssi
        label2.text = "min=%s, max=%s, avg=%.3f" % (
            statistics['min'], statistics['max'], statistics['sum'] / saving_num)

        if saving_num == conf.SAVED_DATA_NUMBER:
            saving = False
            label1.text = label1.text + " finished! " + str(len(statistics['data']))
            label2.text = label2.text + ", median=" + str(np.median(statistics['data']))
            write_raw_data("end saving")
            show_statistics()
            os.system('say "completed"')

        # update plot


def update_plot(client_data):
    doc.add_next_tick_callback(partial(update, client_data=client_data))


if len(conf.BEACONS) > 1:
    button.disabled = True
button.on_click(save_data)
curdoc().add_root(column([row([button])], width=150))
