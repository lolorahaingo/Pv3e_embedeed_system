#!/usr/bin/env python

#   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
#  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
#  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
#   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
#        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
#  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
#   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   telemetry.py
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      Handling telemetry stuff
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|

import serial
import time
import json
import logging
import os

import threading

from PORTNAMES import PORT_TELEMETRY
from server_utils import Publisher, Subscriber

connection = None

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='[%d/%m/%y - %H:%M:%S]', level=logging.DEBUG)

#
# Telemetry class
#
class Telemetry(object):

    def __init__(self, port, baudrate=57600, interval=0.5):
        """Telemetry class for calypso"""
        self.con = None
        while self.con is None:
            try:
                self.con = serial.Serial(port, baudrate=baudrate)
            except Exception as e:
                print(e)

        self.bShouldRun = True
        self.bShouldListen = True
        self.bShouldSend = True

        self.RXData = ""
        self.TXData = ""
        self.receivedCmd = ""
        self.publisher = Publisher("tel")

        self.collection = {}

        # subscribing to other components
        self.canSub = Subscriber("can")
        self.gpsSub = Subscriber("gps")
        self.imuSub = Subscriber("imu")

        self.interval = interval

        self.logger = logging.getLogger(__file__)

    def run(self):
        threadCollect = threading.Thread(target=self.collectData)
        threadCollect.daemon = True

        threadCan = threading.Thread(target=self.canSub.run)
        threadCan.daemon = True

        threadGPS = threading.Thread(target=self.gpsSub.run)
        threadGPS.daemon = True

        threadIMU = threading.Thread(target=self.imuSub.run)
        threadIMU.daemon = True

        threadRX = threading.Thread(target=self.thread_receive)
        threadRX.daemon = True

        threadTX = threading.Thread(target=self.thread_send)
        threadTX.daemon = True

        threadPublish = threading.Thread(target=self.publisher.run)
        threadPublish.daemon = True

        print("Starting threads")

        threadRX.start()
        threadTX.start()

        print("Starting publisher")

        threadPublish.start()

        print("Starting subscriber")

        threadCan.start()
        threadGPS.start()
        threadIMU.start()

        # TODO: this is not correct of course
        while self.bShouldRun:
            if not threadRX.isAlive():
                threadRX.start()
            if not threadTX.isAlive():
                threadTX.start()
            if not threadCan.isAlive():
                threadCan.start()
            if not threadGPS.isAlive():
                threadGPS.start()
            if not threadIMU.isAlive():
                threadIMU.start()

    def handleRX(self, cmd):
        self.receivedCmd = cmd
        stack = {}
        stack["warning"] = cmd
        self.publisher.msg = json.dumps(stack)

    def collectData(self):
        if self.canSub:
            self.collection["CAN"] = self.canSub.data
        if self.gpsSub:
            self.collection["GPS"] = self.gpsSub.data
        if self.imuSub:
            self.collection["IMU"] = self.imuSub.data

    def thread_receive(self):
        while self.bShouldListen:
            self.RXData = self.con.readline()
            self.handleRX(self.RXData)

    def thread_send(self):
        while self.bShouldSend:
            self.collectData()
            self.TXData = json.dumps(self.collection)
            print(self.TXData)
            try:
                self.con.write(self.TXData + "\r\n")
                time.sleep(self.interval)
            except Exception as e:
                print(e)
                self.logger.error(e)


def main():
    tel = Telemetry(PORT_TELEMETRY)
    tel.run()


if __name__ == '__main__':
    main()
