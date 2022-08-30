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
import time

from periphery import GPIO

from threading import *


class Sensor_init(Exception):
    pass


from enum import Enum
class CronosStatus(Enum):
    NONE = 0
    INIT = 1
    BUFFER = 2
    SAVING = 3
    SAVED = 4

class Cronos(object):
    """docstring for cronos."""

    def __init__(self, url):
        super(Cronos, self).__init__()
        self.url = url
        self.camera_url = url

        self.camera_status = CronosStatus.NONE
        self.camera_status_dict = {}
        self.last_update = 0 # cas posledniho behu funkce update

        self.record = {'format': 'h264', 'device': 'sda1'}

        self.config()

    def do_post(self, control, payload = None):
        print("Camera: Send command: {}".format(control))
        post = requests.post(self.camera_url+control, json = payload)
        print(post.status_code)

        if post.reason == "OK":
            print("Camera: Request is accepted")
        else:
            print("Camera: Request error: ", post)
        return post

    def do_get(self, control):
        get = requests.get(self.camera_url + control)
        print(get.status_code, get.json())
        return get

    def config(self):
        print("Camera: Disable camera backlight LCD to save power and reduce temperature")
        self.do_post('/control/p', payload={'backlightEnabled': False})

        print("Camera: Stop previous recording and flush recorded data")
        self.do_post('/control/stopRecording')
        time.sleep(0.1)
        self.do_post('/control/flushRecording')

        print("Camera: Update AOI")
        self.do_post('/control/p', payload = {'resolution': {'hRes': 928, 'vRes': 928, 'hOffset': 176, 'vOffset': 66}} )

        print("Camera: Update buffer length; cca 3s")
        self.do_post('/control/p', payload = {'recMaxFrames':4837} )

        print("Camera: Init text overlay (for HW trigger)")
        self.do_post('/control/p', payload = {'recTrigDelay':2418})  # This value is only informative (it works for HW trigger only)

        self.camera_status = CronosStatus.INIT

        time.sleep(0.5)
        self.start_recording()

    def save_buffer(self, filename, format = 'h264', device = 'mmcblk1p1'):

        post = self.do_post('/control/startFilesave',
                        payload = {'format': format, 'device': device, 'filename': filename })

        if post.reason == "OK":
            print("Camera: Saving the video")
            self.camera_status = CronosStatus.SAVING

        else:
            print("Camera: Unable to save the video")
            print(post)
            print(post.status_code)

    def save_video(self, filename):

        if self.get_videoState() != 'filesave':
            time.sleep(0.05)
            get = self.do_get('/control/p/state').json()

            if get == {'state': 'recording'}:
                time.sleep(0.01)
                post = self.do_post('/control/stopRecording')
                print("Camera: Stopping camera recording")

            elif get == {'state': 'idle'}:
                print("Camera: Camera is already idle")

            else:
                print(post.json())

            time.sleep(0.05)
            get = self.do_get('/control/p/state').json()    ## verify that recording is really stopped

            if get == {'state': 'recording'}:
                time.sleep(0.02)
                post = self.do_post('/control/stopRecording')
                print("Camera does not stop recording: Stopping camera recording again")
                time.sleep(0.1)
            self.save_buffer(filename, format = self.record['format'], device = self.record['device'])

        else:
            print("Camera is already saving the video. Do not disturb!")

    def get_videoState(self, save = True):
        get = self.do_get('/control/p/videoState').json()
        if save:
            print(get)
            self.camera_status_dict['videoState'] = get.get('videoState', None)
        return get.get('videoState', None)

    def start_recording(self):
        print("Camera: Start recording")
        return self.do_post('/control/startRecording', payload = {'recMode': 'normal'})

    def periodic_update(self, min_period = 1):
        if self.last_update+min_period < time.time():
            self.last_update = time.time()
            print("Camera: Update loop started")

            if self.camera_status == CronosStatus.SAVING:
                state = self.get_videoState()
                if state != 'filesave':
                    self.start_recording()



## Zatim priprava na obsluhu kamery ve vlastnim vlaknu..

# def camera_thread_function():
#     camera_url = "http://chronos.lan"
#     camera = Cronos(camera_url)
#
#
# CamThread = Thread(target = camera_thread_function)
# CamThread.setDaemon(True)


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

        # print("Disable camera backlight LCD to save power and reduce temperature")
        # post = requests.post(camera_url + '/control/p',
        #                      json={'backlightEnabled': False})
        # if post.reason == "OK":
        #     print("Camera LCD backlight sucesfully Disabled")
        # else:
        #     print(post)
        #
        # post = requests.post(camera_url+'/control/stopRecording')
        # if post.reason == "OK":
        #     print("Recording stopped.")
        # else:
        #     print(post)
        #
        # post = requests.post(camera_url+'/control/flushRecording')
        # if post.reason == "OK":
        #     print("Recording buffer flushed.")
        # else:
        #     print(post)
        #
        # post = requests.post(camera_url+'/control/p', json = {'resolution': {'hRes': 928, 'vRes': 928, 'hOffset': 176, 'vOffset': 66}})
        # if post.reason == "OK":
        #     print("Video resolution is set.")
        # else:
        #     print(post)
        #
        # post = requests.post(camera_url+'/control/p', json = {'recMaxFrames':4837})  # cca 3 s
        # if post.reason == "OK":
        #     print("Video Recording lenght is set.")
        # else:
        #     print(post)
        #
        # post = requests.post(camera_url+'/control/p', json = {'recTrigDelay':2418})  # This value is only informative (it works for HW trigger only)
        # if post.reason == "OK":
        #     print("Text overlay is inicialized.")
        # else:
        #     print(post)

        camera = Cronos(camera_url)




#### Sensor Configuration ###########################################

        sensor = cfg.get_device("lighting")
        sensor.route()

        # Open GPIO 960 as interrupt input from LIGHTNING01A sensor.
        interrupt = GPIO(960, "in")
        interrupt.edge = "rising"

        lightning_timeout = 5

        time.sleep(0.5)
        sensor.reset()

        time.sleep(0.5)

        print("Calibrating RCO")
        sensor.calib_rco()

        print("Configuring sensor registers")
        sensor.setWDTH(16)
        sensor.setNoiseFloor(16)
        sensor.setIndoor(False)
        sensor.setSpikeRejection(10)
        sensor.setMaskDist(True)

        time.sleep(0.5)

        #### Data Logging ###################################################

        while True:

            print("Waiting for lightning interrupt.. ")

            if interrupt.read() or interrupt.poll(
                    lightning_timeout
            ):  #wait to interrupt from sensor or fail to timeout
                current_time = datetime.datetime.now()  # save time of event
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

                video_filename = current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + "-lightning"

                camera.save_video(video_filename)


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
                print("Interrupt signal line is in {}".format(interrupt.read()))
                camera.periodic_update()

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
