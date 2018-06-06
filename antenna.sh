#!/usr/bin/env bash
# incoming args:  $1: antenna ip, $2: server ip,  $3: port, $4: run_antennas,
# $6: antenna id, $7: msg
ssh root@$1 "test -e /home/pi/optimization_antenna"
if [ $? -eq 0 ]; then
    # if file exists
    ssh root@$1 "rm -rf /home/pi/optimization_antenna/*"
else
    ssh pi@$1 "mkdir /home/pi/optimization_antenna/"
fi

scp antenna.py conf.py "pi@$1:/home/pi/optimization_antenna/"

ssh pi@$1 "kill \$(ps aux | grep antenna.py | grep -v color| awk '{print \$2}')"

if [ $4 -eq 1 ]; then
    ssh pi@$1 "python3 /home/pi/optimization_antenna/antenna.py $1 $3"
fi

