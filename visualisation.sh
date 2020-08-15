#!/bin/sh

./afe5801_conf.py

BUS_CONFIG="/home/odroid/bolidozor/station/bus_config.py"

ulimit -c unlimited

cd

repos/signal-piping-tools/servecmd -w -p 4000 'drivers/dma_test -f -'
