'use strict';

var controllerName = 'Imu',
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();
var PythonShell = require('python-shell');

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  scriptPath: '/home/pi/Desktop/Development/raspstudy/Server/Imu/python/',
  args: ['value1', 'value2', 'value3']
};


var ImuController = function init(modules) {
  var router = modules.router;
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
				//console.log(obj);
				sRC.jsonStruct.result = obj;
				sRC.jsonSendToClient(res);

			} else {
				res.sendStatus(500);
			}
		});

    })
}


module.exports = ImuController;
