'use strict';

var controllerName = 'Leds',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();
var gpio = require("pi-gpio");

var gpioPin =13;
var ledsPin = {
	green:13,
	yellow:12,
	red:11
};
for (var key in ledsPin){
	gpioPin = ledsPin[key];
	gpio.open(gpioPin, "output", function(err) {
		var on = 1;
	});
	gpio.read(gpioPin, function(err, value){
	});
}
var LedsController = function init(modules) {
  var router = modules.router;
  router.route('/' + controllerName)
	.post(function (req, res) {
    	console.log('POST');

		var sRC = new StructResultClient();
		var body = req.body;
		if (body && (body.color === 'green' || body.color === 'yellow' || body.color === 'red')) {
			gpioPin = ledsPin[body.color];
			gpio.read(gpioPin, function(err, value){
				//console.log(err,value, value === '0');
				if(value === 0){
					gpio.write(gpioPin, 1);
				} else {
					gpio.write(gpioPin, 0);
				}
			});
			res.sendStatus(200);
		} else {
			res.sendStatus(400);
		}
    })

    .get(function(req, res) {
    	console.log('GET');
    	console.log(gpio.read);

		var sRC = new StructResultClient();
    	var query = req.query;
    	console.log(ledsPin.green);
		gpio.read(ledsPin.green,function(err, value){
			console.log(err,value);
		});
		if (query && (query.color === 'green' || query.color === 'yellow' || query.color === 'red')) {
	    		gpioPin = ledsPin[query.color];
			gpio.read(gpioPin, function(err, value){
				sRC.jsonStruct.result = value;
				sRC.jsonSendToClient(res);
			});
		} else {
			res.sendStatus(400);
		}
    })
}


module.exports = LedsController;
