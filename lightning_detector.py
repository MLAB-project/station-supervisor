#!/usr/bin/python

#%load_ext autoreload
#%autoreload 2

import time
import datetime
import sys
from pymlab import config

from periphery import GPIO

#### Script Arguments ###############################################

if len(sys.argv) != 2:
    sys.stderr.write("Invalid number of arguments.\n")
    sys.stderr.write("Usage: %s PORT ADDRESS\n" % (sys.argv[0], ))
    sys.exit(1)

port = eval(sys.argv[1])

#### Sensor Configuration ###########################################

cfg = config.Config(
	i2c = {"port": 0},
        bus = [
            {
                "type": "i2chub",
                "address": 0x73,
                "children": [
                    {"name": "i2cspi", "type": "i2cspi" , "channel": 0, "address": 44 },
                    {"name": "lighting", "type": "LIGHTNING01A", "TUN_CAP": 6, "channel": 5, },
                ],
            },
        ],
)

sensor = cfg.get_device("lighting")

time.sleep(0.5)
#sensor.reset()

#print("Start Antenna tunnig.")
#sensor.antennatune_on(FDIV=0,TUN_CAP=6)
#time.sleep(50)
#sensor.reset()

#time.sleep(0.5)

sensor.calib_rco()

sensor.setWDTH(1)
sensor.setNoiseFloor(4)
sensor.setIndoor(True)
sensor.setSpikeRejection(0)
sensor.setMaskDist(False)

time.sleep(0.5)


# Open GPIO 960 as interrupt input from LIGHTNING01A sensor.
interrupt = GPIO(960, "in")
interrupt.edge = "rising"


#### Data Logging ###################################################

try:
    while True:

        if interrupt.pool():

            print("sINTer:", interrupts, datetime.datetime.now().isoformat(' '))
            print("WDTH:",sensor.getWDTH())
            print("TUN_CAP:",sensor.getTUN_CAP())
    #        print("power: ", sensor.getPowerStatus())
            print("indoor:", sensor.getIndoor())
            print("Noise floor is {} uVrms".format(sensor.getNoiseFloor()))
            print("Spike rejection 0b{:04b}".format(sensor.getSpikeRejection()))
            print("single Energy:", sensor.getSingleEnergy())
            print("Mask disturbance:", sensor.getMaskDist())
            print("Storm is {:02d} km away".format(sensor.getDistance()))

        else:
            time.sleep(1)

except KeyboardInterrupt:
    interrupt.close()
    sys.exit(0)
