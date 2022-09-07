#!/bin/sh
set -e
cd /tmp/snaps
while [ true ]; do
	ls -t | tail -n +3 | xargs --no-run-if-empty -n1 rm
	sleep 0.1
done
