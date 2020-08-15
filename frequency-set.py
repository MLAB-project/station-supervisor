#!/usr/bin/python
#
# Sample of measuring and frequency correction with ACOUNTER02A

import time
import datetime
import sys
from pymlab import config
import os
from mlabutils import ejson
import numpy as np


#import logging
#logging.basicConfig(level=logging.DEBUG)

parser = ejson.Parser()

if len(sys.argv) != 3:
    sys.stderr.write("Invalid number of arguments. Missing path to a config files!\n")
    sys.stderr.write("Usage: %s config_file.json i2c_bus.cfg\n" % (sys.argv[0], ))
    sys.exit(1)

value = parser.parse_file(sys.argv[1])

# required frequency
carrier_freq = value['receiver_carrier']

print ("RSMS Station Local Oscillator Setup Utility \r\n")

cfg = config.Config()
cfg.load_file(sys.argv[2])

try:
    cfg.initialize()

    fgen = cfg.get_device("clkgen")
    fgen.route()
    fgen.recall_nvm()
    time.sleep(0.5)	# wait for complete reset of Si570
    fgen.set_freq(10.0, carrier_freq/1e6)

    print ("Local oscillator frequency set to Hz ", carrier_freq)

except IOError:
    sys.stdout.write("\r\n************ I2C Error\r\n")

