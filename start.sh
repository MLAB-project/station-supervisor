#!/bin/sh

./afe5801_conf.py
echo 960 > /sys/class/gpio/export
mount /dev/mmcblk0p3 /data

JSON_CONFIG="Lightning.json"
BUS_CONFIG="bus_config.py"

./frequency-set.py $JSON_CONFIG $BUS_CONFIG

sleep 10
ntp-wait -v

ulimit -c unlimited

#if ! pidof -x lightning_example.py > /dev/null; then
#	python ~/repos/pymlab/examples/lightning_example.py 0 > ~/lightning_log &
#fi

cd ~/drivers


if ! pidof -x trigger > /dev/null; then
	./trigger -pre 222 -post 1 -nofir -recdir /data > /dev/null &
fi
