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

my_antenna = conf.ANTENNAS[sys.argv[1]]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((conf.SERVER, int(sys.argv[2])))

data_num = 1


def callback(addr, rssi, packet, additional_info):
    global data_num
    msg = "%s,%s,%s,%s,%d" % (datetime.now(), my_antenna['ID'], data_num, addr, rssi)
    data_num += 1
    logger.info(msg)
    s.sendall(msg.encode())

    # server_reply = s.recv(1024).decode()
    # print(server_reply)


scanner = BeaconScanner(callback)
scanner.start()
while True:
    time.sleep(10)
s.close()  # close connection
