#!/usr/bin/python
# 
# Software for frequency management on RMDS station
#
# 

import time
import datetime
import sys
from pymlab import config

#### System configuration ###########################################

port = 1  # I2C port number
frequency =

cfg = config.Config(
    i2c = {
        "port": port,
    },
    bus = [
        {
            "type": "i2chub",
            "address": 0x70,
	       	"children": [
                        { "name":"counter", "type":"acount02", "channel": 2, },
                        { "name":"clkgen", "type":"clkgen01", "channel": 5, },
		    ],
        },
    ],
)

#### System Initialization ###############################################

cfg.initialize()
print "RMDS Station frequency management test software \r\n"
fcount = cfg.get_device("counter")
fgen = cfg.get_device("clkgen")
time.sleep(0.5)
frequency = fcount.get_freq()

#### Data Logging ###################################################

try:
    with open("frequency.log", "a") as f:
        while True:
            now = datetime.datetime.now()
            if (now.second == 15) or (now.second == 35) or (now.second == 55):
                frequency = fcount.get_freq()
                if (len(sys.argv) == 3):
                    regs = fgen.set_freq(frequency/1e6, float(eval(sys.argv[2])))              
                now = datetime.datetime.now()

            sys.stdout.write("frequency: " + str(frequency) + " Hz  Time: " + str(now.second))
            f.write("%d\t%s\t%.3f\n" % (time.time(), datetime.datetime.now().isoformat(), frequency))

            sys.stdout.flush()
            time.sleep(0.9)
except KeyboardInterrupt:
    sys.stdout.write("\r\n")
    sys.exit(0)
    f.close()
