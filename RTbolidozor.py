#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# sudo apt-get install python-websocket
#

import sys
import time
import urllib2
import requests
from mlabutils import ejson


exitapp = False
met = False
metData = u""
midiTime = 0

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
        print station
        print observatory
        while True:
            try:
                pipe = sys.stdin.readline()
                if "met" in pipe:
                    print "Meteor from radio-observer pipe:", pipe
                    payload = {'station': station, 'observatory': observatory}
                    print payload
                    r = requests.get('http://rtbolidozor.astro.cz/event', params=payload, timeout=1)
                else:
                    time.sleep(0.5)
            except Exception, e:
                print e
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        raise 0
