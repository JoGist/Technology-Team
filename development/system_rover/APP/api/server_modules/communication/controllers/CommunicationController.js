 'use strict';

var controllerName = 'Imu',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();

var flag = true;
var CommunicationController = function init(modules) {
  var router = modules.router;
  console.log('COMMUNICATION CONTROLLER');
  var data = {};
  modules.io.on('connection', function (socket) {
		socket.on('data_sensors', function (data) {
			var obj = JSON.parse(data);
			socket.broadcast.emit('news', obj);
		});
		socket.on('command', function (data) {
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
}

module.exports = CommunicationController;
