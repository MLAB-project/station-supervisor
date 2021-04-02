#!/bin/sh

./afe5801_conf.py
echo 960 > /sys/class/gpio/export
mount /dev/mmcblk0p3 /data

sleep 10
ntp-wait -v

ulimit -c unlimited

cd ~/drivers


if ! pidof -x trigger > /dev/null; then
	./trigger -pre 210 -post 13 -nofir -recdir /data > /dev/null &
fi
