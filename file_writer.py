import datetime
import conf

filename = datetime.datetime.now().strftime("%Y%m%d %H:%M")
for key, value in conf.FILE_NAME.items():
    filename = filename + "-" + value
for id in conf.ANTENNAS:
    filename = filename + "-a" + str(id)
for id in conf.BEACONS:
    filename = filename + "-b" + str(id)
filename = filename + "-" + conf.FILE_SET + ".csv"


def write_raw_data(msg):
    with open(conf.FILE_PATH + 'rawData-' + filename, 'a') as writer:
        writer.write(msg + '\n')


def write_data(msg):
    with open(conf.FILE_PATH + 'data-' + filename, 'a') as writer:
        writer.write(msg + '\n')


write_raw_data("timestamp,dataNum,antennaID,beaconMac,beaconUUID,beaconRSSI")
write_data("timestamp,dataNum,antennaID,beaconMac,beaconUUID,beaconRSSI")
