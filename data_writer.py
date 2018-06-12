import datetime
import conf
import os

time_data = datetime.datetime.now().strftime("%Y%m%d")
# time_raw_data = datetime.datetime.now().strftime("%Y%m%d %H:%M")

filename = ''
for key, value in conf.EXPERIMENT_HEADER.items():
    filename = filename + "-" + value
for id in conf.ANTENNAS:
    filename = filename + "-a" + str(id)
for id in conf.BEACONS:
    filename = filename + "-b" + str(id)
for key, value in conf.EXPERIMENT_SETTING.items():
    filename = filename + "-" + value

file_raw_data = "%sraw/raw%s%s.csv" % (conf.FILE_PATH, time_data, filename)
file_data = "%s%s%s.csv" % (conf.FILE_PATH, time_data, filename)


def write_raw_data(msg):
    with open(file_raw_data, 'a') as writer:
        writer.write(msg + '\n')


def write_data(msg):
    with open(file_data, 'a') as writer:
        writer.write(msg + '\n')


try:
    os.remove(file_raw_data)
except Exception as e:
    pass
try:
    os.remove(file_data)
except Exception as e:
    pass

data_header = "timestamp,dataNum,antennaID,beaconMac,beaconUUID,beaconRSSI"
write_raw_data(data_header)
write_data(data_header)
