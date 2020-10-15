#!/usr/bin/env node

// we are using mpu9250
// require mpu9250
// install it with npm install

/*
  ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
 ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
 ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
  ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
       ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
 ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
  ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   imu.js
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      IMU informations, need filtering and calibration
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|
*/

'use strict';

var TOPIC = {"Time": 0.0, "Accelerometer": {}, "Gyroscope": {}, "Compass": {}};

var mpu9250 = require('mpu9250');

// These values were generated using calibrate_mag.js - you will want to create your own.
var MAG_CALIBRATION = {
  min: { x: -37.17578125, y: -38.375, z: -113.3125 },
  max: { x: 109.12890625, y: 103.1328125, z: 39.3125 },
  offset: { x: 35.9765625, y: 32.37890625, z: -37 },
  scale:
   { x: 1.5052063865007743,
     y: 1.5562303318058852,
     z: 1.442874692874693 }
};

// These values were generated using calibrate_gyro.js - you will want to create your own.
// NOTE: These are temperature dependent.
var GYRO_OFFSET = { x: 1.0859999999999999,
  y: -0.5146564885496187,
  z: 0.020839694656488557
};

// These values were generated using calibrate_accel.js - you will want to create your own.
var ACCEL_CALIBRATION =  {
   offset:
   { x: 0.04336690266927083,
     y: 0.064090576171875,
     z: 0.0240582275390625 },
  scale:
   { x: [ -1.0019303385416667, 0.9870353190104166 ],
     y: [ -0.9752742513020833, 1.02643310546875 ],
     z: [ -0.9693855794270834, 1.0298063151041668 ] }
};

// Instantiate and initialize.
var mpu = new mpu9250({
    // i2c path (default is '/dev/i2c-1')
    device: '/dev/i2c-2',

    // Enable/Disable debug mode (default false)
    DEBUG: true,

    // Set the Gyroscope sensitivity (default 0), where:
    //      0 => 250 degrees / second
    //      1 => 500 degrees / second
    //      2 => 1000 degrees / second
    //      3 => 2000 degrees / second
    GYRO_FS: 0,

    // Set the Accelerometer sensitivity (default 2), where:
    //      0 => +/- 2 g
    //      1 => +/- 4 g
    //      2 => +/- 8 g
    //      3 => +/- 16 g
    ACCEL_FS: 0,

    scaleValues: true,

    UpMagneto: true,

    magCalibration: MAG_CALIBRATION,

    gyroBiasOffset: GYRO_OFFSET,

    accelCalibration: ACCEL_CALIBRATION
});

if (mpu.initialize()) {


    var amqp = require('amqplib/callback_api');

    amqp.connect('amqp://localhost', function(err, conn) {
      conn.createChannel(function(err, ch) {
        var ex = 'imu';
        ch.assertExchange(ex, 'fanout', {durable: false});

        setInterval(function() { ch.publish(ex, '', new Buffer(JSON.stringify(TOPIC)));}, 50);
      });
    });


    var ACCEL_NAME = 'Accel (g)';
    var GYRO_NAME = 'Gyro (°/sec)';
    var MAG_NAME = 'Mag (uT)';
    var HEADING_NAME = 'Heading (°)';
    var stats = new Stats([ACCEL_NAME, GYRO_NAME, MAG_NAME, HEADING_NAME], 1000);

    //console.log('\n   Time     Accel.x  Accel.y  Accel.z  Gyro.x   Gyro.y   Gyro.z   Mag.x   Mag.y   Mag.z    Temp(°C) heading(°)');
    var cnt = 0;
    var lastMag = [0, 0, 0];
    setInterval(function() {
        var start = new Date().getTime();
        var m9;
        // Only get the magnetometer values every 100Hz
        var getMag = cnt++ % 2;
        if (getMag) {
            m9 = mpu.getMotion6().concat(lastMag);
        } else {
            m9 = mpu.getMotion9();
            lastMag = [m9[6], m9[7], m9[8]];
        }
        var end = new Date().getTime();
        var t = (end - start) / 1000;

        // Make the numbers pretty
        TOPIC["Accelerometer"]  = {"x": m9[0], "y": m9[1], "z": m9[2]};
        TOPIC["Gyroscope"]      = {"x": m9[3], "y": m9[4], "z": m9[5]};
        TOPIC["Compass"]        = {"x": m9[6], "y": m9[7], "z": m9[8]};
        TOPIC["Heading"]        = calcHeading(m9[6], m9[7]);
        TOPIC["Temperature"]    = mpu.getTemperatureCelsiusDigital();
        TOPIC["Time"]           = t;

        var str = '';
        for (var i=0; i < m9.length; i++) {
            str += p(m9[i]);
        }

        stats.add(ACCEL_NAME, m9[0], m9[1], m9[2]);
        stats.add(GYRO_NAME, m9[3], m9[4], m9[5]);
        if (getMag) {
            stats.add(MAG_NAME, m9[6], m9[7], m9[8]);
            stats.addValue(HEADING_NAME, calcHeading(m9[6], m9[7]));
        }

        //process.stdout.write(p(t) + str + p(mpu.getTemperatureCelsiusDigital()) + p(calcHeading(m9[6], m9[7])) + '  \r');
        //process.stdout.write(JSON.stringify(TOPIC)+ '  \r');

    }, 5);
}

