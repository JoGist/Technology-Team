'use strict';

var controllerName = 'Gyroscope',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();
var PythonShell = require('python-shell');

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  scriptPath: '/home/pi/Desktop/Development/raspstudy/Server/Imu/python/',
  args: ['value1', 'value2', 'value3']
};


var GyroscopeController = function init(modules) {
  var router = modules.router;
  router.route('/' + controllerName)
    .get(function(req, res) {
    	console.log('GET');
    	var sRC = new StructResultClient();
        var query = req.query;

        PythonShell.run('g.py', options, function (err, results) {
			if (!err && results && results.length === 1) {
				var values = results[0].split('/');

				var gyroscope = {
					roll: values[0],
					pitch: values[1],
					yaw: values[2]
				}
				
				sRC.jsonStruct.result = gyroscope;
				sRC.jsonSendToClient(res);

		  	} else {
				res.sendStatus(500);
		  	}
        });
    	// if (query) {
        //
        //
    	// } else {
    	// 	res.sendStatus(400);
    	// }
    })
}


module.exports = GyroscopeController;
