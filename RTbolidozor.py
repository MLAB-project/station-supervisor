#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# sudo apt-get install python-websocket
#

import sys
import time
import datetime
import websocket
import binascii
from mlabutils import ejson


exitapp = False
met = False
metData = u""
midiTime = 0

class mWS(websocket.WebSocket):
    def on_connect(self):
        print "connected"
        self.connected=True

    def on_open(self):
        self.send("ahoj")

    def on_message(self, data):
        print data

    def on_ping(self):
        print 'I was pinged'

    def on_pong(self):
        print 'I was ponged'

    def on_close(self):
        print 'Socket closed.'

    def setStation(self, config):
        self.config=config
        self.send("$stanice;"+str(self.config)+";")

    def sendEvent(self, pipe = None, station = "null"):
        self.send("$event;"+station+";"+str(pipe)+";")

    def sendInfo(self, info = None):
        self.send("$info;"+str(info)+";")

def main():
    arg = sys.argv
    if len(arg) != 2:
        print "Usage: dataUpload [radio-observer configFile]"
        sys.exit(1)
    else:
        configFile = arg[1]
        parser = ejson.Parser()
        config = parser.parse_file(configFile)
        station = config["configurations"][0]["children"][0]["origin"]
        observatory = config["storage_username"]
        while 1:
            try:
                client = mWS()
                client.connect("ws://rtbolidozor.astro.cz/ws")
                client.setStation('{"name":"%s","ident":"%s"}' %(station, observatory))
                client.sendEvent("start", station)
                while 1:
                    #print "New line received"
                    pipe = sys.stdin.readline()
                    if "met" in pipe:
                        print "Meteor from radio-observer pipe:", pipe+";"+station
                        client.sendEvent(pipe, station)
                    else:
                        time.sleep(0.5)
            except Exception, e:
                print e
                time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise 0

