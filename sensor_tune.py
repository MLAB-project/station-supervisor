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
    sys.stderr.write("Invalid number of arguments. Missing path to a config files!\n")
    sys.stderr.write("Usage: %s i2c_bus.py\n" % (sys.argv[0], ))
    sys.exit(1)

#### Sensor Configuration ###########################################


cfg = config.Config()
cfg.load_file(sys.argv[1])

sensor = cfg.get_device("lighting")
sensor.route()

time.sleep(0.5)
sensor.reset()

time.sleep(0.5)

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

        if interrupt.poll(-1):

            print("sINTer:", sensor.getInterrupts(), datetime.datetime.now().isoformat(' '))
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
