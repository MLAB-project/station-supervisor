#!/bin/sh

./afe5801_conf.py
echo 960 > /sys/class/gpio/export
mount /dev/mmcblk0p3 /data

sleep 10
ntp-wait -v

JSON_CONFIG="/home/odroid/bolidozor/station/Bolidozor.json"
BUS_CONFIG="/home/odroid/bolidozor/station/bus_config.py"

ulimit -c unlimited

cd

repos/signal-piping-tools/servecmd -w -p 4000 'drivers/dma_test -f -'