#!/usr/bin/env python

#   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
#  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
#  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
#   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
#        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
#  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
#   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   logger.py
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      Place for logging
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|

import os
import logging
import threading
import json
import time

from server_utils import Subscriber

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='[%d/%m/%y - %H:%M:%S]', level=logging.DEBUG)

class SDLogger:

    FOLDER_LOC = os.path.join(os.path.dirname(__file__), "log")
    FILE_LOC = os.path.join(FOLDER_LOC, "pv3e.txt")
    BASENAME = 'pv3e'
    REFRESH_RATE = 0.5 # in seconds

    def __init__(self):
        self.filename = SDLogger.BASENAME
        self.filepath = ""

        self.data_to_write = {}

        self.bShouldRun = True
        self.bShouldWrite = True
        self.bShouldCollect = True

        self.canSub = Subscriber("can")
        self.gpsSub = Subscriber("gps")
        self.imuSub = Subscriber("imu")

        self.logger = logging.getLogger(__file__)

    def run(self):
        """Main thread for SDLogger"""
        self.filepath = self.getFilePath(self.filename)

        threadCan = threading.Thread(target=self.canSub.run)
        threadCan.daemon = True

        threadGPS = threading.Thread(target=self.gpsSub.run)
        threadGPS.daemon = True

        threadIMU = threading.Thread(target=self.imuSub.run)
        threadIMU.daemon = True

        threadCollect = threading.Thread(target=self.collectData)
        threadCollect.daemon = True

        threadWrite = threading.Thread(target=self.thread_write)
        threadWrite.daemon = True

        self.logger.info("Thread created, starting...")

        threadCan.start()
        threadGPS.start()
        threadIMU.start()
        threadCollect.start()
        threadWrite.start()

        self.logger.info("Thread started, serving forever")

        while self.bShouldRun:
            if not threadCollect.isAlive():
                threadCollect = threading.Thread(target=self.collectData)
                threadCollect.daemon = True
                threadCollect.start()
            if not threadWrite.isAlive():
                threadWrite = threading.Thread(target=self.thread_write)
                threadWrite.daemon = True
                threadWrite.start()

    def getFilePath(self, basename):
        """Getting full file path from a base name"""
        counter = 1
        while os.path.isfile(self.pathBuilder(str(basename) + str(counter))):
            counter += 1
        return self.pathBuilder(str(basename) + str(counter))

    def collectData(self):
        if self.canSub.data:
            self.data_to_write["CAN"] = self.canSub.data
        if self.gpsSub.data:
            self.data_to_write["GPS"] = self.gpsSub.data
        if self.imuSub.data:
            self.data_to_write["IMU"] = self.imuSub.data

    def thread_write(self):
        while self.bShouldWrite:
            self.writeData(self.data_to_write)

    def thread_collect(self):
        while self.bShouldCollect:
            self.collectData()

    def writeData(self, dict):
        # TODO: Enumerate critical data to log on sd card.
        # We would go for everything
        try:
            self.data_to_write["Timestamp"] = float(time.time())
            data = json.dumps(self.data_to_write)
            with open(self.filepath, "a") as logfile:
                logfile.write(data + "\r\n")
        except Exception as e:
            print(e)
            self.logger.error(e)
        time.sleep(SDLogger.REFRESH_RATE)

    def pathBuilder(self, name):
        """Forcing log file"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "log", str(name) + ".csv")


if __name__ == "__main__":
    sdLogger = SDLogger()
    sdLogger.run()
