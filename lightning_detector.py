#!/usr/bin/python3

#%load_ext autoreload
#%autoreload 2

import time
import datetime
import sys
import os
from pymlab import config
from mlabutils import ejson
import requests

from periphery import GPIO


class Sensor_init(Exception):
    pass


#### Script Arguments ###############################################

parser = ejson.Parser()

if len(sys.argv) != 3:
    sys.stderr.write(
        "Invalid number of arguments. Missing path to a config files!\n")
    sys.stderr.write("Usage: %s config_file.json i2c_bus_config.py\n" %
                     (sys.argv[0], ))
    sys.exit(1)

value = parser.parse_file(sys.argv[1])

# path to metadata output directory
path = value['metadata_path']

# required frequency
carrier_freq = value['receiver_carrier']  # Beacon frequency

# station name
StationName = value['origin']

camera_url = "http://chronos.lan"

while True:

    cfg = config.Config()
    cfg.load_file(sys.argv[2])

    now = datetime.datetime.now()
    filename = path + time.strftime(
        "%Y%m%d%H", time.gmtime()) + "0000_" + StationName + "_lightning.csv"
    if not os.path.exists(filename):
        with open(filename, "a") as f:
            f.write(
                '#timestamp,INTer,WDTH,TUN_CAP,Indoor_Mode,Noise_floor,Spike_rejction,Single_energy,Mask_disturbance,Distance\n'
            )

    try:

        # disable camera backlight LCD to save power and reduce temperature
        post = requests.post(camera_url + '/control/p',
                             json={'backlightEnabled': False})
        if post.reason == "OK":
            print("Camera LCD backlight sucesfully Disabled")
        else:
            print(post)

#### Sensor Configuration ###########################################

        sensor = cfg.get_device("lighting")
        sensor.route()

        # Open GPIO 960 as interrupt input from LIGHTNING01A sensor.
        interrupt = GPIO(960, "in")
        interrupt.edge = "rising"

        lightning_timeout = 60

        time.sleep(0.5)
        sensor.reset()

        time.sleep(0.5)

        print("Calibrating RCO")
        sensor.calib_rco()

        print("Configuring sensor registers")
        sensor.setWDTH(1)
        sensor.setNoiseFloor(6)
        sensor.setIndoor(False)
        sensor.setSpikeRejection(0)
        sensor.setMaskDist(False)

        time.sleep(0.5)

        #### Data Logging ###################################################

        while True:

            print("Waiting for lightning interrupt.. ")

            if interrupt.read() or interrupt.poll(
                    lightning_timeout
            ):  #wait to interrupt from sensor or fail to timeout
                current_time = datetime.now()  # save time of event
                time.sleep(
                    0.02
                )  #After the signal IRQ goes high the external unit should wait 2ms before reading the interrupt register.
                event_time = time.time()
                distance = sensor.getDistance()
                energy = sensor.getSingleEnergy()
                interrupts = sensor.getInterrupts()
                wdth = sensor.getWDTH()
                tun_cap = sensor.getTUN_CAP()
                #        print("power: ", sensor.getPowerStatus())
                indoor = sensor.getIndoor()
                noise_floor = 0  # sensor.getNoiseFloor()
                spike_rejection = sensor.getSpikeRejection()
                mask_dist = sensor.getMaskDist()

                with open(filename, "a") as f:
                    f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {} \n".format(
                        event_time, interrupts, wdth, tun_cap, indoor,
                        noise_floor, spike_rejection, energy, mask_dist,
                        distance))

                print(
                    "---------------------------------------------------------"
                )
                print("Event {}".format(
                    datetime.datetime.now().isoformat(' ')))
                print("INTer:{}".format(interrupts))
                print("WDTH: 0b{:04b}".format(wdth))
                print("TUN_CAP: {}".format(tun_cap))
                #        print("power: ", sensor.getPowerStatus())
                print("Indoor Mode: {}".format(indoor))
                print("Noise floor is {} uVrms".format(noise_floor))
                print("Spike rejection 0b{:04b}".format(spike_rejection))
                print("Single Energy {}".format(energy))
                print("Mask disturbance: {}".format(mask_dist))
                print("Storm is {:02d} km away".format(distance))
                time.sleep(1)

                filename = current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + "-lightning"

                post = requests.get(camera_url + '/control/p/videoState')
                if post.json() != {'videoState': 'filesave'}:

                    post = requests.get(camera_url + '/control/p/state')
                    if post.json() == {'state': 'recording'}:
                        post = requests.post(camera_url +
                                             '/control/stopRecording')
                        print("Stopping camera recording")

                    elif post.json() == {'state': 'idle'}:
                        print("Camera is already idle")

                    else:
                        print(post.json())

                    post = requests.post(camera_url + '/control/startFilesave',
                                         json={
                                             'format': 'h264',
                                             'device': 'mmcblk1p1',
                                             'filename': filename
                                         })
                    if post.reason == "OK":
                        print("Saving the video")
                    else:
                        print("Unable to save the video")
                        print(post)
                else:
                    print(
                        "Camera is already saving the video. Do not disturb!")

                while (interrupt.read()):
                    print("!! Interrupt signal is still True after readout !!")
                    interrupts = sensor.getInterrupts()
                    print("INTer:{}".format(interrupts))
                    time.sleep(1)
                    raise Sensor_init("Sensor is stalled!")

            else:
                print(
                    "Lightning is not detected in the last {} minutes".format(
                        lightning_timeout / 60.0))
                print("Interrupt signal line is in {}".format(
                    interrupt.read()))

    except IOError as e:
        print("Error: " + str(e))
        sys.stdout.write("\r\n************ I2C Error\r\n")
        time.sleep(2)

    except Sensor_init:
        sys.stdout.write("\r\nReinicialising the sensor!\r\n")
        time.sleep(2)

    except KeyboardInterrupt:
        interrupt.close()
        sys.exit(0)
