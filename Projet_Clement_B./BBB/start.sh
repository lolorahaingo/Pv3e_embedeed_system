#!/bin/bash

# only Publisher node
python ./sources/GPS.py &
/usr/bin/node ./sources/CAN.js &
/usr/bin/node ./sources/imu.js &

# Publisher and Subscriber
python ./sources/telemetry.py &

# Only Subscriber
python ./sources/sd_logger.py &

# let's start the Nextion in last because of shitty thread
python ./sources/Nextion.py &