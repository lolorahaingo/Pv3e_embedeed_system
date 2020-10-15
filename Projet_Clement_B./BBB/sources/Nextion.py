#!/usr/bin/env python

#   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
#  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
#  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
#   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
#        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
#  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
#   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   Nextion.py
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      Nextion wrappers for
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|

import serial
import time
import binascii
import logging
import os

import json

import threading

from PORTNAMES import PORT_NEXTION
from server_utils import Subscriber

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='[%d/%m/%y - %H:%M:%S]', level=logging.DEBUG)

class Nextion(object):

    Pages = {"Splash": 0, "main": 1, "can": 3, "gps": 2}

    def __init__(self, port, baudrate):
        self.con = None
        while self.con is None:
            try:
                self.con = serial.Serial(port, baudrate=baudrate)
            except Exception as e:
                print(e)

        self.bShouldUpdate = True
        self.bShouldRead = True
        self.data = {}

        self.time = time.time()

        self.page = 0

        self.lastTimeUpdate = time.time()
        self.lastGPSUpdate = time.time()
        self.lastCANUpdate = time.time()
        self.lastTELUpdate = time.time()

        # source of data
        self.canSub = Subscriber("can")
        self.gpsSub = Subscriber("gps")
        self.telSub = Subscriber("tel")

        self.logger = logging.getLogger(__file__)

    def run(self):
        self.sendCommand("page 0")
        self.sendCommand("page 1")
        self.page = 1

        threadCan = threading.Thread(target=self.canSub.run)
        threadCan.daemon = True

        threadGPS = threading.Thread(target=self.gpsSub.run)
        threadGPS.daemon = True

        threadTel = threading.Thread(target=self.telSub.run)
        threadTel.daemon = True

        threadUpdate = threading.Thread(target=self.update)
        # threadUpdate.daemon = True

        threadPage = threading.Thread(target=self.read)
        threadPage.daemon = True

        threadCan.start()
        threadGPS.start()
        threadTel.start()
        threadUpdate.start()
        threadPage.start()

    def read(self):
        while self.bShouldRead:
            try:
                result = self.readNextion().encode("hex").replace("ffffff", "")

                # updating page
                if result[0:2] == "66":
                    self.page = int(result[2:4], 16)

            except Exception as e:
                print(e)
                self.logger.error(e)

    def readNextion(self):
        eol = b'\xFF\xFF\xFF'
        line = bytearray()
        while True:
            c = self.con.read(1)
            if c:
                line += c
                if eol in line:
                    break
            else:
                break
        return bytes(line)

    def sendCommand(self, string):
        cmd_string = binascii.hexlify(string) + "FFFFFF"
        try:
            self.con.write(cmd_string.decode("hex"))
        except Exception as e:
            print(e)

    def closeConnection(self):
        if self.con.isOpen():
            self.con.close

    @staticmethod
    def cleanTime(t):
        return str(t) if (t >= 10) else "0" + str(t)

    @staticmethod
    def parseTime(sec):
        seconds = int((sec) % 60)
        minutes = int((sec / (60)) % 60)
        hours = int((sec / (3600)) % 24)

        return Nextion.cleanTime(hours) + ":" + Nextion.cleanTime(minutes) + ":" + Nextion.cleanTime(seconds)

    def update(self):
        """Updating Nextion screen"""
        # Maybe too complex :
        while self.bShouldUpdate:
            try:
                # time update
                if (time.time() - self.lastTimeUpdate) > 1:
                    parsedTime = Nextion.parseTime(time.time() - self.time)
                    self.sendCommand("totaltime.txt=\"" + str(parsedTime) + "\"")
                    self.lastTimeUpdate = time.time()

                self.updateGPS()
                self.updateCAN()
                self.updateTelemetry()
                
            except Exception as e:
                print("While " + str(e))
                self.logger.error(e)


    def updateCAN(self):
        # can update
        if (time.time() - self.lastCANUpdate) > 0.2:
            canData = self.canSub.data
            print("CANDATA (" + str(time.time()) + ") " + str(canData))
            if canData:
                canData = json.loads(canData)
                self.sendCommand("canicon.pic=" + str(4))
                if self.page == Nextion.Pages["main"]:
                    if "PE1" in canData:
                        if "RPM" in canData["PE1"]:
                            self.sendCommand("rpm.txt=\"" + str(int(canData["PE1"]["RPM"])) + "\"")
                            # Linear conversion for progressBar
                            scaledRPM = int(int(canData["PE1"]["RPM"]) * 100.0 / 5500.0)
                            self.sendCommand("mrpmbar.val=" + str(scaledRPM))
                    if "PE5" in canData:
                        if "Frequency 2" in canData["PE5"]:
                            # Adding RPM speed to waveform object using add function
                            self.sendCommand("speed.txt=\"" + str(round(canData["PE5"]["Frequency 2"])) + "\"")
                    if "PE6" in canData:
                        if "Coolant Temp" in canData["PE6"]:
                            self.sendCommand("coolant.txt=\"" + str(canData["PE6"]["Coolant Temp"]) + "\"")
                        if "Battery Level" in canData["PE6"]:
                            scaledBatteryLevel = int(int(canData["PE6"]["Battery Level"]) * 100.0 / 18.0)
                            print(scaledBatteryLevel)
                            self.sendCommand("voltprogress.val=" + str(scaledBatteryLevel))
                if self.page == Nextion.Pages["can"]:
                    if "PE1" in canData:
                        if "TPS" in canData["PE1"]:
                            self.sendCommand("tps.txt=\"" + str(canData["PE1"]["TPS"]) + "\"")
                        if "Ignition" in canData["PE1"]:
                            self.sendCommand("igniangle.txt=\"" + str(canData["PE1"]["Ignition"]) + "\"")
                        if "Fuel Open Time" in canData["PE1"]:
                            self.sendCommand("fop.txt=\"" + str(int(canData["PE1"]["Fuel Open Time"])) + "\"")
                    if "PE2" in canData:
                        if "Lambda" in canData["PE2"]:
                            lamb = float(1.0 / float(canData["PE2"]["Lambda"]))
                            self.sendCommand("lambda.txt=\"" + str(lamb) + "\"")
            else:
                self.sendCommand("canicon.pic=" + str(5))
            self.lastCANUpdate = time.time()

    def updateGPS(self):
        # gps update
        if (time.time() - self.lastGPSUpdate) > 1:
            gpsData = self.gpsSub.data
            print("GPSDATA (" + str(time.time()) + ") " + str(gpsData))
            if gpsData:
                gpsData = json.loads(gpsData)
                if self.page == Nextion.Pages["main"]:
                    if "speed" in gpsData:
                        self.sendCommand("add {},{},{}".format(15, 0, int(gpsData["speed"])))
                    if "location" in gpsData:
                        if gpsData["location"] != [0.0, 0.0]:
                            self.sendCommand("gpsicon.pic=" + str(6))
                        else:
                            self.sendCommand("gpsicon.pic=" + str(7))
                elif self.page == Nextion.Pages["gps"]:
                    if "heading" in gpsData:
                        self.sendCommand("heading.txt=\"" + str(gpsData["heading"]) + "\"")
                    if "altitude" in gpsData:
                        self.sendCommand("altitude.txt=\"" + str(gpsData["altitude"]) + "\"")
                    if "speed" in gpsData:
                        self.sendCommand("gpsspeed.txt=\"" + str(gpsData["speed"]) + "\"")
                    if "satnumber" in gpsData:
                        self.sendCommand("satnumber.txt=\"" + str(gpsData["satnumber"]) + "\"")
                    if "timestamp" in gpsData:
                        self.sendCommand("gpstime.txt=\"" + str(gpsData["timestamp"]) + "\"")
            else:
                self.sendCommand("gpsicon.pic=" + str(8))
            self.lastGPSUpdate = time.time()

    def updateTelemetry(self):
        # tel update
        if (time.time() - self.lastTELUpdate) > 3:
            teldata = self.telSub.data
            if teldata:
                teldata = json.loads(teldata)
                if "warning" in teldata:
                    if not ("+++" in teldata["warning"]):
                        self.sendCommand("warning.txt=\"" + str(teldata["warning"].replace("\r\n", "")) + "\"")
                        self.sendCommand("warning.bco=\"63488\"")
                    else:
                        self.sendCommand("warning.txt=\"\"")
                        self.sendCommand("warning.bco=\"0\"")
                    self.telSub.data = ""
            self.lastTELUpdate = time.time()


def main():
    n = Nextion(PORT_NEXTION, baudrate=115200)
    n.run()


if __name__ == '__main__':
    main()
