#!/usr/bin/env python

#   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
#  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
#  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
#   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
#        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
#  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
#   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   computations.py
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      Place for computations
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|
# Our imports
import threading
import logging
import os

import json
import numpy as np
import scipy
import math

import time

from server_utils import Subscriber, Publisher

# Logger config
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='[%d/%m/%y - %H:%M:%S]', level=logging.DEBUG)

class Computations(object):
    """Class for computations"""

    def __init__(self):
        """Calculating EVERYTHING"""
        # Deceleration
        self.canSub = Subscriber("can")
        self.bShouldComputeDeceleration = False
        self.bShouldComputeInjector = True

        self.logger = logging.getLogger(__name__)

        self.data = {}
        self.publisher = Publisher("computations")
        self.publisher.data = json.dumps(self.data)

    def run(self):
        """Run the task"""
        threadCan = threading.Thread(target=self.canSub.run)
        threadCan.daemon = True

    def decelerationComputations(self):
        """Start this to calculate a second order polynomial to approximate external forces."""
        canData = self.canSub.data
        while self.bShouldComputeDeceleration:
            speed_values, time_values = [], []
            if canData:
                if "PE1" in canData:
                    if "RPM" in canData["PE1"]:
                        # Accumulate speed values
                        while len(speed_values) < 10:
                            speed_values.append(canData["PE1"]["RPM"])
                            time_values.append(time.time())
                        polynomial = scipy.polyfit(np.array(time_values), np.array(speed_values), 2)
                        self.data["friction"] = str(polynomial[0]) + "*x**2 + " + str(polynomial[1]) + "*x + " + str(polynomial)

    def leewayComputations(self):
        """Compute leeway on the three wheels"""
        pass

    def computeInjectedMass(self):
        """Compute the total mass injected in that shit"""
        canData = self.canSub.data
        while self.bShouldComputeInjector:
            if canData:
                if "PE1" in canData and "PE6" in canData and "PE2" in canData:
                    if "Fuel Open Time" in canData["PE1"] and "Battery Level" in canData["PE6"] and "Pressure" in canData["PE2"]:
                        pressure, voltage, injection_time = canData["PE2"]["Pressure"], canData["PE6"]["Battery Level"], canData["PE1"]["Fuel Open Time"]
                        mass = self.injectorModel(pressure, voltage, injection_time)
                        self.data["mass"] = mass

    def injectorModel(self, pressure, voltage, injection_time):
        """Added by R."""
        # pressure, voltage and injection_time from subscribing to can for : ... [PE5](Battery Level) and [PE1](Fuel Open Time)
        return ((0.7717 * math.sqrt(pressure / 5)) - (-0.1402 * voltage + 2.9072) * injection_time)


if __name__ == "__main__":
    computations = Computations()
    computations.run()
