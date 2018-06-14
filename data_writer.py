import datetime
import conf
import os

time_data = datetime.datetime.now().strftime("%Y%m%d")
# time_raw_data = datetime.datetime.now().strftime("%Y%m%d %H:%M")

filename = ''
for id in conf.ANTENNAS:
    filename = filename + "a%s-" % id
for id in conf.BEACONS:
    filename = filename + "b%s-" % id
for key, value in conf.EXPERIMENT_SETTING.items():
    filename = filename + "%s-" % value
filename = filename[:-1]
file_raw_data = "%s/raw/raw-%s.csv" % (conf.FILE_PATH, filename)
file_data = "%s/%s.csv" % (conf.FILE_PATH, filename)


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

data_header = "timestamp,dataNum,antennaID,beaconID,beaconMac,beaconUUID,beaconRSSI,%s" % conf.CSV_COMMENT
write_raw_data(data_header)
write_data(data_header)
