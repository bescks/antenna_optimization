# csv name format: timestamp-pt-b1-b2-a1-a2-home-room-1m-1
FILE_PATH = "newcome"

EXPERIMENT_SETTING = {
    'power': '4dbm',
    'distance': "6.5m",
    'order': '3'
}
CSV_COMMENT = "(office room2.11 path_loss_0.6m)",  # square, corridor,room

# available tags
SCAN_ALL_TAGS = False
BEACONS = {
    1: {'UUID': 'e2c56db5-dffb-48d2-b060-d0f5a71096e0', 'MAC': 'c1:00:dd:00:01:de', 'name': 'MiniBeacon_00478',
        'MSG': ""},
    # 2: {'UUID': 'e2c56db5-dffb-48d2-b060-d0f5a71096e1', 'MAC': 'c1:00:dd:00:01:d7','name': 'MiniBeacon_00478', 'MSG': ""},
    # 3: {'UUID': 'e2c56db5-dffb-48d2-b060-d0f5a71096e2', 'MAC': 'ac:23:3f:24:d3:60', 'name': 'MiniBeacon_00001',
    #     'MSG': "with circle"},
    # 4: {'UUID': 'fda50693-a4e2-4fb1-afcf-c6eb07647825', 'MAC': '40:f3:85:90:91:52', 'MSG': "black"},
    # 5: {'UUID': 'fda50693-a4e2-4fb1-afcf-c6eb07647777', 'MAC': 'ac:23:3f:25:0f:b5', 'name': 'MBeacon', 'MSG': "card"},
}

# available antennas
ANTENNAS = {
    # home
    # 1: {'IP': '192.168.1.127', 'MSG': ""},
    # 2: {'IP': '192.168.1.143', 'MSG': ""},
    # office
    # 1: {'IP': '192.168.171.111', 'MSG': ""},
    2: {'IP': '192.168.171.114', 'MAC': 'B8:27:EB:6F:E9:0E', 'MSG': ""},
}

# server IP
# SERVER = '192.168.1.100'  # home: Huawei-WIFI
SERVER = '192.168.171.101'  # office: ATG-Group

# beacon frequency, unit: second
BEACON_FREQUENCY = 0.2

# show received message in console
SHOW_MSG = False

# whether run antennas directly
RUN_ANTENNAS = True

# number of saved data
SAVED_DATA_NUMBER = 500

# auto start saving
AUTO_START_NUMBER = 50  # 0 means not auto start saving
