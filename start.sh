#!/bin/sh
sleep 5
ulimit -c unlimited
JSON_CONFIG="/home/odroid/Bolidozor/NACHODSKO/NACHODSKO-R0/Bolidozor.json"
BUS_CONFIG="/home/odroid/Bolidozor/NACHODSKO/NACHODSKO-R0/bus_config.py"
~/git/station-supervisor/frequency-guard.py $JSON_CONFIG $BUS_CONFIG &
jackd -r -t5000 -u -c system  -m -dalsa -dhw:1 -r96000 -p2048 -n2 -C -i2 -s&
sleep 3
~/git/radio-observer/radio-observer -c $JSON_CONFIG&
~/git/jacktrip/jacktrip/src/jacktrip -s&
cd ~/git/RMDS-data-uploader
./run.py
