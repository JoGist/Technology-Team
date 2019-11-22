'use strict';

var controllerName = 'Imu',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();

var flag = true;
var ImuController = function init(modules) {
  var router = modules.router;
  console.log('IMU CONTROLLER');
  var data = {};
  modules.io.on('connection', function (socket) {
	  	// console.log(socket);
		socket.on('data_sensors', function (data) {
			var obj = JSON.parse(data);
			socket.broadcast.emit('news', obj);
		});
		socket.on('command', function (data) {
			console.log(command);
			socket.broadcast.emit('command', JSON.stringify(data));
		});
		socket.on('task', function (data) {
			socket.broadcast.emit('task_rover', JSON.stringify(data));
		});
		socket.on('scan_distances_data_by_main', function (data) {
			var obj = JSON.parse(data);
			socket.broadcast.emit('scan_distances_data', obj);
		});
  });

  router.route('/' + controllerName)
    .get(function(req, res) {
		console.log('GET');
    	var sRC = new StructResultClient();
        var query = req.query;
		//console.log(options);
		PythonShell.run('imuData.py',options, function (err, results) {
			console.log(err, results);
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
