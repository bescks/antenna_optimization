# whether run antennas directly
RUN_ANTENNAS = True

# available antennas
ANTENNAS = {
    # '192.168.1.120': {'ID': '1', 'MSG': ""},
    '192.168.1.127': {'ID': '2', 'MSG': ""},
    '192.168.1.143': {'ID': '3', 'MSG': ""}
}

# available tags
TAGS = {'c1:00:dd:00:01:d7': {'ID': '1', 'MSG': ""},
        }

# server IP
SERVER = '192.168.1.100'

# beacon frequency, unit: second
BEACON_FREQUENCY = 0.2
MEASURED_DISTANCE = -59

# show received message in console
SHOW_MSG = False
