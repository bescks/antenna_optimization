# csv name format: pt-b1-b2-a1-a2-1m-square-1
FILE_PATH = "data"
FILE_HEAD = "pt"
FILE_PLACE = "square"
FILE_DISTANCE = "1m"
FILE_GROUP = "1"

# available antennas
ANTENNAS = {
    # '192.168.1.127': {'ID': '2', 'MSG': ""},
    # '192.168.1.143': {'ID': '3', 'MSG': ""},
    # '192.168.171.111': {'ID': '1', 'MSG': ""},
    # '192.168.171.114': {'ID': '2', 'MSG': ""},
}

# available tags
SCAN_ALL_TAGS = None
TAGS = {
    # 'e2c56db5-dffb-48d2-b060-d0f5a71096e0': {'mac': 'c1:00:dd:00:01:de', 'ID': '1', 'MSG': ""},
    # 'e2c56db5-dffb-48d2-b060-d0f5a71096e1': {'mac': 'c1:00:dd:00:01:d7', 'ID': '2', 'MSG': ""},
    'e2c56db5-dffb-48d2-b060-d0f5a71096e2': {'mac': 'ac:23:3f:24:d3:60', 'ID': '3', 'MSG': ""},
    'fda50693-a4e2-4fb1-afcf-c6eb07647825': {'mac': '40:f3:85:90:91:52', 'ID': '4', 'MSG': ""},
    # 'fda50693-a4e2-4fb1-afcf-c6eb07647777': {'mac': 'ac:23:3f:25:0f:b5', 'ID': '5', 'MSG': ""},
}

# server IP
SERVER = '192.168.1.100'  # home
# SERVER = '192.168.171.104' # ATG-Group

# beacon frequency, unit: second
BEACON_FREQUENCY = 0.2

# show received message in console
SHOW_MSG = False

# whether run antennas directly
RUN_ANTENNAS = True
