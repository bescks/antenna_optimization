# required args: $1: antenna ip $2: port
import socket
import sys
from beacontools import BeaconScanner, IBeaconFilter
from datetime import datetime
import time
import logging
import conf

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')
fh = logging.FileHandler('/home/pi/optimization_antenna/data.csv')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

my_id = None

for id, prop in conf.ANTENNAS.items():
    if prop['IP'] == sys.argv[1]:
        my_id = id

ids = {}  # {mac: id}
msgs = {}  # {mac: msg}
for id, prop in conf.BEACONS.items():
    ids[prop['MAC']] = id
    msgs[prop['MAC']] = prop['MSG']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((conf.SERVER, int(sys.argv[2])))

data_num = 1


def callback(addr, rssi, packet, additional_info):
    global data_num
    time = datetime.now()
    if conf.SHOW_MSG:
        msg = "%s,%s,%s,%s,%s,%s,%s,%s" % (time, data_num, my_id, ids[addr], addr, packet.uuid, msgs[addr], rssi)
    else:
        msg = "%s,%s,%s,%s,%s,%s,%s" % (time, data_num, my_id, ids[addr], addr, packet.uuid, rssi)
    data_num += 1
    logger.info(msg)
    s.sendall(msg.encode())

    # server_reply = s.recv(1024).decode()
    # print(server_reply)


scanner = None
if conf.SCAN_ALL_TAGS:
    scanner = BeaconScanner(callback)
else:
    device_filter = []
    for id, prop in conf.BEACONS.items():
        device_filter.append(IBeaconFilter(prop['UUID']))
    scanner = BeaconScanner(callback, device_filter=device_filter)

scanner.start()
while True:
    time.sleep(10)
s.close()  # close connection
