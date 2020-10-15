/*
   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########
#
# Script name:   window.js
# Created on:    09/03/2019
# Author:        raymas
#
# Purpose:      WebTelemetry handling
#
# History:      v0.1 creation of file
#
#
# |-----------------------------------------------------------------|
# | C O N F I D E N T I A L   D O   N O T   R E D I S T R I B U T E |
# |-----------------------------------------------------------------|
*/

// IMPORTS
const fs = require("fs");
const path = require("path");
const serialport = require('serialport');
serialport.parsers = {
  ByteLength: require('@serialport/parser-byte-length'),
  CCTalk: require('@serialport/parser-cctalk'),
  Delimiter: require('@serialport/parser-delimiter'),
  Readline: require('@serialport/parser-readline'),
  Ready: require('@serialport/parser-ready'),
  Regex: require('@serialport/parser-regex'),
}


//GLOBALS
var ALL_MESSAGES = {}
var count = 0;
var CARDS = ['Battery Level', 'Coolant Temp'];
var PORTS = {};

var FLOW = {}

var connection = null;
const parser = new serialport.parsers.Readline()

var filename = "pv3e";
var filetowrite = "default.txt";

// Main function
function main() {

  filetowrite = generateFileName(__dirname + path.sep + "log", filename, ".dat");
  console.log(filetowrite);

  serialport.list((err, ports) => {
    console.log('ports', ports);
    if (err) {
      document.getElementById('error').textContent = err.message
      console.log(err);
      return;
    } else {
      document.getElementById('error').textContent = ''
    }
    if (ports.length === 0) {
      document.getElementById('error').textContent = 'No ports discovered'
    }
    setInterval(function() {
      extractTelemetry();
    }, 1000);
  });


}


document.getElementById("portname").addEventListener('keypress', function(event) {
  //Enter key
  if (event.which == 13) {
    var portnm = document.getElementById('portname').value;
    console.log(portnm);
    if (connection === null) {
      connection = new serialport(portnm, {
        baudRate: 57600
      });
      connection.pipe(parser);
      parser.on('data', function(data) {
        FLOW = data;
        fs.appendFile(filetowrite, data, function(err) {
            if(err) {
                console.log(err);
            }
        });
      });
    } else {
      // TODO: kill the connection
    }
  }
});


document.getElementById("message").addEventListener('keypress', function(event) {
  //Enter key
  if (event.which == 13) {
    var message = document.getElementById('message').value;
    if (connection !== null) {
      connection.write(message + "\n");
      console.log("Message " + message + "Sent");
    }
  }
});



// Page loaded

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, {});
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems, {});
});


function generateJSON() {
  return "{\"CAN\": {\"PE1\": {\"RPM\":" + String(Math.random() * 5500) + ", \"Coolant Temp\":" + String(Math.random() * 100) + ",  \"Speed\":" + String(Math.random() * 40) + ",  \"Battery Level\":" + String(16.4) + ",  \"Lambda\":" + String(0.9) + "  } }, \"timestamp\":" + String(count++) + "}";
}


function generateFileName(filepath, filename, ext) {
  var counter = 0;
  var pseudopath = String(filepath) + String(path.sep) + String(filename) + String(counter) + String(ext);
  while (fs.existsSync(pseudopath)) {
    counter = counter + 1;
    pseudopath = String(filepath) + String(path.sep) + String(filename) + String(counter) + String(ext);
  };
  return pseudopath;
}

function extractTelemetry() {
  try {
    var datas = JSON.parse(FLOW);
  } catch(e) {
    console.log("No data");
    return;
  }

  console.log(datas);

  var timestamp = (datas.hasOwnProperty('timestamp')) ? datas.timestamp : NaN;

  //handling can Bullshit
  if (datas.hasOwnProperty('CAN')) {
    var can = datas.CAN;
    for (var signals in can) {
      if (can.hasOwnProperty(signals)) {
        messages = can[signals]
        for (var name in messages) {
          if (messages.hasOwnProperty(name)) {
            //create graph or just update it
            if (CARDS.indexOf(name) >= 0) {
              updateCard(name, messages[name]);
            } else if (name == 'RPM' || name == 'Speed') {
              if (messages.hasOwnProperty('RPM') && messages.hasOwnProperty('Speed')) {
                if (!ALL_MESSAGES.hasOwnProperty('RPM') && !ALL_MESSAGES.hasOwnProperty('Speed')) {
                  createGraphMultiplePlots(['RPM', 'Speed'], [messages['RPM'], messages['Speed']], timestamp);
                } else {
                  updateGraphMultiplePlots(['RPM', 'Speed'], [messages['RPM'], messages['Speed']], timestamp);
                }
              }
            } else {
              if (!ALL_MESSAGES.hasOwnProperty(name)) {
                createGraph(name, messages[name], timestamp);
              } else {
                updateGraph(name, messages[name], timestamp);
              }
            }
          }
        }
      }
    }
  }

  //handling gps
  if (datas.hasOwnProperty('GPS')) {
    var gps = datas.GPS;
    for (key in gps) {
      if (gps.hasOwnProperty(key)) {
        if (!ALL_MESSAGES.hasOwnProperty(key)) {
          createGraph(key, gps[key], timestamp)
        } else {
          updateGraph(key, gps[key], timestamp);
        }
      }
    }
  }
  //hnadling imu
}

