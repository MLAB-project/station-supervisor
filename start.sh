#!/bin/sh

sleep 10
ntp-wait -v

JSON_CONFIG="/home/odroid/ionozor/station/Ionozor.json"

ulimit -c unlimited

cd ~/repos/signal-piping-tools

rm -rf 3731_taps
./fir_taps -n 512 -r 96000 -c 1000 -w hanning > 3731_taps

if ! pidof sdr-widget > /dev/null; then
	{ ./sdr-widget -r 96000 | buffer & } | ./servestream -d -p 3701
fi

./servecmd -d -p 3731 'nc localhost 3701 | buffer -s 64k -m 2m | ./x_fir_dec -b 128 96000 26500 48 3731_taps'

if ! pidof radio-observer > /dev/null; then
	~/repos/radio-observer/radio-observer -c ~/ionozor/station/Ionozor.json &
fi

cd ~/repos/RMDS-data-uploader


if ! pidof -x data_upload.py > /dev/null; then
	./data_upload.py ~/ionozor/station/Ionozor.json &
fi

