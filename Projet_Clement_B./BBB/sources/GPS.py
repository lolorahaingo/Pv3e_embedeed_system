#!/usr/bin/env python

#   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
#  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
#  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
#   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
#        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
#  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
#   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   gps.py
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      GPS publisher
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|

import serial
import json
import logging
import os

import threading

import datetime

import pynmea2

from server_utils import Publisher
from PORTNAMES import PORT_GPS

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='[%d/%m/%y - %H:%M:%S]', level=logging.DEBUG)

class GPS(object):
    """NEO 6M GPS handling"""
    MESSAGE_QUALITY = {0: "invalid", 1: "GPS fix (SPS)", 2: "DGPS fix", 3: "PPS fix", 4: "Real Time Kinematic", 5: "Float RTK", 6: "estimated (dead reckoning) (2.3 feature)", 7: "Manual input mode", 8: "Simulation mode"}

    def __init__(self, port, baudrate=9600):
        """Cool GPS parser"""
        self.con = None
        while self.con is None:
            try:
                self.con = serial.Serial(port, baudrate=baudrate)
            except Exception as e:
                print(e)

        self.bShouldRead = True

        self.data = {"timestamp": datetime.datetime.now().strftime("%H:%M:%S"), "location": (0.0, 0.0), "speed": 0.0, "heading": 0.0, "altitude": 0.0, "satnumber": 0}
        self.publisher = Publisher("gps")
        self.publisher.data = json.dumps(self.data)

        self.logger = logging.getLogger(__file__)

    def run(self):
        threadNMEA = threading.Thread(target=self.parseNMEA)
        threadNMEA.daemon = True

        threadPublish = threading.Thread(target=self.publisher.run)
        threadPublish.daemon = True

        threadNMEA.start()
        threadPublish.start()

    def parseNMEA(self):
        streamreader = pynmea2.NMEAStreamReader()
        while self.bShouldRead:
            try:
                data = self.con.read()
                for msg in streamreader.next(data):

                    if getattr(msg, "timestamp", False):
                        self.data["timestamp"] = msg.timestamp.strftime("%H:%M:%S")
                        print("Data is " + str(self.data["timestamp"]))

                    if getattr(msg, "num_sats", False):
                        self.data["satnumber"] = msg.num_sats
                        print("Data is " + str(self.data["satnumber"]))

                    if (getattr(msg, "lat", False) and getattr(msg, "lon", False) and getattr(msg, "lat_dir", False) and getattr(msg, "lon_dir", False)):
                        parsed_lat, parsed_lon = msg.lat.split('.'), msg.lon.split('.')
                        self.data["location"] = (self.dms2dd(parsed_lat[0][:-2], parsed_lat[0][-2:] + "." + parsed_lat[1], 0.0, msg.lat_dir),
                                                 self.dms2dd(parsed_lon[0][:-2], parsed_lon[0][-2:] + "." + parsed_lon[1], 0.0, msg.lon_dir))
                        print("Data is " + str(self.data["location"]))

                    if getattr(msg, "gps_qual", False):
                        self.data["gps_qual"] = msg.gps_qual
                        print("Data is " + str(self.data["gps_qual"]))

                    if getattr(msg, "spd_over_grnd", False):
                        self.data["speed"] = msg.spd_over_grnd * 1.61 * 10.0
                        print("Data is " + str(self.data["speed"]))

                    if getattr(msg, "mag_track", False):
                        self.data["heading"] = msg.mag_track
                        print("Data is " + str(self.data["heading"]))

                    self.publisher.data = json.dumps(self.data)

            except Exception as e:
                print(e)
                self.logger.error(e)

    def dms2dd(self, degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd


def main():
    g = GPS(PORT_GPS)
    g.run()


if __name__ == '__main__':
    main()
