from beacontools import BeaconScanner, IBeaconFilter
from datetime import datetime
import time


def callback(addr, rssi, packet, additional_info):
    print(str(datetime.now()) +
          ' [MAC]=' + str(addr) +
          # ' [POWER]=' + str(packet.tx_power) +
          # ' [UUID]=' + str(packet.uuid) +
          # ' [MAJOR]=' + str(packet.major) +
          # ' [MINOR]=' + str(packet.minor) +
          ' [RSSI]=' + str(rssi))

    # only the beacon whose uuid is in device_filter will be shown in the result.
    # scanner = BeaconScanner(callback,
    #                         device_filter=[IBeaconFilter(uuid="e2c56db5-dffb-48d2-b060-d0f5a71096e0"),
    #                                        IBeaconFilter(uuid="00000000-0000-0000-0000-000000000000")]
    #                         )


scanner = BeaconScanner(callback)
scanner.start()

while True:
    time.sleep(10)

    # scanner.stop()
