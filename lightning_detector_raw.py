#!/usr/bin/python3

#%load_ext autoreload
#%autoreload 2

import time
import datetime
import sys
import os
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

        self.record = {'format': 'y12b', 'device': 'sda1'}

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
                print("Camera: Camera recording has not been stoped")

            elif get == {'state': 'idle'}:
                print("Camera: Camera is already idle, saving the video")
                self.save_buffer(filename, format = self.record['format'], device = self.record['device'])

            else:
                print(post.json())
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
        self.camera_status = CronosStatus.INIT
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

camera_url = "http://chronos.lan"

while True:
    try:
        camera = Cronos(camera_url)

#### Sensor Configuration ###########################################

        interrupt = GPIO(960, "in")
        interrupt.edge = "rising"

        lightning_timeout = 5

        time.sleep(0.5)

        #### Data Logging ###################################################

        while True:

            print("Waiting for lightning interrupt.. ")

            if interrupt.read() or interrupt.poll(
                    lightning_timeout
            ):  #wait to interrupt from sensor or fail to timeout
                current_time = datetime.datetime.now()  # save time of event
                time.sleep(0.02)
                print(
                    "---------------------------------------------------------"
                )
                print("Event {}".format(
                    datetime.datetime.now().isoformat(' ')))
                time.sleep(1.6)

                video_filename = current_time.strftime("%Y-%m-%d-%H-%M-%S.%f") + "-lightning"

                camera.save_video(video_filename)

            else:
                print(
                    "Lightning is not detected in the last {} minutes".format(
                        lightning_timeout / 60.0))
                print("Interrupt signal line is in {}".format(interrupt.read()))
                camera.periodic_update()

    except IOError as e:
        print("Error: " + str(e))
        sys.stdout.write("\r\nCommunication Error\r\n")
        time.sleep(2)

    except Sensor_init:
        sys.stdout.write("\r\nReinicialising the sensor!\r\n")
        time.sleep(2)

    except KeyboardInterrupt:
        interrupt.close()
        sys.exit(0)
