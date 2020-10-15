#!/usr/bin/env node
// Install with:  npm install
// https://github.com/sebi2k1/node-can
// https://elinux.org/ECE497_Car_CANBUS

/*
  ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
 ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
 ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
  ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
       ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
 ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
  ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   can.js
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      Can handling for calypso using an400_revC (see can/an400_revC.kcd for full review)
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|
*/
// We don't want to mess with non declared variables
"use strict";

// Required imports
var can = require('socketcan');
var fs = require("fs");

// Our topics to log
var TOPIC = {"PE1": {}, "PE2":{}, "PE3": {}, "PE4": {}, "PE5": {}, "PE6": {}};
// The extended CAN IDs of our topics we want to listen to.
var IDS = {"PE1" : 0x0CFFF048, "PE2": 0x0CFFF148, "PE5": 0x0CFFF448, "PE6": 0x0CFFF548};

// Starting the system channel. See the wiki for more info
var channel = can.createRawChannel("can0");

//This shit is broken need to fix it (maybe complex signals are not correctly handled)
//var network = can.parseNetworkDescription("can/an400_revC.kcd");
//var db_motor = new can.DatabaseService(channel, network.buses["Motor"]);

/*
MESSAGE TO HANDLE
PE1 : rpm, tps, fop, igniangle
PE2 : lambda
PE5 : frequency 2 (rpm tachi)
PE6 : battery level, coolant temp
*/

// Starting the channel can0
channel.start();
console.log("Starting channel");

// Ugly workaround
channel.addListener("onMessage", function(msg) {
  //TODO: Add analogInput <- Is this really
  switch (msg.id) {
     case IDS.PE1:
         TOPIC.PE1["RPM"]              =         ( msg.data[1] * 256 + msg.data[0]) * 1;
         TOPIC.PE1["TPS"]              = toSigned( msg.data[3] * 256 + msg.data[2]) * 0.1;
         TOPIC.PE1["Fuel Open Time"]   = toSigned( msg.data[5] * 256 + msg.data[4]) * 0.1;
         TOPIC.PE1["Ignition"]         = toSigned( msg.data[7] * 256 + msg.data[6]) * 0.1;
         break;
      case IDS.PE2:
         TOPIC.PE2["Pressure"]         = toSigned( msg.data[3] * 256 + msg.data[2]) * 0.01;
         TOPIC.PE2["Lambda"]           = toSigned( msg.data[5] * 256 + msg.data[4]) * 0.001;
         break;
      case IDS.PE5:
         var rpmTachi                  = toSigned( msg.data[3] * 256 + msg.data[2]) * 0.2;
         TOPIC.PE5["Frequency 2"]      = rpmTachi * 0.33923;
         break;
      case IDS.PE6:
         TOPIC.PE6["Battery Level"]    = toSigned( msg.data[1] * 256 + msg.data[0]) * 0.01;
         TOPIC.PE6["Coolant Temp"]     = toSigned( msg.data[5] * 256 + msg.data[4]) * 0.1;
         break;
  }
});

// Helper function to sign a 8 bits number.
function toSigned(i) {
  var result;
  if (i > 32767) {
    result = i - 65536;
  } else {
    result = i;
  }
  return result;
}

// Create a publisher via the MQTT broker
var amqp = require('amqplib/callback_api');
amqp.connect('amqp://localhost', function(_err, conn) {
  conn.createChannel(function(_err, ch) {
    var ex = 'can';
    ch.assertExchange(ex, 'fanout', {durable: false});

    setInterval(function() { ch.publish(ex, '', new Buffer(JSON.stringify(TOPIC)));}, 100);
  });
});
