'use strict';

var controllerName = 'Imu',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();
var PythonShell = require('python-shell');
	var optionsData = {
	  mode: 'text',
	  scriptPath: '/home/pi/development/raspstudy/Server/ai_rover/',
	  args: ['value1', 'value2', 'value3']
	};
	var optionsMotors = {
	    mode: 'text',
  	  	scriptPath: '/home/pi/development/raspstudy/Server/ai_rover/'
	};

	//INVIO solo di dati
	var pyshell = new PythonShell('rover_only_data.py',optionsData);

var net = require('net');
var client = new net.Socket();


var flag = true;
var ImuController = function init(modules) {
  var router = modules.router;
  console.log('IMU CONTROLLER');
  var request_data = true;
  modules.io.on('connection', function (socket) {
	if (request_data) {

		pyshell.on('message', function (data) {
			var obj = JSON.parse(data);
			// console.log(data);
			socket.emit('news', obj);
			// console.log(obj.accel);
			// optionsMotors.args = [obj];
			// // console.log(JSON.stringify(obj));
			// PythonShell.run('motors.py', optionsMotors, function (err, results) {
			//     if (err) throw err;
			//     // results is an array consisting of messages collected during execution
			//
			//     console.log('results: %j', results);
			// });

		});

		pyshell.end(function (err) {
		  if (err) ;
		  console.log('finished');
		});
	};
	// client.connect(9999, '127.0.0.1', function() {
	// 	console.log('Connected');
	// });
	//
	// client.on('data', function(data) {
	// 	console.log('Received: ' + data);
	// 	client.destroy(); // kill client after server's response
	// });
	//
	// client.on('close', function() {
	// 	console.log('Connection closed');
	// });
	// client.on('error', function() {
	// 	console.log('Connection error');
	// });
	// socket.on('info_imu', function (data) {
	// 	console.log(data);
	// 	client.connect(9999, '127.0.0.1', function() {
	// 		console.log('Connected');
	// 	});

	// });

	socket.on('motors', function (data) {
		console.log(data);
		// client.write('ciao');
		// client.on('data', function(data) {
		// 	console.log('Received: ' + data);
		// 	client.destroy(); // kill client after server's response
		// });
		//
		// client.on('close', function() {
		// 	console.log('Connection closed');
		// });
		// client.on('error', function() {
		// 	console.log('Connection error');
		// });
		// client.write(JSON.stringify(data));
	});
	socket.on('task', function (data) {
		if (data.typeTask == 'only_data') {
			console.log('only_data');
			pyshell = new PythonShell('rover_only_data.py',optionsData);

		    modules.io.on('connection', function (socket) {
				pyshell.on('message', function (data) {
					var obj = JSON.parse(data);
					// console.log(data);
					socket.emit('news', obj);
					// console.log(obj.accel);
					// optionsMotors.args = [obj];
					// // console.log(JSON.stringify(obj));
					// PythonShell.run('motors.py', optionsMotors, function (err, results) {
					//     if (err) throw err;
					//     // results is an array consisting of messages collected during execution
					//
					//     console.log('results: %j', results);
					// });

				});

				pyshell.end(function (err) {
				  if (err) ;
				  console.log('finished');
				});
			});
		}else if(data.typeTask == 'azimuth_zero'){
			console.log('azimuth_zero');
		}else if(data.typeTask == 'distance'){
			console.log('distance');
		}
	});
  });

  router.route('/' + controllerName)
    .get(function(req, res) {
		console.log('GET');
    	var sRC = new StructResultClient();
        var query = req.query;
		//console.log(options);
		PythonShell.run('imuData.py',options, function (err, results) {
			// console.log(err, results);
			if (!err && results && results.length === 1) {
				var values = results[0];
				var obj = JSON.parse(values);
				// console.log(obj);
				sRC.jsonStruct.result = obj;
				sRC.jsonSendToClient(res);

			} else {
				res.sendStatus(500);
			}
		});

    })
}


module.exports = ImuController;