function createGraph(name, value, timestamp) {
  var layout = {
    title: name,
    xaxis: {
      title: 'Temps',
      showgrid: true,
      zeroline: true
    },
    yaxis: {
      title: '',
      showline: false
    },
  };

  var data = [{
    x: [timestamp],
    y: [value],
    type: 'scatter'
  }];
  ALL_MESSAGES[name] = data;

  var mainContainer = document.getElementById('mainContent');

  var newplotdiv = document.createElement('div');
  newplotdiv.id = name;
  newplotdiv.classList.add("control-panel");

  mainContainer.appendChild(newplotdiv);

  appendToGraphList(name);

  Plotly.newPlot(name, ALL_MESSAGES[name], layout, {responsive: true});
}

function updateGraph(name, value, timestamp) {
  ALL_MESSAGES[name][0].x.push(timestamp);
  ALL_MESSAGES[name][0].y.push(value);
  Plotly.redraw(name);
}

function updateCard(name, value) {
  document.getElementById(name).innerHTML = value;
}


function createFullName(names) {
  var fullName = "";
  for (var name in names) {
    fullName += names[name] + " ";
  }
  return fullName;
}


function createGraphMultiplePlots(names, values, timestamp) {

  var fullName = createFullName(names);

  var layout = {
    title: fullName,
    xaxis: {
      title: 'Temps',
      showgrid: false,
      zeroline: true
    }
  };

  var count = 1;
  for (var i=0; i < names.length; i++) {
    if (count == 1) {
      layout["yaxis"] = {
        title: names[i],
        showline: false
      }
    } else {
      var key = "yaxis" + count;
      layout[key] = {
        title: names[i],
        showline: false,
        overlaying: 'y',
        side: 'right'
      }
    }
    count++;
  }

  console.log(layout);

  var data = [];
  var count = 1;
  for (var i=0; i < values.length; i++) {
    var d = {
      x: [timestamp],
      y: [values[i]],
      type: 'scatter',
      name: names[i]
    }
    if (count == 1) {
      d["yaxis"] = 'y1';
    } else {
      d["yaxis"] = 'y' + count;
    }
    count++;
    data.push(d);
  };

  for (var i=0; i < names.length; i++) {
    ALL_MESSAGES[names[i]] = [data[i]];
  }

  var mainContainer = document.getElementById('mainContent');

  var newplotdiv = document.createElement('div');
  newplotdiv.id = fullName;
  newplotdiv.classList.add("control-panel");

  mainContainer.appendChild(newplotdiv);

  appendToGraphList(fullName);

  Plotly.newPlot(fullName, data, layout, {responsive: true});
}


function appendToGraphList(id) {
  var liRef = document.createElement('li');
  var aRef = document.createElement('a');

  aRef.id = "a_" + id;
  aRef.innerHTML = id;
  aRef.style.color = "green";

  aRef.addEventListener("click", function(e) {
    var chart = document.getElementById(id);
    var button = document.getElementById( "a_" + id);
    if (chart.style.display == 'none') {
      chart.style.display = 'inline';
      button.style.color = "green";
    } else {
      chart.style.display = 'none';
      button.style.color = "red";
    }
  });

  document.getElementById('slide-out').appendChild(liRef);
  liRef.appendChild(aRef);
}


function updateGraphMultiplePlots(names, values, timestamp) {
  for (var i=0; i < names.length; i++) {
    var name = names[i];
    if (ALL_MESSAGES.hasOwnProperty(name)) {
      ALL_MESSAGES[name][0].x.push(timestamp);
      ALL_MESSAGES[name][0].y.push(values[i]);
    }
  }
  Plotly.redraw(createFullName(names));
}

function getIndexById(list, id) {
  for (var i=0; i < list.length; i++) {
    var dict = list[i];
    if (dict.hasOwnProperty(id)) {
      if (dict.name == id) {
        return i;
      }
    }
  }
  return -1;
}



main();
