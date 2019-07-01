#!/bin/sh

./afe5801_conf.py
echo 960 > /sys/class/gpio/export
mount /dev/mmcblk0p3 /data

sleep 10
ntp-wait -v

JSON_CONFIG="/home/odroid/bolidozor/station/Bolidozor.json"
BUS_CONFIG="/home/odroid/bolidozor/station/bus_config.py"

ulimit -c unlimited

if ! pidof -x lightning_example.py > /dev/null; then
	python ~/repos/examples/lightning_example.py 0 > ~/lightning_log &
fi

cd ~/drivers


if ! pidof -x trigger > /dev/null; then
	./trigger -pre 213 -post 10 -recdir /data > /dev/null &
fi

