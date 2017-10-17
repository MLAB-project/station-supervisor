#!/bin/sh

sleep 10
ntp-wait -v

JSON_CONFIG="/home/odroid/geozor/station/Geozor.json"
#BUS_CONFIG="/home/odroid/bolidozor/station/bus_config.py"

ulimit -c unlimited

cd ~/repos/ISMS01A/SW

if ! pidof -x ISMS_read.py > /dev/null; then
    ./ISMS_read.py 1 $JSON_CONFIG > /dev/null &
fi

if ! pidof -x average.py > /dev/null; then
    ./average.py $JSON_CONFIG > /dev/null &
fi

cd ~/repos/data-uploader

#if ! pidof -x dataUpload.py > /dev/null; then
#	./dataUpload.py $JSON_CONFIG > /dev/null &
#fi