function p(num) {
    if (num === undefined) {
        return '       ';
    }
    var str = num.toFixed(3);
    while (str.length <= 7) {
        str = ' ' + str;
    }
    return str + ' ';
}

function calcHeading(x, y) {
    var heading = Math.atan2(y, x) * 180 / Math.PI;

    if (heading < -180) {
        heading += 360;
    } else if (heading > 180) {
        heading -= 360;
    }

    return heading;
}


/**
 * Calculate Statistics
 * @param {[string]} names The names of the vectors.
 */
function Stats(vectorNames, numStats) {

    this.vectorNames = vectorNames;
    this.numStats = numStats;
    this.vectors = {};
    this.done = false;

    for (var i = 0; i < vectorNames.length; i += 1) {
        var name = vectorNames[i];
        this.vectors[name] = {
            x: [],
            y: [],
            z: [],
            pos: 0
        };
    }

    function exitHandler(options, err) {
        if (err) {
            console.log(err.stack);
        } else {
            this.printStats();
        }
        if (options.exit) {
            var exit = process.exit;
            exit();
        }
    }

    // do something when app is closing
    process.on('exit', exitHandler.bind(this, {cleanup: true}));

    // catches ctrl+c event
    process.on('SIGINT', exitHandler.bind(this, {exit: true}));

    // catches uncaught exceptions
    process.on('uncaughtException', exitHandler.bind(this, {exit: true}));
}
Stats.prototype.add = function(vectorName, x, y, z) {
    var v = this.vectors[vectorName];
    var len = v.x.length;
    if (v.pos >= this.numStats) {
        v.pos = 0;
    } else {
        v.pos += 1;
    }
    v.x[v.pos] = x;
    v.y[v.pos] = y;
    v.z[v.pos] = z;
};
Stats.prototype.addValue = function(vectorName, x) {
    var v = this.vectors[vectorName];
    v.isValue = true;
    if (v.pos >= this.numStats) {
        v.pos = 0;
    } else {
        v.pos += 1;
    }
    v.x[v.pos] = x;
};
Stats.prototype.printStats = function () {
    if (this.done) return;
    this.done = true;

    console.log('\n\n\nStatistics:');
    console.log('           average   std.dev.  num.same.values');
    for (var i = 0; i < this.vectorNames.length; i += 1) {
        var name = this.vectorNames[i];
        var v = this.vectors[name];
        console.log(name + ':');
        console.log(' -> x: ', average(v.x).toFixed(5), standardDeviation(v.x).toFixed(5), numSameValues(v.x));
        if (!v.isValue) {
            console.log(' -> y: ', average(v.y).toFixed(5), standardDeviation(v.y).toFixed(5), numSameValues(v.y));
            console.log(' -> z: ', average(v.z).toFixed(5), standardDeviation(v.z).toFixed(5), numSameValues(v.z));
        }
        console.log(' -> num samples: ', v.x.length);
        console.log();
    }

    function standardDeviation(values) {
        var avg = average(values);

        var squareDiffs = values.map(function (value) {
            var diff = value - avg;
            var sqrDiff = diff * diff;
            return sqrDiff;
        });

        var avgSquareDiff = average(squareDiffs);

        var stdDev = Math.sqrt(avgSquareDiff);
        return stdDev;
    }

    function average(values) {
        var sumData = values.reduce(function (sum, value) {
            return sum + value;
        }, 0);

        var avg = sumData / values.length;
        return avg;
    }

    function numSameValues(values) {
        var same = 0;
        var lastVal = NaN;
        values.forEach(function(val) {
            if (val === lastVal) {
                same += 1;
            }
            lastVal = val;
        });
        return same;
    }
};
