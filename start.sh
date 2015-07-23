#!/bin/sh
#ulimit -c unlimited
cd ~/Bolidozor/station-supervisor/
./frequency-guard.py&
jackd -r -t5000 -u -c system  -m -dalsa -dhw:1 -r96000 -p2048 -n2 -C -i2 -s&
sleep 3
~/git/radio-observer/radio-observer -c ~/Bolidozor/TEST-R0/Bolidozor.json&
~/svn/jacktrip/src/jacktrip -s&
cd ~/git/RMDS-data-uploader
./run.py
