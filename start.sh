#!/bin/sh

./afe5801_conf.py
echo 960 > /sys/class/gpio/export
mount /dev/mmcblk0p3 /data
mount -t tmpfs tmp /tmp
sleep 10
ntp-wait -v

ulimit -c unlimited

if ! pgrep ourperiph.py > /dev/null; then
	./regweb/ourperiph.py &
fi

mkdir -p /tmp/snaps
if ! pgrep cleanup.sh > /dev/null; then
	./cleanup.sh &
fi

cd ~/drivers

if ! pidof -x triggernew > /dev/null; then
	./triggernew -pre 446 -post 446 -nofir -recdir /data \
		-spre 1 -spost 3 -snapdir /tmp/snaps/ -depth 40 > /dev/null &
fi
