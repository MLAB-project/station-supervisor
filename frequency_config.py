import sys

# path to metadata output directory
path = "/home/odroid/Bolidozor/TEST-R0/data/"

# required frequency
carrier_freq = 143.05	# Beacon frequency
echo_freq = 0.0265	# hearing frequency
req_freq = (carrier_freq - echo_freq) * 2

# station name
StationName = "TEST-R0"