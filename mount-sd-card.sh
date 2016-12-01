#!/bin/bash

for dev in $(ls /dev | grep '^mmcblk[0-9]$')
do
	if [ $(mount | grep -c /dev/$dev ) == 0 ]
	then
		mount /dev/${dev}p1 /home/odroid/geozor
		exit 0
	fi
done
